#!/usr/bin/env bash
# Nuit du 22/10 : attend la fin du repos (processus donné), puis joue les paliers de charge de Mistral.
# Lancé sur la machine par SSH (sans passer par SkyPilot, dont le jeton Nebius avait expiré).
# Usage : bash enchainer-paliers.sh <pid à attendre>
set -uo pipefail
W="$HOME/workspace"; P="$W/agent-sous-charge"
PALIERS="${PALIERS:-2,4,8,12,16,24}"; MINUTES="${MINUTES:-10}"
while kill -0 "$1" 2> /dev/null; do sleep 30; done
echo "repos terminé : $(date -u +%H:%M:%S)"
set -a; source ~/.openrouter.env; set +a
pkill -f "vllm serve" || true; pkill -f mcp_banque.serveur || true; sleep 10
(cd "$P" && PYTHONPATH="$P" setsid nohup "$W/venv-tau/bin/python" -m mcp_banque.serveur --port 8765 > "$W/serveur-mcp-charge.log" 2>&1 < /dev/null &)
(setsid nohup env W="$W" bash "$P/pod/servir-modele.sh" > /dev/null 2>&1 < /dev/null &)
debut=$(date +%s)
until curl -sf localhost:8000/v1/models > /dev/null; do
  sleep 10; [ $(( $(date +%s) - debut )) -lt 1500 ] || { echo "vLLM absent"; exit 1; }
done
echo "vLLM prêt en $(( $(date +%s) - debut )) s ; début des paliers : $(date -u +%H:%M:%S)"
cd "$P" && timeout 2h env PYTHONPATH="$P" "$W/venv-tau/bin/python" -m mcp_banque.charge \
  --modele mistralai/Mistral-Small-3.2-24B-Instruct-2506 --paliers "$PALIERS" --minutes "$MINUTES" \
  --reflexion realiste --vidage-max-min 15 --sortie "$W/charge-mistral-l40s.jsonl" > "$W/charge.log" 2>&1
echo "fin des paliers : $(date -u +%H:%M:%S) (code $?)"
ps -o rss= -p "$(pgrep -f mcp_banque.serveur | head -1)" | awk '{printf "mémoire du serveur MCP : %.0f Mo\n",$1/1024}'
pkill -f "vllm serve"; pkill -f mcp_banque.serveur
echo "NUIT FINIE $(date -u +%H:%M:%S)"
