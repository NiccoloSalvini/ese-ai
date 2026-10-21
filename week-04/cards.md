---
marp: true
theme: default
paginate: false
title: "Week 4 — cards"
format:
  revealjs:
    theme: [default, ../slides.scss]
    slide-level: 0
    slide-number: false
    controls: true
    hash: true
    logo: ../images/ese-logo.svg
    footer: "AI for Business & FinTech · ESE Florence · Week 4"
    include-in-header: ../_fonts.html
---

<!-- card 1 -->

# The test comes first

| line | Morgan Stanley, 2023 | yours |
|---|---|---|
| who asks | financial advisors | |
| which questions | the ones they ask every day | |
| who knows the right answer | the advisors, from the research itself | |
| which number comes out | share of answers graded accurate | |
| what ships it | a threshold agreed before the build | |

The expected answer never comes from the system under test.

---

<!-- card 2 -->

# Four boxes, one question

```
 documents ──► CHUNK ──► EMBED ──► [vectors]
                                       │
 question ───────────► EMBED ──► RETRIEVE (the nearest few)
                                       │
                          ┌────────────┘
                          ▼
   CONTEXT [1][2][3] + QUESTION ──► GENERATE ──► answer + citations
```

When the answer is wrong, which box is wrong? The tool will not tell you. The table will.

---

<!-- card 3 -->

# Two kinds of miss

| the right passage… | the answer… | name | what you change |
|---|---|---|---|
| came back | is right | **hit** | nothing |
| came back | is wrong | **generation** miss | instruction, question, model |
| never came back | is wrong | **retrieval** miss | documents, how they are cut, the words |
| never came back | is right | **memory** | it answered without evidence |

Name the failure before you touch anything.

---

<!-- card 4 -->

# Three traps

| | the question | what it tests |
|---|---|---|
| T1 | the maximum number of bitcoins | an answer the model *knows* and the documents do not contain |
| T2 | Coinbase net income, 2024 → 2025 | a number that lives in a table |
| T3 | what Coinbase owes and must pay back | a question in none of the document's words |

True, and still wrong: 21 million is correct, and it is not in the whitepaper.

---

<!-- card 5 -->

# A system instruction that holds

```
Answer only from the attached documents.
If the answer is not in them, reply exactly: "Not in the documents."
Quote the sentence you used, and name the document.
```

The third line makes the first two checkable. A quote you can Ctrl-F is evidence; a paragraph is not.

---

<!-- card 6 -->

# The schema guarantees the type, not the truth

```json
{ "company": "Coinbase", "metric": "Assets on Platform",
  "value": 376, "unit": "USD billion", "period": "31 Dec 2025",
  "source_quote": "Assets on Platform (in billions) $ 376 $ 404" }
```

Valid. Right. Now ask for a metric the filing does not contain — and watch the same shape come back.

---

<!-- card 7 -->

# Klarna, in two numbers

| | February 2024 | May 2025 |
|---|---|---|
| conversations in a month | 2.3 million, two thirds of chats | |
| "the work of" | 700 full-time agents | 853 (Q3 2025) |
| resolution time | 11 min → under 2 | |
| profit improvement, est. | $40 million | |
| quality | "on par" — no number | "lower quality" — the CEO |

Every number in the first column measures cost or speed. None measures whether the answers were right.

---

<!-- card 8 -->

# EU AI Act — the tier follows the use

| tier | in a fintech | the duty |
|---|---|---|
| prohibited | social scoring of customers | do not build |
| high-risk (Annex III) | creditworthiness of a person; insurance pricing | risk management, documentation, logging, human oversight, conformity assessment |
| transparency (Art. 50) | the customer assistant | say it is a machine; label what it generates |
| minimal | internal search over filings | voluntary codes |
| GPAI model | the model behind the panel | the **provider's** duties, not yours |

The day the assistant answers "can I have a higher limit?", it changes row.
