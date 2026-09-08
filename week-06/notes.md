# Week 6 — Minor case presentation and feedback; where AI earns money in fintech; capstone scoping
**Monday 2 November 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Present a built LLM system as a product in 8 minutes and answer questions on framing, correctness, evaluation and limits; receive written feedback against the rubric.
2. Explain why accuracy is meaningless on a 0.5%-positive fraud dataset, and choose a fraud threshold from a table that prices blocked good customers against missed fraud at production volume.
3. Read a logistic credit model's coefficients as the reason list an applicant is entitled to, and show that an approval-rate gap between groups appears even when the group variable is absent.
4. Argue a build / buy / partner decision with a weighted table, and state the one criterion that decided it.
5. Write three capstone candidates in a common template, score feasibility, pick one, and prove its data is obtainable.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:45 | **A. Minor case presentation, questions, feedback** | he presents; tutor writes |
| 09:45–10:20 | **B1. Fraud detection: accuracy is useless** | hands-on, notebook |
| 10:20–10:45 | **B2. Credit scoring: explain the rejection, check the gap** | hands-on, notebook |
| 10:45–11:00 | **B3. Build / buy / partner; what the regulator expects** | cards + notebook |
| 11:00–11:10 | break | |
| 11:10–11:50 | **C. Capstone scoping workshop** | hands-on, notebook |
| 11:50–12:00 | **Homework brief** | |

### A. Minor case presentation, questions, feedback (45')
He presents the week-4/5 LLM system as a product: 8 minutes, timed, laptop on the projector. Do not interrupt. Then 15–20 minutes of questions from the list in the Script (eight, ordered by rubric criterion; ask at least one per criterion, all eight if there is time). Then 10 minutes: fill the written-feedback template below while he reads the presentation back to himself, hand it over, and say the mark band aloud with the single sentence that decides it. The feedback is the deliverable of this block; the presentation is the excuse. [card 1] has the rubric with the four questions the criteria really ask.

### B1. Fraud detection: accuracy is useless (35')
Synthetic transactions, 40,000 rows, 0.5% fraud, generated with a seed. Say it once and clearly: the structure is realistic, the numbers are not evidence about any bank; the method is what we are learning. Two bets before any model runs (never-flag accuracy; fraud cases in a 400-row test set). Then the 🔍 CHECK — **the assistant's fraud model**: 99.5% accuracy "ready for production", plus an unstratified 400-row hold-out with ~3 positives. Both errors are silent; the code is correct and the *evaluation design* is wrong. Corrected cell: stratified 30% split, 67 positives, AUC 0.998 — and at threshold 0.5 the model still flags almost nothing, because with 0.5% positives few transactions reach 50%. Then the threshold table scaled to 100k transactions/day, with `COST_FP` for a blocked customer and the fraud amount for a miss. Bet 3 on blocked good customers at 1% FPR; the arithmetic check is 100,000 × 0.995 × 0.01. Make him change `COST_FP` to 60 and watch the optimum move: the model did not change, the business decision did. [card 2] confusion matrix with costs; [card 3] the threshold trade-off.

### B2. Credit scoring: explain the rejection, check the gap (25')
Synthetic loans, two regions, region B poorer and with shorter history; **region does not enter the default generator**. Logistic regression on purpose: the log-odds is a sum of coefficient × standardised feature, so the largest positive terms are the reasons — the "adverse action" list. Decompose one median rejection; the LLM turns the top two contributions into a three-sentence notice (MOCK without key). 🔍 CHECK: is the sentence true to the model — the two largest contributions, nothing the model did not use? Then Bet 4: does the approval rate differ by region when the model never sees region? It differs by ~40 pp. Bet 5: drop the two features most correlated with region — the gap shrinks, AUC drops, gap remains, because the base default rates differ. Finish on [card 5]: calibration by group and equal approval rates contradict each other whenever base rates differ; the lender must choose and write the choice down. Foreshadow week 9: SHAP does for gradient boosting what the coefficients did here.

### B3. Build / buy / partner; what the regulator expects (15')
The weighted table [card 7]. Weights are the argument, not the scores. Run it for credit (explainability weight 5), then re-weight for fraud and see whether the winner flips. He writes the one criterion that decided it — that sentence is the executive summary of the memo. Close with [card 6]: the three regulatory expectations he must be able to name — model risk management (a documented, validated, monitored model with an owner; week 7 in depth), explainability in credit (a reason list the applicant can act on), and GDPR Art. 22 (right not to be subject to a solely automated decision with legal effect; a human review path must exist). No reading this week; model risk gets its own slot in week 7.

### C. Capstone scoping workshop (40')
Four building weeks remain. The template makes candidates comparable: question, data, method, deliverable, risk, plan for weeks 7–10. The LLM proposes three from his stated interests (MOCK gives three sound ones); he edits each until he would defend it. Feasibility scoring with the tutor's weights, "data obtainable this week" weighing most. He picks one — or two, if the data check on Sunday may kill the first. Then the data-check pattern: load, shape, date range, missing values, dated snapshot. 🔍 CHECK: `[SYNTHETIC]` on the first line means the check has failed. [card 8] is the template.

### Homework brief (10')
`homework.md`. The proposal is one page; the data check is what makes it a proposal rather than a wish. Both due Sunday 8 November.

## Script

### A. Presentation (09:00–09:45)
**Opening:** "Eight minutes, I keep time, I do not interrupt. Your user is in the room. Go."

**The eight probing questions** (one per rubric criterion at minimum; ask in this order, follow up on the weakest answer):
1. *Problem framing and user* — "Who is the one person who uses this on a Tuesday afternoon, and what did they do before your system existed?"
2. *Problem framing and user* — "What is the one question your system must never answer, and how does it refuse?"
3. *Technical build and correctness* — "Open the retrieval step. Show me one chunk boundary. What happens if a number is cut in half?"
4. *Technical build and correctness* — "Take the key out. Does it still run? What does the mock prove and what does it not?"
5. *Evaluation method* — "How many test cases, who wrote them, and how many did the system fail? Show me the worst failure."
6. *Evaluation method* — "If I change the model name tomorrow, what number tells you whether the product got worse?"
7. *Reflection on limits, risk, regulation* — "Which EU AI Act risk tier does this fall in, and what single obligation follows from it?"
8. *Reflection on limits, risk, regulation* — "What would a hostile user type to make it say something your company would have to apologise for — and did you try it?"

**What he should discover before the tutor speaks:** that questions 5 and 6 are the same question asked twice — evaluation is what makes a product changeable.
**Closing sentence:** "Your mark is on the paper; the sentence next to it is the one thing to fix before this becomes the capstone presentation."

**Written-feedback template** (fill in during the read-back; 200–400 words when complete):

> **Minor case — written feedback · Danila · 2 Nov 2026**
> *Overall band:* ___ /100 · *The one sentence that decided it:* ______________________________
>
> **1. Problem framing and user (__/25).** Strongest point: ______. The user was / was not concrete: ______. What the brief promised that the demo did not show: ______. One change: ______.
>
> **2. Technical build and correctness (__/25).** What worked under questioning: ______. The step I could not verify: ______. Assistant-style error found / not found in the repo: ______. One change: ______.
>
> **3. Evaluation method (__/25).** Number of test cases: ___; failure rate: ___; the failure discussed: ______. Whether the eval would detect a regression: yes / partly / no, because ______. One change: ______.
>
> **4. Reflection on limits, risk, regulation (__/25).** Risk tier named: ______; obligation named: ______. Red-team attempt present: yes / no. Honest limit stated in his own words: ______. One change: ______.
>
> **Brief vs presentation.** Where the 1,500–2,000-word brief and the 8 minutes told different stories: ______. Whether the repo runs from a clean runtime as claimed: yes / no / not checked. Which of the eight questions produced the best answer: Q__, because ______; which produced the weakest: Q__, because ______.
>
> **Presentation craft (not marked, for week 10):** timing ___ / 8'; slides vs demo balance ______; the moment the audience lost the thread ______; the sentence that should have opened the talk ______.
>
> **Carry into the capstone:** the one habit to keep ______; the one habit to drop ______; the first thing to build next weekend ______.

### B1. Fraud (09:45–10:20)
**Opening question:** "A card issuer sees 100,000 transactions a day and half a percent are fraud. If you were the fraud manager, which number would you want on your dashboard every morning?" (Let him answer; do not correct yet.)

**Bet 1 (he writes it):** "A rule that never flags anything — what accuracy does it score?" Expected discovery on running: 99.4%; a number that high catches zero frauds. Hint if stuck: "What fraction of the rows is *not* fraud?"
**Bet 2 (before the assistant's cell):** "The assistant holds out 400 random transactions. How many fraud cases are in that test set?" Expected: ~2 (the run gives 3). Discovery: any recall on that set is 0, 1/3, 2/3 or 1 — no model can be judged on it.
**🔍 CHECK:** "Two problems in this cell. It runs, it is green, it says excellent. Ten minutes." One hint after 5': "One problem is in the number it reports, the other is in what it reports the number *on*." Explanation only after he has found at least one. Then the corrected cell; point at the confusion matrix at 0.5: 45 caught, 22 missed, 4 good customers blocked — "why so few flags from a model with AUC 0.998?" [card 2]
**Bet 3 (before the threshold table):** "At a 1% false-positive rate, how many good customers do we block per day?" Expected: ~1,000 (995). Discovery: the number is arithmetic on FPR and volume, nothing to do with the model's cleverness. [card 3]
**Then:** "Set `COST_FP` to 60. Which row wins now?" He should see the optimum move from threshold 0.03 upward.
**Closing sentence:** "Accuracy tells you what the majority is. The threshold table tells you what to do. Only the second one goes to the fraud committee."

### B2. Credit (10:20–10:45)
**Opening question:** "A rejected applicant writes in and asks why. Show me the sentence you would send, and show me where in the model it comes from."
**Worked example (tutor, 30"):** the decomposition cell; "log-odds is a sum, the largest positive terms are the reasons." He reads the table and says the two reasons aloud before the LLM cell runs.
**🔍 CHECK:** "Is the notice true to the model?" Expected discovery: the MOCK notice names debt-to-income and *short history* — but for this applicant `history_years` contributes negatively; the second reason should be `late_payments`. An explanation more persuasive than the model is a compliance problem. (With a live key the notice will usually match; check anyway.)
**Bet 4 (before the fairness cell):** "The model never sees region. Same approval rate for A and B, or a gap? How many points?" Expected: most people bet 'same' or 'a few points'; the run gives ~42 pp. Hint if he cannot explain it: "Which features differ by region in the first table of this block?"
**Bet 5:** "Drop income and history, the two features most correlated with region. Does the gap close?" Expected: it shrinks to ~26 pp and the AUC drops; it does not close, because base default rates differ (17% vs 28%). [card 4] for the formula, [card 5] for the theorem.
**Closing sentence:** "You cannot have equal approval rates and equal default rates among the approved at the same time when base rates differ. Pick one, write it down, be ready to defend it — that is week 9's canvas."

### B3. Build / buy / partner; regulator (10:45–11:00)
**Opening question:** "You are the bank. Which of the two models this morning would you buy from a vendor, and which would you never let out of the building?"
**Worked example:** run the table for credit; then "re-weight it for fraud" — cross-institution signal up, explainability down. Discovery: the winner flips on one or two weights; the scores hardly matter. Hint: "Change only the weights, not the scores."
**[card 6]:** read the three expectations aloud, one sentence each; ask him which of the two models each applies to.
**Closing sentence:** "The memo is the one criterion that decided it. Everything else is appendix."

### C. Capstone scoping (11:10–11:50)
**Opening question:** "In five weeks you present for 15 minutes to someone who will ask 'so what should I do?'. What is the question you want to be able to answer?"
**Run the candidate cell.** "Three proposals from your interests. Which of the three would you be embarrassed to present as your own? Fix that one first." He edits the dictionary; he fills the weekly plan; any week that says 'explore' is sent back.
**Feasibility scoring:** he scores, tutor challenges the 'data obtainable' score only: "Have you seen the endpoint? Have you seen the date range?"
**Data check cell:** worked example on BTC; "adapt it to your source before Sunday." 🔍 CHECK: "[SYNTHETIC] means fail." If the ESE network blocks Yahoo, show that `[snapshot]` from the committed CSV passes.
**Closing sentence:** "A capstone is a question, a dataset you have already loaded, and four weekends that each end with a file. Anything else is a wish."

### Homework brief (11:50–12:00)
"One page, and a notebook that proves the data exists. If the notebook prints [SYNTHETIC], the proposal is not in." Then three take-home lines and commit.

## Key concepts, in one line each
- Class imbalance: when positives are rare, accuracy measures the base rate, not the model.
- Stratified split: keep the positive rate equal in train and test; without it small test sets carry a handful of positives.
- Precision / recall / FPR: of the flagged, how many were fraud; of the fraud, how many were flagged; of the good customers, how many were blocked.
- Cost-weighted threshold: choose the cut-off that minimises (blocked good customers × contact cost) + (missed fraud × amount), at production volume.
- Adverse action reasons: the largest positive contributions to log-odds; what a rejected applicant is entitled to know.
- Proxy discrimination: features carry the group; removing the group variable is not a control.
- Calibration by group vs equal approval rates: two fairness definitions that cannot both hold when base rates differ.
- Model risk management: a model with an owner, documentation, validation and monitoring; week 7 in depth.
- GDPR Art. 22: no solely automated decision with legal or similarly significant effect without safeguards, including human review.
- Build / buy / partner: a weighted table whose weights are the argument.
- Feasibility: data obtainable now, method covered by week 9, fits four weekends, useful if negative.

## Tutor's notes
- **Nothing in blocks B needs live data.** Both datasets are synthetic with fixed seeds by design; every number is reproducible offline. Do not spend a minute apologising for it — say once why (no lawful, realistic labelled fraud/loan data), then move on.
- **API key:** only two cells call `llm()` (adverse-action notice, capstone candidates). The MOCK is deliberately imperfect for the notice — the second reason is wrong for the median applicant — which makes the 🔍 CHECK work *better* without a key. With a live key, the notice usually matches; check anyway.
- **Data check cell** needs yfinance; if the ESE network blocks Yahoo, commit a `data/prices_BTC-USD.csv` snapshot before Monday so it prints `[snapshot]` and the pattern is shown as passing.
- **If behind:** cut the build/buy sensitivity run (keep the card); cut Bet 5 (dropping correlated features) and state the result. Never cut the feedback write-up or the data check.
- **Energy:** the presentation drains him; B1 is deliberately bet-heavy and fast to restart. B2 is the intellectual peak (the fairness theorem) — protect it. The break must be a real break before scoping; scoping is a conversation, not a lecture, so sit next to him.
- **Feedback mark:** decide the band before the questions end; the write-up should not take longer than ten minutes. Hand it to him on paper; it is also the first document in his portfolio's "reflection" folder.
- Keep SHAP to one sentence (week 9). Keep model risk to one card (week 7).
