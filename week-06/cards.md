---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# Minor case — what the four criteria really ask

| Criterion (25 each) | The question behind it |
|---|---|
| Problem framing and user | Who uses this on a Tuesday afternoon, and what did they do before? |
| Technical build and correctness | Take the key out, cut a number in half — does it still tell the truth? |
| Evaluation method | If the model changes tomorrow, which number tells you the product got worse? |
| Limits, risk, regulation | What would a hostile user type, and which obligation applies when they do? |

A product is something you can change without breaking. Evaluation is what makes it changeable.

---

<!-- card 2 -->
# Fraud: two errors, two prices

```
                      predicted normal        predicted fraud
actual normal         fine                    BLOCKED GOOD CUSTOMER
                                              cost = contact + churn risk   (~ EUR 15–60)
actual fraud          MISSED FRAUD            caught
                      cost = the amount       (~ EUR 350 average here)
```

$$\text{cost/day} = \underbrace{100{,}000 \times 0.995 \times \text{FPR}}_{\text{good customers blocked}} \times C_{FP} \;+\; \underbrace{100{,}000 \times 0.005 \times (1-\text{recall})}_{\text{frauds missed}} \times \overline{\text{amount}}$$

Accuracy of "never flag" is 99.5%. It has a cost of about EUR 170,000 a day.

---

<!-- card 3 -->
# The threshold is a business decision, not 0.5

```
recall
 1.0 |                              ........●●●●●●●
     |                        ●●●●●'
 0.9 |                    ●●●'      ← recall gained per 100 customers blocked
     |                ●●'             falls quickly after this point
 0.8 |            ●●'
     |         ●'
 0.7 |     ●'   0.5 threshold: 33 blocked/day, 67% caught
     |   ●'
 0.6 +---+------+------+------+------+------+------+
        0     500   1000   1500   2000   2500   3000   good customers blocked per day
```

Move the cost of a blocked customer from 15 to 60 and the best point moves left. The model did not change.

---

<!-- card 4 -->
# Credit: the model is the explanation

$$\log\frac{p(\text{default})}{1-p(\text{default})} \;=\; b_0 + \sum_{j} \beta_j \, z_j \qquad z_j = \frac{x_j - \bar{x}_j}{s_j}$$

| term | applicant | contribution |
|---|---|---|
| dti | 0.47 | +0.42 |
| late_payments | 1 | +0.19 |
| employment_yrs | 2.4 | +0.18 |
| income | 31,628 | +0.10 |
| history_years | 10.9 | −0.25 |

The two largest positive terms are the reasons the applicant is told. Not more, not different.

---

<!-- card 5 -->
# Two fairness definitions that cannot both hold

```
                  region A          region B
base default       17%               28%
                    |                 |
   same threshold on p(default) < 20%
                    |                 |
approval rate      72%               30%      ← unequal
default among      12%               10%      ← roughly equal (calibrated by group)
approved
```

If base rates differ, equal approval rates and equal default rates among the approved contradict each other. The lender chooses one, writes the choice down, and defends it.

---

<!-- card 6 -->
# What the regulator expects of these two models

| Expectation | Fraud model | Credit model |
|---|---|---|
| Model risk management: an owner, documentation, validation, monitoring, a retirement plan | yes | yes |
| Explainability: a reason list the person can act on | not for the customer; for the auditor | for every rejection |
| GDPR Art. 22: no solely automated decision with legal or similar effect without safeguards and human review | blocking a payment can qualify; a review path must exist | applies directly |
| Fairness evidence: outcomes by group, with the chosen definition stated | monitored | required |

Week 7 opens model risk management fully; week 9 turns the fairness row into your canvas.

---

<!-- card 7 -->
# Build, buy, or partner — the weights are the argument

| criterion | weight (credit) | weight (fraud) | build | buy | partner |
|---|---|---|---|---|---|
| time to value | 3 | 5 | 1 | 5 | 3 |
| control over model and data | 4 | 2 | 5 | 1 | 3 |
| explainability to regulator | 5 | 2 | 5 | 2 | 4 |
| cost year 1 | 2 | 3 | 2 | 4 | 3 |
| cost year 3 cumulative | 3 | 3 | 3 | 2 | 4 |
| cross-institution signal | 3 | 5 | 1 | 5 | 3 |
| lock-in risk | 2 | 2 | 5 | 1 | 3 |

The executive summary of the memo is the one criterion that decided it.

---

<!-- card 8 -->
# Capstone candidate — the template

| field | what a passing entry looks like |
|---|---|
| question | one sentence, a named asset or protocol, a period, a decision someone would take on the answer |
| data | named sources with the endpoint you have seen; snapshot date |
| method | something taught by week 9, in the toolkit's words |
| deliverable | notebook pipeline + memo + canvas + roadmap |
| risk | the most likely way it fails, and what you deliver if it does |
| wk 7 · 8 · 9 · 10 | a file that exists at the end of each weekend |

A week that says "explore" is not a plan. A data check that prints [SYNTHETIC] is not a check.
