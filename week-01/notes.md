# Week 1 — How LLMs work, and how we will work
**Monday 21 September 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Explain, in operational terms, what tokens, context window, sampling and embeddings are, and derive from each one a practical consequence for business use.
2. Run a Colab notebook, save it to a GitHub repository, and store an API key in Colab Secrets.
3. Direct an AI assistant to write pandas code, run it, and verify the result by computing the same number a second way.
4. Distinguish, in an AI-generated answer, the claims that can be verified from those that merely sound right.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **A. Orientation and contract** | talk |
| 09:20–10:10 | **B. LLMs at a working level** | talk + notebook B1–B5 |
| 10:10–10:20 | break | |
| 10:20–11:40 | **C. First data notebook** | hands-on, notebook C |
| 11:40–12:00 | **D. Prompting that matters; homework brief** | discussion |

### A. Orientation and contract (20')
State the deal explicitly, once:
- This is a lab. He will write code from today, with an assistant; he does not need to know Python, he needs to be able to judge what the assistant produces. Every session contains something he cannot already do as a PM.
- Rhythm: Monday 9–12; homework published Tuesday; due Sunday 23:59 in the repo; first 20 minutes of every Monday are his walkthrough of the homework.
- Assessment: minor case brief 40% (after session 5, presented session 6), portfolio 60% (revision week). Both assessed on the repo.
- Tools: Colab, GitHub, one chat assistant of his choice, Gemini API key (free tier) from week 4.
- Rule of the course: *anything an AI produced and you submit, you must be able to explain line by line.*

Setup checklist to complete before block B starts (do it together, do not skip; if it slips, steal time from block B, not from C):
- [ ] Google account works in Colab; notebook opens; runtime starts.
- [ ] GitHub account; private repo `ese-ai-fintech`; tutor added as collaborator.
- [ ] `File ▸ Save a copy in GitHub` done once with path `week-01/session.ipynb`.
- [ ] Google AI Studio key created and stored in Colab Secrets as `GEMINI_API_KEY` (optional today; do it if time allows).

### B. LLMs at a working level (50')
Level: an economist with no CS background. Explain by consequence, not by architecture.

**Tokens (B1).** The model sees chunks, not words. Show the tokenizer cell: English ≈ 1.3 tokens/word, Russian ≈ 2–3×, code and numbers fragment. Consequences: cost, context limits, weaker arithmetic, weaker non-English. PM analogy: story points, not hours — the unit the system counts in is not the unit you think in.

**Context window (B2).** The model's only working memory is what is in the prompt right now. Nothing else exists for it. Hallucination is pattern completion over missing information, not deception. Run the cost cell: a 10-K is ~90k tokens; a thousand reads a day at frontier prices is real money. Consequences: chunking and retrieval (week 4), statelessness between calls, verbosity is cost.

**Sampling (B3).** Next-token distribution + temperature. T=0 for extraction and classification, higher for ideation. Run the Gemini cell live on the projector (tutor's key if his is not set). Then the 🔍 CHECK: sort the model's sentence into *verifiable* vs *plausible-unverifiable*. This is the single habit the course builds; name it as such.

**Embeddings (B4).** Text → vector; similar meaning → nearby. Run the TF-IDF cell and let him discover that paraphrases score near zero: no shared words. That gap is exactly what neural embeddings close. Do not go further today; week 4 uses real embeddings.

**Tool use and agents (B5).** Concept only: model emits a structured call, your code runs it, result returns to context; agent = that in a loop. Say now that everything in weeks 4–5 is this loop, and every agent failure (cost, infinite loop, wrong tool, prompt injection) comes from the same loop.

### C. First data notebook (80')
He drives. Tutor sits beside, does not touch the keyboard except for the projector.

1. Run the `load_prices` helper and the download. Explain only what the helper does (live → snapshot → synthetic fallback), not how; he will read it in week 2.
2. Returns, `describe()`, rebased growth chart. Ask him to read the table like a BI dashboard: which number is a mean, which a dispersion, what is the sign of the min for BTC and what date it was (he can look it up — verification habit).
3. **🔍 CHECK — the assistant's volatility cell.** Give him 10 minutes alone with it. The two planted errors: √252 applied to a 7-day asset; cumulative return as a sum of simple returns. If he finds one, push for the second. Then the corrected cell, with the "compute it a second way" column. Lesson to state: *the assistant is fluent, not correct; constants and formulas are where it fails silently.*
4. If time remains: ask him to prompt his assistant for "the maximum drawdown of each asset" and check it against the chart by eye.

### D. Prompting that matters; homework brief (20')
Run the three prompts of block D in his assistant, side by side. Draw out: role and context cut filler; explicit conventions kill silent assumptions; fixed output shape makes the answer checkable; "say so instead of inventing" reduces but does not remove invention. Then walk through `homework.md`.

## Script

### A. Orientation and contract
**Opening (no screen, seated at an angle to him):** "Before we open anything: this course is a lab, not a lecture. By December you will have built things. You will write code from today, with an assistant. What you need to learn is to judge what it gives you. Every line you submit, you must be able to explain — I will ask, randomly, every week." Then: "Second rule: I will never touch your keyboard." [card 1 for two minutes, then away]
**Closing:** "Repo created, notebook saved. That is your first commit. Everything from now on accumulates there."

### B1. Tokens (whiteboard)
**Opening:** write "The ECB left rates unchanged at 2.00% on Thursday." and cut it with vertical bars: "Thirteen chunks, nine words. Now write the same sentence in Russian for me." Cut his sentence — the Cyrillic words split into two or three pieces each.
**Bet 1 (he writes a number):** "Your company sends a thousand Russian documents a day to a model, same content as English. How much more does it cost?"
**He should discover (after the tokenizer cell):** ~2.5×, and that numbers and code fragment too.
**Hint if stuck on why it matters:** "What is the unit on the invoice — words or chunks?"
**Closing:** "The unit the system counts in is not the unit you think in. Like story points." [card 2, 30 seconds while he copies it]

### B2. Context window (whiteboard)
**Opening:** draw an empty box. "This is everything the model knows about your problem in this one call. Nothing outside the box exists. You ask about page 60 of a 10-K; only pages 1–20 are in the box. What does it answer?"
**He should discover:** it answers anyway, fluently — because it has seen a thousand 10-Ks and page 60 usually says something like X.
**Hint:** "Does it know that it doesn't know?"
**Closing:** "You have just explained hallucination: pattern completion over missing information, not lying. Write that in your words." [card 3 stays on screen while he writes]

### B3. Sampling
**Bet 2 (yes/no):** "Same question three times at temperature 1. Identical answers?" Run the Gemini cell (tutor's key on the projector if his is not set).
**Then the 🔍 CHECK, five minutes alone:** "Split every claim into two columns: verifiable in five minutes, or merely plausible."
**Closing:** "That split is the habit of this course. You will do it with every AI output you ever use."

### B4. Embeddings (whiteboard, then cell)
**Opening:** two axes, three sentences: "ECB raises rates", "monetary tightening", "football match". "Place them." He places the first two close.
**Bet 3 (a number 0–1):** "Similarity between the first two, as the crude embedding will compute it."
**He should discover:** near zero — no shared words. That gap is what neural embeddings close.
**Closing:** "Meaning as geometry. In week 4 we use the real thing." [card 4]

### B5. Tool use and agents (whiteboard only)
**Opening:** draw model → tool → model → tool in a loop. "Everything you build in weeks 4 and 5 is this loop. Everything that goes wrong with agents comes from the same loop. Name one thing that could go wrong." [card 5 for the clean version]

### C. First data notebook (he drives)
**Bet 4 (a date):** before `describe()`: "Worst single day for BTC in this sample — which date? Write it, then look it up."
**Bet 5 (a direction):** before the volatility cell: "Which asset has the highest annualised volatility, and roughly how much?"
**🔍 CHECK — ten minutes, no help:** "This cell is what the assistant writes for 'annualise the volatility'. It runs. It is wrong twice."
**Hint at 5':** "Every constant has a reason. Ask the assistant what 252 is."
**If he finds one:** "There's another. Second line."
**He should discover:** 252 vs 365 (√(252/365) ≈ 17% understated); sum of simple returns is not the cumulative return (+50, −50 → 0 vs 75).
**Closing:** "The assistant is fluent, not correct. Compute the same number a second way — do it now, from first and last price." [card 6 stays on screen]

### D. Prompting; homework brief
**Opening:** "Three prompts, same question, your assistant, side by side. What changed and why?"
**He should discover:** role and context cut filler; explicit conventions kill silent assumptions; a fixed output shape is checkable; "say so instead of inventing" reduces invention.
**Take-home:** "Three lines at the bottom of the notebook. Your words. Save to GitHub."

## Key concepts, in one line each (for his notes)
- Token: the unit the model reads, writes and bills in.
- Context window: the model's entire working memory for one call.
- Hallucination: confident pattern completion over missing information.
- Temperature: how much randomness the model is allowed in choosing the next token.
- Embedding: text as a point in space; distance ≈ difference in meaning.
- Tool use / agent: the model requests an action; your code performs it; the result re-enters the context; repeat.

## Tutor's notes
- The notebooks fall back to synthetic data when Yahoo is unreachable. Run the notebook once in Colab before Monday to confirm live data works from the ESE network; if it does not, run it at home and commit the `data/prices_*.csv` snapshot to the repo so the session runs on the snapshot.
- Tokenizer: `tiktoken` downloads its encoding on first use; needs network. Fallback is built in.
- Keep block B to 50 minutes. The temptation is to lecture; the value is in C.
