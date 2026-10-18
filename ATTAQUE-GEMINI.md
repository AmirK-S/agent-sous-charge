# Consigne d'attaque pour Gemini 4

Mode d'emploi : ouvrir une conversation neuve avec Gemini 4, joindre le fichier `PRE-ENREGISTREMENT.md`, coller le texte ci-dessous comme prompt. Rapporter sa réponse telle quelle dans `tickets/` (fichier `ADV1-gemini.md`).

---

You are a hostile reviewer: a senior performance engineer who has run MLPerf submissions and a statistician who reviews LLM evaluation papers. Attached is the draft pre-registration (in French) of a public experiment: how many concurrent conversations a banking support agent with tools (τ³-bench banking_knowledge, 97 tasks) can serve on a single self-hosted GPU (vLLM) before it stops being reliable, with quality measured under load.

Your job is to break it before it runs. Do not praise it. For each problem, give:
1. the flaw, in one sentence;
2. a concrete scenario where it makes a published number wrong, gameable, or unconvincing to a bank CTO;
3. the fix, specific enough to write into the protocol;
4. severity: fatal, serious, or minor.

Attack at least these angles, and any others you find:
- Validity of the load model (Poisson arrivals of multi-turn conversations, think time, patience, coordinated omission, warm-up and steady state, window length versus conversation length).
- Statistics: unit of analysis, clustering, the non-inferiority test, power with 97 tasks, multiple comparisons, number of looks at the test set.
- The simulated customer: an open model instead of gpt-4.1, its own errors, collusion or leniency, its load on the second GPU, bias it introduces under load.
- The harness: replay strictness of τ³ through an MCP layer, retries and exclusions, TIMEOUT versus infrastructure errors, non-determinism under vLLM batching.
- Overfitting: prompt changes, dev/validation/test split, the retail control.
- The headline claim in section 11: what a skeptical CTO would say it does not prove, and whether the comparison to a frontier model is fair.
- Anything that would make the results irreproducible on another rented GPU.

End with the three changes that would most increase the credibility of the results, ranked.

Answer in French, as a numbered list, no more than 1,200 words.

---
