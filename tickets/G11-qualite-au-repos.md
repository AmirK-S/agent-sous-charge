# G11 · cuisine (avec Amir) · Les modèles réussissent trop peu au repos : que remet-on en cause ?

> Numéro G10 déjà pris le 18/10 (journal de la carte) : ticket renuméroté G11 le 23/10.

**Statut :** décision présentée à Amir le 23/10 (section « Décision », en bas), **en attente de sa reformulation** ; le criblage reste suspendu, rien n'a été dépensé · **Né de :** nuit du P0 (mesures/P0-nuit-22-10.md)

## La question
Au repos, sur les 40 tâches de développement, Mistral Small 3.2 réussit 4,5 % des conversations et Gemma 4 31B en réussit 6 %. Avec si peu de réussites, le critère « pas plus de 5 points de baisse sous charge » ne mesure presque rien. Que change-t-on ?

## Ce qu'on sait (23/10)
- L'examen est dur, même pour les modèles de pointe : 24,7 % pour gpt-5.2 en raisonnement élevé, 25,5 % dans l'article τ-Knowledge, 45 à 55 % pour les meilleurs modèles actuels (taubench.com, Artificial Analysis).
- On ne trouve aucun score publié pour de petits modèles ouverts sur cette partie bancaire.
- Notre erreur : nous avons choisi les modèles sur des scores d'outils généraux (R2, R7), sans chercher leur score sur banking_knowledge. Le 25 % de P1.3, obtenu sur 12 tâches faciles, nous a rassurés à tort.
- Rien n'est gelé : changer de modèle ou de critère reste propre, et ce n'est pas de la triche.

## Options
1. **Repère, puis criblage** (« criblage » : un essai rapide de quelques candidats, au repos seulement).
   - D'abord, un modèle de pointe par API sur les 40 tâches, avec notre harnais. C'était déjà prévu comme repère. Cela dit si notre harnais (BM25, prompt) plafonne.
   - Ensuite, deux ou trois modèles ouverts plus forts sur une H100, en spot (gpt-oss-120b, Mistral Small 4, Gemma avec réflexion).
   - Règle fixée à l'avance : si le meilleur modèle reste sous environ 15 %, on passe à l'option 2.
   - Coût : environ 10 à 15 dollars, et deux séances.
2. **Qualité descriptive.** On garde Mistral et Gemma ; l'affirmation porte sur la capacité et la latence, et la qualité est rapportée sans seuil. Coût : rien. Risque : un CTO demandera à quoi sert la capacité d'un agent qui échoue 95 fois sur 100.
3. **Changer de domaine** (retail, où les résultats publiés sont plus nombreux). Coût : une séance de mise en place. On perd le cadre bancaire, qui est la raison d'être de la vidéo.

## Recommandation
Option 1, avec l'option 2 comme repli fixé à l'avance.

## Résolution (23/10)
- **Reformulation d'Amir** : « soit le modèle change, soit le benchmark change ». L'option 2 est écartée (« ça sert à rien »). Le repli devient donc l'option 3, changer de banc.
- **Oui écrit d'Amir** : plafond de 15 dollars.
- **Changement de plan** : les candidats existent sur OpenRouter, donc le criblage se fait par API, sans louer de GPU. Réserve : le fournisseur de l'API ne quantifie pas forcément comme notre vLLM en FP8. Le criblage sert à choisir ; la mesure qui compte se refera sur notre carte.
- **Avant de retenir un modèle** : vérifier qu'il tient sur une seule carte. gpt-oss-120b tient sur une H100 (poids en 4 bits). Mistral Small 4 (119 milliards de paramètres) ne tient pas sur une H100 en FP8 : il faudrait du 4 bits, à tester.

### Page de dépense (prix OpenRouter lus le 23/10)
Base : 40 tâches × 1 essai ; environ 230 000 tokens d'entrée cumulés par conversation (mesuré sur Mistral), soit 9,3 millions par passe.

| Passe | Prix d'entrée (par million de tokens) | Estimation |
|---|---|---|
| Repère : Claude Sonnet 5.5 | 2 dollars (0,10 en cache) | 5 à 6 dollars (18 dollars sans cache : surveiller) |
| gpt-oss-120b | 0,15 dollar | 1,5 dollar |
| Mistral Small 4 (2603) | 0,15 dollar | 1,5 dollar |
| Gemma 4 31B, réflexion activée | 0,20 dollar | 2 dollars |
| Client simulé (toutes les passes) | | moins de 1 dollar |
| **Total** | | **environ 11 dollars, plafond 15** |

- **Garde-fou** : relever la dépense OpenRouter après les 10 premières conversations du repère, et couper si la projection dépasse 8 dollars.
- **Règle fixée à l'avance** : si le meilleur modèle ouvert reste sous environ 15 %, on passe à l'option 3.

## Diagnostic gratuit (23/10, après la remise en question d'Amir)
- **Ce que d'autres ont mesuré** (taubench.com, partie bancaire) : gros modèles ouverts avec recherche par le sens : 9,8 % ; GPT-5.2 : 12,6 % avec la recherche par le sens seule, 32,2 % en « alltools » (mots-clés, sens et terminal ; réglage par défaut de τ³). Le criblage de petits modèles aurait donc très probablement confirmé ce qu'on savait déjà : il est suspendu.
- **« alltools » par API contredit G9** (« tant que ça tourne sur la machine ») : écarté. Le terminal pose aussi une question de sécurité pour une banque.
- **Mesure sur nos conversations de la nuit** : chaque tâche liste ses documents requis (`required_documents`, 10 en médiane). On compte ceux que l'agent a vus passer dans ses résultats de recherche.

| Part des documents requis trouvée | Mistral (réussies / notées) | Gemma |
|---|---|---|
| 80 % ou plus | 5 / 9 | 0 / 1 |
| 40 à 80 % | 2 / 56 | 0 / 18 |
| moins de 40 % | 0 / 89 | 3 / 31 |

- **Corrigé le 23/10 (revérification, plus bas)** : les 5 réussites du haut du tableau viennent de tâches à 1 ou 2 documents requis, dont 4 sont des « transferts à un humain ». La lecture qui suit ne tient pas.
- **Lecture pour Mistral** (périmée) : quand l'agent trouve les documents, il réussit plus d'une fois sur deux ; sinon, presque jamais. Le goulot est la recherche avant le modèle. Réserves : c'est une corrélation (les tâches faciles demandent peut-être moins de documents), et c'est le modèle qui choisit ses requêtes. Gemma : trop peu de données, et 3 réussites avec peu de documents, à regarder.
- **Piste conforme à G9** : une recherche hybride sur la machine (mots-clés et sens, petit modèle d'embeddings servi localement, reclassement éventuel). C'est ce que ferait une banque réelle. Le coût est en mémoire de la carte, ce qui intéresse l'étude.

## Deuxième diagnostic gratuit (23/10) : l'agent cherche trop peu
- Une tâche demande **10 documents en médiane** (de 1 à 30). L'agent fait **2 recherches en médiane** (moyenne 3,2 ; 6 conversations sans aucune recherche), autant dans les réussites que dans les échecs. Gemma : 1 à 2.
- Exemple, `task_010` (bonus de parrainage versé pour 2 amis sur 4) : 2 documents requis, 2 recherches, 1 document trouvé, note 0.
- **Lecture** : il y a trois maillons, à mesurer séparément.
  1. Le moteur de recherche : trouve-t-il les documents quand la requête est bonne ? (rappel à 10, mesurable hors ligne, sans GPU)
  2. La façon de chercher de l'agent : combien de recherches, quelles requêtes (le prompt et le modèle).
  3. Le raisonnement une fois les documents trouvés : 5 réussites sur 9 pour Mistral, un premier plafond.
- **Conséquence** : changer seulement de moteur de recherche ne suffira pas si l'agent ne cherche que deux fois. Et changer seulement de modèle ne dit pas lequel des trois maillons on a réparé.

## Ce que dit l'article de référence (τ-Knowledge, arXiv 2603.04370, lu le 23/10)
Réussite au premier essai sur la partie bancaire, modèles de pointe :

| Recherche | Moyenne de 6 modèles | GPT-5.2 avec raisonnement | GPT-5.2 sans raisonnement |
|---|---|---|---|
| Documents fournis (« or ») | 32,2 % | 32,7 % | 15,7 % |
| BM25 | 17,0 % | 24,5 % | 9,5 % |
| Embeddings (OpenAI, Qwen) | 16,9 à 17,1 % | 23,5 à 24,7 % | 8,3 à 12,4 % |
| Terminal (grep) | 19,2 % | 25,5 % | 11,6 % |
| Sans aucune recherche | environ 2 % | | |

- **Le moteur de recherche compte peu** : BM25 vaut les embeddings ; reclassement, taille k et modèle d'embeddings : « pas d'amélioration significative, ou une dégradation ». Le terminal gagne un peu, surtout pour les modèles de pointe à raisonnement.
- **Le raisonnement compte beaucoup** : GPT-5.2 passe de 9,5 % à 24,5 % avec BM25 rien qu'en activant le raisonnement.
- **Plafond** : même avec les bons documents fournis, les modèles de pointe ne font que 32 à 40 %.
- **Nombre de recherches** : 9 à 18 par tâche pour les modèles de pointe ; notre agent en fait 2.
- **Conséquences** : (1) l'étape « recherche hybride » de l'option A est abandonnée ; BM25 reste, il est réaliste et à niveau ; (2) le levier à tester est le **raisonnement** (Gemma 4 avec réflexion, gpt-oss-120b, Mistral Small 4), qui coûte des tokens générés, donc de la capacité : c'est un vrai compromis pour la vidéo ; (3) même au mieux, la réussite au repos sera modeste (de l'ordre de 10 à 25 %) : le critère « pas plus de 5 points de baisse » est à revoir pour sa puissance statistique (ticket à ouvrir).

## Revérification depuis les fichiers (23/10, nouvelle séance)
Séance reprise sans se fier aux conclusions précédentes. Scripts : `outils/diagnostic_g11.py` (nos données), `outils/puissance_g11.py` (puissance). Rien dépensé.

### 1. Ce que d'autres ont mesuré sur banking_knowledge
Attention aux versions : la notation v1.0.1 (juillet 2026) a relevé certains scores de 5 à 9 points ; les chiffres de l'article sont d'avant. Notre τ³ (commit 96a3ef92) est en v1.0.1.

| Modèle | Ouvert ? | Réglage | Réussite (pass^1) | Source |
|---|---|---|---|---|
| Mistral Large 2512 (675 milliards de paramètres) | oui | BM25, agent standard, v1.0.1 | **6,4 %** (13 tâches sur 97 réussies au moins une fois) | arXiv 2607.22157, tableau 1 |
| GLM-5, Qwen3.5-397B, réflexion activée | oui | embeddings | 9,8 % | classement taubench.com |
| GPT-4o, GPT-4.1 | non | BM25, avant v1.0.1 | 9,0 et 9,3 % | article τ-Knowledge, annexe G, tableau 12 |
| GPT-5.2 sans raisonnement | non | BM25 / embeddings | 9,5 % (avant v1.0.1) ; 12,6 % (v1.0.1) | article ; classement |
| GLM-5.2, Kimi K3, réflexion maximale | oui, mais 10 fois trop gros pour une carte | alltools | 37,1 % | classement |
| Meilleurs modèles de pointe | non | alltools | 45 à 55 % | classement |
| Sans aucune recherche | | | environ 2 % | article, tableau 6 |

- **Aucun résultat publié pour un modèle qui tient sur une carte** (Mistral Small, Gemma 4, gpt-oss) : ni dans l'article, ni dans les 91 soumissions du classement (vérifiées le 23/10), ni dans la littérature trouvée.
- L'article confirme (annexe F) : moteur de recherche, reclassement et taille k ne changent rien de significatif ; le raisonnement change beaucoup ; même avec les bons documents fournis, la pointe plafonne à 32 à 40 %.
- Écart relevé : l'article annonce 18,6 documents requis par tâche ; les données v1.0.1 en donnent 9,8 en moyenne sur les 97 tâches.

**Ailleurs, un banc bancaire où les modèles d'une carte réussissent** : TauIndianBankBench (NPCI, arXiv 2610.30161, septembre 2026 ; code MIT sur `github.com/npci/TauIndianBankBench`, données MIT sur Hugging Face). Construit sur le harnais τ², 1 000 tâches, 33 outils donnés d'emblée, politique écrite fournie, 24 documents, chaînes de 3,5 appels en moyenne, notation par état final et appels requis. Réussite : Gemma 4 31B 77,6 %, Gemma 4 26B-A4B 71,4 %, Gemma 4 12B 69,9 %, Qwen3.8-27B 84,9 % (client simulé MiniMax-M2.7). Mistral non testé.
Pour mémoire : Gemma 4 31B avec réflexion annonce 86,4 % sur τ² retail (chiffre de Google, non vérifié).

### 2. Ce que disent nos données (revérifié)
- Mistral : 7 réussites sur 154, sur 5 tâches (007, 010, 014, 033, 034). **5 des 7 réussites sont des tâches où la bonne réponse est de transférer à un humain** (014, et les « speedbump tests » 033 et 034). Opérations bancaires réussies : **2 sur 154 (1,3 %)**. Gemma : 3 sur 50, dont `task_034` réussie sans aucune recherche.
- Le tableau « 80 % des documents trouvés → 5 sur 9 » ne porte que sur 033, 034 et 010, des tâches à 1 ou 2 documents requis. Il mesure la facilité de la tâche, pas le moteur. **Le diagnostic « le goulot est la recherche » ne tient pas.**
- Documents requis trouvés : 35 % (Mistral), 31 % (Gemma). L'article : 28 à 31 % pour GPT-5.2 sans raisonnement, 44 à 62 % avec. Recherches par conversation : 3,3 en moyenne (Mistral), 1,8 (Gemma) ; GPT-5.2 sans raisonnement : 4,0 ; avec : 18 à 20.
- **Lecture** : notre harnais n'est pas en cause. Mistral Small à 4,5 % est au niveau de Mistral Large à 6,4 % dans le même réglage, et de GPT-5.2 sans raisonnement. C'est la classe de modèle face à ce banc, et le raisonnement est ce qui manque.

### 3. Puissance du critère de qualité (section 5 du pré-enregistrement)
Hypothèses : 57 tâches, 3 passages, donc 3 conversations appariées par tâche ; rejet de « Δ ≤ −5 points » au seuil unilatéral de 2,5 % ; écart entre tâches calé sur GPT-5.2 (pass^1 24,5 %, pass^4 10,3 %). Probabilité de certifier conforme (objectif du protocole : 80 %) :

| Repos | Vraie baisse 0 | Vraie baisse 2 points | Conversations par tâche pour 80 % à baisse nulle |
|---|---|---|---|
| 10 % | 63 % | 31 % | environ 5 |
| 15 % | 49 % | 23 % | environ 6 à 7 |
| 25 % | 36 % | 16 % | environ 10 |

- **À 4,5 %, le critère ne peut presque pas échouer** : la réussite ne peut pas baisser de plus de 4,5 points. Un agent qui tombe à 0 % sous charge est certifié conforme 3 fois sur 10.
- La marge de 5 points est absolue : à 10 % de repos, elle tolère de perdre la moitié des clients servis correctement.
- L'erreur types naïve rend le test trop permissif à ces taux (4 à 14 % de faux « conforme » au lieu de 2,5 %) : la méthode exacte devra être validée par simulation, comme le prévoit la section 7.
- **Quel que soit le banc**, 3 conversations par tâche ne suffisent pas : il faut redimensionner (plus de répétitions, ou plus de tâches).

### 4. Ce qui ferait tomber la recommandation (cherché activement)
- **Un modèle d'une carte avec réflexion pourrait dépasser 15 % sur banking_knowledge.** Personne ne l'a mesuré. Contre : GLM-5 et Qwen3.5-397B avec réflexion font 9,8 %, Mistral Large 6,4 %. Pour : GLM-5.2 est passé à 37 % en une génération (mais en alltools, réflexion maximale, dix fois plus gros). Test qui trancherait : gpt-oss-120b et Gemma 4 avec réflexion, 40 tâches par API, 2 à 4 dollars.
- **TauIndianBankBench est jeune** (un mois, une seule institution, 6 étoiles) ; ses auteurs n'ont pas mesuré les erreurs de leur client simulé ; avec GPT-6 Luna, les scores seront différents.
- **Il est plus facile** : 24 documents et la politique fournie, donc la recherche pèse peu ; conversations plus courtes, donc une capacité plus haute qu'avec banking_knowledge et moins comparable à P0. Mais c'est aussi plus proche d'un vrai service client, où l'agent connaît la politique.
- **Il est indien**, pas européen ; Mistral n'y a pas de score publié ; son harnais embarqué est une version de τ² à confronter à notre serveur MCP.
- Le passage à un autre banc ne règle pas G2 : Gemma ne tient pas sous charge sur L40S.

## Décision soumise à Amir (23/10)

**La question** : banking_knowledge est hors de portée de tout modèle qui tient sur une carte ; change-t-on de banc, de modèle, ou les deux ?

**Le schéma tableau blanc**
```
banking_knowledge : pointe 45-55 % | ouverts géants 6-10 % | nous 4,5 % | sans recherche 2 %
→ notre harnais est à niveau : c'est la classe de modèle, pas le moteur de recherche
critère « −5 points » : à 4,5 % il ne peut pas échouer ; à 10-25 %, 36 à 63 % de puissance (visé 80)
banc bancaire où un modèle d'une carte réussit : TauIndianBankBench (Gemma 4 31B : 78 %)
donc : on change de banc, on garde la banque et l'outillage ; le critère se redimensionne
```

**Les options**
1. **Changer de banc, garder la banque : TauIndianBankBench.** banking_knowledge reste dans la vidéo en séquence descriptive (« le banc de Sierra : la pointe à 55 %, nous à 4,5 % »), avec les données déjà payées. Coût : vérification gratuite d'abord (code, harnais, compatibilité MCP, tâches lues), puis 2 à 3 séances d'intégration et un repos sur GPU (environ 3 à 5 dollars, plus tard, page de dépense) ; pré-enregistrement à réécrire (banc, découpage, estimand). Risque : banc jeune.
2. **Garder banking_knowledge, ajouter le raisonnement** (gpt-oss-120b, Gemma 4 avec réflexion), par API, avec la règle déjà fixée : sous 15 %, on passe à l'option 1. Coût : 2 à 4 dollars, une séance. Les quatre mesures publiées prédisent 6 à 10 %.
3. **Changer pour τ² retail ou telecom** (Sierra, connu des CTO, classement officiel, déjà dans notre τ³). Coût : 1 à 2 séances. On perd la banque.

**Recommandation** : option 1, avec l'option 3 en repli si la vérification gratuite échoue. C'est la seule qui garde la banque et donne un repos où le critère peut mesurer une baisse. L'option 2 dépenserait pour confirmer, très probablement, ce que quatre mesures disent déjà. Dans tous les cas, un ticket à part redimensionne le critère (répétitions ou nombre de tâches) avant le gel.

**Ce qui la ferait changer** : un score mesuré ou publié d'au moins 15 % pour un modèle d'une carte sur banking_knowledge (on passerait à l'option 2) ; un harnais embarqué incompatible avec notre serveur MCP ou des tâches défectueuses (option 3) ; Amir qui juge qu'une banque indienne ne parle pas à un CTO européen (option 3).

**Réversible** : oui, aucune dépense. En attendant le vendredi, la recommandation s'appliquerait en provisoire, limitée à la vérification gratuite.

**Les mots**
- *Banc* : le jeu de tâches et la façon de les noter.
- *pass^1* : la part des conversations réussies au premier essai.
- *Réflexion (raisonnement)* : le modèle écrit un brouillon avant de répondre ; plus de tokens générés, donc moins de clients par carte.
- *alltools* : réglage du classement où l'agent a mots-clés, sens et terminal en même temps.
- *Puissance* : la probabilité que le test dise « conforme » quand l'agent l'est vraiment.
- *Marge de non-infériorité* : la baisse tolérée (ici 5 points) avant de dire « moins bon ».
- *Speedbump* : tâche piège où l'agent doit d'abord aider, puis transférer à un humain si le client insiste.

**Décisions anciennes rouvertes (règle 8)** : le cas d'usage banking_knowledge (R6, 18/10) ; les sections 3 à 5 et 7 du pré-enregistrement. La mention « recherche BM25 seul remise en cause » est retirée : le moteur n'est pas en cause. Le oui de 15 dollars pour le criblage n'est pas utilisé.

**Micro-leçon proposée** (puissance statistique, dix minutes) : prédiction d'Amir avant : « si l'agent réussit 15 % au repos et 15 % sous charge, sur 100 campagnes de 3 conversations par tâche, combien le test certifie-t-il conforme ? » Réponse : environ 49.

**Reformulation d'Amir** : en attente.
