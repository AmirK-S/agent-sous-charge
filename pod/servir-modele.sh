#!/usr/bin/env bash
# Sert Mistral Small 3.2 en FP8 avec appels d'outils, sur le port 8000 du pod.
# Les arguments sont ceux à épingler dans le pré-enregistrement (section 3).
set -euo pipefail
W=/workspace
export HF_HOME="$W/hf"
source "$W/venv/bin/activate"

vllm serve mistralai/Mistral-Small-3.2-24B-Instruct-2506 \
  --tokenizer-mode mistral --config-format mistral --load-format mistral \
  --quantization fp8 \
  --enable-auto-tool-choice --tool-call-parser mistral \
  --max-model-len 65536 \
  --gpu-memory-utilization 0.92 \
  --enable-prefix-caching \
  --port 8000 \
  2>&1 | tee "$W/vllm.log"
