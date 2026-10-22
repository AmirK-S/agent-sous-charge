# G4 · cuisine · Ce qu'est un utilisateur : temps de réflexion et patience

**Statut :** recommandation appliquée **en provisoire** le 22/10 (décision réversible avant le gel), à confirmer à la revue du vendredi.

## La question
Entre deux messages, combien de temps le client simulé « réfléchit-il » avant de répondre ? C'est ce temps qui décide combien de conversations la carte peut tenir ouvertes : plus il est long, plus la carte sert de clients à la fois.

## Le schéma
```
l'agent répond  →  le client lit la réponse  →  il tape son message  →  il envoie
                   (238 mots/min)              (36 mots/min, mobile)
pendant ce temps, la carte sert les autres clients
```

## Ce que disent les mesures de P1.3 (12 conversations) et les sources de G6
- Réponse de l'agent : 40 mots en médiane (145 au p90) → **lecture d'environ 10 s** à 238 mots/min (Brysbaert 2019, 190 études).
- Message du client simulé : 30 mots en médiane (48 au p90) → **frappe d'environ 49 s** à 36 mots/min (Palin et al. 2019, 37 370 personnes, sur mobile).
- Total réaliste : **environ une minute** entre deux messages. L'intervalle provisoire de 5 à 20 s est environ trois fois trop court.
- Nuance : le client simulé (un LLM) écrit probablement plus long qu'un vrai client de banque, ce qui gonflerait le temps de frappe.

## Les options
1. **Temps calculé à chaque tour** (recommandée) : lecture de la réponse réelle à 238 mots/min + frappe du message réel à 36 mots/min + une pause tirée entre 2 et 5 s. Réaliste et justifiable par des sources. Coût : un peu de code dans le harnais (attendre avant d'envoyer chaque message du client). Avec une analyse de sensibilité « client pressé » (5 à 20 s, l'ancienne valeur), pour montrer l'effet.
2. **Intervalle fixe de 5 à 20 s** : simple, et prudent pour le serveur (il envoie plus de messages qu'un humain), donc la capacité annoncée est un plancher. Coût : on sous-estime probablement la capacité d'un facteur deux à trois, et il faut l'écrire noir sur blanc.
3. **Temps calculé, mais frappe plafonnée** (par exemple 15 mots, longueur typique d'un message de chat) : corrige la verbosité du client simulé. Coût : le plafond est un choix de plus, peu sourcé.

**Recommandation : l'option 1**, avec l'option 2 en sensibilité. Elle colle à des données publiées, et les deux résultats encadrent la réalité.

## Patience
30 s par tour avant abandon (données d'éditeurs de chat, faibles), avec sensibilité à 15 s et 60 s. Voir [G6](G6-seuils.md).

## Les mots
- **Temps de réflexion** : le délai entre la réponse de l'agent et le message suivant du client.
- **Analyse de sensibilité** : refaire la mesure avec une autre hypothèse pour voir si la conclusion change.

## La peur d'Amir (22/10) : « payer la carte pendant que les clients réfléchissent »
`X` = la carte calcule pour ce client ; `.` = le client lit ou tape.
```
3 clients :  la carte  X X X . . X X X . . X X X . .   ← elle attend 40 % du temps
5 clients :  la carte  X X X X X X X X X X X X X X X   ← elle ne s'arrête jamais
```
Le banc ajoute des clients jusqu'à ce que la carte ne s'arrête plus. Des clients lents demandent **plus de clients** (environ 60 au lieu de 15), pas plus de temps de carte : on paie la fenêtre de mesure, pas la réflexion. Les faux clients ne coûtent presque rien pendant qu'ils « réfléchissent ».
La carte n'attend vraiment qu'au début (remplissage) et à la fin (vidage) d'une séance ; **l'escalier continu** (monter d'un palier à l'autre sans vider) réduit ce coût à un seul remplissage et un seul vidage par séance.
Les mesures au repos (partie 1 du pilote) n'en dépendent pas : clients joués sans temps de réflexion.

## Résolution provisoire (22/10)
Temps de réflexion **calculé** (lecture 238 mots/min, frappe 36 mots/min, pause 2 à 5 s) pour le chiffre officiel ; client pressé (5 à 20 s) pour les essais de réglage et en sensibilité ; escalier continu pour ne payer qu'un remplissage et un vidage par séance.
Compréhension d'Amir, à ses mots : « vLLM jette le cache inutilisé, donc les clients lents ne bloquent pas la carte ; ça se répercute sur le temps de réponse ». Il ne l'a pas formulée comme une décision : à confirmer vendredi.
