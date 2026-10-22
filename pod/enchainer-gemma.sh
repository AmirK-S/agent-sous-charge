#!/usr/bin/env bash
# Nuit du 22/10 : après les paliers (processus donné), le repos de Gemma 4 31B (40 tâches × 4 essais).
# Le premier enchaînement s'était tué lui-même : « pkill -f "vllm serve" » visait aussi sa propre ligne
# de commande, qui contenait ce texte. Ici, on vise le processus par son motif [v]llm, qui ne se trouve pas lui-même.
# Usage : bash enchainer-gemma.sh <pid à attendre>
set -uo pipefail
W="$HOME/workspace"; P="$W/agent-sous-charge"
while kill -0 "$1" 2> /dev/null; do sleep 30; done
echo "paliers terminés : $(date -u +%H:%M:%S)"
pkill -f "[v]llm serve" || true; sleep 15
(setsid nohup env W="$W" bash "$P/pod/servir-gemma.sh" > /dev/null 2>&1 < /dev/null &)
debut=$(date +%s)
until curl -sf localhost:8000/v1/models > /dev/null; do
  sleep 10; [ $(( $(date +%s) - debut )) -lt 1500 ] || { echo "vLLM (Gemma) absent"; tail -20 "$W/vllm-gemma.log"; exit 1; }
done
echo "Gemma prêt en $(( $(date +%s) - debut )) s ; début du repos : $(date -u +%H:%M:%S)"
timeout 3h env W="$W" bash "$P/pod/jouer-repos.sh" p0-repos-gemma google/gemma-4-31B-it > /dev/null 2>&1
echo "fin du repos de Gemma : $(date -u +%H:%M:%S) (code $?)"
grep -E "Average Reward|Pass\^1" "$W/jouer-p0-repos-gemma.log" | tail -2
pkill -f "[v]llm serve"
echo "NUIT FINIE $(date -u +%H:%M:%S)"
