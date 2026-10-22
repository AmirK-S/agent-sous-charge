#!/usr/bin/env bash
# P0, partie 1 : réussite « au repos » sur les 40 tâches de développement, 4 essais chacune, pour un modèle.
# Agent servi par vLLM sur la machine ; outils par le serveur MCP de la banque (sur la machine) ;
# client simulé GPT-6 Luna par OpenRouter. 4 conversations à la fois (faible concurrence).
# Usage : bash jouer-repos.sh <nom_du_lot> <identifiant du modèle servi par vLLM>
set -euo pipefail
W="${W:-/workspace}"
LOT="$1"; MODELE="$2"
P="$W/agent-sous-charge"
set -a; source "$HOME/.openrouter.env"; set +a
TACHES=$(python3 -c "import json;print(' '.join(json.load(open('$P/donnees/partage-taches.json'))['developpement']))")

# Serveur MCP de la banque, sur la machine.
pkill -f mcp_banque.serveur || true
(cd "$P" && PYTHONPATH="$P" setsid nohup "$W/venv-tau/bin/python" -m mcp_banque.serveur --port 8765 \
   > "$W/serveur-mcp-$LOT.log" 2>&1 < /dev/null &)
until curl -s -o /dev/null http://127.0.0.1:8765/mcp; do sleep 1; done

cd "$W/tau2-bench"
PYTHONPATH="$P" "$W/venv-tau/bin/python" -m mcp_banque.tau2_mcp run \
  --domain banking_knowledge \
  --retrieval-config bm25 \
  --agent-llm "openai/$MODELE" \
  --agent-llm-args '{"temperature": 0.0, "api_base": "http://localhost:8000/v1", "api_key": "local"}' \
  --user-llm "openrouter/openai/gpt-6-luna" \
  --user-llm-args '{"temperature": 0.0}' \
  --task-ids $TACHES \
  --num-trials 4 \
  --max-concurrency 4 \
  --seed 300 \
  --auto-resume \
  --save-to "$LOT" \
  2>&1 | tee "$W/jouer-$LOT.log"
pkill -f mcp_banque.serveur || true
