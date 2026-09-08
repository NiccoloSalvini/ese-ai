# Homework 3 — A model, a baseline, and what would have to be true
**Due: Sunday 11 October 2026, 23:59 · folder `week-03/hw/` in your repo**

## Goal
Build one supervised model on a financial question of your choice, evaluate it honestly against a baseline, and — the real deliverable — write what would have to be true for it to be useful in a decision.

## Pick a target (one)
- Direction or volatility regime of an asset you did **not** use in class, at a horizon of your choice (state it).
- Whether an asset's next-week absolute move exceeds a threshold (a "big move" classifier).
- A regression target if you prefer: next-week realised volatility as a number (use MAE and compare with "predict last week's volatility").
- Your own, if it is a *prediction at time t of something that happens after t*. Message me first.

## Deliverables (in `week-03/hw/`)
1. `hw3.ipynb` — runs from a clean runtime. Must contain, in this order:
   - data acquisition (reuse your week-1/week-2 code; add at least one external feature, e.g. a macro series or an on-chain series);
   - features with a markdown table: **feature name → latest row of data it uses**;
   - the target, and the **hand check** for one date (recompute from raw data, assert equality);
   - the base rate / trivial baseline, stated;
   - at least two models evaluated with a **time-ordered** split (`TimeSeriesSplit` or a manual walk-forward), reporting accuracy *and* AUC (or MAE vs baseline for regression);
   - one deliberately leaky variant (a centred window, a shuffled split, or a feature using future data) with the score shown next to the honest one, labelled as the leak it is;
   - a threshold/decision table with explicit error costs of your choosing, and a calibration table.
2. `memo.md` (400–600 words) with these headings:
   - **Question and target**
   - **Honest result vs baseline** (one table, one sentence)
   - **What would have to be true for this to be useful** — the decision it would inform, the cost of each error, the threshold you would choose, the KPI you would report in production, and the single strongest reason it might not work out of sample.
   - **AI-use disclosure**

## Constraints
- No shuffled split in the honest evaluation. If the assistant writes `train_test_split` or `cross_val_score` without a time-aware splitter, that is your "what the assistant got wrong" for this week — say so in the memo.
- Every feature must be explainable as "computable at time t". I will pick two and ask.
- No hyperparameter tuning. Two sensible default models are enough.

## Scope
5–6 hours. If the model does not beat the baseline, that is a valid and common result — write it up as such. A memo that says "this is not predictable with these features, here is the evidence" is a good memo.

## Self-check
- [ ] Restart and run all: no errors.
- [ ] Feature table with latest-row-used is present.
- [ ] Target hand-check asserts and passes.
- [ ] Base rate stated next to every accuracy figure.
- [ ] Honest split is time-ordered; leaky variant labelled.
- [ ] Threshold table uses stated costs; a KPI is chosen and defended.
- [ ] Snapshot saved; AI-use disclosure present.

## How this feeds the capstone
This notebook is the evaluation layer of your pipeline: time-ordered validation, baseline comparison, cost-weighted decision, calibration. Week 7 reuses it for backtesting; week 9 reuses it for the risk and controls canvas. If you choose your capstone asset now, use it here.
