"""Week 1 figures for 'from one neuron to an LLM'. Numbers are computed here, not typed."""
import math
from pathlib import Path
HERE = Path(__file__).parent
RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE = "#AF1F25", "#CDBA80", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8"
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',Helvetica,Arial,sans-serif\""

def svg(name, w, h, body, sub):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
         f'  <text x="30" y="34" font-size="13" fill="{MUTED}">{sub}</text>'] + body + ['</svg>']
    (HERE / name).write_text("\n".join(s), encoding="utf-8"); print("wrote", name)

# ------------------------------------------------------------------ one neuron
def neuron():
    x = [("log amount (scaled)", 1.2), ("paid abroad", 1), ("new device", 1)]
    wts = [0.6, 1.1, 1.4]; bias = -2.0
    z = sum(v * w for (_, v), w in zip(x, wts)) + bias
    p = 1 / (1 + math.exp(-z))
    b = []
    for i, ((lab, v), w) in enumerate(zip(x, wts)):
        y = 95 + i * 80
        b += [f'  <rect x="30" y="{y-24}" width="200" height="44" fill="#f7f5ef" stroke="{RULE}"/>',
              f'  <text x="42" y="{y-4}" font-size="14" fill="{INK}">{lab}</text>',
              f'  <text x="42" y="{y+13}" font-size="13" font-weight="700" fill="{NAVY}">x = {v:g}</text>',
              f'  <line x1="230" y1="{y}" x2="455" y2="175" stroke="{NAVY}" stroke-width="{1+w*2.2:.1f}" stroke-opacity=".75"/>',
              f'  <text x="{250}" y="{y - 12 if i < 2 else y + 26}" font-size="14" font-weight="700" fill="{RED}">w = {w}</text>']
    b += [f'  <circle cx="500" cy="175" r="46" fill="#fff" stroke="{INK}" stroke-width="2"/>',
          f'  <text x="500" y="170" font-size="26" text-anchor="middle" fill="{INK}">&#931;</text>',
          f'  <text x="500" y="194" font-size="12" text-anchor="middle" fill="{MUTED}">bias {bias:g}</text>',
          f'  <line x1="546" y1="175" x2="630" y2="175" stroke="{INK}" stroke-width="2"/>',
          f'  <text x="588" y="163" font-size="13" text-anchor="middle" fill="{INK}">{z:.2f}</text>',
          f'  <rect x="630" y="140" width="110" height="70" fill="#fff" stroke="{INK}" stroke-width="2"/>',
          f'  <path d="M640,200 C680,200 690,150 730,150" fill="none" stroke="{GOLDDK}" stroke-width="3"/>',
          f'  <text x="685" y="228" font-size="12" text-anchor="middle" fill="{MUTED}">squash to 0&#8211;1</text>',
          f'  <line x1="740" y1="175" x2="800" y2="175" stroke="{INK}" stroke-width="2"/>',
          f'  <text x="810" y="170" font-size="30" font-weight="700" fill="{RED}">{p:.2f}</text>',
          f'  <text x="810" y="194" font-size="13" fill="{INK}">chance of fraud</text>',
          f'  <line x1="30" y1="300" x2="930" y2="300" stroke="{RULE}"/>',
          f'  <text x="30" y="328" font-size="15" fill="{INK}">Multiply, add, squash. <tspan font-weight="700">The weights are the only thing it learns</tspan> &#8212; here 3 of them and a bias: 4 numbers.</text>',
          f'  <text x="30" y="352" font-size="15" fill="{INK}">With the squash, this one neuron is exactly a logistic regression. You have seen it before under another name.</text>']
    svg("neuron.svg", 960, 370, b, "one artificial neuron, deciding whether to block a card payment &#8212; weights are illustrative")
    return z, p

# ------------------------------------------------------------------ scale
def scale():
    small = (2 + 1) * 5 + (5 + 1)     # 2 inputs, 5 hidden, 1 output, with biases — as in the clip
    rows = [("one neuron", 4, "the slide before"),
            ("a small network, 2 &#8594; 5 &#8594; 1", small, "the clip you just saw"),
            ("GPT-2 small, 2019", 124e6, "the one Karpathy rebuilds from scratch on video"),
            ("gpt-oss-20b, 2025", 21e9, "fits in 16 GB of memory"),
            ("gpt-oss-120b, 2025", 117e9, "fits on one 80 GB GPU")]
    lo, hi = math.log10(1), math.log10(2e11)
    b = []
    for i, (lab, n, note) in enumerate(rows):
        y = 70 + i * 58
        wbar = 30 + (math.log10(n) - lo) / (hi - lo) * 330
        txt = f"{n:,.0f}" if n < 1e6 else (f"{n/1e6:g} million" if n < 1e9 else f"{n/1e9:g} billion")
        col = RED if i >= 2 else NAVY
        b += [f'  <text x="30" y="{y+20}" font-size="15" font-weight="700" fill="{INK}">{lab}</text>',
              f'  <rect x="330" y="{y+4}" width="{wbar:.0f}" height="22" fill="{col}" fill-opacity=".85"/>',
              f'  <text x="{340+wbar:.0f}" y="{y+21}" font-size="15" font-weight="700" fill="{col}">{txt}</text>',
              f'  <text x="{340+wbar:.0f}" y="{y+38}" font-size="12" fill="{MUTED}">{note}</text>']
    b += [f'  <line x1="30" y1="370" x2="930" y2="370" stroke="{RULE}"/>',
          f'  <text x="30" y="396" font-size="15" fill="{INK}">Same arithmetic in every one &#8212; multiply, add, squash. The only thing that changed is <tspan font-weight="700" fill="{RED}">how many weights</tspan>, and what they were trained on.</text>']
    svg("nn-scale.svg", 960, 410, b, "number of weights (parameters), on a log scale: every step to the right is ten times more")
    return small

# ------------------------------------------------------------------ one token's journey
def journey():
    steps = [("text", '"The ECB left rates"', INK),
             ("tokens", "The | ECB | left | rates", INK),
             ("ids", "976 · 81201 · 3561 · 8104", MUTED),
             ("vectors", "each id &#8594; a list of ~3,000 numbers", NAVY)]
    b = []
    x = 30
    for i, (k, v, c) in enumerate(steps):
        y = 60 + i * 52
        b += [f'  <text x="{x}" y="{y+18}" font-size="11" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">{k.upper()}</text>',
              f'  <text x="{x+90}" y="{y+18}" font-size="16" fill="{c}" font-family="\'JetBrains Mono\',Menlo,monospace">{v}</text>']
        if i < 3:
            b.append(f'  <text x="{x+60}" y="{y+42}" font-size="14" fill="{MUTED}">&#8595;</text>')
    # the stack
    b += [f'  <rect x="30" y="270" width="520" height="118" fill="#f7f5ef" stroke="{NAVY}" stroke-width="2"/>',
          f'  <text x="46" y="296" font-size="11" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">ONE BLOCK &#8212; REPEATED 24 TO 100+ TIMES</text>',
          f'  <text x="46" y="324" font-size="15" fill="{INK}"><tspan font-weight="700" fill="{RED}">attention</tspan> &#8212; every token looks at the others and takes what it needs</text>',
          f'  <text x="46" y="350" font-size="15" fill="{INK}"><tspan font-weight="700" fill="{NAVY}">neurons</tspan> &#8212; each token\'s numbers go through a layer like the ones before</text>',
          f'  <text x="46" y="374" font-size="13" fill="{MUTED}">the vector changes a little at every block; the words never come back until the end</text>',
          f'  <line x1="550" y1="330" x2="600" y2="330" stroke="{INK}" stroke-width="2"/>',
          f'  <polygon points="600,324 610,330 600,336" fill="{INK}"/>']
    probs = [("unchanged", .62), ("steady", .11), ("at", .08), ("on", .05), ("…200,000 more", .14)]
    b.append(f'  <text x="625" y="80" font-size="11" font-weight="700" letter-spacing="1.1" fill="{GOLDDK}">A SCORE FOR EVERY TOKEN IT KNOWS</text>')
    for i, (t, p) in enumerate(probs):
        y = 100 + i * 34
        b += [f'  <text x="625" y="{y+16}" font-size="15" fill="{INK}">{t}</text>',
              f'  <rect x="760" y="{y+3}" width="{p*260:.0f}" height="18" fill="{RED if i==0 else GOLD}"/>',
              f'  <text x="{768+p*260:.0f}" y="{y+17}" font-size="13" fill="{INK}">{p:.2f}</text>']
    b += [f'  <text x="625" y="290" font-size="15" fill="{INK}">pick one &#8212; <tspan font-weight="700">temperature</tspan> decides how boldly</text>',
          f'  <text x="625" y="316" font-size="15" fill="{INK}">append it, and run the <tspan font-weight="700" fill="{RED}">whole thing again</tspan></text>',
          f'  <text x="625" y="342" font-size="15" fill="{INK}">for the next token. That is all it does.</text>',
          f'  <line x1="30" y1="408" x2="930" y2="408" stroke="{RULE}"/>',
          f'  <text x="30" y="432" font-size="14" fill="{MUTED}">token ids and probabilities are illustrative; the shape of the pipeline is not</text>']
    svg("token-journey.svg", 960, 445, b, "follow one prediction through the machine")

z, p = neuron(); small = scale(); journey()
print(f"neuron z={z:.2f} p={p:.2f}; small network weights={small}")
