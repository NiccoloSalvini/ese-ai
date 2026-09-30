"""Week 2 — quantization for real: GPT-2's weights squeezed into MXFP4, the format gpt-oss ships in.

MXFP4: each weight is one of 16 values (a 4-bit float: 0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6), and every
block of 32 weights shares one scale, a power of two (8 bits). So 4 + 8/32 = 4.25 bits per weight.
We quantize every weight matrix inside the 12 blocks (the embeddings stay), then read the knobs
after "The ECB left rates" again. Writes w02_quant.json. Run with ~/.venvs/ese-ai-ml.
"""
import json, math
from pathlib import Path
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

HERE = Path(__file__).parent
GRID = torch.tensor([0, 0.5, 1, 1.5, 2, 3, 4, 6])
PROMPT = "The ECB left rates"


def mxfp4(w, block=32):
    flat = w.reshape(-1, block)
    amax = flat.abs().max(1, keepdim=True).values.clamp_min(1e-12)
    scale = 2.0 ** (torch.floor(torch.log2(amax)) - 2)                 # largest value lands near 4..6
    x = (flat / scale).clamp(-6, 6)
    idx = (x.abs().unsqueeze(-1) - GRID).abs().argmin(-1)
    q = GRID[idx] * x.sign() * scale
    return q.reshape(w.shape), scale


tok = GPT2TokenizerFast.from_pretrained("gpt2")
m = GPT2LMHeadModel.from_pretrained("gpt2").eval()
ids = tok(PROMPT, return_tensors="pt").input_ids


def knobs(model):
    with torch.no_grad():
        p = model(ids).logits[0, -1].softmax(-1)
    top = torch.topk(p, 5)
    return [[tok.decode([int(j)]).strip(), round(float(v), 3)] for v, j in zip(top.values, top.indices)]


before = knobs(m)
# one worked block: the first 32 weights of block 1's MLP, first neuron
w = m.transformer.h[0].mlp.c_fc.weight[:32, 0].detach().clone()
q, sc = mxfp4(w)
example = {"weights_16bit": [round(float(v), 4) for v in w[:8]], "scale": float(sc[0, 0]),
           "divided_by_scale": [round(float(v), 2) for v in (w[:8] / sc[0, 0])],
           "nearest_fp4": [float(v) for v in (q[:8] / sc[0, 0])],
           "back": [round(float(v), 4) for v in q[:8]],
           "mean_abs_error_block": round(float((q - w).abs().mean()), 5), "mean_abs_weight_block": round(float(w.abs().mean()), 5)}

n_q, err, mag = 0, 0.0, 0.0
with torch.no_grad():
    for b in m.transformer.h:
        for lin in (b.attn.c_attn, b.attn.c_proj, b.mlp.c_fc, b.mlp.c_proj):
            W = lin.weight
            qW, _ = mxfp4(W.T.contiguous())                              # blocks of 32 along the input dimension
            qW = qW.T
            err += float((qW - W).abs().sum()); mag += float(W.abs().sum()); n_q += W.numel()
            W.copy_(qW)
after = knobs(m)
total = sum(p.numel() for p in m.parameters())
out = {"prompt": PROMPT, "grid": GRID.tolist(), "block": 32, "bits_per_weight": 4 + 8 / 32,
       "example": example, "quantized_weights": n_q, "total_weights": total,
       "relative_error": round(err / mag, 3), "knobs_before": before, "knobs_after": after,
       "gpt_oss": {"params": 117e9, "gb_16bit": round(117e9 * 2 / 1e9), "gb_mxfp4": round(117e9 * 4.25 / 8 / 1e9, 1)}}
(HERE / "w02_quant.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
