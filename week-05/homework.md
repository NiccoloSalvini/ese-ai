# Midterm — Coinbase's third quarter, read by you and an AI (40%)
**Due: Tuesday 3 November 2026, 23:59 · Moodle ▸ *Turnitin Midterm Submission* · presentation and oral on Thursday 5 November**

## The idea
Coinbase publishes its results for the third quarter of 2026 on **Thursday 29 October**, after Wall Street closes — about 21:00 in Florence. You are the analyst. Before the numbers come out, you build a notebook on Coinbase's documents and use it to predict the quarter. After they come out, you test the notebook on the new document and score both of you against a rival that does no work at all: *"Q3 will be like Q2"*.

Six steps, one sheet, one note. Each step uses one session of the course. No code.

## Files {#files}
Download from the course site (right-click ▸ *Save link as…*):

- [SHC015_MIDTERM_GUIDELINES.pdf](https://niccolosalvini.github.io/ese-ai/week-05/data/SHC015_MIDTERM_GUIDELINES.pdf) — this page as a PDF, the same file linked in Moodle.
- [midterm_sheet.xlsx](https://niccolosalvini.github.io/ese-ai/week-05/data/midterm_sheet.xlsx) — the sheet, one tab per step. Upload it to your Drive and open it with Google Sheets; the grey cells are formulas and fill themselves.
- [coinbase_10k_fy2025.txt](https://niccolosalvini.github.io/ese-ai/week-04/data/coinbase_10k_fy2025.txt) — Coinbase's 10-K for 2025, the one from session 4.
- [coinbase_q2_2026_deck.txt](https://niccolosalvini.github.io/ese-ai/week-05/data/coinbase_q2_2026_deck.txt) — Coinbase's Q2 2026 earnings presentation, 30 July 2026, as plain text. The charts were images: their numbers survive without labels, so check any chart number against the [original on EDGAR](https://www.sec.gov/Archives/edgar/data/1679788/000167978826000087/q226earningsdeck_sec.htm).
- [btc_2025_2026.csv](https://niccolosalvini.github.io/ese-ai/week-05/data/btc_2025_2026.csv) — Bitcoin daily closes, 1 January 2025 – 25 October 2026 (already inside the sheet).
- **On Thursday evening:** the Q3 2026 earnings presentation, from [investor.coinbase.com](https://investor.coinbase.com) ▸ *Financials* ▸ *Quarterly results* (or on EDGAR as an 8-K, the same evening or the next morning).
- Optional: the [Q1 2026 presentation](https://www.sec.gov/Archives/edgar/data/1679788/000167978826000053/q126earningsdeck-finalse.htm), 7 May 2026.

## The six steps

| Step | By | What you do | Session |
|---|---|---|---|
| **1. The model** | Wed 28 Oct | Open the model card and the pricing page of the model you use in AI Studio — for the default one, the [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) and [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing). Write down the context window, the price of an input and of an output token, and the knowledge cutoff. Then one line: which of your documents can the model have seen in training? | 1 — reading a model release |
| **2. Look first** | Wed 28 Oct | In Gemini Notebook, with the 10-K and the Q2 presentation as sources, fill Coinbase's revenue for the last five quarters. Check every number by hand on the slide or page. Chart it against the BTC price (already in the sheet) and write two lines: what moves with what? | 3 — explore before you predict |
| **3. Preview** | **Thu 29 Oct, 21:00** | Five predictions for Q3, each with the document and slide your number comes from, and a confidence from 0 to 100. The rival's numbers fill themselves. Write this tab before the results: the sheet's version history shows when. | 3 and 4 |
| **4. Test** | Mon 2 Nov | Add the Q3 presentation to the notebook. Ten questions on it with the answers found by hand first, as in Homework 4, and three traps — T1, the memory trap, is already written. Then the temperature test in AI Studio. Name every miss: *retrieval*, *generation* or *memory*. | 4 — RAG · 2 — temperature |
| **5. Cost** | Tue 3 Nov | From AI Studio's token counter: what one question costs, what one analyst note costs, what it is worth to a desk, and what you would charge a desk per month. Label every estimate. | 2 — tokens · 3b — SaaS |
| **6. Rules** | Tue 3 Nov | Morgan Stanley gave its advisors an assistant like yours in 2023: what did they test before launch, and what would you test before giving yours to a desk? Is your note investment advice? Which EU AI Act tier, and the one obligation that follows? | 4 — the cases, the AI Act |

## What to upload
To *Turnitin Midterm Submission* on the course's Moodle page, by **Tuesday 3 November, 23:59** — one file in each of its three parts. Put your matriculation number, not your name, on the note and in every file name.

1. **Analyst note** — PDF, about 1,500 words, under these headings:
   - **Recommendation** — five lines, first: would you give this notebook to a desk, for what, and on which conditions?
   - **The model** · **What the numbers showed before the results** · **Preview against actual** · **How the notebook did** · **Cost and value** · **Rules and risks**
   - **AI-use disclosure** — what the assistants did, what they got wrong, what you checked by hand.
2. **Sheet** — File ▸ Download ▸ Microsoft Excel (.xlsx).
3. **Slides** — at most six, PDF.

## Thursday 5 November
Time and room on Moodle. Bring your laptop with Gemini Notebook and AI Studio signed in.

- **Presentation, 8 minutes** — your note, as at a morning meeting.
- **Live check, 5 minutes** — I add to your notebook a document you have not seen and ask one question; you check the citation in front of me.
- **Oral, 15 minutes** — one question for each of sessions 1–4, from this list:
  1. *Session 1.* An LLM writes one token at a time, choosing a likely next one. Why does that explain an invented number?
  2. *Session 1.* You open a model release. Which three lines do you read first, and why?
  3. *Session 2.* What does temperature change? What happened in your temperature test, and why?
  4. *Session 2.* An output token costs five times an input token. In your cost tab, which part of the bill is bigger, and why?
  5. *Session 3.* Why does a shuffled split lie on price data, and what does an honest split look like?
  6. *Session 3.* Your preview beat — or lost to — *"Q3 = Q2"*. Why does one quarter prove nothing, and what would?
  7. *Session 4.* Retrieval, generation, memory: one miss of each kind, from your sheet or from class.
  8. *Session 4.* Air Canada's chatbot: who paid, why, and what does it mean for your notebook on a desk?

To revise: the slides of [session 1](../lectures/01-how-llms-work.qmd), [session 2](../lectures/02-pair-programmer.qmd), [session 3](../lectures/03-one-problem.qmd) with [the anatomy of a SaaS](../lectures/03b-anatomy-of-a-saas.qmd), and [session 4](../lectures/04-rag.qmd).

## How it is marked
The five criteria of the [syllabus](../syllabus.qmd#assessment), 100 points. The oral counts: each answer is evidence for the row its topic belongs to.

| Criterion | Points | In this midterm |
|---|---|---|
| Problem framing and business relevance | 15 | The recommendation: who on a desk uses the notebook, for what, on which conditions |
| Quality and critical use of data, evidence and AI methods | 25 | Look first; the preview with its sources; the test with answers found by hand; every miss named |
| Technical artefact: does it work, is it reproducible, is it honestly evaluated | 20 | The notebook and the sheet; the live check; the temperature test |
| Risk, ethics, governance and human oversight | 20 | The memory trap, Morgan Stanley, advice or not, the AI Act tier and its obligation, what stays human |
| Clarity, professional communication and reflection | 20 | The note, the slides, the eight minutes, the oral |

Honest beats lucky: losing to *"Q3 = Q2"* with sources and a clear explanation scores higher than winning without them.

## Rules
- Every expected answer in the Test tab is found by you, in the document, before the notebook sees the question.
- Every number in the note is in the sheet, with where you found it. A number without a source is an opinion: label it.
- This is an educational simulation. No trades, and nothing here is investment advice.

## Scope
About ten hours: steps 1–3 three hours before Thursday, step 4 two hours, steps 5–6 one and a half, the note three, the slides one.

## Self-check
- [ ] Tab 1: context window, two prices, cutoff, each with where you read it.
- [ ] Tab 2: five quarters, every number checked by hand, a chart, two lines.
- [ ] Tab 3 written before Thursday 29 October, 21:00.
- [ ] Tab 4: ten questions, three traps, the temperature test, every miss named.
- [ ] Tab 5: every estimate labelled.
- [ ] Note: recommendation first, about 1,500 words, AI-use disclosure.
- [ ] Note, sheet and slides uploaded to the three parts of *Turnitin Midterm Submission* by Tuesday 3 November, 23:59, with your matriculation number in each file name.
