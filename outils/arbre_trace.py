"""Affiche l'arbre d'une conversation tracée dans Phoenix (P1.6), et vérifie qu'il est complet.

Usage : python outils/arbre_trace.py <projet Phoenix> [--lignes 40]
(à lancer avec l'environnement de Phoenix : ~/.cache/agent-sous-charge/venv-phoenix/bin/python)
"""
import argparse
import warnings

warnings.filterwarnings("ignore")
from phoenix.client import Client  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("projet")
    p.add_argument("--lignes", type=int, default=40)
    p.add_argument("--url", default="http://127.0.0.1:6006")
    a = p.parse_args()
    df = Client(base_url=a.url).spans.get_spans_dataframe(project_identifier=a.projet, limit=20000)
    convs = df[df["name"].str.startswith("conversation")]
    print(f"{len(df)} spans, {len(convs)} conversation(s)")
    for _, conv in convs.iterrows():
        arbre = df[df["context.trace_id"] == conv["context.trace_id"]].copy()
        ids = {r["context.span_id"]: r for _, r in arbre.iterrows()}

        def profondeur(r):
            d = 0
            while r["parent_id"] in ids:
                r, d = ids[r["parent_id"]], d + 1
            return d

        arbre["prof"] = [profondeur(r) for _, r in arbre.iterrows()]
        arbre = arbre.sort_values("start_time")
        tokens = next((c for c in df.columns if c.endswith("llm.token_count.prompt")), None)
        noms = set(arbre["name"])
        complet = {
            "tours agent": any(n == "tour agent" for n in noms),
            "tours client": any(n == "tour client" for n in noms),
            "appels LLM (tokens)": "completion" in noms,
            "outils côté τ³": any(n.startswith("outil ") for n in noms),
            "outils côté serveur MCP": any(n.startswith("banque ") for n in noms),
            "spans vLLM": any(n.startswith("llm_request") or "vllm" in n.lower() for n in noms),
        }
        print(f"\n{conv['name']} : {len(arbre)} spans ; " + ", ".join(f"{k} {'oui' if v else 'NON'}" for k, v in complet.items()))
        for _, r in arbre.head(a.lignes).iterrows():
            ms = (r["end_time"] - r["start_time"]).total_seconds() * 1000
            t = r[tokens] if tokens else None
            extra = f"  [prompt {t:.0f} tokens]" if t is not None and t == t else ""
            print("  " * r["prof"] + f"{r['name']}  ({ms:.0f} ms){extra}")


if __name__ == "__main__":
    main()
