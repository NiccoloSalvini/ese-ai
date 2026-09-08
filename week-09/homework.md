# Homework 9 — Near-final capstone: prototype, canvas, red-team log
**Due: Sunday 29 November 2026, 23:59 · folder `week-09/hw/` in your repo**

## Goal
Bring the capstone to a state where the pipeline runs end-to-end from a clean runtime, has been attacked by you and survived or been fixed, and comes with a completed risk & controls canvas. Week 10 is for finishing and rehearsing; nothing new is built after this week. The artefact is the deliverable.

## What "near-final" means (all three)
- The pipeline runs top to bottom from *Restart and run all* with the three-tier loaders and produces the number, table or answer the decision memo will be about.
- Every harness from this session has been run on **your** pipeline, not on the demo, and the results are in the log.
- The canvas is filled with specific nouns for all nine boxes; the three ranked risks have a control each and a residual you accept.

## Deliverables (in `week-09/hw/`)
1. `capstone_prototype.ipynb` — the near-final pipeline. Must contain, in this order:
   - the data layer with three-tier loaders and a snapshot committed under `data/`;
   - the model or LLM step, with the `llm()` wrapper if there is one;
   - a `validate_*` gate before the model, one check per line, one message per check, including at least one **domain** check you wrote from knowing the data;
   - the `red_team` harness run on your pipeline with **at least eight** hostile inputs (the eight from class adapted to your data shape, plus any that are specific to your source — e.g. a protocol API returning TVL in the wrong unit);
   - `latest_row_used` run on your feature function (skip only if your capstone has no engineered features — then say so);
   - if there is an LLM step: the three injection tests plus **one you wrote**, and the output-verification gate;
   - the `guarded` wrapper (kill-switch, cap, audit log, override) around your decision function, with the five-status demonstration on your own inputs;
   - SHAP (tree models) or coefficients (linear models) computed on the **reporting period**, with the sentence you would sign written under the plot. If your capstone has no model, a one-paragraph explanation of how the LLM output is verified takes its place.
2. `red_team_log.md` — the template from class, every row filled: observed before, fix, observed after, status. Section 4 ("not fixed, and why") must not be empty; a finding you chose to accept, with the reason, is a valid entry.
3. `risk_controls_canvas.md` — the nine boxes and the three ranked risks. Every box points to a cell in the notebook or a section of the log (e.g. "box 6 → `red_team_log.md` §1, 7/8 refused").
4. `explanations.md` (only if there is a model, 200–400 words) — the global explanation, one local explanation for a date you choose, and the two sentences: what the model relies on; what you are *not* claiming about the world.

## Constraints
- The harness must run against your *actual* pipeline function, not a copy with the checks already in it. Show the before-and-after tables; the "before" is the evidence that you attacked something real.
- No "no disparity found" without the group column shown in the output. If your capstone has no decision on people, box 5 must still say who could be harmed and how.
- Secrets stay in Colab Secrets. If the injection test T3 reveals anything, the fix is to remove it from the prompt, not to ask the model to keep it quiet.
- Model name, thresholds and limits live in one `CONFIG` dict at the top; the canvas refers to it.

## Scope
5–6 hours. Order of work: (1) run the four harnesses on your pipeline as it is — one hour, and it produces most of the log; (2) fix what is cheap, accept what is not, with a reason — two hours; (3) canvas and explanations — one and a half hours; (4) restart, run all, commit. If the harness finds something you cannot fix this week, it is a ranked risk in the canvas, not a reason to hide it.

## Self-check
- [ ] Restart and run all: no errors; snapshot committed; runs without the API key (MOCK path) and, if you have the key, with it.
- [ ] Validation gate present with at least one domain check; before/after red-team tables shown.
- [ ] Leakage audit table present; every `LEAK = True` row has an action.
- [ ] If LLM step: four injection tests, results logged for mock and live with model name and date; output-verification gate in place.
- [ ] `guarded` wrapper produces the five statuses on your inputs; audit-log fields listed in canvas box 8.
- [ ] Explanation computed on the reporting period; the sentence you would sign is written.
- [ ] Canvas: nine boxes with nouns, three ranked risks with control and residual; each box points to a cell or a log section.
- [ ] AI-use disclosure and the "what the assistant got wrong" note present (there will be at least one from the harness).

## How this feeds the capstone
This *is* the capstone, one week before it is due. `capstone_prototype.ipynb` becomes the portfolio notebook (rubric: technical execution and reproducibility; validity of method). The canvas is a required portfolio component as it stands. The red-team log and the explanations are the evidence behind the decision memo's "limits and risks" section and behind three of the 15 minutes of your final presentation. Week 10 adds the build/buy/partner analysis, the cost at scale and the roadmap; it does not add code.
