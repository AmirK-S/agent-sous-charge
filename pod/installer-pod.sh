#!/usr/bin/env bash
# Installation du pod de P1 (RunPod, L40S 48 Go, image RunPod PyTorch).
# Tout est rangé sous /workspace, le disque persistant du pod.
# Usage, sur le pod : bash installer-pod.sh
set -euo pipefail

TAU_COMMIT="96a3ef92"                                   # commit lu le 18/10 (version 1.0.1)
MODELE="mistralai/Mistral-Small-3.2-24B-Instruct-2506"  # révision à épingler après le premier téléchargement
W=/workspace
export HF_HOME="$W/hf"

echo "== Machine =="
nvidia-smi --query-gpu=name,memory.total,power.limit,driver_version --format=csv
nproc; free -g | head -2

echo "== Outils =="
pip install -q uv
uv venv "$W/venv" --python 3.12
source "$W/venv/bin/activate"
uv pip install -q vllm

echo "== τ³-bench au commit épinglé =="
if [ ! -d "$W/tau2-bench" ]; then
  git clone https://github.com/sierra-research/tau2-bench "$W/tau2-bench"
fi
cd "$W/tau2-bench"
git fetch -q --all
git checkout -q "$TAU_COMMIT"
uv pip install -q -e .
git rev-parse HEAD > "$W/tau-commit.txt"

echo "== Téléchargement du modèle =="
huggingface-cli download "$MODELE" --exclude "*.pth" > /dev/null
echo "Installation terminée. Lancer ensuite : bash $W/agent-sous-charge/pod/servir-modele.sh"
