# G10 · décision · Les modèles réussissent trop peu au repos

**Statut :** tranché le 23/10 (option 1, plafond 15 dollars), criblage à lancer · **Né de :** nuit du P0 (mesures/P0-nuit-22-10.md)

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
