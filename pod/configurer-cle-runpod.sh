#!/usr/bin/env bash
# Ouvre une fenêtre macOS où Amir colle sa clé Runpod (saisie masquée),
# puis enregistre le serveur MCP Runpod avec cette clé. La clé n'est jamais affichée.
set -euo pipefail
K=$(osascript -e 'text returned of (display dialog "Colle ta clé API Runpod (rpa_...) :" default answer "" with hidden answer with title "Runpod")') || { echo "Annulé."; exit 1; }
[ -n "$K" ] || { echo "Clé vide, rien n'est changé."; exit 1; }
claude mcp remove runpod -s user >/dev/null 2>&1 || true
claude mcp add --transport http runpod -s user https://mcp.getrunpod.io/ --header "Authorization: Bearer $K" >/dev/null
unset K
echo "Serveur Runpod enregistré."
