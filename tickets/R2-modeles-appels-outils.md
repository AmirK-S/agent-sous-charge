# R2 · recherche · Modèles ouverts et appels d'outils

**Statut :** résolu le 18/10 (sous-agent ; mémoires calculées, scores auto-déclarés à relire) · **Débloque :** G3

## Question
Quels modèles ouverts obtiennent des scores publiés sur τ-bench ou BFCL, quelle taille en mémoire (FP8, 4 bits), compatibilité vLLM et appels d'outils, ce qui tient sur 24, 48 et 80 Go.

## Résolution
| Modèle | Total / actifs | Score publié | Poids FP8 |
|---|---|---|---|
| Qwen3.5-27B (dense) | 27B / 27B | τ² 79,0 ; BFCL-V4 68,5 | ~27 Go |
| Qwen3.5-35B-A3B (MoE) | 35B / 3B | τ² 81,2 ; BFCL-V4 67,3 | ~35 Go |
| GLM-4.7-Flash | ~30B / ~3B (non vérifié) | τ² 79,5 | ? |
| Qwen3-30B-A3B-Instruct-2507 | 30,5B / 3,3B | τ²-retail 57,0 | ~30 Go |
| gpt-oss-20b | 21B | τ-retail 54,8 | ? |

Sources : fiches Hugging Face de chaque modèle ; llm-stats.com/benchmarks/tau-bench-retail. Les τ² des fiches Qwen3.5 sont auto-déclarés et ne séparent pas le domaine retail.

- Sur L40S 48 Go : 27B FP8 laisse ~16 Go de cache KV ; 35B-A3B FP8 ~8 Go seulement (calcul, 90 % de mémoire utilisable).
- RTX 4090 : seulement du 4 bits, à éviter (étude NeurIPS 2026 : jusqu'à 13,5 % de décisions d'outil qui changent en INT4, « bons outils, mauvais arguments »).
- vLLM : Qwen3.5 avec `--enable-auto-tool-choice --tool-call-parser qwen3_coder`, version nightly requise ; raisonnement actif par défaut.
- **Conséquence pour G2** : confirme la L40S. **Pour G3** : vrai arbitrage dense contre MoE (27B : plus de place pour les conversations, décodage plus lent ; 35B-A3B : plus rapide, meilleur score, peu de cache). C'est un épisode de vidéo en soi.
- À vérifier avant location : quelques dizaines de tâches τ-bench en FP8 et le débit réel.
