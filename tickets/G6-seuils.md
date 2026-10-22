# G6 · cuisine · Les seuils : latence, patience, temps de réflexion

**Statut :** tranché par Amir le 22/10.

## Valeurs provisoires (21/10) et ce que disent les sources

| Seuil | Provisoire | Sources | Proposition |
|---|---|---|---|
| Délai avant le premier token, par appel au LLM, p99 | < 2 s | MLPerf Inference, scénario Server, niveau standard : 2 000 ms pour Llama 2 70B et Llama 3.1 8B (niveau interactif : 450 à 500 ms) ; DistServe : 2,5 s pour un modèle de 66 milliards de paramètres | **Garder 2 s** : c'est le niveau le plus souple de MLPerf, pas un seuil strict |
| Temps par token de sortie, p99 | (absent) | MLPerf standard : 100 à 200 ms ; lecture humaine 238 mots/min, soit environ 5 tokens/s | **Ajouter < 200 ms** |
| Tour complet de l'agent (outils compris), p95 | < 8 s | Nielsen : vers 10 s, l'attention décroche ; AWS et Cloudscape : afficher la progression pendant les appels d'outils. Aucun objectif publié pour un agent à plusieurs étapes | **8 s sans affichage de progression, 10 s avec** |
| Temps de réflexion du client | uniforme 5 à 20 s | lecture 238 mots/min (méta-analyse de 190 études), frappe mobile 36 mots/min (37 370 personnes) | **Durée calculée** : lecture de la réponse + frappe du message + 2 à 5 s. L'uniforme 5 à 20 s est pessimiste pour le serveur (sous-estime la capacité) : à déclarer comme borne prudente si on la garde |
| Patience par tour | 30 s | données d'éditeurs seulement (chat avec conseiller humain : l'abandon monte nettement entre 30 et 60 s) | **Garder 30 s**, avec sensibilité à 15 s et 60 s |

## Sources
- Nielsen, trois limites de temps de réponse : https://www.nngroup.com/articles/response-times-3-important-limits/
- MLPerf Inference, `mlperf.conf` : https://raw.githubusercontent.com/mlcommons/inference/master/loadgen/mlperf.conf
- DistServe (OSDI 2024) : https://arxiv.org/pdf/2401.09670
- Sarathi-Serve (OSDI 2024) : https://arxiv.org/pdf/2403.02310
- Vitesse de lecture, Brysbaert 2019 : https://www.Gwern.net/doc/psychology/linguistics/2019-brysbaert.pdf
- Frappe mobile, Palin et al. 2019 : https://www.pokristensson.com/pubs/PalinEtAlMobileHCI2019.pdf
- AWS, latence des agents : https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentperf02-bp04.html
- Cloudscape, étapes progressives : https://cloudscape.design/gen-ai/patterns/progressive-steps/
- Abandon en chat (éditeur, non vérifié) : https://v20.velaro.com/blog/response-time-csat.html

## Points faibles
Le « 2 s de Miller » n'est connu que par des sources secondaires ; les taux d'abandon viennent d'éditeurs ; aucun objectif publié pour un agent à plusieurs étapes ; les objectifs de DistServe et Sarathi-Serve sont fixés par leurs auteurs, pas mesurés sur des utilisateurs.

## Résolution (22/10, Amir)
Les quatre seuils sont acceptés : **premier token < 2 s au p99**, **temps par token de sortie < 200 ms au p99**, **tour complet < 10 s au p95** (avec affichage de progression pendant les outils ; 8 s sans), **patience de 30 s** par tour (sensibilité à 15 et 60 s).
Question d'Amir : « peut-on être plus relax ensuite ? » Pas après avoir vu les résultats (ce serait choisir le seuil qui arrange). En revanche, **la courbe capacité contre seuil** (combien de clients à 2 s, 4 s, 6 s…) est pré-enregistrée comme résultat **descriptif** : c'est elle qui permet à une entreprise de choisir son compromis confort contre coût. Le seuil de 2 s reste celui de l'affirmation certifiée.
