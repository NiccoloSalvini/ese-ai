"""Week 2 — one real forward pass through GPT-2 small, by hand, on "The ECB left rates".

Every number on the architecture slides comes from here. The pass is recomputed step by step
from GPT-2's own weights (embeddings, LayerNorm, 12 heads, MLP 768 -> 3072 -> 768, residuals,
final LayerNorm, unembedding) and checked against the library's output. Writes w02_gpt2_walk.json.
Run with a python that has torch + transformers (e.g. ~/.venvs/ese-ai-ml).
"""
import json, math
from pathlib import Path
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

HERE = Path(__file__).parent
PROMPT = "The ECB left rates"
torch.manual_seed(0)
tok = GPT2TokenizerFast.from_pretrained("gpt2")
m = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager").eval()
T = m.transformer
D, H, L, V = m.config.n_embd, m.config.n_head, m.config.n_layer, m.config.vocab_size
dh = D // H
ids = tok(PROMPT, return_tensors="pt").input_ids[0]
toks = [tok.decode([i]) for i in ids]
n = len(ids)
r = lambda v, k=4: [round(float(x), 3) for x in v[:k]]
out = {"prompt": PROMPT, "tokens": toks, "ids": ids.tolist(), "d_model": D, "heads": H, "d_head": dh,
       "layers": L, "vocab": V, "d_mlp": T.h[0].mlp.c_fc.weight.shape[1], "context": m.config.n_positions}

# ---- parameter count, box by box
cnt = lambda mod: sum(p.numel() for p in mod.parameters())
blk = T.h[0]
out["params"] = {"token_embeddings": T.wte.weight.numel(), "position_embeddings": T.wpe.weight.numel(),
                 "attention_per_block": cnt(blk.attn), "mlp_per_block": cnt(blk.mlp),
                 "layernorms_per_block": cnt(blk.ln_1) + cnt(blk.ln_2), "final_layernorm": cnt(T.ln_f),
                 "total": sum(p.numel() for p in m.parameters())}

with torch.no_grad():
    # 1-2. tokens -> embeddings + positions
    te, pe = T.wte.weight[ids], T.wpe.weight[:n]
    x = te + pe
    out["embed"] = [{"token": toks[i], "id": int(ids[i]), "wte": r(te[i]), "wpe": r(pe[i]), "x": r(x[i])} for i in range(n)]

    def ln(mod, v):
        mu, sd = v.mean(-1, keepdim=True), v.var(-1, keepdim=True, unbiased=False).add(mod.eps).sqrt()
        return (v - mu) / sd * mod.weight + mod.bias, mu, sd

    def block(b, x, record=False, layer=None):
        a_in, mu, sd = ln(b.ln_1, x)
        qkv = a_in @ b.attn.c_attn.weight + b.attn.c_attn.bias           # 768 -> 3*768
        q, k, v = qkv.split(D, -1)
        q, k, v = (t.view(n, H, dh).transpose(0, 1) for t in (q, k, v))  # 12 heads x n x 64
        s = q @ k.transpose(-1, -2) / math.sqrt(dh)
        mask = torch.triu(torch.ones(n, n, dtype=torch.bool), 1)
        s = s.masked_fill(mask, float("-inf"))
        w = s.softmax(-1)
        o = (w @ v).transpose(0, 1).reshape(n, D)
        attn = o @ b.attn.c_proj.weight + b.attn.c_proj.bias
        x1 = x + attn
        m_in, _, _ = ln(b.ln_2, x1)
        hid = m_in @ b.mlp.c_fc.weight + b.mlp.c_fc.bias                 # 768 -> 3072
        act = torch.nn.functional.gelu(hid, approximate="tanh")
        mlp = act @ b.mlp.c_proj.weight + b.mlp.c_proj.bias              # 3072 -> 768
        x2 = x1 + mlp
        global best
        if layer is not None:                                           # search every head for "rates" -> "ECB"
            for h_ in range(H):
                wv = float(w[h_, n - 1, 1])
                if best is None or wv > best["weight_on_ECB"]:
                    best = {"layer": layer + 1, "head": h_ + 1, "weight_on_ECB": round(wv, 3),
                            "q": r(q[h_, n - 1]), "k": [r(k[h_, j]) for j in range(n)],
                            "dot": [round(float(q[h_, n - 1] @ k[h_, j]), 2) for j in range(n)],
                            "scaled": [round(float(s[h_, n - 1, j]), 2) for j in range(n)],
                            "exp": [round(math.exp(float(s[h_, n - 1, j]) - float(s[h_, n - 1].max())), 3) for j in range(n)],
                            "weights": [round(float(w[h_, n - 1, j]), 3) for j in range(n)],
                            "out": r(o[n - 1, h_ * dh:(h_ + 1) * dh])}
        rec = None
        if record:
            last = n - 1
            # the head where the last token looks hardest at a token other than the first
            hsel = int(torch.argmax(w[:, last, 1:].max(-1).values))
            rec = {"ln_mean": round(float(mu[last]), 3), "ln_std": round(float(sd[last]), 3), "ln_out": r(a_in[last]),
                   "head": hsel,
                   "q": r(q[hsel, last]), "k": [r(k[hsel, j]) for j in range(n)],
                   "dot": [round(float(q[hsel, last] @ k[hsel, j]), 2) for j in range(n)],
                   "scaled": [round(float(s[hsel, last, j]), 2) for j in range(n)],
                   "weights": [round(float(w[hsel, last, j]), 3) for j in range(n)],
                   "weights_all_heads": [[round(float(x_), 3) for x_ in w[h_, last]] for h_ in range(H)],
                   "masked_example": {"row": toks[1], "scores": [None if mask[1, j] else round(float(s[hsel, 1, j]), 2) for j in range(n)]},
                   "attn_out": r(attn[last]), "x_after_attn": r(x1[last]),
                   "mlp_hidden_positive": int((hid[last] > 0).sum()), "mlp_top": sorted(
                       [[int(i), round(float(act[last, i]), 2)] for i in torch.topk(act[last], 3).indices], key=lambda t: -t[1]),
                   "mlp_out": r(mlp[last]), "x_after_block": r(x2[last])}
        return x2, rec

    lens = []
    best = None
    for i, b in enumerate(T.h):
        x, rec = block(b, x, record=(i == 0), layer=i)
        if rec:
            out["block0"] = rec
        xf = T.ln_f(x[-1])                                              # logit lens after each block
        p = (xf @ T.wte.weight.T).softmax(-1)
        top = torch.topk(p, 3)
        lens.append({"after_block": i + 1, "top": [[tok.decode([int(j)]), round(float(v), 3)] for v, j in zip(top.values, top.indices)]})
    out["logit_lens"] = lens
    out["head_rates_to_ECB"] = best

    xf, mu, sd = ln(T.ln_f, x[-1])
    logits = xf @ T.wte.weight.T                                        # 768 -> 50,257 (tied to the embeddings)
    p = logits.softmax(-1)
    top = torch.topk(p, 5)
    out["final"] = {"x": r(xf), "top": [{"token": tok.decode([int(j)]), "logit": round(float(logits[j]), 2),
                                         "p": round(float(v), 3)} for v, j in zip(top.values, top.indices)],
                    "max_logit": round(float(logits.max()), 2), "sum_exp_note": "p = e^logit / sum over all 50,257"}
    ref = m(ids[None]).logits[0, -1]
    out["check_max_abs_diff_vs_library"] = float((ref - logits).abs().max())
(HERE / "w02_gpt2_walk.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps({k: out[k] for k in ("tokens", "ids", "params", "check_max_abs_diff_vs_library")}, indent=0))
print("best head", out["head_rates_to_ECB"])
print("block0 head", out["block0"]["head"], out["block0"]["weights"], out["block0"]["dot"], out["block0"]["scaled"])
print("mlp positive", out["block0"]["mlp_hidden_positive"], out["block0"]["mlp_top"])
for l in out["logit_lens"]:
    print(l)
print(out["final"]["top"])
