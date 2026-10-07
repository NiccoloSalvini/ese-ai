# Week 3 — Look first, then predict
**Wednesday 7 October 2026, 10:00–13:00 · ESE Florence**

Deck: `lectures/03-one-problem.qmd` · Notebook: `week-03/session.ipynb` (built by `build_nb.py`) · Cards: `cards.md`

## Learning objectives
By the end of the session the student can:
1. Explore an unfamiliar financial dataset by asking small questions in an order — coverage, scale, tails, memory — and say which question is worth a model before fitting one.
2. Build features and a forward target and verify by hand that the target holds nothing from day *t* or before.
3. Judge a black-box model from the outside: base rate, a one-line rule, an honest time split versus the assistant's shuffled split, permutation importance.
4. Turn a predicted probability into a decision with a threshold chosen on error costs, and check it beats both trivial policies.

## Why this shape
The previous version jumped straight into features and splits. This one spends the first hour **looking**, so that every ML result in the second hour is something he already predicted from a chart: direction has no memory, size does. The model then confirms (or fails to beat) what the exploration showed. The random forest is a **black box on purpose**: he has seen a neural network from the inside in weeks 1–2; today he learns to judge a model he cannot read, which is what he will do with every vendor.

Dataset: BTC, ETH and SPY daily since 2018 (yfinance; snapshot in `week-03/data/` as fallback). Chosen for his interests (trading, crypto) and because it carries the one finding that makes the lesson work on real data: volatility clustering.

## Session plan

| Time | Block | Support |
|---|---|---|
| 10:00–10:20 | **HW2 walkthrough** — fraud share, the release decoded | he presents |
| 10:20–10:30 | deck: where we are, how the notebook works, 0.17% | slides |
| 10:30–11:20 | **Part 1 — Explore** (E1–E5 + 🔍 CHECK) | notebook, slides at E4 |
| 11:20–11:30 | break, outside the room | |
| 11:30–11:45 | features, the wall, base rate (M1–M2) | whiteboard + notebook |
| 11:45–12:25 | **the black box** (M3, shuffled CHECK, M4, leak YOUR TURN) | slides → notebook |
| 12:25–12:50 | **probability → decision** (M5) | notebook |
| 12:50–13:00 | homework, three lines, save to Drive | |

The notebook pattern: worked cell → **✍️ BET** → **▶ YOUR TURN** (a piece of the analysis he writes, mostly on ETH or SPY, solution folded). Instead of exercises he does the next piece of the same analysis. Four YOUR TURNs in Part 1 (holidays, ETH worst/best days, SPY clustering, feature table), one in Part 2 (the leak).

## Script

### HW2 walkthrough (20')
**Opening:** "The fraud share — what is it, and what does a model that says 'never fraud' score?" (0.17%; 99.83%.) Then two lines of his release decoding chosen at random: "explain this one to me". Start from the terms he marked as not understood.
**Closing:** "Keep 0.17% in mind. Every score today gets a base rate next to it."

### Part 1 — Explore (50')
**Opening (slide "The question for the morning"):** "Is crypto risk predictable — and which part? We do not answer that with a model. We answer it with four small questions, in order."

- **E1 (quick, not a real bet):** "Out of seven days, how many is SPY missing?" ~2 of 7 (31%). Close: "Every join between crypto and stocks is a decision." YOUR TURN: holidays in 2025 — a two-line filter, good first piece.
- **E2:** worst BTC day — 12 March 2020, −37%. Ask him what happened that week (COVID crash, the BitMEX liquidation cascade). YOUR TURN: ETH worst/best days, same dates?
- **E3 — Bet 1 (a number):** "In eight and a half years, how many days beyond 4 standard deviations? A normal distribution says 0.2." Answer: **17**. Say plainly: *fat tails*. Link: any "99% VaR" that assumes normality is wrong exactly on these days.
- **E4 — Bet 2 (the central one):** "Direction or size — which one has memory?" Before running, he writes it. Chart: direction bars around zero, size bars at 0.1–0.17 for 30 lags. Then the slide **"Calm follows calm"** — this is the sentence of the morning. Whiteboard: two rows of days, arrows from big moves to big moves.
- YOUR TURN: same table for SPY. Surprise: **SPY clusters more than BTC** (size autocorrelation ~0.35 vs ~0.17). Volatility clustering is a property of markets, not of crypto. Let him find it.
- **E5:** BTC–SPY correlation by year: 0.05 (2018) → 0.57 (2022). Kaspersky/Gazprom-Media angle: "digital gold, uncorrelated" was a pitch; the data changed in 2020.
- **🔍 CHECK (10' alone, hint at 5'):** the assistant's summary table — `sqrt(252)` for crypto (should be 365) and **summed simple returns** (BTC: 360% by sum vs 517% true). If he finds one: "there's another". Hint: "How many days a year does crypto trade? What is +50% then −50%?"

**Closing of Part 1:** he writes the three lines in the notebook (direction / size / correlation). Do not skip: Part 2 checks them.

### Part 2 — Predict (80')
**Opening (slide "Three ways to write the same decision", then "Three words"):** "Two targets, same nine features: next week up? next week more volatile than usual? From Part 1 you can already guess how this ends. Write your guess." [card 3]

- **M1, whiteboard:** the wall. The features are relative to "usual" (median weekly vol of the past year) — say why in one sentence: *a forest learns thresholds, and 2024 is calmer than 2018–2023; absolute levels would teach it the wrong ones.* (It is true: with absolute vol the honest AUC is 0.47.) 🔍 hand check of `fwd_ret` — one minute, every time.
- **M2 — Bet 3 (a number):** "Share of weeks BTC went up?" 53%. Base rate.
- **M3, slide "The black box":** say what a forest is in 30 seconds; don't open it. Hint if he asks about parameters: "week 9".
- **Bet 4 (four numbers):** AUC, direction and volatility, honest and shuffled. Results (7 Oct): direction 0.55 honest / 0.70 shuffled; volatility 0.60 / 0.74; the rule "next week like this week" **0.64**. Slides "What came out" → "Read it in this order" → statement. [card 4]
  **He should discover:** shuffled is a lie; direction is a coin, as Part 1 said; volatility is predictable — **and a one-line rule beats the forest**.
  **Hint (if he cannot explain the shuffle gap):** "Thursday is in the test set. Wednesday and Friday are in training with overlapping 7- and 30-day windows. How different are their features?"
  **Closing:** "Same data, same model. The question decides whether ML has anything to offer. Choosing the question is the manager's job — and the exploration is how you choose."
- **M4:** permutation importance: `vol_30`, `vol_7`, then `ret_7` (a big week *is* a volatile week); negative bars are noise. "A black box that agrees with what you saw by eye is one you can start to trust."
- **YOUR TURN — the leak:** centred 7-day window. AUC 0.60 → **0.69** on the honest split. "Why didn't the split protect you?" [card 5]

### Probability → decision (25')
**Opening:** "The model says 0.61. Hedge costs 1, a miss costs 2. Which threshold?"
**Bet 5 (a threshold).** Table: best at 0.5, cost 0.91/week vs never 0.97 and always 1.00 → the model earns its keep.
**Then:** `c_miss = 4`. Now "always hedge" (1.00) beats every threshold (best 1.03). **He should discover:** the model did not change; the business did — and decided the model is not worth running.
**Hint:** "What does 'always hedge' cost per week? Your model has to beat that number."
**Closing:** "Pick the KPI for the dashboard — cost per week vs always-hedge, recall at threshold, or calibration — and defend it." [card 6]

**Take-home:** three lines (exploration / split / black box) at the bottom of the notebook; File ▸ Save a copy in Drive → `ese-ai-fintech/week-03/`.

## Key concepts, in one line each
- Exploration: small questions in an order — coverage, scale, tails, memory — before any model.
- Log return: the daily change that adds up over time; simple returns do not add.
- Fat tails: extreme days far more frequent than the normal curve allows.
- Autocorrelation: the correlation of a series with its own past; zero for direction, positive for size.
- Volatility clustering: large moves follow large moves — why risk is predictable and direction is not.
- Feature / target / horizon: what you know at *t*; what happens after *t*; how far after.
- Base rate and rule baseline: what doing nothing scores; what a one-line rule scores. A model must beat both.
- Random forest: hundreds of decision trees voting; judged from the outside today.
- AUC: does the model rank the 1s above the 0s — 0.5 a coin, 1.0 perfect.
- Shuffled vs time-ordered split; leakage through the split vs through a feature.
- Permutation importance: how much worse the model gets when one feature is scrambled.
- Threshold: the probability above which you act, chosen on costs.

## Tutor's notes
- Run the notebook once in Colab before 10:00: the live yfinance call should print `[live]`. If Yahoo is blocked it falls back to the repo snapshot (to 6 Oct 2026) — numbers identical to the slides. The synthetic fallback kills clustering and the whole point; if you see `[SYNTHETIC]`, stop and fix the network.
- Live numbers can differ from the slides in the second decimal (a new day of data). Say so once; the order of the results does not change.
- Eight BET cells in the notebook; only five are real bets (E3, E4, M2, M3 AUCs, M5). E1, E2 and the shuffled one are quick questions — don't make a production of them.
- If behind: cut the E5 correlation (one slide is enough) and move M5 to homework (the notebook says so).
- If ahead: in M3 swap `RandomForestClassifier` for `HistGradientBoostingClassifier` — a different black box, same verdict. Or remove the "÷ usual" from the features and watch the honest AUC fall to ~0.47: the black box learned 2018's thresholds.
- Energy: Part 1 is mostly him typing small pieces — good for hour one. The black box is the conceptual peak; put it right after the break.
- The fraud material (OpenML card fraud, 3-way software figure) is used only as the 0.17% opener and the "three ways" slide; the full fraud lab stays in the week-1 notebook § A2.
