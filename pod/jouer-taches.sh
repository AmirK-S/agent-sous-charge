#!/usr/bin/env bash
# Joue des tâches banking_knowledge : agent = Mistral Small 3.2 servi par vLLM sur le pod,
# client simulé = GPT-6 Luna par OpenRouter. Une conversation à la fois (P1 : pas de charge).
# Usage, sur le pod : bash jouer-taches.sh <nom_du_lot> task_004 [task_005 ...]
# Ne jouer que des tâches de développement (donnees/partage-taches.json).
set -euo pipefail
W="${W:-/workspace}"   # surchargé par SkyPilot (W=$HOME/workspace) hors RunPod
LOT="$1"; shift
set -a; source "$HOME/.openrouter.env"; set +a
cd "$W/tau2-bench"

"$W/venv-tau/bin/tau2" run \
  --domain banking_knowledge \
  --retrieval-config bm25 \
  --agent-llm "openai/mistralai/Mistral-Small-3.2-24B-Instruct-2506" \
  --agent-llm-args '{"temperature": 0.0, "api_base": "http://localhost:8000/v1", "api_key": "local"}' \
  --user-llm "openrouter/openai/gpt-6-luna" \
  --user-llm-args '{"temperature": 0.0}' \
  --task-ids "$@" \
  --num-trials 1 \
  --max-concurrency 1 \
  --seed 300 \
  --save-to "$LOT" \
  2>&1 | tee "$W/jouer-$LOT.log"
