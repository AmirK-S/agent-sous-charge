# D1 · Image de l'expérience : vLLM et τ³ préinstallés, aux versions épinglées.
# Ne contient ni notre code (ajouté au lancement par SkyPilot), ni clé, ni poids du modèle
# (téléchargés au démarrage dans $W/hf). Publique sur GitHub (décision d'Amir, 21/10).
#
# Base CUDA « devel » : vLLM compile des noyaux au démarrage et a besoin de nvcc
# (« Could not find nvcc » sur l'image par défaut de SkyPilot chez RunPod, 21/10).
FROM nvidia/cuda:12.8.1-devel-ubuntu24.04

ARG VLLM_VERSION=0.32.0
ARG TAU_COMMIT=96a3ef92329baf908ffe9dfe188cea34e8701d2a
ARG UV_VERSION=0.11.25

ENV DEBIAN_FRONTEND=noninteractive \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    PATH=/opt/uv/bin:$PATH

# Outils dont SkyPilot et nos scripts ont besoin dans le conteneur.
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git rsync openssh-client openssh-server sudo procps lsof python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

# uv, à version fixe, et un Python géré par uv (en-têtes inclus, pour la compilation des noyaux).
RUN curl -LsSf https://releases.astral.sh/github/uv/releases/download/${UV_VERSION}/uv-installer.sh | env UV_INSTALL_DIR=/opt/uv/bin sh \
    && uv python install 3.12

# Environnement de vLLM, avec ce qu'il faut pour envoyer ses traces (P1.6).
RUN uv venv /opt/venv --python 3.12 \
    && VIRTUAL_ENV=/opt/venv uv pip install "vllm==${VLLM_VERSION}" \
         opentelemetry-sdk==1.45.1 opentelemetry-api==1.45.1 opentelemetry-exporter-otlp==1.45.1 \
         opentelemetry-semantic-conventions-ai \
    && /opt/venv/bin/python -c "import vllm; assert vllm.__version__ == '${VLLM_VERSION}', vllm.__version__"

# τ³ au commit épinglé, depuis son verrou, avec l'extra du domaine banking ; plus MCP et les traces.
RUN git clone https://github.com/sierra-research/tau2-bench /opt/tau2-bench \
    && cd /opt/tau2-bench && git checkout -q "${TAU_COMMIT}" \
    && UV_PROJECT_ENVIRONMENT=/opt/venv-tau uv sync --frozen --extra knowledge \
    && VIRTUAL_ENV=/opt/venv-tau uv pip install "websockets==15.0.1" "mcp==2.3.0" \
         opentelemetry-sdk==1.45.1 opentelemetry-exporter-otlp-proto-http==1.45.1 \
         opentelemetry-instrumentation-httpx==0.66b1 openinference-instrumentation-litellm==0.1.50 \
    && /opt/venv-tau/bin/tau2 run --help > /dev/null \
    && git rev-parse HEAD > /opt/tau-commit.txt

# Manifeste des versions, lisible depuis le conteneur.
RUN { echo "vllm ${VLLM_VERSION}"; echo "tau2 $(cat /opt/tau-commit.txt)"; nvcc --version | tail -1; \
      /opt/venv/bin/python -c "import torch; print('torch', torch.__version__, 'cuda', torch.version.cuda)"; } \
    > /opt/versions.txt && cat /opt/versions.txt

WORKDIR /root
