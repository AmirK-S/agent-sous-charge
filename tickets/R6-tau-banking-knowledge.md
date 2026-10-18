# R6 · recherche · Domaine banking_knowledge (et R4 : τ³-bench)

**Statut :** résolu le 18/10 (sous-agent, dépôt cloné et lu, rien exécuté ; clone supprimé)

## Résolution
- **τ³-bench = la version 1.0 du dépôt tau2-bench** (MIT, mars 2026) : ajoute le domaine bancaire à base de connaissances, la voix, et plus de 75 corrections. La 1.0.1 (16/07/2026) a corrigé la notation : ne comparer qu'à des résultats postérieurs. Dépôt actif (dernier commit 15/10/2026). R4 est donc résolu.
- **banking_knowledge** : support client d'une fintech (comptes, cartes, litiges, plafonds). Base de 17 tables ; environ 9 outils de lecture et 8 d'écriture visibles, plus de 49 outils « découvrables » à trouver dans la documentation puis débloquer.
- **Base documentaire** : 698 documents, environ 130 000 mots. Recherche au choix : BM25 (hors ligne, sans clé), embeddings OpenAI ou Qwen, grep, shell en lecture, ou contexte complet.
- **Tâches** : 97, sans découpage train/test. Notation : état final de la base pour 88 tâches, séquence d'actions pour 9.
- **Contre** : produit américain en dollars, sans cadre européen ; mise en place plus lourde que retail.
- **Recommandation du sous-agent** : banking_knowledge meilleur que retail pour banques et assureurs ; BM25 pour rester hors ligne ; retail en témoin comparable aux résultats publiés.
- **Conséquence technique** : la recherche documentaire allonge les contextes, donc le cache par conversation pèse plus lourd sur le GPU ; la L40S (G2) est à revérifier avec Gemma 4 31B.
