"""Partage des 97 tâches banking_knowledge en 40 de développement et 57 de confirmation.

Tirage à graine fixe, stratifié par nombre d'actions attendues (proxy de difficulté),
pour que les deux lots aient la même difficulté. Décidé avec Amir le 19/10 (P1).

Usage : python3 -I outils/partager_taches.py <tasks.json au commit 96a3ef92> donnees/partage-taches.json
"""
import hashlib
import json
import random
import sys

GRAINE = 20261019  # date du tirage ; fixée avant de regarder le résultat
N_DEV = 40
N_STRATES = 5      # quintiles du nombre d'actions attendues


def main(source, sortie):
    brut = open(source, "rb").read()
    taches = json.loads(brut)
    actions = {t["id"]: len((t.get("evaluation_criteria") or {}).get("actions") or []) for t in taches}

    # Strates : tâches triées par difficulté puis par id, découpées en parts presque égales.
    ordre = sorted(actions, key=lambda i: (actions[i], i))
    taille = len(ordre) / N_STRATES
    strates = [ordre[round(k * taille):round((k + 1) * taille)] for k in range(N_STRATES)]

    # Quota de développement par strate, au prorata, au plus fort reste pour tomber sur 40.
    exacts = [N_DEV * len(s) / len(ordre) for s in strates]
    quotas = [int(x) for x in exacts]
    for k in sorted(range(N_STRATES), key=lambda k: exacts[k] - quotas[k], reverse=True)[:N_DEV - sum(quotas)]:
        quotas[k] += 1

    rng = random.Random(GRAINE)
    dev = []
    for s, q in zip(strates, quotas):
        dev += rng.sample(sorted(s), q)
    dev = sorted(dev)
    conf = sorted(i for i in ordre if i not in set(dev))

    def resume(ids):
        n = sorted(actions[i] for i in ids)
        return {"taches": len(ids), "actions_moyenne": round(sum(n) / len(n), 2), "actions_mediane": n[len(n) // 2], "actions_max": n[-1]}

    json.dump({
        "source": "sierra-research/tau2-bench@96a3ef92329baf908ffe9dfe188cea34e8701d2a data/tau2/domains/banking_knowledge/tasks.json",
        "sha256_source": hashlib.sha256(brut).hexdigest(),
        "graine": GRAINE,
        "methode": f"stratifié par nombre d'actions attendues, {N_STRATES} strates, quotas au prorata",
        "developpement": dev,
        "confirmation": conf,
        "resume": {"developpement": resume(dev), "confirmation": resume(conf)},
    }, open(sortie, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"developpement": resume(dev), "confirmation": resume(conf)}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
