# Week 4 — LLM applications I: API, structured output, embeddings, RAG · EU AI Act
**Monday 12 October 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Call a language model from Python through one wrapper, choose system prompt, temperature and a JSON schema deliberately, and read the cost and latency of every call from a log.
2. Build a retrieval-augmented generation (RAG) pipeline step by step — chunk, embed, retrieve by cosine similarity, generate with citations — and explain what each step can and cannot fix.
3. Diagnose a wrong answer as a *retrieval* failure or a *generation* failure using a small test set with expected answers, and name the knob that moves each.
4. Place a fintech customer assistant in the EU AI Act: risk tier, transparency duties, and the difference between the provider of a general-purpose model and the deployer of a system built on it.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW3 walkthrough** | he presents |
| 09:20–10:00 | **A. Calling a model from Python** | whiteboard + notebook A |
| 10:00–10:45 | **B (1). Lab: corpus, chunking, the first planted bug** | hands-on, notebook B1–B2 |
| 10:45–10:55 | break | |
| 10:55–11:20 | **B (2). Lab: embeddings, retrieval, generation, the second bug, test set, cost** | hands-on, notebook B3–B6 |
| 11:20–11:50 | **C. EU AI Act** | reading + whiteboard discussion |
| 11:50–12:00 | **Homework brief** | |

### HW3 walkthrough (20')
Memo first, notebook second. Two questions: is the base rate written next to every accuracy figure, and does the "what would have to be true" section name a decision, a cost per error and a KPI? Then pick two features from his table and ask him for the latest row each one uses. If the leaky variant is missing or unlabelled, that is the first thing to fix, not a footnote.

### A. Calling a model from Python (40')
Whiteboard: one box, four arrows in (prompt, system, temperature, schema), two arrows out (text or JSON; a log row with tokens, latency, cost) [card 1]. He has used chat windows for two years; what he has never done is treat the model as a *component with a price*. The wrapper `llm()` is the only interface the course will use from here to the capstone; the else-branch is the only provider-specific code.

Three cells, worked-example style: a plain call; temperature 0 vs 1 (bet first); structured output with a `pydantic` schema and an `assert` on the value. The point of the schema: the type is guaranteed, the truth is not. He still verifies the number against the sentence, as in week 1.

If no key: the notebook prints a loud MOCK banner and every call returns canned text. Retrieval numbers are real in mock mode, generated answers are not. Make sure the key is in Colab Secrets before Monday.

### B. Lab: a RAG pipeline, step by step (70' in two halves)
Whiteboard before any code: the four boxes — chunk, embed, retrieve, generate — and the question that drives the whole block: *when the answer is wrong, which box is wrong?* [card 2]

**Corpus.** Three synthetic 10-K risk-factor excerpts (companies that do not exist, in the style of Coinbase, PayPal and a regional bank) plus the Bitcoin whitepaper abstract. Live EDGAR Item 1A sections are added on top when the network allows; the synthetic set is always loaded because the planted bugs depend on exact text.

**Chunking, bet, 🔍 CHECK 1 — the assistant's chunker.** Bet on the chunk count from a 60-page 10-K, then run the assistant's function. Two mistakes: the 500 "tokens" are characters (units — the week-2 family), and the fixed cut ignores sentences, so one chunk ends `$1,2` and the next starts `50 million`. No embedding can retrieve a fact that exists in no chunk. Corrected cell: sentence-aware, token budget, one-sentence overlap. He checks that the figure is whole again [card 3].

**Embeddings and retrieval.** Three tiers behind one interface: Gemini embeddings (key) → sentence-transformers (download) → TF-IDF (week 1, labelled as the fallback it is). Cosine similarity is a dot product after normalisation [card 4]. The check: rephrase the debt question without the words "convertible" and "debt"; with TF-IDF the score collapses. Business version of the week-1 gap: customers do not use your vocabulary.

**Generation with citations, bet, 🔍 CHECK 2 — the refactored answer function.** Bet on the outage question with k=1 on the bad chunks (facts split across two chunks). Then the assistant's "self-contained" `answer_v2()`: it assembles the passages into `ctx` and formats the prompt with `context`, the new parameter, which is empty — the model sees no context and answers from memory, fluently. A second bug hides behind the first: `argsort(sims)[:k]` takes the *least* similar chunks. Proof is in `CALL_LOG`: the retrieved text is not in the prompt. Corrected cell adds an `assert` that would have caught both, plus a live price entering the prompt through `extra_notes` (the course price loader).

**Test set, bet, cost, bet.** Six questions with expected strings; two columns, retrieval hit and answer hit [card 5]. A miss in the first column is chunking/embedding; a miss only in the second is generation. This table is the homework. Then the cost cell: per-call averages from the log, scaled to 1,000 questions a day [card 6].

### C. EU AI Act (30')
Reading at the end of this file (5' silent), then the three prompts on the whiteboard, all on one case: *a fintech assistant answering customer questions*, which is what he will build for the minor case brief. The corpus gives a factual anchor: Lumen and Arno Valley expect their creditworthiness models to be high-risk; Nordwind expects transparency and oversight duties for its LLM support bot — same law, different tiers, decided by use [card 7]. Last cell of the notebook retrieves those passages.

Prompts:
1. **Risk tier.** The assistant answers "how do I dispute a charge" and "what is my balance". Which tier, and what exactly changes the day it starts answering "can I have a higher credit limit"? (Annex III: creditworthiness of natural persons.)
2. **Transparency.** Article 50 says the customer must know they are talking to a machine. Design the sentence and its place in the interface. Then the internal version: citations and "not in the provided context" are transparency towards your own compliance team — what would you log, and for how long?
3. **Provider vs deployer.** Google provides the general-purpose model; the fintech deploys it and provides the system. Which obligations are inherited through the model's documentation and which are the fintech's own? Use his Gazprom-Media and Kaspersky pilots: who in those organisations would have signed the risk assessment?

### Homework brief (10')
`homework.md`. Emphasise: the hit/miss table with one word per miss is the deliverable; the corpus is the excuse. This homework is the first half of the minor case brief.

## Script

### HW3 walkthrough
- Opening: "Read me the sentence in your memo that says what the model beat and by how much. Now show me the base rate next to it."
- Closing: "Next Monday you will present a RAG system; today you learn why its errors are of two kinds."

### A. Calling a model from Python
- Opening question: "You have used the model through a chat window for two years. What does the window hide from you?" (Expected: the system prompt, the temperature, the price, the token count.) Draw [card 1].
- Worked example: cell A0, 30 seconds: "Four arguments. Everything else in this course goes through this function."
- **Bet 1 (A1):** "Same prompt, temperature 0, twice. Identical character for character — yes or no? And at temperature 1?" He writes two answers. Runs. Discover: at 0 nearly always identical but not guaranteed (the API does not promise it); at 1 different wording, same facts. Hint if stuck: "Read the two T=1 answers aloud — what stayed the same?" Closing: "Temperature 0 for extraction, higher only when you want variety. Never rely on determinism you were not promised."
- A2 worked example: the schema. "What does the `assert` prove, and what does it not prove?" Discover: type yes, truth no. 🔍 CHECK (5'): change the field to dollars. Closing: "The schema is a parser, not a fact-checker. The fact-checker is you, with the source."

### B (1). Corpus and chunking
- Opening question at the whiteboard: "The model has never read the Nordwind filing. Name every way you could make it answer about it." (Expected: paste the whole thing; fine-tune; retrieve the relevant part.) Draw [card 2]. "Today, the third. When the answer is wrong, which of the four boxes is wrong? That is the only question."
- **Bet 2 (B2):** "A 60-page 10-K, 3,000 characters a page, chunks of 500 tokens. How many chunks?" He writes a number. Runs. Discover: ~4 characters per token, so ~45,000 tokens, ~90 chunks. Hint: "How many characters is one token? The cell prints it." Closing: "You will never again be surprised by a token count."
- **🔍 CHECK 1 (10' alone):** "The assistant wrote this chunker. It runs. It has two mistakes. Find them; then look at what happened to the convertible notes." Hint after 5': "Print the mean tokens per chunk. What unit is 500 in?" Discover before the tutor speaks: characters vs tokens; the `$1,2` / `50 million` cut. Then the corrected cell. Closing: "A fact cut in half exists in no chunk. Overlap is not elegance, it is insurance." [card 3]

### B (2). Embeddings, retrieval, generation, tests, cost
- Opening: "Week 1: TF-IDF matched words. What does the neural embedding match?" Draw [card 4]. Run B3, then the rephrasing check. Closing: "Your customers do not use your vocabulary. Embeddings are the fix; TF-IDF is the diagnostic."
- **Bet 3 (B4):** "Outage question — duration *and* accounts — k=1 on the bad chunks, where the two facts are in different chunks. Complete / partial and honest / partial and confidently wrong?" Discover: with one chunk the model can only see half; a strict system prompt makes it say so, a loose one makes it fill in. Hint: "Read the retrieved chunk before reading the answer." Closing: "Partial context produces confident partial answers. k and chunk size are product decisions."
- **🔍 CHECK 2 (10' alone) — with Bet 4:** "The assistant refactored `answer()`. It runs and, with a key, the answers read well. Bet first: the answer to the transaction-fee question is in the corpus — will the model answer it correctly even if retrieval gives it nothing?" He writes yes/no. Then: "Two mistakes. `CALL_LOG` keeps every prompt — prove whether the model saw the passages." Hint after 5': "Print `CALL_LOG[-1]['prompt']`." Discover: empty CONTEXT (variable shadowing) and reversed sort. Closing: "Log every prompt. In tests, assert the retrieved text is inside it. Bugs hide each other; the log does not."
- **Bet 5 (B5):** "Six questions, k=3, this embedder. How many retrieval hits?" Runs. Discover: with the corrected chunks retrieval is near-perfect on this tiny corpus; generation is where the answers diverge. Then the check: re-run with k=1 and 60-token chunks, "which knob moved which column?" [card 5] Closing: "Retrieval miss: fix chunks, embedder, k. Generation miss: fix prompt, schema, model. Different fixes, so name the failure first."
- **Bet 6 (B6):** "1,000 customer questions a day, k=3. Dollars per day?" He writes a number. Runs. Discover: cents per day with a small model; the frontier model is ten times more, still small; latency is the real product constraint. Hint: "Tokens in × price in, plus tokens out × price out." [card 6] Closing: "The model is cheap. The evaluation is what costs you, and it is what you are paid for."

### C. EU AI Act
- Opening after the reading: "Three of the four documents mention the Act. Which two say 'high-risk' and why, and what does the third say instead?" Run the last cell. Draw the tier ladder [card 7].
- Prompts 1–3 above, ten minutes each, he speaks first on every one. Closing: "The Act classifies uses, not models. Your assistant's tier is decided by the question it is allowed to answer."

### Close
- "Three lines for a colleague who wants to 'add an AI assistant' this quarter." Commit.

## Key concepts, in one line each
- System prompt / prompt / temperature / schema: who the model is; what you ask; how much randomness; what shape the answer must have.
- Tokens, cost, latency: the three numbers logged per call; ~4 characters per token in English.
- Structured output: JSON validated against a schema — guarantees the type, not the truth.
- RAG: chunk, embed, retrieve, generate — make the model answer from your documents, with citations.
- Chunk size and overlap: the token budget per passage and the repeated tail that keeps facts whole across a boundary.
- Embedding and cosine similarity: text as a vector; similarity as a dot product of unit vectors.
- Retrieval failure vs generation failure: the answer was not in the retrieved passages vs it was and the model still got it wrong.
- Prompt logging: keep every prompt sent; the only proof of what the model saw.
- EU AI Act tiers: prohibited, high-risk, transparency, minimal — assigned by use, not by technology; GPAI providers have their own duties.
- Provider vs deployer: who puts the system on the market under their name vs who uses it under their authority.

## Tutor's notes
- **Needs the API key** in Colab Secrets (`GEMINI_API_KEY`). Without it the whole lab runs in MOCK mode: retrieval and both planted bugs still work, but bets 1, 3 and 4 lose their point. Check on Sunday evening with a one-line call.
- EDGAR fetch needs the ESE network to allow `sec.gov`; if it fails the notebook falls back to the synthetic corpus silently and nothing else changes. If it works, one real 10-K section (~60k chars) joins the corpus and B5 top scores drop — good talking point, but do not let it eat time.
- Embeddings: with a key, Gemini `text-embedding-004`. Without a key, `sentence-transformers` is a 2–3 minute download; decide before class whether to allow it or stay on TF-IDF.
- Model name and prices in the notebook (`gemini-2.5-flash`, `PRICE_PER_1M`) are illustrative; check the provider's price page the week before and update the constants.
- If behind: cut the B3 rephrasing check and the B5 re-run with k=1; never cut CHECK 2 or the cost cell. The EU AI Act block keeps 30' whatever happens — it is the only regulation slot until week 7.
- Energy: B (1) is dense; the break must happen at 10:45. The Act block after the lab works because it is talk and he will have opinions — let him argue about the credit-limit example, that is where the concept lands.
- He will ask about Russian or Moscow-era systems; the answer is the same: the tier follows the use, and extraterritorial scope applies when the output is used in the EU.

## Reading — EU AI Act

**What it is.** Regulation (EU) 2024/1689, the Artificial Intelligence Act, is the first general law on AI systems. In force since 1 August 2024, it applies in stages: prohibitions from February 2025, duties for general-purpose AI models from August 2025, most high-risk duties from August 2026. The Commission has proposed adjusting parts of this timeline; check the current state before relying on a date. It reaches providers and deployers inside the EU and anyone whose system's output is used in the EU.

**Four tiers, by use.** The Act does not regulate "AI" as a technology; it classifies *uses*. *Prohibited*: social scoring by public authorities, manipulative techniques that cause harm, untargeted scraping of facial images, a few others. *High-risk* (Annex III): among others, systems that evaluate the creditworthiness of natural persons, price life and health insurance, screen job applicants, or manage access to essential services. A high-risk system needs risk management, data-governance and technical documentation, logging, human oversight, accuracy and robustness testing, and a conformity assessment before it goes to market. *Transparency* (Article 50): people must be told when they interact with an AI system, and generated audio, image, video or text must be marked as such. *Minimal risk*: everything else — spam filters, recommendation engines, internal tools — with voluntary codes.

**General-purpose AI models.** The models behind the `llm()` wrapper have their own chapter. Their *provider* must keep technical documentation, give downstream developers what they need to integrate the model, respect copyright law and publish a summary of training content; models above a compute threshold are presumed to carry *systemic risk* and must also be evaluated, red-teamed and reported on. These duties sit with the model provider, not with the company calling the API.

**Provider vs deployer.** A *provider* develops a system, or has it developed, and places it on the market under its own name. A *deployer* uses a system under its own authority. A fintech that builds a customer assistant on a third-party model is a deployer of the model and, usually, the provider of the assistant. A deployer of a high-risk system must follow the instructions for use, ensure trained human oversight, keep the logs, monitor performance and inform the people affected. Substantially modify a high-risk system, or put your name on it, and you become its provider.

**Penalties.** Up to 7% of worldwide turnover for prohibited practices, 3% for most other breaches, 1% for supplying incorrect information.

**Why it matters for the case you are building.** Whether your assistant is a transparency-tier chatbot or a high-risk credit tool is decided not by the model but by the questions it may answer and the decisions it feeds. Draw that line on purpose, write it down, and log every prompt — the log that caught today's second bug is the log a supervisor would ask for.
