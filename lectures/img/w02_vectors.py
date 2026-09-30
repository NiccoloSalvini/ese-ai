"""The first four numbers of GPT-2's token vectors for "The ECB left rates" -> w02_vectors.json (clip B)."""
import json
from pathlib import Path
import transformers
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

tok = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
prompt = "The ECB left rates"
ids = tok(prompt).input_ids
E = model.transformer.wte.weight.detach()
out = {"model": "gpt2", "prompt": prompt, "width": E.shape[1], "transformers": transformers.__version__,
       "tokens": [{"token": tok.decode([i]).strip(), "id": i, "first4": [round(float(v), 4) for v in E[i, :4]]} for i in ids]}
(Path(__file__).parent / "w02_vectors.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out["tokens"]))
