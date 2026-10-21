"""P1.7 (côté banque) · Abandon d'une conversation en pleine rafale d'écritures.

8 fils appellent `log_verification` en boucle (chaque appel ajoute une ligne à la base) ; au bout de
0,3 s, le client abandonne la conversation ; les fils continuent 0,3 s. On vérifie :
1. tout appel parti après l'accusé de réception de l'abandon est refusé, sans exécution ;
2. la base de la conversation contient exactement les écritures confirmées au client, ni plus ni moins :
   on rejoue ces seules écritures sur une base neuve, en direct, et les empreintes doivent être égales.

Usage, serveur lancé : python -m mcp_banque.abandon [--repetitions 5]
"""
import argparse
import itertools
import threading
import time

from mcp_banque.client import EnvironnementMCP, connexion, constructeur
from mcp_banque.serveur import ABANDONNER, CLE_CONVERSATION
from tau2.data_model.message import ToolCall
from tau2.domains.banking_knowledge.environment import get_environment, get_tasks

ARGS = {"name": "Wei Chen", "user_id": "76ad9cc60e", "address": "88 Harbor View Court, Boston, MA 02110",
        "email": "wei.chen.boston@gmail.com", "phone_number": "617-555-0834", "date_of_birth": "04/17/1979"}


def ecriture(i: int) -> ToolCall:
    h, reste = divmod(i, 3600)
    m, s = divmod(reste, 60)
    return ToolCall(id=f"w{i}", name="log_verification",
                    arguments={**ARGS, "time_verified": f"2025-11-{14 + h:02d} {m // 60:02d}:{m % 60:02d}:{s:02d} EST"})


def initialiser(env, tache):
    init = tache.initial_state
    env.set_state(initialization_data=init.initialization_data if init else None,
                  initialization_actions=init.initialization_actions if init else None, message_history=[])


def essai(tache) -> dict:
    env: EnvironnementMCP = constructeur(retrieval_variant="bm25", task=tache)
    initialiser(env, tache)
    compteur, arret, journal, verrou = itertools.count(), threading.Event(), [], threading.Lock()
    abandon_confirme = [None]

    def ecrire():
        while not arret.is_set():
            i = next(compteur)
            depart = time.monotonic()
            m = env.get_response(ecriture(i))
            with verrou:
                journal.append((i, depart, m.error, m.content))

    fils = [threading.Thread(target=ecrire) for _ in range(8)]
    for f in fils:
        f.start()
    time.sleep(0.3)
    connexion().appeler(ABANDONNER, {}, {CLE_CONVERSATION: env.conversation})
    abandon_confirme[0] = time.monotonic()
    time.sleep(0.3)
    arret.set()
    for f in fils:
        f.join()

    reussies = sorted(i for i, _, err, contenu in journal if not err and contenu.startswith("Verification logged"))
    apres = [(i, err, contenu) for i, depart, err, contenu in journal if depart > abandon_confirme[0]]
    fuites = [x for x in apres if not x[1]]

    temoin = get_environment(retrieval_variant="bm25", task=tache)
    initialiser(temoin, tache)
    for i in reussies:
        temoin.get_response(ecriture(i))
    return {
        "appels": len(journal), "ecritures_confirmees": len(reussies), "appels_apres_abandon": len(apres),
        "ecritures_apres_abandon": len(fuites),
        "empreinte_egale": env.get_db_hash() == temoin.get_db_hash(),
        "refus": apres[0][2] if apres else None,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repetitions", type=int, default=5)
    a = p.parse_args()
    tache = next(t for t in get_tasks() if t.id == "task_010")
    ok = True
    for n in range(a.repetitions):
        r = essai(tache)
        ok &= r["ecritures_apres_abandon"] == 0 and r["empreinte_egale"] and r["appels_apres_abandon"] > 0
        print(f"essai {n + 1} : {r['appels']} appels, {r['ecritures_confirmees']} écritures confirmées, "
              f"{r['appels_apres_abandon']} appels après l'abandon dont {r['ecritures_apres_abandon']} exécutés ; "
              f"base = écritures confirmées : {'oui' if r['empreinte_egale'] else 'NON'}")
    print("refus renvoyé :", r["refus"])
    print("RÉSULTAT :", "réussi" if ok else "ÉCHEC")


if __name__ == "__main__":
    main()
