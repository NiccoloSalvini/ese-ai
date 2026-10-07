# Homework 3 — Look first, then predict, on your own asset
**Due: Tuesday 13 October 2026, 23:59 · folder `week-03/` in your shared Drive folder `ese-ai-fintech`**

## Goal
Repeat today's morning on an asset you choose: explore it until you know which question is worth a model, then train one black box, judge it honestly against a base rate and a one-line rule, and — the real deliverable — write what would have to be true for it to be useful in a decision.

## Pick an asset (one)
Anything with a daily price on Yahoo Finance that we did **not** use in class: SOL-USD, an exchange or mining stock (COIN, MSTR, MARA), a stock you follow, gold (GLD), an index outside the US. If you already have a capstone idea, use its asset.

## Deliverables (in `week-03/`)
1. `hw3.ipynb` — runs from a clean runtime (`Runtime ▸ Restart and run all`). Two parts, in this order.

   **Part 1 — Explore** (reuse today's cells; change the data):
   - what is in the table: rows, dates, missing days and why;
   - the five worst and five best days, with one line on what happened for two of them;
   - fat tails: days beyond 4 standard deviations, against what a normal distribution gives;
   - direction vs size: the autocorrelation table, and one sentence on what it tells you;
   - **one chart of your own** whose title is the answer to a question (not "Rolling volatility" but "SOL's calm months end abruptly");
   - three lines: what you now expect a model can and cannot predict.

   **Part 2 — Predict:**
   - features with a markdown table: **feature → latest day of data it uses**; add at least one feature we did not use in class;
   - the target, and the **hand check** for one date (recompute from raw data, `assert`);
   - the base rate and a one-line rule, stated;
   - a random forest evaluated with a **time-ordered** split, AUC and accuracy next to the base rate and the rule;
   - the same forest with a **shuffled** split, labelled as the leak it is;
   - permutation importance, and one sentence: does it agree with Part 1?
   - a threshold table with error costs of your choosing, checked against "never act" and "always act".
2. `memo.md` (400–600 words), with these headings:
   - **Question and asset** — and why the exploration pointed you to this target;
   - **Honest result** — one table (base rate, rule, forest honest, forest shuffled), one sentence;
   - **What would have to be true for this to be useful** — the decision it informs, what each error costs, the threshold you would choose, the KPI you would put on the dashboard, and the single strongest reason it might not work next year;
   - **AI-use disclosure** — what the assistant wrote, and what it got wrong.

3. **Optional, recommended:** run Part 3 · L3 on your asset with your own free key (Google AI Studio → *Get API key* → Colab 🔑 Secrets as `GEMINI_API_KEY`). Add the LLM's AUC to the memo's table, with the number of dates and the cost. Never paste the key into a cell.

## Constraints
- No shuffled split in the honest evaluation. If the assistant writes `train_test_split` without being told, that is your "what the assistant got wrong" for this week.
- Every feature must be explainable as "computable at day *t*". I will pick two and ask.
- No tuning of the forest. Today's settings are enough; the point is the judgement, not the score.
- Stocks trade 5 days a week, crypto 7: state your calendar decision in Part 1.

## Scope
5–6 hours. If the forest does not beat the rule — or the base rate — that is a valid and common result. A memo that says "the rule is enough, here is the evidence" is a good memo.

## Self-check
- [ ] Restart and run all: no errors.
- [ ] Part 1 ends with three lines, and Part 2 refers back to them.
- [ ] Feature table with latest day used is present.
- [ ] Target hand check asserts and passes.
- [ ] Base rate and rule next to every score.
- [ ] The shuffled result is labelled as a leak.
- [ ] Threshold table beats (or honestly fails to beat) both trivial policies; a KPI is chosen and defended.
- [ ] AI-use disclosure present.

## How this feeds the capstone
Part 1 is how you will choose the capstone question; Part 2 is its evaluation layer — base rate, rule, honest split, cost-weighted decision. Week 7 reuses it for backtesting; week 9 opens the black box with SHAP and builds the risk and controls canvas on top.
