#!/usr/bin/env bash
# Saisie masquée de la clé OpenRouter, à lancer par Amir sur le pod :
#   ssh -t p1pod bash /workspace/agent-sous-charge/pod/saisir-cle-openrouter.sh
# La clé va sur le disque conteneur (/root), effacé à l'arrêt du pod ; jamais sur /workspace.
set -euo pipefail
read -rsp "Clé OpenRouter (saisie masquée) : " cle
echo
[ -n "$cle" ] || { echo "Clé vide, rien d'enregistré."; exit 1; }
umask 077
printf 'OPENROUTER_API_KEY=%s\n' "$cle" > /root/.openrouter.env
code=$(curl -s -o /dev/null -w '%{http_code}' https://openrouter.ai/api/v1/key -H "Authorization: Bearer $cle")
echo "Clé enregistrée dans /root/.openrouter.env (${#cle} caractères) ; test OpenRouter : HTTP $code"
