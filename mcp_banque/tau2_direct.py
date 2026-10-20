"""La commande tau2 en exécution directe (sans MCP), avec les mêmes réglages que tau2_mcp : la référence de P1.5."""
from mcp_banque.client import brancher

brancher(par_mcp=False)

from tau2.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
