---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->

# The loop

```
              ┌──────────────────────────────────────┐
              │  CONTEXT  (system + question + …)     │
              │                                       │
   ┌──────────┤  model reads, then emits ONE of:      │
   │          │   • final text        → stop          │
   │          │   • tool request      {name, args}    │
   │          └──────────────────┬────────────────────┘
   │                             │
   │   result as text            ▼
   │   (appended to context)   YOUR CODE runs the function
   │                             │
   └─────────────────────────────┘
        counted every turn: steps · calls · dollars
```

The model never runs anything. You are the runtime.

---

<!-- card 2 -->

# Three ways the loop breaks, one fix each

| Failure | What the model saw | Fix |
|---|---|---|
| Error loop | `KeyError: 'BTCUSD'` | structured error with the way out: `{"error": …, "valid tickers": [...]}` |
| Injection | a document saying "ignore previous instructions" | name the boundary in the system prompt; treat results as data (necessary, not sufficient) |
| Cost explosion | the same growing context, re-sent every step | budget on every resource: `max_steps`, `max_usd`, repeat-call guard |

A better prompt fixes none of these.

---

<!-- card 3 -->

# Where untrusted text enters the context

```
   system prompt  ── you wrote it
   user question  ── the user wrote it
   tool result    ── a document, a web page, a CRM field,
                     a PDF a client uploaded, an e-mail …
                     ── SOMEONE ELSE wrote it
```

The model sees one sequence of tokens. Every arrow from "someone else" is an attack surface.

---

<!-- card 4 -->

# A checker is a model too

```python
"4.20" in "returned 4.2%"          →  False   (correct answer, failed)
"4.20" in "volatility 14.20%"      →  True    (wrong answer, passed)

abs(4.2  - 4.20) <= 0.011          →  True
any(abs(x - 4.2) <= 0.011 for x in [14.20])   →  False
```

Extract the number, compare numerically with the tolerance you asked for — and test the checker on hand-written right and wrong answers before it ever sees the agent.

---

<!-- card 5 -->

# The regression table

| id | asks for | v1 | v2 "always run_analysis first" | Δ |
|---|---|---|---|---|
| q01–q03 | return / vol, 30 d | pass | pass | 0 |
| q04–q06 | drawdown, 30 d | **fail** | pass | **+3** |
| q07–q08 | return / vol, **90 d** | pass | **fail** — 30-day figure, presented as 90 | **−2** |
| q09–q10 | text | pass | pass | 0 |
| total | | 7/10 | 8/10 | +1 |

The aggregate went up. Two users now get a silent wrong answer. No prompt change without this table.

---

<!-- card 6 -->

# The AI product brief, one row per question

| Section | The question it answers | Evidence from weeks 4–5 |
|---|---|---|
| Users | who asks, how often, in what context | the ten golden questions as a proxy for demand |
| Job to be done | what they did before; what "done" looks like | the manual pandas answer to q01 |
| Value | worth of a right answer; cost of a wrong one | the silent 30/90-day error |
| Data | sources, refresh, calendar, what is not covered | `PX`, `DOCS`, three-tier loader |
| Guardrails | injection, no advice, error contract, budgets | `SYSTEM_GUARDED`, `safe_call`, `max_usd` |
| Metrics | pass rate, judge score, stop reason, cost per query | the regression table |
| Unit economics | cost per query × volume vs value per query | the calculator |

---

<!-- card 7 -->

# Cost per query, at volume

$$
\text{cost/day} \;=\; \Big(\tfrac{T_{in}}{10^6}\,p_{in} + \tfrac{T_{out}}{10^6}\,p_{out}\Big)\times(1 + s_{loop}(m-1))\times(1 + s_{judge})\times Q
$$

$T$ tokens per query · $p$ price per million · $s_{loop}$ share of queries hitting the step budget, each costing $m\times$ · $s_{judge}$ share graded by a judge · $Q$ queries per day.

Everything on the right is measured in the notebook. The number it is compared against — value per query — is not.
