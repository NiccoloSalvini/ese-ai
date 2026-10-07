"""Week 3 figures. Every number is computed here from the week-03 price snapshot,
with the same code as week-03/session.ipynb, and written to w03_story.json.
Run:  python figs_w03.py   (needs pandas, numpy, scikit-learn)."""
import json
from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
PX = pd.read_csv(HERE.parents[1] / "week-03" / "data" / "prices_BTC-USD_ETH-USD_SPY.csv", index_col=0, parse_dates=True)
PX = PX.loc[:"2026-10-06"]
RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE, PAPER = (
    "#AF1F25", "#CDBA80", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8", "#f7f5ef")
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',Helvetica,Arial,sans-serif\""


def svg(name, w, h, body, sub):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
         f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>'] + body + ['</svg>']
    (HERE / name).write_text("\n".join(s), encoding="utf-8")
    print("wrote", name)


def t(x, y, s, size=15, fill=INK, weight="400", anchor="start"):
    return f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def line(x1, y1, x2, y2, col=RULE, w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'


def rect(x, y, w, h, col, op=1.0):
    return f'  <rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" fill="{col}" fill-opacity="{op}"/>'


def num(v, d=2):
    return f"{v:.{d}f}".replace("-", "−")


# ================================================================== the numbers (same code as the notebook)
ret = np.log(PX / PX.shift(1))
btc = ret["BTC-USD"].dropna()
S = {"first": str(PX.index[0].date()), "last": str(PX.index[-1].date())}

z = (btc - btc.mean()) / btc.std()
S["tails"] = [{"k": k, "btc": int((z.abs() > k).sum()), "normal": (1 - erf(k / sqrt(2))) * len(z)} for k in (3, 4, 5)]
S["years"] = round(len(btc) / 365.25, 1)

lags = list(range(1, 31))
S["ac_dir"] = [btc.autocorr(k) for k in lags]
S["ac_size"] = [btc.abs().autocorr(k) for k in lags]
spy = ret["SPY"].dropna()
S["ac_size_spy1"] = spy.abs().autocorr(1)

vol30 = (ret["BTC-USD"].rolling(30).std() * np.sqrt(365)).dropna()
vol30m = vol30.resample("W").last()
S["vol30"] = {"dates": [str(d.date()) for d in vol30m.index], "v": vol30m.round(4).tolist()}

both = ret[["BTC-USD", "SPY"]].dropna()
rc = both["BTC-USD"].rolling(90).corr(both["SPY"])
S["corr_year"] = {str(k.year): round(v, 2) for k, v in rc.resample("YE").mean().items()}

simple = PX[["BTC-USD", "ETH-USD"]].pct_change().dropna()
S["check"] = {a: {"vol252": simple[a].std() * sqrt(252), "vol365": simple[a].std() * sqrt(365),
                  "sum": simple[a].sum(), "true": (1 + simple[a]).prod() - 1} for a in simple}

H = 7
d = pd.DataFrame({"ret": btc})
vol_7, vol_30 = d["ret"].rolling(7).std(), d["ret"].rolling(30).std()
usual = vol_7.rolling(365).median()
X = pd.DataFrame(index=d.index)
X["ret_1"] = d["ret"]; X["ret_7"] = d["ret"].rolling(7).sum(); X["ret_30"] = d["ret"].rolling(30).sum()
X["vol_7"] = vol_7 / usual; X["vol_30"] = vol_30 / usual; X["vol_ratio"] = vol_7 / vol_30
X["eth_ret_7"] = ret["ETH-USD"].rolling(7).sum().reindex(d.index)
X["spy_ret_5"] = ret["SPY"].ffill().rolling(5).sum().reindex(d.index)
X["weekday"] = d.index.dayofweek
fwd_ret = d["ret"][::-1].rolling(H).sum()[::-1].shift(-1)
fwd_vol = d["ret"][::-1].rolling(H).std()[::-1].shift(-1)
y = pd.DataFrame({"y_dir": (fwd_ret > 0).astype(int), "y_vol": (fwd_vol > usual).astype(int)}, index=d.index)
data = pd.concat([X, y, fwd_ret.rename("fwd_ret")], axis=1).dropna()
feats = list(X.columns)
train, test = data.loc[:"2023-12-31"], data.loc["2024-01-01":]
forest = lambda: RandomForestClassifier(n_estimators=300, min_samples_leaf=20, random_state=0, n_jobs=-1)
tr, te = train_test_split(data, test_size=0.3, random_state=0)
S["results"] = {}
for tg in ["y_dir", "y_vol"]:
    p = forest().fit(train[feats], train[tg]).predict_proba(test[feats])[:, 1]
    ps = forest().fit(tr[feats], tr[tg]).predict_proba(te[feats])[:, 1]
    S["results"][tg] = {"base": max(test[tg].mean(), 1 - test[tg].mean()),
                        "honest": roc_auc_score(test[tg], p), "shuffled": roc_auc_score(te[tg], ps)}
S["results"]["y_vol"]["rule"] = roc_auc_score(test["y_vol"], test["vol_7"])
rf = forest().fit(train[feats], train["y_vol"])
p_vol = rf.predict_proba(test[feats])[:, 1]
imp = permutation_importance(rf, test[feats], test["y_vol"], scoring="roc_auc", n_repeats=10, random_state=0)
S["importance"] = dict(sorted(zip(feats, imp.importances_mean.round(4)), key=lambda kv: -kv[1]))
Xl = data[feats].copy(); Xl["c"] = d["ret"].rolling(7, center=True).std().reindex(data.index); Xl = Xl.dropna()
yl = data.loc[Xl.index, "y_vol"]
S["leak_auc"] = roc_auc_score(yl.loc["2024":], forest().fit(Xl.loc[:"2023"], yl.loc[:"2023"]).predict_proba(Xl.loc["2024":])[:, 1])
yv = test["y_vol"].values
ths = np.round(np.arange(0.1, 0.81, 0.05), 2)
S["hedge"] = {str(cm): {"th": ths.tolist(),
                        "cost": [float((1 * (p_vol > th) + cm * ((p_vol <= th) & (yv == 1))).mean()) for th in ths],
                        "never": float(cm * yv.mean()), "always": 1.0} for cm in (2, 4)}
S["test_share_high"] = float(yv.mean())
(HERE / "w03_story.json").write_text(json.dumps(S, indent=1, default=float))


# ================================================================== figures
def tails():
    B, x0, base, top = [], 120, 360, 70
    mx = max(r["btc"] for r in S["tails"])
    sc = lambda v: (base - top) * min(v, mx) / mx
    for i, r in enumerate(S["tails"]):
        cx = x0 + i * 280
        hb, hn = sc(r["btc"]), sc(r["normal"])
        B += [rect(cx, base - hn, 90, hn, MUTED, 0.6), rect(cx + 100, base - hb, 90, hb, RED, 0.9),
              t(cx + 45, base - hn - 8, num(r["normal"], 1 if r["normal"] >= 0.1 else 3), 16, MUTED, "700", "middle"),
              t(cx + 145, base - hb - 8, str(r["btc"]), 20, RED, "700", "middle"),
              t(cx + 95, base + 26, f"beyond {r['k']} standard deviations", 15, INK, "700", "middle")]
    B += [line(90, base, 900, base, INK),
          rect(620, 64, 14, 14, MUTED, 0.6), t(640, 76, "if returns were normal", 14, MUTED),
          rect(620, 88, 14, 14, RED, 0.9), t(640, 100, "what Bitcoin did", 14, RED, "700"),
          t(30, 425, f"Days with a move beyond k standard deviations, in {len(btc):,} days of Bitcoin. The bell curve says a 4σ day is a once-in-40-years event.", 14, INK)]
    svg("w03-tails.svg", 960, 440, B, f"Bitcoin daily log returns, {S['first']} to {S['last']}")


def memory():
    B, x0, W = [], 250, 680
    bw = W / 30
    rows = [("direction", "return today vs return k days later", S["ac_dir"], NAVY, 150),
            ("size", "|return| today vs |return| k days later", S["ac_size"], RED, 340)]
    for lab, sub, vals, col, y0 in rows:
        sc = 500  # px per unit of correlation
        B += [t(30, y0 - 22, lab, 20, col, "700"), t(30, y0 - 2, sub.split(" vs ")[0] + " vs", 13, MUTED),
              t(30, y0 + 15, "the same, k days later", 13, MUTED), line(x0, y0, x0 + W, y0, INK)]
        for i, v in enumerate(vals):
            h = v * sc
            B.append(rect(x0 + i * bw + 3, y0 - max(h, 0), bw - 6, abs(h), col, 0.9))
        B += [line(x0, y0 - 0.1 * sc, x0 + W, y0 - 0.1 * sc, MUTED, 1, "3 3"), t(x0 + W + 8, y0 - 0.1 * sc + 4, "0.10", 11, MUTED),
              t(x0 + W + 8, y0 + 4, "0", 11, MUTED)]
    for k in (1, 5, 10, 15, 20, 25, 30):
        B.append(t(x0 + (k - 0.5) * bw, 362, str(k), 12, MUTED, "400", "middle"))
    B += [t(x0 + W / 2, 382, "lag k, in days", 13, MUTED, "400", "middle"),
          t(30, 420, f"0 means no memory. Direction hovers around 0 at every lag; size stays positive for a month (lag 1: {num(S['ac_size'][0])}).", 14, INK)]
    svg("w03-memory.svg", 960, 440, B, "autocorrelation of Bitcoin daily returns, lags 1 to 30 days")


def vol_chart():
    dates = pd.to_datetime(S["vol30"]["dates"]); v = np.array(S["vol30"]["v"])
    x0, W, y0, H = 80, 840, 60, 300
    hi = 2.0
    X = lambda dt: x0 + (dt - dates[0]).days / (dates[-1] - dates[0]).days * W
    Y = lambda val: y0 + H - min(val, hi) / hi * H
    B = []
    for g in (0.5, 1.0, 1.5, 2.0):
        B += [line(x0, Y(g), x0 + W, Y(g), RULE), t(x0 - 8, Y(g) + 4, f"{g:.0%}", 12, MUTED, "400", "end")]
    pts = " ".join(f"{X(dt):.1f},{Y(val):.1f}" for dt, val in zip(dates, v))
    B.append(f'  <polyline points="{pts}" fill="none" stroke="{RED}" stroke-width="2"/>')
    for yr in range(2018, 2027):
        dt = pd.Timestamp(f"{yr}-01-01")
        if dates[0] <= dt <= dates[-1]:
            B += [line(X(dt), y0 + H, X(dt), y0 + H + 5, MUTED), t(X(dt), y0 + H + 22, str(yr), 12, MUTED, "400", "middle")]
    B += [line(x0, y0 + H, x0 + W, y0 + H, INK),
          t(30, 420, "Calm stretches and storms, each lasting weeks or months. The level of today is the best single guess of the level next week.", 14, INK)]
    svg("w03-vol.svg", 960, 440, B, "Bitcoin, 30-day volatility, annualised (√365), weekly points")


def corr_chart():
    yrs = list(S["corr_year"].items())
    x0, base, Hh = 110, 330, 240
    bw = 780 / len(yrs)
    B = [line(x0 - 10, base, x0 + 790, base, INK)]
    for i, (yr, v) in enumerate(yrs):
        h = v / 0.7 * Hh
        col = RED if v == max(S["corr_year"].values()) else NAVY
        B += [rect(x0 + i * bw + 12, base - h, bw - 24, h, col, 0.9),
              t(x0 + i * bw + bw / 2, base - h - 8, num(v), 16, col, "700", "middle"),
              t(x0 + i * bw + bw / 2, base + 22, yr + ("*" if yr == "2026" else ""), 14, MUTED, "400", "middle")]
    B += [t(30, 400, "“Digital gold, uncorrelated with stocks” was roughly true until 2019. A correlation is a series, not a constant — it has regimes too.", 14, INK),
          t(30, 422, "* 2026 to date", 12, MUTED)]
    svg("w03-corr.svg", 960, 440, B, "Bitcoin vs S&amp;P 500 (SPY): 90-trading-day correlation of daily returns, yearly average")


def check_chart():
    c = S["check"]["BTC-USD"]
    rows = [("annual volatility", [("√252 — the assistant", c["vol252"], GOLDDK), ("√365 — crypto trades every day", c["vol365"], RED)], 1.0),
            ("total return since 2018", [("simple returns added up", c["sum"], GOLDDK), ("compounded — what really happened", c["true"], RED)], 6.0)]
    B, y = [], 70
    for title, bars, scale in rows:
        B.append(t(30, y + 10, title, 17, INK, "700"))
        for j, (lab, v, col) in enumerate(bars):
            yy = y + 26 + j * 46
            w = v / scale * 480
            B += [t(30, yy + 22, lab, 15, col, "700" if col == RED else "400"), rect(320, yy + 4, w, 28, col, 0.9 if col == RED else 0.5),
                  t(330 + w, yy + 25, f"{v:.0%}", 18, col, "700")]
        y += 160
    B.append(t(30, 410, f"Bitcoin, {S['first']} to {S['last']}. Two lines of code that run and look right; one makes it calmer, the other poorer, than it was.", 14, INK))
    svg("w03-check.svg", 960, 430, B, "the assistant’s summary table, and the corrected one")


def results_chart():
    r = S["results"]
    x0, W = 260, 620
    lo, hi = 0.4, 0.8
    X = lambda v: x0 + (v - lo) / (hi - lo) * W
    B = []
    for g in (0.4, 0.5, 0.6, 0.7, 0.8):
        B += [line(X(g), 70, X(g), 330, RULE if g != 0.5 else INK, 1 if g != 0.5 else 1.5, None if g != 0.5 else "4 3"),
              t(X(g), 352, num(g, 1), 13, MUTED, "400", "middle")]
    B.append(t(X(0.5), 372, "a coin", 13, INK, "700", "middle"))
    for i, (tg, lab) in enumerate([("y_dir", "up next week?"), ("y_vol", "more volatile than usual?")]):
        yy = 130 + i * 140
        B += [t(30, yy + 5, lab, 17, INK, "700")]
        marks = [("shuffled split", r[tg]["shuffled"], GOLDDK, False), ("forest, honest split", r[tg]["honest"], RED, True)]
        if "rule" in r[tg]:
            marks.append(("one-line rule", r[tg]["rule"], NAVY, True))
        for j, (ml, v, col, solid) in enumerate(marks):
            B.append(f'  <circle cx="{X(v):.1f}" cy="{yy:.1f}" r="10" fill="{col if solid else "white"}" stroke="{col}" stroke-width="3"/>')
            B.append(t(X(v), yy - 18 - (j % 2) * 0 , num(v), 15, col, "700", "middle"))
            B.append(t(X(v) + (14 if j == 2 else -14 if "rule" in str(marks) and j == 1 else 0), yy + 32,
                       ml, 12, col, "400", "start" if j == 2 else "end" if "rule" in str(marks) and j == 1 else "middle"))
    B.append(t(30, 410, "AUC on 2024 → today: does the model rank the 1s above the 0s? Hollow = the assistant’s shuffled split, which is a leak.", 14, INK))
    svg("w03-results.svg", 960, 430, B, "random forest, nine features, trained on 2019–2023")


def importance_chart():
    items = list(S["importance"].items())
    mx = max(abs(v) for _, v in items)
    x0, W = 330, 520
    zero = x0 + W * 0.25
    B, y = [line(zero, 60, zero, 60 + 32 * len(items), INK)], 60
    for f, v in items:
        w = v / mx * W * 0.7
        col = RED if v > 0.01 else (MUTED if v >= 0 else GOLDDK)
        B += [t(zero - 12 if v >= 0 else zero + w - 12, y + 19, f, 14, INK, "400", "end"),
              rect(min(zero, zero + w), y + 6, abs(w), 20, col, 0.9),
              t(zero + max(w, 0) + 8 if v >= 0 else zero + 8, y + 21, num(v, 3), 12, col, "700")]
        y += 32
    B.append(t(30, 400, "How much the AUC drops when one feature is scrambled. The volatility features and last week’s move carry it; below zero is noise.", 14, INK))
    svg("w03-importance.svg", 960, 420, B, "permutation importance, volatility target, test years 2024 → today")


def hedge_chart():
    x0, W, y0, Hh = 90, 560, 60, 300
    lo, hi = 0.8, 2.0
    X = lambda th: x0 + (th - 0.1) / 0.7 * W
    Y = lambda c: y0 + Hh - (min(c, hi) - lo) / (hi - lo) * Hh
    B = []
    for g in (0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0):
        B += [line(x0, Y(g), x0 + W, Y(g), RULE), t(x0 - 8, Y(g) + 4, num(g, 1), 12, MUTED, "400", "end")]
    for th in (0.1, 0.3, 0.5, 0.7):
        B.append(t(X(th), y0 + Hh + 20, num(th, 1), 12, MUTED, "400", "middle"))
    B.append(t(x0 + W / 2, y0 + Hh + 40, "hedge when the forest’s probability is above…", 13, MUTED, "400", "middle"))
    for cm, col in (("2", NAVY), ("4", RED)):
        h = S["hedge"][cm]
        pts = " ".join(f"{X(a):.1f},{Y(c):.1f}" for a, c in zip(h["th"], h["cost"]))
        B.append(f'  <polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>')
        i = int(np.argmin(h["cost"]))
        B.append(f'  <circle cx="{X(h["th"][i]):.1f}" cy="{Y(h["cost"][i]):.1f}" r="6" fill="{col}"/>')
        B.append(line(x0, Y(h["never"]), x0 + W, Y(h["never"]), col, 1.2, "5 4"))
    B.append(line(x0, Y(1.0), x0 + W, Y(1.0), INK, 1.5, "2 3"))
    h2, h4 = S["hedge"]["2"], S["hedge"]["4"]
    i2, i4 = int(np.argmin(h2["cost"])), int(np.argmin(h4["cost"]))
    B += [t(680, 90, "a miss costs 2", 16, NAVY, "700"),
          t(680, 112, f"best: {num(h2['cost'][i2])} per week at {num(h2['th'][i2], 2)}", 14, NAVY),
          t(680, 132, f"never hedge {num(h2['never'])} · always hedge 1.00", 14, NAVY),
          t(680, 152, "→ the model earns its keep", 14, NAVY, "700"),
          t(680, 200, "a miss costs 4", 16, RED, "700"),
          t(680, 222, f"best: {num(h4['cost'][i4])} per week at {num(h4['th'][i4], 2)}", 14, RED),
          t(680, 242, f"never hedge {num(h4['never'])} · always hedge 1.00", 14, RED),
          t(680, 262, "→ always hedge; switch the model off", 14, RED, "700"),
          t(680, 310, "dashed: never hedge · dotted: always hedge", 12, MUTED),
          t(30, 425, "Cost per week on 2024 → today, hedge = 1. Same forest, same probabilities: only the price of a miss changed.", 14, INK)]
    svg("w03-hedge.svg", 960, 440, B, "expected cost per week against the threshold, for two prices of a missed high-volatility week")


def llm_wall():
    x0, W = 60, 840
    yr = lambda y: x0 + (y - 2018) / (2027 - 2018) * W
    B = []
    for y in range(2018, 2028):
        B += [line(yr(y), 300, yr(y), 306, MUTED), t(yr(y), 324, str(y), 12, MUTED, "400", "middle")]
    B.append(line(x0, 300, x0 + W, 300, INK))
    B += [rect(yr(2019), 90, yr(2024) - yr(2019), 44, NAVY, 0.85), t((yr(2019) + yr(2024)) / 2, 117, "forest learns: 2019–2023", 15, "white", "700", "middle"),
          rect(yr(2024), 90, yr(2026.75) - yr(2024), 44, GOLD, 0.9), t((yr(2024) + yr(2026.75)) / 2, 117, "test: 2024 → today", 15, INK, "700", "middle"),
          line(yr(2024), 70, yr(2024), 290, RED, 3), t(yr(2024), 62, "the wall", 14, RED, "700", "middle"),
          rect(x0, 180, yr(2025.5) - x0, 44, RED, 0.18), t(x0 + 12, 207, "what an LLM read in training: the web, news, prices…", 15, RED, "700"),
          line(yr(2025.5), 170, yr(2025.5), 290, RED, 1.5, "5 4"), t(yr(2025.5) + 8, 246, "its cut-off", 13, RED, "400"),
          rect(yr(2024), 180, yr(2025.5) - yr(2024), 44, RED, 0.45),
          t(30, 380, "For the forest the wall holds by construction. For an LLM, every test date before its cut-off may already be in its memory:", 14, INK),
          t(30, 402, "tell it “Bitcoin, August 2024” and it may remember the week instead of forecasting it. Hide the name and the date.", 14, INK)]
    svg("w03-llm-wall.svg", 960, 420, B, "the same wall, seen from a language model (cut-off date illustrative)")


for f in (tails, memory, vol_chart, corr_chart, check_chart, results_chart, importance_chart, hedge_chart, llm_wall):
    f()
print(json.dumps({k: S[k] for k in ("tails", "results", "leak_auc", "corr_year")}, indent=1, default=float))
