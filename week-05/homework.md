# Homework 5 — Minor case brief (40% of the final mark)
**Due: Sunday 1 November 2026, 23:59 · folder `week-05/hw/` in your repo · Moodle submission of the same files · 8-minute presentation in session 6 (Monday 2 November)**

## Goal
Treat the LLM system you built in weeks 4 and 5 — retrieval over financial documents, an agent with tools, and its evaluation — as a product, and write the brief that would let a team decide whether to build it. The system is the evidence; the brief is the deliverable. It is assessed on the repo and the presentation, not on a PDF.

## Pick a framing (one)
- **Internal tool**: the research-analyst agent for a desk or a team you know (a BI team, a startup-scouting team, a product team following a market). Users are colleagues; value is time and error avoided.
- **Customer-facing feature**: the same system inside a product for retail investors or a crypto wallet. Users are the public; the guardrails and regulation rows carry more weight.
- **Your own**, if it is *this* system (or a clear extension of it) and the users are real. Message me first.

## Deliverables (in `week-05/hw/`)
1. `brief.md` — 1,500–2,000 words, these sections in this order:
   - **Problem and user** — who asks, how often, in what context; what they do today without the system; what "done" looks like for one concrete question.
   - **The system** — what it does, in one diagram (ASCII or mermaid) and one paragraph; which tools, which corpus, which model; what it explicitly does not do (no advice, no assets outside the universe, no live news).
   - **Evaluation** — the golden set (how many questions, how the expected answers were computed and why *independently* of the system), the checkers, the judge and how you spot-checked it, and the regression table for at least two versions of the system, per question, with the failures explained.
   - **Guardrails and failure modes** — tool-error contract, step/cost budgets, injection surfaces you identified and what you did about each, what happens when the data loader falls back to a snapshot.
   - **Unit economics** — measured tokens per query, cost per query, cost per day at your assumed volume, and your value-per-query assumption with where it comes from and how you would test it.
   - **Limits, risks, regulation** — what the eval does not cover; the worst silent wrong answer you found; the EU AI Act classification of your framing (week 4 reading) and the one obligation that binds you; MiCA if the users are retail crypto investors; what a human must still do.
   - **AI-use disclosure** — what the assistant wrote, what you rewrote, what it got wrong.
2. `system.ipynb` — runs from a clean runtime. Contains the loader, the RAG from week 4, the agent loop with `safe_call`, guards and cost counter, the golden set, the checkers with their own tests, the judge, and the regression run. Every LLM cell guarded by the key check with the `[MOCK]` fallback.
3. `eval/golden.json` — the golden set (at least 12 questions: at least 8 numeric, at least 2 textual, at least 2 that the current system *cannot* answer correctly, labelled as such).
4. `eval/results.csv` — the regression table exported from the notebook: one row per question per version, columns `id, version, pass, judge, tool_calls, stop, usd`.
5. `slides.md` (Marp, at most 8 pages) or the brief itself — whatever you present from. Eight minutes, then ten of questions.

## Constraints
- The expected answers in the golden set must be computed with pandas from the price table or read from the document by you — never taken from the agent's own output. I will pick one and ask how you got it.
- At least one planted failure must be preserved and reported honestly: a question that fails, why, and what a real fix would be (tool, prompt, or golden set — say which and why).
- Numbers in the brief must trace to a cell in `system.ipynb`. A number with no cell is an opinion; label it as one.
- Word count is for the brief body, excluding the diagram, tables and the disclosure.

## Scope
This is the reading-week assignment: budget 10–12 hours over two weeks, not 4–6. Roughly: 3 h making `system.ipynb` clean and re-runnable, 3 h extending the golden set and running the regression twice, 4 h writing, 1–2 h on the presentation. If the system is honestly weak on a rubric row, write that; a brief reporting 7/12 with a clear analysis scores higher than one claiming 12/12 with no evidence.

## Rubric (each row 0–25; 100 total; 40% of the final mark)
| Row | What is assessed |
|---|---|
| Problem framing and user | A real user and a real question; the job to be done before and after; what "done" means |
| Technical build and correctness | The notebook runs; the loop, tools, guards and loaders work; the numbers are right |
| Evaluation method (evals, baseline, metrics) | Independent golden set; verified checkers; judge used as a second signal; per-question regression, not aggregates |
| Reflection on limits, risk, regulation | Silent failures named; injection surfaces; what the eval does not cover; AI Act / MiCA position; what stays human |

## Self-check
- [ ] `system.ipynb`: restart and run all, with and without the API key — no errors.
- [ ] Golden expected values computed independently; the cell that computes them is visible.
- [ ] Checker has its own asserts on hand-written right and wrong answers.
- [ ] Regression table has at least two versions, per question, and at least one failure explained.
- [ ] Cost per query is measured, not assumed; the value-per-query assumption is labelled as an assumption.
- [ ] Two injection surfaces named, one guardrail each.
- [ ] AI Act classification stated with one obligation; MiCA mentioned if retail crypto.
- [ ] Brief is 1,500–2,000 words; every number has a cell.
- [ ] Files in `week-05/hw/`, committed; the same files uploaded to Moodle.

## How this feeds the capstone
The brief is the first draft of the capstone's decision memo, and `system.ipynb` with `eval/` is the LLM half of the capstone pipeline. Week 6 uses your presentation to scope the capstone; week 9 applies the risk and controls canvas to exactly this system and red-teams the injection surfaces you list here; week 10's build/buy/partner and cost-at-scale discussion starts from your unit-economics section. Write the brief so that its "Limits" section becomes the capstone roadmap.
