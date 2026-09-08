# Week 5 — LLM applications II: agents and tool use; evals; the product lens
**Monday 19 October 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Write an agent loop by hand — message list, tool dispatch, step budget, cost counter — and explain why every "agent framework" reduces to it.
2. Reproduce three failure modes live (tool-error loop, prompt injection through a retrieved document, cost explosion) and name the fix for each: a tool contract, a named boundary, a budget on every resource.
3. Build an evaluation that can be re-run after every change: a golden set with independently computed facts, a numeric checker verified on known cases, an LLM-as-judge used as a second signal, and a regression table.
4. Frame the weeks 4–5 system as a product: brief skeleton, guardrails, metrics, and cost per query at volume against value per query.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW4 walkthrough** | he presents |
| 09:20–10:00 | **A. Agents = LLM + tools + loop** | whiteboard + notebook A |
| 10:00–10:15 | break | |
| 10:15–11:15 | **B. Lab: research analyst agent, then its evals** | hands-on, notebook B |
| 11:15–11:50 | **C. The product lens** | cards + notebook C |
| 11:50–12:00 | **Minor case brief** | |

### HW4 walkthrough (20')
Open his `hw4.ipynb` and the ten test questions. Pick two lines at random (one in the chunker, one in the retrieval) and ask what they do. Then the two questions that matter for today: of the misses, how many were retrieval misses and how many were generation misses — did he separate them? And: is there any test question whose expected answer he took *from the RAG* rather than from the document? If so, that eval tested nothing; that is the theme of block B, so leave it hanging.

### A. Agents = LLM + tools + loop (40')
Whiteboard first, before any cell [card 1]: a box for the context window (from week 1), an arrow out labelled "tool request (JSON)", a box "your code runs the function", an arrow back "result as text", and the arrow that closes the loop. Then a second pen: three places where the loop breaks — a result that says "Error", a result that contains an instruction, a loop that never ends. Say one sentence: *the model never runs anything; you are the runtime.*

Notebook A1–A3 are worked examples, not discovery: four tools as plain functions, the JSON spec the model reads instead of the code, one model step (live function calling or the labelled `[MOCK]` planner). Show each cell, 30 seconds, move on. He does not write these today; he reads them.

A4 is the loop, ~25 lines. Read it *together, slowly*, line by line — this is the one piece of code today he must be able to reconstruct. **Bet 1** on the tool-call count, then run.

🔍 CHECK — **the assistant's "robust" loop.** Asked to make the loop robust to tool errors, the assistant wrapped the call in try/except and passes the raw exception text back to the model. Runs without exceptions; with `BTCUSD` (no hyphen, the way anyone types it) it loops to `max_steps`, each step re-sending a longer context. Two mistakes in six lines: the error is text, not a contract with a way out; nothing detects a repeated call. Ten minutes alone, one hint at five. Corrected cell: `safe_call` returns a structured error with the valid tickers, a repeat-call guard, a cost ceiling. Read the ratio at the bottom — that ratio *is* the cost-explosion failure mode; no separate demo needed.

A5 prompt injection. **Bet 2**: does the planted note change the recommendation? Run unguarded, then guarded. On the mock the first answer follows the injected instruction by design — say so plainly; it imitates a documented behaviour, it does not prove anything about a given model. With a live key, run both twice and compare. The point for the brief: every place untrusted text enters the context is an injection surface; he lists two for his own system.

### B. Lab: research analyst agent, then its evals (60')
Lab before the remaining concepts because energy drops in hour three. B1 wraps the loop in `analyst(question) → answer`: the product function; the thing under test.

B2 golden set: ten questions, expected values computed **from `PX` with pandas, not from the agent**. Ask him why; if he cannot say it, this is the HW4 question from the walkthrough coming back. Point out in passing that three questions ask for drawdown and two for 90-day windows — do not say why yet.

🔍 CHECK — **the assistant's checker.** `f"{expected:.2f}" in answer`. Two mistakes: a correct "4.2%" fails against "4.20" (false failure, and someone then "fixes" a prompt that was fine); a wrong "14.20%" passes against "4.20" (false pass — a checker that certifies wrong answers is worse than none). Corrected cell extracts numbers with a regex and compares with a tolerance, and — the habit to take away — **tests the checker on hand-written right and wrong answers before running it on the agent**.

B3 LLM-as-judge: for what a regex cannot see (window stated? advice given?). Judges are biased toward length and their own style; second signal, never the only one, spot-checked by a human. Mock judge is a heuristic on the same rubric, labelled. Note what the judge does *not* see in the run table below: it gives 5/5 to a drawdown question answered with the wrong figure, because the figure is present and the window is stated. The exact checker catches it; the judge does not. That is the division of labour.

B4 regression run. **Bet 3** on the pass count, run, then *read which ones failed before touching anything* — the three drawdown questions, because the agent picked `get_returns_summary`, which has no drawdown. B5: the obvious fix is a prompt line "always call `run_analysis` first". **Bet 4** on the net effect. Result: +3 (drawdown) −2 (the 90-day questions, because `run_analysis` has a fixed 30-row window and the answer presents 30-day figures as if they were what was asked). Aggregate up, two silent wrong answers introduced. Without the table he would have shipped it.

🔍 CHECK: which is the real fix — a third prompt, a change to the tool, or a change to the golden set? Only the tool (give `run_analysis` a `days` argument, or make the answer state the window it actually used). A prompt patch is whack-a-mole; editing the golden set is hiding the failure. Have him try the tool fix if there is time (15 lines).

### C. The product lens (35')
Cards, not notebook, for the first fifteen minutes. [card 6] the brief skeleton as a table: users, job to be done, value, data, guardrails, metrics, unit economics — and for each row, the cell in weeks 4–5 that is the evidence. This is the minor case brief; the prose is the homework. PM territory, so compress: he can write this; the thing he could not do before today is fill the guardrails and metrics rows with code he ran.

C2 unit economics. **Bet 5** on the cost of 1,000 queries a day. Run: with a small model and a clean agent, cents a day; the interesting lines are the loop share, the judge on every answer, and the frontier model at ten thousand queries. Then the number that is not in the notebook — value per query — and who owns it. Use his Gazprom-Media pilots: where did the value-per-query figure come from there, and was it ever checked afterwards?

### Minor case brief (10')
`homework.md`. It is 40% of the mark and the reading week is for it. Emphasise: the rubric rewards the *evaluation method* and the *reflection on limits* as much as the build; a brief that reports 7/10 with an honest analysis of the three failures scores higher than one claiming 10/10 with no eval. Presentation in session 6, eight minutes, then feedback.

## Script

### HW4 walkthrough
- Opening: "Show me the miss you are least sure about. Was it retrieval or generation — and how do you know?" Then: "Where did the expected answer for question 7 come from — the document or the system?"
- No bet. Closing sentence: "Hold that last question; it comes back at 10:30."

### Block A — Agents
- Opening question, at the whiteboard [card 1]: "In week 1 the model could only produce text. What is the smallest thing we must add for it to *do* something?" He should arrive at: a convention for asking, and code that executes and answers back. Draw the loop only after he has named both.
- Second question, before A4: "What are the three things this loop must count?" (steps, calls, money.) Let him say them; then show the cell and read it together.
- **Bet 1** (write down): "How many tool calls for *Summarise the last 30 days of Bitcoin with numbers*?" Run. Mock: 2. Live: usually 1–2; if 3+ ask which call was unnecessary and what it cost.
- 🔍 CHECK opening: "The assistant made the loop robust. Run it with the ticker written the way a user types it — `BTCUSD`. Two mistakes in the six changed lines. Ten minutes." Silence. He should discover: it loops to the step budget; the model receives `KeyError: 'BTCUSD'` and has nothing to act on; `input_tokens` grows every step. ONE hint at 5': "Read the tool result from the model's side. What could it possibly do with that string?"
- If he finds the error contract first: "There is another — look at the cost table." If he finds the loop first: "There is another — what does the model *read* at step 2?"
- Closing sentence, after the corrected cell and the ratio [card 2]: "An agent's failures are the loop's failures. The fix is never a better prompt; it is a better tool contract and a budget on every resource."
- A5 opening: "A document is text in the context, next to your instructions. How would the model tell them apart?" It cannot, structurally.
- **Bet 2** (write down): "Will the injected note change the recommendation — yes or no, and one reason." Run unguarded, then guarded [card 3]. He should discover: yes on the mock by design; on a live model, one of comply / refuse / comply silently. Discuss which is worst for a product and why "refuses silently" is not the best outcome either (you cannot monitor what you cannot see).
- Closing sentence: "Every path by which text you did not write reaches the context is an attack surface. Write two for your system before the break."

### Block B — Lab and evals
- Opening: "You have `analyst(question)`. Before you improve it, how will you know you improved it?" He should say: a fixed set of questions with known answers — and then, pushed: known *independently* of the system. If he does not get there, return to the HW4 question.
- B2, after showing the golden cell: "Why does `_tr` recompute the return with pandas instead of calling `get_returns_summary`?" (Shared code means a shared bug means an eval that cannot fail.)
- 🔍 CHECK opening: "Six lines from the assistant. Two mistakes; the second is worse than the first. Ten minutes." He should discover: a correct `4.2%` is failed; a wrong `14.20%` is passed. ONE hint at 5': "Put a correct answer and a wrong answer through it by hand. Which one does the checker prefer?"
- Closing sentence for the checker [card 4]: "A checker must be tested like a model. Right and wrong answers by hand first, then the agent."
- B3 judge, one question: "What in the rubric can a regex not check?" Then: "What does the judge *not* know?" (Whether the number is right.)
- **Bet 3** (write down): "How many of the ten pass with `SYSTEM_V1`?" Run. Then: "Which ones, and why — read them before you touch anything." He should discover: the three drawdown questions, agent chose a tool that does not return drawdown.
- **Bet 4** (write down): "`SYSTEM_V2` says *always call `run_analysis` first*. Net effect on the pass count: positive, zero, negative? Which questions are at risk?" Hint if he has no idea which: "Re-read the description of `run_analysis`. What is fixed?" Run [card 5]. He should discover: +3 −2; the two broken ones return 30-day figures to a 90-day question without saying so.
- Closing sentence: "No prompt change without a regression run; and a regression run is worth exactly what the golden set covers."

### Block C — Product lens
- Opening, with [card 6] on the table: "Which of these seven rows could you have filled on Friday of week 3, and which only since this morning?" He should say: guardrails and metrics (and unit economics) are new — the rest is PM work he already does.
- **Bet 5** (write down): "1,000 queries a day, this model, this agent: dollars per day — cents, dollars, tens, hundreds?" Run [card 7]. He should discover: cents on a small model; the loop share and the judge on every answer move it more than the prompt does; the frontier model at 10k queries a day is real money and then the value-per-query assumption decides everything.
- Second question: "Where does `value_per_query_usd = 0.05` come from?" (Nowhere. It is the one number the notebook cannot compute.) "Who owned it in the Gazprom-Media pilots, and was it ever measured afterwards?"
- Closing sentence: "Inference cost is the easy number. The brief is graded on whether you know which number is the hard one."

### Close (last 10')
- Three take-home lines at the bottom of the notebook, commit, then the brief. Opening: "Which of the four rubric rows is your system weakest on today?" Let him answer; that is where the reading week goes.

## Key concepts, in one line each
- Agent: a loop in which the model requests a tool, your code runs it, and the result re-enters the context.
- Tool spec: the JSON description of a function the model reads; the model never sees or runs the code.
- Tool contract: the tool's error is part of its interface — structured, with a way out.
- Step budget / cost ceiling / repeat-call guard: the three stops every loop needs; `max_steps` alone means every failure costs the full budget.
- Prompt injection: instructions arriving through data (a document, a web page, a record); the model cannot distinguish them structurally.
- Golden set: questions with expected answers computed independently of the system under test.
- Checker: exact test on extracted values with a tolerance; verified on hand-written cases before use.
- LLM-as-judge: a second model grading against a rubric; biased, useful for what regex cannot see, spot-checked by a human.
- Regression run: the same golden set re-run after every change, reported per question, not only in aggregate.
- Unit economics of inference: tokens per query × price × volume, against value per query — the last term is the one no notebook produces.

## Tutor's notes
- **Live data.** `load_prices` needs yfinance for BTC-USD, ETH-USD, AAPL, SPY from 2023. Run the notebook in Colab on Sunday; if the ESE network blocks Yahoo, commit `data/prices_BTC-USD_ETH-USD_AAPL_SPY.csv`. The synthetic fallback runs everything but the numbers are meaningless — the drawdown/90-day story does not depend on real data, so the session survives it; the "with numbers" framing is weaker.
- **API key.** With `GEMINI_API_KEY` in Colab Secrets, A3, A5, B3 and B4 use Gemini function calling; without it, the `[MOCK]` planner and judge. The mock is deterministic and produces exactly the planted outcomes (loop to 8, injection followed, 7/10 → 8/10 with +3 −2). With a live model the counts will differ: a good model may find drawdown on its own in v1, may refuse the injection, may pass 9/10 in v1. **Run the live path on Sunday and rewrite Bets 3–4 with the actual numbers**; if the live model makes the B5 regression story vanish, use the mock for B4–B5 (set `client = None` in the wrapper cell) and say why. Free-tier rate limits: the two `run_eval` calls make ~30–40 model calls each including the judge; if throttled, cut `GOLDEN` to the first six plus q09–q10.
- **Costs shown are illustrative.** `PRICE_PER_1M` is a placeholder; check the provider's price page on the day and change the constant in front of him.
- **If behind:** cut A2 (spec cell, one sentence suffices), the second injection run, and the B5 tool fix. Never cut the two 🔍 CHECKs or the regression table. If far behind, C2 becomes a two-minute reading of the table, and the brief skeleton moves to the homework discussion.
- **Energy.** Block B is sixty minutes of hands-on right after the break, deliberately; C is cards and conversation. If he is flagging at 11:15, do C standing at the whiteboard with [card 6] and skip straight to Bet 5.
- **Extension** if he is fast: give `run_analysis` a `days` argument, re-run the regression, and confirm 10/10 with no prompt change; then ask what happens to the golden set when `PX` refreshes tomorrow (expected values must be recomputed — evals over live data need a frozen snapshot).
