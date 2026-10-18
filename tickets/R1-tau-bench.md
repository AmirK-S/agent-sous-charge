# R1 · recherche · τ-bench ou τ²-bench

**Statut :** résolu le 18/10 (sous-agent, dépôts clonés et lus ; benchmarks non lancés) · **Débloque :** G4, G5

## Question
Licence, domaines, nombre de tâches, outils, notation (état final de la base, pass^k), fonctionnement du client simulé et son coût, possibilité de brancher un modèle servi par vLLM, possibilité d'exposer les outils par MCP.

## Résolution
- **Licence** : MIT pour τ-bench et τ²-bench. Le README de τ-bench dit ses tâches périmées et renvoie vers un « τ³-bench » (non lu, à vérifier).
- **τ²-bench retail** : 114 tâches (74 train, 40 test), une quinzaine d'outils (dont 6 d'écriture), base de 500 clients, 1 000 commandes, 50 produits.
- **Notation** : récompense = état final de la base × communication des informations exigées ; une autre trajectoire qui aboutit au même état passe. pass^k implémenté dans `metrics/agent_metrics.py`.
- **Référence publiée (τ-bench retail, pass^1)** : claude-3.5-sonnet 0,692 (pass^4 0,462) ; gpt-4o 0,604 (pass^4 0,383).
- **Client simulé** : LLM, gpt-4.1 par défaut dans τ² ; un tour = un appel ; coût par tâche non publié. Modes sans LLM : `dummy_user` (τ²), `human` (τ-bench). Pas de dialogues rejoués.
- **vLLM** : τ² passe par LiteLLM, donc une API compatible OpenAI devrait marcher (non vérifié).
- **MCP** : aucun portage ; faisable, puisque la notation ne regarde que l'état final de la base (un serveur MCP qui encapsule l'environnement).
- **Concurrence** : `--max-concurrency` (3 par défaut), prévu pour accélérer l'évaluation, pas pour mesurer.
- **Recommandation** : τ²-bench, retail, 40 tâches de test. Le client simulé ne doit pas tourner sur le GPU testé : il passe par une API (coût à chiffrer en G5) ou un petit modèle ailleurs.
