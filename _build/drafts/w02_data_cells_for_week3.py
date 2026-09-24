w2 = [
md("""
# Week 2 — The assistant writes it. You decide whether it is true.
**ESE · AI for Business and FinTech · 30 September 2026**

The sections follow the slides. Every number here is computed from the same dated snapshot as the slides, so you can check each one.
"""),
code("!pip -q install tiktoken yfinance"),
code("""
import math, numpy as np, pandas as pd, matplotlib.pyplot as plt
from collections import Counter

SNAPSHOT = "https://raw.githubusercontent.com/NiccoloSalvini/ese-ai/main/week-02/data/btc_spy_2022-01-01_2026-09-18.csv"
YIELDS   = "https://raw.githubusercontent.com/NiccoloSalvini/ese-ai/main/week-02/data/dgs10_2022-01-01_2026-09-18.csv"
px  = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)       # Bitcoin and the S&P 500 (SPY), dollars
y10 = pd.read_csv(YIELDS, index_col=0, parse_dates=True)["DGS10"] # US 10-year yield, in PERCENT
print(px.shape, px.index.min().date(), "->", px.index.max().date())
"""),
md("""
## 1. Temperature reshapes the odds

Last week's table. The model does not look the answer up: it picks from these odds. Temperature `T` decides how: raise every probability to `1/T`, then divide by the new total.
"""),
code("""
tokens = ["unchanged", "steady", "at", "on", "higher"]
p = np.array([0.62, 0.15, 0.10, 0.08, 0.05])

def at_temperature(p, T):
    if T == 0:                                   # T = 0: always the top token
        q = np.zeros_like(p); q[p.argmax()] = 1; return q
    q = p ** (1 / T)
    return q / q.sum()

pd.DataFrame({f"T = {T}": at_temperature(p, T).round(2) for T in [0, 0.5, 1, 2]}, index=tokens)
"""),
md("""
**Bet first:** at `T = 1`, ask ten times. How many times "unchanged"? Then run the cell below.
"""),
code("""
rng = np.random.default_rng(0)
for T in [0, 1, 2]:
    q = at_temperature(p, T)
    picks = rng.choice(tokens, size=10, p=q)
    print(f"T = {T}:", " ".join(picks))
"""),
md("""
## 2. Two piles

Ask your assistant: *"Summarise the last annual results of [a company you know]: revenue, profit, number of employees, and the CEO's name."*

Copy the answer below. Then split every sentence into two piles.

| Verifiable — a number, date, name or source you can open | Plausible — fluent, and nothing to check it against |
|---|---|
| … | … |

Now check two items from the left pile against the company's own report. Were they right?
"""),
md("""
## 3. Your tiny LLM, piece 1: a tokenizer

Find the pair of symbols that appears most often; give it a new name; repeat. This is byte-pair encoding, the method real tokenizers use.
"""),
code("""
def learn_merges(text, merges=8):
    seq = [c if c != " " else "_" for c in text]          # _ marks a space
    for step in range(1, merges + 1):
        pairs = Counter(zip(seq, seq[1:]))
        (a, b), n = max(pairs.items(), key=lambda kv: (kv[1], -list(pairs).index(kv[0])))
        if n < 2:
            break
        out, i = [], 0
        while i < len(seq):
            if i < len(seq) - 1 and (seq[i], seq[i + 1]) == (a, b):
                out.append(a + b); i += 2
            else:
                out.append(seq[i]); i += 1
        seq = out
        print(f"merge {step}: {a!r} + {b!r} seen {n} times -> {a+b!r:10}  text is now {len(seq)} symbols")
    return seq

text = ("the bank left rates unchanged. the bank said rates will stay unchanged. "
        "rates are high and the bank expects rates to stay high.")
print(len(text), "characters to start")
pieces = learn_merges(text)
"""),
md("""
**Your turn.** Paste a paragraph of your own in English, then the same in Russian. Run 30 merges on each. How many symbols per word does each language end up with — and why?
"""),
code("""
mine_en = "paste an English paragraph here"
mine_ru = "вставьте сюда абзац на русском"
for name, t in [("English", mine_en), ("Russian", mine_ru)]:
    seq = learn_merges(t, merges=30)
    print(f"{name}: {len(seq) / len(t.split()):.1f} symbols per word\\n")
"""),
md("""
## 4. Is Bitcoin riskier than the stock market? Ten real days first

The week the US approved spot Bitcoin ETFs. Note the gaps.
"""),
code("""
ten = px.loc["2024-01-05":"2024-01-16"]
print(ten.round(2))
print("\\nBitcoin days:", ten["BTC-USD"].notna().sum(), "| stock-market days:", ten["SPY"].notna().sum())
print("Monday 8 Jan, Bitcoin: %.0f / %.0f - 1 = %+.1f%%" % (ten.loc["2024-01-08", "BTC-USD"], ten.loc["2024-01-07", "BTC-USD"],
      100 * (ten.loc["2024-01-08", "BTC-USD"] / ten.loc["2024-01-07", "BTC-USD"] - 1)))
"""),
md("""
### 🔍 CHECK — the assistant's cell

Asked for "Bitcoin's annual volatility and its return in 2022", the assistant wrote the cell below. It runs, and the numbers look reasonable. **Two are wrong.** Ten minutes, alone.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
r = px["BTC-USD"].pct_change().dropna()
vol = r.std() * np.sqrt(252)
r22 = px.loc["2022", "BTC-USD"].pct_change().dropna()
total_2022 = r22.sum()
print(f"Bitcoin annual volatility: {vol:.1%}")
print(f"Bitcoin return in 2022:    {total_2022:.1%}")
"""),
md("""
<details><summary>What went wrong</summary>

1. **√252** is the number of days the *stock market* trades in a year. Bitcoin trades every day: √365. The formula is right, the constant is wrong, and Bitcoin looks 17% calmer than it is.
2. **Returns added up.** A return compounds: +50% then −50% is not 0%, it is 1.5 × 0.5 − 1 = −25%. Adding the daily returns of 2022 says −85%; the true loss, from the first and last price, is −65%.
</details>
"""),
code("""
# corrected: the right constant, and returns multiplied — then the same number a second way
vol_btc = r.std() * np.sqrt(365)
vol_spy = px["SPY"].dropna().pct_change().std() * np.sqrt(252)
s22 = px.loc["2022", "BTC-USD"].dropna()
total_2022 = (1 + s22.pct_change().dropna()).prod() - 1
check_2022 = s22.iloc[-1] / s22.iloc[0] - 1                 # first and last price: must agree
print(f"Bitcoin annual volatility {vol_btc:.1%}  vs S&P 500 {vol_spy:.1%}")
print(f"Bitcoin 2022: compounded {total_2022:.1%}, from first and last price {check_2022:.1%}")
"""),
md("""
## 5. Two calendars, one join

**Bet first:** fill the stock market's weekends with Friday's price. Does the S&P 500 look more volatile, or less?
"""),
code("""
equity = px.dropna()                   # equity calendar: only days both traded
crypto = px.ffill().dropna()           # crypto calendar: SPY carried over weekends and holidays
for name, df in [("equity calendar", equity), ("crypto calendar", crypto)]:
    r = df.pct_change().dropna()
    print(f"{name}: {len(df):,} rows | S&P 500 vol {r['SPY'].std() * np.sqrt(252):.1%} | "
          f"corr BTC-S&P {r.corr().iloc[0, 1]:.2f} | days SPY 'returned' exactly 0: {(r['SPY'] == 0).sum()}")
"""),
md("""
**After every join, three checks:** rows before and after; `isna().sum()`; one row from the middle, read.
"""),
code("""
btc = px[["BTC-USD"]].dropna()                   # 7 days a week
spy = px[["SPY"]].dropna()                       # trading days only
for how in ["inner", "left"]:
    joined = btc.join(spy, how=how)
    print(f"{how:5} join: rows {len(btc):,} and {len(spy):,} -> {len(joined):,} | missing SPY: {joined['SPY'].isna().sum()}")
print("\\none row from the middle of the left join:")
print(joined.iloc[len(joined) // 2])
"""),
md("""
## 6. A number without a unit
"""),
code("""
pct_returns = [1.2, -0.8, 0.5]                                   # written in percent
right = np.prod([1 + r / 100 for r in pct_returns]) - 1          # convert first
wrong = np.prod([1 + r for r in pct_returns]) - 1                # read as decimals by mistake
print(f"right: {right:+.2%}   wrong: {wrong:+.0%}")

wk = equity.join(y10, how="left").ffill().resample("W-FRI").last().dropna()
d_btc = wk["BTC-USD"].pct_change()
for label, y in [("percentage points", wk["DGS10"]), ("decimal", wk["DGS10"] / 100)]:
    d_y = y.diff(); ok = d_btc.notna() & d_y.notna()
    print(f"yield in {label:17}: correlation {d_btc[ok].corr(d_y[ok]):.3f}   slope {np.polyfit(d_y[ok], d_btc[ok], 1)[0]:.2f}")
"""),
md("""
## 7. Snapshots, and what never goes into a chatbot

Every number above came from one dated file. Save the data behind every number you report, with the date in the name; pin your library versions; set a seed wherever randomness enters.

Nothing confidential goes into an AI tool: no client names, no unpublished figures, no personal data.

### Before you leave: three lines, in your words

1. …
2. …
3. …

---
# For the homework: joining an external series

The sections below show the full pattern on live data — a macro series (FRED) and an on-chain series — for Homework 2.
"""),
code(UTILS),
code("""
px = load_prices(["BTC-USD", "SPY", "AAPL"], start="2022-01-01")
print(px.index.min().date(), "->", px.index.max().date(), "|", px.shape)
"""),
md("## Block B — Join with external series (macro + on-chain)"),
md("""
This is where analysis becomes interesting: internal or market data alone rarely answers a business question. We add:
- **US 10-year Treasury yield** (FRED series `DGS10`), a proxy for the risk-free rate / macro regime;
- **Bitcoin unique active addresses** (blockchain.com public chart API), an on-chain adoption proxy.

Both are free and need no key. Both fetches have a fallback so the notebook still runs offline.
"""),
code("""
import requests, io, os

def load_fred(series="DGS10", cache_dir="data"):
    os.makedirs(cache_dir, exist_ok=True); snap = f"{cache_dir}/fred_{series}.csv"
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
        s = pd.read_csv(io.StringIO(requests.get(url, timeout=20).text), index_col=0, parse_dates=True)[series]
        s = pd.to_numeric(s, errors="coerce").rename(series); s.to_csv(snap); print("[live] FRED", series); return s
    except Exception as e:
        print("[warn] FRED failed:", type(e).__name__)
    if os.path.exists(snap):
        print("[snapshot] FRED"); return pd.read_csv(snap, index_col=0, parse_dates=True).iloc[:, 0].rename(series)
    print("[SYNTHETIC] FRED"); idx = pd.bdate_range("2022-01-01", pd.Timestamp.today().normalize())
    return pd.Series(3 + np.cumsum(np.random.default_rng(1).normal(0, 0.03, len(idx))), idx, name=series)

def load_btc_addresses(cache_dir="data"):
    os.makedirs(cache_dir, exist_ok=True); snap = f"{cache_dir}/btc_active_addresses.csv"
    try:
        url = "https://api.blockchain.info/charts/n-unique-addresses?timespan=5years&format=json&sampled=false"
        js = requests.get(url, timeout=20).json()["values"]
        s = pd.Series({pd.to_datetime(v["x"], unit="s"): v["y"] for v in js}, name="active_addresses")
        s.to_csv(snap); print("[live] blockchain.com"); return s
    except Exception as e:
        print("[warn] blockchain.com failed:", type(e).__name__)
    if os.path.exists(snap):
        print("[snapshot] blockchain.com"); return pd.read_csv(snap, index_col=0, parse_dates=True).iloc[:, 0].rename("active_addresses")
    print("[SYNTHETIC] addresses"); idx = pd.date_range("2022-01-01", pd.Timestamp.today().normalize())
    return pd.Series(7e5 + 1e5 * np.sin(np.arange(len(idx)) / 60) + np.random.default_rng(2).normal(0, 5e4, len(idx)), idx, name="active_addresses")

dgs10 = load_fred("DGS10")
addr = load_btc_addresses()
print(dgs10.tail(3)); print(addr.tail(3))
"""),
md("""
### 🔍 CHECK — the assistant's join
Asked to "merge the price data with the yield and the on-chain series", the assistant wrote the cell below. It runs. Look at the row count and the date range of the result before and after, then explain what was lost and why.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
merged_bad = pd.merge(px, dgs10, left_index=True, right_index=True).merge(addr, left_index=True, right_index=True)
print("rows before:", len(px), "| rows after:", len(merged_bad))
print(merged_bad.index.min().date(), "→", merged_bad.index.max().date())
merged_bad.isna().sum()
"""),
md("""
<details><summary>What went wrong</summary>

`pd.merge` defaults to an **inner join**: only dates present in *all three* series survive. FRED has no weekends and has `NaN` on US holidays (which survive as NaN — check the `isna()` output); the on-chain series is daily. The result silently dropped weekends and is on an equity calendar without anyone deciding that. Also: FRED yields are in **percent** (4.25 = 4.25%), prices in dollars, addresses in counts — the assistant will happily correlate them without saying so. Units are your job.
</details>
"""),
code("""
# Explicit version: choose the calendar (equity days), left-join, forward-fill macro, state units.
base = px.dropna()                                    # equity calendar
df = base.join(dgs10.ffill(), how="left").join(addr, how="left")
df["DGS10"] = df["DGS10"] / 100                       # now a decimal rate
df = df.rename(columns={"DGS10": "us10y"})
df["active_addresses"] = df["active_addresses"].ffill()
print(len(base), len(df)); df.tail()
"""),
md("## Block C — Charts that answer a question, and rolling statistics"),
code("""
import matplotlib.pyplot as plt
rets = df[["BTC-USD", "SPY", "AAPL"]].pct_change()
roll_corr = rets["BTC-USD"].rolling(60).corr(rets["SPY"])

fig, ax = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
roll_corr.plot(ax=ax[0], title="60-day rolling correlation, BTC vs SPY")
ax[0].axhline(0, color="k", lw=0.5)
df["us10y"].plot(ax=ax[1], title="US 10y yield (decimal)")
events = {"2024-01-10": "spot ETF approval", "2024-04-19": "halving"}
for d, label in events.items():
    if pd.Timestamp(d) in df.index:
        for a in ax: a.axvline(pd.Timestamp(d), color="grey", ls="--", lw=0.8)
        ax[0].annotate(label, (pd.Timestamp(d), roll_corr.max() * 0.9), fontsize=8, rotation=90)
plt.tight_layout(); plt.show()
"""),
md("""
**🔍 CHECK.** Does the correlation chart *answer a question*, or only show a line? Write the question it answers in one sentence. If you cannot, the chart is not finished. (Sanity check the data too: you should see BTC's correlation with equities fall after some events and rise in macro-stress periods. If the line looks like noise around zero everywhere, suspect an alignment problem.)
"""),
code("""
# On-chain vs price: is address activity leading or lagging price? Cross-correlation at different lags (weekly data).
w = df[["BTC-USD", "active_addresses"]].resample("W-FRI").last().pct_change().dropna()
lags = range(-8, 9)
xc = pd.Series({k: w["BTC-USD"].corr(w["active_addresses"].shift(k)) for k in lags})
xc.plot(kind="bar", figsize=(9, 3), title="corr(BTC weekly return, address growth shifted by k weeks)  — k>0: addresses lead")
plt.show()
"""),
md("""
**🔍 CHECK.** Positive `k` means address growth from `k` weeks *ago* vs return *now*. If the biggest bar is at negative `k`, price leads activity, not the reverse — the opposite of the story "adoption drives price". Read the sign convention in `shift()` before you conclude anything. This is exactly the kind of check an assistant will not do for you.
"""),
md("## Block D — Reproducibility and privacy"),
code("""
# 1) Snapshot the exact data you analysed, with the date, so the memo can be re-run.
import datetime as dt, os
os.makedirs("data", exist_ok=True)
stamp = dt.date.today().isoformat()
df.to_csv(f"data/week02_merged_{stamp}.csv")
print("saved", f"data/week02_merged_{stamp}.csv", df.shape)

# 2) Record the environment.
!pip freeze 2>/dev/null | grep -i -E "^(pandas|numpy|yfinance|matplotlib)=" > data/requirements_week02.txt; cat data/requirements_week02.txt
"""),
md("""
**Rules from here on:**
- every notebook that produces a number in a memo saves the data it used (`data/…_YYYY-MM-DD.csv`);
- random operations set a seed (`np.random.default_rng(0)`);
- nothing confidential goes into an AI tool: no client data, no personal data, no internal documents. Public market data is fine. If in doubt, anonymise or aggregate first.

**Homework brief** → see `week-02/homework.md`.
"""),
]

