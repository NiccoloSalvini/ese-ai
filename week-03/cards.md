---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# The wall

```
   known at time t                  │   happens after t
   ─────────────────────────────────┼─────────────────────────
   ret_1, ret_5, ret_21             │   fwd_ret  (t+1 … t+5)
   vol_5, vol_21, vol_ratio         │   y_dir    = fwd_ret > 0
   spy_ret_5, day of week           │   y_vol    = fwd_vol > trailing median
```

Every feature: write the latest row it uses. Every target: recompute one date by hand.

---

<!-- card 2 -->
# Base rate first

| Target | Share of 1s | "Do nothing clever" accuracy |
|---|---|---|
| 5-day direction, BTC | ~0.55 | ~0.55 (always up) |
| high-vol regime | ~0.50 | ~0.50 |

A model at 0.56 accuracy has learned almost nothing. An accuracy without its base rate next to it is not a report.

---

<!-- card 3 -->
# Two ways to split

```
shuffled:      train  test  train  train  test  train  test  train …   ← Thursday tested, Wed & Fri trained
time-ordered:  train train train train train │ test test test          ← test always in the future
walk-forward:  [train ───][test] → [train ──────][test] → [train ─────────][test]
```

The gap between the two scores is leakage, not skill.

---

<!-- card 4 -->
# Same data, same models — different question

| | shuffled | time-ordered | base rate |
|---|---|---|---|
| direction | higher | ≈ base rate | 0.55 |
| volatility regime | higher | **above 0.5 AUC** | 0.50 |

Direction is a coin flip with these features. Volatility clusters.
Choosing the question is the manager's job.

---

<!-- card 5 -->
# Leakage through a feature

`rolling(5, center=True)` uses two future rows.
The time-ordered split does not protect you. No validation scheme does.

The only defence: for each feature, the latest row it uses — on paper.

---

<!-- card 6 -->
# From probability to decision

$$\text{cost}(\theta) = c_{hedge}\cdot\#\{p>\theta\} \;+\; c_{miss}\cdot\#\{p\le\theta,\ y=1\}$$

Threshold from costs, never from 0.5. Beat both "never hedge" and "always hedge".

KPI candidates: cost per week vs always-hedge · recall at θ · calibration (when it says 70%, does it happen 70%?).
Accuracy is not on the list: it does not price errors.
