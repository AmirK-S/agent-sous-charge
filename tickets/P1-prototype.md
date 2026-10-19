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
  - Vérification par le calcul : cache KV par token = 40 couches × 8 têtes KV × 128 dimensions × 2 (K et V) × 2 octets = 160 Kio ; 14,91 Gio / 160 Kio = 97 710 tokens, ce que vLLM annonce.
  - τ³ : installé depuis son verrou (`uv sync --frozen --extra knowledge`) ; bug du commit (le cœur importe `websockets` sans le déclarer), contourné en ajoutant seulement `websockets==15.0.1`. Retrieval retenu : `bm25` (hors ligne, sans clé ni bac à sable).
  - Client simulé : `openai/gpt-6-luna` sur OpenRouter, 0,10 $/M en entrée et 0,50 $/M en sortie (liste lue le 18/10).
- 18/10, 19 h 45 UTC : **pod arrêté** (EXITED, relu) en attendant Amir ; clé OpenRouter jamais saisie (P1.2 non lancée). Disque de 100 Go facturé environ 0,20 $/Go/mois à l'arrêt, soit environ 0,65 $/jour, jusqu'à l'arrêt définitif du pod. Journaux rapatriés dans `mesures/pod-18-10/`.
- 19/10 : **prédiction d'Amir pour P1.3**, écrite avant toute mesure : **B**, environ 15 000 tokens par conversation, soit environ 6 clients à la fois sur la L40S (« B perso, en réalité A, mais sûrement C » : il hésite entre 5 000 et 40 000). Raison donnée : ce sont les documents ramenés par la recherche qui font exploser le contexte. À comparer avec la mesure de P1.3.
- 19/10 : préparation de l'oral de P1.1 par questions ; carte 1 (FP8, BF16, facteur d'échelle) écrite dans `apprentissage/cartes.md`. Idée hors carte, pour le brouillard : mesurer au repos l'écart de qualité BF16 contre FP8 sur une carte de 80 Go.
- 19/10 : **porte de P1.1 fermée.** Oral enregistré et transcrit (`apprentissage/oraux/P1.1-2026-10-19.*`), puis reprise des points flous à l'écrit : option écartée (le BF16, pas le FP16 ; la H100), prix (1,09 $/h), perte de qualité non mesurée. Restent deux glissements de vocabulaire, à surveiller : « facteur de puissance » pour facteur d'échelle ; « on ne mesure pas, donc on avance » au lieu de « on ne mesure pas, donc on délimite l'affirmation ».
- **En attente avant P1.2** : (1) ~~l'oral de P1.1~~ fait ; (2) ~~le partage~~ fait le 19/10, voir ci-dessous ; (2 bis) le partage écrit des 97 tâches en 40 développement / 57 confirmation, absent du protocole : P1.2 et P1.3 ne doivent toucher que le développement. Recommandation provisoire : tirage à graine fixe, stratifié par nombre d'actions attendues (de 1 à 37, proxy de difficulté), sur `tasks.json` au commit `96a3ef92` (sha256 `213c7f3e…`) ; (3) la clé OpenRouter, saisie par Amir avec `ssh -t p1pod bash /workspace/agent-sous-charge/pod/saisir-cle-openrouter.sh`.
- 19/10 : **partage 40 / 57 décidé avec Amir** (reformulation : « on garde des tâches jamais vues, parce que réussir sur des cas inconnus vaut plus qu'un score sur des cas appris » ; objection d'abord soulevée : « on veut hyper-optimiser, pourquoi se priver de 57 tâches ? »). Tirage par `outils/partager_taches.py`, graine 20261019, 5 strates de nombre d'actions attendues, résultat dans `donnees/partage-taches.json` (sha256 de la source vérifié). Développement : 40 tâches, 10,6 actions en moyenne ; confirmation : 57 tâches, 9,3. Pas de nouveau tirage pour « mieux » équilibrer. Écartés : tout sur les 97 (chiffre optimiste par construction) ; validation croisée (3 à 5 fois plus de GPU par réglage).
- 19/10 : clé OpenRouter donnée par Amir dans le chat, à sa demande ; rangée dans `~/.config/openrouter/env` (hors dépôt, chmod 600), envoyée sur le pod à chaque démarrage. Plafond du compte : 50 $.
