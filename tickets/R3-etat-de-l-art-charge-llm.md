# R3 · recherche · État de l'art des tests de charge d'agents

**Statut :** résolu le 18/10 (sous-agent, sources à relire avant de les citer publiquement) · **Débloque :** G1 (angle de la vidéo)

## Question
Ce qui existe déjà (bancs vLLM, LLMPerf, GuideLLM, articles, vidéos) en tests de charge de LLM, et surtout d'agents multi-tours avec outils et mesure de qualité sous charge. Quel angle reste libre.

## Résolution
- Outils de charge LLM (GuideLLM, vLLM `benchmarks/multi_turn`, GenAI-Perf, LLMPerf, k6) : ils mesurent latence et débit ; multi-tours parfois, appels d'outils nulle part dans leurs README (non vérifié dans le code). Les définitions de métriques diffèrent d'un outil à l'autre (NVIDIA : https://docs.nvidia.com/nim/benchmarking/llm/latest/overview.html).
- Qualité sous charge : aucune source trouvée qui publie pass^k ou un taux de réussite de tâche à plusieurs niveaux de concurrence. Pistes voisines : comparatif Ollama et vLLM où la précision tombe par troncatures et délais (https://www.mdpi.com/2076-3417/16/11/5435) ; préprint où les gros lots cassent la sortie JSON (https://www.medrxiv.org/content/10.1101/2025.08.22.25334049.full.pdf) ; PeakBench et XPerf (arXiv 2608.24509, 2608.20370, à relire).
- Pas d'équivalent vidéo populaire trouvé ; seulement des guides écrits aux chiffres très variables (35 à 64 utilisateurs concurrents selon GPU et modèle).
- **Angle libre** : faire de la qualité la variable de la montée en charge. Pass^k, JSON d'appel d'outil invalide, troncatures et délais mesurés à chaque palier, puis après chaque optimisation, sur des conversations multi-tours avec outils. Les bancs donnent la latence ; personne ne dit combien de clients tiennent avant que l'agent cesse d'être fiable.
