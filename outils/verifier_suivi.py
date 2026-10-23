"""Garde-fou du suivi (règle 9 de METHODE.md), lancé avant chaque commit par .githooks/pre-commit.

Bloque le commit si un ticket ou une mesure change sans que le suivi suive :
la section « État » de REPRISE.md et le journal de CARTE.md doivent porter la date du jour,
chaque ticket doit être lié depuis la carte, et deux tickets ne partagent jamais un numéro.
Contournement (avec l'accord d'Amir seulement) : git commit --no-verify.
"""
import datetime
import pathlib
import re
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent.parent
jour = datetime.date.today().strftime("%d/%m")
erreurs = []

modifies = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=ICI,
                          capture_output=True, text=True).stdout.split()
suivi_concerne = any(f.startswith(("tickets/", "mesures/")) for f in modifies)

carte = (ICI / "CARTE.md").read_text()
reprise = (ICI / "REPRISE.md").read_text()

# Numéros de ticket uniques, et chaque ticket lié depuis la carte.
numeros = {}
for f in sorted((ICI / "tickets").glob("*.md")):
    num = f.name.split("-")[0]
    if num in numeros:
        erreurs.append(f"numéro {num} pris deux fois : {numeros[num]} et {f.name}")
    numeros[num] = f.name
    if f"tickets/{f.name}" not in carte:
        erreurs.append(f"ticket non lié depuis CARTE.md : {f.name}")

if suivi_concerne:
    m = re.search(r"## État au (\d{2}/\d{2})", reprise)
    if not m or m.group(1) != jour:
        erreurs.append(f"REPRISE.md : la section « État au {jour} » n'est pas réécrite")
    journal = carte.split("## Journal de la carte", 1)[-1]
    if not re.search(rf"^- {re.escape(jour)}", journal, re.M):
        erreurs.append(f"CARTE.md : aucune ligne du {jour} dans le journal")

if erreurs:
    print("Suivi incomplet (règle 9 de METHODE.md) :")
    for e in erreurs:
        print("  -", e)
    sys.exit(1)
