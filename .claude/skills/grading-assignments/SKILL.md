---
name: grading-assignments
description: Use when marking, grading, scoring or writing feedback for a student submission in this course (weekly homework, minor case brief, portfolio/capstone), or when asked what mark/band a piece of student work deserves.
---

# Grading Assignments (ESE postgraduate)

## Overview

Two documents govern every mark. Both are local. Never search the web for criteria, never invent criteria or weightings.

1. **Assignment rubric** in the week's `homework.md` ("Rubric" table: rows with a max score, e.g. 0–25 or 0–20). This gives the structure and the numeric mark.
2. **ESE general marking criteria** in `rubric.md` (this folder; PDF original alongside). Five criteria (Relevance, Content, Depth, Structure, Style) × five bands (80–100 / 70–79 / 60–69 / 50–59 / <50). This gives the band descriptors used to calibrate each row and the overall result.

Core rule: **every score is a band decision first, a number second.** Pick the ESE band whose descriptor the evidence matches, then place the row score inside that band's proportional range.

## Procedure

1. Read the assignment brief (`week-NN/homework.md`): deliverables, constraints, rubric table, self-check list.
2. Read `rubric.md`. Load all five criteria, not a summary.
3. Read the whole submission (`week-NN/hw/` or the path given). Notebooks: run them or state that you did not. Do not grade on the brief alone.
4. For each rubric row of the assignment:
   - Map the row to the ESE criteria it expresses (see table below).
   - Quote 1–3 pieces of evidence from the submission (file + cell/section) that decide the band.
   - State the band, then the score inside the row's max.
5. Sum rows → total /100. Report the ESE band of the total.
6. Write feedback in the format below. For the portfolio use `week-10/final_feedback_template.md` verbatim.

No assignment rubric (free-standing essay, ad-hoc task): use the five ESE criteria as the rows, 20 each, same band placement.

## Row → ESE criteria mapping

| Assignment row (typical) | ESE criteria that decide the band |
|---|---|
| Problem framing / user / product framing | Relevance, Content |
| Technical build / correctness / reproducibility | Depth, Structure |
| Evaluation method / validity of method | Content, Depth |
| Reflection on limits, risk, regulation / domain reasoning | Content, Depth |
| Communication / brief / presentation | Structure, Style |

Referencing: "Harvard system" in the Style row means in-text `(Author Year)` plus a reference list; for code work, treat traceability of numbers to cells as the equivalent.

## Band placement inside a row

| ESE band | Share of row max |
|---|---|
| 80–100 | 0.80–1.00 |
| 70–79 | 0.70–0.79 |
| 60–69 | 0.60–0.69 |
| 50–59 | 0.50–0.59 |
| <50 | below 0.50 |

Example: row max 25, evidence matches the 60–69 descriptor → 15–17.

## Feedback format (weekly homework and minor brief)

```
**Mark:** NN / 100 — ESE band: <label> (<range>)

| Row | Band | Score | Evidence |
|---|---|---|---|
| ... | 60–69 | 16/25 | `brief.md` §Evaluation: golden set of 12, expected values computed in `system.ipynb` cell 9; regression has one version only |

**Strengths** (2–3, each tied to a file/cell)
**Gaps** (2–4, each tied to a rubric row and a location; distinguish missing from wrong)
**Next steps** (2–3, concrete, ordered)
```

Register: formal English, second person, facts that were verified. Quote the student's own text or code when it decides a band.

## Hard rules

- Use only the rubric rows in `homework.md` and the five ESE criteria. No extra criteria, no re-weighting.
- Do not assert institutional penalties (word count, lateness, plagiarism) as rules. Note the fact ("brief is 900 words; the range was 1,500–2,000") and let it lower the relevant row; the tutor decides any formal penalty.
- Word count and length are evidence for Structure/Style rows, never a cap on the total.
- A weak result reported honestly with a clear analysis outscores an inflated claim without evidence. The briefs say this; apply it.
- Missing deliverable file → that row's evidence column says "not submitted"; score the row from what exists, do not zero the whole assignment.
- Never fabricate a run. If the notebook was not executed, say so in Summary and grade correctness from reading only, flagged as such.

## Common mistakes (seen in baseline testing)

| Mistake | Fix |
|---|---|
| Inventing a 6-criterion rubric with weights | Rows come from `homework.md`; bands from `rubric.md` |
| Searching the web for "ESE marking criteria" | It is `rubric.md`, next to this file |
| "Under most institutional regulations this caps the mark" | Not your call; report the fact only |
| Grading the brief without opening the notebook | Read/run every deliverable listed |
| Feedback with no file/cell locations | Every strength and gap names a location |
