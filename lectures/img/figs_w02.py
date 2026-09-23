"""Week 2 figures. Every number is read from w02_story.json (written by w02_story.py)."""
import json, math
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
S = json.loads((HERE / "w02_story.json").read_text())
PX = pd.read_csv(HERE.parents[1] / "week-02" / "data" / "btc_spy_2022-01-01_2026-09-18.csv", index_col=0, parse_dates=True)
RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE, PAPER = (
    "#AF1F25", "#CDBA80", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8", "#f7f5ef")
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',Helvetica,Arial,sans-serif\""


def svg(name, w, h, body, sub):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
         f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>'] + body + ['</svg>']
    (HERE / name).write_text("\n".join(s), encoding="utf-8")
    print("wrote", name)


def t(x, y, s, size=15, fill=INK, weight="400", anchor="start"):
    return f'  <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def pct(v, d=0):
    return f"{v*100:.{d}f}%".replace("-", "−")


# ------------------------------------------------------------------ volatility: which constant?
def vol():
    v = S["vol"]
    rows = [("Bitcoin, √365 — it trades every day", v["btc_365"], RED, True),
            ("Bitcoin, √252 — the assistant’s constant", v["btc_252"], GOLDDK, False),
            ("S&amp;P 500 (SPY), √252", v["spy_252"], NAVY, True)]
    B = []
    for i, (lab, val, col, ok) in enumerate(rows):
        y = 80 + i * 78
        w = val / 0.6 * 560
        B += [t(30, y + 22, lab, 16, INK, "700"),
              f'  <rect x="370" y="{y+2}" width="{w:.0f}" height="30" fill="{col}" fill-opacity="{0.9 if ok else 0.45}"/>',
              t(380 + w, y + 24, pct(val, 1), 18, col, "700")]
    B += [f'  <line x1="30" y1="330" x2="930" y2="330" stroke="{RULE}"/>',
          t(30, 358, f"daily standard deviation × √(trading days in a year). Same formula; the wrong constant makes Bitcoin look {pct(v['understatement'])} calmer.", 15, INK)]
    svg("w02-vol.svg", 960, 372, B, f"annualised volatility of daily returns, {S['snapshot']['first']} to {S['snapshot']['last']}")


# ------------------------------------------------------------------ compounding: Bitcoin in 2022, added vs multiplied
def compounding():
    s = PX.loc["2022", "BTC-USD"].dropna()
    r = s.pct_change().fillna(0)
    true = (1 + r).cumprod() - 1
    added = r.cumsum()
    x0, W, y0, H = 90, 800, 60, 260
    lo, hi = -1.0, 0.1
    X = lambda i: x0 + i / (len(s) - 1) * W
    Y = lambda v: y0 + (hi - v) / (hi - lo) * H
    B = [f'  <line x1="{x0}" y1="{Y(0):.1f}" x2="{x0+W}" y2="{Y(0):.1f}" stroke="{RULE}"/>']
    for v in (0, -0.25, -0.5, -0.75, -1.0):
        B.append(t(x0 - 10, Y(v) + 5, pct(v), 12, MUTED, "400", "end"))
    for series, col, lab in [(added, GOLDDK, "daily returns added up"), (true, RED, "compounded — what really happened")]:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(series.values))
        B.append(f'  <polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.6"/>')
        B.append(t(X(len(s) - 1) + 8, Y(series.values[-1]) + 5, f"{pct(series.values[-1])}", 16, col, "700"))
    B += [t(x0 + 10, Y(-0.93), "daily returns added up", 14, GOLDDK, "700"),
          t(x0 + 10, Y(-0.82), "compounded — what really happened", 14, RED, "700"),
          f'  <line x1="30" y1="345" x2="930" y2="345" stroke="{RULE}"/>',
          t(30, 372, f"From {S['btc2022']['first']:,.0f} to {S['btc2022']['last']:,.0f} dollars: the true loss is {pct(S['btc2022']['true'])}. Adding the daily returns says {pct(S['btc2022']['added'])}.", 15, INK)]
    svg("w02-compounding.svg", 960, 386, B, "Bitcoin, calendar year 2022 — cumulative return, two ways")


# ------------------------------------------------------------------ calendars: what filling the weekend does
def calendars():
    c = S["calendar"]
    B = []
    panels = [("rows", [("Bitcoin days", c["rows_btc"], MUTED), ("stock-market days", c["rows_spy"], NAVY),
                        ("equity calendar (drop weekends)", c["rows_eq"], GREEN), ("crypto calendar (fill weekends)", c["rows_cr"], GOLDDK)], 1800, "{:,.0f}"),
              ("S&amp;P 500 volatility", [("equity calendar", c["spy_vol_eq"], GREEN), ("crypto calendar", c["spy_vol_cr_252"], GOLDDK)], 0.2, "pct"),
              ("correlation BTC–S&amp;P", [("equity calendar", c["corr_eq"], GREEN), ("crypto calendar", c["corr_cr"], GOLDDK)], 0.5, "{:.2f}")]
    x = 30
    for title, bars, mx, fmt in panels:
        w_panel = 300
        B.append(t(x, 70, title, 16, INK, "700"))
        for i, (lab, val, col) in enumerate(bars):
            y = 90 + i * 52
            w = val / mx * 180
            txt = pct(val, 1) if fmt == "pct" else fmt.format(val)
            B += [t(x, y + 14, lab, 12, MUTED), f'  <rect x="{x}" y="{y+20}" width="{w:.0f}" height="18" fill="{col}"/>',
                  t(x + w + 6, y + 34, txt, 14, col, "700")]
        x += w_panel + 20
    B += [f'  <line x1="30" y1="315" x2="930" y2="315" stroke="{RULE}"/>',
          t(30, 342, f"Filling the weekend invents {c['spy_zero_days']} days on which the stock market ‘returned’ exactly zero.", 15, INK),
          t(30, 366, "It looks calmer and less connected to Bitcoin — because of days that never happened.", 15, INK)]
    svg("w02-calendars.svg", 960, 380, B, f"Bitcoin and the S&amp;P 500, {S['snapshot']['first']} to {S['snapshot']['last']}, joined two ways")


# ------------------------------------------------------------------ units: same correlation, slope off by 100
def units():
    u = S["units"]
    rows = [("yield change written in percentage points (0.25)", u["slope_pct"], u["corr_pct"]),
            ("the same change written as a decimal (0.0025)", u["slope_dec"], u["corr_dec"])]
    B = [t(560, 70, "correlation", 14, MUTED, "700", "middle"), t(780, 70, "slope", 14, MUTED, "700", "middle")]
    for i, (lab, sl, co) in enumerate(rows):
        y = 100 + i * 60
        B += [t(30, y + 20, lab, 16, INK), t(560, y + 20, f"{co:.3f}", 20, INK, "700", "middle"),
              t(780, y + 20, f"{sl:.2f}", 20, RED, "700", "middle"),
              f'  <line x1="30" y1="{y+38}" x2="930" y2="{y+38}" stroke="{RULE}"/>']
    B += [t(30, 262, f"Read literally: “a one-point rise in the 10-year yield moves Bitcoin by {u['slope_pct']*100:.0f}%” — or by {u['slope_dec']*100:.0f}%.", 15, INK),
          t(30, 286, "Same data, same code. The correlation cannot tell you anything is wrong; the slope silently changes by 100.", 15, INK, "700")]
    svg("w02-units.svg", 960, 300, B, f"weekly Bitcoin return against the weekly change in the US 10-year yield, {u['weeks']} weeks")


if __name__ == "__main__":
    vol(); compounding(); calendars(); units()
