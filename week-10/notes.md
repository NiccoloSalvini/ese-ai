# Week 10 — Implementation and operating model; capstone studio
**Monday 30 November 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Turn "prototype → production" into three decisions with numbers attached: build/buy/partner for his own pipeline, the cost of inference at target volume, and a latency budget against a target.
2. Compute the cost of a query from tokens in, tokens out and the two prices, and show where a cost estimate breaks (volume, tier, caching, routing) with a sensitivity table and a break-even value per query.
3. Score the readiness of his capstone on data, technology, people and governance, and convert every low score into a gate in a 30/60/90 roadmap with KPIs and a rollback.
4. Pass his own repo through the review checklist and rehearse the six-beat presentation storyline against the clock.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW9 walkthrough** (red-team log) | he presents |
| 09:20–10:10 | **B. Prototype → production, as decisions with numbers** | whiteboard + notebook B |
| 10:10–10:20 | break | |
| 10:20–10:40 | **C. Readiness, roles, roadmap** | notebook C |
| 10:40–11:40 | **D. Studio** — review pass on the repo, then rehearsal | his repo on the projector |
| 11:40–12:00 | **Wrap-up** — portfolio brief, three take-home lines for the course, commit | |

(The plan in the course design says studio 1:20–2:40; C is short and the studio starts ten minutes early. If C runs long, take the time from the review pass, not from the rehearsal.)

### HW9 walkthrough (20')
Open the red-team log before the canvas. Pick two attacks at random and ask: what did the pipeline do, what should it have done, which control in the canvas now covers it. Then the two-lines-of-code rule on the control he implemented (input filter, output check, whatever it is). One question to end: which finding is still open — that is the first row of today's readiness table.

### B. Prototype → production, as decisions with numbers (50')
He has run pilots for a living; what he has not done is put the numbers on a pilot before deciding. The block reuses his safe ground (build/buy/partner, roadmap) but every cell ends in a figure he cannot produce from experience alone.

**B1 (10').** The week-6 scoring table, now with his capstone components as rows. Weights × scores; 🔍 CHECK: move one weight by 0.10 and see whether the ranking flips. If it flips, the table is not deciding — he is, and the memo should say why.

**B2 (15').** Cost of inference. Whiteboard: a query as two arrows into the model box (input: system prompt + retrieved chunks + question) and one arrow out (answer). Price per million tokens, two prices. He bets the cost per query of his *own* main prompt (he has the token count from week 4 — if not, count it with tiktoken on the spot). Then the 🔍 CHECK planted bug: the assistant's estimate that prices only the output tokens. It prints $90/month; the true figure with an 8,000-token RAG prompt is ~$890. Off by 10× and always in the same direction, because the assistant's mental model of "a query" is a chat turn, not a document pipeline. Rule: **every cost figure shows tokens_in and tokens_out separately, next to the two prices.** Corrected cell = the calculator with a caching parameter.

**B3 (10').** Sensitivity table: volume × tier, without and with caching. The point is not the number but the shape: which cells are ten times the budget.

**B4 (10').** Routing and break-even. Bet: at what monthly volume does the frontier model exceed a $2,000 budget? Chart: cost vs volume by tier with the routed mix as a dashed line; bars of value-minus-cost per query. The question the chart cannot answer: is the frontier model actually better on his golden set? No evals → no routing, only guessing. This connects week 5 to money.

**B5 (5').** Latency budget: stages summed; generation is `tokens_out / tokens_per_second` and usually the biggest line. 🔍 CHECK: halve `tokens_out` and watch cost and latency drop together — the one lever that improves both.

### C. Readiness, roles, roadmap (20')
**C1.** Readiness checklist as a dataframe: 13 items over data / technology / people / governance, weight 1–3, score 0–2. He fills his own scores; the cell prints readiness by area and the gates (weight ≥ 2, score 0). It is a map of where the pilot breaks first, not a grade.

**C2.** Roles table with names, not departments. If the owner and the validator are the same name, there is no validation. For a one-person capstone the honest answer is "the tutor" or "nobody yet" — write it down.

**C3.** 30/60/90 roadmap as a table: scope, gate criteria that can fail, KPI, rollback, owner. 🔍 CHECK: for each gate criterion, point to the notebook cell that produces the number. No cell → the gate is a wish.

### D. Studio (60')
Two passes, his repo on the projector, tutor does not touch the keyboard.

**Review pass (30').** Run the *final checks* cell on his `capstone/` folder (mechanical checks: notebooks, error outputs, dated snapshots, memo/canvas/roadmap/README present). Then the non-mechanical items of the review checklist below, in order, him reading each cell aloud. Every FAIL becomes a line in a to-do list at the top of his memo draft; the to-do list is the output of this half hour.

**Rehearsal (30').** He presents from the storyline below, timed. First run uninterrupted with the timing table on the desk; feedback after, in the order: did the number at beat 3 land, did the limits at beat 5 sound like his own finding or like a disclaimer, did he finish in time. Second run only of the beats that overran.

### Wrap-up (20')
`homework.md` is the portfolio brief. Read the rubric together (5 × 20) and the operational definition of "reproducible". Then three take-home lines for the whole course, not this session, and the last commit of the term.

## Script

### HW9 walkthrough
- **Opening:** "Pick a line in your red-team log at random. What did the pipeline do, and which control in the canvas covers it now?"
- **Bet:** none.
- **Discover:** at least one attack is still uncovered; he says so before I ask.
- **Hint:** "Read the 'status' column of the log aloud."
- **Closing:** "The open one is the first row of the readiness table we build at 10:20."

### B1 — Build / buy / partner
- **Opening:** "In week 6 you scored this for a generic case. Rows are now your pipeline: retrieval, model, evals, monitoring. Which option wins, and by how much?"
- **Bet:** none (arithmetic, not discovery).
- **Discover:** after the 🔍 CHECK, whether a 0.10 weight change flips the ranking.
- **Hint:** "Take the 0.10 from 'skills you actually have' and give it to 'control over data'."
- **Closing:** "If it flips on 0.10, you decided, not the table. The memo says why you decided." `[card 1]`

### B2 — Cost of inference (planted bug)
- **Opening:** "Your main prompt: how many tokens go in, how many come out? Write both. Now write what one query costs on the frontier tier."
- **Bet 1 (write it down):** cost per query of his main prompt, in dollars, and monthly cost at his target volume.
- **Then:** "The assistant estimated it for you — cell 9. It runs. Find what is wrong. Ten minutes."
- **Discover:** only output tokens are priced; input is 27× larger; the true figure is ~10× the printed one.
- **Hint (after 5'):** "How many arrows go *into* the box on the whiteboard?"
- **Closing:** "Any cost you write in the memo shows tokens in, tokens out and the two prices. If I cannot see both, the number is not verified." `[card 2]`

### B3 — Sensitivity
- **Opening:** "Before you run: which cells of the table will be above your budget?"
- **Bet:** none (extends bet 1).
- **Discover:** caching moves the frontier row by less than switching tier; volume matters more than either.
- **Hint:** "Read the table by column first, then by row."
- **Closing:** "A sensitivity table is the honest form of a cost estimate: it shows the reader where the number breaks." `[card 3]`

### B4 — Routing and break-even
- **Opening:** "At what monthly volume does the frontier model, no routing, exceed $2,000 a month? Write the number."
- **Bet 2 (write it down):** the volume. (With the defaults: ~45,000 queries/month.)
- **Discover:** the routed mix is closer to the small model than to the frontier one; the break-even value per query is just the cost per query.
- **Hint:** "Budget divided by cost per query."
- **Closing:** "The chart tells you the cost of routing. Only your golden set from week 5 tells you its price in quality. No evals, no routing." `[card 4]`

### B5 — Latency
- **Opening:** "Sum the six stages in your head. Over or under five seconds?"
- **Bet 3 (write it down):** over / under, and which stage is the biggest.
- **Discover:** generation dominates (80% here); halving `tokens_out` fixes latency and cost together.
- **Hint:** "Which line has 'tokens' in it?"
- **Closing:** "Shorter outputs are the one lever that improves both columns. It goes in the roadmap." `[card 5]`

### C1 — Readiness
- **Opening:** "Score the thirteen items for your capstone. Before the cell runs: what is your overall readiness, as a percentage?"
- **Bet 4 (write it down):** the percentage.
- **Discover:** the gates are in people and governance, not in technology; the technical part is the easy part.
- **Hint:** "Look at the weights of the zero rows."
- **Closing:** "The pilot breaks where the score is zero and the weight is three. That row is the first gate of your roadmap." `[card 6]`

### C2 — Roles
- **Opening:** "Who validates? A name."
- **Bet:** none.
- **Discover:** the owner and the validator are the same person.
- **Hint:** "Would a bank accept that?"
- **Closing:** "Write 'nobody yet'. It is a true sentence and it belongs in the memo."

### C3 — Roadmap
- **Opening:** "For each gate criterion, which cell in your notebook produces the number?"
- **Bet:** none.
- **Discover:** at least one criterion has no cell.
- **Hint:** "Search the notebook for the KPI name."
- **Closing:** "A gate without a cell is a wish. Add the cell as a deliverable or delete the criterion." `[card 7]`

### D — Studio
- **Opening (review pass):** "Run the final-checks cell on `capstone/`. Read every FAIL aloud, then restart and run all — on the projector."
- **Opening (rehearsal):** "Fifteen minutes from now you have finished. Go." — timer visible.
- **Discover:** which beat overruns; usually beat 2 (the pipeline) because it is the part he built.
- **Hint:** none during the run; feedback after.
- **Closing:** "Beat 3 is the sentence they will remember. Everything else supports it." `[card 8]`

### Wrap-up
- **Opening:** "Three lines for the whole course. What can you do now that you could not do on 21 September?"
- **Closing:** "Commit. Portfolio due Sunday 6 December, 23:59. Presentation Monday 7 December, 09:00, this room."

## Review checklist (used in the studio; the same list is in `homework.md`)

Mechanical (the *final checks* cell reports these):
- [ ] `capstone/` contains at least one notebook, `memo.md`, `canvas.md`, `roadmap.md`, `README.md`, a `data/` folder with a dated snapshot.
- [ ] No error outputs saved in any notebook.
- [ ] A take-home cell exists.

Not mechanical (read the cell aloud):
- [ ] Restart-and-run-all from a clean Colab runtime passes with **no API key** (mock path) and with the key.
- [ ] Every data loader has the three tiers and prints which one it used.
- [ ] The evaluation is time-ordered (or the eval set is held out by construction) and the **baseline is stated next to every score**.
- [ ] The forward target, if any, has its hand check; the feature table has the "latest row used" column.
- [ ] Backtests (if any) include costs and a walk-forward; the pitfall checklist from week 7 is answered line by line.
- [ ] LLM calls go through the `llm()` wrapper; prompts are in the repo, not in a chat history.
- [ ] The cost of a query is shown as tokens_in, tokens_out, two prices, and a monthly figure at target volume.
- [ ] The canvas from week 9 is current: every red-team finding has a status and a control.
- [ ] The roadmap's gate criteria each point to a cell that produces the number.
- [ ] The memo's "what would have to be true" section names the single strongest reason it might not work.
- [ ] AI-use disclosure present, specific, and includes what the assistant got wrong.

## Presentation storyline — six beats, 15 minutes

| Beat | Content | Time | Cumulative |
|---|---|---|---|
| 1. The decision | Who decides what, how often, and what it costs to get it wrong today. One sentence on the user. | 1'30" | 1'30" |
| 2. The pipeline | Data → features/retrieval → model/LLM → decision. One diagram, one live cell if it is safe. | 3'00" | 4'30" |
| 3. The honest result | The number, the baseline next to it, the split or eval that produced it. The sentence they will remember. | 3'00" | 7'30" |
| 4. What it would cost to run | Cost per query and per month at target volume; latency vs target; build/buy/partner in one line. | 2'00" | 9'30" |
| 5. What could go wrong | Top three rows of the canvas; the red-team finding that is still open; the kill-switch. | 2'30" | 12'00" |
| 6. What would have to be true | The roadmap's first gate; the single strongest reason it might not work; the ask. | 1'30" | 13'30" |
| Q&A buffer | | 1'30" | 15'00" |

Rules for the rehearsal: no beat starts without a number on screen; beat 3 is spoken from memory; if beat 2 overruns, cut the live cell, not beat 5.

## Six questions for the revision week (the tutor will ask at least three)
1. Pick a random line of code in your pipeline: what does it do, and what is the latest row of data it uses?
2. What is the baseline your result is compared with, and why is that the right baseline and not an easier one?
3. Your cost per query: which tokens are input, which are output, and which price applies to each? What happens to the monthly figure if volume is 10× your assumption?
4. If the model or the API disappeared tomorrow morning, what would the user see, and who would switch it off?
5. Which red-team finding is still open, and what is the control you would build first with one more week?
6. What did the assistant get wrong that you caught, and how did you catch it?

## Twelve-week self-study plan (after the course)

| Week | Focus | Evidence in the repo |
|---|---|---|
| 1 | Re-run the capstone from a clean runtime with fresh data; fix what broke. | commit "refresh" with a new dated snapshot |
| 2 | Python fundamentals without the assistant: functions, loops, dicts, errors (one hour a day, e.g. the official Python tutorial, chapters 3–8). | `practice/py-basics.ipynb` |
| 3 | pandas without the assistant: rebuild the week-2 EDA from memory. | `practice/eda-from-memory.ipynb` |
| 4 | Move the pipeline out of the notebook: one `.py` module with the loaders and the `llm()` wrapper, imported by the notebook. | `capstone/src/` |
| 5 | Tests: five `assert`-based tests on the loaders and the target construction; run them before every commit. | `capstone/tests/` |
| 6 | Second provider: swap the LLM wrapper to another API (OpenAI-compatible endpoint or a local open model); regression eval before/after. | eval report in `evals/` |
| 7 | Backtesting depth: implement a purged walk-forward and a simple transaction-cost model; reread the week-7 pitfall list. | updated backtest notebook |
| 8 | On-chain depth: one protocol's data pulled weekly by a scheduled script; a monitoring chart with an alert threshold. | `monitor/` |
| 9 | Evals as a habit: extend the golden set to 50 items; add one LLM-as-judge criterion and measure its agreement with you. | `evals/golden_v2.csv` |
| 10 | Model risk documentation: write a one-page model card for the capstone, the way a bank's validation team would read it. | `capstone/model_card.md` |
| 11 | Ship a tiny interface (Gradio or Streamlit) for one user; log every query and its cost. | `app/` + a log file |
| 12 | Retrospective: rerun the readiness table; write what changed and the next three gates. | `capstone/retro.md` |

Rule for all twelve weeks: the assistant is allowed, but every week has one artefact produced without it, and the README says which.

## Key concepts, in one line each
- Cost per query: `tokens_in × price_in + tokens_out × price_out`, per million; input dominates in document pipelines.
- Cached input: the reusable prefix (system prompt + fixed context) billed at a discount when the provider serves it from cache.
- Routing: sending easy queries to a small model and hard ones to a frontier model; cost is a weighted average, quality is what the evals say.
- Break-even value per query: the value one query must create to cover its cost; below it the system loses money on every call.
- Sensitivity table: the same figure across the assumptions that could move it; the honest form of an estimate.
- Latency budget: stage times summed against a target; generation time = tokens_out / tokens per second.
- Readiness: weighted 0–2 scores over data, technology, people, governance; zeros with high weight become gates.
- Gate: a criterion that can fail, with a KPI that shows whether it passed and a rollback for when it did not.
- Kill-switch: who can stop the system, how fast, and whether that has been tested.
- Reproducible: a stranger with the repo and no key gets the same numbers; with the key, the same numbers up to the model's stated nondeterminism.

## Tutor's notes
- Nothing in this notebook needs a key or the network; all cells run offline. The only live element is his repo: he must have it cloned or mounted in Colab before 10:40 (ask on Telegram on Sunday).
- The prices in `PRICES` are illustrative tiers. Check the provider's price page on Sunday and update the three rows in `build_nb.py` if they have moved; the argument does not depend on the exact figures, the ratio input/output does.
- If behind: cut B1 (he did it in week 6) and C2 (fold roles into the roadmap table). Never cut the planted bug in B2, the review pass, or the rehearsal.
- If ahead: in B4, replace the fixed 80/20 routing split with a split driven by a confidence score from his own evals; or add a second budget line for the latency chart.
- Energy: the studio is hour three. Keep it his voice and his keyboard; the tutor's only tool is the timer and the checklist. The rehearsal must happen — a first run that goes badly on 30 November is worth more than a polished memo on 6 December.
- Feedback template for the ESE record is in `final_feedback_template.md`; fill it after the presentation on 7 December.
