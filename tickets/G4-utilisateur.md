# G4 · cuisine · Ce qu'est un utilisateur : temps de réflexion et patience

**Statut :** préparé le 21/10, à trancher par Amir. Débloque G6 (seuils) et le scénario de charge du pilote.

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

## Résolution
_à remplir par Amir (reformulation)_
