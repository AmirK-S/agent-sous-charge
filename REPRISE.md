# Reprise : où on en est (18/10/2026, 21 h)

> À lire après `CLAUDE.md`, avant `CARTE.md`. Écrit à la fin de la séance de cadrage du 18/10, pour qu'une nouvelle session reprenne sans rien redemander.

## Pourquoi ce projet existe (les mots d'Amir)
- Être payé 800 €/j et plus : maîtriser le métier d'ingénieur logiciel au-delà de ses expériences passées, et tenir une discussion technique serrée (montée en charge, déploiement, observabilité, coût, latence).
- Apprendre en faisant, puis le raconter : Amir doit être **propriétaire** du projet, capable de l'expliquer face caméra et de distinguer le signal du bruit.
- Une vidéo divertissante pour CTO et tech leads, inspirée de « How Many Users Can a $12 Server Handle? » et de sa suite communautaire (optimisations successives, chaque compromis expliqué).
- Réaliste pour un grand groupe européen : d'où la banque, l'hébergement souverain, et des modèles non chinois.

## Les décisions de la séance, en une ligne chacune
- Cas d'usage : τ³-bench banking_knowledge (97 tâches, 698 documents, BM25 hors ligne), notation par état final de la base.
- Tout en réel sur un GPU loué ; aucun simulateur du fournisseur (écarté : il fige la qualité et casse quand une conversation dérape).
- Modèles : Mistral Small 3.2 (européen) et Gemma 4 31B ; modèle de pointe par API en repère, hors charge. Ni Qwen, ni DeepSeek, ni Llama 4 pour l'agent (le client simulé peut être de n'importe quelle famille, autre que celle de l'agent).
- Client simulé : sur un second GPU pour les campagnes (l'API coûterait des milliers de dollars à grande échelle) ; pour P1, par OpenRouter avec un modèle bon marché (GPT-6 Luna, environ 0,10 $ par million de tokens en entrée, liste OpenRouter du 18/10).
- Protocole : `PRE-ENREGISTREMENT.md` v3, après trois revues adverses (Gemini, Astra en fusion, Astra seul par API). Une seule affirmation certifiée ; le reste descriptif ; devis plafond avant de figer. Amir a jugé la revue d'Astra seul la plus utile : elle a retiré de l'inutile coûteux.
- La règle « pas de nouveau projet perso avant le 22/10 » est levée par Amir : le projet compte comme préparation aux entretiens.
- Le Mac reste libre (mission, prospection) : tout calcul tourne sur le GPU loué, allumé seulement pendant les séances.

## État de l'infrastructure
- Plugin Runpod 1.7.4 installé pour Claude Code (compétences runpod:*). Commencer par la compétence `runpod:runpod-mcp`.
- L'OAuth Runpod **échoue depuis l'app de bureau** (adresse de retour refusée). Solution en place : serveur MCP `runpod` en portée utilisateur, avec la clé API d'Amir en en-tête (vérifiée le 18/10 : 50 caractères, préfixe `rpa_`). Si la clé change : `pod/configurer-cle-runpod.sh` ouvre une fenêtre de saisie masquée.
- Compte Runpod crédité par Amir. **Pod `xe77f1xnjb3r8x` (L40S, EU-NL-1) arrêté le 18/10 à 19 h 45 UTC**, tout installé sur son disque `/workspace` (vLLM 0.32, τ³, poids). Relancer : `pod-action start` ; l'adresse SSH change à chaque démarrage, mettre à jour l'alias `p1pod` dans `~/.ssh/config` (clé `~/.ssh/runpod_ed25519`). Le disque coûte environ 0,65 $/jour tant que le pod n'est pas supprimé.
- Clé OpenRouter : depuis le 19/10, à la demande d'Amir, rangée dans `~/.config/openrouter/env` (hors dépôt, chmod 600) ; la copier sur le pod dans `/root/.openrouter.env` à chaque démarrage. Sur le pod, il la saisit lui-même (même méthode : fenêtre ou saisie masquée), jamais dans le chat.

## Prochaine action précise

**Au 18/10, 19 h 45 UTC : P1.1 passe le contrôle technique** (voir le journal du ticket P1). Avant P1.2 : oral de P1.1 par Amir, partage 40/57 des tâches à écrire et valider, clé OpenRouter à saisir. Le plan initial ci-dessous reste la référence.

### Plan initial : P1.1 à P1.3 (ticket `tickets/P1-prototype.md`)
1. Lire en direct le prix et le stock de la L40S (Secure Cloud ; référence relevée le 18/10 : environ 1,09 $/h), puis proposer à Amir le pod exact : centre de données, image RunPod PyTorch, au moins 100 Go de disque, CUDA 12.8 minimum, coût horaire. **Lancer seulement après son accord écrit.**
2. Sur le pod : `pod/installer-pod.sh` (τ³ au commit 96a3ef92, vLLM, téléchargement de Mistral Small 3.2), puis `pod/servir-modele.sh`. Vérifier d'abord les drapeaux vLLM du modèle (format mistral, FP8 à la volée) : non testés.
3. Jouer une tâche banking de bout en bout (agent sur vLLM, client simulé par OpenRouter) ; lire `tau2 run --help` sur le pod pour les bons arguments (LiteLLM, `api_base`, préfixe `openai/`).
4. Mesurer une douzaine de tâches de développement : tokens par tour, total, occupation du cache KV, durée. Cela tranche G2 (L40S ou H100).
5. Éteindre le pod. Amir s'enregistre 2 minutes sur ce qui a été fait ; transcription ; points flous repris.

## Comment travailler avec Amir sur ce projet
- En français, court, une question à la fois avec une recommandation ; pas de tiret long.
- Toute commande qui attend une saisie (clé, mot de passe) ne marche pas depuis la zone de message de l'app : utiliser une fenêtre de saisie masquée (comme `pod/configurer-cle-runpod.sh`) ou le panneau Terminal.
- Toute dépense : la montrer avant, avec son prix, et attendre son accord.
- Avant chaque nouvelle tâche, il apprécie la version « plus profonde, pas plus grosse » (ce qu'un pro ferait, la matière brute, les méthodes, la preuve externe) puis le prompt réécrit.
- Il veut un journal signal / bruit : chaque décision, et ce qu'on a écarté en route.
