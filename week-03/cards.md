---
marp: true
theme: default
paginate: false
title: "Week 3 — cards"
format:
  revealjs:
    theme: [default, ../slides.scss]
    slide-level: 0
    slide-number: false
    controls: true
    hash: true
    logo: ../images/ese-logo.svg
    footer: "AI for Business & FinTech · ESE Florence · Week 3"
    include-in-header: ../_fonts.html
---

<!-- card 1 -->
# Explore in an order

| small question | what it decides |
|---|---|
| what is in the table? | how to join crypto (7 days) and stocks (5) |
| how big are the moves? | units, scale, which returns |
| how often is "impossible"? | whether the bell curve is allowed |
| does yesterday tell us about today? | **what is worth predicting** |

---

<!-- card 2 -->
# Direction has no memory. Size does.

| lag | BTC return | BTC absolute return |
|---|---|---|
| 1 day | −0.05 | **0.17** |
| 2 days | 0.04 | **0.13** |
| 5 days | 0.02 | **0.14** |

Calm follows calm, storms follow storms: volatility clustering.
Found before training anything.

---

<!-- card 3 -->
# The wall

```
   known at day t                    │   happens after t
   ──────────────────────────────────┼──────────────────────────
   ret_1, ret_7, ret_30              │   fwd_ret  (t+1 … t+7)
   vol_7, vol_30  (÷ usual)          │   y_dir = fwd_ret > 0
   eth_ret_7, spy_ret_5, weekday     │   y_vol = fwd_vol > usual
```

Every feature: write the latest day it uses. Every target: recompute one date by hand.

---

<!-- card 4 -->
# What came out (2024 → today)

| | base rate | AUC shuffled | AUC honest | rule "like this week" |
|---|---|---|---|---|
| direction | 53% | 0.70 | **0.55** | — |
| volatility | 54% | 0.74 | **0.60** | **0.64** |

The gap between shuffled and honest is leakage, not skill.
The one-line rule beats the forest. Same data, same model: the question decides.

---

<!-- card 5 -->
# Leakage through a feature

`rolling(7, center=True)` uses three future days.
Honest split, AUC 0.60 → 0.69. No validation scheme catches it.

The only defence: for each feature, the latest day it uses — on paper.

---

<!-- card 6 -->
# From probability to decision

$$\text{cost}(\theta) = c_{hedge}\cdot\#\{p>\theta\} \;+\; c_{miss}\cdot\#\{p\le\theta,\ y=1\}$$

Threshold from costs, never from 0.5. Beat both "never hedge" and "always hedge".

KPI candidates: cost per week vs always-hedge · recall at θ · calibration (when it says 70%, does it happen 70%?).
Accuracy is not on the list: it does not price errors.

---

<!-- card 7 -->
# Three black boxes, one discipline

| | what it is | cost per answer |
|---|---|---|
| rule | "next week like this week" | 0 |
| forest | 300 trees voting on 9 features | ≈ 0 |
| LLM | a prompt, a system message, a temperature | tokens × price |

Same base rate, same honest dates, same AUC. For an LLM, every date before its cut-off may already be in its memory: hide the name and the date.
