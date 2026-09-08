"""Builds week-08/session.ipynb with nbformat (same style as build_nbs_weeks1-3.py)."""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

# --- course helper, reused verbatim from build_nbs_weeks1-3.py ---
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

LLM = r'''
# --- course helper: one LLM wrapper, guarded. If no key -> deterministic MOCK so the notebook runs end-to-end. ---
import os, json, re

API_KEY = None
try:
    from google.colab import userdata
    API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    API_KEY = os.environ.get("GEMINI_API_KEY")

MOCK_MODE = not bool(API_KEY)
if MOCK_MODE:
    print("No GEMINI_API_KEY found -> llm() runs in MOCK mode (fixed, deterministic answers; labelled as such).")

def _mock(prompt, json_schema):
    """Fixed answers so every cell below runs offline. The mock summary deliberately contains one wrong number
    (80% instead of 79.5%) so that the source-check cell has something to catch."""
    p = prompt.lower()
    if json_schema is not None and "mica" in p:
        return {"classifications": [
            {"asset": "USDC", "mica_category": "EMT", "reason": "references one fiat currency 1:1; issuer must be a credit institution or EMI"},
            {"asset": "stETH", "mica_category": "other crypto-asset", "reason": "not a stablecoin; represents staked ETH plus rewards; issued by a protocol"},
            {"asset": "UNI", "mica_category": "other crypto-asset", "reason": "governance token, no claim on assets, no reference to fiat"}]}
    if "governance" in p or "proposal" in p:
        return ("[MOCK] The proposal raises the wstETH loan-to-value on Aave v3 Ethereum from 78.5% to 80% and the "
                "liquidation threshold from 81% to 82%, keeps the liquidation bonus at 6%, and raises the supply cap "
                "to 1.2M wstETH. Risk provider Chaos Labs supports it; the vote closes on 20 November 2026.")
    return "[MOCK] no canned answer for this prompt."

def llm(prompt, system=None, json_schema=None, temperature=0):
    """Single entry point for LLM calls. Returns text, or a dict when json_schema is given.
    Ports to any provider: only this function changes."""
    if MOCK_MODE:
        return _mock(prompt, json_schema)
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=API_KEY)
    cfg = dict(temperature=temperature, system_instruction=system)
    if json_schema is not None:
        cfg.update(response_mime_type="application/json", response_schema=json_schema)
    r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,
                                       config=types.GenerateContentConfig(**cfg))
    return json.loads(r.text) if json_schema is not None else r.text.strip()

print("llm() ready —", "MOCK" if MOCK_MODE else "live Gemini")
'''

cells = [
md("""
# Week 8 — Digital assets, on-chain data and DeFi
**ESE · AI for Business and FinTech · 16 November 2026**

Today the working object is a *protocol*: a program that holds money and follows rules anyone can read. We simulate the most important one (a constant-product market maker) from its one equation, then read real protocol data through public APIs, then look at a protocol through a risk canvas and through MiCA.

Every number on the whiteboard today gets recomputed here. Cells marked **🔍 CHECK** contain assistant-style code with a planted error: find it before opening the solution.
"""),
code("!pip -q install yfinance google-genai"),
code(UTILS),
code(LLM),

# =====================================================================
md("## Block B — Lab 1: a constant-product pool from one equation"),
md("""
A pool holds two reserves, `x` (say ETH) and `y` (say USDC). The rule is that a swap must leave the product **x · y = k** unchanged (before fees). Everything else — price, slippage, LP returns — follows from that one line.

Spot price of x in units of y: **p = y / x**. A trader who puts in `dx` gets out `dy = y − k / (x + dx)`. The fee (0.3% on Uniswap v2-style pools) is taken on the way in and stays in the pool, which is how LPs earn.
""" ),
code("""
class Pool:
    \"\"\"Constant-product AMM (x*y = k) with a fee on input, Uniswap-v2 style.\"\"\"
    def __init__(self, x, y, fee=0.003):
        self.x, self.y, self.fee = float(x), float(y), fee
    @property
    def price(self):            # y per 1 x  (e.g. USDC per ETH)
        return self.y / self.x
    @property
    def k(self):
        return self.x * self.y
    def quote_x_for_y(self, dx):
        \"\"\"How much y you get for dx of x, without changing the pool.\"\"\"
        dx_net = dx * (1 - self.fee)
        return self.y - self.k / (self.x + dx_net)
    def swap_x_for_y(self, dx):
        dy = self.quote_x_for_y(dx)
        self.x += dx; self.y -= dy          # the full dx enters the pool: k grows by the fee
        return dy

pool = Pool(x=1_000, y=3_000_000)           # 1,000 ETH and 3,000,000 USDC -> spot 3,000 USDC/ETH
print("spot price:", pool.price, "| k:", f"{pool.k:.3e}")
"""),
md("""
**🔍 CHECK (bet 1).** You sell **100 ETH** (10% of the pool's ETH reserve). Before running: what price per ETH do you actually receive versus the spot 3,000, and where is the pool price *after* the trade? Write both numbers down.
"""),
code("""
dx = 100
dy = pool.quote_x_for_y(dx)
exec_price = dy / dx
p_after = (pool.y - dy) / (pool.x + dx)
print(f"received {dy:,.0f} USDC for {dx} ETH -> execution price {exec_price:,.1f}  ({exec_price/pool.price-1:+.2%} vs spot)")
print(f"pool price after the trade: {p_after:,.1f}  ({p_after/pool.price-1:+.2%} vs spot)")
"""),
md("""
Two different numbers, both called "price impact" in conversation. Execution price ≈ p·x/(x+dx) → about −9% for a 10% trade; pool price after ≈ p·x²/(x+dx)² → about −17%. Neither is a fee: the pool simply *has* fewer USDC per ETH left. The curve is the market maker.
"""),
code("""
import matplotlib.pyplot as plt
sizes = np.array([0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50])
rows = []
for s in sizes:
    dx = s * pool.x; dy = pool.quote_x_for_y(dx)
    rows.append([s, dy/dx, dy/dx/pool.price - 1, (pool.y-dy)/(pool.x+dx)/pool.price - 1])
impact = pd.DataFrame(rows, columns=["trade / reserve", "execution price", "exec vs spot", "pool price after vs spot"])
display(impact.round(4))
impact.set_index("trade / reserve")[["exec vs spot", "pool price after vs spot"]].plot(
    figsize=(8, 3.5), logx=True, marker="o", title="Price impact vs trade size (share of the x reserve)")
plt.axhline(0, color="k", lw=0.5); plt.ylabel("vs spot"); plt.show()
"""),
md("""
### 🔍 CHECK — the assistant's swap function
Asked to "write a function that swaps ETH for USDC in a constant-product pool with a 0.3% fee", the assistant produced the cell below. It runs and prints numbers. **It contains two errors.** Compare its answers with the `Pool` class above for the same 100 ETH trade before opening the solution.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
def swap_assistant(x, y, dx, fee=0.3):
    price = y / x
    dy = dx * price * (1 - fee)        # output at the current price, minus the fee
    return dy, (y - dy) / (x + dx)     # amount out, new pool price

for dx in [1, 100, 500]:
    dy, p_new = swap_assistant(1_000, 3_000_000, dx)
    print(f"sell {dx:>3} ETH -> {dy:,.0f} USDC | execution {dy/dx:,.1f} | pool price after {p_new:,.1f}")
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **`dy = dx * price`** is a linear quote: it ignores the curve. Selling 500 ETH gets you 500 × 3,000 = 1.5M USDC minus fee, whatever the reserve — so the execution price never moves, slippage is zero, and the pool would go *negative* on a large enough trade. The correct output is `y - k/(x + dx_net)`: the pool keeps `x·y = k`, so every unit you sell is priced a little lower than the last. The "pool price after" it prints only looks reasonable because it is computed from wrong `dy`.
2. **`fee=0.3`** is 30%, not 0.3%. Percent vs decimal — the same silent error as the week-2 FRED yields. With a 30% fee the 1-ETH trade returns 2,100 USDC instead of ~2,991.

Rule: whenever a function returns money, test it on a trade of size 0 (must return 0) and on a trade the size of the whole reserve (must not drain the pool).
</details>
"""),
code("""
# Corrected version — same signature, curve respected, fee as a decimal
def swap(x, y, dx, fee=0.003):
    k = x * y
    dx_net = dx * (1 - fee)
    dy = y - k / (x + dx_net)
    return dy, (y - dy) / (x + dx)

for dx in [0, 1, 100, 500, 100_000]:
    dy, p_new = swap(1_000, 3_000_000, dx)
    print(f"sell {dx:>7,} ETH -> {dy:>12,.0f} USDC | pool price after {p_new:,.1f} | pool never below 0 USDC: {3_000_000 - dy > 0}")
"""),

md("""
### LP value vs holding
An LP deposits both assets and owns a share of the pool. When the price moves, arbitrageurs trade against the pool until its price matches the market — and that rebalancing sells the LP's winner and buys the loser. So the LP's position is worth **less than simply holding the two coins**, by an amount that depends only on the price ratio `r = p_now / p_deposit`:

$$\\frac{\\text{LP value}}{\\text{hold value}} = \\frac{2\\sqrt{r}}{1 + r}$$

That gap is called *impermanent loss* (a bad name: it is a real loss unless the price returns). Fees are what the LP is paid to bear it.
"""),
md("""
**🔍 CHECK (bet 2).** ETH doubles (`r = 2`). Before running: by what percentage is the LP position worth less than just holding? Write the number.
"""),
code("""
def lp_vs_hold(r):
    \"\"\"Value of a constant-product LP position divided by the value of holding the deposited coins, for price ratio r.\"\"\"
    return 2 * np.sqrt(r) / (1 + r)

# Same thing computed the long way, from the pool, so the formula is not taken on faith
x0, y0 = 1_000, 3_000_000; p0 = y0 / x0; k = x0 * y0
r = 2.0; p1 = p0 * r
x1, y1 = np.sqrt(k / p1), np.sqrt(k * p1)          # reserves after arbitrage brings the pool price to p1
lp_value = y1 + x1 * p1                            # in USDC
hold_value = y0 + x0 * p1
print(f"price 2x: LP value {lp_value:,.0f} | hold value {hold_value:,.0f} | LP/hold {lp_value/hold_value:.4f} | formula {lp_vs_hold(r):.4f}")
print(f"impermanent loss at 2x: {lp_vs_hold(r)-1:+.2%}")
"""),
md("""
### 🔍 CHECK — the assistant's impermanent-loss curve
Asked to "plot impermanent loss as a function of the price ratio", the assistant wrote the cell below. It plots a smooth curve. Compare the value at `r = 2` with the number you just computed.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
ratios = np.linspace(0.2, 5, 200)
x0, y0 = 1_000, 3_000_000; k = x0 * y0; p0 = y0 / x0
initial_value = y0 + x0 * p0
il_assistant = []
for r in ratios:
    p = p0 * r
    lp_value = np.sqrt(k / p) * p + np.sqrt(k * p)     # value of the rebalanced reserves at the new price
    il_assistant.append(lp_value / initial_value - 1)
il_assistant = pd.Series(il_assistant, index=ratios)
print("assistant's 'impermanent loss' at r=2:", f"{il_assistant.loc[2.0] if 2.0 in il_assistant.index else np.interp(2.0, ratios, il_assistant.values):+.2%}")
il_assistant.plot(figsize=(8, 3.5), title="Impermanent loss vs price ratio (assistant version)"); plt.axhline(0, color="k", lw=0.5); plt.show()
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

The benchmark is wrong. The assistant divides by the **initial** value of the deposit, so at `r = 2` it reports **+41%** — the LP made money, and the chart shows a "loss" that is positive whenever price goes up. Impermanent loss is defined **against holding the same coins**: at `r = 2` holding is worth 1.5× the initial value, the LP position 1.414×, and the loss is 1.414/1.5 − 1 = **−5.7%**. Same LP value, different denominator, opposite conclusion.

This is the general form of the bug: a return is always *relative to something*; the assistant picks the denominator that is easiest to code. Ask "compared to what?" for every percentage a model or a person gives you.
</details>
"""),
code("""
# Corrected: benchmark = holding the deposited coins at the new price
il = pd.Series([lp_vs_hold(r) - 1 for r in ratios], index=ratios)
table = pd.DataFrame({"price ratio r": [0.25, 0.5, 0.8, 1.0, 1.25, 2, 3, 4, 5]})
table["LP / hold"] = lp_vs_hold(table["price ratio r"]).round(4)
table["impermanent loss"] = (table["LP / hold"] - 1).map("{:+.2%}".format)
display(table)
il.plot(figsize=(8, 3.5), title="Impermanent loss vs price ratio (vs holding)"); plt.axhline(0, color="k", lw=0.5); plt.ylabel("LP/hold − 1"); plt.show()
"""),

md("""
### Fee income vs impermanent loss
Fees are the other side of the ledger. If the pool turns over a fraction `v` of its reserves every day at fee `f`, the LP earns roughly `f · v · 365` per year on the pool's value. Whether providing liquidity beats holding is then a race between that yield and the impermanent loss the price path produces.
"""),
md("""
**🔍 CHECK (bet 3, sign only).** Daily volume equal to 20% of pool value, 0.3% fee, held for one year, and ETH ends the year at 2×. Before running: does the LP finish ahead of or behind holding? Write **+** or **−**.
"""),
code("""
fee, days = 0.003, 365
vol_over_tvl = np.array([0.02, 0.05, 0.10, 0.20, 0.50, 1.00])     # daily volume as a share of pool value
fee_yield = fee * vol_over_tvl * days                              # annual fee income as share of pool value
fees = pd.DataFrame({"daily volume / TVL": vol_over_tvl, "annual fee yield": fee_yield})
for r in [1.25, 2, 3]:
    fees[f"net vs hold @ {r}x"] = fee_yield + (lp_vs_hold(r) - 1)
display(fees.set_index("daily volume / TVL").apply(lambda col: col.map("{:+.1%}".format)))
print("break-even daily volume/TVL to cover IL at 2x:", f"{-(lp_vs_hold(2)-1) / (fee * days):.3f}")
"""),
md("""
### LP on a real price path
The curve above assumes a single jump. On a real path the LP position is marked every day: `Pool` reserves follow the price, fees accrue with assumed volume. We use ETH-USD from the course loader (live → snapshot → synthetic). *If the loader printed `[SYNTHETIC]`, the path below is a random walk and the numbers are only a pipeline test.*
"""),
code("""
px = load_prices(["ETH-USD"], start="2022-01-01").ffill().dropna()
eth = px["ETH-USD"]
p0 = eth.iloc[0]
x0 = 1.0; y0 = x0 * p0                     # deposit 1 ETH and the same value in USDC
k = x0 * y0
r_path = eth / p0
lp = pd.DataFrame(index=eth.index)
lp["hold"] = y0 + x0 * eth                             # value in USDC of holding the deposit
lp["lp_no_fees"] = 2 * np.sqrt(k * eth)                # value of the rebalanced reserves at each price
lp["il"] = lp["lp_no_fees"] / lp["hold"] - 1
vol_over_tvl = 0.20                                    # assumption — replace with pool data in the homework
lp["fees_cum"] = (fee * vol_over_tvl * lp["lp_no_fees"]).cumsum()
lp["lp_with_fees"] = lp["lp_no_fees"] + lp["fees_cum"]
print(f"deposit {p0:,.0f} USDC/ETH -> today {eth.iloc[-1]:,.0f} (r = {r_path.iloc[-1]:.2f})")
print(f"hold {lp['hold'].iloc[-1]:,.0f} | LP no fees {lp['lp_no_fees'].iloc[-1]:,.0f} (IL {lp['il'].iloc[-1]:+.1%}) | LP with fees {lp['lp_with_fees'].iloc[-1]:,.0f}")
lp[["hold", "lp_no_fees", "lp_with_fees"]].plot(figsize=(10, 4), title="1 ETH + USDC: hold vs LP (constant product), fees at assumed 20%/day volume/TVL"); plt.ylabel("USDC"); plt.show()
"""),
md("""
**🔍 CHECK.** The fee line depends entirely on the `vol_over_tvl` assumption. Change it to 0.05 and to 0.50 and see when the LP crosses hold. The honest version of this chart needs the pool's *actual* volume, which is what the DefiLlama block gives you next.
"""),

# =====================================================================
md("## Block C — Lab 2: protocol data through public APIs"),
md("""
DefiLlama aggregates on-chain data per protocol: **TVL** (value locked), **fees** (what users pay) and **revenue** (the part the protocol or its token keeps; the rest goes to LPs, stakers or validators). CoinGecko gives token price and market cap. Both are free and need no key. Both go through the same three-tier loader: live → dated snapshot in `data/` → a small **SYNTHETIC** table labelled as such.
"""),
code("""
import requests, glob, datetime as dt

SLUGS = {"uniswap": "uniswap", "aave": "aave", "lido": "lido-dao"}      # DefiLlama slug -> CoinGecko id
def _get(url, timeout=15):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "ese-course"}); r.raise_for_status(); return r.json()

def load_protocol_metrics(slugs=SLUGS, cache_dir="data"):
    os.makedirs(cache_dir, exist_ok=True)
    stamp = dt.date.today().isoformat()
    snap = f"{cache_dir}/protocol_metrics_{stamp}.csv"
    try:
        rows = []
        for slug, cg in slugs.items():
            tvl = _get(f"https://api.llama.fi/tvl/{slug}")
            fees = _get(f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyFees")
            rev = _get(f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyRevenue")
            rows.append(dict(protocol=slug, tvl=float(tvl), fees_30d=fees.get("total30d"), revenue_30d=rev.get("total30d")))
        m = pd.DataFrame(rows).set_index("protocol")
        cg = _get("https://api.coingecko.com/api/v3/simple/price?ids=" + ",".join(slugs.values()) + "&vs_currencies=usd&include_market_cap=true")
        m["price"] = [cg[c]["usd"] for c in slugs.values()]
        m["market_cap"] = [cg[c]["usd_market_cap"] for c in slugs.values()]
        m["source"] = "live " + stamp
        m.to_csv(snap); print("[live] DefiLlama + CoinGecko; snapshot saved to", snap); return m
    except Exception as e:
        print("[warn] live fetch failed:", type(e).__name__)
    snaps = sorted(glob.glob(f"{cache_dir}/protocol_metrics_*.csv"))
    if snaps:
        m = pd.read_csv(snaps[-1], index_col=0); print("[snapshot]", snaps[-1]); return m
    print("[SYNTHETIC] illustrative order-of-magnitude numbers, NOT real data — do not quote them.")
    m = pd.DataFrame({
        "tvl":         [4.5e9, 25e9, 28e9],
        "fees_30d":    [80e6, 55e6, 90e6],
        "revenue_30d": [6e6, 9e6, 9e6],
        "price":       [8.0, 230.0, 1.10],
        "market_cap":  [5.0e9, 3.5e9, 1.0e9],
    }, index=pd.Index(list(slugs), name="protocol"))
    m["source"] = "SYNTHETIC"
    return m

metrics = load_protocol_metrics()
metrics
"""),
md("""
**🔍 CHECK (bet 4).** Three protocols, three business models: an exchange (Uniswap), a lender (Aave), a staking service (Lido). Before running: which has the highest **annualised fees / TVL**, and which the highest **revenue / market cap**? Write the two names.
"""),
code("""
m = metrics.copy()
m["fees_annual"] = m["fees_30d"] * 12
m["revenue_annual"] = m["revenue_30d"] * 12
m["fees / TVL"] = m["fees_annual"] / m["tvl"]
m["revenue / TVL"] = m["revenue_annual"] / m["tvl"]
m["revenue / mcap"] = m["revenue_annual"] / m["market_cap"]
m["take rate (rev/fees)"] = m["revenue_annual"] / m["fees_annual"]
out = m[["tvl", "fees_annual", "revenue_annual", "market_cap", "fees / TVL", "revenue / TVL", "revenue / mcap", "take rate (rev/fees)"]]
display(out.style.format({"tvl": "{:,.0f}", "fees_annual": "{:,.0f}", "revenue_annual": "{:,.0f}", "market_cap": "{:,.0f}",
                          "fees / TVL": "{:.1%}", "revenue / TVL": "{:.2%}", "revenue / mcap": "{:.1%}", "take rate (rev/fees)": "{:.0%}"}))
print("source:", metrics["source"].iloc[0])
"""),
md("""
Read the ratios as a PM would read a SaaS dashboard: **fees/TVL** is asset turnover (how hard the capital works), **take rate** is what the protocol keeps of what users pay, **revenue/mcap** is the inverse of a price-to-sales multiple. An exchange turns its capital over daily; a lender or a staking service earns a spread on capital that sits. The ratios differ by an order of magnitude *because the businesses differ*, not because one is "better".
"""),
md("""
### TVL concentration
How concentrated is DeFi? The whole protocol list from DefiLlama, or a labelled synthetic list.
"""),
code("""
def load_tvl_table(cache_dir="data"):
    os.makedirs(cache_dir, exist_ok=True)
    stamp = dt.date.today().isoformat(); snap = f"{cache_dir}/defillama_protocols_{stamp}.csv"
    try:
        js = _get("https://api.llama.fi/protocols")
        t = pd.DataFrame([{"name": p["name"], "category": p.get("category"), "tvl": p.get("tvl") or 0} for p in js])
        t = t[t["tvl"] > 0].sort_values("tvl", ascending=False).reset_index(drop=True)
        t.to_csv(snap, index=False); print("[live] DefiLlama /protocols:", len(t), "protocols; snapshot", snap); return t, "live"
    except Exception as e:
        print("[warn] DefiLlama /protocols failed:", type(e).__name__)
    snaps = sorted(glob.glob(f"{cache_dir}/defillama_protocols_*.csv"))
    if snaps:
        print("[snapshot]", snaps[-1]); return pd.read_csv(snaps[-1]), "snapshot"
    print("[SYNTHETIC] illustrative list, NOT real data.")
    t = pd.DataFrame({"name": ["Lido", "Aave", "EigenLayer", "ether.fi", "Sky", "Binance staked ETH", "Ethena", "Uniswap", "Morpho",
                               "Pendle", "Spark", "Rocket Pool", "Compound", "Curve", "Jito"] + [f"protocol_{i}" for i in range(16, 216)],
                      "tvl": [28e9, 25e9, 12e9, 8e9, 6e9, 6e9, 5e9, 4.5e9, 4e9, 4e9, 3e9, 3e9, 2.5e9, 2e9, 2e9]
                             + list(np.round(1.5e9 * 0.97 ** np.arange(200), 0))})
    t["category"] = "n/a"
    return t.sort_values("tvl", ascending=False).reset_index(drop=True), "SYNTHETIC"

tvl_table, tvl_source = load_tvl_table()
total = tvl_table["tvl"].sum()
share = tvl_table["tvl"] / total
hhi = (share ** 2).sum()
print(f"[{tvl_source}] {len(tvl_table)} protocols | total TVL {total/1e9:,.1f}B | top-5 share {share.head(5).sum():.1%} | top-10 share {share.head(10).sum():.1%} | HHI {hhi:.3f}")
tvl_table.head(10).assign(share=share.head(10).map("{:.1%}".format))
"""),
md("""
**🔍 CHECK (bet 5).** You wrote a top-10 share before running. Now the interpretive question: DefiLlama counts the same ETH once in Lido (staked) and again in Aave if the stETH is deposited as collateral. Is the concentration you see over- or under-stated by that double counting? (Look for a `category` column: liquid staking and restaking are the layers most exposed to it.)
"""),

md("""
### Reading a governance proposal with the LLM, then checking it against the source
Protocol parameters (collateral ratios, caps, fees) are changed by governance votes. The texts are long and full of numbers. An LLM summary is useful **only** with a mechanical check that every number in the summary exists in the source. `llm()` is mocked if no key; the mock deliberately contains one wrong number so the check has something to catch.
"""),
code("""
proposal = \"\"\"
AIP-412 — Risk parameter update for wstETH on Aave v3 Ethereum (Chaos Labs)

Summary. We propose to increase the loan-to-value (LTV) of wstETH from 78.5% to 79.5% and the liquidation threshold
from 81% to 82%, reflecting deeper wstETH/ETH liquidity on-chain and lower realised volatility of the stETH/ETH rate
over the last 180 days. The liquidation bonus remains at 6%. We also propose raising the wstETH supply cap from 1.0M
to 1.2M wstETH, given current utilisation of 91% of the cap.

Risk analysis. The stETH/ETH secondary-market discount has stayed within 0.3% for 180 days. Under a 10% ETH price
shock with a simultaneous 2% stETH discount, simulated bad debt is below 50k USD. The oracle remains the Chainlink
wstETH/ETH × ETH/USD feed. Recommended: ARFC forum discussion closes 13 November 2026; on-chain vote closes
20 November 2026.
\"\"\"
summary = llm("Summarise this governance proposal in three sentences, keeping every parameter change with its old and new value.\\n\\n" + proposal,
              system="You are a DeFi risk analyst. Be precise; never invent numbers.")
print(summary)
"""),
code("""
def numbers_in(text):
    \"\"\"All numeric tokens (with %, k, M) in a text, normalised as strings.\"\"\"
    return set(re.findall(r"\\d+(?:[.,]\\d+)?", text))

src, summ = numbers_in(proposal), numbers_in(summary)
unsupported = sorted(summ - src)
print("numbers in summary:", sorted(summ))
print("NOT in source (possible hallucination):", unsupported if unsupported else "none")
missing = {"79.5", "82", "6", "1.2"} - summ
print("parameter values missing from the summary:", sorted(missing) if missing else "none")
"""),
md("""
**🔍 CHECK.** The check catches a number that is in the summary but not in the source. What does it *not* catch? (Two kinds of error survive it: a source number attached to the wrong parameter, and a correct number with the wrong direction — "from 80% to 78.5%".) A number check is necessary, not sufficient — the same lesson as the RAG evals in week 4.
"""),

# =====================================================================
md("## Block D — Protocol risk canvas"),
md("""
Five lenses, one protocol. The table below is a template: fill it for **one** protocol from the metrics table above (or your capstone protocol). Each cell must be a sentence with a fact you can point to (a contract audit date, an oracle name, a governance quorum, a peg history), not an adjective.
"""),
code("""
canvas = pd.DataFrame({
    "lens":      ["smart-contract", "oracle", "governance", "depeg / collateral", "liquidity"],
    "question":  ["Can the code lose the money? (audits, upgradeability, admin keys, bug history)",
                  "Where does the protocol get prices from, and what happens if that source is wrong for 10 minutes?",
                  "Who can change the parameters, how fast, and what is the quorum?",
                  "What backs the assets in the pool, and what breaks if the backing trades at a discount?",
                  "If 20% of TVL leaves today, does the protocol keep working?"],
    "what I found": ["", "", "", "", ""],
    "severity 1-5": [None] * 5,
    "evidence (link / number)": ["", "", "", "", ""],
})
canvas.set_index("lens")
"""),
md("""
Historical cases, one line each, are on the card; the exercise is to place each case in a row of this table. Every big DeFi loss fits one row — and most fit two, because an oracle failure is usually exploited through a lending contract, and a depeg becomes a liquidity crisis.
"""),

# =====================================================================
md("## Block E — MiCA in practice (regulation slot)"),
md("""
Reading and prompts are in `notes.md`. Here, one structured LLM call classifies three assets under MiCA. The output is a *hypothesis*: check each line against the reading before accepting it. (Mocked without a key.)
"""),
code("""
schema = {"type": "object", "properties": {"classifications": {"type": "array", "items": {"type": "object",
          "properties": {"asset": {"type": "string"}, "mica_category": {"type": "string", "enum": ["ART", "EMT", "other crypto-asset", "out of scope"]},
                         "reason": {"type": "string"}}, "required": ["asset", "mica_category", "reason"]}}}, "required": ["classifications"]}
res = llm("Classify USDC, stETH and UNI under MiCA (Regulation (EU) 2023/1114): ART, EMT, other crypto-asset, or out of scope. One-line reason each.",
          system="You are an EU financial-regulation analyst.", json_schema=schema)
pd.DataFrame(res["classifications"]).set_index("asset")
"""),
md("""
**🔍 CHECK.** For each line: which MiCA article or definition supports the category? If you cannot name one from the reading, the classification is not yet yours. Then the harder question for stETH: is the *token* the regulated object, or is it the *service* (staking on behalf of clients) that a CASP would need authorisation for?
"""),

# =====================================================================
md("## Take-home (write three lines)"),
md("""
_Three things you did not know at 09:00 and now can compute. Then `File ▸ Save a copy in GitHub` → `week-08/session.ipynb`._

1.
2.
3.

**Homework brief** → see `week-08/homework.md`.

**Vocabulary you now own:** ledger, wallet = key, transaction, block, gas, stablecoin (ART/EMT), smart contract, constant-product AMM, spot vs execution price, price impact, impermanent loss (vs holding), fee yield, TVL, fees vs revenue, take rate, concentration (HHI), oracle, governance, depeg, CASP.
"""),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["colab"] = {"provenance": [], "name": "week-08_session.ipynb"}
out = ROOT / "session.ipynb"
nbf.write(nb, out); print("wrote", out, "|", sum(c.cell_type == "code" for c in cells), "code cells")
