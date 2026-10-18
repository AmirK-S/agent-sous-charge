# R5 · recherche · Ce que les grands groupes européens veulent tester

**Statut :** résolu le 18/10 (sous-agent ; sources surtout secondaires, à relire avant toute citation publique)

## Résolution
- **Hébergement interne réel** : BNP Paribas et Mistral, partenariat depuis 07/2024, déploiement « dans notre infrastructure » (on-premise non confirmé) ; Albert (DINUM) sur modèles ouverts, SecNumCloud ou serveur local, testé dans une trentaine de France Services. Rien de trouvé sur AXA, BPCE, Société Générale.
- **Contraintes** : DORA (19 prestataires TIC critiques désignés le 18/11/2025), AI Act haut risque (crédit, assurance) au 02/08/2026 (texte primaire non vérifié). DeepSeek bloqué ou restreint (Italie, Berlin, Pays-Bas) pour l'application hébergée ; aucune restriction trouvée sur Qwen, mais l'objection reste probable. **Licence Llama 4 : exclurait les entreprises établies dans l'UE** (à confirmer sur la licence).
- **Adoption** : Banque de France 2026, 67 % des entreprises de 20 salariés et plus utilisent l'IA générative, surtout en expérimental ; EY, 11 % des services financiers prêts pour l'AI Act ; banques et assureurs déploient des agents pour la fraude et le traitement des demandes (Capgemini 2026).
- **Dimensionnement** : la mémoire de cache par session domine en contexte long ; rentabilité d'un GPU vers 60-70 % d'utilisation ; exploitation = 1,3 à 2 fois le coût GPU (blogs de fournisseurs).
- **Vide confirmé** : aucun banc indépendant de fiabilité sous charge pour des agents avec outils.
- **Conclusion** : cas d'usage = agent de traitement de dossiers ou de service client avec outils sur données internes ; question = « combien de conversations simultanées sur un GPU avant que la réussite des appels d'outils chute ou que la latence dépasse le seuil », comparée au coût d'une API ; modèle européen ou de licence claire, Mistral en priorité.
