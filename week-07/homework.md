# Homework 7 — One strategy, every pitfall answered with evidence
**Due: Sunday 15 November 2026, 23:59 · folder `week-07/hw/` in your repo**

## Goal
Backtest one trading rule honestly on at least two assets, with costs and a walk-forward, and — the real deliverable — answer the pitfall checklist with evidence from your own notebook. Then add one text-derived feature and show whether it earns its place. Everything is an educational simulation: no live trading, no advice.

## Pick a rule (one)
- A momentum or mean-reversion rule with one or two parameters (as in Block B), on your capstone asset plus one other.
- A volatility-targeting rule: position size = target vol / realised vol, long only. Message me first if you choose this; the cost model changes.
- The week-3 classifier turned into a rule: long when P(up) > threshold, flat otherwise, using your HW3 model.
- Your own, if it is *a position decided at close t and held from t+1*. Message me first.

## Deliverables (in `week-07/hw/`)
1. `hw7.ipynb` — runs from a clean runtime. Must contain, in this order:
   - data acquisition with the three-tier loader; **at least two assets**, from 2018 or the earliest available; snapshot saved;
   - the rule as a function, and the backtest pipeline with the `shift(1)` **commented** in the cell where it happens;
   - a statistics table (annual return, vol, Sharpe, max drawdown, turnover per year) at **0, 10 and 25 bps** per unit traded, per asset;
   - a **walk-forward** parameter choice: fit on an expanding or rolling window, apply to the next block, report the out-of-sample Sharpe next to the best in-sample Sharpe and the number of parameter values tried;
   - a **by-period table** (by year, and at least one split you name as a regime);
   - one **text-derived feature** — Block D's headline scorer on your own headline set, or any dated text you can obtain (press releases, protocol announcements, exchange status posts, your own notes) — with its `published` column, added to the rule or to the classifier, shown **against the baseline without it**, net of the same costs;
   - the **pitfall checklist** as a markdown table (below), each row answered with the cell number that is the evidence.
2. `memo.md` (400–600 words) with these headings:
   - **The rule and the assets**
   - **Honest result** (one table: per asset, Sharpe at 10 bps, walk-forward OOS Sharpe, worst year)
   - **Pitfall checklist** — one line per row: look-ahead, survivorship, multiple testing, costs, regime, data snooping; each answered "not affected because…" or "affected, and here is the size of it…"
   - **The text feature** — what it adds beyond the price, or that it adds nothing, with the number
   - **What would have to be true** for anyone to act on this, and the monitoring metric and kill-switch threshold you would set before go-live
   - **AI-use disclosure** — including every parameter value the assistant tried on your behalf

### Pitfall checklist (copy into the notebook)

| pitfall | question | evidence (cell) |
|---|---|---|
| look-ahead | is every position decided with data ≤ the previous close? | |
| survivorship | is the asset list the list you would have had on the start date? | |
| multiple testing | how many parameter values were tried in total, by you and by the assistant? | |
| costs | is the cost charged per unit traded, and is the level stated? | |
| regime | does the result hold in more than one period? | |
| data snooping | did you look at the out-of-sample period before choosing anything? | |

## Constraints
- No parameter chosen on the full sample. If the assistant proposes a grid search without a walk-forward, that is your "what the assistant got wrong" this week — say so in the memo.
- Costs per unit traded, never per day held. A rule with turnover above 100 per year must be shown at 25 bps too.
- The text feature must be dated by *availability*, and the memo must state where the dates come from. If you cannot obtain availability dates, say so and use Block D's synthetic set, labelled.
- Two assets minimum. A rule that works on one and not the other is a valid and common result — report it as such.

## Scope
4–6 hours. The strategy is the excuse; the checklist with evidence and the memo are what I read first. A memo that says "this rule has no edge after costs and here are the six pieces of evidence" is a good memo.

## Self-check
- [ ] Restart and run all: no errors; first data line prints `[live]` or `[snapshot]`.
- [ ] `shift(1)` is present and commented.
- [ ] Statistics at 0/10/25 bps, per asset.
- [ ] Walk-forward OOS Sharpe next to best in-sample, with N tried.
- [ ] By-year table present.
- [ ] Text feature vs baseline, same costs, availability dates stated.
- [ ] Checklist table filled with cell numbers; memo has all six headings.
- [ ] Monitoring metric and kill-switch threshold stated; AI-use disclosure lists parameters tried.

## How this feeds the capstone
This is the strategy or decision-rule layer of your pipeline, and the checklist is the first half of the risk and controls canvas (week 9 adds the responsible-AI half). Week 8 supplies on-chain features you can add to the same backtest. If your capstone asset is a price series, this notebook becomes a section of the portfolio notebook as it stands.
