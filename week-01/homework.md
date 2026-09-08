# Homework 1 — Three assets, one honest table
**Due: Sunday 27 September 2026, 23:59 · folder `week-01/hw/` in your repo**

## Goal
Reproduce, on your own, the loop we practised in class: get data with the assistant's help, compute a few numbers, chart one thing that answers a question, and document one mistake the assistant made and how you caught it.

## Deliverables (in `week-01/hw/`)
1. `hw1.ipynb` — a Colab notebook that, from a clean runtime, runs top to bottom without errors and produces:
   - daily close prices since 1 January 2022 for **three assets of your choice: one equity, one cryptocurrency, one index or ETF** (not the three used in class);
   - a table with, per asset: annualised volatility (with the correct day-count for each), cumulative return over the period, maximum drawdown, and the date of the worst single day;
   - **one chart that answers a question you state in a markdown cell above it** (e.g. "Did asset X recover its 2022 drawdown?"). One chart, one question.
2. `README.md` (150–250 words) with: the question, the answer in two sentences, and a section titled **"What the assistant got wrong"** describing one concrete error (a wrong constant, a wrong formula, a misread column, a hallucinated function) and the check that exposed it. If the assistant got nothing wrong, say which checks you ran to establish that.
3. `data/` — the CSV snapshot your notebook saved (so the numbers are reproducible even if Yahoo changes).

## Constraints
- Use the assistant as much as you like, but every line in the notebook must be one you can explain. I will ask.
- Verify at least one number a second way (e.g. cumulative return from first and last price vs from the returns series) and show the check in the notebook.
- Commit at least twice (the history is part of the work).

## Scope
4–6 hours. If you are past 6 hours, stop, commit what you have, and write in the README where you got stuck.

## Self-check before submitting
- [ ] `Runtime ▸ Restart and run all` works without errors.
- [ ] Day-count convention is stated per asset and is right (365 for crypto).
- [ ] The chart has a title that is a question, and the README answers it.
- [ ] The "what the assistant got wrong" section describes a real, specific error and a real check.
- [ ] Data snapshot saved and committed.

## How this feeds the capstone
`load_prices` and the summary table are the first reusable pieces of your pipeline. Every later week adds to this repo; by week 6 your capstone will already have data acquisition, cleaning and a verified summary layer.
