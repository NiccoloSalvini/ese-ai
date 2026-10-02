"""Week 2 — the real GPT-2, drawn: the full architecture and one card of real arithmetic per box.
Every number is read from w02_gpt2_walk.json (w02_gpt2_walk.py, one forward pass by hand)."""
import json
from pathlib import Path
from figs_w02llm import svg, t, box, arrow, RED, GOLD, GOLDDK, NAVY, GREEN, INK, MUTED, RULE, PAPER, MONO

HERE = Path(__file__).parent
W = json.loads((HERE / "w02_gpt2_walk.json").read_text())
P = W["params"]
M = lambda n: f"{n / 1e6:.2f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e3 else str(n)
f = lambda v: f"{v:+.2f}".replace("+", " ").replace("-", "−")
vec = lambda v: "[" + " ".join(f(x) for x in v) + " …]"


def arch():
    """GPT-2 small, every layer, bottom to top as in the papers — with real sizes and parameter counts."""
    B = []
    cx, bw = 262, 300
    x0 = cx - bw // 2
    rx = x0 - 26                                                          # the residual stream
    def lay(y, h, label, col, sub="", size=14):
        out = [box(x0, y, bw, h, col, "#fff", 2), t(cx, y + h / 2 + 5 - (6 if sub else 0), label, size, col, "700", "middle")]
        if sub:
            out.append(t(cx, y + h / 2 + 13, sub, 11, MUTED, "400", "middle"))
        return out
    B += lay(48, 28, "softmax → 50,257 probabilities", GOLDDK)
    B += [arrow(cx, 90, cx, 78, MUTED)]
    B += lay(90, 34, "unembedding: 768 → 50,257 scores", GOLDDK, "the token-embedding table, reused")
    B += [arrow(cx, 136, cx, 126, MUTED)]
    B += lay(136, 22, "final LayerNorm", MUTED, size=13)
    by, bh = 170, 178
    B += [box(x0 - 44, by, bw + 64, bh, INK, PAPER, 2.2),
          t(x0 + bw + 28, by + bh / 2 + 7, f"× {W['layers']}", 20, INK, "700"),
          t(x0 + bw + 14, by + 16, "ONE BLOCK", 11, GOLDDK, "700", "end", 'letter-spacing="1.2"'),
          arrow(cx, by + 2, cx, 160, MUTED)]
    B += [f'  <line x1="{rx}" y1="{by + bh + 14}" x2="{rx}" y2="{by - 6}" stroke="{GREEN}" stroke-width="3"/>',
          f'  <line x1="{rx}" y1="{by - 6}" x2="{cx}" y2="{by - 6}" stroke="{GREEN}" stroke-width="3"/>']
    # two sub-layers, each: LayerNorm (tap off the stream) -> layer -> added back with ⊕
    subs = [(by + 96, "masked attention: 12 heads × 64", RED, "tokens read earlier tokens · " + M(P["attention_per_block"])),
            (by + 10, f"MLP: 768 → {W['d_mlp']:,} → 768 (GELU)", NAVY, "each token on its own · " + M(P["mlp_per_block"]))]
    for y, lab, col, sub in subs:
        ln_y, ly = y + 58, y + 18
        B += lay(ln_y, 20, "LayerNorm", MUTED, size=12)
        B += lay(ly, 32, lab, col, sub)
        B += [f'  <line x1="{rx}" y1="{ln_y + 28}" x2="{cx}" y2="{ln_y + 28}" stroke="{GREEN}" stroke-width="1.6"/>',
              arrow(cx, ln_y + 28, cx, ln_y + 22, MUTED), arrow(cx, ln_y, cx, ly + 34, MUTED),
              f'  <line x1="{x0}" y1="{ly + 10}" x2="{rx + 9}" y2="{ly + 10}" stroke="{GREEN}" stroke-width="1.6"/>',
              f'  <circle cx="{rx}" cy="{ly + 10}" r="9" fill="#fff" stroke="{GREEN}" stroke-width="2"/>',
              t(rx, ly + 15, "+", 15, GREEN, "700", "middle")]
    ey = by + bh + 16
    B += [box(x0, ey, 142, 36, NAVY, "#fff", 2), t(x0 + 71, ey + 16, "token embedding", 13, NAVY, "700", "middle"),
          t(x0 + 71, ey + 30, f"50,257 × 768 · {M(P['token_embeddings'])}", 10.5, MUTED, "400", "middle"),
          box(x0 + 158, ey, 142, 36, NAVY, "#fff", 2), t(x0 + 229, ey + 16, "+ position embedding", 13, NAVY, "700", "middle"),
          t(x0 + 229, ey + 30, f"1,024 × 768 · {M(P['position_embeddings'])}", 10.5, MUTED, "400", "middle"),
          f'  <line x1="{x0}" y1="{ey - 2}" x2="{rx}" y2="{ey - 2}" stroke="{GREEN}" stroke-width="1.6"/>',
          f'  <line x1="{rx}" y1="{ey - 2}" x2="{rx}" y2="{by + bh + 14}" stroke="{GREEN}" stroke-width="3"/>']
    ty = ey + 58
    B += [t(cx, ty, "“The ECB left rates” → " + " ".join(str(i) for i in W["ids"]), 13, INK, "700", "middle", MONO),
          arrow(cx, ty - 14, cx, ey + 38, MUTED)]
    # right column: legend
    lx = 520
    notes = [(70, "READ IT BOTTOM TO TOP", GOLDDK, "700", 11),
             (98, "the text → token ids → one vector of 768 numbers per token", INK, "400", 14),
             (124, "each block: attention, then MLP; each adds to the vector", INK, "400", 14),
             (146, "— the green line, the residual stream — never replaces it", INK, "400", 14),
             (172, "LayerNorm: rescale the 768 numbers to mean 0, spread 1", INK, "400", 14),
             (198, "masked: a token only reads the tokens before it", INK, "400", 14),
             (224, "the last token's vector becomes 50,257 scores → the knobs", INK, "400", 14),
             (268, "WHERE THE 124,439,808 NUMBERS ARE", GOLDDK, "700", 11)]
    for y, s, c, w, sz in notes:
        B.append(t(lx, y, s, sz, c, w, extra='letter-spacing="1.1"' if sz == 11 else ""))
    rows = [("token + position embeddings", P["token_embeddings"] + P["position_embeddings"], NAVY),
            (f"attention × {W['layers']}", P["attention_per_block"] * W["layers"], RED),
            (f"MLP × {W['layers']}", P["mlp_per_block"] * W["layers"], NAVY),
            ("LayerNorms", P["layernorms_per_block"] * W["layers"] + P["final_layernorm"], MUTED)]
    tot = P["total"]
    for i, (lab, v, c) in enumerate(rows):
        y = 290 + i * 30
        B += [t(lx, y + 14, lab, 14, INK), f'  <rect x="{lx + 190}" y="{y + 2}" width="{v / tot * 170:.1f}" height="16" fill="{c}" opacity="0.85"/>',
              t(lx + 196 + v / tot * 170, y + 15, f"{M(v)} · {v / tot:.0%}", 13, INK)]
    B.append(t(lx, 424, f"total {tot:,} — checked against the library", 13, MUTED))
    svg("w02-gpt2.svg", 960, 460, B, "GPT-2 small, every layer, with its real sizes — gpt-oss has the same shape: 36 blocks, 128 experts in the MLP")


def table(name, sub, head, rows, widths, hl=None, foot=None, h=None, x=30, y0=70, size=15, rh=34, mono=True):
    B, xs, mono_ok = [], [x], mono
    for wd in widths[:-1]:
        xs.append(xs[-1] + wd)
    for xi, hd in zip(xs, head):
        B.append(t(xi, y0, hd, 11, MUTED, "700", extra='letter-spacing="1.1"'))
    B.append(f'  <line x1="{x}" y1="{y0 + 10}" x2="{x + sum(widths)}" y2="{y0 + 10}" stroke="{RED}" stroke-width="1.5"/>')
    for i, row in enumerate(rows):
        y = y0 + 38 + i * rh
        col = RED if hl is not None and i == hl else INK
        for j, (xi, cell) in enumerate(zip(xs, row)):
            mono = mono_ok and j > 0 and any(ch.isdigit() for ch in str(cell))
            B.append(t(xi, y, cell, size, col, "700" if (hl is not None and i == hl) or j == 0 else "400", extra=MONO if mono else ""))
        B.append(f'  <line x1="{x}" y1="{y + 12}" x2="{x + sum(widths)}" y2="{y + 12}" stroke="{RULE}"/>')
    yb = y0 + 38 + len(rows) * rh
    for k, line in enumerate(foot or []):
        B.append(t(x, yb + 14 + k * 24, line, 15, INK, "700" if k == 0 else "400"))
    svg(name, 960, h or yb + 20 + 24 * len(foot or []), B, sub)


def calc_embed():
    rows = [[e["token"].strip(), str(e["id"]), vec(e["wte"]), vec(e["wpe"]), vec(e["x"])] for e in W["embed"]]
    table("w02-calc-embed.svg", "step ② for real — GPT-2's own numbers, the first 4 of 768 shown",
          ["token", "id", "its row in the token table", "+ row for its position", "= what enters block 1"],
          rows, [80, 90, 260, 260, 250],
          foot=["Two lookups and one sum. Nothing is computed yet: the table rows were learned by the loop.",
                "The position row is how the model knows “ECB” is 2nd — attention alone would not know the order."])


def calc_attn():
    A = W["head_rates_to_ECB"]
    toks = [x.strip() for x in W["tokens"]]
    rows = [[tk, vec(k), f"{d:.2f}", f"{s:.2f}", f"{e:.3f}", f"{w:.0%}"] for tk, k, d, s, e, w in
            zip(toks, A["k"], A["dot"], A["scaled"], A["exp"], A["weights"])]
    hl = max(range(len(rows)), key=lambda i: A["weights"][i])
    table("w02-calc-attn.svg", f"step ③ for real — block {A['layer']}, head {A['head']} of {W['heads']}: what “rates” reads",
          ["token", "its key (4 of 64)", "query · key", "÷ √64 = 8", "e^(score − max)", "share"],
          rows, [80, 250, 130, 120, 170, 90], hl=hl,
          foot=[f"“rates” asks with its query {vec(A['q'])} — multiply by each key, 64 pairs, and add: a neuron.",
                f"Into shares: e^ each score, divide by the total ({sum(A['exp']):.3f}). {A['weights'][hl]:.0%} of what “rates” reads here comes from “{toks[hl]}”.",
                "Masked: “left” could not read “rates” — a token only sees the ones before it. 12 heads do this at once, in each of 12 blocks."])


def calc_mlp():
    b = W["block0"]
    v3 = lambda v: "[" + " ".join(f(x) for x in v[:3]) + " …]"
    rows = [["LayerNorm", "rescale the 768 numbers", f"mean {b['ln_mean']:.3f}, spread {b['ln_std']:.3f} → 0 and 1"],
            ["expand", f"768 → {W['d_mlp']:,} neurons", "each: weigh, add, bias — 4× wider"],
            ["switch", "GELU: negatives → about 0", f"{b['mlp_hidden_positive']} of {W['d_mlp']:,} fire for “rates”"],
            ["shrink", f"{W['d_mlp']:,} → 768", "back to the width of the vector"],
            ["add", "⊕ to the vector", f"{v3(b['x_after_attn'])} → {v3(b['x_after_block'])}"]]
    table("w02-calc-mlp.svg", "step ④ for real — the MLP of block 1, on “rates”", ["", "what happens", "the real numbers"],
          rows, [120, 290, 510],
          foot=[f"{M(P['mlp_per_block'])} numbers per block, ×12: two thirds of every block — 46% of GPT-2 — lives here.",
                "A hidden layer like card testing, 3,072 wide: each neuron is a question nobody wrote. In gpt-oss, 128 experts."])


def calc_lens():
    L = W["logit_lens"]
    rows = []
    for l in L:
        tops = "  ".join(f"{tk.strip()} {p:.0%}" for tk, p in l["top"])
        rows.append([f"after block {l['after_block']}", tops])
    hl = next(i for i, l in enumerate(L) if l["top"][0][0].strip() == "unchanged" and l["top"][0][1] > 0.5)
    table("w02-calc-lens.svg", "stop after each block and read the knobs — what the stack adds, on GPT-2 for real",
          ["", "top 3 next tokens if we stopped here"], rows, [160, 700], hl=hl, size=14, y0=62, rh=29,
          foot=None)


def calc_final():
    F = W["final"]["top"]
    d = F[0]["logit"] - F[1]["logit"]
    rows = [[x["token"].strip(), f"{x['logit']:.2f}", f"{x['logit'] - F[0]['logit']:+.2f}".replace("-", "−"), f"{x['p']:.1%}"] for x in F]
    table("w02-calc-final.svg", "step ⑤ for real — the last vector of “rates” × the 50,257 rows of the token table",
          ["next token", "score", "vs the top", "probability"], rows, [200, 180, 180, 160], hl=0,
          foot=[f"Only differences matter: “unchanged” scores {d:.2f} above “at”, so it is e^{d:.2f} = {2.718281828 ** d:.2f} times as likely — {F[0]['p']:.1%} vs {F[1]['p']:.1%}.",
                "The other 50,252 tokens share what is left. Temperature divides the scores before this step."])


def calc_quant():
    Q = json.loads((HERE / "w02_quant.json").read_text())
    e = Q["example"]
    g = lambda v: f"{abs(v) if v == 0 else v:g}".replace("-", "−")
    z = lambda v, fm: (fm.format(0.0) if abs(v) < 5e-5 else fm.format(v)).replace("-", "−")
    rows = [[f"weight {i + 1}", z(a, "{:.4f}"), z(b, "{:.2f}"), g(c), z(d, "{:.4f}")]
            for i, (a, b, c, d) in enumerate(zip(e["weights_16bit"], e["divided_by_scale"], e["nearest_fp4"], e["back"]))]
    table("w02-calc-quant.svg", "quantization by hand — 8 real weights of GPT-2 (block 1, MLP), squeezed into MXFP4",
          ["", "stored in 16 bits", f"÷ the block's scale {e['scale']:g}", "nearest of 16 values", "what is kept"],
          rows, [120, 190, 230, 210, 190], size=14, rh=27, y0=64,
          foot=[f"Allowed values: 0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6 — 16 of them, so 4 bits. Every 32 weights share one scale (8 bits).",
                f"4 + 8/32 = {Q['bits_per_weight']} bits instead of 16. For 117 billion weights: {Q['gpt_oss']['gb_16bit']} GB → {Q['gpt_oss']['gb_mxfp4']} GB."])
    rows = [[f"{i + 1}", a[0], f"{a[1]:.1%}", b[0], f"{b[1]:.1%}"] for i, (a, b) in enumerate(zip(Q["knobs_before"], Q["knobs_after"]))]
    table("w02-calc-quant2.svg", f"all {Q['quantized_weights']:,} weights inside GPT-2's 12 blocks squeezed to 4 bits — then the same prompt",
          ["", "16 bits: next token", "", "4 bits: next token", ""], rows, [60, 230, 150, 230, 150], hl=0,
          foot=[f"Each weight moved by {Q['relative_error']:.0%} on average — and the answer is the same: “unchanged” still on top.",
                "The knobs shift a little. gpt-oss ships “natively” in 4 bits — tuned for them — so it loses even less."])


def oss_vs_gpt2():
    """GPT-2 (our walk) next to gpt-oss-120b (model card, OpenAI, Aug 2025): same skeleton, newer parts."""
    O = {"layers": 36, "d": 2880, "vocab": 201088, "context": 131072, "q_heads": 64, "kv_heads": 8,
         "experts": 128, "active_experts": 4, "mlp": 114.71e9, "attn": 0.96e9, "embed": 1.16e9, "total": 116.83e9,
         "active": 5.13e9, "ckpt_gib": 60.8}
    pm = P["mlp_per_block"] * W["layers"]
    rows = [["blocks", f"{W['layers']}", f"{O['layers']}"],
            ["numbers per token vector", f"{W['d_model']}", f"{O['d']:,}"],
            ["vocabulary", f"{W['vocab']:,}", f"{O['vocab']:,} (o200k_harmony)"],
            ["where am I?", f"a learned row per position, max {W['context']:,}", f"RoPE: rotate q and k by position → {O['context']:,}"],
            ["rescaling", "LayerNorm", "RMSNorm (the same idea, cheaper)"],
            ["attention heads", f"{W['heads']}, each with its own keys and values", f"{O['q_heads']} questions sharing {O['kv_heads']} key/value sets (GQA)"],
            ["which tokens it reads", "all earlier ones", "all earlier, or only the last 128 — alternating"],
            ["MLP", f"one: 768 → {W['d_mlp']:,} → 768, GELU", f"{O['experts']} experts, {O['active_experts']} picked per token, SwiGLU"],
            ["share of numbers in the MLP", f"{pm / P['total']:.0%}", f"{O['mlp'] / O['total']:.0%}"],
            ["total numbers", f"{P['total'] / 1e6:.0f} million", f"{O['total'] / 1e9:.2f} billion, {O['active'] / 1e9:.2f}B used per token"]]
    table("w02-oss-vs-gpt2.svg", "the same skeleton, newer parts — gpt-oss numbers from its model card (OpenAI, August 2025)",
          ["", "GPT-2 small (2019)", "gpt-oss-120b (2025)"], rows, [240, 300, 400], size=15, rh=30, y0=62, mono=False,
          foot=["Every new part saves memory or reaches further back. None changes the loop or the block."])


def calc_kv():
    K = json.loads((HERE / "w02_kv.json").read_text())
    rows = [["read the prompt (prefill)", f"{K['N']} tokens in one pass", f"{K['prefill_s']:.2f} s", f"{K['prefill_tokens_per_s']:,} tokens/s"],
            ["write the answer (decode)", f"{K['N']} tokens, one at a time", f"{K['decode_cached_s']:.1f} s", f"{K['decode_tokens_per_s']:.0f} tokens/s"],
            ["write 128 tokens, no cache", "re-read everything each step", f"{K['decode_nocache_s']:.1f} s", ""],
            ["write 128 tokens, with cache", "keep each token's keys and values", f"{K['decode_cached_M_s']:.1f} s", ""]]
    table("w02-calc-kv.svg", f"GPT-2 timed on a laptop — reading is parallel, writing is one token at a time",
          ["", "", "time", "speed"], rows, [280, 320, 140, 200], hl=1, size=15, rh=32, y0=62, mono=False,
          foot=[f"Reading is {K['prefill_tokens_per_s'] / K['decode_tokens_per_s']:.0f}× faster than writing. One reason output tokens cost more than input tokens.",
                f"The cache: each token's keys and values, kept. gpt-oss at full context: {K['oss_kv_GB_full_context']} GB per conversation,",
                f"thanks to 8 shared key/value sets and the 128-token windows. Without them: {K['oss_kv_GB_if_no_gqa_no_window']} GB — more than the GPU."])


if __name__ == "__main__":
    arch(); calc_embed(); calc_attn(); calc_mlp(); calc_lens(); calc_final(); calc_quant(); oss_vs_gpt2(); calc_kv()
