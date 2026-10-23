# Méthode de travail

> Écrite le 18/10/2026 avec Amir. S'applique à toute session qui travaille sur ce projet. Base : la méthode de Matt Pocock (carte Wayfinder, un ticket par séance, tranches verticales, vérification à chaque tranche), adaptée à la situation d'Amir.

## Le but, et le piège

Deux objectifs à tenir ensemble :
1. **Livrer** l'expérience et la vidéo.
2. **Qu'Amir possède chaque décision** et sache l'expliquer à tout moment sur un tableau blanc, face à un CTO ou un tech lead. C'est la condition des missions à 800 €/j.

Le piège, connu d'Amir lui-même : il veut aller vite et droit au but, il passe d'un contexte à l'autre (mission, prospection, projet), et il n'a pas envie, sur le moment, d'apprendre ce qui ne l'attire pas. Laissé à lui-même, le projet avancerait et Amir resterait derrière. La méthode est faite pour que **ce soit le système qui bloque, pas sa volonté**.

## Règle 1 : la porte du tableau blanc

Une tranche n'est fermée que quand elle a ses **deux** validations :
- **Technique** : le contrôle prévu dans le ticket passe (test vert, chiffre mesuré).
- **Amir** : il explique la tranche et ses décisions en quatre temps (contexte, choix et option écartée, ce que le choix coûte, un chiffre), à voix haute, enregistré, sans support. Si l'explication bute, on reprend le point flou ; la porte reste fermée.

**La tranche suivante ne démarre pas tant que la porte est fermée.** Une session peut préparer la suite (recherche, lecture), jamais l'exécuter.

## Règle 2 : chaque décision arrive prête à être possédée

Toute décision soumise à Amir arrive sous cette forme, dans le ticket :
- **La question**, en une phrase.
- **Le schéma tableau blanc** : cinq lignes au plus, ou un petit dessin, que Amir pourrait refaire de mémoire.
- **Les options** (deux ou trois), chacune avec ce qu'elle coûte.
- **La recommandation**, et pourquoi.
- **Les mots techniques définis** au passage, en une ligne chacun.

Amir **reformule** la décision avant qu'elle soit actée (une ou deux phrases, à l'écrit ou à l'oral). S'il n'y arrive pas, c'est que la décision est mal expliquée : la session simplifie, elle ne passe pas outre.

**Réversible ou irréversible.** Une décision réversible (un réglage, l'ordre des tickets) peut attendre la revue du vendredi ; en attendant, la recommandation s'applique et c'est noté « provisoire ». Une décision irréversible (une dépense, le gel du protocole, une publication) attend toujours le oui écrit d'Amir.

## Règle 3 : apprendre au moment où ça sert

Amir n'a pas envie d'apprendre « en général » ; il apprend quand il en a besoin tout de suite. Donc :
- **Une micro-leçon par séance, liée au travail du jour** : la notion exacte dont la décision ou la tranche du jour dépend (par exemple le cache KV le jour où l'on mesure sa taille). Dix minutes au plus, avec un exemple concret tiré du projet, pas de cours.
- **Prédire avant, comparer après** : en début de séance, Amir écrit une prédiction en une ligne (« je pense que la L40S suffira ») ; en fin de séance, on la compare au résultat. Se tromper est le moteur.
- **Chaque notion apprise devient une carte d'entretien** (question d'un tech lead au recto, réponse en quatre temps au verso), rangée dans `apprentissage/cartes.md`. Le gain est immédiat et visible : une réponse de plus pour un entretien à 800.
- **Le tableau de niveau** (`apprentissage/niveau.md`) : les postes clés (architecture, montée en charge, déploiement, CI/CD, évaluations, incidents, sécurité, travail en équipe, données, API, coût et latence), chacun noté après chaque simulation. Amir voit sa progression vers le niveau visé.

## Règle 4 : la carte est le seul tableau de bord

- Toute séance part **d'un seul ticket** de `CARTE.md` et se termine en écrivant sa résolution dans le ticket, puis une ligne dans le journal de la carte.
- **Une idée hors carte n'est jamais traitée sur le moment** : elle devient un ticket dans le brouillard.
- **Chaque ticket a une durée estimée ; à deux fois l'estimation, on s'arrête** et on replanifie avec Amir.
- **Le briefing d'arrivée** : quand Amir revient sur le projet, la session lui donne en cinq lignes au plus ce qui a été fait, ce qui a été appris, la micro-leçon du jour, la seule décision qui l'attend avec sa recommandation, et ce qui a été dépensé. Pas plus : il arrive souvent d'un autre contexte.

## Règle 5 : moins de changements de contexte

- **Un créneau fixe par jour pour le projet**, de préférence le même, que la mission et la prospection ne grignotent pas. Hors créneau, les sessions ne sollicitent pas Amir, sauf blocage réel.
- **Les décisions non urgentes se regroupent** dans la revue du vendredi.
- **Mode bas régime**, les jours de fatigue ou de surcharge : Amir lit le briefing et fait son enregistrement de deux minutes, rien d'autre. Ce jour-là, les sessions ne font que du travail sans décision (recherche, lecture de code, tests, préparation) ; le projet avance mais ne prend aucun virage.

## Règle 6 : la revue du vendredi, 30 minutes

1. **Signal ou bruit** : ce qui a rapproché de la destination, et ce qui n'était que du mouvement.
2. **Les décisions regroupées**, chacune reformulée par Amir.
3. **Une simulation hostile** sur ce qui a été construit dans la semaine (un agent joue le tech lead, jusqu'à la troisième relance) ; les questions ratées deviennent des cartes.
4. **La carte ajustée** et le tableau de niveau mis à jour.

## Règle 7 : les revues adverses aux grands jalons seulement

Avant le gel du protocole, à la fin du pilote, avant toute publication. Par un modèle d'une autre famille, appelé seul (la revue d'Astra seul a été la plus utile : elle a retiré de l'inutile coûteux). Pas à chaque étape.

## Règle 8 : la preuve avant la recommandation (ajoutée le 23/10)

Écrite après une erreur : 15 $ de criblage de modèles proposés le 23/10 sans avoir lu le classement officiel du banc, qui donnait déjà la réponse.
- **Avant toute recommandation qui dépense ou qui change de cap**, deux vérifications, écrites dans le ticket : *ce que d'autres ont déjà mesuré* (classement, article, dépôt) et *ce que nos propres données disent déjà* (diagnostic gratuit).
- **Une décision qui en contredit une ancienne rouvre l'ancienne** dans la carte (« remise en cause le … »), au lieu de la contourner en silence.
- **Une remise en question d'Amir n'est pas un ordre de changer d'avis.** La session garde sa recommandation si la preuve la soutient, et dit ce qui la ferait changer.

## Règle 9 : la fin de séance (ajoutée le 23/10)

Avant de rendre la main, la session coche :
1. La résolution ou l'état est écrit dans le ticket.
2. Une ligne dans le journal de `CARTE.md` ; la frontière et le brouillard sont à jour (rien de fait ne reste « ouvert », rien d'ouvert n'est oublié).
3. `REPRISE.md`, section « État », est réécrite : fait, ticket en cours, ce qui tourne, dépensé, prochaine action.
4. Un numéro de ticket nouveau est vérifié contre la carte et le journal (pas de doublon).
5. Commit et push.
