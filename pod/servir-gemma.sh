#!/usr/bin/env bash
# Sert Gemma 4 31B (instruction) en FP8 avec appels d'outils, sur le port 8000.
# Réglages de la recette officielle de vLLM (vllm-project/recipes, Google/Gemma4.md) : analyseurs gemma4,
# gabarit d'outils de vLLM 0.32.0 (copié dans pod/). Mode réflexion désactivé (défaut du gabarit) :
# même terrain que Mistral Small 3.2, qui n'en a pas (décision provisoire du 22/10).
# Contexte limité à 32 768 tokens : sur L40S, Gemma 31B en FP8 ne laisse que 7,18 Gio de cache KV, soit
# 33 792 tokens au plus (vLLM refuse 65 536 ; nuit du 22/10). Valeur de la recette officielle de vLLM.
set -euo pipefail
W="${W:-/workspace}"
export HF_HOME="$W/hf"
export HF_HUB_OFFLINE=1
source "$W/venv/bin/activate"
ICI="$(cd "$(dirname "$0")" && pwd)"

vllm serve google/gemma-4-31B-it \
  --revision 842da3794eaa0b77d5f08bae87a17459d91ff475 \
  --quantization fp8 \
  --enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4 \
  --chat-template "$ICI/tool_chat_template_gemma4.jinja" \
  --limit-mm-per-prompt '{"image":0,"audio":0}' \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.92 \
  --enable-prefix-caching \
  --port 8000 \
  2>&1 | tee "$W/vllm-gemma.log"
