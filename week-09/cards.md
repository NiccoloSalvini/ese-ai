---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# One prediction, taken apart

```
 base value (average prediction, log-odds)
 |
 |   vol_ratio  ████████████▶  +0.62
 |   vol_21     ██████▶        +0.31
 |   ret_5      ◀███           −0.14
 |   spy_ret_5  ◀█             −0.05
 |   dow        ▏              +0.01
 |
 └──────────────────────────────▶ this prediction
        the arrows add up exactly to the distance
```

A SHAP value is a feature's share of the distance between one prediction and the average — on the rows you chose to explain.

---

<!-- card 2 -->
# Would you sign this?

| Claim | Sign it? |
|---|---|
| "The model relies mostly on recent volatility relative to the 21-day level." | Yes — it is a statement about the model, on the reporting period. |
| "The model uses 21-day volatility." | Only with "and two other measures of the same thing; the split between them is arbitrary." |
| "Volatility clustering drives BTC risk." | No — SHAP explains the model, not the world. |
| "The base probability is −0.31." | No — that is log-odds; the probability is 0.42. |

Explain the model you trained, on the rows you report on, in the units the reader expects.

---

<!-- card 3 -->
# Three fairness definitions that cannot all hold

| Definition | Says | Column in the table | Holds here? |
|---|---|---|---|
| Demographic parity | same approval rate in every group | `approval_rate` | no (A 8%, B 50%) |
| Equal opportunity | same approval rate *among good applicants* | `opportunity` | no (10% vs 55%) |
| Calibration | a score of 0.20 means 20% default in every group | `calibration` | nearly (22% vs 16%) |

When base default rates differ between groups, a calibrated model must approve fewer people in the riskier group. Closing the approval gap means giving up calibration — and somebody pays.

---

<!-- card 4 -->
# Removing the column is not removing the proxy

```
 region ──▶ income ──▶ p(default) ──▶ decision
    │            ▲
    └── dropped ─┘   the information still arrives
```

| | Approval gap (A−B) | Calibration gap | Defaults among approved |
|---|---|---|---|
| original | −0.42 | 0.07 | 137 |
| region removed | −0.42 | 0.08 | 138 |
| threshold per group | 0.00 | 0.11 | 152 |

"We do not use protected attributes" is a description of the input, not a fairness result.

---

<!-- card 5 -->
# Three outcomes of a hostile input

| Outcome | What happened | Who finds out |
|---|---|---|
| CRASH | the pipeline raised an exception | whoever is watching the logs, after the fact |
| SILENT | it returned a number as if nothing happened | nobody, ever |
| REFUSED | it raised a deliberate validation error with a message | the caller, immediately |

The wrong-units case differed from the reference by +0.000. A pipeline that cannot tell cents from dollars is not robust; it is blind.

---

<!-- card 6 -->
# The leakage audit as code

```
 perturb price at row t+k, recompute features, look at row t

 k:      −21 ... −5 −4 −3 −2 −1  0  +1 +2 +3
 ret_1                        ■  ■
 vol_21   ■  ■  ■  ■  ■  ■  ■  ■  ■
 dow      (no price row at all)
 vol_5_smooth          ■  ■  ■  ■  ■  ■  ■   ← latest row used = +2
                                        ^^^^^^ future
```

Any k > 0 is a leak, and no split — time-ordered, walk-forward, anything — can see it. Only this table can.

---

<!-- card 7 -->
# The risk & controls canvas

| | | |
|---|---|---|
| **1. Decision & users** who decides what, how often, with what at stake | **2. Data & rights** what enters, under which terms; the data-to-tool table | **3. Model validity** baseline, walk-forward, leakage audit, where it fails |
| **4. Explainability** SHAP on the reporting period; the sentence you would sign | **5. Fairness & harm** proxy groups; the definition chosen; who pays | **6. Security & robustness** red-team log: refused / silent / crash; injection tests |
| **7. Dependence & cost** price ×3, deprecation, outage; second provider | **8. Oversight & kill-switch** who overrides, what is logged, how it stops | **9. Regulation & disclosure** AI Act tier, model risk, MiCA; what users are told |

Every box contains a noun — a feature, a number, a person, a file. A category in a box is a wish, not a control.

---

<!-- card 8 -->
# Oversight is three questions, not a phrase

```
            ┌──────────────┐
  input ───▶│ kill_switch? │──on──▶ BLOCKED, logged
            └──────┬───────┘
                  off
            ┌──────▼───────┐
            │  validate    │──fail─▶ REFUSED, logged (reason)
            └──────┬───────┘
            ┌──────▼───────┐
            │  model       │
            └──────┬───────┘
            ┌──────▼───────┐   override by a named role ─▶ OVERRIDDEN, logged (who, what)
            │  cap / log   │   override by anyone else ─▶ DENIED, logged
            └──────┬───────┘
                   ▼ output, logged (ts, input hash, model version)
```

Who can turn the switch on at 3 a.m., and how do they know they should? Neither is a coding question.
