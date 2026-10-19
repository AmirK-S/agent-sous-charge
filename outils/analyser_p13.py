"""Analyse de P1.3 : taille des conversations τ³ banking, vue depuis l'agent.

Pour chaque conversation : note, tours, recherches, tokens du contexte de l'agent au premier et au dernier tour
(le dernier = place prise dans le cache KV au pire moment), tokens traités en tout, durée.
Puis l'occupation du cache KV relevée sur vLLM toutes les 5 s.

Usage : python3 -I outils/analyser_p13.py <results.json> [<metriques-p1-3.txt>]
"""
import json
import statistics
import sys

KV_TOKENS_L40S = 97_712  # mesuré le 18/10 et le 19/10 (vLLM 0.32, FP8, 0,92 de la mémoire)


def n(x):
    """Nombre à la française : 10 233."""
    return f"{x:,.0f}".replace(",", " ")


def conversations(chemin):
    d = json.load(open(chemin))
    for s in d["simulations"]:
        agent = [m for m in s["messages"] if m.get("role") == "assistant" and m.get("usage")]
        appels = [t["name"] for m in s["messages"] if m.get("role") == "assistant" for t in (m.get("tool_calls") or [])]
        contextes = [m["usage"]["prompt_tokens"] + m["usage"]["completion_tokens"] for m in agent]
        yield {
            "tache": s["task_id"],
            "note": (s.get("reward_info") or {}).get("reward"),
            "messages": len(s["messages"]),
            "tours_agent": len(agent),
            "recherches": sum(1 for a in appels if a.startswith("KB_search")),
            "outils": len(appels),
            "contexte_debut": contextes[0] if contextes else 0,
            "contexte_max": max(contextes) if contextes else 0,
            "tokens_traites": sum(m["usage"]["prompt_tokens"] for m in agent),
            "tokens_generes": sum(m["usage"]["completion_tokens"] for m in agent),
            "duree_s": round(s.get("duration") or 0),
            "fin": s.get("termination_reason"),
        }


def metriques(chemin):
    kv, en_cours = [], []
    for ligne in open(chemin):
        champs = dict(p.rsplit(" ", 1) for p in ligne.split(" vllm:")[1:] if " " in p)
        for cle, val in champs.items():
            if cle.startswith(("kv_cache_usage_perc", "gpu_cache_usage_perc")):
                kv.append(float(val))
            elif cle.startswith("num_requests_running"):
                en_cours.append(float(val))
    return kv, en_cours


def main():
    lignes = list(conversations(sys.argv[1]))
    print("| Tâche | Note | Messages | Recherches | Outils | Contexte au 1er tour | Contexte max | Tokens traités | Durée (s) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c in lignes:
        print(f"| {c['tache']} | {c['note']} | {c['messages']} | {c['recherches']} | {c['outils']} | "
              f"{n(c['contexte_debut'])} | {n(c['contexte_max'])} | {n(c['tokens_traites'])} | {c['duree_s']} |")
    maxs = [c["contexte_max"] for c in lignes]
    med = statistics.median(maxs)
    print()
    print(f"- Conversations : {len(lignes)} ; réussite : {sum(1 for c in lignes if c['note'] == 1.0)}/{len(lignes)}")
    print(f"- Contexte max par conversation : médiane {n(med)}, min {n(min(maxs))}, max {n(max(maxs))} tokens")
    print(f"- Conversations tenant à la fois dans {n(KV_TOKENS_L40S)} tokens de cache, au pire moment de chacune : "
          f"{KV_TOKENS_L40S / med:.1f} avec la médiane, {KV_TOKENS_L40S / max(maxs):.1f} avec la plus longue")
    if len(sys.argv) > 2:
        kv, en_cours = metriques(sys.argv[2])
        if kv:
            pic = max(kv)
            print(f"- Cache KV relevé (toutes les 5 s, {len(kv)} relevés) : pic {pic * 100:.1f} %, "
                  f"moyenne {statistics.mean(kv) * 100:.1f} % ; requêtes en cours au plus : {max(en_cours or [0]):.0f}")


if __name__ == "__main__":
    main()
