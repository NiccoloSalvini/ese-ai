"""Generator for the course figures that carry numbers.

Pure diagrams (boxes and arrows) are hand-written SVG next to this file. Anything
with a curve, a coordinate or an arithmetic claim is generated here instead, so
the picture and the number cannot drift apart. Run: python3 lectures/img/figs.py
"""
import math, pathlib

HERE = pathlib.Path(__file__).parent
INK, MUTED, RULE, RED, GOLD, GOLDDK, NAVY, GREEN, SOFT = (
    "#363636", "#7a7f85", "#e6e2d8", "#AF1F25", "#CDBA80", "#a8955a",
    "#2471a3", "#1e8449", "#fcfbf8")
FONT = ("font-family=\"'Source Sans 3','Source Sans Pro',-apple-system,"
        "Helvetica,Arial,sans-serif\"")


def head(w, h, title, sub=None):
    """The slide heading is the figure's title, so the figure does not repeat it.

    `title` is kept in the call for readability — it says what the figure is —
    but only the subtitle is drawn, in the space the title used to occupy.
    """
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
         f'width="{w}" height="{h}" {FONT}>',
         f'  <rect width="{w}" height="{h}" fill="#ffffff"/>']
    if sub:
        s.append(f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>')
    return s


def write(name, parts):
    parts.append("</svg>")
    (HERE / name).write_text("\n".join(parts) + "\n")
    print("wrote", name)


class Axes:
    """Minimal linear mapper from data space to SVG space, y flipped."""
    def __init__(self, x0, x1, y0, y1, left, right, top, bottom):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.l, self.r, self.t, self.b = left, right, top, bottom

    def x(self, v): return self.l + (v - self.x0) / (self.x1 - self.x0) * (self.r - self.l)
    def y(self, v): return self.b - (v - self.y0) / (self.y1 - self.y0) * (self.b - self.t)
    def path(self, pts, **kw):
        d = " ".join(("M" if i == 0 else "L") + f"{self.x(a):.1f} {self.y(b):.1f}"
                     for i, (a, b) in enumerate(pts))
        attrs = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
        return f'  <path d="{d}" fill="none" {attrs}/>'
    def frame(self):
        return [f'  <line x1="{self.l}" y1="{self.t}" x2="{self.l}" y2="{self.b}" stroke="#c9c4b8"/>',
                f'  <line x1="{self.l}" y1="{self.b}" x2="{self.r}" y2="{self.b}" stroke="#c9c4b8"/>']


# ---------------------------------------------------------------- week 3
def threshold_ev():
    """Expected value against the acting threshold, for a fixed cost table.

    Scores are drawn once from two beta-ish populations so the curve has the
    shape a real sweep has; the optimum is then read off the curve, not asserted.
    """
    import random
    random.seed(7)
    N, BASE, GAIN, COST = 20000, 0.20, 400.0, 60.0
    pos = [min(0.999, random.betavariate(5, 3)) for _ in range(int(N * BASE))]
    neg = [min(0.999, random.betavariate(2, 8)) for _ in range(N - int(N * BASE))]
    taus = [i / 200 for i in range(201)]
    ev = []
    for t in taus:
        tp = sum(1 for p in pos if p >= t)
        fp = sum(1 for p in neg if p >= t)
        ev.append((tp * GAIN - fp * COST) / N)
    best = max(range(len(taus)), key=lambda i: ev[i])
    t_star, ev_star = taus[best], ev[best]
    ev_half = ev[taus.index(0.5)]
    lo, hi = min(ev), max(ev)
    pad = (hi - lo) * 0.12
    A = Axes(0, 1, lo - pad, hi + pad, 90, 640, 96, 300)

    s = head(960, 360, "A probability is not a decision. The costs choose the threshold.",
             f"gain on a true positive &#8364;{GAIN:.0f} &#183; cost of a false positive &#8364;{COST:.0f} "
             f"&#183; positives are {BASE:.0%} of the population")
    s += A.frame()
    s.append(f'  <line x1="{A.l}" y1="{A.y(0):.1f}" x2="{A.r}" y2="{A.y(0):.1f}" stroke="#c9c4b8" stroke-dasharray="3 3"/>')
    s.append(A.path(list(zip(taus, ev)), stroke=NAVY, stroke_width="3"))
    for t, v, col, lab in ((t_star, ev_star, GREEN, "the optimum"), (0.5, ev_half, RED, "the default")):
        s += [f'  <line x1="{A.x(t):.1f}" y1="{A.y(v):.1f}" x2="{A.x(t):.1f}" y2="{A.b}" stroke="{col}" stroke-dasharray="3 3"/>',
              f'  <circle cx="{A.x(t):.1f}" cy="{A.y(v):.1f}" r="6" fill="{col}"/>',
              f'  <text x="{A.x(t):.1f}" y="{A.b+20}" font-size="13" font-weight="700" fill="{col}" text-anchor="middle">{t:.2f}</text>',
              f'  <text x="{A.x(t):.1f}" y="{A.b+37}" font-size="12" fill="{col}" text-anchor="middle">{lab}</text>']
    s += [f'  <text x="{A.l}" y="{A.t-12}" font-size="12" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">EXPECTED VALUE PER TRANSACTION</text>',
          f'  <text x="{(A.l+A.r)/2:.0f}" y="{A.b+58}" font-size="13" fill="{MUTED}" text-anchor="middle">act when the predicted probability is at least this</text>',
          f'  <line x1="690" y1="80" x2="690" y2="330" stroke="{RULE}"/>',
          f'  <text x="716" y="120" font-size="15" font-weight="700" fill="{GREEN}">&#8364;{ev_star:.2f} at {t_star:.2f}</text>',
          f'  <text x="716" y="140" font-size="13" fill="{MUTED}">what the cost table says</text>',
          f'  <text x="716" y="184" font-size="15" font-weight="700" fill="{RED}">&#8364;{ev_half:.2f} at 0.50</text>',
          f'  <text x="716" y="204" font-size="13" fill="{MUTED}">what the library gives you</text>',
          f'  <text x="716" y="248" font-size="14" font-weight="700" fill="{INK}">&#8364;{ev_star-ev_half:.2f} per transaction,</text>',
          f'  <text x="716" y="267" font-size="14" font-weight="700" fill="{INK}">left on the table by a default.</text>',
          f'  <text x="716" y="300" font-size="13" fill="{MUTED}">The model is identical in both.</text>',
          f'  <text x="716" y="317" font-size="13" fill="{MUTED}">Only the cut-off moved.</text>']
    write("threshold-ev.svg", s)
    return t_star, ev_star, ev_half


# ---------------------------------------------------------------- week 8
def impermanent_loss():
    f = lambda r: 2 * math.sqrt(r) / (1 + r) - 1
    xs = [0.25 + i * (4.0 - 0.25) / 400 for i in range(401)]
    A = Axes(0.25, 4.0, -0.30, 0.02, 90, 600, 100, 290)
    s = head(960, 360, "Impermanent loss: always negative, in either direction",
             "value of the LP position against simply holding the two assets, as the price ratio r moves")
    s += A.frame()
    s.append(f'  <line x1="{A.l}" y1="{A.y(0):.1f}" x2="{A.r}" y2="{A.y(0):.1f}" stroke="#c9c4b8"/>')
    s.append(A.path([(x, f(x)) for x in xs], stroke=NAVY, stroke_width="3"))
    for r, lab in ((0.5, "price halves"), (1.0, "no move"), (2.0, "price doubles"), (4.0, "price 4&#215;")):
        v = f(r)
        col = GREEN if r == 1.0 else RED
        s += [f'  <circle cx="{A.x(r):.1f}" cy="{A.y(v):.1f}" r="5" fill="{col}"/>',
              f'  <text x="{A.x(r):.1f}" y="{A.y(v)-12:.1f}" font-size="13" font-weight="700" fill="{col}" text-anchor="middle">{v:+.2%}</text>',
              f'  <text x="{A.x(r):.1f}" y="{A.b+20:.0f}" font-size="12" fill="{MUTED}" text-anchor="middle">{lab}</text>']
    s += [f'  <text x="{A.l}" y="{A.t-14}" font-size="12" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">LP VALUE &#247; HOLD VALUE &#8722; 1</text>',
          f'  <text x="{(A.l+A.r)/2:.0f}" y="{A.b+48:.0f}" font-size="13" fill="{MUTED}" text-anchor="middle">r = the price now, divided by the price when you deposited</text>',
          f'  <line x1="648" y1="86" x2="648" y2="330" stroke="{RULE}"/>',
          f'  <text x="674" y="124" font-size="15" fill="{INK}">It is symmetric in log price:</text>',
          f'  <text x="674" y="146" font-size="15" font-weight="700" fill="{RED}">halving hurts as much as doubling.</text>',
          f'  <text x="674" y="190" font-size="15" fill="{INK}">The benchmark is <tspan font-weight="700">holding</tspan></text>',
          f'  <text x="674" y="210" font-size="15" fill="{INK}"><tspan font-weight="700">the two assets</tspan> &#8212; never your deposit.</text>',
          f'  <text x="674" y="248" font-size="13" fill="{MUTED}">An LP can be up in euros and still</text>',
          f'  <text x="674" y="265" font-size="13" fill="{MUTED}">have lost to doing nothing.</text>',
          f'  <text x="674" y="300" font-size="13" fill="{INK}">Fee income is the payment for</text>',
          f'  <text x="674" y="317" font-size="13" fill="{INK}">bearing this. Compare the two.</text>']
    write("impermanent-loss.svg", s)
    return [(r, f(r)) for r in (0.5, 1.0, 2.0, 4.0)]


# ---------------------------------------------------------------- week 8
def amm_three_prices():
    """The three prices are three slopes on one curve, so draw them as slopes."""
    X0, Y0, DX = 100.0, 6_000_000.0, 38.0
    k = X0 * Y0
    X1 = X0 - DX
    Y1 = k / X1
    paid = (Y1 - Y0) / DX
    p0, p1 = Y0 / X0, Y1 / X1
    xs = [50 + i * 0.5 for i in range(141)]
    A = Axes(50, 120, 4_500_000, 12_500_000, 140, 600, 100, 300)
    s = head(960, 370, "Three prices, and they are three slopes on one curve",
             f"a pool of {X0:.0f} ETH and {Y0:,.0f} USDC &#183; you buy {DX:.0f} ETH &#183; x &#183; y = k, and nothing else")
    s += A.frame()
    # guides and ticks, so the arithmetic is readable off the axes
    for val, lab, col in ((Y0, "6.00m", NAVY), (Y1, "9.68m", RED)):
        s += [f'  <line x1="{A.l}" y1="{A.y(val):.1f}" x2="{A.r}" y2="{A.y(val):.1f}" stroke="{col}" stroke-opacity="0.25" stroke-dasharray="3 3"/>',
              f'  <text x="{A.l-10}" y="{A.y(val)+5:.1f}" font-size="12" fill="{col}" text-anchor="end">{lab}</text>']
    for val, col in ((X0, NAVY), (X1, RED)):
        s += [f'  <line x1="{A.x(val):.1f}" y1="{A.t}" x2="{A.x(val):.1f}" y2="{A.b}" stroke="{col}" stroke-opacity="0.25" stroke-dasharray="3 3"/>',
              f'  <text x="{A.x(val):.1f}" y="{A.b+20}" font-size="12" fill="{col}" text-anchor="middle">{val:.0f}</text>']
    # tangents first, so the curve sits on top of them
    for xt, yt, sl, col, h in ((X0, Y0, -p0, NAVY, 26), (X1, Y1, -p1, RED, 13)):
        s.append(f'  <line x1="{A.x(xt-h):.1f}" y1="{A.y(yt-sl*h):.1f}" x2="{A.x(xt+h):.1f}" y2="{A.y(yt+sl*h):.1f}" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    s.append(A.path([(x, k / x) for x in xs], stroke=INK, stroke_width="2.5"))
    s.append(f'  <line x1="{A.x(X0):.1f}" y1="{A.y(Y0):.1f}" x2="{A.x(X1):.1f}" y2="{A.y(Y1):.1f}" stroke="{GOLDDK}" stroke-width="3.5"/>')
    s += [f'  <circle cx="{A.x(X0):.1f}" cy="{A.y(Y0):.1f}" r="6" fill="{NAVY}"/>',
          f'  <circle cx="{A.x(X1):.1f}" cy="{A.y(Y1):.1f}" r="6" fill="{RED}"/>',
          f'  <text x="{A.x(X0)+14:.1f}" y="{A.y(Y0)+6:.1f}" font-size="13" font-weight="700" fill="{NAVY}">before</text>',
          f'  <text x="{A.x(X1)+14:.1f}" y="{A.y(Y1)-10:.1f}" font-size="13" font-weight="700" fill="{RED}">after</text>',
          f'  <text x="{(A.l+A.r)/2:.0f}" y="{A.b+44:.0f}" font-size="13" fill="{MUTED}" text-anchor="middle">ETH in the pool</text>',
          f'  <text x="{A.l-50}" y="{A.t-14}" font-size="12" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">USDC IN THE POOL</text>',
          f'  <line x1="640" y1="86" x2="640" y2="346" stroke="{RULE}"/>',
          f'  <rect x="666" y="110" width="22" height="4" fill="{NAVY}"/>',
          f'  <text x="700" y="118" font-size="16" font-weight="700" fill="{NAVY}">{p0:,.0f}</text>',
          f'  <text x="700" y="137" font-size="13" fill="{MUTED}">pool price &#8212; the tangent before</text>',
          f'  <rect x="666" y="176" width="22" height="4" fill="{GOLDDK}"/>',
          f'  <text x="700" y="184" font-size="16" font-weight="700" fill="{GOLDDK}">{paid:,.0f}</text>',
          f'  <text x="700" y="203" font-size="13" fill="{MUTED}">what you paid &#8212; the chord</text>',
          f'  <rect x="666" y="242" width="22" height="4" fill="{RED}"/>',
          f'  <text x="700" y="250" font-size="16" font-weight="700" fill="{RED}">{p1:,.0f}</text>',
          f'  <text x="700" y="269" font-size="13" fill="{MUTED}">pool price &#8212; the tangent after</text>',
          f'  <text x="666" y="310" font-size="14" font-weight="700" fill="{INK}">You paid {paid/p0-1:.0%} over the price</text>',
          f'  <text x="666" y="329" font-size="14" font-weight="700" fill="{INK}">you saw. That is slippage,</text>',
          f'  <text x="666" y="348" font-size="14" font-weight="700" fill="{INK}">and it is not a fee.</text>']
    write("amm-three-prices.svg", s)
    return p0, paid, p1



# ---------------------------------------------------------------- week 7
def walk_forward():
    """One split against an expanding walk-forward, on the same timeline."""
    Y0, Y1 = 2018, 2025
    L, R = 150, 786
    px = lambda y: L + (y - Y0) / (Y1 - Y0) * (R - L)
    s = head(960, 380, "Walk-forward: the only honest home for a parameter search",
             "fit on a past window, test on the next one, roll forward &#8212; and never look back")
    s += [f'  <text x="30" y="96" font-size="11" font-weight="700" letter-spacing="1.3" fill="{GOLDDK}">ONE SPLIT</text>']
    s += [f'  <rect x="{px(2018):.0f}" y="104" width="{px(2023)-px(2018):.0f}" height="30" fill="{NAVY}" fill-opacity="0.85"/>',
          f'  <text x="{(px(2018)+px(2023))/2:.0f}" y="124" font-size="13" fill="#ffffff" text-anchor="middle">fit</text>',
          f'  <rect x="{px(2023):.0f}" y="104" width="{px(2025)-px(2023):.0f}" height="30" fill="{GOLDDK}" fill-opacity="0.9"/>',
          f'  <text x="{(px(2023)+px(2025))/2:.0f}" y="124" font-size="13" fill="#ffffff" text-anchor="middle">test</text>',
          f'  <text x="{R+14}" y="117" font-size="13" fill="{RED}">one number, from</text>',
          f'  <text x="{R+14}" y="134" font-size="13" fill="{RED}">one period</text>']
    s += [f'  <text x="30" y="188" font-size="11" font-weight="700" letter-spacing="1.3" fill="{GOLDDK}">WALK-FORWARD</text>']
    folds = [(2018, 2021, 2022), (2018, 2022, 2023), (2018, 2023, 2024), (2018, 2024, 2025)]
    for i, (a, b, c) in enumerate(folds):
        y = 196 + i * 40
        s += [f'  <rect x="{px(a):.0f}" y="{y}" width="{px(b)-px(a):.0f}" height="28" fill="{NAVY}" fill-opacity="0.85"/>',
              f'  <text x="{(px(a)+px(b))/2:.0f}" y="{y+19}" font-size="12" fill="#ffffff" text-anchor="middle">fit</text>',
              f'  <rect x="{px(b):.0f}" y="{y}" width="{px(c)-px(b):.0f}" height="28" fill="{GOLDDK}" fill-opacity="0.9"/>',
              f'  <text x="{(px(b)+px(c))/2:.0f}" y="{y+19}" font-size="12" fill="#ffffff" text-anchor="middle">test</text>',
              f'  <text x="120" y="{y+19}" font-size="12" fill="{MUTED}" text-anchor="end">fold {i+1}</text>']
    for yr in range(Y0, Y1 + 1):
        s.append(f'  <text x="{px(yr):.0f}" y="376" font-size="12" fill="{MUTED}" text-anchor="middle">{yr}</text>')
    s.append(f'  <line x1="{L}" y1="356" x2="{R}" y2="356" stroke="#c9c4b8"/>')
    s.append(f'  <text x="{R+14}" y="262" font-size="13" font-weight="700" fill="{GREEN}">four out-of-sample</text>')
    s.append(f'  <text x="{R+14}" y="280" font-size="13" font-weight="700" fill="{GREEN}">numbers, and the</text>')
    s.append(f'  <text x="{R+14}" y="298" font-size="13" font-weight="700" fill="{GREEN}">spread between them</text>')
    write("walk-forward.svg", s)


# ---------------------------------------------------------------- week 6
def confusion_costs():
    """A fraud matrix at one threshold, with the accuracy trap made arithmetic."""
    N, RATE = 1_000_000, 0.005
    fraud, legit = int(N * RATE), N - int(N * RATE)
    recall, fpr = 0.70, 0.01
    tp = int(fraud * recall); fn = fraud - tp
    fp = int(legit * fpr);    tn = legit - fp
    precision = tp / (tp + fp)
    acc = (tp + tn) / N
    acc_nothing = legit / N
    CONTACT, TICKET = 8.0, 220.0
    cost = fp * CONTACT + fn * TICKET

    X, Y, W, H = 200, 120, 190, 74
    # (column, row): column 0 is "flagged", row 0 is "fraud" — so a false positive
    # is a legitimate transaction that got flagged, and sits at (0, 1).
    cells = [(0, 0, tp, "caught", GREEN), (1, 0, fn, "missed fraud", RED),
             (0, 1, fp, "blocked a good customer", RED), (1, 1, tn, "let through, correctly", MUTED)]
    s = head(960, 420, "99.5% accurate, and useless &#8212; the arithmetic",
             f"{N:,} transactions &#183; fraud is {RATE:.1%} of them &#183; one threshold, one matrix")
    s += [f'  <text x="{X+W}" y="{Y-34}" font-size="11" font-weight="700" letter-spacing="1.3" fill="{GOLDDK}" text-anchor="middle">WHAT THE MODEL SAID</text>',
          f'  <text x="{X+W/2:.0f}" y="{Y-12}" font-size="13" fill="{MUTED}" text-anchor="middle">flagged</text>',
          f'  <text x="{X+W*1.5:.0f}" y="{Y-12}" font-size="13" fill="{MUTED}" text-anchor="middle">not flagged</text>',
          f'  <text x="{X-14}" y="{Y+42}" font-size="13" fill="{MUTED}" text-anchor="end">fraud</text>',
          f'  <text x="{X-14}" y="{Y+H+42}" font-size="13" fill="{MUTED}" text-anchor="end">legitimate</text>']
    for col, row, n, lab, c in cells:
        x, y = X + col * W, Y + row * H
        s += [f'  <rect x="{x}" y="{y}" width="{W}" height="{H}" fill="{c}" fill-opacity="0.09" stroke="{c}"/>',
              f'  <text x="{x+W/2:.0f}" y="{y+34}" font-size="19" font-weight="700" fill="{c}" text-anchor="middle">{n:,}</text>',
              f'  <text x="{x+W/2:.0f}" y="{y+55}" font-size="12" fill="{c}" text-anchor="middle">{lab}</text>']
    rows = [(f"precision {precision:.1%}", "of what we flagged, this much really was fraud"),
            (f"recall {recall:.0%}", "of the fraud out there, this much we caught"),
            (f"false positive rate {fpr:.0%}", f"of the good customers, {fp:,} people blocked")]
    for j, (bold, hint) in enumerate(rows):
        yy = Y + 2 * H + 36 + j * 44
        s += [f'  <text x="{X}" y="{yy}" font-size="15" font-weight="700" fill="{INK}">{bold}</text>',
              f'  <text x="{X}" y="{yy+18}" font-size="12" fill="{MUTED}">{hint}</text>']
    s += [
          f'  <line x1="620" y1="86" x2="620" y2="404" stroke="{RULE}"/>',
          f'  <text x="648" y="124" font-size="11" font-weight="700" letter-spacing="1.3" fill="{GOLDDK}">THE ACCURACY TRAP</text>',
          f'  <text x="648" y="152" font-size="15" fill="{INK}">this model &#160;<tspan font-weight="700">{acc:.2%}</tspan></text>',
          f'  <text x="648" y="176" font-size="15" fill="{RED}">flag nothing at all &#160;<tspan font-weight="700">{acc_nothing:.2%}</tspan></text>',
          f'  <text x="648" y="202" font-size="13" fill="{MUTED}">The useless model scores higher.</text>',
          f'  <text x="648" y="248" font-size="11" font-weight="700" letter-spacing="1.3" fill="{GOLDDK}">WHAT IT COSTS, IN EUROS</text>',
          f'  <text x="648" y="276" font-size="14" fill="{INK}">{fp:,} &#215; &#8364;{CONTACT:.0f} contact &#160;=&#160; &#8364;{fp*CONTACT:,.0f}</text>',
          f'  <text x="648" y="298" font-size="14" fill="{INK}">{fn:,} &#215; &#8364;{TICKET:.0f} missed &#160;=&#160; &#8364;{fn*TICKET:,.0f}</text>',
          f'  <line x1="648" y1="312" x2="920" y2="312" stroke="#c9c4b8"/>',
          f'  <text x="648" y="336" font-size="16" font-weight="700" fill="{RED}">&#8364;{cost:,.0f}</text>',
          f'  <text x="648" y="362" font-size="13" fill="{MUTED}">Sweep the threshold and minimise</text>',
          f'  <text x="648" y="379" font-size="13" fill="{MUTED}">this number. Not the accuracy.</text>']
    write("confusion-costs.svg", s)
    return precision, acc, acc_nothing, cost


# ---------------------------------------------------------------- week 10
def latency_budget():
    parts = [("retrieval", 120, NAVY), ("time to first token", 400, GOLDDK),
             ("generation, 200 tokens at 80 tok/s", 2500, RED), ("your own code", 180, MUTED)]
    total = sum(p[1] for p in parts)
    TARGET = 2000
    L, R = 40, 920
    scale = (R - L) / 3600
    s = head(960, 330, "A latency budget is a sum, and it either fits or it does not",
             "measured, not felt &#8212; and stated against a target you set before you built it")
    x = L; y = 110
    for lab, ms, col in parts:
        w = ms * scale
        s += [f'  <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="46" fill="{col}" fill-opacity="0.9"/>']
        if w > 60:
            s.append(f'  <text x="{x+w/2:.1f}" y="{y+29}" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">{ms} ms</text>')
        x += w
    lx = L
    for i, (lab, ms, col) in enumerate(parts):
        w = ms * scale
        ly = 182 + (i % 2) * 22
        s.append(f'  <text x="{lx+w/2:.1f}" y="{ly}" font-size="12" fill="{col}" text-anchor="middle">{lab}</text>')
        lx += w
    s += [f'  <line x1="{L+TARGET*scale:.1f}" y1="92" x2="{L+TARGET*scale:.1f}" y2="170" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>',
          f'  <text x="{L+TARGET*scale:.1f}" y="86" font-size="13" font-weight="700" fill="{INK}" text-anchor="middle">target {TARGET} ms</text>',
          f'  <text x="{L+total*scale+10:.1f}" y="139" font-size="15" font-weight="700" fill="{RED}">{total:,} ms</text>',
          f'  <text x="40" y="250" font-size="16" font-weight="700" fill="{RED}">Over budget by {total-TARGET:,} ms, and {parts[2][1]/total:.0%} of it is one thing.</text>',
          f'  <text x="40" y="278" font-size="14" fill="{INK}">Cut the answer to 80 tokens and generation falls to 1,000 ms: <tspan font-weight="700" fill="{GREEN}">1,700 ms, inside the target</tspan>.</text>',
          f'  <text x="40" y="304" font-size="14" fill="{MUTED}">Which is a product decision about how long an answer should be &#8212; not an engineering one.</text>']
    write("latency-budget.svg", s)
    return total


# ---------------------------------------------------------------- week 4
def ai_act_tiers():
    tiers = [("PROHIBITED", "social scoring, some biometrics",
              ["not deployable at all"], RED, 200),
             ("HIGH-RISK", "credit scoring, employment, essential services",
              ["conformity assessment, documentation,", "human oversight"], "#d35400", 344),
             ("TRANSPARENCY", "chatbots, synthetic media",
              ["people must be told"], GOLDDK, 488),
             ("MINIMAL", "everything else, which is most things",
              ["no specific obligation"], GREEN, 640)]
    s = head(960, 450, "The EU AI Act regulates the use, not the technology",
             "the same model sits in a different tier depending on what you point it at")
    y = 92
    for name, examples, duty, col, w in tiers:
        x = 40 + (640 - w) / 2
        s += [f'  <rect x="{x:.0f}" y="{y}" width="{w}" height="58" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-width="2"/>',
              f'  <text x="{x+w/2:.0f}" y="{y+24}" font-size="14" font-weight="700" letter-spacing="1.1" fill="{col}" text-anchor="middle">{name}</text>',
              f'  <text x="{x+w/2:.0f}" y="{y+45}" font-size="12" fill="{col}" text-anchor="middle">{examples}</text>']
        for j, line in enumerate(duty):
            dy = y + (29 if len(duty) == 1 else 22) + j * 17
            s.append(f'  <text x="700" y="{dy}" font-size="12" fill="{MUTED}">{line}</text>')
        y += 68
    s += [f'  <text x="40" y="{y+28}" font-size="15" font-weight="700" fill="{INK}">A CV screener and a recipe generator are different risk classes of the same technology.</text>',
          f'  <text x="40" y="{y+56}" font-size="14" fill="{INK}">And the word that decides who is liable: a <tspan font-weight="700" fill="{RED}">provider</tspan> puts it on the market under their own name;</text>',
          f'  <text x="40" y="{y+76}" font-size="14" fill="{INK}">a <tspan font-weight="700" fill="{NAVY}">deployer</tspan> uses it under theirs. Fine-tune an open model, put your logo on it, and you may have become the provider.</text>']
    write("ai-act-tiers.svg", s)


# ---------------------------------------------------------------- week 9
def risk_canvas():
    boxes = [("purpose", "one sentence, and who signed it"),
             ("users", "named, and what they did before"),
             ("data", "the source, the licence, the snapshot"),
             ("failure modes", "the red-team log, by outcome"),
             ("controls", "a validation gate, one per failure"),
             ("monitoring", "monitor.py, 2&#963; on feature means"),
             ("human oversight", "who reviews, on what sample"),
             ("kill-switch", "who stops it, and the date tested"),
             ("audit log", "what is written, and by whom")]
    s = head(960, 434, "The risk and controls canvas &#8212; nine boxes, every one a specific noun",
             "each box names a file, a cell, a function or a person. Nothing in a box may be a verb phrase.")
    W, H, X, Y = 288, 86, 30, 86
    for i, (name, hint) in enumerate(boxes):
        x, y = X + (i % 3) * (W + 8), Y + (i // 3) * (H + 8)
        s += [f'  <rect x="{x}" y="{y}" width="{W}" height="{H}" fill="{SOFT}" stroke="#c9c4b8"/>',
              f'  <text x="{x+16}" y="{y+32}" font-size="15" font-weight="700" fill="{INK}">{name}</text>',
              f'  <text x="{x+16}" y="{y+58}" font-size="12" fill="{MUTED}">{hint}</text>']
    s += [f'  <text x="30" y="398" font-size="14" fill="{INK}">&#8220;We will monitor for drift&#8221; is not a control.</text>',
          f'  <text x="30" y="420" font-size="14" font-weight="700" fill="{RED}">&#8220;monitor.py compares this week&#8217;s feature means against the training window and emails me above 2&#963;&#8221; is.</text>']
    write("risk-canvas.svg", s)



# ---------------------------------------------------------------- week 1
def software_123():
    """Three ways to write the same decision, and what each one costs you.

    The frame is Karpathy's; the worked example is the one this course keeps
    coming back to — block this transaction, or do not.

    Written twice: once complete, and once as four transparent layers on the
    same 960x440 grid, so the deck can reveal a column at a time inside an
    `.r-stack`. The layers carry no background rect — the slide is the canvas.
    """
    cols = [
        ("SOFTWARE 1.0", "rules, since 1950", MUTED,
         ["if amount > 150", "and country != home:", "    block()"], True,
         [("you write", "the logic itself"),
          ("it fails when", "the fraud is new"),
          ("you debug it by", "reading the code"),
          ("you can always say", "exactly why")]),
        ("SOFTWARE 2.0", "learned, since 2010", NAVY,
         ["fit(features, labels)", "p = model(transaction)", "if p > t: block()"], True,
         [("you write", "the data and the target"),
          ("it fails when", "tomorrow stops looking like yesterday"),
          ("you debug it by", "auditing the data and the split"),
          ("you give up", "being able to read why")]),
        ("SOFTWARE 3.0", "prompted, since 2023", RED,
         ["\u201cHere is the transaction", "and the customer\u2019s history.", "Block it? And why?\u201d"], False,
         [("you write", "the instruction, in English"),
          ("it fails when", "the answer is fluent and invented"),
          ("you debug it by", "checking the output against the source"),
          ("you give up", "reproducibility, unless you pin T=0")]),
    ]
    X, W, GAP = 36, 288, 12

    def column(i):
        name, era, col, code, mono, rows = cols[i]
        x = X + i * (W + GAP)
        out = [f'  <text x="{x}" y="80" font-size="13" font-weight="700" letter-spacing="1.2" fill="{col}">{name}</text>',
               f'  <text x="{x}" y="99" font-size="12" fill="{MUTED}">{era}</text>',
               f'  <rect x="{x}" y="112" width="{W}" height="76" fill="{col}" fill-opacity="0.08" stroke="{col}"/>']
        fam = ' font-family="\'JetBrains Mono\',Menlo,monospace"' if mono else ''
        for j, line in enumerate(code):
            out.append(f'  <text x="{x+14}" y="{135+j*21}" font-size="{12 if mono else 13}" fill="{col}"{fam}>{line}</text>')
        for j, (k, v) in enumerate(rows):
            yy = 214 + j * 50
            out += [f'  <text x="{x}" y="{yy}" font-size="11" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">{k.upper()}</text>',
                    f'  <text x="{x}" y="{yy+19}" font-size="13" fill="{INK}">{v}</text>']
        return out

    footer = [f'  <line x1="{X}" y1="418" x2="924" y2="418" stroke="{RULE}"/>',
              f'  <text x="{X}" y="436" font-size="13" fill="{INK}">You build <tspan font-weight="700" fill="{NAVY}">2.0 in week 3</tspan>, <tspan font-weight="700" fill="{RED}">3.0 in weeks 4 and 5</tspan>, and in week 6 you decide which of the three a problem actually needs.</text>']

    full = head(960, 440, "Software 1.0, 2.0, 3.0",
                "the same decision &#8212; block this transaction, or do not &#8212; written three ways")
    for i in range(3):
        full += column(i)
    write("software-123.svg", full + footer)

    # the same grid, as reveal layers
    def layer(name, body, background):
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" '
             f'width="960" height="440" {FONT}>']
        if background:
            s.append('  <rect width="960" height="440" fill="#ffffff"/>')
        write(name, s + body)

    layer("software-123-l0.svg",
          [f'  <text x="30" y="34" font-size="13" fill="{MUTED}">the same decision &#8212; block this transaction, or do not &#8212; written three ways</text>',
           f'  <text x="924" y="34" font-size="12" fill="{MUTED}" text-anchor="end">frame: Andrej Karpathy</text>'],
          background=True)
    for i in range(3):
        layer(f"software-123-l{i+1}.svg", column(i), background=False)
    layer("software-123-l4.svg", footer, background=False)


# ---------------------------------------------------------------- week 10
def cost_quality():
    """The chart that picks a model. Axes and rule are stable; the dots are not."""
    # (label, cost, score, colour, dx, dy, anchor) — offsets are hand-placed
    # because five labels round five dots collide in every automatic scheme.
    pts = [("a small model",           0.10, 0.58, MUTED,  14,   5, "start"),
           ("a mid model",             0.45, 0.74, NAVY,    0, -16, "middle"),
           ("a frontier model",        2.20, 0.86, RED,   -14,  -8, "end"),
           ("frontier, long context",  6.00, 0.87, RED,     0,  26, "middle"),
           ("an older frontier model", 1.60, 0.70, MUTED,  16,  -8, "start")]
    import math
    A = Axes(math.log10(0.05), math.log10(10.0), 0.50, 0.95, 120, 600, 96, 300)
    s = head(960, 370, "Choosing a model is a chart, not an opinion",
             "your evaluation score against your measured cost per query &#8212; one dot per candidate")
    s += A.frame()
    for v in (0.1, 1.0, 10.0):
        s.append(f'  <text x="{A.x(math.log10(v)):.1f}" y="{A.b+20}" font-size="12" fill="{MUTED}" text-anchor="middle">&#8364;{v:g}</text>')
    for v in (0.6, 0.7, 0.8, 0.9):
        s.append(f'  <text x="{A.l-10}" y="{A.y(v)+5:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{v:.1f}</text>')
    # the frontier: the upper-left envelope
    front = [p for p in pts if p[0] in ("a small model", "a mid model", "a frontier model")]
    s.append(A.path([(math.log10(p[1]), p[2]) for p in front], stroke=GREEN, stroke_width="2.5", stroke_dasharray="6 4"))
    for lab, c, q, col, dx, dy, anc in pts:
        dominated = lab in ("frontier, long context", "an older frontier model")
        s += [f'  <circle cx="{A.x(math.log10(c)):.1f}" cy="{A.y(q):.1f}" r="7" fill="{col}" fill-opacity="{0.3 if dominated else 1}" stroke="{col}" stroke-width="2"/>',
              f'  <text x="{A.x(math.log10(c))+dx:.1f}" y="{A.y(q)+dy:.1f}" font-size="12" fill="{col}" text-anchor="{anc}">{lab}</text>']
    s += [f'  <text x="{A.l}" y="{A.t-14}" font-size="12" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">YOUR EVAL SCORE</text>',
          f'  <text x="{(A.l+A.r)/2:.0f}" y="{A.b+44}" font-size="13" fill="{MUTED}" text-anchor="middle">cost per query, log scale</text>',
          f'  <text x="{A.x(math.log10(2.6)):.0f}" y="{A.y(0.655):.0f}" font-size="12" font-style="italic" fill="{MUTED}" text-anchor="middle">dominated</text>',
          f'  <line x1="640" y1="82" x2="640" y2="346" stroke="{RULE}"/>',
          f'  <text x="666" y="120" font-size="15" font-weight="700" fill="{GREEN}">The frontier is the only</text>',
          f'  <text x="666" y="140" font-size="15" font-weight="700" fill="{GREEN}">shortlist.</text>',
          f'  <text x="666" y="166" font-size="13" fill="{MUTED}">Anything below and to the right of</text>',
          f'  <text x="666" y="183" font-size="13" fill="{MUTED}">it is dominated: you are paying more</text>',
          f'  <text x="666" y="200" font-size="13" fill="{MUTED}">for less. Drop it without debate.</text>',
          f'  <text x="666" y="240" font-size="15" font-weight="700" fill="{INK}">Then routing moves you</text>',
          f'  <text x="666" y="260" font-size="15" font-weight="700" fill="{INK}">along the dashed line.</text>',
          f'  <text x="666" y="286" font-size="13" fill="{MUTED}">Easy queries small, hard ones large:</text>',
          f'  <text x="666" y="303" font-size="13" fill="{MUTED}">the cost becomes a weighted average,</text>',
          f'  <text x="666" y="320" font-size="13" fill="{MUTED}">and whether quality survives is a</text>',
          f'  <text x="666" y="337" font-size="13" fill="{MUTED}">question for your evals, not a vendor.</text>']
    write("cost-quality.svg", s)


if __name__ == "__main__":
    print("threshold:", threshold_ev())
    print("IL:", impermanent_loss())
    print("AMM:", amm_three_prices())
    walk_forward()
    print("fraud:", confusion_costs())
    print("latency:", latency_budget())
    ai_act_tiers()
    risk_canvas()
    software_123()
    cost_quality()
