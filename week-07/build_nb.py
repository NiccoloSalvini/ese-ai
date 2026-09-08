"""Builds week-07/session.ipynb with nbformat. Run: python build_nb.py"""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

UTILS = r'''
# --- course helper: price loader with fallbacks (run this cell once per session) ---
import warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")

def load_prices(tickers, start="2022-01-01", end=None, cache_dir="data"):
    """Daily close prices, one column per ticker.
    1) try yfinance (live)  2) try a CSV snapshot in data/  3) synthetic random walk (pipeline test only)."""
    import os
    os.makedirs(cache_dir, exist_ok=True)
    key = "_".join(t.replace("^", "") for t in tickers)
    snap = os.path.join(cache_dir, f"prices_{key}.csv")
    try:
        import yfinance as yf
        raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
        px = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].rename(columns={"Close": tickers[0]})
        px = px.dropna(how="all")
        if len(px) < 50:
            raise RuntimeError("empty download")
        px.to_csv(snap)
        print(f"[live] {px.shape[0]} rows from yfinance; snapshot saved to {snap}")
        return px
    except Exception as e:
        print(f"[warn] yfinance failed ({type(e).__name__}); trying snapshot")
    if os.path.exists(snap):
        px = pd.read_csv(snap, index_col=0, parse_dates=True)
        print(f"[snapshot] {px.shape[0]} rows from {snap}")
        return px
    print("[SYNTHETIC] no network and no snapshot: generating a random walk. Numbers below are NOT real.")
    rng = np.random.default_rng(0)
    idx = pd.bdate_range(start, end or pd.Timestamp.today().normalize())
    px = pd.DataFrame({t: 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.02 if "USD" in t else 0.011, len(idx))))
                       for t in tickers}, index=idx)
    return px
'''

cells = [
md("""
# Week 7 — AI in markets: backtesting done honestly
**ESE · AI for Business and FinTech · 9 November 2026**

One trading rule, one honest backtest, and every way the assistant will quietly make it look better than it is. Then a text signal scored by an LLM, tested with the same discipline. Then twenty minutes on what a bank calls *model risk* and why it applies to you.

Everything here is an educational simulation. Nothing in this notebook is investment advice and nothing is meant to be traded.
"""),
code("!pip -q install yfinance google-genai"),
code(UTILS),
code("""
px = load_prices(["BTC-USD", "SPY"], start="2018-01-01")
btc = px["BTC-USD"].dropna()          # 7-day calendar
spy = px["SPY"].dropna()              # 5-day calendar
DPY = {"BTC-USD": 365, "SPY": 252}    # day-count for annualisation (week 1)
print(btc.index.min().date(), "→", btc.index.max().date(), "| BTC rows:", len(btc), "| SPY rows:", len(spy))
"""),

# ------------------------------------------------------------------ A
md("## Block A — HW6 walkthrough and capstone sign-off (no code)"),
md("""
Twenty minutes, his screen. Two lines of code picked at random from `hw6.ipynb`; then the capstone proposal: **one question, one dataset, one number that would change a decision**. Sign-off or one concrete revision, written at the bottom of his proposal before we move on.
"""),

# ------------------------------------------------------------------ B
md("## Block B — Lab: a vectorised backtest in six steps"),
md("""
A backtest is a pipeline: **signal → position → returns → equity curve → statistics**. Every step is one line of pandas. The single most important line is the `shift(1)`: a signal computed at the close of day *t* can only earn the return of day *t+1*.

Statistics we report (risk-free rate taken as zero for simplicity):

| statistic | meaning | formula |
|---|---|---|
| annualised return | growth per year | `(1+net).prod() ** (dpy/n) - 1` |
| Sharpe ratio | return per unit of risk | `mean(net)/std(net) * sqrt(dpy)` |
| max drawdown | worst peak-to-trough loss | `min(equity/cummax(equity) - 1)` |
| turnover per year | units bought + sold per year | `sum(|Δposition|) / years` |
"""),
code("""
def momentum_signal(price, L=20):
    \"\"\"+1 if the last L days were up, -1 if down (long/short).\"\"\"
    return np.sign(price / price.shift(L) - 1)

def meanrev_signal(price, L=5):
    \"\"\"the opposite bet: fade the last L days.\"\"\"
    return -np.sign(price / price.shift(L) - 1)

def backtest(price, signal, cost_bps=0.0):
    \"\"\"Daily close-to-close backtest. cost_bps = cost per unit traded (a full flip +1 -> -1 trades 2 units).\"\"\"
    r = price.pct_change()
    pos = signal.shift(1)                       # decided at close t, earns the return of t+1
    traded = pos.diff().abs()                   # units traded at each close
    net = pos * r - traded * cost_bps / 1e4
    return pd.DataFrame({"ret": r, "pos": pos, "traded": traded, "gross": pos * r, "net": net}).dropna()

def stats(bt, dpy):
    net = bt["net"]; eq = (1 + net).cumprod()
    return pd.Series({
        "ann_return":        (1 + net).prod() ** (dpy / len(net)) - 1,
        "ann_vol":           net.std() * np.sqrt(dpy),
        "sharpe":            net.mean() / net.std() * np.sqrt(dpy),
        "max_drawdown":      (eq / eq.cummax() - 1).min(),
        "turnover_per_year": bt["traded"].sum() / (len(net) / dpy),
        "time_in_market":    (bt["pos"] != 0).mean(),
    })

# buy-and-hold for reference
def buy_and_hold(price):
    return backtest(price, pd.Series(1.0, index=price.index), 0.0)
"""),
md("""
**🔍 CHECK (bet 1).** Before running: write down your guess for the Sharpe ratio of the 20-day momentum rule on BTC since 2018, *before costs*. For scale: buy-and-hold BTC over the same period is printed next to it.
"""),
code("""
L = 20
bt0 = backtest(btc, momentum_signal(btc, L), cost_bps=0)
pd.DataFrame({"momentum L=20, no costs": stats(bt0, DPY["BTC-USD"]),
              "buy & hold": stats(buy_and_hold(btc), DPY["BTC-USD"])}).round(3)
"""),
md("""
**🔍 CHECK (bet 2).** Now the same rule paying **10 basis points per unit traded** (0.10% — a realistic all-in cost for a liquid pair on a good exchange; spread plus fees plus slippage). Write down the Sharpe you expect *after* costs. Then run the sweep.
"""),
code("""
rows = {}
for c in [0, 5, 10, 25, 50]:
    rows[f"{c} bps"] = stats(backtest(btc, momentum_signal(btc, L), cost_bps=c), DPY["BTC-USD"])
cost_table = pd.DataFrame(rows).round(3)
cost_table
"""),
code("""
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 4))
for c, ls in [(0, "-"), (10, "--"), (50, ":")]:
    bt = backtest(btc, momentum_signal(btc, L), cost_bps=c)
    (1 + bt["net"]).cumprod().plot(ax=ax, ls=ls, label=f"momentum {c} bps")
(1 + buy_and_hold(btc)["net"]).cumprod().plot(ax=ax, color="grey", lw=0.8, label="buy & hold")
ax.set_yscale("log"); ax.set_title("BTC, 20-day momentum: equity curve (log scale) at three cost levels"); ax.legend(); plt.show()
"""),
md("""
Why costs bite: turnover. A rule that flips often pays every time. Look at `turnover_per_year` in the table above and compute by hand: turnover × cost per unit = annual drag. Compare with `ann_return`.

**Your turn (replicate on different data):** run the *mean-reversion* rule (`meanrev_signal`, L=5) on **SPY** at 0 and 10 bps, with `DPY["SPY"]`. Then answer: which of the two rules is more sensitive to costs, and why does the turnover column already tell you?
"""),
code("""
# your replication: SPY, mean reversion, L=5, 0 and 10 bps
pd.DataFrame({f"{c} bps": stats(backtest(spy, meanrev_signal(spy, 5), cost_bps=c), DPY["SPY"]) for c in [0, 10]}).round(3)
"""),

# ------------------------------------------------------------------ C
md("## Block C — The ways it goes wrong"),
md("""
### C1. 🔍 CHECK — the assistant's backtest
Asked to *"backtest a 20-day momentum strategy on BTC with 10 bps transaction costs and report the Sharpe ratio"*, the assistant produced the cell below. It runs. Its Sharpe is different from the one you computed in Block B with the same rule and the same costs. **There are two mistakes.** Find them (10 minutes, on your own), then open the solution.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
L, COST_BPS = 20, 10
r = btc.pct_change()
sig = np.sign(btc / btc.shift(L) - 1)
pos = sig
net = (pos * r - COST_BPS / 1e4 * pos.abs()).dropna()
print("Sharpe after costs:", round(net.mean() / net.std() * np.sqrt(365), 2))
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **Look-ahead, off by one.** `pos = sig` holds today's position using a signal that needs today's close. The signal `sign(P_t / P_{t-L} − 1)` contains `P_t`; the return it is multiplied by, `P_t / P_{t-1} − 1`, also contains `P_t`. On a day when the price jumps, the signal "knows" it and the rule is credited with the jump. Fix: `pos = sig.shift(1)`. This is the single most common bug in assistant-written backtests and it *always* flatters the result.
2. **Costs charged on holding, not on trading.** `COST_BPS/1e4 * pos.abs()` deducts 10 bps *every day you have a position* — 365 × 10 bps ≈ 37% a year of imaginary fees — instead of 10 bps per unit *traded*. Fix: `traded = pos.diff().abs()` and charge `traded * COST_BPS/1e4`.

The two errors push in opposite directions, so the buggy Sharpe can look "reasonable". Two bugs that partly cancel are worse than one: nobody looks.
</details>
"""),
code("""
# Corrected — and the 2x2 that separates the two effects
def sharpe(x, dpy=365): return x.mean() / x.std() * np.sqrt(dpy)
r = btc.pct_change(); sig = momentum_signal(btc, 20)
grid = {}
for lag, lag_name in [(0, "same close (look-ahead)"), (1, "next day (correct)")]:
    pos = sig.shift(lag); traded = pos.diff().abs()
    grid[(lag_name, "cost on holding")] = sharpe((pos * r - 10 / 1e4 * pos.abs()).dropna())
    grid[(lag_name, "cost per trade")]  = sharpe((pos * r - 10 / 1e4 * traded).dropna())
pd.Series(grid).unstack().round(2)
"""),
md("""
Read the row *next day, cost per trade* — that is the honest number and it matches Block B. Read the column difference: the look-ahead alone is worth how many points of Sharpe? Write it down; that is the size of the lie in a backtest that forgets one `shift`.
"""),
md("""
### C2. Survivorship — today's list is not 2018's list
If you backtest on "the top coins" or "S&P 500 members" *as they are today*, you have removed every asset that died. The universe below is **synthetic by construction** (seeded, labelled) because the mechanism matters, not the names: twelve tokens in 2018, four of which collapse and are delisted. Compare an equal-weight portfolio of *today's survivors* with the *point-in-time* universe that includes the dead ones until they die.
"""),
code("""
rng = np.random.default_rng(7)
idx = pd.date_range("2018-01-01", "2024-12-31")
n = 12
names = [f"TOKEN{i:02d}" for i in range(n)]
drift = rng.normal(0.0006, 0.0005, n); vol = rng.uniform(0.03, 0.06, n)
rets = pd.DataFrame(rng.normal(drift, vol, (len(idx), n)), index=idx, columns=names)

# four tokens die: a 95% collapse over 5 days, then delisted (NaN forever)
dead = names[:4]
death_dates = pd.to_datetime(["2019-03-15", "2020-09-02", "2022-05-10", "2022-11-09"])
for t, d in zip(dead, death_dates):
    loc = idx.get_loc(d)
    rets.iloc[loc:loc + 5, rets.columns.get_loc(t)] = (0.05) ** (1 / 5) - 1     # 5 days of -45%
    rets.iloc[loc + 5:, rets.columns.get_loc(t)] = np.nan
survivors = [t for t in names if t not in dead]

port_survivors = rets[survivors].mean(axis=1)               # the universe as it looks TODAY, applied to 2018
port_pit       = rets.mean(axis=1)                          # point-in-time: everyone who existed on that day
def ann(x): return pd.Series({"ann_return": (1 + x).prod() ** (365 / len(x)) - 1, "sharpe": sharpe(x, 365),
                              "max_drawdown": ((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min()})
pd.DataFrame({"survivors-only (biased)": ann(port_survivors), "point-in-time (honest)": ann(port_pit)}).round(3)
""" ),
md("""
**🔍 CHECK.** The gap between the two columns is not a property of the tokens; it is a property of *when the list was written*. Real cases: LUNA (May 2022, −99.9% in a week) and FTT (November 2022) were both top-20 assets that no longer appear in a "top coins today" list. For equities the same happens through delistings and index changes. The only defence is a universe defined **as of each date**, or an explicit statement that you could not get one.
"""),
md("""
### C3. Multiple testing — try 200 rules, keep the best, and it fails
The assistant offers to "optimise the parameters". Here are 200 moving-average crossover rules (10 fast windows × 20 slow windows) on BTC with 10 bps costs, fitted on **2018–2021**, then checked on **2022 onwards**.

**🔍 CHECK (bet 3).** Before running: how many of the 200 pairs will have Sharpe > 1 **in-sample**? How many **out-of-sample**? And the best in-sample pair — positive or negative Sharpe out-of-sample?
"""),
code("""
def sma_signal(price, fast, slow):
    return np.sign(price.rolling(fast).mean() - price.rolling(slow).mean())

fasts = list(range(5, 55, 5))          # 10 values
slows = list(range(60, 460, 20))       # 20 values
rows = []
for f in fasts:
    for s in slows:
        bt = backtest(btc, sma_signal(btc, f, s), cost_bps=10)
        rows.append({"fast": f, "slow": s,
                     "sharpe_IS":  sharpe(bt.loc[:"2021-12-31", "net"]),
                     "sharpe_OOS": sharpe(bt.loc["2022-01-01":, "net"])})
grid = pd.DataFrame(rows)
best = grid.sort_values("sharpe_IS", ascending=False).iloc[0]
print(f"{len(grid)} rules | Sharpe>1 in-sample: {(grid.sharpe_IS > 1).sum()} | Sharpe>1 out-of-sample: {(grid.sharpe_OOS > 1).sum()}")
print(f"best in-sample: fast={int(best.fast)}, slow={int(best.slow)}, Sharpe IS={best.sharpe_IS:.2f} -> OOS={best.sharpe_OOS:.2f}")
print(f"correlation between IS and OOS Sharpe across the 200 rules: {grid.sharpe_IS.corr(grid.sharpe_OOS):.2f}")
"""),
code("""
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(grid.sharpe_IS, grid.sharpe_OOS, s=12)
ax.scatter(best.sharpe_IS, best.sharpe_OOS, color="red", s=60, label="best in-sample")
ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
ax.set_xlabel("Sharpe 2018–2021 (in-sample)"); ax.set_ylabel("Sharpe 2022– (out-of-sample)")
ax.set_title("200 SMA-crossover rules, BTC, 10 bps"); ax.legend(); plt.show()
"""),
md("""
How good can the *best of 200* look if none of them works? Replace the rules by 200 **random** position series (coin-flips with some persistence, so turnover stays realistic) and record the best in-sample Sharpe. This is the Harvey–Liu–Zhu argument as a simulation: the maximum of many noisy estimates is large even when every true value is zero.
"""),
code("""
rng = np.random.default_rng(0)
r_is = btc.pct_change().loc[:"2021-12-31"].dropna()
noise_sharpes = []
for k in range(200):
    flips = rng.random(len(r_is)) < 0.05                        # change side ~every 20 days
    pos = pd.Series(np.where(np.cumsum(flips) % 2 == 0, 1.0, -1.0), index=r_is.index)
    noise_sharpes.append(sharpe(pos * r_is))
noise_sharpes = pd.Series(noise_sharpes)
years = len(r_is) / 365
print(f"200 random rules on the same data: mean Sharpe {noise_sharpes.mean():.2f}, best {noise_sharpes.max():.2f}, share > 1: {(noise_sharpes > 1).mean():.2f}")
print(f"theory: std of a noise Sharpe over {years:.1f} years ≈ 1/sqrt(years) = {1/np.sqrt(years):.2f}; expected max of 200 ≈ {np.sqrt(2*np.log(200))/np.sqrt(years):.2f}")
"""),
md("""
### C4. Regime change — the same rule, year by year
A backtest over 2018–2026 is one number that averages several different markets. Split it.
"""),
code("""
def by_period(bt, dpy):
    out = bt["net"].groupby(bt.index.year).apply(lambda x: sharpe(x, dpy)).rename("sharpe by year").round(2)
    sub = {"2022": sharpe(bt.loc["2022", "net"], dpy), "2023–2024": sharpe(bt.loc["2023":"2024", "net"], dpy)}
    return out, pd.Series(sub).round(2)
yr, sub = by_period(backtest(btc, momentum_signal(btc, 20), 10), 365)
print(yr.to_string()); print(); print(sub.to_string())
"""),
md("""
**🔍 CHECK.** Is the full-sample Sharpe made by one or two years? What did 2022 look like for a trend rule versus 2023–24? A rule whose whole edge sits in a single regime is a bet on that regime returning — say so in the memo, do not let the average hide it.
"""),

# ------------------------------------------------------------------ D
md("## Block D — An LLM-derived signal, tested honestly"),
md("""
"News sentiment" is the most pitched AI signal in finance. We build one and test it with exactly the discipline of Blocks B–C.

**Data.** Real headline archives with reliable timestamps cost money. We generate a **synthetic, seeded headline set** with the property that matters: each headline is published on day *t* and describes the move of day *t−1* — the way news actually works. Two date columns: `event_date` (what it is about) and `published` (when you could have read it). Keep both; the difference is where leakage hides.
"""),
code("""
rng = np.random.default_rng(42)
r_btc = btc.pct_change().dropna()
POS = ["Bitcoin rallies {p:.1f}% as institutional inflows accelerate", "BTC surges {p:.1f}%; analysts see momentum building",
       "Crypto market jumps {p:.1f}% on ETF optimism", "Bitcoin climbs {p:.1f}% to fresh highs amid strong demand"]
NEG = ["Bitcoin slumps {p:.1f}% as risk appetite fades", "BTC tumbles {p:.1f}% after exchange outflows spike",
       "Crypto sell-off deepens: Bitcoin down {p:.1f}%", "Bitcoin drops {p:.1f}% amid regulatory concerns"]
NEU = ["Bitcoin little changed as traders await Fed decision", "BTC trades sideways; volumes thin",
       "Miners' revenue steady as hashrate hits record", "Stablecoin supply flat this week, data show"]
rows = []
for t, r in r_btc.items():
    if rng.random() < 0.25: pool = NEU                       # 25% noise: the headline ignores the move
    elif r > 0.02: pool = POS
    elif r < -0.02: pool = NEG
    else: pool = NEU
    rows.append({"event_date": t, "published": t + pd.Timedelta(days=1),
                 "headline": rng.choice(pool).format(p=abs(r) * 100)})
news = pd.DataFrame(rows)
print("[SYNTHETIC] headlines generated from realised returns with noise — NOT real news")
news.tail(3)
"""),
md("""
**Scoring.** Two scorers behind one interface. With `GEMINI_API_KEY` in Colab Secrets, an LLM scores a batch of headlines in one call with a JSON schema. Without a key, a **keyword lexicon** (clearly labelled MOCK) does the same job. Every LLM call goes through `llm()` so the provider can be swapped.
"""),
code("""
import os, json
API_KEY = None
try:
    from google.colab import userdata; API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    API_KEY = os.environ.get("GEMINI_API_KEY")

def llm(prompt, system=None, json_schema=None, temperature=0):
    \"\"\"One wrapper for every LLM call. Returns text (or parsed JSON when a schema is given); None when no key.\"\"\"
    if not API_KEY:
        return None
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=API_KEY)
    cfg = dict(temperature=temperature, system_instruction=system)
    if json_schema:
        cfg.update(response_mime_type="application/json", response_schema=json_schema)
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=types.GenerateContentConfig(**cfg))
    return json.loads(resp.text) if json_schema else resp.text

LEX_POS = {"rallies", "surges", "jumps", "climbs", "highs", "inflows", "optimism", "strong", "momentum", "demand"}
LEX_NEG = {"slumps", "tumbles", "sell-off", "down", "drops", "fades", "outflows", "concerns", "regulatory", "deepens"}
def score_lexicon(headlines):
    out = []
    for h in headlines:
        w = set(h.lower().replace(":", "").replace(";", "").split())
        p, n = len(w & LEX_POS), len(w & LEX_NEG)
        out.append(0.0 if p + n == 0 else (p - n) / (p + n))
    return out

SCHEMA = {"type": "array", "items": {"type": "object", "properties": {"i": {"type": "integer"}, "score": {"type": "number"}}, "required": ["i", "score"]}}
def score_llm(headlines):
    \"\"\"Batch scoring: one call, all headlines, score in [-1, 1].\"\"\"
    numbered = "\\n".join(f"{i}: {h}" for i, h in enumerate(headlines))
    res = llm(f"Score each headline's sentiment for Bitcoin's price from -1 (very negative) to 1 (very positive).\\n{numbered}",
              system="You are a financial news analyst. Return only the JSON array.", json_schema=SCHEMA)
    if res is None: return None
    m = {d["i"]: float(d["score"]) for d in res}
    return [m.get(i, 0.0) for i in range(len(headlines))]

# Full history: lexicon (cheap, deterministic). Last 40 headlines: LLM if available, to measure agreement.
news["score_lex"] = score_lexicon(news["headline"])
recent = news.tail(40)
llm_scores = score_llm(list(recent["headline"]))
if llm_scores is None:
    print("[MOCK] no GEMINI_API_KEY — sentiment = keyword lexicon for the whole history. Label this in any memo.")
    SCORER = "lexicon (MOCK)"
else:
    agree = np.corrcoef(llm_scores, recent["score_lex"])[0, 1]
    print(f"[live] Gemini scored {len(llm_scores)} recent headlines; correlation with the lexicon: {agree:.2f}")
    news.loc[recent.index, "score_llm"] = llm_scores
    SCORER = "lexicon for history, Gemini on the last 40"
news["score"] = news["score_lex"]          # the feature used below; swap for score_llm if you score the full history
news[["published", "headline", "score"]].tail(5)
"""),
md("""
**Point-in-time alignment.** The feature for day *t* must use only headlines with `published ≤ t`. Index the score by `published`, not by `event_date`.
"""),
code("""
sent = news.set_index("published")["score"].rename("sent")           # honest: available on the day it was published
sent_leaky = news.set_index("event_date")["score"].rename("sent")    # what an assistant does when the file has a 'date' column
"""),
md("""
### D1. Added to the week-3 walk-forward
Same features as week 3 (rebuilt compactly), target = 5-day direction, gradient boosting, time-ordered splits. Baseline AUC vs baseline + `sent`.

**🔍 CHECK (bet 4).** Does the sentiment feature raise the out-of-sample AUC by more than 0.02? Yes or no — write it down.
"""),
code("""
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score

H = 5
d = pd.DataFrame({"ret": r_btc})
f = pd.DataFrame(index=d.index)
f["ret_1"] = d["ret"]; f["ret_5"] = d["ret"].rolling(5).sum(); f["ret_21"] = d["ret"].rolling(21).sum()
f["vol_5"] = d["ret"].rolling(5).std(); f["vol_21"] = d["ret"].rolling(21).std(); f["vol_ratio"] = f["vol_5"] / f["vol_21"]
f["sent"] = sent.reindex(f.index).fillna(0)
f["sent_5"] = f["sent"].rolling(5).mean()
fwd_ret = d["ret"][::-1].rolling(H).sum()[::-1].shift(-1)
y = (fwd_ret > 0).astype(int)
data = f.join(y.rename("y")).dropna()

def walk_forward_auc(cols):
    m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200, random_state=0)
    aucs = []
    for tr, te in TimeSeriesSplit(n_splits=6, test_size=250).split(data):
        m.fit(data.iloc[tr][cols], data.iloc[tr]["y"])
        aucs.append(roc_auc_score(data.iloc[te]["y"], m.predict_proba(data.iloc[te][cols])[:, 1]))
    return np.mean(aucs)

base_cols = ["ret_1", "ret_5", "ret_21", "vol_5", "vol_21", "vol_ratio"]
res = pd.Series({"baseline (price features)": walk_forward_auc(base_cols),
                 "baseline + sentiment":      walk_forward_auc(base_cols + ["sent", "sent_5"]),
                 "sentiment only":            walk_forward_auc(["sent", "sent_5"])}).round(3)
print(f"scorer: {SCORER} | base rate (share up): {data.y.mean():.3f}"); res
"""),
md("""
Why it adds little, and why that is the *expected* result: the headline of day *t* is a noisy function of the return of day *t−1*, which is already in the feature set as `ret_1`. A text signal has to carry information that is **not already in the price** and that arrives **before** the price moves. Most do not. The honest test is not "does sentiment correlate with returns" (it does — backwards) but "does it improve a model that already has the price".
"""),
md("""
### D2. As a trading rule, with costs — and the join that leaks
"""),
code("""
sig_sent = np.sign(sent.reindex(btc.index).fillna(0))
honest = stats(backtest(btc, sig_sent, cost_bps=10), 365)

# the leak: join on event_date and skip the shift -> today's position uses the headline about today's move
pos_leak = np.sign(sent_leaky.reindex(btc.index).fillna(0))
r = btc.pct_change(); traded = pos_leak.diff().abs()
leak_net = (pos_leak * r - traded * 10 / 1e4).dropna()
pd.DataFrame({"sentiment rule, published-date, shift(1), 10 bps": honest,
              "joined on event_date, no shift (LEAK)": stats(pd.DataFrame({"pos": pos_leak, "traded": traded, "net": leak_net}).dropna(), 365)}).round(3)
"""),
md("""
**How to test any text signal** — the four questions to answer in writing before believing a number:

| question | what to show |
|---|---|
| point-in-time | for each row, the timestamp at which the text was *readable*; feature date ≥ that |
| no date leakage | join on availability date, then `shift(1)`; never on the event date |
| beyond the price | AUC / Sharpe of *price features + text* vs *price features alone* |
| after costs | a text signal that flips daily pays daily; report net of a stated cost |
"""),

# ------------------------------------------------------------------ E
md("## Block E — Model risk (20')"),
md("""
Reading and prompts are in `notes.md`. Here, one number: a **monitoring rule with a kill-switch** for the momentum rule of Block B, treated as if it decided a hedge. Rolling one-year Sharpe and drawdown from peak; the switch fires when either crosses a line set *before* going live.
"""),
code("""
bt = backtest(btc, momentum_signal(btc, 20), cost_bps=10)
eq = (1 + bt["net"]).cumprod()
roll_sharpe = bt["net"].rolling(365).apply(lambda x: sharpe(x, 365), raw=False)
dd = eq / eq.cummax() - 1
KILL_SHARPE, KILL_DD = 0.0, -0.30                      # decided before go-live, written in the model inventory
kill = (roll_sharpe < KILL_SHARPE) | (dd < KILL_DD)
episodes = (kill & ~kill.shift(1, fill_value=False)).sum()
print(f"days switched off: {kill.sum()} of {len(kill)} | episodes: {episodes} | first trigger: {kill[kill].index.min().date() if kill.any() else '—'}")
fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
roll_sharpe.plot(ax=ax[0], title="rolling 1y Sharpe (net of 10 bps)"); ax[0].axhline(KILL_SHARPE, color="red", lw=0.8)
dd.plot(ax=ax[1], title="drawdown from peak"); ax[1].axhline(KILL_DD, color="red", lw=0.8)
plt.tight_layout(); plt.show()
"""),
md("""
**Model inventory entry — fill it in (5 minutes):**

| field | your entry |
|---|---|
| model name and owner | |
| decision it takes or informs | |
| inputs, and the date each becomes available | |
| validation performed *by someone else*, and when | |
| known failure modes (from Blocks C and D) | |
| monitoring metric and threshold | |
| who can switch it off, and how fast | |
"""),

md("""
## Take-home (write three lines)

_1._

_2._

_3._

Then `File ▸ Save a copy in GitHub` → `week-07/session.ipynb`. **Homework brief** → `week-07/homework.md`.
"""),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["colab"] = {"provenance": [], "name": "week-07_session.ipynb"}
out = ROOT / "session.ipynb"
nbf.write(nb, out); print("wrote", out, "| code cells:", sum(c.cell_type == "code" for c in cells))
