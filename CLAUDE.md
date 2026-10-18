# Agent sous charge

Expérience : combien de clients un agent bancaire avec outils (τ³-bench banking_knowledge) sert sur un seul GPU loué, en restant conforme aux critères de qualité du banc ; vidéo pour CTO ; apprentissage d'Amir (montée en charge, latence, coût, observabilité, déploiement).

Reprendre par `REPRISE.md` (contexte, décisions, état de l'infrastructure, prochaine action), puis `CARTE.md` (méthode Wayfinder : destination, frontière, brouillard), puis `PRE-ENREGISTREMENT.md` (protocole v3) et le ticket en cours dans `tickets/` (P1 au 18/10).

Règles : rien ne se loue sans l'accord d'Amir et une page de dépense ; GPU éteint hors séance ; les modèles et données lourdes vivent sur le pod, jamais sur le Bureau (synchronisé iCloud) ; Amir saisit lui-même toute clé ou identifiant ; chaque tranche se termine par Amir qui l'explique à l'oral.

## Méthode (obligatoire, détail dans `METHODE.md`)
1. **Un seul ticket par séance**, pris dans `CARTE.md` ; résolution écrite dans le ticket puis une ligne dans le journal de la carte. Une idée hors carte devient un ticket dans le brouillard, jamais traitée sur le moment. À deux fois la durée estimée, on s'arrête et on replanifie.
2. **La porte du tableau blanc** : une tranche n'est fermée que quand le contrôle technique passe **et** qu'Amir l'a expliquée à l'oral en quatre temps, enregistré. La tranche suivante ne démarre pas avant.
3. **Toute décision soumise à Amir** : la question en une phrase, un schéma tableau blanc de cinq lignes, deux ou trois options avec leur coût, une recommandation, les mots techniques définis. Amir la reformule avant qu'elle soit actée. Réversible : la recommandation s'applique en provisoire jusqu'au vendredi. Irréversible (dépense, gel, publication) : oui écrit d'Amir.
4. **Une micro-leçon par séance**, liée au travail du jour, dix minutes au plus ; prédiction d'Amir avant, comparaison après ; la notion devient une carte dans `apprentissage/cartes.md`.
5. **Briefing d'arrivée** de cinq lignes au plus quand Amir revient : fait, appris, micro-leçon, la seule décision qui l'attend, dépensé.
6. **Mode bas régime** si Amir le dit : seulement du travail sans décision.
