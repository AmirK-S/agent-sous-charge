"""Serveur MCP de la banque (P1.4) : les outils banking_knowledge de τ³, à l'identique, derrière MCP.

Serveur à état : il tient une base bancaire par conversation, comme une banque tient ses données.
Chaque appel porte, dans son `_meta`, l'identifiant de sa conversation et qui appelle (agent ou client).
Aucune optimisation ici : P1.5 doit prouver zéro écart avec l'exécution directe dans τ³.

Lancement : python -m mcp_banque.serveur [--port 8765]
"""
import argparse
import threading
import uuid
from typing import Any

import anyio
import uvicorn
from mcp import types
from mcp.server.lowlevel import Server

from tau2.data_model.tasks import EnvFunctionCall, InitializationData
from tau2.domains.banking_knowledge.environment import get_environment
from tau2.environment.environment import Environment

CLE_CONVERSATION = "agent-sous-charge/conversation"
CLE_DEMANDEUR = "agent-sous-charge/demandeur"

# Outils de gestion de session, à côté des outils bancaires.
OUVRIR, ETAT, EMPREINTE, FERMER = "session_ouvrir", "session_etat_initial", "session_empreinte", "session_fermer"

conversations: dict[str, Environment] = {}
verrous: dict[str, threading.Lock] = {}


def _texte(contenu: str, erreur: bool = False) -> types.CallToolResult:
    return types.CallToolResult(content=[types.TextContent(type="text", text=contenu)], is_error=erreur)


def _catalogue() -> list[types.Tool]:
    """Les schémas tels que τ³ les génère (agent puis client), plus les outils de session."""
    modele = get_environment(retrieval_variant="bm25")
    outils = []
    for outil in modele.get_tools() + modele.get_user_tools():
        f = outil.openai_schema["function"]
        outils.append(types.Tool(name=f["name"], description=f.get("description", ""), input_schema=f["parameters"]))
    for nom, desc in [
        (OUVRIR, "Ouvre une conversation : crée sa base bancaire. Renvoie l'identifiant de conversation."),
        (ETAT, "Applique l'état initial d'une tâche (données et actions d'initialisation)."),
        (EMPREINTE, "Renvoie les empreintes (hash) des bases agent et client de la conversation."),
        (FERMER, "Ferme la conversation et libère sa base."),
    ]:
        outils.append(types.Tool(name=nom, description=desc, input_schema={"type": "object"}))
    return outils


def _executer(nom: str, args: dict[str, Any], meta: dict[str, Any]) -> types.CallToolResult:
    """Exécution synchrone, dans un fil à part : les outils τ³ sont du Python bloquant."""
    if nom == OUVRIR:
        cid = uuid.uuid4().hex
        conversations[cid] = get_environment(
            retrieval_variant=args.get("retrieval_variant"),
            retrieval_kwargs=args.get("retrieval_kwargs"),
            read_log_allowlist=set(args["read_log_allowlist"]) if args.get("read_log_allowlist") is not None else None,
        )
        verrous[cid] = threading.Lock()
        return _texte(cid)

    cid = meta.get(CLE_CONVERSATION)
    if cid not in conversations:
        return _texte(f"conversation inconnue : {cid}", erreur=True)
    env = conversations[cid]
    with verrous[cid]:
        if nom == ETAT:
            donnees = args.get("initialization_data")
            actions = args.get("initialization_actions")
            env.set_state(
                initialization_data=InitializationData.model_validate(donnees) if donnees else None,
                initialization_actions=[EnvFunctionCall.model_validate(a) for a in actions] if actions else None,
                message_history=[],
            )
            return _texte("ok")
        if nom == EMPREINTE:
            return _texte(f"{env.get_db_hash()}|{env.get_user_db_hash()}")
        if nom == FERMER:
            conversations.pop(cid, None)
            verrous.pop(cid, None)
            return _texte("ok")
        # Outil bancaire : même chemin que Environment.get_response, moins l'enveloppe d'erreur,
        # que le client remet à l'identique en relançant l'exception avec le même texte.
        try:
            resultat = env.make_tool_call(nom, requestor=meta.get(CLE_DEMANDEUR, "assistant"), **args)
            env.sync_tools()
        except Exception as e:  # noqa: BLE001 — le texte de l'exception fait partie de la réponse attendue
            return _texte(str(e), erreur=True)
        return _texte(Environment.to_json_str(resultat))


def creer_serveur() -> Server:
    catalogue = _catalogue()

    async def lister(ctx, params) -> types.ListToolsResult:
        return types.ListToolsResult(tools=catalogue)

    async def appeler(ctx, params: types.CallToolRequestParams) -> types.CallToolResult:
        meta = dict(params.meta or {})
        return await anyio.to_thread.run_sync(_executer, params.name, dict(params.arguments or {}), meta)

    return Server("banque-tau3", version="0.1.0", on_list_tools=lister, on_call_tool=appeler)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    app = creer_serveur().streamable_http_app(json_response=True, max_sessions=None)
    uvicorn.run(app, host="127.0.0.1", port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
