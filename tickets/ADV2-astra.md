# ADV2 · revue adverse de GPT-6 Astra sur le pré-enregistrement v1.1

**Reçue le 18/10/2026**, collée par Amir. Astra a fusionné trois modèles (Gemini Pro, GPT, Claude Opus). Résumé fidèle :

| # | Objection | Gravité |
|---|---|---|
| 1 | Écart a (cache conservé) : décision maintenue, mais la longueur du préfixe partagé fait partie de la capacité ; publier les blocs partagés, sensibilité avec préfixe personnalisé, intituler « capacité avec ce préfixe » | sérieuse |
| 2 | Écart b : l'appariement n'annule pas le sur-ajustement (développer une tâche peut changer sa sensibilité à la charge) ; les 57 tâches doivent être la population confirmatoire, les 97 une analyse secondaire ; ne pas choisir la population selon un test d'hétérogénéité | fatale (généralisation) |
| 3 | Écart c : maintenu, mais famille de Holm à lister avant confirmation, hypothèses non testées comprises, α = 0,025 par étape | sérieuse |
| 4 | Capacité et qualité : exiger des bornes unilatérales (qualité, erreurs, dépassements de latence) et un plancher absolu métier ; test intersection-union | fatale (« fiable ») |
| 5 | Non-infériorité indéfinie : H0 Δ ≤ -0,05 avec une borne validée par simulation | fatale (inférence) |
| 6 | Les arrivées de Poisson ne garantissent pas K essais par tâche : horaires et tâches pré-générés par permutations équilibrées, homologues au repos | sérieuse |
| 7 | Maintien de durée p95 insuffisant, débit stable pouvant cacher une file qui grossit : maintenir jusqu'à la fin de toutes les conversations mesurées, surveiller la pente de la file, l'âge des requêtes, le retard d'injection | sérieuse |
| 8 | Ce n'est pas un maximum : dire « plus haut débit testé et confirmé », publier l'intervalle de recherche et les échecs | sérieuse |
| 9 | Client simulé : valider sur l'agent testé et ses trajectoires dégradées, accords positifs et négatifs, arbitrage humain, même client dans les deux conditions, échec de calibrage = arrêt ou remplacement symétrique | sérieuse |
| 10 | Simultanéité : publier sessions ouvertes, requêtes actives, mesurées directement | sérieuse |
| 11 | Tests MCP et annulation trop étroits : au-delà du pic, entrelacements adverses, expiration avant et après écriture, idempotence | sérieuse |
| 12 | Coût : définir occupation, provisionnement entier, coûts inclus ; essai de rafale ; taux d'erreurs par gravité avec bornes | sérieuse |
| 13 | Réplication : manifeste exécutable, traces d'arrivée, CPU, fréquences, températures, noyaux ; tolérance fixée d'avance ; MLPerf ne valide pas ce workload | sérieuse |

Verdict d'Astra : renverser b ; garder a et c sous conditions.

## Traitement
Toutes retenues ; 12 en partie (coûts de production d'une banque hors périmètre, déclarés comme tels). Voir `PRE-ENREGISTREMENT.md` v2, section 12.
