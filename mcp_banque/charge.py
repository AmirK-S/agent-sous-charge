"""P0 · Générateur de charge : des clients simulés qui arrivent au rythme voulu, en escalier continu.

- Arrivées : processus de Poisson (intervalles exponentiels) de débit λ conversations/minute, tirés
  d'avance avec une graine ; tâches tirées par permutations de l'ensemble de développement.
- Escalier continu (G4, 22/10) : les paliers s'enchaînent sans vider ; seules les conversations
  commencées pendant la fenêtre de mesure d'un palier lui sont attribuées.
- Temps de réflexion (G4) : « réaliste » = lecture de la réponse de l'agent à 238 mots/min + frappe du
  message à 36 mots/min + pause uniforme 2 à 5 s ; « presse » = uniforme 5 à 20 s ; « aucun » = 0.
- Mesures par conversation : note τ³, fin, et chaque tour [instant de début, durée] (du message du client
  à la réponse finale de l'agent, outils compris). Mesures par palier : histogrammes vLLM (premier token, temps par token),
  relevés au début et à la fin de la fenêtre.
- Limite connue (pilote) : la patience de 30 s est comptée après coup (tours trop longs = abandons),
  sans couper réellement la conversation.

Usage, serveur MCP et vLLM lancés :
  python -m mcp_banque.charge --modele mistralai/Mistral-Small-3.2-24B-Instruct-2506 \
     --paliers 2,4,8 --minutes 10 --reflexion realiste --sortie charge.jsonl
"""
import argparse
import json
import os
import random
import re
import threading
import time
import urllib.request

import litellm

# Une conversation sur 8 a perdu la clé OpenRouter dans un fil (essai du 22/10, « api_key must be set »).
# On la donne à LiteLLM au niveau global, jamais dans la configuration (elle finirait dans les résultats).
litellm.openrouter_key = os.environ.get("OPENROUTER_API_KEY")

from mcp_banque.client import brancher

brancher()

from tau2.agent.llm_agent import LLMAgent  # noqa: E402
from tau2.data_model.simulation import TextRunConfig  # noqa: E402
from tau2.domains.banking_knowledge.environment import get_tasks  # noqa: E402
from tau2.runner.batch import run_single_task  # noqa: E402
from tau2.user.user_simulator import UserSimulator  # noqa: E402

LECTURE_MPM, FRAPPE_MPM = 238, 36
_local = threading.local()  # état de la conversation du fil courant
MODE_REFLEXION = "realiste"
T0 = [time.monotonic()]  # début de la séance, fixé dans main()


def _mots(texte) -> int:
    return len((texte or "").split())


def temps_reflexion(rng: random.Random, reponse_agent: str, message_client: str) -> float:
    if MODE_REFLEXION == "aucun":
        return 0.0
    if MODE_REFLEXION == "presse":
        return rng.uniform(5, 20)
    return _mots(reponse_agent) / LECTURE_MPM * 60 + _mots(message_client) / FRAPPE_MPM * 60 + rng.uniform(2, 5)


def _instrumenter() -> None:
    gen_client = UserSimulator.generate_next_message
    gen_agent = LLMAgent.generate_next_message

    def client(self, message, state):
        msg, state = gen_client(self, message, state)
        c = getattr(_local, "conv", None)
        if c is not None and not msg.is_tool_call():
            pause = temps_reflexion(c["rng"], getattr(message, "content", "") or "", msg.content or "")
            c["reflexion"].append(round(pause, 2))
            time.sleep(pause)
            c["debut_tour"] = time.monotonic()  # le client envoie son message
        return msg, state

    def agent(self, message, state):
        msg, state = gen_agent(self, message, state)
        c = getattr(_local, "conv", None)
        if c is not None and not msg.is_tool_call() and c.get("debut_tour") is not None:
            # Tour horodaté (secondes depuis le début de la séance) : avec l'escalier continu, un tour se
            # range dans la fenêtre de temps où il a eu lieu, pas dans le palier où sa conversation a commencé.
            c["tours"].append([round(c["debut_tour"] - T0[0], 1), round(time.monotonic() - c["debut_tour"], 3)])
            c["debut_tour"] = None
        return msg, state

    UserSimulator.generate_next_message = client
    LLMAgent.generate_next_message = agent


def lire_histogrammes(url: str) -> dict:
    """Compteurs cumulés des histogrammes vLLM utiles à G6 (premier token, temps par token)."""
    try:
        texte = urllib.request.urlopen(f"{url}/metrics", timeout=10).read().decode()
    except Exception:  # noqa: BLE001
        return {}
    h = {}
    for nom in ("time_to_first_token_seconds", "inter_token_latency_seconds", "request_time_per_output_token_seconds",
                "e2e_request_latency_seconds"):
        seaux = re.findall(rf'^vllm:{nom}_bucket\{{[^}}]*le="([^"]+)"[^}}]*\}} ([0-9.e+]+)', texte, re.M)
        if seaux:
            h[nom] = {le: float(v) for le, v in seaux}
    return h


def quantile_histo(avant: dict, apres: dict, q: float):
    """Quantile approché d'un histogramme cumulé sur la fenêtre (apres - avant)."""
    if not apres:
        return None
    bornes = sorted(apres, key=lambda le: float("inf") if le == "+Inf" else float(le))
    total = apres["+Inf"] - avant.get("+Inf", 0)
    if total <= 0:
        return None
    for le in bornes:
        if apres[le] - avant.get(le, 0) >= q * total:
            return float("inf") if le == "+Inf" else float(le)
    return None


def main() -> None:
    global MODE_REFLEXION
    p = argparse.ArgumentParser()
    p.add_argument("--modele", required=True)
    p.add_argument("--api", default="http://localhost:8000/v1")
    p.add_argument("--agent-llm", default=None, help="remplace openai/<modele> (essais sur OpenRouter)")
    p.add_argument("--client-llm", default="openrouter/openai/gpt-6-luna")
    p.add_argument("--paliers", default="2,4,8", help="débits en conversations/minute")
    p.add_argument("--minutes", type=float, default=10, help="durée de chaque palier")
    p.add_argument("--reflexion", choices=["realiste", "presse", "aucun"], default="realiste")
    p.add_argument("--graine", type=int, default=2026)
    p.add_argument("--sortie", default="charge.jsonl")
    p.add_argument("--vidage-max-min", type=float, default=20, help="attente max des dernières conversations")
    a = p.parse_args()
    MODE_REFLEXION = a.reflexion
    _instrumenter()

    dev = json.load(open("donnees/partage-taches.json"))["developpement"]
    taches = {t.id: t for t in get_tasks() if t.id in set(dev)}
    rng = random.Random(a.graine)
    api_vllm = a.api.rsplit("/v1", 1)[0]

    config = TextRunConfig(
        domain="banking_knowledge", retrieval_config="bm25", task_ids=dev, num_trials=1,
        agent="llm_agent", llm_agent=a.agent_llm or f"openai/{a.modele}",
        llm_args_agent={"temperature": 0.0} if a.agent_llm else {"temperature": 0.0, "api_base": a.api, "api_key": "local"},
        user="user_simulator", llm_user=a.client_llm, llm_args_user={"temperature": 0.0},
        max_concurrency=1000, seed=a.graine,
    )

    # Calendrier tiré d'avance : (instant, palier, tâche, graine de conversation).
    calendrier, t, ordre = [], 0.0, []
    for i, debit in enumerate(float(x) for x in a.paliers.split(",")):
        fin = (i + 1) * a.minutes * 60
        while True:
            t += rng.expovariate(debit / 60)
            if t >= fin:
                t = fin
                break
            if not ordre:
                ordre = list(dev)
                rng.shuffle(ordre)
            calendrier.append((t, i, ordre.pop(), rng.randrange(1 << 30)))
    print(f"{len(calendrier)} conversations prévues sur {len(a.paliers.split(','))} paliers de {a.minutes} min "
          f"(réflexion : {a.reflexion})", flush=True)

    verrou, sortie = threading.Lock(), open(a.sortie, "w")
    histos, en_cours = {}, [0]

    def jouer(instant, palier, tache_id, graine):
        _local.conv = {"rng": random.Random(graine), "reflexion": [], "tours": [], "debut_tour": None}
        debut = time.monotonic()
        with verrou:
            en_cours[0] += 1
        try:
            sim = run_single_task(config, taches[tache_id], seed=graine)
            note = (sim.reward_info.reward if sim.reward_info else None)
            fin_raison = str(sim.termination_reason)
        except Exception as e:  # noqa: BLE001
            # Panne d'authentification ou de fournisseur = instrument (à rejouer) ; le reste = système (compte 0).
            instrument = any(m in repr(e) for m in ("AuthenticationError", "RateLimitError", "openrouter"))
            note, fin_raison = (None if instrument else 0.0), f"{'instrument' if instrument else 'systeme'}: {e!r:.200}"
        c = _local.conv
        ligne = {"palier": palier, "tache": tache_id, "prevu_s": round(instant, 1), "debut_s": round(debut - t0, 1),
                 "duree_s": round(time.monotonic() - debut, 1), "note": note, "fin": fin_raison,
                 "tours_s": c["tours"], "reflexion_s": c["reflexion"]}
        with verrou:
            en_cours[0] -= 1
            sortie.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            sortie.flush()

    t0 = time.monotonic()
    T0[0] = t0
    fils, prochain_palier = [], 0
    for instant, palier, tache_id, graine in calendrier:
        while palier >= prochain_palier:  # bornes de palier : relevé des histogrammes vLLM
            histos[prochain_palier] = (time.monotonic() - t0, lire_histogrammes(api_vllm))
            print(f"palier {prochain_palier} : début à {histos[prochain_palier][0]:.0f} s, {en_cours[0]} conversations en cours", flush=True)
            prochain_palier += 1
        attente = instant - (time.monotonic() - t0)
        if attente > 0:
            time.sleep(attente)
        f = threading.Thread(target=jouer, args=(instant, palier, tache_id, graine), daemon=True)
        f.start()
        fils.append(f)
    histos[prochain_palier] = (time.monotonic() - t0, lire_histogrammes(api_vllm))
    print(f"fin des arrivées à {histos[prochain_palier][0]:.0f} s ; vidage des {en_cours[0]} conversations en cours", flush=True)
    limite = time.monotonic() + a.vidage_max_min * 60
    for f in fils:
        f.join(timeout=max(0, limite - time.monotonic()))

    # Latences vLLM par palier (quantiles approchés des histogrammes sur chaque fenêtre).
    resume = []
    for i in range(prochain_palier):
        (_, av), (_, ap) = histos[i], histos[i + 1]
        resume.append({"palier": i,
                       "ttft_p99_s": quantile_histo(av.get("time_to_first_token_seconds", {}), ap.get("time_to_first_token_seconds", {}), .99),
                       "itl_p99_s": quantile_histo(av.get("inter_token_latency_seconds", {}), ap.get("inter_token_latency_seconds", {}), .99)})
    sortie.write(json.dumps({"resume_vllm": resume, "paliers": a.paliers, "minutes": a.minutes,
                             "reflexion": a.reflexion}, ensure_ascii=False) + "\n")
    sortie.close()
    print(json.dumps(resume, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
