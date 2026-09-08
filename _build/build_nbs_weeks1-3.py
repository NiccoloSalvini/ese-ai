"""Builds week-01..03 session notebooks with nbformat."""
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

# =====================================================================
# WEEK 1
# =====================================================================
w1 = [
md("""
# Week 1 — How LLMs work, and how we will work
**ESE · AI for Business and FinTech · 21 September 2026**

This notebook is the live material for session 1. Run it top to bottom in Google Colab (`Runtime ▸ Run all` is fine the first time).
Cells marked **🔍 CHECK** contain something you must verify or critique before moving on — that is the main skill of this course.

How to use the AI assistant in this course: ask it to write code, run the code, read the error or the output, ask again, and **verify against something you already know** (a price you can look up, a number you can compute by hand, a date you remember).
"""),
md("## Block A — Setup (Colab, GitHub, assistant)"),
code("""
# Install what is not already in Colab. (~30 s)
!pip -q install yfinance tiktoken google-genai
"""),
code("""
import sys, platform, pandas as pd, numpy as np, matplotlib
print("Python", sys.version.split()[0], "| pandas", pd.__version__, "| numpy", np.__version__)
try:
    import google.colab  # noqa
    IN_COLAB = True
except ImportError:
    IN_COLAB = False
print("Running in Colab:", IN_COLAB)
"""),
md("""
**Saving your work to GitHub** (do this now, once):

1. Create a private repository on GitHub named `ese-ai-fintech` and invite the tutor as a collaborator.
2. In Colab: `File ▸ Save a copy in GitHub` → choose the repo, path `week-01/session.ipynb`, and write a commit message. Every time you finish work, repeat this. The commit history is your evidence of work.
3. Homework goes in `week-01/hw/`.

**API key** (optional today, needed from week 4): create a free key at Google AI Studio, then in Colab open the 🔑 *Secrets* panel on the left, add `GEMINI_API_KEY`, and enable notebook access. Never paste a key into a cell.
"""),
md("## Block B — LLMs at a working level"),
md("""
### B1. Tokens: the model does not see words
An LLM reads and writes **tokens** — chunks of characters, roughly ¾ of an English word each. Everything is billed, limited and reasoned about in tokens. Numbers, code and non-English text tokenize badly: a Russian sentence costs ~2–3× the tokens of its English translation.
"""),
code("""
try:
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")   # tokenizer family used by recent OpenAI models; others are similar
except Exception as e:                           # offline fallback: crude approximation, only to show the idea
    import re
    class _Enc:
        def encode(self, s): return re.findall(r"\\w+|[^\\w\\s]", s)
        def decode(self, t): return t[0]
    enc = _Enc(); print("tiktoken unavailable (%s) — using a crude word/punctuation splitter instead" % type(e).__name__)

samples = [
    "The ECB left rates unchanged at 2.00% on Thursday.",
    "Bitcoin fell 4.2% to $58,310 after the ETF outflow data.",
    "ЕЦБ оставил ставки без изменений на уровне 2,00%.",
    "df.groupby('ticker')['ret'].rolling(21).std()",
]
for s in samples:
    toks = enc.encode(s)
    print(f"{len(toks):3d} tokens | {len(s.split()):2d} words | {s}")
    print("     ", [enc.decode([t]) for t in toks][:14], "...\\n")
"""),
md("""
### B2. Context window: the model's working memory
Everything the model knows about *your* problem must fit in the context window (today: 128k–1M tokens depending on the model). What is not in the context does not exist for the model — it will fill the gap with something plausible. This is the root of most "hallucinations": not lying, but **completing a pattern with missing information**.

Practical consequences for business use:
- long documents must be chunked and only the relevant parts fed in (that is what *retrieval* does — week 4);
- the model has no memory between calls unless you send the history again;
- cost ≈ (input tokens + output tokens) × price per token — so verbosity is money.
"""),
code("""
# Rough cost of sending a document to a model. Prices are illustrative — check the provider page.
price_per_1M_input = {"small model": 0.10, "mid model": 1.00, "frontier model": 5.00}   # USD per 1M input tokens
doc_tokens = 90_000          # e.g. a 10-K annual report, ~60 pages of dense text
for name, p in price_per_1M_input.items():
    print(f"{name:15s}: ${doc_tokens/1e6*p:.3f} per read; 1,000 reads/day -> ${doc_tokens/1e6*p*1000:,.0f}/day")
"""),
md("""
### B3. Sampling: the same prompt gives different answers
The model outputs a probability distribution over the next token and *samples* from it. `temperature` controls how much randomness is allowed. Temperature 0 is (almost) deterministic — use it for extraction and classification. Higher temperatures for brainstorming.

The cell below calls Gemini **only if** you set up the key. If not, skip it — the tutor will demonstrate.
"""),
code("""
import os
API_KEY = None
try:
    from google.colab import userdata
    API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=API_KEY)
    prompt = "In one sentence: why did Bitcoin fall in the week of 5 August 2024?"
    for temp in (0.0, 1.0, 1.0):
        r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,
                                           config=types.GenerateContentConfig(temperature=temp))
        print(f"T={temp}: {r.text.strip()}\\n")
else:
    print("No API key found — skipping. Ask the tutor to run this cell on the projector.")
"""),
md("""
**🔍 CHECK.** Whatever the model answered above: which claims can you verify in five minutes, and from which source? Which claims are *plausible but unverifiable*? Write two lines in the cell below. (This exact exercise — separate what you can check from what merely sounds right — is what you will do with every AI output in this course.)
"""),
md("""
_Your notes here:_
"""),
md("""
### B4. Embeddings: meaning as geometry
An **embedding** turns a piece of text into a vector (a list of numbers) so that texts with similar meaning are close together. This is what makes search-by-meaning, clustering and retrieval possible. We do not need a neural model to understand the idea — the cell below uses a crude bag-of-words embedding so you can see the mechanics; real embeddings from a model are much better at *meaning*, but the geometry is the same.
"""),
code("""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "The central bank raised interest rates to fight inflation.",
    "Monetary policy tightened as the ECB hiked its deposit rate.",
    "The football match ended in a draw after extra time.",
    "Ethereum gas fees dropped after the network upgrade.",
    "Transaction costs on the blockchain fell following the protocol update.",
]
X = TfidfVectorizer().fit_transform(docs)
sim = pd.DataFrame(cosine_similarity(X), index=range(len(docs)), columns=range(len(docs))).round(2)
print(sim)
print("\\nDoc 0 vs doc 1 (same meaning, different words):", sim.loc[0, 1])
print("Doc 3 vs doc 4 (same meaning, different words):", sim.loc[3, 4])
"""),
md("""
**🔍 CHECK.** Docs 0–1 and docs 3–4 say the same thing in different words, yet the crude embedding gives them low similarity. Why? What would a model-based embedding do differently? (Hint: "raised rates" and "hiked its deposit rate" share no words.) This is the gap that neural embeddings close — we will use them in week 4.
"""),
md("""
### B5. Tool use and agents (concept only today)
A plain LLM can only produce text. **Tool use** lets the model emit a structured request ("call `get_price('BTC-USD')`"), your code executes it, and the result goes back into the context. An **agent** is a loop: model → tool → model → tool … until done. Everything you will build in weeks 4–5 is this loop; everything that goes wrong with agents (cost, loops, wrong tool, injected instructions) comes from the same loop.
"""),
md("## Block C — First data notebook: three assets"),
code(UTILS),
code("""
tickers = ["BTC-USD", "AAPL", "^GSPC"]
px = load_prices(tickers, start="2022-01-01")
px.tail()
"""),
code("""
# Daily simple returns
rets = px.pct_change().dropna()
print(rets.describe().round(4))
"""),
code("""
import matplotlib.pyplot as plt
(px / px.iloc[0] * 100).plot(figsize=(10, 4), title="Growth of 100 (rebased)")
plt.ylabel("index"); plt.show()
"""),
md("""
### 🔍 CHECK — the assistant's volatility code
The cell below is the kind of code an assistant produces when asked "annualise the volatility of these assets". It runs without errors. **It contains two mistakes.** Find them before reading the solution.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
ann_vol = rets.std() * np.sqrt(252)
cum_ret = rets.sum()
summary = pd.DataFrame({"annualised_vol": ann_vol, "cumulative_return": cum_ret}).round(3)
summary
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **252** is the number of trading days for equities. Bitcoin trades every day: 365 rows per year, so its annualised volatility is understated by √(252/365) ≈ 17%. Whenever a constant appears in assistant code, ask where it comes from.
2. **Summing simple returns is not the cumulative return.** +50% then −50% sums to 0 but leaves you at 75. The correct figure is `(1 + rets).prod() - 1`. Check: compare with `px.iloc[-1] / px.iloc[0] - 1`.

The general lesson: the assistant is fluent, not correct. The cheapest verification is always *compute the same number a second way*.
</details>
"""),
code("""
# Corrected version
days_per_year = {t: (365 if t.endswith("-USD") else 252) for t in px.columns}
ann_vol = pd.Series({t: rets[t].std() * np.sqrt(days_per_year[t]) for t in px.columns})
cum_ret = (1 + rets).prod() - 1
check = px.iloc[-1] / px.iloc[0] - 1           # second way
pd.DataFrame({"annualised_vol": ann_vol, "cumulative_return": cum_ret, "check": check}).round(3)
"""),
md("## Block D — Prompting that matters at work"),
md("""
Try these in your chat assistant now, on the same question, and compare the outputs:

1. **Bare:** "Explain the volatility of Bitcoin vs Apple."
2. **Framed:** "You are a quantitative analyst. Using daily data 2022–2026, compare the annualised volatility of BTC-USD and AAPL. State the day-count convention you use for each. Output a two-row table and one sentence of interpretation. If you are not sure of a number, say so instead of inventing it."
3. **Structured for code:** "Write Python (pandas) that computes annualised volatility for a DataFrame `rets` of daily returns, using 365 days for columns ending in `-USD` and 252 otherwise. Return a Series. No explanation."

What changed and why: role and context reduce generic filler; explicit conventions remove silent assumptions; asking for a fixed output shape makes the answer checkable; "say so instead of inventing" lowers (does not remove) hallucination.

**Homework brief** → see `week-01/homework.md`.
"""),
]

# =====================================================================
# WEEK 2
# =====================================================================
w2 = [
md("""
# Week 2 — Data analysis with AI as pair programmer
**ESE · AI for Business and FinTech · 28 September 2026**

Goal of the session: acquire, clean, join and chart financial data with the assistant writing most of the code — while you catch its silent errors. By the end you will have a reproducible pipeline that joins market prices with an external macro series and an on-chain series.
"""),
code("!pip -q install yfinance"),
code(UTILS),
md("## Block A — pandas by doing"),
code("""
px = load_prices(["BTC-USD", "SPY", "AAPL"], start="2022-01-01")
print(px.index.min().date(), "→", px.index.max().date(), "|", px.shape)
px.head(3)
"""),
md("""
A DataFrame is a spreadsheet with an index. The four operations you will use 90% of the time:

| Operation | Excel analogue | pandas |
|---|---|---|
| filter rows | AutoFilter | `df[df["col"] > 0]` |
| new column | formula column | `df["ret"] = df["px"].pct_change()` |
| aggregate | PivotTable | `df.groupby(...).agg(...)` / `df.resample("W").last()` |
| join | VLOOKUP / Power Query merge | `df.join(other)` / `pd.merge(...)` |
"""),
code("""
# Missing values: BTC trades 7 days a week, SPY and AAPL 5. Look at a week that contains a weekend.
px.loc["2024-01-05":"2024-01-09"]
"""),
md("""
**🔍 CHECK.** `load_prices` already dropped rows where *all* columns were missing, but weekend rows survive because BTC has a value. Before computing anything across assets you must decide: drop weekends (equity calendar), or fill equities forward (crypto calendar)? Neither is "right" — but choosing silently is wrong. Which one does `pct_change()` implicitly choose if you do nothing?
"""),
code("""
# Two explicit choices, side by side
px_eq = px.dropna()                       # equity calendar: only days where everything traded
px_cr = px.ffill()                        # crypto calendar: carry equities over the weekend
print("equity calendar rows:", len(px_eq), "| crypto calendar rows:", len(px_cr))

rets_eq = px_eq.pct_change().dropna()
rets_cr = px_cr.pct_change().dropna()
print("\\nBTC daily vol — equity calendar: %.4f | crypto calendar: %.4f" % (rets_eq["BTC-USD"].std(), rets_cr["BTC-USD"].std()))
print("BTC mean Monday return on equity calendar (Fri→Mon, 3 days of moves): %.4f" % rets_eq["BTC-USD"][rets_eq.index.dayofweek == 0].mean())
"""),
code("""
# Resampling: weekly prices (last obs of the week), and weekly returns
wk = px_eq.resample("W-FRI").last()
wk_rets = wk.pct_change().dropna()
wk_rets.tail()
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

# =====================================================================
# WEEK 3
# =====================================================================
w3 = [
md("""
# Week 3 — Machine learning through one problem
**ESE · AI for Business and FinTech · 5 October 2026**

One problem, done properly, teaches more than a tour of algorithms. Today: *can we predict anything about next week's BTC from what we know today?* We build features, train two models against a trivial baseline, and — most importantly — evaluate them in the only way that means anything for time series. Then we turn a prediction into a decision.
"""),
code("!pip -q install yfinance"),
code(UTILS),
code("""
px = load_prices(["BTC-USD", "SPY"], start="2018-01-01").ffill().dropna()
d = pd.DataFrame(index=px.index)
d["ret"] = px["BTC-USD"].pct_change()
d["spy_ret"] = px["SPY"].pct_change()
d = d.dropna()
print(d.shape); d.tail(3)
"""),
md("## Block A — Features, targets, baselines"),
md("""
**Feature** = something known *at the time of prediction*. **Target** = the thing we want to know, which happens *after*. The entire discipline of ML on time series is keeping the wall between them intact.

We define two targets for the same features, because they behave very differently:
- **Direction**: is the return over the next 5 trading days positive?
- **Volatility regime**: will realised volatility over the next 5 days be above its trailing median?
"""),
code("""
H = 5   # horizon in trading days

# Features: everything uses only past information (note the .shift(1) is NOT needed because rolling windows end at t inclusive, and the target starts at t+1)
f = pd.DataFrame(index=d.index)
f["ret_1"]   = d["ret"]
f["ret_5"]   = d["ret"].rolling(5).sum()
f["ret_21"]  = d["ret"].rolling(21).sum()
f["vol_5"]   = d["ret"].rolling(5).std()
f["vol_21"]  = d["ret"].rolling(21).std()
f["vol_ratio"] = f["vol_5"] / f["vol_21"]
f["spy_ret_5"] = d["spy_ret"].rolling(5).sum()
f["dow"]     = d.index.dayofweek

# Targets: strictly in the future (t+1 … t+H)
fwd_ret = d["ret"][::-1].rolling(H).sum()[::-1].shift(-1)   # sum of returns t+1..t+H (reverse-rolling, then shift) — verified by hand below
fwd_vol = d["ret"][::-1].rolling(H).std()[::-1].shift(-1)
y_dir = (fwd_ret > 0).astype(int).rename("y_dir")
y_vol = (fwd_vol > f["vol_21"].expanding().median()).astype(int).rename("y_vol")   # vs trailing (expanding) median: no future info

data = f.join([y_dir, y_vol, fwd_ret.rename("fwd_ret")]).dropna()
print(data.shape)
data.tail(3)
"""),
md("""
**🔍 CHECK — verify the target by hand.** Pick a date, and confirm that `fwd_ret` on that date equals the sum of `ret` over the *following* 5 rows. If it includes the current day, the target leaks. Do this every single time you build a forward-looking target; it takes one minute and it is the most common bug in trading ML.
"""),
code("""
i = 1000
t = data.index[i]
manual = d["ret"].loc[t:].iloc[1:H+1].sum()
print(t.date(), "| fwd_ret in table:", round(data.loc[t, "fwd_ret"], 6), "| recomputed by hand:", round(manual, 6))
assert abs(manual - data.loc[t, "fwd_ret"]) < 1e-12, "target leaks or is misaligned"
print("OK — target uses only future rows")
"""),
code("""
# Base rates: what does 'doing nothing clever' score?
for col in ["y_dir", "y_vol"]:
    print(f"{col}: share of 1s = {data[col].mean():.3f}  -> majority-class accuracy = {max(data[col].mean(), 1-data[col].mean()):.3f}")
"""),
md("""
The **baseline** is the number a model must beat. For direction, "always predict up" already scores ~55% because BTC drifted up over the sample. A model with 56% accuracy has learned almost nothing. Any assistant that reports "our model achieves 58% accuracy" without the base rate next to it has reported nothing.
"""),
md("## Block B — Two models, two ways of splitting"),
code("""
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score

features = ["ret_1", "ret_5", "ret_21", "vol_5", "vol_21", "vol_ratio", "spy_ret_5", "dow"]
X = data[features]

models = {
    "logistic": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "gradient boosting": HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200, random_state=0),
}

def evaluate(model, X, y, splits):
    accs, aucs = [], []
    for tr, te in splits:
        model.fit(X.iloc[tr], y.iloc[tr])
        p = model.predict_proba(X.iloc[te])[:, 1]
        accs.append(accuracy_score(y.iloc[te], p > 0.5)); aucs.append(roc_auc_score(y.iloc[te], p))
    return np.mean(accs), np.mean(aucs)
"""),
md("""
### 🔍 CHECK — the assistant's split
Asked to "evaluate the model with cross-validation", the assistant used the sklearn default: a **random shuffle**. For time series this is a leak: the model trains on Wednesday and Friday and is tested on Thursday, with overlapping 21-day windows on both sides. Compare with a **time-ordered** split where the test set is always in the future of the training set.
"""),
code("""
rng = np.random.default_rng(0)
n = len(X)
shuffled = [(tr, te) for tr, te in [train_test_split(np.arange(n), test_size=0.2, random_state=s) for s in range(5)]]
ordered  = list(TimeSeriesSplit(n_splits=5, test_size=250).split(X))

rows = []
for target in ["y_dir", "y_vol"]:
    y = data[target]
    for name, m in models.items():
        a_s, u_s = evaluate(m, X, y, shuffled)
        a_o, u_o = evaluate(m, X, y, ordered)
        rows.append([target, name, a_s, u_s, a_o, u_o])
res = pd.DataFrame(rows, columns=["target", "model", "acc (shuffled)", "auc (shuffled)", "acc (time-ordered)", "auc (time-ordered)"]).round(3)
res["base rate"] = res["target"].map(lambda c: round(max(data[c].mean(), 1 - data[c].mean()), 3))
res
"""),
md("""
Read the table slowly. Three things should be visible:

1. **Shuffled scores are higher than time-ordered ones.** The difference is leakage, not skill.
2. **Direction is close to the base rate under an honest split.** With these features, 5-day direction of BTC is essentially unpredictable — which is what finance theory predicts and what an assistant will rarely tell you.
3. **Volatility regime is predictable** (AUC well above 0.5): volatility clusters. Same data, same models — the *question* decides whether ML has anything to offer. Choosing the question is the manager's job.
"""),
md("## Block C — Leakage on purpose"),
md("""
To recognise leakage you must see it once. We add a feature that is *almost* legitimate: a 5-day rolling volatility computed with a **centred** window (`center=True`), which is what an assistant may write when asked to "smooth" a series. Centred windows use future rows.
"""),
code("""
X_leak = X.copy()
X_leak["vol_5_centred"] = d["ret"].rolling(5, center=True).std().reindex(X.index)
X_leak = X_leak.dropna(); y = data.loc[X_leak.index, "y_vol"]
ordered_l = list(TimeSeriesSplit(n_splits=5, test_size=250).split(X_leak))
a, u = evaluate(models["gradient boosting"], X_leak, y, ordered_l)
print(f"with the 'smoothed' feature — time-ordered acc {a:.3f}, auc {u:.3f}   (compare with the honest row above)")
"""),
md("""
**🔍 CHECK.** The score jumped with a time-ordered split — so the split did not protect you. Leakage through *features* is invisible to any validation scheme. The only defence is reading every feature and asking: *at time t, could I have computed this?* Write down, for each of the eight honest features, the latest row it uses.
"""),
md("## Block D — From prediction to decision"),
md("""
A probability is not a decision. To act you need a **decision rule** (a threshold) and the **cost of each error**. Example: a treasury desk that wants to hedge BTC exposure when a high-volatility week is coming. Hedging costs money (`c_hedge`); an unhedged high-vol week costs more (`c_miss`). The best threshold depends on that ratio, not on accuracy.
"""),
code("""
# Walk-forward probabilities for the volatility target (out-of-sample only)
y = data["y_vol"]; m = models["gradient boosting"]
oos = pd.Series(index=X.index, dtype=float)
for tr, te in TimeSeriesSplit(n_splits=8, test_size=200).split(X):
    m.fit(X.iloc[tr], y.iloc[tr]); oos.iloc[te] = m.predict_proba(X.iloc[te])[:, 1]
oos = oos.dropna(); y_oos = y.loc[oos.index]

c_hedge, c_miss = 1.0, 4.0     # relative costs: hedge costs 1, missing a high-vol week costs 4
rows = []
for thr in np.arange(0.2, 0.81, 0.05):
    hedge = oos > thr
    cost = (hedge * c_hedge + (~hedge & (y_oos == 1)) * c_miss).sum()
    rows.append([thr, hedge.mean(), recall_score(y_oos, hedge), precision_score(y_oos, hedge, zero_division=0), cost])
dec = pd.DataFrame(rows, columns=["threshold", "share hedged", "recall (high-vol caught)", "precision", "total cost"]).round(3)
print("cost of never hedging:", (y_oos == 1).sum() * c_miss, "| cost of always hedging:", len(y_oos) * c_hedge)
dec
"""),
md("""
**🔍 CHECK.** Which threshold minimises cost? Does it change if `c_miss` is 2 instead of 4? Now the important question: *what KPI would you report to management for this system in production?* Accuracy is wrong (it does not price errors). Candidates: cost per week vs the always-hedge policy; recall at the chosen threshold; calibration (when the model says 70%, does it happen 70% of the time?). Pick one and defend it.
"""),
code("""
# Calibration: does p=0.7 mean 70%?
bins = pd.cut(oos, [0, .3, .4, .5, .6, .7, 1.0])
cal = pd.DataFrame({"predicted": oos.groupby(bins).mean(), "observed": y_oos.groupby(bins).mean(), "n": oos.groupby(bins).size()}).round(3)
cal
"""),
md("""
**Homework brief** → see `week-03/homework.md`.

**Vocabulary you now own:** feature, target, horizon, base rate, baseline, train/test, time-ordered split, walk-forward, leakage (through split and through features), accuracy vs AUC vs precision/recall, threshold, calibration, cost-weighted decision.
"""),
]

for week, cells in [("week-01", w1), ("week-02", w2), ("week-03", w3)]:
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["colab"] = {"provenance": [], "name": f"{week}_session.ipynb"}
    out = ROOT / week / "session.ipynb"; out.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, out); print("wrote", out)
