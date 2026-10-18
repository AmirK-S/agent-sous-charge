# R7 · recherche · Modèles ouverts non chinois

**Statut :** résolu le 18/10 (sous-agent ; poids FP8 calculés, scores d'agrégateurs non comparables entre protocoles)

## Résolution
| Modèle | Origine | Licence | Total / actifs | Score outils publié | FP8 | 48 Go | 80 Go |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | US | Apache 2.0 | 31B dense | τ² 76,9 (fiche HF) | ~31 Go | oui, cache modeste | oui |
| gpt-oss-120b | US | Apache 2.0 | 117B / 5,1B | τ retail 67,8 | ~60 Go MXFP4 | non | oui |
| Mistral Small 4 | FR | Apache 2.0 | 119B / 6,5B | aucun publié | ~120 Go (NVFP4 ~60) | non | NVFP4 seulement |
| Mistral Small 3.2 | FR | Apache 2.0 | 24B dense | aucun publié | ~24 Go | oui | oui |
| Nemotron 3 Nano | US | NVIDIA | 30B / 3,5B | τ² 47,0 | ~30 Go | oui | oui |

- Parser vLLM `mistral` confirmé pour les Mistral ; non vérifié pour Gemma 4 et gpt-oss.
- Mistral Medium 3.5 : licence MIT modifiée, quatre GPU, hors contrainte.
- Llama 4 : très bas sur τ² selon un agrégateur, et licence douteuse pour l'UE (R5) : écarté.
- Repère : Qwen3.5-27B τ² 79,0 auto-déclaré ; Gemma 4 31B à environ 2 points.
- **Recommandation** : sur L40S, Gemma 4 31B FP8 en premier, Mistral Small 3.2 comme représentant européen ; sur H100, gpt-oss-120b ou Mistral Small 4 NVFP4 après test. Montrer deux modèles, un européen et un américain. Les scores Mistral sont à mesurer nous-mêmes.
