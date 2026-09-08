---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# You already know pandas

| Operation | Excel / Power Query | pandas |
|---|---|---|
| filter rows | AutoFilter | `df[df["col"] > 0]` |
| new column | formula column | `df["ret"] = df["px"].pct_change()` |
| aggregate | PivotTable | `df.groupby(...).agg(...)` · `df.resample("W").last()` |
| join | VLOOKUP / merge | `df.join(other)` · `pd.merge(...)` |

---

<!-- card 2 -->
# The calendar is a modelling decision

```
            Fri     Sat     Sun     Mon
BTC       42,100  41,900  43,200  44,000     7 days a week
SPY        470      NaN     NaN    473       5 days a week

equity calendar (dropna): Fri → Mon is one "day" — a 3-day move for BTC
crypto calendar (ffill):  SPY "moves" 0% on Sat and Sun — its vol is diluted
```

Neither is right. Choosing silently is wrong.

---

<!-- card 3 -->
# After every join

```
print(len(before), len(after))
print(after.isna().sum())
after.sample(3)
```

Inner join keeps only dates present everywhere. Left join keeps your calendar and shows the gaps.
Yields are in **percent**, prices in **dollars**, addresses in **counts** — a correlation between them is still a number. That is the problem.

---

<!-- card 4 -->
# A chart is a claim

Title = the question it answers.
Axis labels with units.
Event lines for what the reader already knows happened.

`shift(k)` with k > 0 moves the series **into the future** — so `corr(ret, addr.shift(k))` compares today's return with addresses **k periods ago**. Read the convention before you conclude.

---

<!-- card 5 -->
# What may enter an AI tool

| Data | Into a chatbot? |
|---|---|
| public market and on-chain data | yes |
| aggregated, anonymised internal KPIs | usually |
| client names, contracts, personal data | never |
| internal strategy documents | not without an approved deployment |

Snapshot with a date · seed · pinned versions. Re-runnable by someone else on Sunday night.
