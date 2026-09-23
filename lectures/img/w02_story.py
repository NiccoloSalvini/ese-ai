"""Week 2 numbers, from the dated snapshots in week-02/data/.

Two threads, each built from one small example up:
  1. the model's side: how temperature reshapes the next-token probabilities
     from week 1, and what a tokenizer learns;
  2. the data side: "is Bitcoin riskier than the stock market, and does it
     move with it?" — ten real days by hand, then four and a half years.
Every number on the week 2 slides, figures and clips comes from here.
"""
import json, math
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE.parents[1] / "week-02" / "data"
PX = pd.read_csv(DATA / "btc_spy_2022-01-01_2026-09-18.csv", index_col=0, parse_dates=True)
Y10 = pd.read_csv(DATA / "dgs10_2022-01-01_2026-09-18.csv", index_col=0, parse_dates=True)["DGS10"]
OUT = {}

# ------------------------------------------------------------------ 1. temperature
# the week-1 table, closed over five candidate tokens
TOKENS = ["unchanged", "steady", "at", "on", "higher"]
P1 = np.array([0.62, 0.15, 0.10, 0.08, 0.05])
def at_temperature(p, T):
    if T == 0:
        q = np.zeros_like(p); q[np.argmax(p)] = 1; return q
    q = p ** (1 / T); return q / q.sum()
TEMPS = [0, 0.5, 1, 2]
OUT["temperature"] = dict(tokens=TOKENS, temps=TEMPS,
                          probs={str(T): [round(float(v), 3) for v in at_temperature(P1, T)] for T in TEMPS})
# by hand at T = 0.5: square every probability, divide by the new total
sq = P1 ** 2
OUT["temperature_hand"] = dict(squares=[round(float(v), 4) for v in sq], total=round(float(sq.sum()), 4),
                               result=[round(float(v), 2) for v in sq / sq.sum()])

# ------------------------------------------------------------------ 2. a tokenizer, learned by merging pairs
TEXT = ("the bank left rates unchanged. the bank said rates will stay unchanged. "
        "rates are high and the bank expects rates to stay high.")
def bpe(text, merges=8):
    seq = [c if c != " " else "_" for c in text]
    steps = []
    for _ in range(merges):
        pairs = Counter(zip(seq, seq[1:]))
        (a, b), n = max(pairs.items(), key=lambda kv: (kv[1], -list(pairs).index(kv[0])))
        if n < 2:
            break
        new, out, i = a + b, [], 0
        while i < len(seq):
            if i < len(seq) - 1 and seq[i] == a and seq[i + 1] == b:
                out.append(new); i += 2
            else:
                out.append(seq[i]); i += 1
        seq = out
        steps.append(dict(pair=[a, b], count=n, new=new, length=len(seq)))
    return steps, seq
steps, final = bpe(TEXT)
OUT["bpe"] = dict(text=TEXT, start=len(TEXT), steps=steps, final_len=len(final), pieces=final[:24])

# ------------------------------------------------------------------ 3. ten real days, by hand
ten = PX.loc["2024-01-05":"2024-01-16"].copy()
OUT["ten_days"] = [dict(date=d.strftime("%a %d %b"), btc=None if pd.isna(r["BTC-USD"]) else round(float(r["BTC-USD"]), 0),
                        spy=None if pd.isna(r["SPY"]) else round(float(r["SPY"]), 2)) for d, r in ten.iterrows()]
inner = ten.dropna()
OUT["ten_rows"] = dict(btc=int(ten["BTC-USD"].notna().sum()), spy=int(ten["SPY"].notna().sum()), both=len(inner))
fri, sun, mon = ten.loc["2024-01-05", "BTC-USD"], ten.loc["2024-01-07", "BTC-USD"], ten.loc["2024-01-08", "BTC-USD"]
OUT["monday"] = dict(fri=float(fri), sun=float(sun), mon=float(mon),
                     one_day=float(mon / sun - 1), three_days=float(mon / fri - 1))

# ------------------------------------------------------------------ 4. volatility: which constant?
r_btc = PX["BTC-USD"].pct_change().dropna()
r_spy = PX["SPY"].dropna().pct_change().dropna()
sd_btc, sd_spy = float(r_btc.std()), float(r_spy.std())
OUT["vol"] = dict(sd_btc=sd_btc, sd_spy=sd_spy, btc_365=sd_btc * math.sqrt(365), btc_252=sd_btc * math.sqrt(252),
                  spy_252=sd_spy * math.sqrt(252), understatement=1 - math.sqrt(252 / 365))

# ------------------------------------------------------------------ 5. compounding: add or multiply?
OUT["toy"] = dict(up=0.5, down=-0.5, added=0.0, compounded=(1.5 * 0.5) - 1)
y22 = PX.loc["2022", "BTC-USD"].dropna()
r22 = y22.pct_change().dropna()
OUT["btc2022"] = dict(first=float(y22.iloc[0]), last=float(y22.iloc[-1]), true=float(y22.iloc[-1] / y22.iloc[0] - 1),
                      added=float(r22.sum()), compounded=float((1 + r22).prod() - 1))

# ------------------------------------------------------------------ 6. calendars: which days exist?
both_eq = PX.dropna()                         # equity calendar
both_cr = PX.ffill().dropna()                 # crypto calendar: SPY carried over weekends
re_eq, re_cr = both_eq.pct_change().dropna(), both_cr.pct_change().dropna()
OUT["calendar"] = dict(rows_btc=int(PX["BTC-USD"].notna().sum()), rows_spy=int(PX["SPY"].notna().sum()),
                       rows_eq=len(both_eq), rows_cr=len(both_cr),
                       corr_eq=float(re_eq.corr().iloc[0, 1]), corr_cr=float(re_cr.corr().iloc[0, 1]),
                       spy_vol_eq=float(re_eq["SPY"].std() * math.sqrt(252)),
                       spy_vol_cr_252=float(re_cr["SPY"].std() * math.sqrt(252)),
                       spy_zero_days=int((re_cr["SPY"] == 0).sum()))

# ------------------------------------------------------------------ 7. units: percent or decimal?
j = both_eq.join(Y10, how="left")
j["DGS10"] = j["DGS10"].ffill()
wk = j.resample("W-FRI").last().dropna()
d_btc = wk["BTC-USD"].pct_change()
d_y_pct = wk["DGS10"].diff()                   # change in percentage points
d_y_dec = (wk["DGS10"] / 100).diff()          # the same change, as a decimal
ok = d_btc.notna() & d_y_pct.notna()
slope_pct = float(np.polyfit(d_y_pct[ok], d_btc[ok], 1)[0])
slope_dec = float(np.polyfit(d_y_dec[ok], d_btc[ok], 1)[0])
OUT["units"] = dict(y10_last=float(Y10.dropna().iloc[-1]), corr_pct=float(d_btc[ok].corr(d_y_pct[ok])),
                    corr_dec=float(d_btc[ok].corr(d_y_dec[ok])), slope_pct=slope_pct, slope_dec=slope_dec,
                    weeks=int(ok.sum()))
# compounding a return written in percent as if it were a decimal
OUT["units_toy"] = dict(pct=[1.2, -0.8, 0.5], right=float(np.prod([1.012, 0.992, 1.005]) - 1),
                        wrong=float(np.prod([1 + 1.2, 1 - 0.8, 1 + 0.5]) - 1))

OUT["snapshot"] = dict(file="btc_spy_2022-01-01_2026-09-18.csv", rows=len(PX),
                       first=str(PX.index.min().date()), last=str(PX.index.max().date()))

if __name__ == "__main__":
    t = OUT["temperature"]
    print("TEMPERATURE"); [print(f"  T={T}: {dict(zip(TOKENS, t['probs'][str(T)]))}") for T in TEMPS]
    print("  by hand T=0.5:", OUT["temperature_hand"])
    print("BPE", len(TEXT), "chars ->", OUT["bpe"]["final_len"], [(s['new'], s['count']) for s in steps])
    print("TEN DAYS rows", OUT["ten_rows"], "monday", {k: round(v, 4) for k, v in OUT["monday"].items()})
    print("VOL", {k: round(v, 4) for k, v in OUT["vol"].items()})
    print("TOY", OUT["toy"], "BTC 2022", {k: round(v, 4) for k, v in OUT["btc2022"].items()})
    print("CALENDAR", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in OUT["calendar"].items()})
    print("UNITS", {k: round(v, 4) if isinstance(v, float) else v for k, v in OUT["units"].items()}, OUT["units_toy"])
    (HERE / "w02_story.json").write_text(json.dumps(OUT, indent=1, default=str))
