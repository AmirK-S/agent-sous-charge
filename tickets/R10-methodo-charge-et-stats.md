# R10 · recherche · Méthodologie de charge et statistique

**Statut :** résolu le 18/10 (sous-agent, sources primaires lues sauf mention)

## Résolution
**MLPerf Inference** (github.com/mlcommons/inference_policies, inference_rules.adoc)
- Scénarios Server et Interactive : arrivées de Poisson, métrique = débit maximal qui tient la latence au 99e centile ; durée minimale 600 s.
- Seuils TTFT/TPOT, exemples : Llama3.1-8B 2000/100 ms (conversationnel) et 500/30 ms (interactif) ; Llama2-70B 2000/200 puis 450/40.
- Exactitude : 99 % ou 99,9 % de la référence ; garde-fou de longueur de sortie (au moins 90 % de la longueur de référence).
- Permis : batching continu, KV-cache paginé, quantification encadrée. Interdit : cache de réponses entre requêtes, troncature des sorties, connaissance du générateur de charge.
- À transposer : arrivées ouvertes, fenêtre de mesure et seuils fixés d'avance, exactitude relative à la référence, garde-fou de longueur, liste permis/interdit. Le cache de préfixe de vLLM est à trancher et déclarer.

**Miller, « Adding Error Bars to Evals »** (arXiv 2411.00640)
- Erreurs types groupées par tâche (éq. 4) ; ne jamais traiter les K×N essais comme indépendants.
- K essais par tâche : réduction de variance plafonnée (au mieux d'environ 2/3 dans l'exemple binaire).
- Analyse appariée entre deux configurations (éq. 7-8), préférable dès que la covariance est positive.
- Taille d'échantillon et effet minimal détectable (éq. 9-10) ; exemple de l'article : n = 198, MDE de 13,2 % (K = 1) à 7,5 % (K = 10). Avec 97 tâches, nos MDE seront larges : à calculer avant de pré-enregistrer.

**Omission coordonnée** (README wrk2, doc k6 open vs closed et arrival-rate)
- Une boucle fermée sous-échantillonne les pires latences. Correction : modèle ouvert (k6 constant-arrival-rate / ramping-arrival-rate), latence mesurée depuis l'instant prévu d'envoi ; surveiller dropped_iterations.
- Multi-tours (raisonnement, pas une source) : arrivées de conversations en Poisson ; au sein d'une conversation le tour suivant dépend légitimement de la réponse ; mesurer chaque tour depuis son instant d'émission possible et la conversation depuis son arrivée planifiée.

**Comparaisons multiples et tests appariés groupés**
- Holm-Bonferroni sur une famille définie d'avance (toutes contre la référence).
- McNemar groupé : Eliasziw et Donner 1991, Obuchowski 1998, Durkalski 2003, Yang 2010 ; paquet R clust.bin.pair ; bootstrap ou permutation par tâche, à justifier.

**Chauffe et régime stable**
- Aucune règle officielle pour vLLM : fixer d'avance la chauffe, une règle de coupure (coefficient de variation glissant) et la fenêtre de mesure ; MLPerf ne fixe qu'une durée minimale de 600 s.
