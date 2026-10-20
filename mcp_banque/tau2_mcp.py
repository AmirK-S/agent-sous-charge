"""La commande tau2, avec banking_knowledge branché sur le serveur MCP.

Usage, serveur lancé : python -m mcp_banque.tau2_mcp run --domain banking_knowledge ...
                     python -m mcp_banque.tau2_mcp evaluate-trajs <results.json>
"""
from mcp_banque.client import brancher

brancher()

from tau2.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
