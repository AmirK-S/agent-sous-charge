# Cartes d'entretien

Une carte par notion apprise sur le projet. Recto : la question d'un tech lead. Verso : la réponse en quatre temps (contexte, choix et option écartée, ce que ça coûte, un chiffre tiré du projet).

---

## Carte 1 · FP8, BF16 : pourquoi servir le modèle en FP8 ? (19/10, P1.1)

**Recto** : « Vous servez Mistral Small 3.2 en FP8 sur une L40S. Pourquoi pas en BF16, et qu'est-ce que ça vous coûte ? »

**Verso**
- **Contexte** : un modèle de 24 milliards de paramètres sur une L40S de 48 Go (45 utilisables). Il faut loger les poids **et** le cache KV des conversations.
- **Choix et option écartée** : FP8 (1 octet par poids) plutôt que BF16 (2 octets). En BF16, 24 × 2 = 48 Go : ça ne rentre pas. Option écartée : une H100 de 80 Go, environ deux fois plus chère à l'heure.
- **Coût** : chaque poids est arrondi plus grossièrement, d'où un peu de qualité en moins, non mesurée sur notre banc. L'affirmation est donc délimitée (« ce modèle en FP8, sur cette carte ») et le repère de qualité est un modèle de pointe par API.
- **Chiffre** : poids FP8 = 23,6 Go ; il reste 14,9 Go de cache KV, soit 97 712 tokens.

**Les formats, en une image** : un nombre s'écrit comme en notation scientifique, chiffres × 10^puissance (la mantisse, puis l'exposant). Les bits se partagent entre les deux.
- FP = *floating point*, nombre à virgule flottante. BF16 = *brain float 16*, inventé chez Google Brain.
- FP16 : 5 bits de puissance, 10 de chiffres → précis, mais déborde vite (trop grand → erreur, trop petit → 0).
- BF16 : 8 bits de puissance, 7 de chiffres → moins précis, mais ne déborde presque jamais. Utile **à l'entraînement**, où les corrections des poids sont minuscules et tomberaient à 0 en FP16 (ce n'est pas « plus de précision », c'est « plus de plage »).
- FP8 : 8 bits en tout, très peu de chiffres. Utilisé **au service** pour gagner de la mémoire.
- **Facteur d'échelle** : on multiplie chaque matrice de poids pour qu'elle occupe au mieux les 8 bits, puis on divise au calcul. Comme mesurer une fourmi en millimètres plutôt qu'en mètres. Dans le journal vLLM : `fp8_per_tensor_static` (un facteur par matrice, calculé au chargement).

---

## Carte 2 · Le cache KV : pourquoi la taille des conversations décide du GPU (20/10, P1.3)

**Recto** : « Votre agent bancaire tourne sur une L40S. Combien de clients en même temps, et qu'est-ce qui lâche en premier quand vous en ajoutez ? »

**Verso**
- **Contexte** : pour écrire chaque token, le modèle relit tous les précédents. Le cache KV garde ses « notes de lecture » (vecteurs K et V) sur chaque token : 160 Ko par token pour Mistral Small 3.2 (40 couches × 8 têtes KV × 128 × 2 × 2 octets). Sans cache, une réponse de 100 tokens au bout de 14 000 coûterait environ 1,4 million de relectures au lieu de 14 100 : le cache transforme du calcul en mémoire.
- **Choix et option écartée** : vLLM ne réserve pas la place d'une conversation en attente (client qui réfléchit, outil qui répond) ; il garde ses notes tant qu'il y a de la place (cache des débuts de conversation) et jette les plus anciennes sous pression, puis les recalcule au tour suivant (relecture en parallèle, bien moins chère que l'écriture). Écarté : tout réserver (place bloquée par les clients lents) ou tout jeter (recalcul à chaque tour).
- **Coût** : sous charge, les recalculs et la file d'attente allongent d'abord **le temps de réponse** ; la réussite baisse ensuite, par les délais dépassés (patience du client) et le non-déterminisme du regroupement des requêtes. D'où la mesure de la qualité **sous charge**.
- **Chiffre** : L40S, 97 712 tokens de cache ; conversation bancaire médiane 14 822 tokens, soit 6,6 clients au plancher prudent (prédiction d'Amir : 15 000, juste). Mais 1,7 conversation sur 4 calculait en moyenne, et 74,5 % des tokens ont été retrouvés dans le cache : la vraie capacité est au-dessus du plancher, et ce sont les paliers de charge qui la diront.
