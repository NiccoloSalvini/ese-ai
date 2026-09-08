# Homework 6 — Capstone proposal and data check
**Due: Sunday 8 November 2026, 23:59 · folder `week-06/hw/` in your repo**

## Goal
Commit to a capstone question, write it as a one-page proposal in the template from the session, and prove the data exists by loading it: shape, date range, missing values, a dated snapshot. The proposal is the argument; the data check is what makes it a proposal instead of a wish.

## Pick a candidate (one)
- The candidate that scored highest in the feasibility cell — if the data check passes.
- The runner-up, with a note on why the first failed (a failed data check is a legitimate and useful reason).
- A candidate not in the session's three, if it is a *decision question answerable with free public data* using a method taught by week 9. Message me first with the question in one sentence.

## Deliverables (in `week-06/hw/`)
1. `proposal.md` — one page (400–600 words), these headings, in this order:
   - **Question** — one sentence; a named asset, protocol, or filing set; a period; the decision someone would take on the answer.
   - **Data** — every source by name and endpoint (yfinance ticker, FRED series id, DefiLlama route, EDGAR form type, blockchain.com chart); frequency; expected rows; the snapshot file name and date.
   - **Method** — in the toolkit's words (time-ordered validation, threshold on costs, walk-forward backtest with costs, RAG/extraction with evals, AMM/lending simulation, SHAP); the baseline you must beat.
   - **Deliverable** — notebook pipeline, ~2,000-word decision memo, risk and controls canvas, roadmap, 15' presentation — and what is specific to your question in each.
   - **Risk** — the most likely way it fails, and what you deliver if it does (a well-evidenced negative is a deliverable).
   - **Weekly plan** — a table, weeks 7–10, one row per weekend: the file that exists on Sunday night. No row may say "explore".
   - **AI-use disclosure** — which parts the assistant drafted, which parts you rewrote.
2. `data_check.ipynb` — runs from a clean runtime and, for **every** data source in the proposal:
   - loads it with the three-tier pattern (live → snapshot in `data/` → synthetic, clearly labelled);
   - prints `shape`, first and last date, number of missing values, the last value;
   - saves a dated snapshot `data/<source>_<YYYY-MM-DD>.csv` and commits it if under 5 MB;
   - passes only if the loader printed `[live]` or `[snapshot]` — a `[SYNTHETIC]` line means the check failed; say so in the proposal and switch candidate or source.

## Constraints
- The question must be answerable with data you have already loaded. "I will find the data in week 7" fails the check.
- Every method named in the proposal must be one taught by week 9 or shown in the toolkit list. No new libraries as the plan.
- If the assistant proposes a question you would not defend in front of your last employer, rewrite it. I will ask you to defend it on Monday.
- Nothing confidential from previous employers as data or as the case.

## Scope
4–5 hours. Two hours on the data check (the loaders will fight you — that is the point), two on the proposal, the rest on the weekly plan. If the check kills your first candidate on Saturday, that is a normal Saturday.

## Self-check
- [ ] `proposal.md` fits one page and has all seven headings in order.
- [ ] The question names an asset/protocol/filing set, a period, and a decision.
- [ ] Every data source has an endpoint and a snapshot date.
- [ ] `data_check.ipynb` restarts and runs all without errors; no `[SYNTHETIC]` line.
- [ ] Shape, date range, missing values, and last value printed for every source.
- [ ] Weekly plan: four rows, four files, no "explore".
- [ ] Risk section states what you deliver if the answer is negative.
- [ ] AI-use disclosure present.

## How this feeds the capstone
This is the capstone's first page and its data layer. Week 7 builds the backtest or evaluation on the snapshot you commit now; week 8 adds the on-chain or market context; week 9 fills the risk and controls canvas from the risk section you write today; week 10 turns the proposal into the memo's first section. A proposal that changes after week 7 costs a weekend; one that changes after week 8 costs the mark.
