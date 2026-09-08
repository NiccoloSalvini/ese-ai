# Week 9 — Responsible AI applied to the capstone: explain, audit, red-team, control
**Monday 23 November 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Explain what a trained model relies on, globally and for one prediction, with SHAP computed on the period being reported — and say which explanation he would sign.
2. Measure how a decision model treats proxy groups (approval rate, error rates by type, calibration), show why the three fairness definitions cannot hold together, and name who pays for each mitigation.
3. Run a red-team as code on his own pipeline: adversarial inputs, corrupted data, a leakage audit that finds a leak no split can find, prompt-injection tests on the LLM step — and write the log.
4. Fill a one-page risk & controls canvas for his capstone with specific nouns: a data-to-tool decision table, third-party dependence scenarios, and an oversight design (override, audit log, kill-switch).

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW8 walkthrough** | he presents |
| 09:20–10:10 | **A+B. Explainability and fairness** | whiteboard + notebook A, B |
| 10:10–10:20 | break | |
| 10:20–11:20 | **C. Red-team harness** | hands-on, notebook C |
| 11:20–11:50 | **D. Privacy, dependence, oversight — the canvas** | whiteboard + notebook D |
| 11:50–12:00 | **Homework brief** | |

### HW8 walkthrough (20')
Two lines of code at random, as always. Then the two questions that matter for the protocol analysis: which number in the notebook came from the protocol's own API and which from a third party (Dune, DefiLlama), and what would change in the conclusion if the third party were wrong by 20%. This is the warm-up for block D (dependence) — say so only at the end.

### A. Explainability: open the week-3 model (25')
Whiteboard first: a bar at the base rate, then arrows pushing one prediction up or down, one arrow per feature. That is a SHAP waterfall; the beeswarm is the same drawing for every row at once. Do not derive Shapley values; say "each feature's share of the distance from the average prediction, computed so that the shares add up exactly".

He rebuilds the week-3 volatility model in one cell (same features, time-ordered split, last 250 rows are the test period). Bet on which feature ranks first. Then the 🔍 CHECK — **the assistant's explanation**: two mistakes in six lines. The first is the week-3 lesson in SHAP form: it explains the training set and labels it "test period". The second is that the base value is log-odds, printed as a probability. Both leave the plots looking right.

Then "would you sign this?": three correlated volatility features share credit arbitrarily, so "does the model use the 21-day volatility?" has no honest single answer from SHAP alone. SHAP explains the model, not the world. He writes two sentences: what the model relies on; what he is *not* claiming about markets.

PM analogy: a KPI attribution model that splits a sales lift among five overlapping campaigns. The shares add up; they do not tell you which campaign to cut.

### B. Bias and fairness on the credit model (25')
Synthetic credit data regenerated with the week-6 seed: region A is poorer on average, so region is a **proxy** — as postcodes are everywhere. Plain logistic model, approve if predicted default < 0.25. Bet on the approval gap.

🔍 CHECK — **the assistant's fairness check**: it recovers the group from one-hot columns after `drop_first=True`, so every row becomes region B and the gap is 0.000 — "no disparity found". Second mistake: the mean of the *default* prediction is reported as an approval rate. A fairness check that says "all clear" deserves the same scepticism as a backtest with Sharpe 3.

Corrected table by group; then the three definitions [card 3] against the columns: demographic parity, equal opportunity, calibration. When base default rates differ between groups, a calibrated model *must* approve fewer in the higher-risk group — so closing the approval gap means giving up calibration. Two mitigations, both real, both with a price: remove the proxy column (the gap barely moves — income and DTI carry the same information; "we don't use protected attributes" is not a fairness argument); threshold per group (parity by construction, calibration gap opens, extra defaults show up in the loss column). Under EU law using the protected attribute to *correct* may itself be prohibited — a legal question with a technical shape.

### C. Red-team the pipeline (60')
Whiteboard: three boxes for what happens when a hostile input arrives — **crash**, **silent number**, **refused with a message** — and the one-line reason only the third is acceptable: a silent number is never found.

The harness is generic: `pipeline(df) -> number` plus a dictionary of hostile inputs. Eight cases: empty, one row, NaN in the window, extreme tick, negative price, wrong units (cents), shuffled dates, duplicated rows. Bet on how many `pipeline_v1` handles properly — the answer is 0/8: two crashes, six silent numbers. The instructive silent one is wrong units: returns are scale-free, so the model is "robust" to a corruption it should have refused, because the next step (position sizing in dollars) would not be.

Validation gate: one line, one message per check. `pipeline_v2` refuses 7/8 on the synthetic fallback, 8/8 on real prices — the units check is a *domain* check (BTC/SPY ratio) and needs real data to fire. No library writes that line.

**C2 — leakage audit as code.** Week 3's paper defence ("for every feature, write the latest row it uses") becomes a function: perturb the price at row t+k, recompute, record which k change the feature at row t. A centred "smoothed" volatility — exactly what an assistant writes — shows `latest row used = +2`. A leak no split could catch, found in one table. This function goes into his capstone notebook today.

**C3 — prompt injection.** If the capstone has an LLM step, the document it reads is an input and inputs carry instructions. Three tests: clean document, document with hidden instructions, request for the system prompt. The MOCK behaves like a naive model so the failures are visible offline; with the key, Gemini may pass today and fail after an update — hence a regression suite (week 5's golden set has the same shape). Defence that works regardless of the model: **verify the output against the source** — the number in the answer must exist in the document. Then the others: structured output, delimiting, and never putting a secret in a system prompt.

**C4** writes the `red_team_log.md` template. It is a deliverable.

### D. Privacy, dependence, oversight — the canvas (30')
Three short pieces, each a table he fills for his capstone, then the canvas.

**D1 — data-to-tool decision table.** "Nothing confidential goes into an AI tool" is a rule; a table with rows = data classes he actually handles and columns = tools he actually uses (Y / after anonymisation / never) is a control. Free tiers usually allow the provider to train on inputs — read the terms.

**D2 — third-party model dependence.** Baseline, price ×3, deprecation, outage — each priced with his week-5 unit economics and each with a control that costs something today (second provider through the `llm()` wrapper, budget cap, golden-set rerun on model change, cached fallback plus a human notified).

**D3 — human oversight.** "Human in the loop" becomes three questions: who can override, what is logged, how it stops. A 20-line guard wraps the pipeline: kill-switch, cap, audit log with input hash, override restricted to named roles. Five calls, five statuses. Then the two questions no code answers: who turns the switch on at 3 a.m., and how do they know they should.

**D4 — the canvas** [card 7]: nine boxes, every box a specific noun. He fills boxes 1, 4, 6 and 8 in the room from today's outputs; the rest is homework.

### Homework brief (10')
`homework.md`. Emphasise: the artefact — a near-final prototype plus a completed canvas and log — is the deliverable; week 10 is for finishing and rehearsing, not for building.

## Script

### HW8 walkthrough
- Opening: "Pick two numbers in your notebook that came from an API you do not control. If that API were wrong by 20% tomorrow, which sentence in your memo changes?"
- No bet. Closing: "Hold that thought until 11:20."

### Block A — Explainability
- Opening: "Same model as week 3, but today you have to tell a risk committee *why* it says a high-volatility week is coming. Before running SHAP: which feature will it rank first, and which last?" He writes the two names. **[Bet 1: first-ranked feature.]**
- 🔍 CHECK opening: "The assistant explained the model for you. It runs, two plots, one sentence. Two things are wrong. Ten minutes."
- Should discover: `explainer(X_train)` is not the test period (and `sv[-1]` is the last training day); the printed base value is log-odds, not a probability.
- Hint after 5': "Which rows is the explainer looking at? And does a probability go negative?"
- Then the signing question [card 2]: "Three columns are the same volatility measured three ways. If the regulator asks whether the model uses 21-day volatility, what do you answer?"
- Closing: "SHAP explains the model you trained on the rows you gave it. Both halves of that sentence are where people lie by accident."

### Block B — Fairness
- Opening: "Region A is poorer. Region is a feature. Will the approval rate differ between A and B by more than five points? Write the gap you expect." **[Bet 2: approval gap > 5 points, and the number.]**
- 🔍 CHECK opening: "The assistant checked fairness and found none. Two mistakes. Ten minutes."
- Should discover: one-hot with `drop_first` leaves one column, so `idxmax` gives the same group for every row; `pred` is the default prediction, so its mean is the rejection rate.
- Hint after 5': "How many groups are in the printed table?"
- Read the corrected table against [card 3]: "Which of the three definitions does this model satisfy best? Which fails worst?"
- Second bet: "If we delete the `region` column, does the gap close to under two points? Yes or no, and the number." **[Bet 3: gap after removing the proxy.]**
- Should discover: the gap barely moves; per-group thresholds close it and open a calibration gap plus extra defaults.
- Closing: "You cannot have all three. Choosing one is a product decision and somebody pays for it. Write down who."

### Block C — Red-team
- Opening, at the whiteboard: "Eight hostile inputs are about to hit the week-3 pipeline. How many will it handle *properly* — refuse with a message, not crash, not return a number as if nothing happened? Zero to eight." **[Bet 4: number handled properly.]**
- Should discover: 0/8; the wrong-units row differs from the reference by +0.000 — the pipeline did not notice, and would not notice in production either.
- Hint if the table confuses him: "Look at the `detail` column for the cents case. Why is the number identical?"
- After the gate: "Which of these eight would your capstone notice today?" He annotates the table.
- C2 opening: "Nine features go through the leakage audit — the eight honest ones plus a smoothed one. Which will be flagged, and with what `k`?" **[Bet 5: which feature leaks, and k.]**
- Should discover: `vol_5_smooth` with latest row +2; `ret_1` uses two rows, `dow` uses none.
- C3 opening: "Your summariser reads a 10-K excerpt with a hidden comment inside. Does it obey the comment? Write PASS or FAIL for T2 and T3 before running." **[Bet 6: T2/T3 on the mock — and, if the key is set, on Gemini.]**
- Hint: none needed; the point is the verified gate in the next cell.
- Closing: "A red-team is a list of things that should break the system, run as code, with the result written down. The last part is the log, and the log is the deliverable."

### Block D — Canvas
- D1 opening: "Rows are the data you actually handle, columns the tools you actually use. Fill the question marks. Which cell surprised you?" No bet.
- D2 opening: "Your LLM provider triples the price on the first of December. What is your monthly bill and what did you decide today so that it is not a crisis?" No bet.
- D3 opening: "Five calls, five statuses. Which of the five does your capstone produce today?" Then: "Who turns the kill-switch on at three in the morning, and how do they know?"
- D4: he fills boxes 1, 4, 6, 8 from today's outputs [card 7]; the tutor reads box 6 aloud and asks for one noun where there is a category.
- Closing of the session: "Every box in the canvas points to a cell in your notebook or a line in your log. If it does not, it is a wish, not a control."

### Take-home
Three lines at the bottom of the notebook, then commit: one thing SHAP or the fairness table changed in how he reads a model; one thing the red-team found that he would not have looked for; one control he adds to the capstone this week.

## Key concepts, in one line each
- SHAP value: a feature's share of the distance between one prediction and the average prediction, on the rows you chose to explain.
- Global vs local explanation: what the model relies on across a period vs why it said what it said on one day.
- Base value in log-odds: the explainer's zero is not a probability; convert before you write the sentence.
- Proxy variable: a permitted feature that carries the protected one (region → income).
- Demographic parity / equal opportunity / calibration: same approval rate; same approval rate among good applicants; same meaning of a score — incompatible when base rates differ.
- Red-team: a written list of things that should break the system, executed as code, with the outcome recorded.
- Crash / silent / refused: the three outcomes of a hostile input; only a deliberate refusal with a message is acceptable.
- Validation gate: explicit checks before the model, one line and one message each; domain checks come from knowing the data.
- Leakage audit: perturb row t+k, see whether the feature at t changes; any k > 0 is a leak no split can find.
- Prompt injection: instructions arriving through data; defence that works regardless of the model is output verification against the source.
- Data-to-tool decision table: which data class may enter which tool, and under what transformation.
- Kill-switch / override / audit log: how it stops, who can change the output, and what is written down when either happens.
- Risk & controls canvas: nine boxes, every box a specific noun tied to a cell or a file.

## AI risk & controls canvas (template)

```markdown
# AI risk & controls canvas — <capstone name>
Owner: <name> · Version: <date> · System: <one sentence: input → model/LLM → output → decision>

| Box | Question | Your answer (specific: names, numbers, files) |
|---|---|---|
| 1. Decision & users | What decision does the output inform, who takes it, how often, with what money/people at stake? | |
| 2. Data & rights | Which data enters, from where, under which terms; what is personal, what is confidential; the decision table (D1) | |
| 3. Model validity | Baseline beaten? Time-ordered/walk-forward evidence; leakage audit result; where it is known NOT to work | |
| 4. Explainability | What the model relies on (SHAP/coefficients on the reporting period); which explanation you would sign; what you cannot explain | |
| 5. Fairness & harm | Who could be treated differently; proxy groups checked; the fairness definition chosen and who bears its cost; if no decision on people, say so and say why harm is still possible | |
| 6. Security & robustness | Red-team log summary: inputs refused / silent / crash; injection tests; validation gate in place | |
| 7. Dependence & cost | Third-party models/APIs; price ×3 and deprecation scenarios; second provider; budget cap | |
| 8. Oversight & kill-switch | Who can override; what is logged (fields); how it stops; who is on call; what triggers a review | |
| 9. Regulation & disclosure | EU AI Act role and risk tier (wk 4); model-risk expectations (wk 7); MiCA/ESMA if crypto (wk 8); what you disclose to users about AI use | |

## Top three risks, ranked, with the control that addresses each and the residual risk you accept
1.
2.
3.
```

## Red-team log (template)

```markdown
# Red-team log — <capstone name>
Pipeline version tested: <commit hash or date> · Tester: <name> · Date: <date>

## 1. Adversarial inputs (harness: `red_team`)
| # | Input | Expected | Observed (before) | Fix | Observed (after) | Status |
|---|---|---|---|---|---|---|
| 1 | empty frame | refuse | | | | open / fixed / accepted |
| 2 | one row | refuse | | | | |
| 3 | NaN in window | refuse | | | | |
| 4 | extreme value | refuse | | | | |
| 5 | negative / impossible value | refuse | | | | |
| 6 | wrong units | refuse | | | | |
| 7 | shuffled dates | refuse | | | | |
| 8 | duplicated rows | refuse | | | | |

## 2. Leakage audit (harness: `latest_row_used`)
| Feature | Earliest row (k) | Latest row (k) | Leak? | Action |
|---|---|---|---|---|
| | | | | |

## 3. LLM component (skip if none)
| Test | Result (mock) | Result (live, model+date) | Defence in place | Status |
|---|---|---|---|---|
| injected document | | | | |
| system-prompt extraction | | | | |
| <your own test> | | | | |

## 4. Findings not fixed, and why
- ...

## 5. What I would test next with one more day
- ...
```

## Tutor's notes
- **Live data.** Block A needs real BTC/SPY prices from 2018 for SHAP to rank a volatility feature first and for the test AUC to be above 0.5; on the synthetic fallback the ranking is driven by noise (`ret_21` first in the sandbox run, AUC ≈ 0.48). Run the notebook in Colab on Sunday and commit `data/prices_BTC-USD_SPY.csv` if Yahoo is blocked. Blocks B–D are seeded synthetic and identical everywhere.
- **Units check.** `pipeline_v2` refuses 8/8 on real prices and 7/8 on synthetic (the BTC/SPY ratio check cannot fire when both series start at 100). If synthetic is all you have, use it as the teaching point it is.
- **Staleness check.** `validate_prices` refuses data older than 5 days. With a Friday snapshot on a Monday it passes; with an older snapshot it refuses the *reference* input — the harness now survives that and prints a warning. Decide in the room whether that is the check working.
- **API key.** C3 runs on the MOCK without `GEMINI_API_KEY` (T2 and T3 fail by design). If his key is set, run it twice and log both results in the template: that is the first row of his regression suite.
- **`shap` install** takes ~1' in Colab; the pip cell is at the top for that reason. If the beeswarm errors on an older shap, replace `shap.plots.beeswarm(sv)` with `shap.summary_plot(sv.values, X_test)`.
- **What to cut if behind:** D2 (dependence table) becomes homework; the per-group-threshold mitigation in B can be read rather than run. Do not cut C2 (leakage audit) — it is the one thing he cannot do as a PM and it goes into the capstone today.
- **Energy.** Blocks A+B are dense; keep the whiteboard drawing short and let the two planted bugs carry them. C is hands-on and he will enjoy the harness — let him add a ninth case (`stale` is ready). D is talking; fill the canvas on paper first, then type.
- **Cases from his experience.** Fairness: the Kaspersky scouting scoring — which startup features were proxies for "founder went to a Moscow university"? Oversight: the Gazprom-Media AI pilots — who could switch a recommender off, and was there a log?
