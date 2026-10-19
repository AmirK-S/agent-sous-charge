# Carte : combien de clients un agent tient-il sur un seul GPU ?

> Méthode Wayfinder (Matt Pocock) : une destination, une frontière de tickets prenables maintenant, du brouillard pour ce qui ne peut pas encore se décider. Chaque ticket se traite dans sa propre séance ; sa résolution est écrite dans le ticket, puis résumée ici en une ligne.
> Ouverte le 18/10/2026. Les modèles et les données lourdes se rangent hors du Bureau (synchronisation iCloud).

## Destination

Une **spécification construisible** : le protocole complet de l'expérience (règles, cas d'usage, protocole qualité, progression des optimisations, budget, scénario de la vidéo), assez précise pour être découpée en tickets d'implémentation, la première tranche étant le système entier en tout petit.

But derrière la destination : qu'Amir devienne réellement bon en montée en charge, latence, coût, observabilité et déploiement de systèmes IA, et qu'il en tire une vidéo divertissante pour des CTO.

## Ce qui est déjà tranché

| Décision | Source |
|---|---|
| Question : « votre agent bancaire tourne chez vous, sur votre GPU : combien de clients avant de cesser d'être fiable, à quel coût par conversation réussie, à quelle distance d'un modèle de pointe ? » | Amir, 18/10 |
| Cas d'usage : domaine banking_knowledge de τ³-bench (97 tâches, 698 documents, BM25 hors ligne), notation par état final de la base ; outils servis par MCP (à construire) ; témoin retail supprimé (ADV3) | R1, R6, Amir 18/10 |
| Modèles : Mistral Small 3.2 (européen) et Gemma 4 31B (américain) ; un modèle de pointe par API en repère de qualité, hors charge ; ni Qwen, ni DeepSeek, ni Llama 4 | R5, R7, Amir 18/10 |
| Un seul GPU, tout en réel, aucun simulateur | Amir, 18/10 |
| Destination, hors périmètre et critère d'arrêt ([G1](tickets/G1-destination-et-hors-perimetre.md)) | Amir, 18/10 |
| Règles du défi ([G9](tickets/G9-regles-du-defi.md)) | Amir, 18/10 |
| Barrière de qualité : aucune optimisation n'est retenue si elle dégrade la qualité au-delà du bruit | séance du 18/10 |
| Qualité mesurée sous charge, pas seulement au repos | séance du 18/10 |
| Angle libre confirmé : personne ne publie pass^k par palier de concurrence sur un agent avec outils | R3, 18/10 |
| Chaque tranche se termine à l'oral (contexte, choix, coût, chiffre) | séance du 18/10 |
| Protocole : [pré-enregistrement v3](PRE-ENREGISTREMENT.md), après trois revues adverses ([ADV1](tickets/ADV1-gemini.md), [ADV2](tickets/ADV2-astra.md), [ADV3](tickets/ADV3-astra-direct.md)) ; une seule affirmation certifiée (un modèle, une carte, un site, 57 tâches) ; le reste descriptif ; devis plafond avant gel | Amir, Gemini, Astra, 18/10 |

## Frontière (prenable maintenant)

| Ticket | Type | Objet | Bloque |
|---|---|---|---|
| P1 | prototype | Sur le Mac : une tâche de bout en bout, serveur MCP, traces, test d'équivalence MCP sur les 97 tâches | pilote |
| [G2](tickets/G2-gpu-impose.md) | cuisine | Le GPU imposé : L40S ou H100, selon la place mémoire des conversations bancaires | T1 |
| G4 | cuisine | Ce qu'est un utilisateur : une tâche bancaire τ³, temps de réflexion, patience | G6 |
| G5 | cuisine | Le client simulé : quel LLM, hors du GPU testé, et son coût | T1 |

## Brouillard (pas encore décidable)

| Ticket | Type | Objet | Attend |
|---|---|---|---|
| G6 | cuisine | Les seuils : latence, erreurs, pass^k, test statistique | G4 |
| G7 | cuisine | La progression des optimisations et leur ordre | P1 |
| G8 | cuisine | Le scénario et le ton de la vidéo | G6, G7 |
| P0 | prototype | Essai pilote sur GPU loués (section 9 du pré-enregistrement), 40 à 70 $ | P1, T1 |
| T1 | tâche | Compte de location GPU et page de dépense | G2 |
| D1 | déploiement | Image Docker à nous (vLLM et τ³ préinstallés, poids téléchargés au démarrage) : plus de réinstallation ni de disque payé entre deux séances, n'importe quelle machine libre fait l'affaire ; et la même image tourne chez d'autres fournisseurs (Scaleway, OVHcloud, Nebius : voir R8), d'où l'argument souverain (la comparaison de prix : une anecdote, pas un segment). Construction par GitHub Actions (Amir a des minutes ; disque des machines standard d'environ 14 Go, à vérifier) ; maintenance faible car versions épinglées puis gelées. À décider après P1, selon le rythme des séances. Né de la panne du 19/10 | P1 |
| R11 | recherche | Coût du FP8 en qualité : BF16 contre FP8 au repos, sur les 40 tâches de développement, sur une carte de 80 Go | P1, devis |

## Journal de la carte

- 19/10 : P1.1 fermée (vLLM sert Mistral Small 3.2 en FP8 sur une L40S, 97 712 tokens de cache ; oral d'Amir validé) ; R11 ajouté au brouillard.

- 18/10 : revue d'Astra seul par API (0,21 $), 12 objections retenues, 3 exigences supprimées ; pré-enregistrement v3, simplifié.

- 18/10 : revue d'Astra reçue, 13 objections retenues (une en partie), écart b renversé ; pré-enregistrement v2 ; G10 résolu ; plus de tour adverse avant le pilote.

- 18/10 : v1.1 (sensibilité 40/57, repli de confirmation) ; consigne ADV2 pour GPT-6 Astra écrite.

- 18/10 : revue adverse de Gemini reçue ([ADV1](tickets/ADV1-gemini.md)), 11 objections : 7 retenues, 4 adaptées ; pré-enregistrement passé en v1.

- 18/10 : R9 et R10 résolus ; brouillon de pré-enregistrement v0 et consigne d'attaque Gemini écrits ; pilote défini.

- 18/10 : cadrage bancaire, G1 et G9 validés par Amir ; modèles tranchés (G3 retiré), R2 historique (Qwen écarté).

- 18/10 : R5, R6, R7 résolus ; cadrage proposé à Amir (banque, deux modèles, L40S à revérifier).

- 18/10 : Amir questionne le cas d'usage et la crédibilité ; R5, R6, R7 ouverts.

- 18/10 : carte ouverte, 5 tickets en frontière, 8 dans le brouillard.
- 18/10 : R3 résolu, l'angle « qualité sous charge » est libre.
- 18/10 : R1 résolu, τ²-bench retail retenu ; G4 et G5 passent en frontière, R4 ouvert.
- 18/10 : R2 résolu, la L40S est confirmée ; G3 devient l'arbitrage dense contre MoE.
