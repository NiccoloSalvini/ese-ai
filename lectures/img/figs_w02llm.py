"""Week 2 figures — inside an LLM. Every number is read from w02_llm_story.json."""
import json, math
from pathlib import Path

HERE = Path(__file__).parent
S = json.loads((HERE / "w02_llm_story.json").read_text())
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
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.8"/>\n'
            f'  <polygon points="{x2},{y2} {ax:.1f},{ay:.1f} {bx:.1f},{by:.1f}" fill="{c}"/>')


# ------------------------------------------------------------------ the real knobs of GPT-2
def knobs():
    K = S["knobs"]
    B = [t(30, 70, f"“{S['prompt']}” →", 20, INK, "700", extra=MONO)]
    top, bot = 110, 320
    for j, k in enumerate(K):
        cx = 70 + j * 92
        yk = bot - k["p"] / 0.4 * (bot - top)
        col = RED if j == 0 else (NAVY if j < 3 else MUTED)
        B += [f'  <line x1="{cx}" y1="{top}" x2="{cx}" y2="{bot}" stroke="{RULE}" stroke-width="5" stroke-linecap="round"/>',
              f'  <line x1="{cx}" y1="{yk:.1f}" x2="{cx}" y2="{bot}" stroke="{col}" stroke-width="5" stroke-opacity=".55"/>',
              f'  <rect x="{cx-14}" y="{yk-7:.1f}" width="28" height="14" rx="2" fill="{col}"/>',
              t(cx + 20, yk + 5, f"{k['p']:.0%}", 14, col, "700"),
              t(cx, bot + 24, k["token"].strip(), 14, INK, "400", "middle")]
    B += [t(830, 215, f"…the other", 14, MUTED, "400", "middle"),
          t(830, 235, f"{S['gpt2']['vocab'] - len(K):,} tokens", 14, MUTED, "700", "middle"),
          t(830, 255, f"share {S['knobs_rest']:.0%}", 14, MUTED, "400", "middle"),
          f'  <line x1="30" y1="370" x2="930" y2="370" stroke="{RULE}"/>',
          t(30, 396, f"GPT-2 small, {S['gpt2']['params']/1e6:.0f} million weights: one knob for each of its {S['gpt2']['vocab']:,} tokens. These are its real settings after this prompt.", 14, INK)]
    svg("w02-knobs.svg", 960, 410, B, "the same mixer as last week — now a real model")


# ------------------------------------------------------------------ embeddings: meaning as a place
OFFSET = {"banks": (9, -6, "start"), "bank": (-9, -8, "end"), "mortgage": (9, 14, "start"), "credit": (0, 22, "middle"), "loan": (-9, 5, "end"),
          "prices": (9, -6, "start"), "rates": (9, 16, "start"), "wages": (-9, 5, "end"), "inflation": (-9, 5, "end"),
          "dollar": (9, 16, "start"), "Rome": (9, -6, "start"), "Paris": (9, 16, "start"), "London": (-9, 5, "end")}
def embed():
    pts = S["embed"]
    xs, ys = [p["x"] for p in pts], [p["y"] for p in pts]
    x0, x1, y0, y1 = min(xs) - 0.3, max(xs) + 0.5, min(ys) - 0.3, max(ys) + 0.3
    X = lambda v: 60 + (v - x0) / (x1 - x0) * 840
    Y = lambda v: 360 - (v - y0) / (y1 - y0) * 300
    groups = {"banking": ["bank", "banks", "lender", "loan", "credit", "debt", "mortgage"],
              "crypto": ["Bitcoin", "crypto", "blockchain", "Ethereum"],
              "cities": ["Paris", "Rome", "Berlin", "London"],
              "prices": ["inflation", "rates", "prices", "wages"],
              "currencies": ["euro", "dollar", "yen"]}
    col = {"banking": NAVY, "crypto": GOLDDK, "cities": GREEN, "prices": RED, "currencies": MUTED}
    B = []
    for g, words in groups.items():
        for p in pts:
            if p["word"] in words:
                dx, dy, anc = OFFSET.get(p["word"], (9, 5, "start"))
                B += [f'  <circle cx="{X(p["x"]):.1f}" cy="{Y(p["y"]):.1f}" r="6" fill="{col[g]}"/>',
                      t(X(p["x"]) + dx, Y(p["y"]) + dy, p["word"], 14, col[g], "700", anc)]
    c = {f"{d['a']}–{d['b']}": d["c"] for d in S["cosine"]}
    B += [f'  <line x1="30" y1="385" x2="930" y2="385" stroke="{RULE}"/>',
          t(30, 410, f"Nobody told the model these groups. Similarity (1 = same direction): bank–lender {c['bank–lender']}, bank–Paris {c['bank–Paris']}, Bitcoin–crypto {c['Bitcoin–crypto']}.", 14, INK)]
    svg("w02-embed.svg", 960, 424, B, "GPT-2’s own vectors for 22 words — 768 numbers each, flattened onto a page")


# ------------------------------------------------------------------ attention by hand
def attention_hand():
    A = S["toy_attention"]
    cols = ["token", "its key", "score = query · key", "e^score", "attention", "its value"]
    xs = [30, 160, 300, 520, 640, 800]
    B = [t(30, 66, "“it” asks, with query (1.5, 0): who in this sentence is an actor that can fear?", 15, INK, "700")]
    for x, c in zip(xs, cols):
        B.append(t(x, 100, c.upper(), 11, MUTED, "700", extra='letter-spacing="1"'))
    B.append(f'  <line x1="30" y1="108" x2="930" y2="108" stroke="{RED}" stroke-width="1.5"/>')
    for i, tk in enumerate(A["tokens"]):
        y = 134 + i * 32
        hi = tk == "bank"
        k = A["keys"][i]; v = A["values"][i]
        row = [tk, f"({k[0]:g}, {k[1]:g})", f"1.5×{k[0]:g} + 0×{k[1]:g} = {A['scores'][i]:g}", f"{A['exp'][i]:.2f}",
               f"{A['weights'][i]:.0%}", f"({v[0]:g}, {v[1]:g})"]
        for x, cell in zip(xs, row):
            B.append(t(x, y, cell, 15, RED if hi else INK, "700" if hi else "400", extra=MONO if x in (160, 300, 800) else ""))
        B.append(f'  <line x1="30" y1="{y+10}" x2="930" y2="{y+10}" stroke="{RULE}"/>')
    tot = sum(A["exp"])
    B += [t(520, 134 + 6 * 32, f"total {tot:.2f}", 13, MUTED), t(640, 134 + 6 * 32, "each ÷ total", 13, MUTED),
          t(30, 372, f"New meaning of “it” = the values mixed by attention = ({A['mixed'][0]:.2f}, {A['mixed'][1]:.2f}): mostly “bank”, a little “rates”.", 15, INK, "700"),
          t(30, 398, "Score: multiply and add — a neuron. Divide the exponentials by their total — the knobs. Nothing new, just arranged differently.", 14, INK)]
    svg("w02-attention-hand.svg", 960, 412, B, "attention with two numbers per vector, by hand — values are (is an institution, is a price)")


# ------------------------------------------------------------------ real attention
def attention_real():
    R = S["real_attention"]
    B = [t(30, 70, f"GPT-2, layer {R['layer']}, head {R['head']}: where “it” looks", 16, INK, "700")]
    for i, (tk, v) in enumerate(zip(R["tokens"], R["weights"])):
        y = 92 + i * 40
        w = v * 600
        col = RED if tk == "bank" else NAVY
        B += [t(150, y + 22, tk, 16, INK, "700", "end"),
              f'  <rect x="165" y="{y+6}" width="{max(w,2):.0f}" height="24" fill="{col}" fill-opacity="{0.9 if tk == "bank" else 0.5}"/>',
              t(175 + w, y + 24, f"{v:.0%}", 15, col, "700")]
    B += [f'  <line x1="30" y1="345" x2="930" y2="345" stroke="{RULE}"/>',
          t(30, 372, f"A real model has {S['gpt2']['layers']} layers × {S['gpt2']['heads']} heads = {S['gpt2']['layers']*S['gpt2']['heads']} of these, each looking for something different. Nobody programmed this one:", 14, INK),
          t(30, 394, "it was learned, by the same nudge, because resolving “it” helps guess the next token.", 14, INK, "700")]
    svg("w02-attention-real.svg", 960, 408, B, f"“{R['sentence']}” — measured inside the model, not drawn")


# ------------------------------------------------------------------ the transformer block
def block():
    g = S["gpt2"]
    B = []
    toks = ["The", "ECB", "left", "rates"]
    for i, tk in enumerate(toks):
        x = 60 + i * 110
        B += [t(x + 40, 72, tk, 15, INK, "700", "middle"), arrow(x + 40, 80, x + 40, 104, MUTED),
              box(x, 106, 80, 34, NAVY, "#fff"), t(x + 40, 128, "vector", 12, NAVY, "400", "middle")]
    B.append(t(520, 128, f"+ position: each token also gets a vector for “where am I”", 13, MUTED))
    B += [box(40, 160, 450, 150, INK, PAPER, 2), t(60, 184, "ONE BLOCK", 11, GOLDDK, "700", extra='letter-spacing="1.2"'),
          box(60, 196, 410, 44, RED, "#fff", 2), t(265, 223, "attention — tokens exchange information", 14, RED, "700", "middle"),
          box(60, 252, 410, 44, NAVY, "#fff", 2), t(265, 279, "neurons — each token thinks on its own", 14, NAVY, "700", "middle"),
          t(520, 223, "the query · key · value step you just did by hand", 13, INK),
          t(520, 279, "a hidden layer, like the card-testing network", 13, INK),
          t(520, 184, "each part adds its result to the vector — it never replaces it", 13, MUTED),
          t(265, 336, f"× {g['layers']} in GPT-2 small · × 36 in gpt-oss-120b", 16, INK, "700", "middle"),
          arrow(265, 344, 265, 370),
          box(40, 372, 450, 40, GOLDDK, "#fff", 2), t(265, 398, f"last vector → {g['vocab']:,} scores → softmax → the knobs", 14, INK, "700", "middle")]
    svg("w02-block.svg", 960, 424, B, "a transformer, the architecture of every current LLM — nothing in it you have not already met")


# ------------------------------------------------------------------ mixture of experts
def moe():
    B = [t(30, 70, "one token arrives", 15, INK, "700"), box(30, 84, 120, 40, NAVY, "#fff"), t(90, 109, "vector", 13, NAVY, "400", "middle"),
         arrow(150, 104, 200, 104), box(200, 80, 130, 48, GOLDDK, "#fff", 2), t(265, 102, "router", 14, GOLDDK, "700", "middle"),
         t(265, 119, "picks 4", 12, MUTED, "400", "middle")]
    chosen = {3, 17, 40, 91}
    for k in range(128):
        r, c = divmod(k, 32)
        x, y = 380 + c * 17, 70 + r * 22
        on = k in chosen
        B.append(f'  <rect x="{x}" y="{y}" width="13" height="16" fill="{RED if on else PAPER}" stroke="{RED if on else RULE}"/>')
    B += [arrow(330, 104, 372, 104), t(650, 176, "128 experts — small networks of neurons; 4 run for this token", 13, INK, "700", "middle"),
          f'  <line x1="30" y1="210" x2="930" y2="210" stroke="{RULE}"/>',
          t(30, 238, "gpt-oss-120b: 117 billion weights in total, 5.1 billion used per token.", 15, INK, "700"),
          t(30, 262, "It holds as much as a big model and costs, per token, like a small one.", 15, INK)]
    svg("w02-moe.svg", 960, 276, B, "mixture-of-experts: the block’s neurons, split into specialists")


# ------------------------------------------------------------------ one prediction end to end, real GPT-2 numbers
def journey():
    g = S["gpt2"]; toks = S["prompt_tokens"]; ids = S["prompt_ids"]
    steps = [("text", f"“{S['prompt']}”", INK), ("tokens", " | ".join(tk.strip() for tk in toks), INK),
             ("ids", " · ".join(str(i) for i in ids), MUTED), ("vectors", f"each id → {g['width']} numbers (+ its position)", NAVY)]
    B = []
    for i, (k, v, c) in enumerate(steps):
        y = 60 + i * 52
        B += [t(30, y + 18, k.upper(), 11, GOLDDK, "700", extra='letter-spacing="1.1"'), t(120, y + 18, v, 16, c, "400", extra=MONO)]
        if i < 3:
            B.append(t(90, y + 42, "↓", 14, MUTED))
    B += [box(30, 270, 520, 110, NAVY, PAPER, 2),
          t(46, 296, f"ONE BLOCK — × {g['layers']} IN GPT-2 SMALL", 11, GOLDDK, "700", extra='letter-spacing="1.1"'),
          t(46, 324, "attention — every token looks at the others and takes what it needs", 14, INK),
          t(46, 350, "neurons — each token’s numbers through a hidden layer", 14, INK),
          arrow(550, 330, 605, 330)]
    B.append(t(625, 80, "THE KNOBS: A SCORE FOR EVERY TOKEN", 11, GOLDDK, "700", extra='letter-spacing="1.1"'))
    K = S["knobs"][:4]
    for i, k in enumerate(K):
        y = 100 + i * 34
        B += [t(625, y + 16, k["token"].strip(), 15, INK), f'  <rect x="740" y="{y+3}" width="{k["p"]*420:.0f}" height="18" fill="{RED if i == 0 else GOLD}"/>',
              t(748 + k["p"] * 420, y + 17, f"{k['p']:.0%}", 13, INK)]
    B += [t(625, 256, f"…{g['vocab'] - 4:,} more", 14, MUTED),
          t(625, 300, "pick one — temperature decides how boldly", 15, INK),
          t(625, 326, "append it, and run the whole thing again", 15, INK),
          f'  <line x1="30" y1="400" x2="930" y2="400" stroke="{RULE}"/>',
          t(30, 424, "Real numbers from GPT-2 small: its token ids, its width, its layers, its probabilities after this prompt.", 14, MUTED)]
    svg("w02-journey.svg", 960, 438, B, "one prediction, through a real model")


if __name__ == "__main__":
    knobs(); embed(); attention_hand(); attention_real(); block(); moe(); journey()
