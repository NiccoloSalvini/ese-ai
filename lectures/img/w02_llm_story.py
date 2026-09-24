"""Week 2 — inside an LLM. Real numbers from GPT-2 small (124M), the model the student runs in Colab.

Needs torch + transformers once; writes w02_llm_story.json, which the figures and slides read
(so they can be regenerated without the model). Deterministic: greedy decoding and fixed seeds.
"""
import json, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
OUT = {}

# ------------------------------------------------------------------ attention by hand (toy, 2 numbers per vector)
# "The bank raised rates because it" — the token "it" asks a question (query);
# every token shows a label (key) and carries a content (value).
TOKS = ["The", "bank", "raised", "rates", "because", "it"]
Q_IT = np.array([1.5, 0.0])                        # "it" is looking for: an actor that can fear
KEYS = np.array([[0.0, 0.2], [2.0, 0.0], [0.0, 1.0], [1.0, 0.5], [0.0, 0.5], [0.2, 0.0]])
VALS = np.array([[0, 0], [1, 0], [0, 0], [0, 1], [0, 0], [0, 0]], float)   # (is an institution, is a price)
scores = KEYS @ Q_IT
w = np.exp(scores) / np.exp(scores).sum()
OUT["toy_attention"] = dict(tokens=TOKS, query=Q_IT.tolist(), keys=KEYS.tolist(), values=VALS.tolist(),
                            scores=[round(float(s), 2) for s in scores], exp=[round(float(math.exp(s)), 2) for s in scores],
                            weights=[round(float(v), 3) for v in w], mixed=[round(float(v), 3) for v in w @ VALS])

if __name__ == "__main__":
    import torch
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    tok = GPT2TokenizerFast.from_pretrained("gpt2")
    m = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager")
    m.train(False)                                   # inference mode
    OUT["gpt2"] = dict(params=int(sum(p.numel() for p in m.parameters())), vocab=int(m.config.vocab_size),
                       layers=int(m.config.n_layer), heads=int(m.config.n_head), width=int(m.config.n_embd),
                       context=int(m.config.n_positions))

    # the real knobs after "The ECB left rates"
    prompt = "The ECB left rates"
    ids = tok(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        logits = m(ids).logits[0, -1]
    OUT["prompt"] = prompt
    OUT["prompt_tokens"] = [tok.decode([i]) for i in ids[0]]
    OUT["prompt_ids"] = ids[0].tolist()
    p = torch.softmax(logits, -1)
    top = torch.topk(p, 8)
    OUT["knobs"] = [dict(token=tok.decode([int(i)]), p=round(float(v), 3)) for v, i in zip(top.values, top.indices)]
    OUT["knobs_rest"] = round(1 - float(top.values.sum()), 3)
    # temperature applied to the whole vocabulary, read on the top five
    five = top.indices[:5]
    OUT["temperature"] = {}
    for T in (0.5, 1.0, 2.0):
        q = torch.softmax(logits / T, -1)
        OUT["temperature"][str(T)] = [round(float(q[i]), 3) for i in five]
    OUT["temperature_tokens"] = [tok.decode([int(i)]) for i in five]

    # generation: one token at a time
    greedy = m.generate(ids, max_new_tokens=12, do_sample=False, pad_token_id=tok.eos_token_id)
    OUT["greedy"] = tok.decode(greedy[0][ids.shape[1]:])
    samples = []
    for seed in (1, 2, 3):
        torch.manual_seed(seed)
        s = m.generate(ids, max_new_tokens=12, do_sample=True, temperature=1.0, top_k=0, pad_token_id=tok.eos_token_id)
        samples.append(tok.decode(s[0][ids.shape[1]:]))
    OUT["samples_T1"] = samples

    # embeddings: 22 single-token words, real GPT-2 vectors, flattened to 2-D
    words = [" bank", " banks", " lender", " loan", " credit", " debt", " mortgage", " Bitcoin", " crypto", " blockchain",
             " Ethereum", " Paris", " Rome", " Berlin", " London", " euro", " dollar", " yen", " inflation", " rates",
             " prices", " wages"]
    E = m.transformer.wte.weight.detach().numpy()
    X = np.array([E[tok.encode(wd)[0]] for wd in words])
    Xc = X - X.mean(0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    P = Xc @ Vt[:2].T
    OUT["embed"] = [dict(word=wd.strip(), x=round(float(a), 3), y=round(float(b), 3)) for wd, (a, b) in zip(words, P)]
    def cos(a, b):
        va, vb = E[tok.encode(a)[0]], E[tok.encode(b)[0]]
        return round(float(va @ vb / np.linalg.norm(va) / np.linalg.norm(vb)), 2)
    OUT["cosine"] = [dict(a=a.strip(), b=b.strip(), c=cos(a, b)) for a, b in
                     [(" bank", " lender"), (" bank", " Paris"), (" Bitcoin", " crypto"), (" euro", " dollar")]]

    # real attention: which head links "it" to "bank"?
    s = "The bank raised rates because it feared inflation"
    ids2 = tok(s, return_tensors="pt").input_ids
    toks2 = [tok.decode([i]) for i in ids2[0]]
    with torch.no_grad():
        att = m(ids2, output_attentions=True).attentions
    it, bank = toks2.index(" it"), toks2.index(" bank")
    best = max(((float(a[0, h, it, bank]), L, h) for L, a in enumerate(att) for h in range(a.shape[1])))
    _, L, h = best
    OUT["real_attention"] = dict(sentence=s, tokens=[t.strip() for t in toks2[:it + 1]], layer=L + 1, head=h + 1,
                                 weights=[round(float(v), 3) for v in att[L][0, h, it, :it + 1]])

    for k, v in OUT.items():
        print(k, v if not isinstance(v, list) or len(v) < 10 else f"[{len(v)} items]")
    (HERE / "w02_llm_story.json").write_text(json.dumps(OUT, indent=1, ensure_ascii=False))
