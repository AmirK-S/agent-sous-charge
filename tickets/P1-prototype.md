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
- 18/10, 19 h 09 UTC : pod `xe77f1xnjb3r8x` lancé (L40S, Secure Cloud, EU-NL-1, 1,09 $/h, image `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`, hôte CUDA 13.0, volume 100 Go sur `/workspace`, SSH seul). Clé SSH dédiée `~/.ssh/runpod_ed25519`, alias `p1pod`. Premier essai refusé (solde trop bas, 402), recrédité par Amir.
- 18/10 : **P1.1 fini.** vLLM 0.32.0, Mistral Small 3.2 (révision `95a6d26c`) en FP8 à la volée : poids 23,6 Go, cache KV 14,9 Go = **97 712 tokens**, soit 1,49 conversation de 65 536 tokens. `curl` renvoie un appel d'outil propre.
  - Écueils rencontrés (signal pour la vidéo, « ce qui casse en vrai ») : `pip install` refusé par Ubuntu 24.04 (PEP 668), donc uv par son script officiel ; τ³ et vLLM dans deux environnements séparés (ils ne se parlent que par HTTP) ; `hf download --exclude` ne prend qu'un motif par drapeau ; le volume de 100 Go ne tient pas les poids en double (format HF et format mistral, 45 + 48 Go) ; vLLM 0.32 bascule seul sur le format mistral en voyant `params.json` et télécharge 48 Go en douce, d'où `--config-format hf --load-format safetensors` et `HF_HUB_OFFLINE=1`.
  - Écarté : le format mistral natif (`consolidated.safetensors`), recommandé par la fiche, mais en double des poids HF déjà là ; le tokenizer mistral (`tekken.json`) est gardé pour les appels d'outils.
