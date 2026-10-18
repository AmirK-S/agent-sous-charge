# G9 · cuisine · Les règles du défi (ce qui est permis, interdit, permis avec astérisque)

**Statut :** résolu le 18/10

Principe, repris de la vidéo du défi communautaire : le contrat mesuré ne change jamais ; tout le reste est libre ; un compromis réel est permis mais affiché.

## Gelé (interdit d'y toucher)
1. Le harnais d'évaluation : tâches, client simulé, notation par état final de la base.
2. Le sens des documents : on peut changer leur forme, jamais l'information qu'ils portent.
3. Les règles métier : vérification d'identité, procédures ; une écriture en base passe par les mêmes contrôles.
4. La machine : un seul GPU, rien d'externe pour l'agent (l'API de pointe ne sert que de repère, hors charge).
5. Pas de connaissance des tâches : aucune réponse, aucun cache, aucune règle écrite pour une tâche précise. Les optimisations se règlent sur une moitié des tâches et se mesurent sur l'autre moitié, jamais vue.
6. Répondre au client seulement après que l'action est enregistrée en base.
7. Un client refusé à l'entrée, abandonné ou coupé compte comme un échec, pas comme un client en moins.

## Libre (encouragé)
- Format des données : découper, indexer, transformer les fiches produits en tables, tant que c'est fait pour tous les documents et sans perte.
- Recherche documentaire : BM25, hybride, reranking, tant que ça tourne sur la machine.
- Prompts : ordre pour le cache du préfixe, descriptions d'outils raccourcies.
- Service du modèle : réglages vLLM, batching, cache du préfixe, FP8 natif.
- Architecture de l'agent : moins d'appels au modèle, routage, appels d'outils en parallèle, calculs faits par le code (« le modèle comprend, le code décide »), avec des outils génériques.

## Permis avec astérisque (déclaré, et soumis à la barrière de qualité)
- Quantification sous FP8, cache KV quantifié.
- Résumés de documents générés par un modèle.
- Décodage spéculatif.
- Troncature du contexte, délais d'abandon.

## Témoin de généralisation
- Le domaine retail, passé avant et après les optimisations, pour montrer qu'elles ne sont pas taillées pour la banque.

## Résolution
Adopté tel quel par Amir le 18/10.
