#!/usr/bin/env bash
# Installation du pod de P1 (RunPod, L40S 48 Go, image RunPod PyTorch).
# Tout est rangé sous /workspace, le disque persistant du pod.
# Usage, sur le pod : bash installer-pod.sh
set -euo pipefail

TAU_COMMIT="96a3ef92"                                   # commit lu le 18/10 (version 1.0.1)
MODELE="mistralai/Mistral-Small-3.2-24B-Instruct-2506"
REVISION="95a6d26c4bfb886c58daf9d3f7332c857cb27b43"         # lue sur l'API Hugging Face le 18/10
W="${W:-/workspace}"   # surchargé par SkyPilot (W=$HOME/workspace) hors RunPod
export HF_HOME="$W/hf"

echo "== Machine =="
nvidia-smi --query-gpu=name,memory.total,power.limit,driver_version --format=csv
nproc; free -g | head -2

echo "== Outils =="
# vLLM compile des noyaux au démarrage : il lui faut Python.h. Plutôt que de dépendre du Python du
# système (absent ou sans en-têtes selon l'image : Nebius le 19/10, RunPod via SkyPilot le 21/10),
# on utilise le Python géré par uv, qui embarque ses en-têtes.
export UV_PYTHON_PREFERENCE=only-managed
# Ubuntu 24.04 protège le Python système (PEP 668) : uv s'installe par son script officiel.
command -v uv > /dev/null || [ -x /opt/uv/bin/uv ] || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/opt/uv/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
VLLM_VERSION="0.32.0"   # épinglée (avant le 21/10 : non épinglée, 0.32.0 obtenue par chance à chaque fois)
# Avec l'image D1 (docker/Dockerfile), tout est déjà dans /opt : on s'y branche au lieu de réinstaller.
mkdir -p "$W"
for d in venv venv-tau tau2-bench; do
  [ -d "/opt/$d" ] && [ ! -e "$W/$d" ] && ln -s "/opt/$d" "$W/$d"
done
# Deux environnements séparés : vLLM et τ³ ne se parlent que par HTTP,
# et leurs dépendances épinglées ne doivent pas se marcher dessus.
[ -d "$W/venv" ] || uv venv "$W/venv" --python 3.12
VIRTUAL_ENV="$W/venv" uv pip install -q "vllm==$VLLM_VERSION"
"$W/venv/bin/python" -c "import vllm; print('vLLM', vllm.__version__)"

echo "== τ³-bench au commit épinglé =="
if [ ! -d "$W/tau2-bench" ]; then
  git clone https://github.com/sierra-research/tau2-bench "$W/tau2-bench"
fi
cd "$W/tau2-bench"
git fetch -q --all
git checkout -q "$TAU_COMMIT"
# Versions exactes du verrou du dépôt, plus l'extra du domaine banking (BM25).
# --inexact : ne pas retirer ce que l'image a ajouté (MCP, OpenTelemetry) ; sans lui, uv sync les supprimait
# et le serveur MCP ne démarrait plus (nuit du 22/10).
UV_PROJECT_ENVIRONMENT="$W/venv-tau" uv sync --frozen --inexact --extra knowledge
# Bug de τ³ à ce commit : le cœur importe le module vocal (websockets) sans le déclarer.
# L'extra voice tirerait pyaudio, à compiler : on n'ajoute que websockets, à la version du verrou.
VIRTUAL_ENV="$W/venv-tau" uv pip install -q "websockets==15.0.1"
"$W/venv-tau/bin/tau2" run --help > /dev/null
git rev-parse HEAD > "$W/tau-commit.txt"

echo "== Téléchargement du modèle =="
# Poids au format HF seulement : consolidated.safetensors (format mistral, 48 Go) les double
# et ferait déborder le volume de 100 Go. Le tokenizer mistral (tekken.json) reste téléchargé.
"$W/venv/bin/hf" download "$MODELE" --revision "$REVISION" \
  --exclude "*.pth" --exclude "consolidated.safetensors" > /dev/null
du -sh "$HF_HOME"
echo "Installation terminée. Lancer ensuite : bash $W/agent-sous-charge/pod/servir-modele.sh"
