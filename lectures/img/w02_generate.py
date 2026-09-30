"""Week 2 — one token at a time. GPT-2 small's real knobs at each greedy step after "The ECB left rates".

Writes w02_generate.json (top-5 next pieces + probabilities for the first STEPS greedy steps, and the
full greedy continuation) for the manim clip anim/src/w02_generate.py. Needs torch + transformers once.
"""
import json
from pathlib import Path

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

HERE = Path(__file__).parent
PROMPT, STEPS, TOP, TAIL = "The ECB left rates", 4, 5, 12

tok = GPT2TokenizerFast.from_pretrained("gpt2")
m = GPT2LMHeadModel.from_pretrained("gpt2")
m.train(False)

ids = tok(PROMPT, return_tensors="pt").input_ids
steps = []
with torch.no_grad():
    for i in range(TAIL):
        p = torch.softmax(m(ids).logits[0, -1], -1)
        top = torch.topk(p, TOP)
        if i < STEPS:
            steps.append(dict(text=tok.decode(ids[0]),
                              knobs=[dict(token=tok.decode([int(t)]), p=round(float(v), 3)) for v, t in zip(top.values, top.indices)]))
        ids = torch.cat([ids, top.indices[:1].view(1, 1)], 1)

OUT = dict(prompt=PROMPT, steps=steps, greedy=tok.decode(ids[0])[len(PROMPT):])
(HERE / "w02_generate.json").write_text(json.dumps(OUT, indent=1))
print(json.dumps(OUT, indent=1))
