---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->

# One call, four arguments

| In | What it decides | Today's default |
|---|---|---|
| `prompt` | what you ask, with the context you supply | question + retrieved passages |
| `system` | who the model is, what it may not do | "answer ONLY from the context; cite; else say 'Not in the provided context'" |
| `temperature` | how much randomness in the choice of the next token | 0 for extraction |
| `json_schema` | the shape the answer must have, validated in code | a `pydantic` class |

Out: text or a dict — and one log row: tokens in, tokens out, latency, cost.

---

<!-- card 2 -->

# RAG — four boxes, one question

```
 documents ──► CHUNK ──► EMBED ──► [vectors]
                                       │
 question ───────────► EMBED ──► RETRIEVE (cosine, top-k)
                                       │
                          ┌────────────┘
                          ▼
   prompt = CONTEXT [1][2][3] + QUESTION ──► GENERATE ──► answer + citations
```

When the answer is wrong, which box is wrong?

---

<!-- card 3 -->

# Chunking

$$
\text{chunks} \approx \frac{\text{pages} \times \text{chars per page}}{4 \text{ chars per token} \times \text{tokens per chunk}}
\qquad
60 \times 3{,}000 \;/\; (4 \times 500) \approx 90
$$

```
fixed cut at 500 chars:   ...December 31, 2025, we had $1,2 | 50 million aggregate principal...
sentence-aware + overlap: ...we had $1,250 million aggregate principal amount of convertible...
```

A fact cut in half exists in no chunk.

---

<!-- card 4 -->

# Cosine similarity

$$
\cos(\mathbf{q}, \mathbf{c}) = \frac{\mathbf{q}\cdot\mathbf{c}}{\lVert\mathbf{q}\rVert\,\lVert\mathbf{c}\rVert}
\quad\Longrightarrow\quad
\text{after normalising, } \; \text{score} = \hat{\mathbf{q}}\cdot\hat{\mathbf{c}}
$$

TF-IDF (week 1) counts shared words: "convertible debt" ≠ "what we owe bondholders".
A neural embedding maps meaning: the two questions land close together.

Your customers do not use your vocabulary.

---

<!-- card 5 -->

# Two kinds of miss

| Expected string is in… | retrieved chunks | the answer | Name | Fix |
|---|---|---|---|---|
| both | yes | yes | hit | — |
| chunks only | yes | no | **generation** miss | prompt, schema, k, model |
| neither | no | no | **retrieval** miss | chunk size, overlap, embedder, k |
| answer only | no | yes | **memory** — answered without evidence | the log; a stricter system prompt |

Name the failure before you touch a knob.

---

<!-- card 6 -->

# What it costs

$$
\text{cost per day} = N \times \frac{t_{in}\, p_{in} + t_{out}\, p_{out}}{10^{6}}
\qquad
1{,}000 \times \frac{500 \times 0.30 + 40 \times 2.50}{10^{6}} \approx \$0.25
$$

The model is cheap; latency and evaluation are the constraints.

---

<!-- card 7 -->

# EU AI Act — the tier follows the use

| Tier | Example in a fintech | Duty |
|---|---|---|
| Prohibited | social scoring of customers | do not build |
| High-risk (Annex III) | creditworthiness of a person; insurance pricing | risk management, documentation, logging, human oversight, conformity assessment |
| Transparency (Art. 50) | customer support chatbot | tell the person it is a machine; label generated content |
| Minimal | internal search over filings | voluntary codes |
| GPAI model | the model behind `llm()` | provider's duties: documentation, copyright, training summary |

The day the chatbot answers "can I have a higher limit?", it changes row.
