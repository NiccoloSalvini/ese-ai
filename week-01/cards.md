---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# The course in one table

| # | Date | We build |
|---|---|---|
| 1–3 | 21 Sep – 5 Oct | Data pipeline and an honest model |
| 4–5 | 12 – 19 Oct | An LLM application with retrieval, tools and evals |
| — | 26 Oct | Reading week — **minor case brief (40%)** |
| 6–8 | 2 – 16 Nov | Fintech cases, a backtest, a DeFi analysis |
| 9–10 | 23 – 30 Nov | Red-team and finish the capstone — **portfolio (60%)** |
| Rev. | 7 Dec | Final presentation |

Every line you submit, you can explain.

---

<!-- card 2 -->
# What a model reads

| Text | Words | Tokens |
|---|---|---|
| "The ECB left rates unchanged at 2.00% on Thursday." | 9 | ~13 |
| Same sentence in Russian | 8 | ~30 |
| `df.groupby('ticker')['ret'].rolling(21).std()` | 1 | ~17 |

| Model tier | $ per 1M input tokens | One 10-K (~90k tokens) | 1,000 reads/day |
|---|---|---|---|
| small | 0.10 | $0.009 | $9 |
| mid | 1.00 | $0.09 | $90 |
| frontier | 5.00 | $0.45 | $450 |

The unit on the invoice is the chunk, not the word.

---

<!-- card 3 -->
# Hallucination

## is pattern completion over missing information —
## not lying.

Whatever is outside the context window does not exist for the model.
It fills the gap with what usually goes there.

---

<!-- card 4 -->
# Meaning as geometry

```
            monetary tightening ●
                                  ● ECB raises rates
                                             
                                             
                                             
     ● football match ended in a draw
```

Close = similar meaning. A crude embedding only sees shared words;
a neural embedding sees that "raises rates" and "tightening" are the same thing.

---

<!-- card 5 -->
# The loop that is every agent

```
      ┌────────────────────────────────────┐
      │                                    ▼
   MODEL ── "call get_price('BTC')" ──▶ YOUR CODE runs the tool
      ▲                                    │
      └──────── result goes back ──────────┘
                    … until "done"
```

Cost, infinite loops, wrong tool, injected instructions: all four live in this loop.

---

<!-- card 6 -->
# The assistant is fluent, not correct.

## Compute the same number a second way.

Cumulative return: `(1 + r).prod() - 1`  **and**  `p_last / p_first - 1`
Volatility: √365 for what trades every day, √252 for what does not.

---

<!-- card 7 -->
# Three prompts, same question

| | What it does |
|---|---|
| Role and context | cuts generic filler |
| Explicit conventions ("365 days for crypto") | kills silent assumptions |
| Fixed output shape ("a two-row table") | makes the answer checkable |
| "If unsure, say so" | reduces — does not remove — invention |
