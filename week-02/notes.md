# Week 2 — Data analysis with AI as pair programmer
**Monday 28 September 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Perform the four core pandas operations (filter, derive, aggregate/resample, join) on real financial data with the assistant writing the code.
2. Recognise and fix the two silent errors that dominate AI-generated data code: calendar/alignment mistakes and unit mistakes.
3. Join market data with an external macro series and an on-chain series, and state explicitly which calendar and which units the result is in.
4. Produce a chart that answers a stated question, and save the exact data behind it with a date stamp.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW1 walkthrough** | he presents, tutor questions |
| 09:20–10:00 | **A. pandas by doing** | hands-on, notebook A |
| 10:00–10:10 | break | |
| 10:10–11:00 | **B. Join with external series** | hands-on, notebook B |
| 11:00–11:35 | **C. Charts that answer a question; rolling statistics** | hands-on, notebook C |
| 11:35–12:00 | **D. Reproducibility and privacy; homework brief** | talk |

### HW1 walkthrough (20')
He opens his notebook and README; tutor picks two lines of code at random and asks what they do. Then: was the "what the assistant got wrong" error real and the check real? If the check was "I looked at it and it seemed fine", push: what number would have been different if the code were wrong?

### A. pandas by doing (40')
Anchor to his Excel/Power Query experience with the table in the notebook (filter/formula column/pivot/VLOOKUP). Do not teach pandas syntax; teach him to *ask for* the operation by name and to read the result.

Core moment: **the weekend problem**. BTC has 7 rows a week, equities 5. Show the January 2024 slice with the NaNs. 🔍 CHECK: what does `pct_change()` silently do if you leave the NaNs? (It computes Friday→Monday returns for equities across a gap, and for BTC it computes a return against a NaN that becomes NaN — so the BTC series loses Mondays, not weekends.) Then make the choice explicit: equity calendar (`dropna`) vs crypto calendar (`ffill`). Show the BTC Monday mean return under the equity calendar: it is a 3-day move labelled as one day. Lesson: **the calendar is a modelling decision, not a cleaning step; an assistant will always make it silently.**

Resampling: weekly close via `resample("W-FRI").last()`. Ask him what `.mean()` would have meant instead and why it would be wrong for prices.

### B. Join with external series (50')
Why: internal/market data alone rarely answers a business question (this is his own professional experience — connecting internal KPIs with external context; say so). We add FRED 10y yield (macro regime) and blockchain.com active addresses (adoption proxy). Both free, no key, with fallbacks.

🔍 CHECK — **the assistant's inner join.** Let him run the cell and read the row count and date range before and after. What was lost: weekends (FRED has none), and dates where any source had a gap. What was *not* fixed: FRED's NaN on US holidays survives. And the units: yield in percent, price in dollars, addresses in counts. Then the explicit version: choose calendar, left-join, forward-fill macro, convert units, rename. Say the rule: **after every join, print `len()` before and after, `isna().sum()`, and one row from the middle. Every time.**

If he asks why `ffill` on the yield is legitimate but `ffill` on the target of a model would not be — good; park it for week 3.

### C. Charts that answer a question; rolling statistics (35')
Rolling 60-day correlation BTC–SPY with the yield below and event lines (spot ETF approval, halving). 🔍 CHECK: write the question the chart answers in one sentence. If he cannot, the chart is not finished. Expected pattern on live data: correlation positive in 2022 macro stress, lower in 2023, variable around 2024 events. If the line is noise around zero everywhere, suspect alignment.

Cross-correlation of weekly BTC returns vs address growth at lags −8…+8. 🔍 CHECK: sign convention of `shift(k)`. Positive k = past addresses vs current return. If the largest bar is at negative k, price leads activity — the opposite of the "adoption drives price" narrative. He must read the convention before concluding. This is the kind of check no assistant performs.

### D. Reproducibility and privacy; homework brief (25')
Snapshot the merged data with a date in the filename; `pip freeze` the four libraries; seeds for anything random. Privacy: no client, personal or internal data into any AI tool; public market data is fine; anonymise or aggregate if in doubt. Relate to his Kaspersky/Gazprom context: what of his past work could he have pasted into a chatbot, and what not. Then `homework.md`.

## Script

### HW1 walkthrough
**Opening:** "Open the README. Read me the error the assistant made. Now show me the check that exposed it — which number would have been different if the code were wrong?" Then two random lines of code: "What does this do?"

### A. pandas by doing
**Opening:** "Four operations cover ninety percent of what you'll do. You already know them by other names." [card 1: Excel ↔ pandas table]
**Bet 1 (a number):** show the January 2024 slice. "BTC has seven rows a week, SPY five. If you call `pct_change()` and do nothing, how many Monday returns does BTC lose in a year — zero, 52, or 104?"
**He should discover:** BTC loses Mondays (return against a NaN Sunday), while equities compute a Friday→Monday jump labelled as one day. Neither was chosen.
**Hint:** "Look at the Monday row for BTC. What is the previous row?"
**Closing:** "The calendar is a modelling decision, not a cleaning step. The assistant always makes it silently." [card 2]

### B. Join with external series
**Opening:** "Market data alone rarely answers a business question. You know this — you spent years joining internal KPIs with external context. Today the external context is the 10-year yield and on-chain activity."
**Bet 2 (a number):** before the assistant's merge cell: "Rows before: N. Rows after the merge — more, fewer, how many?"
**🔍 CHECK — ten minutes:** "The assistant's merge ran. Read the row count, the date range, and the `isna()` output. What was lost, and what was *not* fixed?"
**Hint at 5':** "What is the default `how=` of `pd.merge`? And what unit is 4.25 in?"
**He should discover:** inner join dropped weekends and every date any source lacked; FRED holiday NaNs survived; percent vs dollars vs counts correlated without a word.
**Closing:** "After every join: `len()` before and after, `isna().sum()`, one row from the middle. Every time." [card 3]

### C. Charts that answer a question
**Bet 3 (a sign and a period):** before the rolling-correlation chart: "BTC–SPY correlation in 2022 — positive or negative? And after the ETF approval?"
**Opening after the chart:** "Write the question this chart answers. One sentence. If you can't, the chart isn't finished."
**Bet 4 (a sign):** before the cross-correlation bars: "Do addresses lead price, or price lead addresses? Positive k or negative k?"
**He should discover:** the sign convention of `shift(k)` decides the story; if the biggest bar is at negative k, price leads activity — the opposite of the adoption narrative.
**Hint:** "Read the docstring of `shift`. Positive k moves the series which way?"
**Closing:** "A chart is a claim. Read the convention before you make it." [card 4]

### D. Reproducibility and privacy
**Opening:** "Which of your past projects could you have pasted into a chatbot, and which not? Be specific." [card 5]
**Closing:** "Snapshot with a date, seed, four pinned libraries. The memo you write for homework must be re-runnable by me on Sunday night."
**Take-home:** "Three lines. Commit."

## Key concepts, in one line each
- Calendar alignment: deciding which days exist before computing anything across assets.
- Inner vs left join: inner keeps only dates present everywhere; left keeps your calendar and shows gaps as NaN.
- Forward fill: carry the last known value; legitimate for slow-moving context data, dangerous for anything used as a target.
- Units: percent vs decimal, dollars vs counts; a correlation between mismatched units is still a number, which is the problem.
- Resample: change the frequency, choosing an aggregation that makes sense for the quantity (last for prices, sum for volumes, mean for rates).
- Rolling statistic: a window that moves through time; the window length is a modelling choice.
- Snapshot: the data behind any reported number, saved with a date.

## Tutor's notes
- FRED CSV endpoint and blockchain.com chart API are unauthenticated; if either is blocked from the ESE network, the notebook falls back to a snapshot in `data/` and then to synthetic data. Run once at home and commit the snapshots.
- Time pressure: block B is the core; if behind, cut the cross-correlation exercise in C, not the join check.
