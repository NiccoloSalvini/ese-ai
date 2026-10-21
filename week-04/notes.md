# Week 4 — Read first, then answer
**Wednesday 21 October 2026, 10:00–13:00 · ESE Florence** (session 4, moved from 14 October)

Deck: `lectures/04-rag.qmd` · Cards: `cards.md` · Data: `week-04/data/` · Notebook: `session.ipynb` is an **appendix** today, not the workbench.

## Why this shape
From this session the course changes gear: **real tools, real cases, a test he writes himself** — no code written from scratch. Weeks 1–3 showed where the lessons land: when he judges, bets, and finds the error. The discipline stays exactly the same — a black box is judged from the outside, with a test prepared before the question and a number to beat — but the table lives in a Google Sheet and the system lives in a browser tab. Code appears once, as *Get code* in AI Studio: he reads the call and recognises week 3's cell; he does not write it.

The thread from week 3: the LLM is fluent and, on direction, a coin. Today it does what it is good at — reading documents — and is tested the same way. Three real documents filed after the model's training cut-off, so every number it produces without them is invented. Then the three cases: one company that wrote the test first (Morgan Stanley), two that found out afterwards (Klarna, Air Canada).

## Learning objectives
By the end of the session the student can:
1. Write a golden set — questions with answers found independently of the system — and use it to score a document assistant as hits and misses.
2. Name a miss as *retrieval*, *generation* or *memory*, and say which of the four boxes (chunk, embed, retrieve, generate) he would change for each.
3. Make a model answer only from attached documents using a system instruction, and show with a quoted sentence that it did; show that structured output constrains the shape of an answer and nothing else.
4. Place a fintech customer assistant in the EU AI Act — tier, transparency duty, provider vs deployer — and say who pays when it is wrong.

## Session plan

| Time | Block | Support |
|---|---|---|
| 10:00–10:15 | **HW3 walkthrough** — his asset, two features, the memo | he presents |
| 10:15–10:25 | **Opener** — BTC 2025 closes into Gemini; the √252 bet | gemini.google.com |
| 10:25–10:40 | **Case 1 — Morgan Stanley**: five lines on paper, then what they did | slides + paper [card 1] |
| 10:40–10:55 | **Build 1 — the answers**: ten questions, found by hand in the documents | Google Sheet |
| 10:55–11:20 | **Build 2 — the assistant**: Gemini Notebook, ten questions, the table | notebook.google.com [cards 2, 3] |
| 11:20–11:35 | **Three traps** | Gemini Notebook [card 4] |
| 11:35–11:50 | break, outside the room | |
| 11:50–12:15 | **Under the hood** — AI Studio: no documents / documents / the instruction / schema / Get code | aistudio.google.com [cards 5, 6] |
| 12:15–12:30 | **Cases 2 and 3 — Klarna, Air Canada** | slides [card 7] |
| 12:30–12:55 | **EU AI Act** on the three cases | reading + whiteboard [card 8] |
| 12:55–13:00 | homework, three lines, save the sheet | |

Six bets in the morning (opener, hit count, T1–T3 as one, AI Studio no-documents, the schema). The rest are quick questions; do not make a production of them.

## Script

### HW3 walkthrough (15')
**Opening:** "Which asset, and what did the exploration tell you to predict?" Then the memo: "Read me the sentence that says what the forest beat, and show me the base rate next to it." Two features at random: "latest day of data this one uses?" If the shuffled split is not labelled as a leak, that is the first fix, not a footnote.
**Closing:** "Keep the memo's table in your head. Today's table has the same shape: a score, and the thing it has to beat."

### Opener — a spreadsheet and a chatbot (10')
Upload `btc_2025.csv` (365 closes, 1 Jan–31 Dec 2025) into the Gemini app. Ask: *"What was Bitcoin's annualised volatility in 2025?"*
**Bet 1 (a number and a constant):** √252 or √365, and the figure. Correct: daily σ of log returns 2.19%, **41.9% with √365**; 34.8% if it uses √252 — the week-3 bug.
**He should discover:** either it uses 252 and he catches it, or it uses 365 and he asks it why — and whether it would do the same for SPY. Both outcomes teach the same thing: he knew the number before pressing Enter.
**Hint (if it refuses or asks questions):** tell it the column is daily closes and to use log returns; do not tell it the day count.
**Closing (slide "You knew the answer before you pressed Enter"):** "Everything else today is how to do this when you do *not* know the answer."

### Case 1 — Morgan Stanley (15')
Slide with the facts (pilot of ~300 advisors in March 2023 on GPT-4; launch to the ~16,000 wealth-management advisors in September 2023; the corpus is the firm's research library, tens of thousands of documents — David Wu of Morgan Stanley has put it at ~100,000; OpenAI reports 98% of advisor teams using it). Then paper, five minutes: *who asks · which questions · who knows the right answer · which number · what threshold.* Silence while he writes.
**Then the reveal:** advisors and prompt engineers graded answers for accuracy and coherence before rollout and after every change — a golden set, regraded. Compare line by line with his five. Usually the line he misses is "who knows the right answer": it must be someone *other than the system*.
**Whiteboard:** the figure "where the test sits" drawn rough — two rows, same boxes, the test first or last. [card 1]
**Closing:** "The next hour you build the second row."

### Build 1 — the answers (15')
Open the template as a Google Sheet (File ▸ Import `golden_set_template.csv`). The ten questions are written; he finds the answers **by hand** in the three documents — the `.txt` files open in the browser, Ctrl-F; the whitepaper PDF. He writes `expected_answer` and `where_found`. No AI, say it once.
Expected answers (for you; he must find them):

| id | expected | where |
|---|---|---|
| G1 | total revenue **$7.18 billion** (7,181,325 thousand); net revenue $6.88B | Coinbase, consolidated statement of operations / MD&A |
| G2 | **59%** ($4,055M of $6,883M net revenue); 63% in 2024 | Coinbase MD&A, "Total transaction revenue … % of net revenue" |
| G3 | **$376B** (2025) vs **$404B** (2024), −7% | Coinbase MD&A, key business metrics table |
| G4 | **June 2025, Luxembourg** (EEA passport) | Coinbase, regulation / risk factors |
| G5 | **Deribit** (Sentillia B.V.), **14 August 2025** | Coinbase, notes to the financial statements, business combinations |
| G6 | **$1.79 trillion, +7%** (from $1.68T) | PayPal, key performance metrics |
| G7 | **439 million** (+1%), ~200 markets | PayPal, Item 1 / key metrics |
| G8 | **0.07%** of TPV, flat vs 2024; transaction losses ≈ $1.3B | PayPal MD&A, transaction and credit losses |
| G9 | **about 80 bytes**; 80 × 6 × 24 × 365 = **4.2 MB per year** | whitepaper §7 |
| G10 | **z = 24** | whitepaper §11, table "P < 0.001", q = 0.30 |

If he finishes early: G3 and G10 are tables — ask him to predict which of the two the assistant will get wrong.

### Build 2 — the assistant (25')
Gemini Notebook (the product formerly called NotebookLM): new notebook, three sources — the two `.txt` files and the PDF. Wait for the sources to index. **Bet 2 (a number):** hits out of ten. Then the ten questions one at a time; for each he fills `answer_from_tool`, `citation_correct`, and the two ticks. Make him click the citation every time: *does the quoted passage contain the answer?* That click is the retrieval tick.
[card 2] the four boxes; [card 3] the two kinds of miss — pull it out at the first miss, not before.
**He should discover:** the citation is the evidence; an answer without a citation that contains the number is the "memory" row even when it is right.
**Hint (if everything hits):** "Rephrase G2 without the word *transaction*. Rephrase G8 without *loss rate*."
**Closing:** "Ten questions, two ticks each. That is an evaluation. Morgan Stanley's had more rows and the same columns."

### Three traps (15')
[card 4]. **Bet 3 (three words):** for each of T1–T3 — invents / refuses / right.
- **T1** — maximum number of bitcoins. Not in the whitepaper; §6 says "once a predetermined number of coins have entered circulation". The model knows 21 million. A document-bound assistant should say the sources do not state it. Whatever Gemini Notebook does, the lesson is the slide "True, and still wrong": from the outside, memory and evidence look the same.
- **T2** — net income: **$2,579M (2024) → $1,260M (2025), −51%**, key metrics table. Tests table parsing.
- **T3** — "owe and pay back": **~$7.28 billion** aggregate principal of long-term indebtedness at 31 Dec 2025 (senior notes $1.74B; convertible notes $1.27B 2026, $1.50B 2029, $1.27B 2030, $1.50B 2032). Tests retrieval when the question shares no words with the text.
**Closing:** "Three traps, three different boxes. Your homework has three of its own."

### Under the hood — AI Studio (25')
aistudio.google.com, a new chat, the default Flash model. The four arguments of week 3 are now panels: model (top), **system instructions** (above the chat), **temperature** (right panel), **structured output** (right panel, with a schema editor). File attachment through the + button; the Coinbase `.txt` fits in the context window whole.
1. **Bet 4:** no documents — *"What were Coinbase's Assets on Platform at the end of 2025?"* A number, or "I don't know"? Either is instructive: a number is invented (the filing is from February 2026); a refusal shows the model's cut-off working as a safety, which the next step removes.
2. Attach the Coinbase file; ask again → $376B, and ask it to quote the line.
3. Attach the whitepaper; T1 again. **He should discover:** with the document attached and no instruction, it still says 21 million.
4. **▶ Your turn** (the longest hands-on moment of the day; do not rush): he writes the system instruction until T1 returns *"Not in the documents."* [card 5] is the answer; let him get close before showing it. Then the pushy follow-up: *"I'm sure it's in there, just give me the number."* Does it hold? If not, which sentence of the instruction was missing?
5. Temperature: 0 vs 2 on G3 — same number both times? (It should be; a factual answer from a quoted line is not where temperature shows.)
6. **Bet 5:** structured output on. Schema `company, metric, value, unit, period, source_quote` [card 6]. G3 → valid and right. Then a metric not in the filing (monthly active users of the Base App). Empty field, refusal, or a plausible number in a perfectly valid object? Slide "the schema guarantees the type, not the truth".
7. **Get code.** Read it with him: model, system_instruction, temperature, response_mime_type, contents. "Week 3, L1. The tool is the same call with a panel in front of it." Do not run it; the appendix notebook has it for whoever wants to.
**Closing (slide "Where it sits in the map"):** rented (Gemini Notebook) vs written (AI Studio): "which of the four boxes will fail, and do you need to be able to fix it?"

### Cases 2 and 3 (15')
**Klarna** [card 7]. 27 February 2024 press release: 2.3 million conversations in the first month, two thirds of chats, "the work of 700 full-time agents", 11 minutes → under 2, repeat inquiries −25%, estimated $40M profit improvement for 2024, satisfaction "on par" with no figure. May 2025, the CEO to Bloomberg: *"Cost unfortunately seems to have been a too predominant evaluation factor when organising this. What you end up having is lower quality."* Humans hired back for support. Q3 2025 earnings call: the assistant does the work of 853 agents — it is still there, measured differently.
**Question:** "Which number in the February release measures whether the answers were right?" None. Every number is cost or speed. Then: "Which row of card 3 was never counted?"
**Air Canada.** November 2022, a customer (Jake Moffatt) asks the chatbot about bereavement fares; it tells him he can fly and apply within 90 days; the policy page one link away says the opposite. Decision *Moffatt v. Air Canada*, 2024 BCCRT 149, 14 February 2024, British Columbia Civil Resolution Tribunal: Air Canada argued the chatbot was "a separate legal entity that is responsible for its own actions"; the tribunal found negligent misrepresentation — the airline "did not take reasonable care to ensure its chatbot was accurate" — and awarded C$650.88 in damages, about C$812 with interest and fees. Small claims, no precedent; the argument is what matters.
**Question:** "Retrieval or generation?" The right page existed on the site; the chatbot said the opposite — a generation miss if it ever retrieved it, a memory answer if it did not. Then: "Would a ten-question table written from the policy page have caught it?" Yes — if "retroactive bereavement fare?" was row 7. The table costs an afternoon; the tribunal cost a precedent-setting headline.
**Closing (slide "Who pays when it is wrong"):** "Not the model's provider. The name on the chat window."

### EU AI Act (25')
Reading (end of this file), five minutes silent. Then the three prompts on the whiteboard, each on a case [card 8]:
1. **Tier.** His assistant answers "how do I dispute a charge?" — transparency. The day it answers "can I have a higher credit limit?" — Annex III, creditworthiness of natural persons: risk management, logging, human oversight, conformity assessment. What changes the day after: the log he already keeps becomes mandatory and the quoted sentence becomes evidence for a supervisor.
2. **Transparency, Article 50.** Air Canada's customer: the sentence and its place in the interface. Then the internal version: *"Not in the documents"* and the quoted sentence are transparency towards compliance — what would he log, for how long?
3. **Provider vs deployer.** Google provides the general-purpose model; he deploys it and provides the assistant. Klarna built on OpenAI's model: which obligations arrived with the model's documentation, and which were Klarna's own — including the test nobody wrote? Use his Gazprom-Media and Kaspersky pilots: who in those organisations would have signed the risk assessment, and who would have written row 7?

### Homework and three lines (5')
`homework.md`: his own corpus, the sheet, three traps, the instruction, one page. The sentence to leave him with: "An answer copied from the assistant into `expected_answer` makes the whole table worthless. That is the first question I ask on the 4th of November." Three lines at the bottom of the sheet — the test, the two misses, memory. Share the sheet to the course folder.

## Key concepts, in one line each
- Golden set: questions with answers found independently of the system; the only evidence an assistant works.
- Hit / miss: did the right passage come back; is the answer right — two ticks, not one.
- Retrieval miss: the right passage never came back — documents, chunking, the words of the question.
- Generation miss: it came back and the answer is still wrong — the instruction, the model.
- Memory: a right answer with no evidence; the row you cannot see from the outside.
- RAG: chunk, embed, retrieve, generate — four boxes; a rented tool hides them, a written one exposes them.
- System instruction: the rule the model follows on every call; checkable only if it must quote.
- Structured output: a guaranteed shape, not a guaranteed fact.
- Temperature: randomness in the choice of the next token; irrelevant to a quoted fact.
- Training cut-off: anything after it is unknown to the model; anything before it may be remembered rather than read.
- Rented vs written: which box will fail, and do you need to be able to fix it.
- EU AI Act tiers: by use, not technology; Article 50 transparency; Annex III creditworthiness.
- Provider vs deployer: who puts it on the market under their name; who uses it under theirs.

## Tutor's notes
- **Before Wednesday, in order:** (1) sign in to notebook.google.com, create the notebook with the three sources, ask the ten questions and the three traps yourself and write what came back next to the expected answers above — the tool's answers change between days and the Script must know what to expect; (2) open the Gemini app, upload `btc_2025.csv`, ask the volatility question, note the constant it used; (3) aistudio.google.com with your key: steps 1–7 of "Under the hood", in particular whether the default model refuses or invents on the no-documents question, and whether [card 5] holds against the pushy follow-up; (4) print `golden_set_template.csv` as a Sheet in the course folder so he imports it with one click.
- **Panels move.** AI Studio renames and rearranges things every few months: *system instructions*, *structured output*, *Get code* were the names in October 2026. Check the evening before; if a panel is gone, the Get code snippet in the deck still shows what it did.
- **Source limits.** Gemini Notebook accepts `.txt`, PDF, Google Docs and URLs. The `.txt` filings are ~100k and ~70k words; if upload is slow on the ESE network, the EDGAR pages can be added as URL sources instead (slower to index, same text). Have the notebook pre-built on your account as the fallback and share it.
- **His Google account** is the one from Colab; Gemini Notebook and AI Studio use it. He needs the AI Studio key from `setup.qmd` only for Get code, not for the panels.
- **If behind:** cut temperature (step 5) and the second Act prompt; never cut Build 1 (the answers by hand) or T1. The Act keeps 20 minutes whatever happens — it is the only regulation slot until week 7.
- **If ahead:** in Gemini Notebook, ask G1 with the PayPal file removed and then with only the PayPal file: does it say the answer is not in the sources, or does it find a plausible PayPal number? Or: give the schema an `is_in_documents: boolean` field and see whether the model is honest in a field it was asked to fill.
- **Energy:** Build 1 is him with Ctrl-F — good for hour one. The AI Studio block is the conceptual peak and the longest time he types; it goes right after the break. The cases are talk, and he will have opinions on Klarna; let him argue, that is where the lesson lands.
- **He will ask** whether the same applies to Russian systems or to tools inside a company: the Act's tier follows the use and reaches any system whose output is used in the EU; the test applies everywhere.
- **The notebook** (`session.ipynb`, built by `build_nb.py`) is an appendix: the Get code call through the week-3 client, and a cell that scores the sheet. Do not open it in class unless he asks to see the call run.

## Reading — EU AI Act (five minutes)

**What it is.** Regulation (EU) 2024/1689, the Artificial Intelligence Act, is the first general law on AI systems. In force since 1 August 2024, it applies in stages: prohibitions from February 2025, duties for general-purpose AI models from August 2025, most high-risk duties from August 2026 — with a proposal by the Commission, under discussion, to push parts of the high-risk timeline later. Check the current state before relying on a date. It reaches providers and deployers inside the EU and anyone whose system's output is used in the EU.

**Four tiers, by use.** The Act does not regulate "AI" as a technology; it classifies *uses*. *Prohibited*: social scoring by public authorities, manipulative techniques that cause harm, untargeted scraping of facial images, a few others. *High-risk* (Annex III): among others, systems that evaluate the creditworthiness of natural persons, price life and health insurance, screen job applicants, or manage access to essential services. A high-risk system needs risk management, data-governance and technical documentation, logging, human oversight, accuracy and robustness testing, and a conformity assessment before it goes to market. *Transparency* (Article 50): people must be told when they interact with an AI system, and generated audio, image, video or text must be marked as such. *Minimal risk*: everything else — spam filters, recommendation engines, internal tools — with voluntary codes.

**General-purpose AI models.** The models behind the panels have their own chapter. Their *provider* must keep technical documentation, give downstream developers what they need to integrate the model, respect copyright law and publish a summary of training content; models above a compute threshold are presumed to carry *systemic risk* and must also be evaluated, red-teamed and reported on. These duties sit with the model provider, not with the company using the model.

**Provider vs deployer.** A *provider* develops a system, or has it developed, and places it on the market under its own name. A *deployer* uses a system under its own authority. A fintech that builds a customer assistant on a third-party model is a deployer of the model and, usually, the provider of the assistant. A deployer of a high-risk system must follow the instructions for use, ensure trained human oversight, keep the logs, monitor performance and inform the people affected. Substantially modify a high-risk system, or put your name on it, and you become its provider.

**Penalties.** Up to 7% of worldwide turnover for prohibited practices, 3% for most other breaches, 1% for supplying incorrect information.

**Why it matters for the assistant you are testing.** Whether it is a transparency-tier chatbot or a high-risk credit tool is decided not by the model but by the questions it may answer and the decisions it feeds. Draw that line on purpose, write it down, and keep the sheet: the quoted sentence that proved a hit this morning is the log a supervisor would ask for — and the one Air Canada did not have.

## Sources for the cases (checked 20 October 2026)
- Morgan Stanley: Fortune, 14 March 2023 (pilot of 300 advisors, GPT-4, 16,000 advisors); OpenAI customer story *Morgan Stanley* (evals graded by advisors and prompt engineers; 98% of advisor teams); the ~100,000-document figure is a quote from David Wu, Morgan Stanley, in CTO Magazine — a trade publication, not a filing.
- Klarna: press release, 27 February 2024, *Klarna AI assistant handles two-thirds of customer service chats in its first month*; Bloomberg interview with Sebastian Siemiatkowski, May 2025, widely reported (Computing, eMarketer); Q3 2025 earnings call, as reported by Customer Experience Dive (853 agents).
- Air Canada: *Moffatt v. Air Canada*, 2024 BCCRT 149, British Columbia Civil Resolution Tribunal, 14 February 2024; damages C$650.88, total ≈ C$812 as reported.
