# Homework 4 — Your own RAG, tested
**Due: Sunday 18 October 2026, 23:59 · folder `week-04/hw/` in your repo**

## Goal
Point the pipeline from class at documents of your own choosing, write ten questions with the answers you expect, and — the real deliverable — say for every miss whether retrieval or generation failed, and why. This is the first half of your minor case brief: the system you test here is the product you will present.

## Pick a corpus (one)
- **Filings.** Item 1A "Risk Factors" from three or more real 10-K or 20-F filings on SEC EDGAR (the fetcher from class, or download the HTML by hand and save it in `hw/data/`). Coinbase, Block, PayPal, Robinhood, MicroStrategy are natural for your interests.
- **Crypto and DeFi.** Three or more protocol documents — whitepapers, docs pages, governance proposals (Uniswap, Aave, MakerDAO, Lido). Save the text you used; web pages change.
- **Product management.** Three or more public documents you would want an assistant to answer from — a public API's documentation, a bank's terms and conditions, a regulator's FAQ. Nothing confidential, nothing from a former employer.
- Your own, if it is at least three documents and at least 15,000 characters in total. Message me first.

## Deliverables (in `week-04/hw/`)
1. `hw4.ipynb` — runs from a clean runtime, in mock mode too. Must contain, in this order:
   - the `llm()` wrapper and the `Embedder` class from class (copy them; change only what you must);
   - corpus loading with the three-tier pattern — live fetch, snapshot in `hw/data/`, and a clear message if neither works — and a table: **document → characters → tokens → chunks**;
   - the corrected chunker with the values of `max_tokens` and `overlap_sentences` you chose, and one sentence on why;
   - `TESTS`: **ten questions with expected strings**, at least two of which need facts from two different chunks, and at least one whose answer is *not* in the corpus (the expected answer is "Not in the provided context");
   - the **hit/miss table**: question × (retrieval hit, answer hit, top score);
   - one change to one knob (chunk size, overlap, `k`, or the embedder) with the table re-run and shown next to the first one;
   - the `assert` that the retrieved text is in the logged prompt, and the cost cell: mean tokens and cost per answer, scaled to 1,000 questions a day.
2. `memo.md` (300–400 words) with these headings:
   - **Corpus and user** — who would ask these questions, and what decision they take with the answer
   - **Results** — the two tables in one line each (hits before and after the knob)
   - **Every miss, one word and one reason** — *retrieval* or *generation*, then the mechanism (a cut number, a vocabulary gap, a passage that was retrieved but ignored, a question the corpus cannot answer)
   - **What I would not let this assistant answer** — the question that would move it to a different EU AI Act tier
   - **AI-use disclosure** — what the assistant wrote, what you rewrote, what it got wrong

## Constraints
- Every miss must be classified with evidence from the notebook: the retrieved chunks for a retrieval miss, the logged prompt for a generation miss. "The model hallucinated" without the prompt is not a classification.
- The out-of-corpus question is mandatory. If the model answers it anyway, that is a finding — report it, do not remove the question.
- Snapshot the corpus. If your notebook depends on a live fetch to run, it does not run.
- No confidential documents; no personal data of real people in the corpus or the questions.

## Scope
4–6 hours. Most of the time goes into writing good questions and reading retrieved chunks, not into code. If eight of ten hit on the first run, make the questions harder until something breaks; a table with no misses teaches nothing and reads as untested.

## Self-check
- [ ] Restart and run all: no errors, with and without the API key.
- [ ] Document table with characters, tokens, chunks is present.
- [ ] Ten questions; two multi-chunk; one out-of-corpus.
- [ ] Hit/miss table before and after one knob change.
- [ ] Every miss labelled *retrieval* or *generation* with evidence.
- [ ] Prompt-contains-context assert present and passing; cost per 1,000 questions stated.
- [ ] Snapshot saved; memo 300–400 words; AI-use disclosure present.

## How this feeds the capstone
This is the evaluation layer of the minor case brief (due Sunday 1 November): the "evaluation method" quarter of the rubric is exactly this table, extended. Week 5 adds tools and an agent on top of the same `llm()` wrapper and the same corpus; the misses you explain now become the limits section of the brief, and the tier question becomes its regulation paragraph. Choose the corpus you want to present.
