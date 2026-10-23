# G11 · cuisine (avec Amir) · Les modèles réussissent trop peu au repos : que remet-on en cause ?

> Numéro G10 déjà pris le 18/10 (journal de la carte) : ticket renuméroté G11 le 23/10.

**Statut :** rouvert le 23/10 : le criblage est suspendu, rien n'a été dépensé (voir « Diagnostic ») · **Né de :** nuit du P0 (mesures/P0-nuit-22-10.md)

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

- **Lecture pour Mistral** : quand l'agent trouve les documents, il réussit plus d'une fois sur deux ; sinon, presque jamais. Le goulot est la recherche avant le modèle. Réserves : c'est une corrélation (les tâches faciles demandent peut-être moins de documents), et c'est le modèle qui choisit ses requêtes. Gemma : trop peu de données, et 3 réussites avec peu de documents, à regarder.
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
