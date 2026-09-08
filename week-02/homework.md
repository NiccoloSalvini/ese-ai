# Homework 2 — One question, one dataset, one memo
**Due: Sunday 4 October 2026, 23:59 · folder `week-02/hw/` in your repo**

## Goal
Answer one empirical question about a financial asset by joining market data with at least one external series, and write it up the way you would for a manager who has ten minutes.

## Pick one question (or propose your own; message me first)
- Does Bitcoin's correlation with US equities depend on the level or the change of US interest rates?
- Do on-chain active addresses lead or lag Bitcoin's price, and at what horizon?
- How did a specific asset behave around a specific event (ETF approval, halving, an earnings date, a rate decision), compared with its normal behaviour?
- Is the "weekend effect" in crypto real — are Saturday/Sunday returns and volatility different from weekdays?

## Deliverables (in `week-02/hw/`)
1. `hw2.ipynb` — runs top to bottom from a clean runtime. Must contain:
   - the data acquisition (at least one market series + at least one external series: FRED, blockchain.com, DefiLlama, CoinGecko, or another public source);
   - an explicit calendar decision and an explicit units statement, in markdown, before any computation across series;
   - the `len()` / `isna().sum()` check after every join;
   - the analysis, and **one chart whose title is the question**;
   - a date-stamped CSV snapshot saved to `data/`.
2. `memo.md` — one page (300–450 words): question; data and its limits; answer in two sentences with the chart; what would change your mind; **AI-use disclosure** (which assistant, for what, what you verified and how).
3. `data/` — the snapshot(s).

## Constraints
- At least one join. At least one rolling or resampled statistic.
- The chart must be readable without the notebook: title, axis labels, units.
- Do not conclude causation from a correlation. If you are tempted, write the sentence and then write the alternative explanation next to it.

## Scope
4–6 hours.

## Self-check
- [ ] Restart and run all: no errors.
- [ ] Calendar and units stated in markdown before the analysis.
- [ ] Join check printed (rows before/after, NaN count).
- [ ] Chart title is a question; memo answers it.
- [ ] Snapshot saved and committed; AI-use disclosure present.

## How this feeds the capstone
The join pattern (your calendar, left join, forward-fill context, convert units, check) is the backbone of any data pipeline you will build later, including the one in your portfolio. The memo format is the format of the decision memo in the final portfolio.
