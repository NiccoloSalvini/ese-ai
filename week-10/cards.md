---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# Build / buy / partner — the table does not decide

| criterion | weight | build | buy | partner |
|---|---|---|---|---|
| time to a working pilot | 0.25 | 4 | 5 | 3 |
| control over data and prompts | 0.20 | 5 | 2 | 3 |
| cost at target volume | 0.20 | 4 | 2 | 3 |
| vendor / lock-in risk | 0.15 | 3 | 2 | 2 |
| auditability | 0.10 | 4 | 3 | 3 |
| skills you actually have | 0.10 | 3 | 5 | 4 |
| **weighted total** | 1.00 | **3.95** | **3.15** | **2.95** |

If the ranking flips when one weight moves by 0.10, you decided — write the real reason.

---

<!-- card 2 -->
# Cost of one query

$$
\text{cost} = \frac{\text{tokens}_{in}\cdot p_{in} + \text{tokens}_{out}\cdot p_{out}}{10^6}
$$

```
      RAG prompt                         answer
  ┌───────────────────────────┐       ┌──────────┐
  │ system + 6 chunks + query │ ───▶  │  model   │ ───▶  300 tokens
  │        8,000 tokens       │       └──────────┘
  └───────────────────────────┘
       8,000 × $5 / 1M = $0.0400        300 × $15 / 1M = $0.0045
```

Input is cheaper per token and 27× larger. An estimate that shows only one of the two numbers is not verified.

---

<!-- card 3 -->
# Sensitivity — where the number breaks

| queries / month | small | mid | frontier |
|---|---|---|---|
| 1,000 | $1 | $9 | $45 |
| 5,000 | $5 | $46 | $223 |
| 20,000 | $18 | $184 | $890 |
| 100,000 | $92 | $920 | $4,450 |
| 500,000 | $460 | $4,600 | $22,250 |

(8,000 in / 300 out, illustrative prices, no caching.) Volume moves the figure more than caching does; tier moves it more than either.

---

<!-- card 4 -->
# Break-even and routing

$$
\text{break-even value per query} = \text{cost per query}
\qquad\qquad
\text{volume at budget} = \frac{\text{budget}}{\text{cost per query}}
$$

```
  easy queries (80%) ──▶ small model    ┐
                                        ├──▶  weighted cost
  hard queries (20%) ──▶ frontier model ┘
```

The chart gives the cost of routing. Only your golden set gives its price in quality. No evals, no routing.

---

<!-- card 5 -->
# Latency budget

```
  network+auth  embed   search   first token   generate 300 tok @ 60 tok/s   guardrail
  ▏40▕ ▏120▕ ▏350▕ ▏────700────▕ ▏──────────────5,000──────────────▕ ▏30▕
  ────────────────────────────────────────────────────────────────────────▶ 6,240 ms
                                                          target: 5,000 ms
```

Generation time is tokens_out ÷ tokens per second. Shorter outputs are the one lever that cuts latency and cost at the same time.

---

<!-- card 6 -->
# Readiness — a map of where the pilot breaks first

| area | weighted / max | readiness |
|---|---|---|
| data | 15 / 20 | 75% |
| technology | 15 / 24 | 63% |
| people | 3 / 10 | 30% |
| governance | 2 / 10 | 20% |

Score 0 with weight 3 is not a low mark. It is the first gate of the roadmap.

---

<!-- card 7 -->
# A gate is a criterion that can fail

| | 0–30 days · shadow | 30–60 days · limited | 60–90 days · production |
|---|---|---|---|
| **scope** | internal users, outputs not acted on | one team, human approves every output | all users, human samples 5% |
| **gate** | eval ≥ baseline; $/query ≤ budget; no open P1 finding | acceptance ≥ 70%; p95 latency ≤ target; drift monitor live | 30 days without kill-switch; validator sign-off |
| **rollback** | stop | back to shadow | kill-switch, old process in < 1 h |

Every gate criterion points to a cell that produces the number. No cell, no gate.

---

<!-- card 8 -->
# Fifteen minutes, six beats

| beat | what they hear | ends at |
|---|---|---|
| 1 | the decision, the user, the cost of being wrong today | 1'30" |
| 2 | the pipeline, one diagram | 4'30" |
| 3 | **the number, with the baseline next to it** | 7'30" |
| 4 | cost and latency at target volume | 9'30" |
| 5 | what could go wrong; the open finding; the kill-switch | 12'00" |
| 6 | what would have to be true; the first gate; the ask | 13'30" |

Beat 3 is the sentence they will remember. Everything else supports it.
