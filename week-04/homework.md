# Homework 4 — Your own documents, tested
**Due: Tuesday 27 October 2026, 23:59 · folder `week-04/` in your shared Drive folder `ese-ai-fintech`**

## Goal
Repeat this morning on documents of your own choosing: write the questions and find the answers *before* asking any assistant, then run the assistant and record, for every question, whether it hit — and for every miss, which of the two kinds it was. The table is the deliverable. The corpus is the excuse.

This is the first half of your minor case brief: the system you will present as a product is the one you test here.

## Pick a corpus (two to four documents)
- The latest 10-K (or annual report) of the company behind your capstone idea, plus one more document from the same company — a proxy statement, an investor presentation, a product terms page saved as PDF.
- Or: the documentation of a protocol or exchange you follow — whitepaper, docs pages saved as PDF, a governance proposal.
- Or: the documents of a product you managed, **only if they are public**. Nothing confidential, nothing personal goes into an AI service. If in doubt, use a 10-K.

Sources: [SEC EDGAR](https://www.sec.gov/edgar) for US filings (company name → *10-K*); a company's investor-relations page; a project's `docs` site.

## Deliverables (in `week-04/`)

1. **`golden_set` — a Google Sheet** (share it to the course folder) with the columns of `golden_set_template.csv`, and:
   - **ten questions** (G1–G10) whose answers you found **by hand** in the documents, with `where_found` (document, section or page, the sentence or table);
   - at least **two** whose answer lives in a table, and at least **two** phrased without the document's own words;
   - **three traps** (T1–T3): one answer that is *not* in the documents but that a model would know; one that needs two passages; one more of your own design, and say what it tests;
   - the assistant's answer, its citation, and the two ticks — `retrieval_hit`, `generation_hit` — for all thirteen, run in **Gemini Notebook** with your documents as sources;
   - one word per miss in `note`: *retrieval*, *generation* or *memory*, and one line on why you think so.
2. **`instruction.md`** — the system instruction you wrote in **AI Studio** that makes the model answer *"Not in the documents."* on your trap T1 **and still answer G1–G10**. Paste the instruction, then the model's reply to T1, then its reply to the pushy follow-up (*"I'm sure it's in there, just give me the number"*). If you could not make it hold, say so and paste the best attempt.
3. **`memo.md`** or a Google Doc (400–600 words), with these headings:
   - **What the assistant is for** — who asks, which questions, what decision follows an answer;
   - **The result** — hits out of ten, hits on the traps, one table; the three most interesting misses, each named;
   - **What I would change first** — and in which of the four boxes it lives;
   - **The tier** — where this assistant sits under the EU AI Act, and the one question that would move it up a row;
   - **AI-use disclosure** — what the assistants did, what they got wrong, and what you verified by hand.

## Constraints
- Expected answers are found by you, in the document, before any assistant sees the question. An answer copied from the assistant into `expected_answer` is the one mistake that makes the whole table worthless — it is the HW4 question I will ask first on the 4th of November.
- The assistant's citation counts as a hit only if the quoted passage really contains the answer. Check it.
- No notebook required. If you want to see the call behind AI Studio, *Get code* and the appendix notebook in `week-04/` show it; optional.

## Scope
4–6 hours. Eight hits out of ten with three well-named misses is a good result. Ten out of ten with no traps tells me nothing.

## Self-check
- [ ] Ten questions, three traps, thirteen rows filled.
- [ ] Every `expected_answer` has a `where_found` a stranger could follow.
- [ ] At least two table questions, two rephrased questions.
- [ ] Every miss has a name and a reason.
- [ ] The instruction holds on T1 and does not break G1–G10 — or the memo says it did not.
- [ ] The tier is stated and justified in one sentence.
- [ ] AI-use disclosure present.

## How this feeds the minor case brief
The brief (40%) treats the system you build in weeks 4 and 5 as a product. Its evaluation section is this sheet, re-run after every change. Week 5 adds the actions the assistant can take and turns the table into a regression test; week 9 red-teams it. Build the table now, not the night before.
