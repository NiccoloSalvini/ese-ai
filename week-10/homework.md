# Portfolio (60%) — Capstone brief
**Due: Sunday 6 December 2026, 23:59 · folder `capstone/` in your repo, link posted on Moodle**
**Final presentation: Monday 7 December 2026, 09:00 (proposed), ESE Florence, 15 minutes + questions**

## Goal
Deliver the AI pipeline you have been building since week 6 as one reproducible repository, and make the case — with numbers — for whether, how and at what cost it should be run for a real decision in finance. The portfolio is assessed on the content of the repo (notebooks, commits, markdown), not on PDFs or slides.

## What the portfolio is
Your capstone as proposed in week 6 and prototyped in week 9: a pipeline that takes market, on-chain or document data, produces a prediction, a retrieval-grounded answer, or a signal, and turns it into a decision with a stated cost of error. The weekly homework since week 3 is the raw material; the portfolio is the assembled, cleaned and defended version. Nothing new is required beyond what the course covered; what is required is that it all holds together.

## Deliverables (in `capstone/`)

1. **Working notebook pipeline** — `capstone/pipeline.ipynb` (split into two or three notebooks only if one becomes unreadable; then `01_data.ipynb`, `02_model.ipynb`, `03_decision.ipynb`, and a `README.md` says the order). Must contain, in this order:
   - data acquisition with the three-tier loaders (live → dated snapshot in `capstone/data/` → labelled synthetic), each printing which tier it used;
   - features and/or corpus, with the table **feature → latest row of data it uses** (or, for a RAG system, chunking parameters and the corpus manifest);
   - the target with its hand check, or the golden set with its provenance;
   - the model or LLM component, every call through the `llm()` wrapper, guarded so the notebook runs end-to-end without a key;
   - the honest evaluation: time-ordered split or held-out golden set, **baseline stated next to every score**, one labelled leaky or naive variant for contrast;
   - the decision layer: threshold on error costs, or backtest with costs and walk-forward, or eval-gated output — whichever fits your question;
   - the cost and latency cells from week 10, with *your* token counts, volume and target;
   - a final "Take-home" cell.
2. **Decision memo** — `capstone/memo.md`, ~2,000 words (1,800–2,300), with exactly these sections:
   - **Decision and user** — who decides what, how often, what it costs to get it wrong today.
   - **Data and pipeline** — sources, tiers, snapshot dates, what the pipeline does in five sentences and one diagram.
   - **Method and honest result** — the baseline, the split or eval, the number, one table; the leaky or naive variant next to it and what the gap means.
   - **Financial reasoning** — why the question is worth asking in this market or protocol; what theory or evidence says about whether it should be predictable, retrievable or automatable at all; what the result costs or earns in the decision's own units.
   - **Cost of running it** — cost per query with tokens in, tokens out and both prices visible; monthly figure at target volume; sensitivity to volume and tier; latency vs target; build/buy/partner in one paragraph.
   - **Risks and controls** — the top rows of the canvas, the red-team findings and their status, model-risk / AI Act / MiCA classification as applicable (one paragraph each, not more).
   - **What would have to be true** — the decision it would inform, the single strongest reason it might not work out of sample, the first gate.
   - **AI-use disclosure** (see below).
3. **Risk & controls canvas** — `capstone/canvas.md`: the week-9 canvas, current. Every red-team finding from HW9 appears with a status (open / mitigated / accepted) and, if mitigated, the cell or control that does it.
4. **Roadmap** — `capstone/roadmap.md`: 30/60/90 days, one table with scope, gate criteria that can fail, KPI, rollback, owner. Each gate criterion names the notebook cell that produces its number. Add the readiness table from week 10 with your scores and the gates it generated.
5. **Presentation** — 15 minutes on Monday 7 December, from your laptop, following the six-beat storyline in `week-10/notes.md` (decision → pipeline → honest result → cost → what could go wrong → what would have to be true). No slide deck is required; a notebook, the memo and `cards.md`-style pages are all acceptable. Whatever you show must be in the repo by the deadline.

Also in `capstone/`: `README.md` (what it is, how to run it in Colab in five lines, which cells need the key, snapshot dates) and `data/` with dated snapshots small enough to commit.

## Submission
- Everything in `capstone/` on the `main` branch of your course repo by **Sunday 6 December, 23:59**. The last commit before the deadline is what is assessed; commits after it are ignored.
- On Moodle, under *Portfolio*, post the repo URL and the commit hash. Nothing else needs to be uploaded; if Moodle requires a file, upload `memo.md` as it is.
- Before submitting, run the *final checks* cell from `week-10/session.ipynb` against `capstone/` and fix every FAIL.

## Rubric — five criteria, 0–20 each, 100 total

| Criterion | 0–20 |
|---|---|
| **Technical execution and reproducibility** | The pipeline runs from a clean runtime, with and without the key; loaders have three tiers; snapshots are dated; code is readable and every line can be explained by you. |
| **Validity of method** | No leakage; time-ordered evaluation or properly held-out golden set; baseline stated; honest backtest or eval; the leaky variant is labelled and understood; costs and thresholds are explicit. |
| **Financial-domain reasoning** | The question makes sense in its market or protocol; the result is read in the decision's own units; the limits of predictability, retrieval or automation are argued from evidence, not asserted. |
| **Product framing and roadmap** | User and decision are specific; cost, latency and build/buy/partner are quantified; readiness, gates, KPIs, rollback and owners are concrete; the canvas is current. |
| **Communication** | The memo is precise and within length; the presentation follows the storyline, lands the number at beat 3, finishes in time, and answers the questions. |

A criterion scores above 15 only if the point is demonstrated by a cell, a table or a number, not by a paragraph.

## What "reproducible" means here (operational definition)
Your notebook is reproducible if a person who has never seen it, given only the repo:
1. opens `pipeline.ipynb` in Colab, runs *Runtime ▸ Restart and run all* **without any API key**, and reaches the last cell with zero errors, with every LLM-dependent cell printing that it used the mock or cached path;
2. repeats with `GEMINI_API_KEY` set and reaches the last cell with zero errors;
3. obtains the same numbers as in your memo for every non-LLM figure (returns, scores, costs, thresholds), and the same numbers up to the provider's stated nondeterminism for LLM figures — with the snapshot tier, not the live one;
4. can find, from the file names alone, the date of every snapshot and the version of every prompt.

The tutor will do exactly this on 7 December before the presentation.

## AI-use disclosure
Assistants are allowed and expected. The disclosure in `memo.md` states, specifically: which assistants you used and for which parts (code, text, debugging, ideas); which parts you wrote without assistance; at least three things the assistant got wrong that you caught, with the cell or paragraph where it happened; and a sentence confirming that no confidential data from any employer was given to an AI tool. A disclosure that says "I used ChatGPT for help" is incomplete. Every line in the repo must be one you can explain; the tutor will pick lines at random on 7 December.

## Constraints
- No shuffled split, no evaluation without a baseline, no cost figure without tokens in and out shown separately.
- No new data source or model in the last week unless the current one is broken; polish beats scope.
- Snapshots must be small (< 5 MB each); anything larger is fetched by code with a dated file name.
- Word limit for the memo is a limit: 2,300 words including tables' captions, excluding the disclosure.

## Scope
The week-10 to week-13 hours of the course budget: 12–15 hours, most of it cleaning and defending what exists. Priority order if short of time: (1) reproducibility, (2) the honest result with its baseline, (3) the memo's cost and "what would have to be true" sections, (4) the roadmap, (5) everything else.

## Self-check (do all before the last commit)
- [ ] `final checks` cell: 9/9 mechanical checks pass on `capstone/`.
- [ ] Restart and run all, no key: zero errors, mock path announced.
- [ ] Restart and run all, with key: zero errors.
- [ ] Every score has a baseline next to it; the leaky/naive variant is labelled.
- [ ] Feature table with latest-row-used (or corpus manifest) present; hand check asserts and passes.
- [ ] Cost cell shows tokens_in, tokens_out, both prices, monthly figure at your volume, sensitivity table.
- [ ] Latency table vs a stated target.
- [ ] `canvas.md` has a status for every red-team finding.
- [ ] `roadmap.md`: each gate criterion names a cell; readiness table included.
- [ ] Memo has all eight sections and is within length; AI-use disclosure is specific.
- [ ] README explains how to run it in five lines; snapshot dates visible in file names.
- [ ] Rehearsed once against the clock; beat 3 fits in three minutes.
- [ ] Repo URL and commit hash posted on Moodle.

## How this feeds the capstone
This is the capstone. Every homework since week 3 was a part of it: the evaluation layer (week 3), the RAG or agent component and its evals (weeks 4–5), the product brief (minor case), the backtest (week 7), the protocol analysis (week 8), the canvas and red-team log (week 9), the cost and roadmap cells (week 10). The portfolio is the proof that they were one project all along.
