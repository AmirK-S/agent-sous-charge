# R9 · recherche · Le code d'évaluation et le client simulé de τ³-bench

**Statut :** résolu le 18/10 (sous-agent, commit 96a3ef92 lu, version 1.0.1 ; clone supprimé)

## Résolution
- **Récompense banking** : 88 tâches notées sur la base (rejeu des appels d'écriture de l'agent et des actions dorées sur deux environnements neufs, hash comparés), 9 sur la présence des actions dorées (ordre libre, arguments stricts). Toute fin autre que AGENT_STOP ou USER_STOP vaut 0 (MAX_STEPS, TIMEOUT, TOO_MANY_ERRORS). Horloge figée, identifiants déterministes.
- **Faux échecs possibles** : ordre des écritures quand l'état en dépend, écriture en trop.
- **pass^k** : comb(c,k)/comb(n,k) par tâche puis moyenne ; INFRASTRUCTURE_ERROR exclus et k ramené au minimum observé ; TIMEOUT compté en échec.
- **Client simulé** : gpt-4.1-2025-04-14, température 0, graine 300 ; jetons d'arrêt ###STOP###, ###TRANSFER###, ###OUT-OF-SCOPE### ; plafond 200 messages, 10 erreurs. Aucun taux d'erreur publié ; un juge LLM « user only » classe ses erreurs (evaluator/review_llm_judge_user_only.py).
- **Orchestration** : boucle synchrone ; agent branché par LiteLLM (api_base compatible OpenAI) sans toucher à la notation. Un serveur MCP doit exposer exactement les mêmes noms, arguments et sorties d'outils (rejeu strict, sinon exception puis relance de la conversation).
- **Délais** : seulement à l'échelle de la conversation, vérifiés entre deux pas ; aucun délai par appel ; LiteLLM relance 3 fois ; une exception relance la conversation entière jusqu'à 3 fois puis la classe INFRASTRUCTURE_ERROR, exclue.
- **Concurrence** : ThreadPool (--max-concurrency, --workers) ; httpx limité à 10 connexions ; isolation de la base par conversation.
- **BM25** : rank_bm25 par défaut, top_k 10, index reconstruit environ 4 fois par conversation ; required_documents (1 à 30 documents par tâche) non noté par le code, à croiser avec les « ID: » des sorties d'outil.
- **1.0.1** : notation banking modifiée (lectures en trop ignorées, jusqu'à +9 points de pass^1), tâches 074 et 077 à 086 corrigées ; comparer seulement à des résultats 1.0.1.
- **Risques** : relances silencieuses qui masquent des échecs ; TIMEOUT à 0 mais erreurs d'infrastructure exclues (biais sous charge) ; pas de délai par appel ; température 0 non déterministe sous batching vLLM ; reconstruction BM25 coûteuse en CPU ; épingler commit, version et variante de recherche.
