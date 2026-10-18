#!/usr/bin/env bash
# Sert Mistral Small 3.2 en FP8 avec appels d'outils, sur le port 8000 du pod.
# Les arguments sont ceux à épingler dans le pré-enregistrement (section 3).
set -euo pipefail
W=/workspace
export HF_HOME="$W/hf"
# Les poids sont déjà sur le volume : aucun téléchargement pendant le service.
export HF_HUB_OFFLINE=1
source "$W/venv/bin/activate"

vllm serve mistralai/Mistral-Small-3.2-24B-Instruct-2506 \
  --revision 95a6d26c4bfb886c58daf9d3f7332c857cb27b43 \
  --tokenizer-mode mistral --config-format hf --load-format safetensors \
  --quantization fp8 \
  --enable-auto-tool-choice --tool-call-parser mistral \
  --limit-mm-per-prompt '{"image":0}' \
  --max-model-len 65536 \
  --gpu-memory-utilization 0.92 \
  --enable-prefix-caching \
  --port 8000 \
  2>&1 | tee "$W/vllm.log"
