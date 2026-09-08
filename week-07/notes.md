# Week 7 — AI in markets and trading: backtesting done honestly; LLM signals; model risk
**Monday 9 November 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Write a vectorised backtest as a five-step pipeline (signal → position → returns → equity → statistics), with per-trade costs, and explain why the `shift(1)` between signal and position is not optional.
2. Recognise the four ways a backtest lies — look-ahead, survivorship, multiple testing, regime averaging — and produce the evidence that a given backtest is or is not affected by each.
3. Test a text-derived (LLM-scored) feature with point-in-time rules and state whether it adds information *beyond the price*, net of costs.
4. Describe model risk in a bank's vocabulary (inventory, independent validation, monitoring, kill-switch) and map it onto a model that would decide a hedge.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **A. HW6 walkthrough + capstone sign-off** | he presents |
| 09:20–10:00 | **B. Lab first: a backtest in six steps** | notebook B |
| 10:00–10:40 | **C. The ways it goes wrong** | whiteboard + notebook C |
| 10:40–10:50 | break | |
| 10:50–11:30 | **D. An LLM signal, tested honestly** | notebook D |
| 11:30–11:50 | **E. Model risk** | reading + discussion + notebook E |
| 11:50–12:00 | **Homework brief** | |

### A. HW6 walkthrough and capstone sign-off (20')
His screen. Two lines of `hw6.ipynb` chosen at random — he explains them. Then the proposal: one question, one dataset, one number that would change a decision. Did `data_check.ipynb` print `[live]` or `[snapshot]`? If it printed `[SYNTHETIC]` the proposal is not signed off; agree the fix and a date. Write the sign-off (or the single revision) at the bottom of his proposal file before opening anything else. Everything from Block B onwards will be reused on his capstone asset, so decide now which asset he replicates on today.

### B. Lab first: a backtest in six steps (40')
No theory before the code. Worked example on the projector: `momentum_signal`, `backtest`, `stats` — three functions, thirty seconds each. The one line to stare at is `pos = signal.shift(1)`. Whiteboard [card 1]: the timeline of one day — close *t* → signal computed → position held → return of *t+1* earned.

Bet 1 (Sharpe before costs), bet 2 (Sharpe after 10 bps). He runs the cost sweep and the equity curves. Then the arithmetic on paper: turnover per year × cost per unit = annual drag; compare with annual return. Replication: mean reversion on SPY at 0 and 10 bps — his own cell, his own conclusion about which rule is more cost-sensitive and why the turnover column already says so.

Vocabulary that comes out of the table, not before it: Sharpe, max drawdown, turnover, time in market. He has seen returns, vol and annualisation in week 1; Sharpe is mean/std × √dpy, that is all.

### C. The ways it goes wrong (40')
Four mechanisms, one whiteboard drawing each, one notebook proof each [cards 2–5].

**C1 — planted bugs.** The assistant's backtest cell (six lines). Two bugs: `pos = sig` instead of `sig.shift(1)`, and cost charged on `pos.abs()` (every day held) instead of on `pos.diff().abs()` (units traded). Ten minutes alone; one hint at five. The 2×2 corrected cell separates the two effects. Make him write down the Sharpe gap from the look-ahead alone: that number is the size of the lie in a backtest that forgets one `shift`. Say it: two bugs that partly cancel are worse than one, because nobody looks.

**C2 — survivorship.** Twelve synthetic tokens, four of which die. The universe "as of today" vs the point-in-time universe. The gap is not about the tokens; it is about *when the list was written*. Real names: LUNA (May 2022), FTT (November 2022) — both top-20 assets that no "top coins today" list contains. Defence: a universe defined as of each date, or an explicit statement that you could not get one.

**C3 — multiple testing.** 200 SMA-crossover pairs on BTC, 10 bps, fitted 2018–2021, checked 2022 onwards. Bet 3 first. The scatter of in-sample vs out-of-sample Sharpe; then the noise simulation: 200 random position series, best in-sample Sharpe. Harvey–Liu–Zhu on the whiteboard [card 4]: the expected maximum of N noise Sharpes grows like √(2 ln N)/√years — with 200 tries over three years, a "Sharpe 1.9" is what nothing looks like. The rule he takes away: every parameter you tried counts, including the ones the assistant tried for you.

**C4 — regime.** The same rule year by year, and 2022 vs 2023–24 [card 5]. Is the full-sample Sharpe made by one or two years? A rule whose edge sits in a single regime is a bet on that regime returning; the memo must say so.

### D. An LLM signal, tested honestly (40')
"News sentiment" is the most pitched AI signal in finance. Build one, test it with the discipline of B and C.

Headlines are synthetic and seeded (real archives with reliable timestamps cost money) but carry the property that matters: the headline about day *t* is published on day *t+1*. Two date columns, `event_date` and `published`; the difference is where leakage hides [card 6].

Scoring goes through the `llm()` wrapper. With `GEMINI_API_KEY` in Colab Secrets, Gemini scores the last 40 headlines against a JSON schema and the notebook prints the correlation with the lexicon. Without a key, the lexicon (labelled MOCK) scores everything. Either way the feature used downstream is the lexicon score, so the result is reproducible.

D1: the week-3 walk-forward rebuilt compactly, gradient boosting, six time-ordered folds. Bet 4: does `sent` raise out-of-sample AUC by more than 0.02? It does not, and that is the expected result: the headline is a noisy function of yesterday's return, which the model already has as `ret_1`. A text signal must carry information *not in the price* that arrives *before* the price moves. D2: the same score as a trading rule with costs, next to the leaky join on `event_date` without shift — a Sharpe near 10 that would sell a fund. Close with the four-question table: point-in-time, no date leakage, beyond the price, after costs.

### E. Model risk (20')
Reading first (5', silent, `## Reading — Model risk` below), then the three prompts (10'), then the notebook kill-switch cell (5') [card 7]. Frame: everything in C and D is what a bank's model-risk function exists to catch, and it was written down (SR 11-7) after 2008 because the mechanisms are the same whether the model is a regression or an LLM. The scenario throughout is *a model that decides hedging* — the week-3 hedging desk. He fills the model-inventory table in the notebook.

### Homework brief (10')
`homework.md`. The deliverable is the pitfall checklist answered with evidence; the strategy is the excuse. Educational only, no live trading, say it once.

## Script

### A. HW6 walkthrough
**Opening:** "Show me `data_check.ipynb` first. What did the first line print?" Then: "Pick a random cell number between 5 and 20." He explains the cell.
**Closing:** "Read me your one question, one dataset, one number. I sign, or I write one revision, now."

### B. Backtest in six steps
**Opening:** "I will show you three functions in ninety seconds. Then you tell me which line, if you deleted it, would make every backtest in the world look better." [card 1]
**Bet 1 (write it down):** "Sharpe ratio of 20-day momentum on BTC since 2018, before costs. One number. Buy-and-hold is printed next to it for scale."
**Bet 2 (write it down):** "Same rule, 10 basis points per unit traded. Sharpe after costs."
**He should discover:** costs are proportional to turnover, not to time in market; the equity curves at 0/10/50 bps fan out because the rule flips ~60 times a year.
**Hint if stuck:** "Multiply `turnover_per_year` by 0.001. What is that number, in the units of `ann_return`?"
**Closing:** "A backtest without a cost line is a chart, not a result. Write the drag formula in your takeaway."

### C1. The assistant's backtest
**Opening:** "This cell was written by the assistant for the exact task you just did. It runs. Its Sharpe is 2.2; yours was 0.2. There are two mistakes. Ten minutes, no hint." [card 2]
**Bet (implicit, he writes it):** "Which direction does each bug push the Sharpe?"
**He should discover:** `pos = sig` uses today's close to decide today's position; `pos.abs()` charges the cost every day held.
**Hint at 5':** "Print `pos.head(25)` and `r.head(25)` side by side. On which day does the position first know something?"
**Closing:** "The two bugs pull in opposite directions. That is why nobody found them. The corrected 2×2 is the table you show anyone who claims a Sharpe."

### C2. Survivorship
**Opening:** "If you ask the assistant to backtest 'the top 10 coins since 2018', which list does it use — 2018's or today's?" [card 3]
**He should discover:** the survivors-only column beats the point-in-time column by construction; no token in the survivors list ever collapsed *because they were selected for not collapsing*.
**Hint:** "Where would LUNA be in each column?"
**Closing:** "The number you got is the property of the date the list was written. Either build the universe as of each date, or write that you could not."

### C3. Multiple testing
**Opening:** "The assistant offers to 'optimise the parameters'. Two hundred pairs. Before running:" [card 4]
**Bet 3 (write it down, three numbers):** "How many of the 200 have Sharpe > 1 in-sample? How many out-of-sample? Best in-sample pair — positive or negative out-of-sample?"
**He should discover:** in-sample and out-of-sample Sharpe are close to uncorrelated across rules; the best in-sample pair is unremarkable out-of-sample; 200 random rules produce a best Sharpe well above 1 with no information at all.
**Hint:** "Look at the correlation line. If skill were real, what sign and size would it have?"
**Closing:** "The expected best of N tries grows with √(2 ln N). Every parameter you tried counts, including the ones the assistant tried for you. Write N in the memo."

### C4. Regime
**Opening:** "One Sharpe for 2018–2026 is an average of how many markets?" [card 5]
**He should discover:** the full-sample number is made by two or three years; 2022 and 2023–24 give different answers for the same rule.
**Hint:** "Which year would you delete to make the strategy look bad? If one year is enough, what is the strategy a bet on?"
**Closing:** "Report by regime, or the average will be read as a promise."

### D. LLM signal
**Opening:** "A headline about Monday's crash is published on Tuesday morning. Which date goes on the feature?" [card 6]
**Bet 4 (write it down):** "Adding sentiment to the week-3 model: does out-of-sample AUC rise by more than 0.02? Yes or no."
**He should discover:** the honest gain is near zero because the headline restates `ret_1`; the leaky join on `event_date` gives an absurd Sharpe; with a key, Gemini and the lexicon agree strongly on a synthetic set (and disagree more on real news — say so).
**Hint:** "What does the model already know that the headline is telling it again?"
**Closing:** "A text signal earns its place only if it carries something the price does not, before the price moves, net of costs. Four questions, in writing, before you believe any sentiment number."

### E. Model risk
**Opening:** "Read the page. Then: if the momentum rule from Block B decided a hedge for a treasury desk, who would be allowed to switch it off, and on what evidence?" [card 7]
**He should discover:** the kill-switch thresholds must be set before go-live; the rolling Sharpe fires often on a rule with no edge; independent validation is exactly Blocks C and D done by someone who did not build the rule.
**Hint:** "Who in Kaspersky's BI team would have been the *second* pair of eyes on a KPI model, and what did they check?"
**Closing:** "Model risk is not a form. It is the discipline of Blocks C and D, owned by somebody else, on a schedule."

### Take-home
"Three lines. One about the shift, one about N, one about who switches it off. Commit."

## Key concepts, in one line each
- Backtest pipeline: signal at close *t* → position from *t+1* → returns → equity → statistics.
- Sharpe ratio: mean daily net return / its std × √(days per year); risk-free taken as zero here.
- Max drawdown: worst peak-to-trough fall of the equity curve.
- Turnover: units bought plus sold per year; the multiplier on every cost.
- Look-ahead (off-by-one): a position that uses the close of the day whose return it earns.
- Survivorship: a universe defined today applied to the past; removes everything that died.
- Multiple testing / data snooping: the best of N tries is large by chance; expected max ≈ √(2 ln N)/√years.
- Walk-forward: fit on a past window, test on the next, roll; the only honest use of a parameter search.
- Regime: a period with its own statistics; a full-sample average hides which regime made the number.
- Point-in-time: every feature dated by when it was *readable*, not by what it is about.
- Model risk: the loss from a model that is wrong, misused or drifting; managed by inventory, validation, monitoring, kill-switch.

## Tutor's notes
- **Live data matters.** On the synthetic fallback all Sharpes sit near zero, momentum and buy-and-hold look alike, and the 200-rule scatter is pure noise (fine for C3, useless for B and C4). Confirm yfinance loads from 2018 for BTC-USD and SPY before Monday; commit `data/prices_BTC-USD_SPY.csv` if the ESE network blocks Yahoo. With the snapshot the bets in B and C4 have real answers.
- **API key.** Only the Gemini scorer in D needs `GEMINI_API_KEY`; without it the lexicon MOCK runs and prints a label. If the key works, show the correlation line and ask him why agreement is high (synthetic headlines are built from the lexicon's vocabulary — the honest caveat). Free-tier quota: one call of 40 headlines, nothing else.
- **Bugs and bets.** Planted bugs: C1 only (two in one cell). Bets: 1 Sharpe before costs; 2 Sharpe after 10 bps; 3 count of Sharpe > 1 in-sample vs out-of-sample and the sign of the best pair OOS; 4 sentiment AUC gain > 0.02. Four written bets plus C1's directional guess — under the limit.
- **If behind:** cut C4 (keep the by-year cell as homework), shorten D2 to the leaky-vs-honest table only. Never cut C1 or the reading.
- **Energy:** B is fast and rewarding; C1 is the low point (ten silent minutes) — keep it, then the survivorship cell is quick relief. Break before D as planned; D1 fits gradient boosting six times and takes ~30 s.
- **Replication asset:** SPY for mean reversion in B; his capstone asset if it is a daily price series and loads live.
- **Educational-only line:** say it at the start of B and again at the homework brief, once each; do not moralise.

## Reading — Model risk

**One page. Read before the prompts.**

A model is a method that turns inputs into a number someone acts on. A model is *wrong* when its output would have been different had it been built correctly; it is *misused* when it is applied outside the conditions it was built for; it *drifts* when the world changes and its inputs stop meaning what they meant. Model risk is the loss — money, decisions, reputation — that follows from any of the three. Banks were forced to write this down after 2008, when models that priced mortgage risk were correct on their inputs and catastrophically wrong on the world. The US supervisory letter SR 11-7 (2011) and the ECB's guide to internal models are the reference texts; the ideas fit a spreadsheet, a gradient-boosting classifier, or an LLM that scores headlines, because the mechanisms of error are the same.

Four practices carry the whole discipline.

**Inventory.** Every model that informs a decision is listed: name, owner, the decision it takes or informs, its inputs and the date on which each input becomes available, the version in use, and the date of the last review. A model that is not in the inventory cannot be validated or switched off, because nobody knows it exists. In a firm without a model-risk function the inventory is a table in a repository; the discipline is that it is kept.

**Independent validation.** Someone who did not build the model tries to break it *before* it goes live and again on a schedule. For a trading or hedging model this is exactly this week's Block C and D: rerun with the shift, rebuild the universe point-in-time, count the parameters tried, split by regime, test the text feature against the price alone. The validator writes what was tested, what failed and what limits apply. Building and validating are different jobs because the builder cannot see their own assumptions.

**Monitoring.** Once live, the model's inputs and outputs are watched against thresholds set *before* go-live: performance (rolling Sharpe, hit rate, calibration), input drift (is the news feed still the same feed; has the exchange changed its fee), and use (is the model being applied to an asset it was never validated on). Thresholds chosen after the fact are chosen to avoid the alarm.

**Kill-switch.** A named person can switch the model off, within a stated time, without asking the builder. The fall-back — what is done while the model is off — is written down. For a hedging model the fall-back is usually "hedge fully" or "hedge as last week"; either is acceptable, silence is not.

None of this requires a bank. It requires that the four artefacts exist and that someone other than the builder owns two of them.

### Three prompts (for "a model that decides hedging")
1. **Inventory.** Write the inventory entry for the momentum rule of Block B as a hedging model for the week-3 treasury desk: inputs and their availability dates, the decision, the owner. Which field could you not fill in, and what does that tell you?
2. **Independent validation.** You are the validator, not the builder. List the five tests you would run, in order, and for each the number that would make you refuse sign-off. Which of the five could an LLM assistant run for you, and which must a person read?
3. **Monitoring and kill-switch.** The notebook fires the switch on rolling Sharpe < 0 or drawdown < −30%. Argue for or against each threshold, name who at the desk can pull it, and write the fall-back position in one sentence. What would you monitor on the *news feed* if the model used Block D's sentiment feature?
