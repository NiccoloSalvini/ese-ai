# Written feedback — Portfolio (60%) · template for the ESE record

Fill every `[...]` placeholder; delete this heading block and the guidance in italics before uploading to Moodle. Target length 200–400 words, formal register, English. Each rubric score is 0–20; the total is out of 100.

---

**Course:** Artificial Intelligence for Business and FinTech (Term 1, AY 2026/27)
**Student:** [Student name]
**Assessment:** Portfolio / capstone (60% of the final mark)
**Submitted:** [date] · repository `[repo URL]` at commit `[hash]` · presentation delivered on [date]
**Tutor:** [Tutor name]

| Criterion | Score |
|---|---|
| Technical execution and reproducibility | [n] / 20 |
| Validity of method | [n] / 20 |
| Financial-domain reasoning | [n] / 20 |
| Product framing and roadmap | [n] / 20 |
| Communication | [n] / 20 |
| **Total** | **[n] / 100** |

## Summary
The portfolio presents [one-sentence description of the pipeline: data source, model or LLM component, decision it informs]. The repository was executed from a clean runtime on [date] [with and without an API key / with the snapshot tier]; [it ran to completion without errors / the following cells failed: ...]. The memo runs to [n] words and the presentation lasted [mm:ss].

*Guidance: state facts that were verified, not impressions. Name the notebook and the number that the assessment turned on.*

## Strengths
[Two to four sentences. Name the specific element and where it is in the repo: e.g. "The forward target in `pipeline.ipynb` (cell 14) is verified by hand against raw returns, and the walk-forward evaluation reports accuracy and AUC next to the base rate." Cover at least one technical and one reasoning strength. If the honest result is a null result reported as such, say so explicitly as a strength.]

## Gaps
[Two to four sentences, each tied to a rubric criterion and a location. E.g. "The cost estimate in the memo (section 5) reports a monthly figure without the input/output token split, which the rubric requires for a score above 15 on product framing." Distinguish what was missing from what was wrong. Do not list more than four; the rest belongs in the oral feedback.]

## Next steps
[Two to three sentences with concrete, checkable actions and an order: e.g. "First, move the loaders and the `llm()` wrapper into a module with five assert-based tests; second, extend the golden set to 50 items and re-run the regression eval; third, write a one-page model card." Refer to the twelve-week self-study plan in `week-10/notes.md` where applicable.]

## Attendance and formative work
All ten sessions attended [/ sessions missed: ...]. Weekly homework submitted [n]/9; [note any late or incomplete submission and whether it was completed later — completion of all homework is a condition for the certificate].

[Tutor name] · [date]

---
*Word count of the sections Summary → Next steps (excluding the table and the attendance line): [n] — must be between 200 and 400.*
