# Week 3 — Machine learning through one problem; from prediction to decision
**Monday 5 October 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Build features and a forward-looking target from a price series and verify by hand that the target contains no current or past information.
2. Compare a model against the base rate using a time-ordered split, and explain why a shuffled split overstates performance on time series.
3. Recognise leakage introduced through a feature (not through the split) and name the only defence against it.
4. Turn a predicted probability into a decision with a threshold chosen on error costs, and propose a KPI that prices errors.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW2 walkthrough** | he presents |
| 09:20–10:05 | **A. Features, targets, baselines** | talk + notebook A |
| 10:05–10:15 | break | |
| 10:15–11:00 | **B. Two models, two splits** | hands-on, notebook B |
| 11:00–11:20 | **C. Leakage on purpose** | hands-on, notebook C |
| 11:20–11:50 | **D. From prediction to decision** | hands-on, notebook D |
| 11:50–12:00 | **Homework brief** | |

### HW2 walkthrough (20')
Read the memo first, then the notebook. Two questions: was the calendar decision stated *before* the analysis, and does the chart title answer the memo? Then challenge the conclusion with the alternative explanation he should have written.

### A. Features, targets, baselines (45')
Vocabulary by construction, not by definition. Feature = known at time t. Target = happens after t. The wall between them is the whole discipline. PM analogy: a sprint forecast may use everything up to today's standup, not the retro of the sprint being forecast.

Two targets on the same features, chosen because they behave oppositely: 5-day direction and 5-day volatility regime. Build the target with reverse-rolling and shift; then the 🔍 CHECK: recompute `fwd_ret` for one date by hand from the raw returns and assert equality. Say it plainly: **do this every time you build a forward target; it is the most common bug in trading ML and it takes one minute.**

Base rates. "Always up" scores ~55% on BTC because of drift. A model at 56% has learned nothing. Any report of accuracy without the base rate next to it is not a report.

### B. Two models, two splits (45')
Logistic regression (a linear score through a squashing function — he knows regression from his degree) and gradient boosting (many small decision trees, each correcting the last; treat as a black box today, open it in week 9 with SHAP).

🔍 CHECK — **the assistant's shuffled cross-validation.** It is the sklearn default and what every assistant writes. Explain the leak: rolling windows overlap, so a Thursday in the test set has Wednesday and Friday in the training set with nearly identical features and correlated targets. Run the comparison table.

Three things to read out of the table, in this order:
1. shuffled > time-ordered: the gap is leakage, not skill;
2. direction ≈ base rate under an honest split: with these features 5-day BTC direction is essentially unpredictable, as theory predicts and assistants rarely admit;
3. volatility regime is predictable on real data (AUC well above 0.5): volatility clusters. *Same data, same models — the question decides whether ML has anything to offer, and choosing the question is the manager's job.* This is the sentence of the session.

Caveat for the tutor: on the synthetic fallback data there is no clustering and the vol AUC will sit at 0.5; the point only appears on live data. Make sure live data loads.

### C. Leakage on purpose (20')
Add a centred rolling volatility — exactly what an assistant writes when asked to "smooth" a series. The time-ordered score jumps. 🔍 CHECK: the split did not protect him; leakage through features is invisible to any validation scheme. The only defence: for every feature, write the latest row it uses. Have him do it for the eight honest features on paper.

### D. From prediction to decision (30')
A probability is not a decision. Scenario: a treasury desk hedges BTC exposure when a high-volatility week is coming; hedging costs 1, missing a high-vol week costs 4. Walk-forward out-of-sample probabilities, then the threshold table. 🔍 CHECK: which threshold minimises cost; what changes if the miss cost is 2; compare with "never hedge" and "always hedge". Then the KPI question: accuracy is wrong because it does not price errors; candidates are cost per week vs always-hedge, recall at the chosen threshold, calibration. Show the calibration table: when the model says 70%, does it happen 70% of the time? He picks one KPI and defends it — this is a PM skill and he will be good at it; make him connect it to the model mechanics.

### Homework brief (10')
`homework.md`. Emphasise: the "what would have to be true" section is the deliverable; the model is the excuse.

## Script

### HW2 walkthrough
**Opening:** "Memo first. Was the calendar decision stated before the analysis? Does the chart title answer the memo?" Then: "Give me the alternative explanation you should have written next to your conclusion."

### A. Features, targets, baselines
**Opening (whiteboard):** a vertical line. "Left: everything known at time t. Right: everything that happens after. The whole discipline is keeping this wall intact. A sprint forecast may use today's standup — not the retro of the sprint being forecast."
**Bet 1 (a number):** before the base-rate cell: "'Always up' on BTC since 2018 — what accuracy?"
**He should discover:** ~55% from drift alone; a model at 56% has learned nothing.
**🔍 CHECK (hand check of the target):** "Pick a date. Recompute `fwd_ret` by hand from the raw returns. Does it include today?"
**Closing:** "Every accuracy number without its base rate next to it is not a number." [card 1, card 2]

### B. Two models, two splits
**Opening:** "The assistant evaluated with cross-validation. It used the sklearn default. What is the default, and why is it a leak for time series?" [card 3]
**Bet 2 (two numbers):** "Direction, gradient boosting, shuffled split — accuracy? Time-ordered — accuracy?"
**Bet 3 (a ranking):** "Which target is more predictable under the honest split — direction or volatility regime?"
**He should discover:** shuffled > ordered (leakage, not skill); direction ≈ base rate; volatility clusters and is predictable.
**Hint:** "Thursday is in the test set. Wednesday and Friday are in training with 21-day windows. How different are their features?"
**Closing:** "Same data, same models. The question decides whether ML has anything to offer. Choosing the question is the manager's job." [card 4]

### C. Leakage on purpose
**Opening:** "The assistant offers to 'smooth' the volatility feature. Centred window. Time-ordered split. What happens to the score?"
**Bet 4 (up or down, by how much):** he writes it, then runs.
**He should discover:** the score jumps although the split is honest — leakage through a feature is invisible to any validation scheme.
**Closing:** "For every feature, write the latest row it uses. Do it now on paper for the eight honest ones." [card 5]

### D. From prediction to decision
**Opening:** "A probability is not a decision. A treasury desk hedges when a high-vol week is coming: hedge costs 1, missing one costs 4. Which threshold?"
**Bet 5 (a threshold):** before the table.
**He should discover:** the cost-minimising threshold is below 0.5 because misses cost more; it moves when the cost ratio moves; accuracy is the wrong KPI because it does not price errors.
**Hint:** "What does 'never hedge' cost? 'Always hedge'? Your model has to beat both."
**Closing:** "Pick the KPI you would put on the dashboard — cost per week vs always-hedge, recall at threshold, or calibration — and defend it. This is your job; connect it to the mechanics." [card 6]

**Take-home:** "Three lines. One on the wall, one on the split, one on the threshold. Commit."

## Key concepts, in one line each
- Feature / target / horizon: what you know at t; what happens after t; how far after.
- Base rate and baseline: what a trivial rule scores; the number to beat.
- Time-ordered split / walk-forward: test data always in the future of training data.
- Leakage: future information reaching the model — through the split or through a feature.
- Accuracy vs AUC vs precision/recall: share correct; ranking quality; correctness of positives vs coverage of positives.
- Threshold: the probability above which you act; chosen on costs, not on 0.5.
- Calibration: whether a stated probability matches an observed frequency.
- Volatility clustering: large moves follow large moves; the reason vol is predictable while direction is not.

## Tutor's notes
- Needs live yfinance data from 2018 for the point about volatility to appear. Confirm before Monday; commit the snapshot if the ESE network blocks Yahoo.
- If he is fast, extension: add the 10y yield change from week 2 as a feature and see whether it helps either target (it should not, much).
- Keep gradient boosting a black box today; do not get pulled into hyperparameters.
