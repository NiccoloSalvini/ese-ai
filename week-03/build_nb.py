"""Builds week-03/session.ipynb with nbformat (same style as week-04/build_nb.py).
Run:  python build_nb.py   → writes session.ipynb next to this file.

Week 3: explore a real dataset (BTC, ETH, S&P 500 since 2018), then one black-box
model (a random forest) on the question the exploration suggests.
Pattern: worked cell → ✍️ bet → ▶ YOUR TURN (he writes the next piece, on ETH or on a new question)."""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

SNAP_URL = "https://raw.githubusercontent.com/NiccoloSalvini/ese-ai/main/week-03/data/prices_BTC-USD_ETH-USD_SPY.csv"

def your_turn(task, solution):
    """A piece of the analysis he writes himself; the solution sits collapsed under it."""
    return [
        md(f"### ▶ YOUR TURN\n{task.strip()}\n\n<details><summary>solution (open only after trying)</summary>\n\n```python\n{solution.strip()}\n```\n</details>"),
        code("# your code here\n"),
    ]

cells = []
cells += [
md(f"""
# Week 3 — Look first, then predict
**ESE · AI for Business and FinTech · Wednesday 7 October 2026**

One dataset, one question, two halves.

1. **Explore** — eight years of daily Bitcoin, Ether and S&P 500 prices. What does crypto risk actually look like?
2. **Predict** — a model we do not open today (a *random forest*) on the question the exploration tells us is worth asking.

How this notebook works:
- grey cells are **worked examples**: run them, read them, ask;
- **✍️ BET** cells: write a number *before* you run the next cell;
- **▶ YOUR TURN** cells are pieces of the analysis you write — with your assistant if you like. The solution is folded underneath; open it only after trying.
"""),
code("!pip -q install yfinance scikit-learn"),
md("Run once. Live data from Yahoo Finance; if the network blocks it, a dated snapshot from the course repo (6 Oct 2026)."),
code(f'''
import warnings, numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
pd.set_option("display.precision", 4)
plt.rcParams.update({{"axes.prop_cycle": plt.cycler(color=["#2471a3", "#AF1F25", "#a8955a", "#1e8449", "#7a7f85"]),
                     "axes.spines.top": False, "axes.spines.right": False}})

SNAPSHOT = "{SNAP_URL}"

def load_prices(tickers=("BTC-USD", "ETH-USD", "SPY"), start="2018-01-01"):
    """Daily close prices. 1) yfinance live  2) course snapshot  3) synthetic (pipeline test only)."""
    try:
        import yfinance as yf
        px = yf.download(list(tickers), start=start, auto_adjust=True, progress=False)["Close"].dropna(how="all")
        if len(px) < 1000: raise RuntimeError("short download")
        print(f"[live] {{len(px)}} rows, {{px.index[0].date()}} → {{px.index[-1].date()}}")
        return px[list(tickers)]
    except Exception as e:
        print(f"[warn] live download failed ({{type(e).__name__}}); using the snapshot")
    try:
        px = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)
        print(f"[snapshot] {{len(px)}} rows, {{px.index[0].date()}} → {{px.index[-1].date()}}")
        return px[list(tickers)]
    except Exception:
        print("[SYNTHETIC] no network: random walk. Numbers below are NOT real.")
        rng = np.random.default_rng(0); idx = pd.date_range(start, pd.Timestamp.today().normalize())
        return pd.DataFrame({{t: 100*np.exp(np.cumsum(rng.normal(0.0004, 0.035 if "USD" in t else 0.011, len(idx))))
                             for t in tickers}}, index=idx)

px = load_prices()
px.tail()
'''),

# ---------------------------------------------------------------- PART 1
md("""
# Part 1 — Exploration
The question for the whole morning: **is crypto risk predictable — and which part of it?**

Exploration is not "make charts". It is asking the data small questions, in an order, until you know what question is worth a model.
"""),
md("## E1 — What is in the table?"),
code('''
print(px.shape)
print(px.isna().sum())
px.head(8)
'''),
md("""
**✍️ BET.** SPY has missing values and BTC does not. Before running the next cell: out of every 7 days, how many is SPY missing? Write it: `____`
"""),
code('''
missing = px["SPY"].isna()
print(f"SPY missing on {missing.mean():.1%} of days")
px.index[missing].day_name().value_counts()
'''),
md("""
Crypto trades 7 days a week, the stock market 5 (minus holidays). **Every join between the two is a decision**: drop the weekends (lose 2/7 of crypto) or carry Friday's SPY price forward (pretend nothing happened). Neither is wrong; not deciding is.
"""),
*your_turn(
"Which **holidays** is SPY closed on that are *not* weekends? List the weekday dates where SPY is missing, for 2025 only.",
'''
m = px["SPY"].isna() & (px.index.dayofweek < 5)
px.index[m & (px.index.year == 2025)]
'''),

md("## E2 — From prices to returns"),
md("Prices are not comparable across assets (BTC ≈ 85,000, ETH ≈ 2,700). Returns are. We use **log returns**: they add up over time, so a week is the sum of seven days."),
code('''
ret = np.log(px / px.shift(1))          # daily log return, per asset
btc = ret["BTC-USD"].dropna()
btc.describe()
'''),
md("""
**✍️ BET.** BTC's worst single day since 2018: how much did it lose? `____ %` And on which date (roughly)? `____`
"""),
code('''
worst = btc.nsmallest(5)
(np.exp(worst) - 1).map("{:.1%}".format)       # back to simple % moves, which is what people quote
'''),
*your_turn(
"Same question for **ETH**: the five worst and the five best days, as simple % moves. Are they on the same dates as BTC?",
'''
eth = ret["ETH-USD"].dropna()
print((np.exp(eth.nsmallest(5)) - 1).map("{:.1%}".format))
print((np.exp(eth.nlargest(5)) - 1).map("{:.1%}".format))
'''),

md("## E3 — How often does the 'impossible' happen?"),
md("If daily returns were *normal* (the bell curve of every textbook), a move beyond 4 standard deviations would happen about **once every 43 years** of daily data."),
md("**✍️ BET.** In ~8.5 years of BTC, how many days beyond 4 standard deviations? `____`"),
code('''
z = (btc - btc.mean()) / btc.std()
from math import erf, sqrt
p_normal = 1 - erf(4 / sqrt(2))                  # two-sided probability beyond 4σ under a normal
print(f"days beyond 4σ: {(z.abs() > 4).sum()}   |  a normal distribution would give {p_normal * len(z):.2f}")

z.hist(bins=120, figsize=(8, 3)); plt.title("BTC daily returns, in standard deviations"); plt.show()
'''),
md("""
**Fat tails.** Big days are rare, but far less rare than the bell curve says. Any risk model that assumes normality underestimates the days that matter. Remember this when someone shows you a "99% VaR".
"""),

md("## E4 — The central discovery: direction vs size"),
md("""
Two questions that sound alike:
- **direction**: if BTC went up today, is it more likely to go up tomorrow?
- **size**: if BTC moved *a lot* today (either way), is it more likely to move a lot tomorrow?

We measure both with the **autocorrelation**: the correlation between a series and itself, *k* days earlier. 0 = no memory.
"""),
md("**✍️ BET.** Which one has memory — direction, size, both, neither? `____`"),
code('''
lags = range(1, 31)
ac = pd.DataFrame({
    "direction  (return)":          [btc.autocorr(k) for k in lags],
    "size  (absolute return)":      [btc.abs().autocorr(k) for k in lags],
}, index=lags)
ax = ac.plot(kind="bar", figsize=(10, 3.5), width=0.8)
ax.axhline(0, color="k", lw=0.8); ax.set_xlabel("lag (days)"); ax.set_title("BTC: does yesterday tell you about today?")
plt.show()
ac.head(5)
'''),
md("""
**This is the sentence of the morning.** The *direction* of tomorrow has essentially no memory; the *size* of tomorrow does — for weeks. Calm follows calm, storms follow storms: **volatility clustering**.

So before training anything we already know which question a model can help with, and which one it cannot.
"""),
md("Seen as a picture: 30-day rolling volatility, annualised. Crypto trades 365 days a year, so annualise with √365."),
code('''
vol30 = ret.rolling(30).std() * np.sqrt(365)
vol30[["BTC-USD", "ETH-USD"]].plot(figsize=(10, 3.5), title="30-day volatility, annualised")
plt.show()
'''),
*your_turn(
"Does the S&P 500 cluster too? Make the same autocorrelation table for **SPY** (drop its missing days first). Is the size-memory stronger or weaker than BTC's?",
'''
spy = ret["SPY"].dropna()
pd.DataFrame({"direction": [spy.autocorr(k) for k in range(1, 11)],
              "size": [spy.abs().autocorr(k) for k in range(1, 11)]}, index=range(1, 11))
'''),

md("## E5 — Does crypto move with the stock market?"),
code('''
both = ret[["BTC-USD", "SPY"]].dropna()            # stock-market days only: a decision, see E1
rc = both["BTC-USD"].rolling(90).corr(both["SPY"])
rc.plot(figsize=(10, 3), title="BTC vs S&P 500: 90-trading-day correlation"); plt.axhline(0, color="k", lw=0.8)
plt.show()
rc.resample("YE").mean().round(2)
'''),
md("""
"Digital gold, uncorrelated with stocks" was roughly true before 2020 and has not been true since. A correlation is not a constant: it is a series, and it has regimes too.
"""),

md("""
## 🔍 CHECK — the assistant's summary table
Asked for *"annualised volatility and total return of BTC and ETH since 2018"*, an assistant wrote the cell below. It runs, and it looks professional. **There are two errors.** Ten minutes; a hint after five.
"""),
code('''
simple = px[["BTC-USD", "ETH-USD"]].pct_change().dropna()
summary = pd.DataFrame({
    "annual vol":   simple.std() * np.sqrt(252),
    "total return": simple.sum(),
})
summary.style.format("{:.1%}")
'''),
md("""
<details><summary>hint</summary>How many days a year does crypto trade? And what happens if you add +50% and −50%?</details>

<details><summary>solution</summary>

1. `np.sqrt(252)` is the stock-market convention. Crypto trades 365 days: vol is understated by √(365/252) ≈ 20%.
2. **Simple returns do not add up.** +50% then −50% sums to 0, but you have lost 25%. Total return is the product of (1 + r), minus 1 — or the sum of *log* returns, exponentiated.
</details>
"""),
code('''
summary_ok = pd.DataFrame({
    "annual vol":   simple.std() * np.sqrt(365),
    "total return": (1 + simple).prod() - 1,
})
summary_ok.style.format("{:.1%}")
'''),

md("""
### What the exploration told us
Write three lines before we go on. Direction? Size? Correlation with stocks?

-
-
-
"""),

# ---------------------------------------------------------------- PART 2
md("""
# Part 2 — Machine learning, with a black box

We now ask a model to predict **next week**. Two targets, the same inputs:
- `y_dir` — will BTC be **up** over the next 7 days?
- `y_vol` — will the next 7 days be **more volatile than usual**?

The exploration already predicts the outcome. Let's see whether the model agrees.
"""),
md("""
## M1 — Features and target: the wall
**Feature** = something known *at* day *t*. **Target** = something that happens *after* *t*. Nothing on the right of the wall may leak into the left.
"""),
code('''
H = 7                                                   # horizon: 7 calendar days
d = pd.DataFrame(index=btc.index)
d["ret"] = btc

# features — every one uses rows up to and including t, never after
X = pd.DataFrame(index=d.index)
X["ret_1"]     = d["ret"]
X["ret_7"]     = d["ret"].rolling(7).sum()
X["ret_30"]    = d["ret"].rolling(30).sum()
vol_7, vol_30 = d["ret"].rolling(7).std(), d["ret"].rolling(30).std()
usual = vol_7.rolling(365).median()                      # 'usual' weekly vol = median of the past year, known at t
X["vol_7"]     = vol_7 / usual                           # this week's vol, relative to usual (1 = normal)
X["vol_30"]    = vol_30 / usual
X["vol_ratio"] = vol_7 / vol_30
X["eth_ret_7"] = ret["ETH-USD"].rolling(7).sum().reindex(d.index)
X["spy_ret_5"] = ret["SPY"].ffill().rolling(5).sum().reindex(d.index)   # weekends: Friday's value carried
X["weekday"]   = d.index.dayofweek

# target — the next H days, t+1 … t+H
fwd_ret = d["ret"][::-1].rolling(H).sum()[::-1].shift(-1)
fwd_vol = d["ret"][::-1].rolling(H).std()[::-1].shift(-1)
y = pd.DataFrame({"y_dir": (fwd_ret > 0).astype(int),
                  "y_vol": (fwd_vol > usual).astype(int)}, index=d.index)

data = pd.concat([X, y, fwd_ret.rename("fwd_ret")], axis=1).dropna()
print(data.shape); data.tail(3)
'''),
md("**🔍 CHECK — the target, by hand.** Pick a date. `fwd_ret` must be the sum of the *next* 7 daily returns, not including today."),
code('''
t = data.index[1500]
by_hand = d["ret"].loc[t:].iloc[1:H + 1].sum()
print(t.date(), "| in the table:", round(data.loc[t, "fwd_ret"], 6), "| by hand:", round(by_hand, 6))
assert abs(by_hand - data.loc[t, "fwd_ret"]) < 1e-12, "the target leaks or is misaligned"
'''),
*your_turn(
"Fill this table in a markdown cell: for each of the 9 features, the **latest day it uses** (t, t−1, …). Then answer: is `spy_ret_5` on a Sunday honest?",
'''
# ret_1 … t | ret_7 … t | ret_30 … t | vol_7 … t | vol_30 … t | vol_ratio … t
# eth_ret_7 … t | spy_ret_5 … last trading day ≤ t (Friday on a Sunday: honest, just stale) | weekday … t
'''),

md("## M2 — Before any model: what does doing nothing score?"),
md("**✍️ BET.** Share of 7-day windows in which BTC went up: `____ %`"),
code('''
for col in ["y_dir", "y_vol"]:
    p = data[col].mean()
    print(f"{col}: share of 1s = {p:.1%}  →  'always say the majority' scores {max(p, 1 - p):.1%}")
'''),
md("""
That is the **base rate**. A model at 54% on direction has learned nothing if 54% of weeks are up weeks. An accuracy without its base rate next to it is not a number.

And for volatility we have a smarter baseline, a rule anyone can write: **"next week will be like this week"** — predict high-vol if this week's vol is above the usual.
"""),

md("""
## M3 — The black box: a random forest
Today we do not open it. What you need to know:
- it is **hundreds of decision trees**, each a flowchart of yes/no questions on the features ("is `vol_7` above 0.03?"), each grown on a slightly different sample of the data;
- they **vote**; the share of votes is the probability;
- it finds interactions and non-linear effects by itself, which a regression does not.

What it does *not* do is tell you whether it is right. That is our job: **an honest split**. Train on the past, test on the future.
"""),
code('''
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

features = list(X.columns)
train = data.loc[:"2023-12-31"]          # learn on 2019–2023
test  = data.loc["2024-01-01":]           # judge on 2024 → today: data the model has never seen
print(f"train {train.index[0].date()} → {train.index[-1].date()} ({len(train)})   test {test.index[0].date()} → {test.index[-1].date()} ({len(test)})")

def forest():
    return RandomForestClassifier(n_estimators=300, min_samples_leaf=20, random_state=0, n_jobs=-1)

rf = forest().fit(train[features], train["y_vol"])
p = rf.predict_proba(test[features])[:, 1]       # the forest's probability of a high-vol week
pd.Series(p, index=test.index).plot(figsize=(10, 3), title="P(high-vol week), out of sample"); plt.show()
'''),
md("""
Two scores:
- **accuracy** — share of weeks called right (at a 0.5 threshold);
- **AUC** — does the model rank the high-vol weeks above the calm ones? 0.5 = coin, 1.0 = perfect. It does not depend on a threshold.
"""),
md("**✍️ BET.** Fill the table before running: forest accuracy on *direction* `____`, on *volatility* `____`."),
code('''
rows = []
for target in ["y_dir", "y_vol"]:
    m = forest().fit(train[features], train[target])
    prob = m.predict_proba(test[features])[:, 1]
    base = max(test[target].mean(), 1 - test[target].mean())
    rows.append({"target": target, "base rate": base,
                 "forest accuracy": accuracy_score(test[target], prob > 0.5),
                 "forest AUC": roc_auc_score(test[target], prob)})

rows[1]["rule accuracy"] = accuracy_score(test["y_vol"], test["vol_7"] > 1)     # 'next week like this week': no model
rows[1]["rule AUC"]      = roc_auc_score(test["y_vol"], test["vol_7"])             # one feature, used as the score
pd.DataFrame(rows).set_index("target").round(3)
'''),
md("""
Read the table in this order:
1. **direction ≈ base rate.** The forest — hundreds of trees, nine features — has nothing to say about next week's direction. Exactly what E4 told us for free.
2. **volatility is somewhat predictable.** AUC clearly above 0.5: clustering, again.
3. **the rule beats the forest.** "Next week like this week" is one line and one feature, and on 2024–2026 it does as well as hundreds of trees, or better. *A rule you can write down beats a model that guesses it* — and you only know that because you built the rule first.

> Same data, same model. **The question decides whether ML has anything to offer** — and choosing the question is the manager's job.
"""),

md("""
## 🔍 CHECK — the assistant's validation
Asked to *"evaluate the model with a train/test split"*, every assistant writes `train_test_split` — which **shuffles** the days.
"""),
md("**✍️ BET.** Volatility AUC with the shuffled split: higher, lower or the same as the honest one? `____`"),
code('''
from sklearn.model_selection import train_test_split
tr, te = train_test_split(data, test_size=0.3, random_state=0)          # the assistant's default: shuffled
for target in ["y_dir", "y_vol"]:
    m = forest().fit(tr[features], tr[target])
    print(f"{target}: shuffled AUC = {roc_auc_score(te[target], m.predict_proba(te[features])[:, 1]):.3f}")
'''),
md("""
<details><summary>why</summary>

With a shuffle, Thursday is in the test set while Wednesday and Friday are in the training set. Their 7-day and 30-day windows overlap almost entirely, and so do their targets. The model is not predicting Thursday: it is **remembering its neighbours**. The gap between the two scores is leakage, not skill — and on direction it can make a coin look like a signal.
</details>
"""),

md("## M4 — What did the black box look at?"),
md("""
We can't read 300 trees, but we can ask a simpler question: **if I scramble one feature, how much worse does the model get?** That is *permutation importance*. Measured on the test period.
"""),
code('''
from sklearn.inspection import permutation_importance
rf_vol = forest().fit(train[features], train["y_vol"])
imp = permutation_importance(rf_vol, test[features], test["y_vol"], scoring="roc_auc", n_repeats=10, random_state=0)
pd.Series(imp.importances_mean, index=features).sort_values().plot.barh(figsize=(7, 3.5),
    title="how much AUC drops when the feature is scrambled"); plt.show()
'''),
md("""If the exploration was right, the volatility features dominate. `ret_7` helps too — a week with a big move *is* a volatile week, seen from another angle. Bars below zero mean the feature is noise the model would be better without.

A black box that agrees with what you saw by eye is one you can start to trust; one that leans on `weekday` is one you should not."""),

*your_turn(
"""**Leak it on purpose.** An assistant asked to "smooth" the volatility adds `d["ret"].rolling(7, center=True).std()` as a feature. Add it, retrain on the *honest* split, and compare the volatility AUC. Then write one sentence: why did the honest split not protect you?""",
'''
X_leak = data[features].copy()
X_leak["vol_7_centred"] = d["ret"].rolling(7, center=True).std().reindex(data.index)
X_leak = X_leak.dropna(); yl = data.loc[X_leak.index, "y_vol"]
m = forest().fit(X_leak.loc[:"2023-12-31"], yl.loc[:"2023-12-31"])
print("AUC with the centred feature:", round(roc_auc_score(yl.loc["2024":], m.predict_proba(X_leak.loc["2024":])[:, 1]), 3))
# a centred window at t uses t+1 … t+3: the future is inside the feature, and no split can see that
'''),

md("""
## M5 — From probability to decision *(if time; otherwise homework)*
A treasury desk holds BTC. Hedging next week costs **1**; an unhedged high-vol week costs **2**. Hedge when the forest's probability is above a threshold. Which threshold?
"""),
md("**✍️ BET.** Threshold: `____`"),
code('''
c_hedge, c_miss = 1, 2
yv = test["y_vol"].values
rows = []
for th in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    hedge = p > th
    rows.append({"threshold": th, "hedged weeks": hedge.mean(),
                 "cost per week": (c_hedge * hedge + c_miss * (~hedge & (yv == 1))).mean()})
rows += [{"threshold": "never hedge",  "hedged weeks": 0, "cost per week": c_miss * yv.mean()},
         {"threshold": "always hedge", "hedged weeks": 1, "cost per week": c_hedge}]
pd.DataFrame(rows).round(3)
'''),
md("""Find the cheapest row, and check it beats **both** trivial policies — a model has to beat "never" and "always", not just look clever.

Now set `c_miss = 4` and run again. The best threshold drops, and "always hedge" may win outright: when misses are expensive enough, the model is not worth running. **The model did not change — the business did.**"""),

md("""
## Three lines to take home
Write them here, in your words, then **File ▸ Save a copy in Drive** into `ese-ai-fintech/week-03/`.

1. On exploration:
2. On the honest split:
3. On the black box:
"""),
]

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {"colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"},
                  "language_info": {"name": "python"}}
nbf.write(nb, ROOT / "session.ipynb")
print("wrote", ROOT / "session.ipynb", len(cells), "cells")
