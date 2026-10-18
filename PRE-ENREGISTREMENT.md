# Pré-enregistrement : fiabilité d'un agent bancaire sous charge, sur un seul GPU

> **Brouillon v3 du 18/10/2026, non figé.** Trois revues adverses : Gemini 4 sur v0 (ADV1), GPT-6 Astra en fusion de trois modèles sur v1.1 (ADV2), GPT-6 Astra seul par API sur v2 (ADV3). La v3 simplifie : une seule affirmation certifiée, sur un modèle, une carte, un site ; le reste est descriptif. Les cases `[PILOTE]`, `[G4]`, `[G6]` se remplissent avant le gel. Le document est figé après le pilote par un commit dont l'empreinte est publiée avant toute mesure confirmatoire.

## 1. Question

Un agent de support bancaire avec outils, hébergé sur un seul GPU : quel est le plus haut débit de clients qu'il sert en restant conforme aux critères de qualité du banc, à quel coût par conversation réussie, et à quelle distance d'un modèle de pointe ?

Le chiffre phare est la capacité ; la qualité est la barrière qui la valide.

## 2. Ce qui est certifié, ce qui est descriptif

| Statut | Contenu |
|---|---|
| **Confirmatoire (une seule affirmation testée)** | Le débit C\* d'**une** configuration gelée (un modèle, une carte, un site), sur les 57 tâches de confirmation |
| Descriptif | Le second modèle ; la seconde location ; les étapes de la progression des optimisations ; la sensibilité au préfixe personnalisé ; l'essai de rafale ; les 97 tâches ; la distance au modèle de pointe ; le coût |

**Choix du modèle confirmatoire, sur le développement seulement** : Mistral Small 3.2 si sa réussite au repos n'est pas inférieure de plus de `[G6]` points à celle de Gemma 4 31B sur les 40 tâches de développement (préférence souveraine assumée) ; sinon Gemma 4 31B. Règle appliquée avant tout regard sur la confirmation.

## 3. Objet mesuré

| Élément | Choix | Épinglé |
|---|---|---|
| Banc | τ³-bench, domaine banking_knowledge | dépôt sierra-research/tau2-bench, commit `[à épingler]`, version ≥ 1.0.1 |
| Recherche documentaire | variante `bm25` | rank_bm25 par défaut, top_k 10 |
| Agent | notre agent, servi par vLLM, outils par un serveur MCP | image Docker, tous les arguments vLLM (dont cache de préfixe et moteur d'attention) |
| Modèles | Mistral Small 3.2 24B ; Gemma 4 31B ; FP8 natif | révisions Hugging Face |
| Repère de qualité | un modèle de pointe par API, même harnais, hors charge | `[à choisir]`, date d'appel |
| Client simulé | modèle ouvert d'une autre famille, second GPU, même centre de données, le même partout | choisi et calibré **sur le développement, avant le gel** |
| Matériel | un GPU pour l'agent (L40S ou H100, tranché par le pilote) | manifeste exécutable : fournisseur, région, variante, série, limite de puissance, fréquences et températures pendant les campagnes, CUDA, CPU, NUMA, vCPU |

**Conditions d'entrée, vérifiées avant toute mesure** :
1. Équivalence MCP : actions dorées des 97 tâches rejouées par le serveur MCP et directement, en série puis à deux fois le pic observé au pilote ; zéro écart de sortie et de hash.
2. Abandons : expiration du tour avant et après une écriture, entrelacements adverses ; jamais d'écriture validée après abandon, jamais de doublon.
3. Annulation : aucune génération vLLM ne survit à un abandon ; vérifié par test et surveillé en campagne.
4. Serveur MCP et BM25 sur processus CPU dédiés.

## 4. Découpage et estimand

- **Développement**, 40 tâches : construction de l'agent, choix du modèle, choix et calibrage du client simulé.
- **Confirmation**, 57 tâches : jamais utilisées pour développer cet agent. (L'exposition des modèles pré-entraînés au banc reste inconnue ; on n'écrit pas « jamais vues ».)
- **Estimand : la réussite moyenne équipondérée sur ces 57 tâches précises** (population finie). L'incertitude vient des répétitions et des passages, pas d'un tirage hypothétique de tâches. Aucune généralisation à « toutes les tâches bancaires » n'est affirmée. Ce choix est le seul compatible avec la phrase finale et avec un budget de quelques centaines de dollars.

## 5. Critère de capacité

C\* est le plus haut débit d'arrivée λ **testé et confirmé** tel que, sur les 57 tâches et au même débit :

**Critère statistique (le seul testé)**
- **Qualité** : Δ = réussite sous charge − réussite au repos (appariée par tâche et graine). H0 : Δ ≤ −5 points ; rejet si la borne inférieure unilatérale de Δ dépasse −5 points, au seuil de la section 7.
- **Plancher métier sous charge** : borne inférieure unilatérale de la réussite **sous charge** ≥ `[G6]` %.
- Les deux sont combinés par intersection-union : p-valeur de la configuration = maximum des deux p-valeurs.

**Critères opérationnels (seuils observés, à la manière de MLPerf, pas de test)**
- Échecs d'exécution observés ≤ 1 % des conversations mesurées, avec au moins `[PILOTE]` conversations par passage.
- Latence : p99 observé du délai avant le premier token par appel ≤ `[G6]` s, p95 observé du temps de réponse par tour ≤ `[G6]` s. **Tout appel prévu compte** : un appel sans premier token à l'échéance est un dépassement ; le temps est mesuré depuis l'horodatage avant toute file du harnais, et un tour inclut outils, attente et annulation.
- Stationnarité (section 6).

**Incidents communs, descriptifs** : les blocages qui touchent tout un passage (panne, contention) sont comptés et publiés par passage, séparément des erreurs individuelles ; trois passages ne permettent pas de certifier leur rareté, et on ne le prétend pas.

**Règle d'arrêt sur incident grave** : une action non autorisée en base ou un contrôle d'identité contourné, confirmé par lecture humaine, à C\*, invalide l'affirmation de conformité pour ce palier.

## 6. Scénario de charge

- **Modèle ouvert** : interarrivées exponentielles de débit λ, indépendantes des réponses ; dans une conversation, le tour suivant attend la réponse.
- **Calendrier** : interarrivées tirées d'avance ; identités de tâches tirées par permutations indépendantes des 57 tâches. La cohorte mesurée se termine au **premier bloc de 57 complet après 600 s** et après l'effectif minimal ; le K obtenu est publié avant exécution. Des arrivées de **maintien** continuent jusqu'à la dernière échéance possible des conversations mesurées ; elles ne sont pas notées, leur coût est budgété. Chaque conversation mesurée a son homologue au repos (même tâche, même graine du client).
- **Chauffe** : ≥ 300 s et ≥ 2 durées moyennes de conversation `[PILOTE]`.
- **Stationnarité, règle opérationnelle** : fenêtres glissantes de `[PILOTE]` s ; dérive du débit < `[PILOTE]` %, file d'attente en fin de fenêtre ≤ `[PILOTE]` fois son niveau de début, âge maximal d'une requête en attente ≤ `[PILOTE]` s, retard d'injection p99 ≤ `[PILOTE]` s. Règle validée au pilote sur une surcharge volontaire (elle doit la rejeter). Les expirations restent des échecs, même si elles stabilisent la file.
- **Cache de préfixe** : activé pour le préfixe commun, marqueur unique par conversation juste après ; séquences tokenisées et blocs partagés publiés ; preuve d'absence de réutilisation après le marqueur. Intitulé : « capacité avec ce préfixe partagé ». Sensibilité au préfixe personnalisé, descriptive.
- **Temps de réflexion** : uniforme sur `[G4]`, compté après la génération du client simulé ; client tenu à un p99 de génération < 1,5 s, distribution publiée.
- **Patience par tour** : budget de `[G6]` s propagé aux appels ; expiration = échec, connexion fermée, génération annulée.
- **Recherche exploratoire de C\*** : doublement puis dichotomie sur les critères opérationnels, tâches de développement ; ne conclut rien. λ candidat figé avant confirmation.
- **Confirmation** : trois passages au λ candidat sur les 57 tâches ; critère statistique testé une fois sur l'ensemble.
- **Repli unique** : un palier 15 % plus bas si la confirmation échoue, données neuves, mêmes critères.

## 7. Analyse statistique

- **Incertitude** : sur l'estimand de population finie, variance issue des répétitions intra-tâche et des passages ; erreurs types groupées par passage pour la dépendance temporelle sous charge. Méthode exacte (bootstrap par blocs de passages et de répétitions, ou modèle à effets de passage) choisie et **validée par simulation au pilote** (couverture à Δ = 0 et Δ = −5).
- **Seuils** : 2,5 % pour la confirmation, 2,5 % pour le repli. Une seule configuration confirmatoire : pas de famille à corriger. Si le pilote amène à confirmer deux configurations, Holm sur les deux, listées avant gel.
- **Puissance** : simulée à Δ = 0 et Δ = −2 points, sur plusieurs dépendances plausibles tirées du pilote, pour **le critère complet** (qualité et plancher). Objectif 80 %.
- **Si la puissance ou le budget manque** : on l'annonce avant de mesurer et l'étude devient **descriptive avec bornes**, sans C\* certifié. Ne pas rejeter H0 ne s'écrit jamais « pas de baisse ».
- **Alerte précoce** : validité des appels d'outils sur tous les appels ; déclenche l'examen, pas une conclusion.

## 8. Discipline des données

- Tout ce qui se choisit (agent, prompt, modèle, client simulé, recherche, seuils) se choisit sur le développement, avant le gel. **Une configuration gelée, une procédure confirmatoire.** Toute modification après le gel ouvre une nouvelle étude, publiée comme telle.
- Aucun fait métier absent des documents, aucune consigne visant une tâche ; modifications du prompt journalisées ; script anti-fuite ; relecteur indépendant.
- Les regards intermédiaires sur la confirmation pendant la progression (au plus trois, fixés dans G7) sont descriptifs et ne servent jamais à choisir.

## 9. Qualité de la mesure

- **Client simulé** : calibré sur le développement contre gpt-4.1, sur les agents testés y compris leurs trajectoires dégradées, accords positifs et négatifs séparés (kappa ≥ 0,85 visé), arbitrage humain des désaccords. Choix figé avant le gel.
- **Erreurs du client** : juge « user only » du dépôt, lecture humaine de 20 conversations par campagne, sensibilité avec et sans les conversations déviantes.
- **Grille de gravité** : grave, moyenne, mineure (définitions dans le ticket G6) ; taux et bornes publiés, sans prétendre certifier la sécurité bancaire.
- **Instrument contre système** : définis avant mesure. Défaillance de l'instrument (client simulé hors p99, générateur saturé, GPU loué perdu) : la tentative est conservée publiquement et rejouée, **deux reprises au plus par palier**. Défaillance du système évalué (échec d'exécution, expiration, erreur d'infrastructure de l'agent) : compte 0, jamais rejouée.
- **Réplication** : la configuration confirmatoire rejouée une fois sur une autre location, **descriptive**, tolérance annoncée d'avance. Débit MLPerf de la même carte en ordre de grandeur seulement.
- **Non-déterminisme** sous batching vLLM : d'où les répétitions.

## 10. Essai pilote et budget

**But** : remplir les cases, trancher le GPU, choisir modèle et client simulé, valider la règle de stationnarité, simuler la puissance, **chiffrer un devis plafond** avant gel.
**Déroulé** : sur le Mac (gratuit), prototype P1 et conditions d'entrée ; calibrage du client simulé ; sur GPU loués, 40 tâches de développement × 4 essais × 2 modèles à faible concurrence, 3 paliers, une surcharge volontaire, une heure sur une deuxième machine.
**Coût du pilote** : de l'ordre de 40 à 70 $.
**Devis plafond de la campagne** (produit par le pilote, validé par Amir avant gel) : deux GPU, API, chauffes, maintiens, reprises, repli, réplication. **Arrêt budgétaire** fixé dans le devis : au-delà, l'étude passe en descriptive.

## 11. Ce que nous affirmerons, et rien de plus

« Sur cette carte (variante, limite de puissance), avec ce modèle, cet agent, ce banc et ce préfixe partagé : C\* conversations par minute, plus haut débit testé et confirmé, soit S sessions ouvertes en moyenne, où l'agent reste conforme aux critères du banc (réussite non inférieure au repos à 5 points près et au-dessus du plancher, échecs observés < 1 %, latences tenues) sur 57 tâches jamais utilisées pour le développer ; X € par conversation réussie à saturation, Y € pour le profil de pointe déclaré. » Le reste est présenté comme descriptif.

## 12. Traitement des revues adverses

Les décisions sur ADV1 et ADV2 restent valables (voir la v2 dans l'historique git), sauf ce que la v3 simplifie ci-dessous.

**ADV3, GPT-6 Astra seul (sur v2)**

| # | Objection | Décision |
|---|---|---|
| 1 | Seuils des bornes contraires à l'allocation du risque | Retenue : p-valeur maximale par configuration ; une seule configuration, seuil 2,5 %. |
| 2 | Borne d'erreurs fondée sur une indépendance fausse | Retenue : erreurs et latences deviennent des seuils opérationnels observés ; incidents communs descriptifs ; plus de certification « ≤ 1 % ». |
| 3 | Estimand ambigu | Retenue : population finie des 57 tâches. |
| 4 | Puissance mal définie | Retenue : simulée à Δ = 0 et −2 pour le critère complet. |
| 5 | Plancher au repos insuffisant | Retenue : plancher sous charge. |
| 6 | Calendrier, K et fenêtre incompatibles | Retenue : premier bloc complet après 600 s, maintien séparé. |
| 7 | Stationnarité non opérationnelle | Retenue : tolérances fixées, validées sur surcharge volontaire. |
| 8 | Budget non démontré | Retenue : un modèle, une carte, un site confirmatoires ; devis plafond et arrêt budgétaire ; repli descriptif. |
| 9 | Invalidations exploitables | Retenue : instrument contre système, deux reprises au plus, tout publié. |
| 10 | Dénominateurs de latence | Retenue : tout appel prévu compte. |
| 11 | Gel ambigu | Retenue : tout choix sur le développement, une configuration gelée. |
| 12 | « Fiable » trop fort | Retenue : « conforme aux critères du banc », « jamais utilisées pour le développer », arrêt sur incident grave. |
| Suppr. 1 | Garde-fou de longueur | Supprimé. |
| Suppr. 2 | Témoin retail | Supprimé (ne valide pas la capacité banking ; la confirmation sur 57 tâches couvre la généralisation affirmée). |
| Suppr. 3 | Trois locations obligatoires | Remplacé par une réplication descriptive. |
