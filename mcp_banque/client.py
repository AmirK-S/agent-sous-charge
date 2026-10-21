"""Côté τ³ (P1.4) : un Environment dont les outils bancaires s'exécutent sur le serveur MCP.

Ce qui reste local : les schémas des outils (ce que voit le modèle), la politique, l'enveloppe
d'erreur et la sérialisation de `Environment.get_response`. Ce qui part au serveur : l'exécution
des outils, l'état initial de la tâche, et les empreintes de la base pour la notation.

τ³ est synchrone et multi-fils ; le client MCP est asynchrone. Une boucle asyncio dédiée tourne
dans un fil à part, avec une seule connexion MCP partagée par toutes les conversations.
"""
import asyncio
import os
import threading
import weakref
from typing import Any, Literal, Optional

from mcp import Client

from mcp_banque.serveur import CLE_CONVERSATION, CLE_DEMANDEUR, EMPREINTE, ETAT, FERMER, OUVRIR
from tau2.domains.banking_knowledge.environment import get_environment as get_environment_local
from tau2.environment.environment import Environment

URL = os.environ.get("BANQUE_MCP_URL", "http://127.0.0.1:8765/mcp")


class _Connexion:
    """Une boucle asyncio et un client MCP, partagés par tout le processus."""

    def __init__(self, url: str):
        self.boucle = asyncio.new_event_loop()
        threading.Thread(target=self.boucle.run_forever, daemon=True, name="mcp-banque").start()
        self.client = Client(url)
        self._attendre(self.client.__aenter__())

    def _attendre(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.boucle).result()

    def appeler(self, nom: str, arguments: dict[str, Any], meta: dict[str, Any]) -> tuple[str, bool]:
        r = self._attendre(self.client.call_tool(nom, arguments, meta=meta))
        return r.content[0].text, bool(r.is_error)

    def appeler_sans_attendre(self, nom: str, arguments: dict[str, Any], meta: dict[str, Any]) -> None:
        """Pour la fermeture depuis le ramasse-miettes : ne jamais bloquer (risque d'interblocage)."""
        if not self.boucle.is_closed():
            asyncio.run_coroutine_threadsafe(self.client.call_tool(nom, arguments, meta=meta), self.boucle)


_connexion: Optional[_Connexion] = None
_verrou = threading.Lock()


def connexion() -> _Connexion:
    global _connexion
    with _verrou:
        if _connexion is None:
            _connexion = _Connexion(URL)
    return _connexion


def _fermer(conversation: str) -> None:
    if _connexion is not None:
        _connexion.appeler_sans_attendre(FERMER, {}, {CLE_CONVERSATION: conversation})


class ErreurOutil(Exception):
    """Exception relancée côté client avec le texte exact de l'exception côté serveur."""


class EnvironnementMCP(Environment):
    def __init__(self, local: Environment, retrieval_variant, retrieval_kwargs, read_log_allowlist):
        self.__dict__.update(local.__dict__)  # schémas, politique, nom du domaine : identiques
        texte, erreur = connexion().appeler(OUVRIR, {
            "retrieval_variant": retrieval_variant,
            "retrieval_kwargs": retrieval_kwargs,
            "read_log_allowlist": sorted(read_log_allowlist) if read_log_allowlist is not None else None,
        }, {})
        if erreur:
            raise RuntimeError(f"ouverture de conversation refusée : {texte}")
        self.conversation = texte
        # τ³ n'a pas de fin de conversation explicite : on ferme quand il abandonne l'objet.
        weakref.finalize(self, _fermer, texte)

    def _appel(self, nom: str, arguments: dict[str, Any], demandeur: str = "assistant") -> tuple[str, bool]:
        return connexion().appeler(nom, arguments, {CLE_CONVERSATION: self.conversation, CLE_DEMANDEUR: demandeur})

    def make_tool_call(self, tool_name: str, requestor: Literal["user", "assistant"] = "assistant", **kwargs) -> Any:
        texte, erreur = self._appel(tool_name, kwargs, requestor)
        if erreur:
            raise ErreurOutil(texte)
        return texte

    def set_state(self, initialization_data, initialization_actions, message_history, strict: bool = True):
        texte, erreur = self._appel(ETAT, {
            "initialization_data": initialization_data.model_dump(mode="json") if initialization_data else None,
            "initialization_actions": [a.model_dump(mode="json") for a in initialization_actions] if initialization_actions else None,
        })
        if erreur:
            raise RuntimeError(f"état initial refusé : {texte}")
        # Le rejeu des appels passés reprend la logique de τ³ ; chaque appel rejoué part au serveur.
        super().set_state(None, None, message_history, strict=strict)

    def _empreintes(self) -> tuple[Optional[str], Optional[str]]:
        texte, _ = self._appel(EMPREINTE, {})
        agent, client = texte.split("|")
        return (None if agent == "None" else agent), (None if client == "None" else client)

    def get_db_hash(self) -> Optional[str]:
        return self._empreintes()[0]

    def get_user_db_hash(self) -> Optional[str]:
        return self._empreintes()[1]


def constructeur(solo_mode: bool = False, retrieval_variant=None, retrieval_kwargs=None,
                 read_log_allowlist=None, **kwargs) -> Environment:
    """Remplace get_environment de banking_knowledge dans le registre de τ³."""
    local = get_environment_local(solo_mode=solo_mode, retrieval_variant=retrieval_variant,
                                  retrieval_kwargs=retrieval_kwargs, read_log_allowlist=read_log_allowlist, **kwargs)
    return EnvironnementMCP(local, retrieval_variant, retrieval_kwargs, read_log_allowlist)


def _bm25_par_defaut(fabrique):
    """`tau2 evaluate-trajs` ne relit pas la configuration de recherche enregistrée et retombe sur
    `alltools` (embeddings OpenAI). On impose `bm25`, celle de nos conversations."""
    def fabrique_bm25(**kwargs):
        if kwargs.get("retrieval_variant") is None:
            kwargs["retrieval_variant"] = "bm25"
        return fabrique(**kwargs)
    return fabrique_bm25


def brancher(par_mcp: bool = True) -> None:
    """Fait passer banking_knowledge par MCP (ou le laisse en direct), partout où τ³ construit l'environnement."""
    from tau2.registry import registry
    registry._domains["banking_knowledge"] = _bm25_par_defaut(constructeur if par_mcp else get_environment_local)
