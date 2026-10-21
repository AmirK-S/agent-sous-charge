"""P1.5 · Test de fidélité : les 97 tâches banking_knowledge, en direct puis par MCP, sans modèle ni GPU.

Pour chaque tâche : même état initial des deux côtés, puis les actions de la solution officielle de τ³,
plus trois appels de contrôle (une recherche dans les documents, un outil inexistant, des arguments faux).
On compare chaque réponse d'outil telle que l'agent la verrait (contenu et drapeau d'erreur), puis les
empreintes finales des bases agent et client.

Seule normalisation : le pied de page `[Timing: ...]` de KB_search, qui change à chaque appel même en direct.

Usage, serveur lancé : python -m mcp_banque.fidelite [--paralleles 8] [--sortie mesures/P1.5.json]
"""
import argparse
import gc
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

from mcp_banque.client import connexion, constructeur
from tau2.data_model.message import ToolCall
from tau2.domains.banking_knowledge.environment import get_environment, get_tasks
from tau2.runner.build import _derive_read_log_allowlist

PIED_TIMING = re.compile(r"\n\n\[Timing: [^\]]*\]$")


def normaliser(texte: str) -> str:
    return PIED_TIMING.sub("", texte)


def appels(tache) -> list[ToolCall]:
    """Actions de la solution, puis trois appels de contrôle."""
    liste = [ToolCall(id=f"a{i}", name=a.name, arguments=dict(a.arguments or {}), requestor=a.requestor)
             for i, a in enumerate((tache.evaluation_criteria.actions if tache.evaluation_criteria else None) or [])]
    scenario = str(getattr(tache.user_scenario, "instructions", tache.user_scenario) or tache.id)
    requete = " ".join(scenario.split()[:12])
    liste += [
        ToolCall(id="c1", name="KB_search", arguments={"query": str(requete)}),
        ToolCall(id="c2", name="outil_qui_n_existe_pas", arguments={}),
        ToolCall(id="c3", name="get_user_information_by_id", arguments={"argument_faux": 1}),
    ]
    return liste


def jouer(tache, fabrique) -> dict:
    kwargs = {"retrieval_variant": "bm25", "task": tache, "read_log_allowlist": _derive_read_log_allowlist(tache)}
    env = fabrique(**kwargs)
    init = tache.initial_state
    env.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=[],
    )
    reponses, durees = [], []
    for appel in appels(tache):
        t0 = time.perf_counter()
        m = env.get_response(appel)
        durees.append(time.perf_counter() - t0)
        reponses.append({"outil": appel.name, "contenu": normaliser(m.content), "erreur": m.error})
    return {"reponses": reponses, "agent": env.get_db_hash(), "client": env.get_user_db_hash(), "durees": durees}


def comparer(tache, direct: dict, mcp: dict) -> list[str]:
    ecarts = []
    for i, (d, m) in enumerate(zip(direct["reponses"], mcp["reponses"])):
        if d != m:
            ecarts.append(f"{tache.id} appel {i} ({d['outil']}) : direct={d!r:.200} | mcp={m!r:.200}")
    if len(direct["reponses"]) != len(mcp["reponses"]):
        ecarts.append(f"{tache.id} : nombre d'appels différent")
    for cle in ("agent", "client"):
        if direct[cle] != mcp[cle]:
            ecarts.append(f"{tache.id} : empreinte {cle} différente")
    return ecarts


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--paralleles", type=int, default=8)
    p.add_argument("--sortie", default=None)
    a = p.parse_args()
    taches = get_tasks()
    print(f"{len(taches)} tâches")

    direct = {t.id: jouer(t, get_environment) for t in taches}
    nb_appels = sum(len(r["reponses"]) for r in direct.values())
    print(f"direct : {nb_appels} appels d'outils")

    resultats = {}
    for mode, paralleles in (("série", 1), ("parallèle", a.paralleles)):
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=paralleles) as pool:
            mcp = dict(zip([t.id for t in taches], pool.map(lambda t: jouer(t, constructeur), taches)))
        duree = time.perf_counter() - t0
        ecarts = [e for t in taches for e in comparer(t, direct[t.id], mcp[t.id])]
        lat = sorted(d for r in mcp.values() for d in r["durees"])
        lat_direct = sorted(d for r in direct.values() for d in r["durees"])
        resultats[mode] = {
            "paralleles": paralleles, "duree_s": round(duree, 1), "ecarts": ecarts,
            "latence_mcp_ms": {"mediane": round(lat[len(lat) // 2] * 1000, 2), "p99": round(lat[int(len(lat) * .99)] * 1000, 2)},
            "latence_direct_ms": {"mediane": round(lat_direct[len(lat_direct) // 2] * 1000, 2),
                                  "p99": round(lat_direct[int(len(lat_direct) * .99)] * 1000, 2)},
        }
        print(f"{mode} ({paralleles} à la fois) : {len(ecarts)} écart(s) sur {nb_appels} appels et {2 * len(taches)} empreintes, "
              f"{duree:.1f} s ; latence par appel MCP médiane {resultats[mode]['latence_mcp_ms']['mediane']} ms, "
              f"p99 {resultats[mode]['latence_mcp_ms']['p99']} ms (direct : {resultats[mode]['latence_direct_ms']['mediane']} ms)")
        for e in ecarts[:10]:
            print("  ", e)
        del mcp
        gc.collect()  # déclenche la fermeture des conversations côté serveur
        time.sleep(2)
        print(f"   conversations encore ouvertes sur le serveur : {connexion().appeler('session_compte', {}, {})[0]}")

    if a.sortie:
        json.dump({"taches": len(taches), "appels": nb_appels, "resultats": resultats}, open(a.sortie, "w"),
                  ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
