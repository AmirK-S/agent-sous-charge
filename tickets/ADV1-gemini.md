# ADV1 · revue adverse de Gemini 4 sur le pré-enregistrement v0

**Reçue le 18/10/2026**, collée par Amir. Résumé fidèle des onze objections (texte complet conservé dans la conversation du 18/10) :

| # | Objection | Gravité selon Gemini |
|---|---|---|
| 1 | Biais de vidange : arrêter les arrivées à 600 s fait baisser la charge en fin de fenêtre | fatale |
| 2 | Chauffe de 120 s trop courte ; tâches rejouées plusieurs fois par palier, le cache de préfixe vLLM réutilise des débuts de conversation identiques | fatale |
| 3 | Temps de réflexion couplé à la lenteur du client simulé ; rafales synchronisées ; loi de Little faussée | sérieuse |
| 4 | Délai par appel égal à la patience par tour ; requêtes zombies non annulées dans vLLM | fatale |
| 5 | 32 tâches de test : effet minimal détectable de 15 à 25 points | fatale |
| 6 | Dichotomie de λ et confirmations : comparaisons séquentielles non corrigées, malédiction du gagnant | sérieuse |
| 7 | Client simulé ouvert complaisant ; calibrage insuffisant | sérieuse |
| 8 | Test d'équivalence MCP séquentiel, aveugle à la concurrence | fatale |
| 9 | Sur-ajustement de la recherche au vocabulaire du corpus, invisible pour le témoin retail | sérieuse |
| 10 | Coût par conversation à C* irréaliste (taux d'occupation, pics) ; repère de pointe pas dans le même harnais | sérieuse |
| 11 | Configuration vLLM et matériel sous-spécifiés | mineure |

Ses trois priorités : (1) garder les 97 tâches banking pour le test, développer ailleurs ; (2) régime stationnaire (chauffe 300 s, arrivées maintenues pendant la vidange, cache KV non partagé, annulation propagée) ; (3) isolation sous concurrence du serveur MCP et du client simulé.

## Traitement
Voir `PRE-ENREGISTREMENT.md` v1 et le tableau de tri dans la carte.
