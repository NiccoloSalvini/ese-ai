"""Week 2 — the same small model before and after post-training, on the same questions.

Qwen2.5-0.5B (pre-trained only: a base model) vs Qwen2.5-0.5B-Instruct (the same model after
supervised fine-tuning and RL). Same size, same pre-training — only post-training differs.
Greedy decoding, so the output is deterministic. Writes w02_base_vs_chat.json for the clip.

Run once with torch + transformers (e.g. ~/.venvs/ese-ai-ml/bin/python w02_base_vs_chat.py).
"""
import datetime, json
from pathlib import Path

import torch, transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = Path(__file__).parent
BASE, CHAT = "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-0.5B-Instruct"
QUESTIONS = ["What is the capital of France?", "Should I buy Bitcoin today?"]
NEW = 40


def load(mid):
    tok = AutoTokenizer.from_pretrained(mid)
    model = AutoModelForCausalLM.from_pretrained(mid, torch_dtype=torch.float32)
    model.train(False)
    return tok, model


def generate(tok, model, text):
    ids = tok(text, return_tensors="pt").input_ids
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=NEW, do_sample=False, pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)


torch.manual_seed(0)
rows = []
tb, mb = load(BASE)
base_out = [generate(tb, mb, q) for q in QUESTIONS]          # raw continuation of the text
del mb
tc, mc = load(CHAT)
chat_out = [generate(tc, mc, tc.apply_chat_template([{"role": "user", "content": q}],
                                                      tokenize=False, add_generation_prompt=True))
            for q in QUESTIONS]

for q, b, c in zip(QUESTIONS, base_out, chat_out):
    rows.append({"question": q, "base": b, "chat": c})
    print(f"\nQ: {q}\n  BASE : {b!r}\n  CHAT : {c!r}")

json.dump({"base_model": BASE, "chat_model": CHAT, "max_new_tokens": NEW, "decoding": "greedy",
           "date": datetime.date.today().isoformat(), "transformers": transformers.__version__,
           "torch": torch.__version__, "rows": rows},
          open(HERE / "w02_base_vs_chat.json", "w"), indent=1, ensure_ascii=False)
