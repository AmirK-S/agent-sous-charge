# ADV3 · revue adverse de GPT-6 Astra seul, par API, sur le pré-enregistrement v2

**Reçue le 18/10/2026** via OpenRouter (modèle `openai/gpt-6-astra`, sans fusion), 6 177 tokens envoyés, 2 687 reçus, coût 0,21 $. Réponse intégrale :

1. **Les seuils des bornes contredisent l’allocation du risque. — Fatale.**  
   L’intersection-union évite une correction *entre critères*, mais n’autorise pas des bornes à 95 % lorsque chaque étape dispose de 2,5 %, avant Holm. **Scénario :** 300 conversations sans échec donnent une borne de 0,994 % à 95 %, mais de 1,22 % à 97,5 %. **Correction :** construire une p-valeur par critère, prendre leur maximum par configuration, puis appliquer Holm. Pour dimensionner conservativement, utiliser α = 0,025/m : sans échec et sous indépendance, il faut 368 conversations pour m = 1, 437 pour m = 2. Définir aussi le test du plancher métier.

2. **Le calcul « 300 conversations » suppose précisément l’indépendance que le protocole interdit ailleurs. — Fatale.**  
   Les pannes communes et la contention corrèlent conversations et appels ; trois passages ne permettent pas une inférence robuste groupée par passage. **Scénario :** aucun incident pendant trois passages, mais un blocage survient dans 10 % des passages ; multiplier les appels ne renseigne guère ce risque. Un bootstrap de données toutes nulles donne même une borne nulle. **Correction :** distinguer erreurs individuelles et incidents communs ; préspécifier un modèle de dépendance justifié, ou augmenter les blocs temporels indépendants. À défaut, publier les fréquences observées sans certification « ≤ 1 % ». Ne jamais employer un bootstrap naïf pour une proportion nulle.

3. **La « population finie de 57 tâches » et le bootstrap des tâches visent deux estimands différents. — Fatale.**  
   Rééchantillonner les tâches représente une population hypothétique de tâches, alors que le texte limite toute affirmation aux 57 tâches fixées. **Scénario :** des différences propres aux tâches persistent avec K croissant ; le bootstrap conserve une variance intertâche, même lorsque leurs performances moyennes sont connues précisément. **Correction :** choisir explicitement : moyenne équipondérée des 57 tâches, avec incertitude sur répétitions et exécutions ; ou généralisation à une population définie de tâches, avec rééchantillonnage des tâches. Dans les deux cas, traiter séparément la dépendance temporelle sous charge.

4. **La puissance annoncée n’est ni définie ni garantie par K. — Sérieuse.**  
   « Détecter la marge » omet l’alternative réelle et la puissance de la certification complète. **Scénario :** à Δ = 0, sans correction supplémentaire et sous approximation normale, il faut une erreur-type inférieure à 0,05/(1,96 + 0,84) ≈ 1,8 point pour 80 % de puissance. Avec 57 grappes et une variance intertâche irréductible, cela exige un écart-type des différences inférieur à environ 13,5 points ; augmenter K ne suffit pas nécessairement. **Correction :** simuler à Δ = 0 et −2 points, sur plusieurs dépendances plausibles, avec intervalles d’incertitude issus du pilote. Rapporter la puissance de *tous les critères réunis*, pas seulement celle de la non-infériorité.

5. **Le plancher au repos ne garantit pas le plancher métier sous charge. — Sérieuse.**  
   **Scénario :** un plancher de 80 %, une réussite au repos de 83 % et sous charge de 79 % peuvent satisfaire vos deux conditions avec assez de données. **Correction :** exiger également que la borne inférieure de réussite **sous charge** dépasse le plancher métier, ou remplacer le plancher au repos par celui-ci. Sinon, retirer toute formulation laissant entendre que ce minimum est tenu à C*.

6. **Le calendrier équilibré laisse indéfinie la compatibilité entre K exact, Poisson et fenêtre minimale. — Sérieuse.**  
   L’équilibrage des identités ne garantit pas simultanément un nombre fixé d’arrivées et une fenêtre temporelle fixée. **Scénario :** la Kᵉ permutation finit après 600 secondes ; tronquer détruit l’équilibre, comprimer les horaires détruit Poisson. **Correction :** générer des interarrivées exponentielles et des permutations indépendantes ; terminer la cohorte au premier bloc équilibré achevé après 600 secondes et après l’effectif minimal. Publier avant exécution le K ainsi obtenu. Prévoir séparément les arrivées de maintien jusqu’à la dernière échéance possible, non incluses dans les scores, et leur coût.

7. **Cinq signaux ne constituent pas une règle de stationnarité. — Sérieuse.**  
   **Scénario :** une pente estimée légèrement positive apparaît dans un régime stable ; inversement, un test peu puissant accepte une dérive lente. Les expirations peuvent aussi stabiliser artificiellement une file surchargée. **Correction :** fixer les fenêtres, les métriques exactes, les tolérances de dérive et les plafonds d’âge/retard, puis les valider sur surcharge artificielle. Employer une règle opérationnelle bornée, non « absence de significativité ». Les expirations restent des échecs, même si elles stabilisent la file.

8. **Quelques centaines de dollars constituent une hypothèse budgétaire, pas encore un plan réalisable. — Sérieuse.**  
   **Scénario :** avec une seule configuration, K = 7 donne 399 conversations ; repos et charge sur trois locations représentent déjà 2 394 conversations, hors pilote, maintien, repli, calibrage et API. À deux minutes par conversation au repos strictement sériel, les seules références occupent environ 40 heures sur trois locations. Ce n’est pas nécessairement impossible, mais les tarifs et durées décident. **Correction :** publier un devis plafond intégrant les deux GPU, les API, les queues de campagne et les reprises. Design honnête : un modèle, une carte, un site confirmatoire ; seconde location descriptive ; arrêt budgétaire fixé. Si la puissance manque, annoncer une étude descriptive avec bornes, sans C* certifié.

9. **Les règles d’invalidation permettent d’effacer des conditions défavorables. — Sérieuse.**  
   **Scénario :** les campagnes avec client simulé lent sont rejouées jusqu’à obtenir un créneau favorable ; les erreurs d’infrastructure sont simultanément annoncées comme échecs et comme motifs de reprise. **Correction :** distinguer avant mesure défaillance de l’instrument et défaillance du système évalué. Conserver publiquement toute tentative, limiter les reprises et fixer leur traitement statistique. Si les incidents d’hébergement sont exclus, qualifier explicitement le résultat de capacité conditionnelle hors incident.

10. **Les dénominateurs de latence peuvent masquer les requêtes les plus mauvaises. — Sérieuse.**  
    **Scénario :** un appel expire avant le premier token et disparaît du calcul TTFT ; les appels réussis respectent alors artificiellement le seuil. **Correction :** enregistrer tout appel prévu, horodater avant les files du harnais et compter comme dépassement toute absence de premier token à l’échéance. Pour les tours, inclure outils, attente et annulation ; préciser les dépendances utilisées dans les bornes.

11. **Quatre regards et un calibrage tardif rendent ambigu le gel confirmatoire. — Sérieuse.**  
    **Scénario :** une mauvaise confirmation conduit à remplacer le client, puis à recommencer « toutes les conditions », sans comptabiliser cette sélection. **Correction :** terminer calibrage, choix du client et choix de l’agent sur développement uniquement. Une configuration gelée, une procédure confirmatoire. Toute modification ultérieure ouvre une nouvelle étude ; les regards intermédiaires restent aveugles aux résultats comparatifs.

12. **« Fiable » dépasse les garanties réellement testées. — Sérieuse.**  
    **Scénario :** quelques actions bancaires graves restent compatibles avec le score global, puisque leur gravité n’est qu’une analyse secondaire. **Correction :** écrire « conforme aux critères du benchmark », ajouter une règle d’arrêt sur incident grave confirmé et publier sa borne sans prétendre certifier la sécurité bancaire. Remplacer aussi « tâches jamais vues » par « jamais utilisées pour développer cet agent » : l’exposition des modèles préentraînés est inconnue.

13. **Trois changements prioritaires, classés :**  
    **1)** Unifier estimand, dépendance, tests et seuils corrigés.  
    **2)** Budgéter avant gel et réduire à une configuration confirmatoire réellement finançable.  
    **3)** Rendre exécutables les règles de calendrier, stationnarité, invalidation et gel.

14. **Trois exigences à supprimer :**  
    **1)** Le seuil de longueur moyenne à 90 % : la verbosité ne certifie pas la qualité.  
    **2)** Retail avant/après : il ne valide pas la capacité banking et consomme des ressources.  
    **3)** Deux locations supplémentaires obligatoires : remplacer par une réplication descriptive sur une autre location, sans prétention de généralisation matérielle.

## Traitement
Voir `PRE-ENREGISTREMENT.md` v3, section 12.
