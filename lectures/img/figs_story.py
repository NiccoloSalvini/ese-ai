"""Week 1 figures for the running example — "is this card payment fraud?".

Every number is read from nn_story.json (written by nn_story.py), so the
slides, the clips and the notebook show the same arithmetic.
"""
import json, math
from pathlib import Path

HERE = Path(__file__).parent
S = json.loads((HERE / "nn_story.json").read_text())
RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE, PAPER = (
    "#AF1F25", "#CDBA80", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8", "#f7f5ef")
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',Helvetica,Arial,sans-serif\""
MONO = "font-family=\"'JetBrains Mono',Menlo,monospace\""


def svg(name, w, h, body, sub):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
         f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>'] + body + ['</svg>']
    (HERE / name).write_text("\n".join(s), encoding="utf-8")
    print("wrote", name)


def t(x, y, s, size=15, fill=INK, weight="400", anchor="start", extra=""):
    return f'  <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


def box(x, y, w, h, stroke=INK, fill=PAPER, sw=1.6):
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, c=INK):
    ang = math.atan2(y2 - y1, x2 - x1)
    ax, ay = x2 - 9 * math.cos(ang - 0.4), y2 - 9 * math.sin(ang - 0.4)
    bx, by = x2 - 9 * math.cos(ang + 0.4), y2 - 9 * math.sin(ang + 0.4)
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.6"/>\n'
            f'  <polygon points="{x2},{y2} {ax:.1f},{ay:.1f} {bx:.1f},{by:.1f}" fill="{c}"/>')


def sig(z): return 1 / (1 + math.exp(-z))


# ------------------------------------------------------------------ 1. the neuron with the old rule, on payment D
def neuron():
    (w, b) = S["start"]
    name, x, y = S["payments"][4]          # E: large, abroad, not a new device — fraud
    z = sum(a * c for a, c in zip(w, x)) + b
    labels = ["large? (over €1,000)", "abroad?", "new device?"]
    B = []
    for i, (lab, xi, wi) in enumerate(zip(labels, x, w)):
        y0 = 70 + i * 90
        B += [box(30, y0, 200, 54), t(44, y0 + 23, lab), t(44, y0 + 44, f"x = {xi}", 15, NAVY, "700"),
              f'  <line x1="230" y1="{y0+27}" x2="420" y2="174" stroke="{NAVY}" stroke-width="{3 if wi else 1.2}"'
              f'{"" if wi else " stroke-dasharray=\"4 4\""}/>',
              t(250, y0 + 14 if i < 2 else y0 + 56, f"w = {wi:g}", 16, RED, "700")]
    B += [f'  <circle cx="465" cy="174" r="44" fill="#fff" stroke="{INK}" stroke-width="2"/>',
          t(465, 170, "Σ", 26, INK, "400", "middle"), t(465, 194, f"bias {b:g}", 12, MUTED, "400", "middle"),
          arrow(509, 174, 600, 174), t(555, 162, f"{z:g}", 16, INK, "700", "middle"),
          box(600, 134, 110, 80, INK, "#fff", 2),
          f'  <polyline points="615,196 655,196 655,152 695,152" fill="none" stroke="{GOLDDK}" stroke-width="3"/>',
          t(655, 232, "block if &gt; 0", 12, MUTED, "400", "middle"),
          arrow(710, 174, 770, 174),
          t(780, 166, "don’t block", 22, INK, "700"), t(780, 192, f"but {name} was fraud ✗", 15, RED, "700"),
          f'  <line x1="30" y1="330" x2="930" y2="330" stroke="{RULE}"/>',
          t(30, 360, "score = " + " + ".join(f"{wi:g}·{xi}" for wi, xi in zip(w, x)) + f" − {abs(b):g} = {z:g}", 18, INK, "700", extra=MONO)]
    svg("story-neuron.svg", 960, 375, B, f"a first guess, written as one neuron — payment {name}: large, abroad, fraud")


# ------------------------------------------------------------------ 2. step versus sigmoid, with our four payments
def step_sigmoid():
    *w, b = S["perceptron_final"]
    groups = {}
    for name, x, y in S["payments"]:
        z = round(sum(a * c for a, c in zip(w, x)) + b, 2)
        groups.setdefault(z, []).append((name, y))
    B = []
    for k, (title, f, col) in enumerate([("step: yes or no", lambda z: 1.0 if z > 0 else 0.0, GOLDDK),
                                          ("sigmoid: how sure", sig, NAVY)]):
        x0, y0, W, H = 40 + k * 460, 70, 400, 230
        B += [box(x0, y0, W, H, RULE, PAPER, 1), t(x0, y0 - 10, title, 17, col, "700")]
        X = lambda z: x0 + 20 + (z + 1.8) / 3.6 * (W - 40)
        Y = lambda v: y0 + H - 20 - v * (H - 40)
        B += [f'  <line x1="{X(0)}" y1="{y0+10}" x2="{X(0)}" y2="{y0+H-10}" stroke="{RULE}"/>',
              t(x0 + W - 6, Y(0) + 16, "score →", 12, MUTED, "400", "end"),
              t(x0 + 6, Y(1) + 4, "1", 12, MUTED), t(x0 + 6, Y(0) + 4, "0", 12, MUTED)]
        line = " ".join(f"{X(-1.8+3.6*i/200):.1f},{Y(f(-1.8+3.6*i/200)):.1f}" for i in range(201))
        B.append(f'  <polyline points="{line}" fill="none" stroke="{col}" stroke-width="3.5"/>')
        for z, members in sorted(groups.items()):
            v = f(z); fraud = members[0][1]
            label = " ".join(n for n, _ in members) + (f"  {v:.2f}" if k else "")
            below = (k == 0 and v == 0) or (k == 1 and z < 0.25)
            B += [f'  <circle cx="{X(z):.1f}" cy="{Y(v):.1f}" r="7" fill="{RED if fraud else "#fff"}" stroke="{RED if fraud else INK}" stroke-width="2"/>',
                  t(X(z) + (0 if below else -10), Y(v) + (28 if below else -12), label, 14, INK, "700", "middle" if below else "end")]
    B += [f'  <line x1="30" y1="345" x2="930" y2="345" stroke="{RULE}"/>',
          t(30, 372, "Step: nudging a weight changes nothing until the answer flips — no signal for which way to move.", 15, INK),
          t(30, 396, "Sigmoid: every nudge moves the output a little. Now “how wrong” is a number you can shrink.", 15, INK)]
    svg("story-step-sigmoid.svg", 960, 410, B,
        "the eight payments at the learned weights (" + ", ".join(f"{v:g}" for v in S["perceptron_final"]) + ") — red = fraud")


# ------------------------------------------------------------------ 3. backprop graph, Karpathy style: value and blame on every node
def graph():
    g = S["graph"]
    def node(x, y, label, val, grad, col=INK, w=168):
        return [box(x, y, w, 40, col, "#fff", 1.6),
                f'  <line x1="{x+44}" y1="{y}" x2="{x+44}" y2="{y+40}" stroke="{RULE}"/>',
                f'  <line x1="{x+106}" y1="{y}" x2="{x+106}" y2="{y+40}" stroke="{RULE}"/>',
                t(x + 22, y + 25, label, 13 if len(label) > 3 else 15, col, "700", "middle"),
                t(x + 75, y + 25, f"{val:.2f}", 15, INK, "400", "middle"),
                t(x + 137, y + 25, "—" if grad is None else (f"{grad:+.2f}" if abs(grad) >= 0.005 else "0.00"), 15, MUTED if grad is None else RED, "700", "middle")]
    def op(x, y, s):
        return [f'  <circle cx="{x}" cy="{y}" r="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>', t(x, y + 6, s, 17, INK, "700", "middle")]
    B = [t(30, 60, "each box:", 13, MUTED), t(100, 60, "name", 13, INK, "700"), t(145, 60, "value (forward) →", 13, INK),
         t(265, 60, "← blame (backward)", 13, RED, "700")]
    subs = ["₁", "₂", "₃"]
    ys = [78, 188, 298]
    for i, y0 in enumerate(ys):
        B += node(30, y0, "x" + subs[i], g["x"][i], None, MUTED) + node(30, y0 + 48, "w" + subs[i], g["w"][i], g["g_w"][i], NAVY)
        B += op(240, y0 + 44) if False else op(240, y0 + 44, "×")
        B += [arrow(198, y0 + 20, 225, y0 + 36), arrow(198, y0 + 68, 225, y0 + 52)]
        B += node(270, y0 + 24, "x" + subs[i] + "w" + subs[i], g["m"][i], g["g_m"][i])
        B += [arrow(438, y0 + 44, 505, 222 - (1 - i) * 16)]
    B += op(520, 222, "+")
    B += node(552, 202, "sum", g["s"], g["g_s"])
    B += node(552, 300, "b", g["b"], g["g_b"], NAVY)
    B += op(752, 262, "+") + [arrow(720, 222, 738, 250), arrow(720, 320, 738, 274)]
    B += node(778, 150, "z", g["z"], g["g_z"])
    B += [arrow(762, 248, 800, 192)]
    B += op(862, 228, "σ") + [arrow(862, 190, 862, 212)]
    B += node(778, 262, "p", g["p"], g["g_p"]) + [arrow(862, 244, 862, 262)]
    B += node(778, 340, "loss", g["L"], 1.0, RED) + [arrow(862, 302, 862, 340)]
    B += [t(30, 412, "Backward, right to left: each box’s blame = the blame of the box after it × how much it moved that box.", 14, INK),
          t(30, 434, f"Each weight’s blame is (p − y) × its input: ({g['p']:.2f} − 1) × 1 = {g['g_w'][0]:+.2f} — and w₃ gets none, because x₃ was 0.", 14, INK, "700")]
    svg("story-backprop.svg", 960, 446, B, "backpropagation on payment E, one neuron — the chain rule, box by box")


# ------------------------------------------------------------------ 4. the training loop, with the formula
def loop():
    steps = [("1 · guess", ["p = σ(w·x + b)"], INK),
             ("2 · how wrong?", ["loss =", "−log p(right answer)"], RED),
             ("3 · blame", ["for each weight:", "(p − y) · x"], NAVY),
             ("4 · nudge", ["w ← w − η · blame", "η = learning rate"], GREEN)]
    B = []
    for i, (h, lines, c) in enumerate(steps):
        x = 30 + i * 232
        B += [box(x, 80, 200, 130, c, PAPER, 2.5), t(x + 100, 116, h, 19, c, "700", "middle")]
        for j, line in enumerate(lines):
            B.append(t(x + 100, 150 + j * 24, line, 14 if len(line) > 18 else 15, INK, "400", "middle", MONO))
        if i < 3:
            B.append(arrow(x + 202, 145, x + 230, 145))
    B += [f'  <path d="M825,212 C825,285 130,285 130,215" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>',
          f'  <polygon points="124,222 130,210 136,222" fill="{MUTED}"/>',
          t(480, 298, "repeat for every example, many times", 15, MUTED, "400", "middle"),
          t(480, 338, "step 3 is backpropagation · the perceptron rule was the same shape: w ← w + η · (y − ŷ) · x", 14, INK, "400", "middle")]
    svg("story-loop.svg", 960, 355, B, "how every neural network learns — from our one neuron to a hundred billion weights")


# ------------------------------------------------------------------ 5. card testing: two hidden neurons
def card_testing():
    A, F, H = S["amounts"], S["fraud2"], S["hidden"]
    def net(a):
        hs = sig(H["small"][0] * a + H["small"][1]); hl = sig(H["large"][0] * a + H["large"][1])
        return hs, hl, sig(H["out"][0] * hs + H["out"][1] * hl + H["out"][2]), hl
    x0, W = 130, 780
    X = lambda a: x0 + a / 3.0 * W
    B = []
    rows = [(("one neuron alone", "fraud?"), 3, MUTED, 52, "its best try: one threshold"),
            (("hidden neuron 1", "small?"), 0, NAVY, 142, ""),
            (("hidden neuron 2", "large?"), 1, GOLDDK, 222, ""),
            (("output", "fraud?"), 2, RED, 302, "small OR large")]
    for label, k, col, y0, note in rows:
        Y = lambda v, y0=y0: y0 + 62 - v * 52
        B += [f'  <line x1="{x0}" y1="{Y(0)}" x2="{x0+W}" y2="{Y(0)}" stroke="{RULE}"/>',
              f'  <line x1="{x0}" y1="{Y(1)}" x2="{x0+W}" y2="{Y(1)}" stroke="{RULE}" stroke-dasharray="2 4"/>',
              t(x0 - 8, Y(1) + 4, "1", 10, MUTED, "400", "end"), t(x0 - 8, Y(0) + 4, "0", 10, MUTED, "400", "end"),
              t(x0 - 24, y0 + 30, label[0], 12, MUTED, "400", "end"), t(x0 - 24, y0 + 48, label[1], 15, col, "700", "end")]
        pts = " ".join(f"{X(3*i/300):.1f},{Y(net(3*i/300)[k]):.1f}" for i in range(301))
        B.append(f'  <polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>')
        if note:
            B.append(t(X(1.05), Y(1) + 14, note, 12, col, "700", "middle"))
    B += [t(X(0.02) + 8, 100, "misses the €10–€50 tests ✗", 12, RED, "700")]
    yp = 392
    B += [f'  <line x1="{x0}" y1="{yp}" x2="{x0+W}" y2="{yp}" stroke="{RULE}"/>', t(x0 - 24, yp + 4, "payments", 12, MUTED, "400", "end")]
    for a, y in zip(A, F):
        B.append(f'  <circle cx="{X(a):.1f}" cy="{yp}" r="6" fill="{RED if y else "#fff"}" stroke="{RED if y else INK}" stroke-width="2"/>')
    for a in (0, 1, 2, 3):
        B.append(t(X(a), yp + 24, f"€{a*1000:,}", 12, MUTED, "400", "middle"))
    B += [t(30, 446, "Red = fraud. One neuron draws one threshold, so it can catch one end only. Two hidden neurons each learn a question;", 14, INK),
          t(30, 466, "the output neuron combines them. Parameters: 2 × 2 in the hidden layer + 3 in the output = 7.", 14, INK, "700")]
    svg("story-card-testing.svg", 960, 478, B, "card testing — a fraudster tries the card with €10, then spends €2,000: fraud sits at both ends of the amount")


# ------------------------------------------------------------------ 6. same machine, bigger: fraud network vs LLM
def same_machine():
    rows = [("input", "3 answers: large? abroad? new device?", "the text so far, as token vectors"),
            ("output", "1 probability: fraud?", "~200,000 probabilities: which token next?"),
            ("loss", "−log p(right answer)", "−log p(right next token)"),
            ("update", "w ← w − η · blame", "w ← w − η · blame"),
            ("weights", "4", "117,000,000,000"),
            ("training data", "8 payments", "~15 trillion tokens of text")]
    B = [t(300, 80, "our fraud neuron", 18, NAVY, "700", "middle"), t(700, 80, "an LLM", 18, RED, "700", "middle")]
    for i, (k, a, b) in enumerate(rows):
        y = 112 + i * 44
        B += [f'  <line x1="30" y1="{y-18}" x2="930" y2="{y-18}" stroke="{RULE}"/>',
              t(30, y + 8, k.upper(), 12, GOLDDK, "700", extra='letter-spacing="1.1"'),
              t(300, y + 8, a, 16, INK, "400", "middle"), t(700, y + 8, b, 16, INK, "400", "middle")]
    B += [f'  <line x1="30" y1="{112+6*44-18}" x2="930" y2="{112+6*44-18}" stroke="{RULE}"/>',
          t(480, 402, "Same loss. Same update. Same loop. Only the size changed.", 17, RED, "700", "middle")]
    svg("story-same-machine.svg", 960, 418, B, "an LLM is a classifier: instead of “fraud or not?”, “which of 200,000 tokens comes next?”")


# ------------------------------------------------------------------ 7. from 3 to 117 billion
def scale():
    rows = [("our neuron", 4, "3 answers + a bias"),
            ("our small network, 1 → 2 → 1", 7, "card testing"),
            ("GPT-2 small, 2019", 124e6, "small enough to train yourself"),
            ("gpt-oss-20b, 2025", 21e9, "fits in 16 GB of memory"),
            ("gpt-oss-120b, 2025", 117e9, "fits on one 80 GB GPU")]
    lo, hi = 0, math.log10(2e11)
    B = []
    for i, (lab, n, note) in enumerate(rows):
        y = 70 + i * 58
        wbar = 30 + (math.log10(n) - lo) / (hi - lo) * 330
        txt = f"{n:,.0f}" if n < 1e6 else (f"{n/1e6:g} million" if n < 1e9 else f"{n/1e9:g} billion")
        col = RED if i >= 2 else NAVY
        B += [t(30, y + 20, lab, 15, INK, "700"),
              f'  <rect x="330" y="{y+4}" width="{wbar:.0f}" height="22" fill="{col}" fill-opacity=".85"/>',
              t(340 + wbar, y + 21, txt, 15, col, "700"), t(340 + wbar, y + 38, note, 12, MUTED)]
    B += [f'  <line x1="30" y1="370" x2="930" y2="370" stroke="{RULE}"/>',
          t(30, 396, "Every bar is the same arithmetic — multiply, add, squash — and the same training loop.", 15, INK)]
    svg("story-scale.svg", 960, 410, B, "number of weights (parameters), log scale — each step right is ten times more")


# ------------------------------------------------------------------ 8. the same nudge on text: a mixer of next tokens
def faders():
    F = S["faders"]
    toks = F["tokens"]
    B = [t(30, 66, "the training text", 13, MUTED, "700")]
    for i, (ctx, y) in enumerate(F["sentences"]):
        B.append(t(30, 92 + i * 24, f"{ctx} <tspan font-weight=\"700\" fill=\"{RED}\">{y}</tspan>", 14, INK))
    panels = F["snaps"]
    x0 = 300
    for k, sn in enumerate(panels):
        px0 = x0 + k * 160
        B.append(t(px0 + 62, 66, sn["label"], 12, INK, "700", "middle"))
        for j, (tok, pv) in enumerate(zip(toks, sn["p"])):
            cx = px0 + 10 + j * 26
            top, bot = 90, 300
            yk = bot - pv * (bot - top)
            col = RED if tok == "unchanged" else (NAVY if tok in ("steady", "at") else MUTED)
            B += [f'  <line x1="{cx}" y1="{top}" x2="{cx}" y2="{bot}" stroke="{RULE}" stroke-width="4" stroke-linecap="round"/>',
                  f'  <line x1="{cx}" y1="{yk:.1f}" x2="{cx}" y2="{bot}" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-opacity=".55"/>',
                  f'  <rect x="{cx-9}" y="{yk-6:.1f}" width="18" height="12" rx="2" fill="{col}"/>',
                  f'  <text x="{cx}" y="{bot+16}" font-size="10" fill="{MUTED}" text-anchor="end" transform="rotate(-45 {cx} {bot+16})">{tok}</text>']
        top_p = sn["p"][0]
        B.append(t(px0 + 62, 356, f"unchanged {top_p:.0%}", 13, RED, "700", "middle"))
    B += [f'  <line x1="30" y1="376" x2="930" y2="376" stroke="{RULE}"/>',
          t(30, 400, "One knob per possible next token. Each sentence turns the right one up a little and the others down.", 14, INK),
          t(30, 422, "After many passes the knobs sit where the text is: 3 in 5 said “unchanged”. Tokens never seen after “left rates” go to zero.", 14, INK, "700")]
    svg("story-faders.svg", 960, 436, B, "“… left rates” → ?  five sentences, five knobs, the same nudge as on payment E")


if __name__ == "__main__":
    neuron(); step_sigmoid(); graph(); loop(); card_testing(); same_machine(); scale(); faders()
