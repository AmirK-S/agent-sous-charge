# P1 · prototype · Le système entier en tout petit

**Statut :** en cours depuis le 18/10 (au titre de la préparation aux entretiens, décision d'Amir)
**Machine :** une L40S 48 Go louée chez RunPod (Secure Cloud), allumée seulement pendant les séances ; le Mac reste libre.
**Budget :** moins de 10 $ ; arrêt du pod après chaque séance.

## Tranches, dans l'ordre

| # | Tranche | Fini quand | Calcul estimé |
|---|---|---|---|
| P1.1 | Installer τ³ (commit épinglé) et vLLM sur le pod ; servir Mistral Small 3.2 en FP8 | `curl` sur l'API locale renvoie une réponse avec appel d'outil | 30 min |
| P1.2 | Jouer **une** tâche banking de bout en bout, agent sur vLLM, client simulé par OpenRouter (modèle bon marché) | une note τ³ (0 ou 1) et la trajectoire complète enregistrée | 30 min |
| P1.3 | **Mesurer la taille des conversations** sur une douzaine de tâches de développement : tokens par tour, tokens totaux, occupation du cache KV, durée | tableau publié dans `mesures/P1.3.md` ; réponse à G2 (L40S suffit-elle ?) | 1 h |
| P1.4 | Serveur MCP qui expose les outils banking à l'identique | les outils appelés par l'agent passent par MCP | construction |
| P1.5 | Test de fidélité MCP : actions dorées des 97 tâches, en série puis en parallèle | zéro écart de sortie et de hash | quelques minutes |
| P1.6 | Traces OpenTelemetry de bout en bout, visibles dans Phoenix | un arbre complet pour une conversation | construction |
| P1.7 | Tests d'abandon et d'annulation | aucune écriture après abandon, aucune génération orpheline dans vLLM | 30 min |

**Ce soir visé :** P1.1 à P1.3.

## À la fin de chaque tranche
Amir s'enregistre 2 minutes : ce qu'on a fait, pourquoi, ce que ça coûte, ce qu'on a écarté. Transcription, points flous repris. Une ligne dans le journal signal / bruit de la carte.

## Journal
- 18/10 : découpage écrit ; L40S retenue pour P1 (la RTX 4090 ne tient pas Mistral Small 3.2 avec du cache, la mesure de P1.3 serait fausse).
