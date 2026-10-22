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
| G5 : client simulé par API (GPT-6 Luna, 0,0014 $ la conversation mesurée en P1.3) plutôt qu'un second GPU ; tenue du p99 < 1,5 s à vérifier au pilote | Amir, 21/10 |
| G2 : ne pas trancher avant le pilote ; mesurer L40S et H100 le même jour (environ 10 $ de plus), choisir sur le coût par conversation réussie | Amir, 21/10 |
| P0 : pilote accordé, plafond 80 $ ; soldes des fournisseurs vérifiés et recharges indiquées à Amir avant lancement (pas de recharge automatique) | Amir, 21/10 |
| G4 et G6, **provisoire** : réflexion du client 5 à 20 s, patience 30 s par tour ; premier token < 2 s au p99, tour < 8 s au p95. Amir trouve 2 s peut-être trop strict : sources à trouver avant de trancher. Biais du temps de réflexion neutralisé par des tirages communs à toutes les configurations, l'affirmation en débit, et une sensibilité publiée | Amir, 21/10 |

## Feuille de route et budget (estimation du 20/10, à remplacer par le devis plafond de P0)

| # | Étape | Séances | GPU | Coût estimé |
|---|---|---|---|---|
| 1 | Clore P1.3 (micro-leçon cache KV, oral) | 0,3 | non | 0 |
| 2 | P1.4 serveur MCP, P1.5 fidélité sur les 97 tâches | 2 à 3 | non | 0 |
| 3 | P1.6 traces (OpenTelemetry, Phoenix), P1.7 abandons | 2 à 3 | un peu | 2 à 5 $ |
| 4 | D1 image Docker | 1 | non | 0 |
| 5 | Cuisine G4 (utilisateur), G5 (client simulé), G6 (seuils) | 2 à 3 | non | 0 |
| 6 | P0 pilote, dont G2 tranché en mesurant L40S et H100 le même jour | 2 à 3 | oui | 50 à 80 $ |
| 7 | G7 optimisations successives, sur le développement (cœur de la vidéo) | 5 à 10 | oui, spot | 20 à 40 $ |
| 8 | Devis plafond, revue adverse, gel du protocole | 1 | non | 1 $ |
| 9 | Campagne confirmatoire, repli, réplication | 2 à 3 | oui | 40 à 150 $ selon la carte |
| 10 | G8 scénario et vidéo | ? | non | 0 |

Total estimé : environ 100 à 170 $ si la carte est une L40S, 180 à 300 $ si c'est une H100 (repère de pointe par API et marge de reprises compris). Base : conversation moyenne de 98 s et 131 500 tokens de prompt côté agent, client simulé à 0,0014 $ la conversation par API (mesures de P1.3).

## Frontière (prenable maintenant)

| Ticket | Type | Objet | Bloque |
|---|---|---|---|
| ~~P1~~ | prototype | **Terminé le 21/10** : vLLM sur L40S, une tâche de bout en bout, taille des conversations, serveur MCP à état, fidélité 0 écart, traces jusqu'à vLLM, abandons | pilote |
| [G2](tickets/G2-gpu-impose.md) | cuisine | Le GPU imposé : L40S ou H100, selon la place mémoire des conversations bancaires | T1 |
| [G4](tickets/G4-utilisateur.md) | cuisine | Ce qu’est un utilisateur : temps de réflexion et patience ; préparé le 21/10 (mesure : environ une minute entre deux messages) | G6 |
| G5 | cuisine | Le client simulé : quel LLM, hors du GPU testé, et son coût | T1 |

## Brouillard (pas encore décidable)

| Ticket | Type | Objet | Attend |
|---|---|---|---|
| [G6](tickets/G6-seuils.md) | cuisine | Seuils de latence **tranchés le 22/10** (2 s, 200 ms, 10 s, 30 s ; courbe capacité contre seuil en descriptif) ; restent erreurs, pass^k et test statistique | G4 |
| G7 | cuisine | La progression des optimisations et leur ordre. Piste d'Amir (20/10) : une courbe qui part du bas, comme la vidéo du serveur à 12 $ : (1) Ollama ou serveur Python, une requête à la fois ; (2) vLLM et son regroupement continu ; (3) cache du préfixe commun ; (4) cache KV en FP8 ; (5) harness sobre (moins de résultats, garde-fou anti-boucle) ; (6) décodage spéculatif, découpage des longs prompts ; (7) seulement à la fin, « et si on achète une H100 ? ». Chute visée : le logiciel multiplie plus que le matériel, au même prix | P1 |
| G8 | cuisine | Le scénario et le ton de la vidéo | G6, G7 |
| P0 | prototype | Essai pilote sur GPU loués (section 9 du pré-enregistrement), 40 à 70 $ | P1, T1 |
| T1 | tâche | Compte de location GPU et page de dépense | G2 |
| ~~[D1](tickets/D1-image-docker.md)~~ | déploiement | **Fait le 21/10** : image publique, vérifiée sur L40S ; environnement identique partout, mais pas de gain de temps (25 min de la location au modèle, dominés par les téléchargements) ; suite : poids sur un volume réseau | P0 |
| S1 | sécurité | Ce qu'une banque ou la défense exigerait des outils derrière MCP : authentification et permissions par client, journal d'audit, défense contre l'injection de prompt par les documents ; isolation du cache entre clients (sinon fuite par mesure du temps de réponse ; parade : `cache_salt` de vLLM, et le marqueur unique par conversation du protocole) ; et ce que chaque garde-fou coûte en latence, en tokens, donc en clients par GPU | P1.4 |
| R12 | recherche | Fine-tuning agentique (par exemple LoRA sur les trajectoires de développement) : levier très avancé ; risque d'apprendre le développement par cœur, et l'affirmation ne porterait plus sur « ce modèle » | G7 |
| R11 | recherche | Coût du FP8 en qualité : BF16 contre FP8 au repos, sur les 40 tâches de développement, sur une carte de 80 Go | P1, devis |

## Journal de la carte

- 22/10 : G6 (latence) tranché par Amir ; recharge OpenRouter préparée (15,89 $, factures au numéro de TVA de l'entreprise), à valider par Amir lui-même : l'achat par Claude est bloqué par la sécurité de l'environnement.

- 21/10 (soir) : D1 construite par GitHub Actions ; trouvaille : vLLM 0.32.0 embarque PyTorch pour CUDA 13.0 (nos recettes visaient 12.8) ; G4 préparé (environ une minute de réflexion par tour, mesuré) ; G6 sourcé.

- 21/10 : **P1 terminé** (portes de P1.6 et P1.7 fermées) ; image Docker D1 accordée en public sur GitHub (gratuit, sans notre code ni clé) ; G6 : sources réunies, 2 s est le niveau le plus souple de MLPerf.

- 21/10 : P1.4 et P1.5 fermées (MCP à état, 0 écart sur 1 246 appels) ; P1.6 (traces de bout en bout jusqu'à vLLM) et P1.7 (aucune écriture après abandon, générations arrêtées en 0,22 s) passent le contrôle technique ; oraux à faire. Environ 1,10 $ de GPU.

- 20/10 : P1.3 fermée (micro-leçon cache KV, carte 2, oral) ; feuille de route et budget estimés ; ancien pod RunPod supprimé ; prochaine tranche : P1.4.

- 19/10 : P1.2 et P1.3 jouées via SkyPilot (D2) chez Nebius ; P1.2 fermée ; P1.3 : médiane 14 822 tokens par conversation, prédiction d'Amir juste ; oral de P1.3 et décision G2 en attente.

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
