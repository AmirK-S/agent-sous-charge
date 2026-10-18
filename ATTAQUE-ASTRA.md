# Consigne d'attaque pour GPT-6 Astra (deuxième tour)

Mode d'emploi : ouvrir une conversation neuve avec GPT-6 Astra, joindre les deux fichiers `PRE-ENREGISTREMENT.md` et `tickets/ADV1-gemini.md`, coller le texte ci-dessous comme prompt. Rapporter sa réponse dans la conversation avec Claude, qui la consignera dans `tickets/ADV2-astra.md`.

---

You are the second hostile reviewer of a pre-registration, after a first reviewer (Gemini). You combine a senior performance engineer who has run MLPerf submissions and a statistician who reviews LLM evaluation papers.

Attached: (1) the pre-registration v1.1 (in French) of a public experiment: how many concurrent conversations a banking support agent with tools (τ³-bench banking_knowledge, 97 tasks, simulated customers) can serve on a single self-hosted GPU (vLLM) while keeping its quality; the headline number is the maximum load that holds quality, quality is the guard rail; (2) a summary of the first review (11 objections). Section 12 of the pre-registration says how each objection was handled.

Do not repeat the first review. Do not praise. Focus on:
1. The three points where the authors deliberately did not follow the first reviewer. Is each decision sound? What breaks?
   a. Prefix caching stays enabled for the shared system prompt and tool schemas, with a unique per-conversation marker right after that shared prefix.
   b. Development on 40 banking tasks; absolute quality on the 57 others; but quality-under-load is a paired difference (same frozen agent, same tasks, at rest vs under load) measured on all 97 tasks, with a sensitivity check on 40 vs 57.
   c. No alpha-spending function: exploratory search for the capacity (doubling then bisection on latency and error criteria, dev tasks), then a single pre-registered confirmatory test, with one fallback step at 15 % lower load and alpha split 2.5 % / 2.5 %.
2. Whether the fixes made after the first review introduce new flaws (open-loop Poisson arrivals with held arrivals during drain, think time counted after the simulator's generation, per-turn deadline propagation with cancellation in vLLM, 50-session MCP equivalence test, kappa ≥ 0.85 calibration of the open simulator against gpt-4.1, two cost figures).
3. Anything both the authors and the first reviewer missed, especially: whether the capacity number and the quality test can truly be combined in one criterion; what a bank CTO would still not believe; what would make a replication on another rented GPU disagree.

For each problem give: the flaw in one sentence; a concrete scenario where it makes a published number wrong, gameable, or unconvincing; the fix, specific enough to write into the protocol; severity (fatal, serious, minor).

End with the three changes that would most increase the credibility of the results, ranked, and say explicitly which of the three deliberate deviations (a, b, c) you would overturn, if any.

Answer in French, as a numbered list, no more than 1,200 words.

---
