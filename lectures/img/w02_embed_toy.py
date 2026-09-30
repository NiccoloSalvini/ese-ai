"""A toy that builds word vectors from scratch, then lets context move them — for the week 2
embedding and attention clips (anim/src/w02_embed.py). Writes w02_embed_toy.json.

1. Embeddings: every word starts at a random place on a 2-D map. The training loop is last week's:
   guess which words appear near this one, measure how wrong, blame, nudge. Words that keep the
   same company end up close. "bank" keeps company with both money words and river words.
2. Attention (simplified): in a sentence, each word's new place is an average of the words'
   places, weighted by how similar they are (similarity -> shares of 100%, the knobs' squash).
   Real models first learn *which* similarity to look for; the arithmetic is the same.
"""
import json
import numpy as np
from pathlib import Path

SENTS = [
    "the bank raised rates", "the lender raised rates", "the bank cut rates", "the lender cut rates",
    "the bank gave a loan", "the lender gave a loan",
    "the river flooded the bank", "the river flooded the shore", "water covered the bank",
    "water covered the shore", "we sat on the bank of the river", "we sat on the shore of the river",
]
STOP = {"the", "a", "of", "on", "we"}
WINDOW, DIM, EPOCHS, LR, SEED = 2, 2, 400, 0.05, 3

words = sorted({w for s in SENTS for w in s.split() if w not in STOP})
ix = {w: i for i, w in enumerate(words)}
pairs = []
for s in SENTS:
    toks = [w for w in s.split() if w not in STOP]
    for i, w in enumerate(toks):
        for j in range(max(0, i - WINDOW), min(len(toks), i + WINDOW + 1)):
            if j != i:
                pairs.append((ix[w], ix[toks[j]]))

rng = np.random.default_rng(SEED)
E = rng.normal(0, 0.5, (len(words), DIM))      # the map: one row per word
O = rng.normal(0, 0.5, (len(words), DIM))      # "which neighbour" knobs
snaps, losses = {0: E.copy()}, []
for ep in range(1, EPOCHS + 1):
    loss = 0.0
    for c, o in pairs:                          # guess the neighbour of c
        z = O @ E[c]; p = np.exp(z - z.max()); p /= p.sum()
        loss -= np.log(p[o])
        g = p.copy(); g[o] -= 1                 # blame
        gE = O.T @ g; O -= LR * np.outer(g, E[c]); E[c] -= LR * gE   # nudge
    losses.append(loss / len(pairs))
    if ep in (5, 20, 60, 150, EPOCHS):
        snaps[ep] = E.copy()

def cos(a, b):
    return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))

def attend(sentence, focus):
    """Relevance = how strongly the loop learned that each word appears near `focus` (E[focus] . O[w]).
    Shares = relevance through the knobs' squash. The word keeps its place and ADDS the mix of the
    others, half-weight: new = old + 0.5 * (mix - old). Real models do the same, with more numbers."""
    toks = [w for w in sentence.split() if w not in STOP]
    others = [w for w in toks if w != focus]
    rel = np.array([E[ix[focus]] @ O[ix[w]] for w in others])
    share = np.exp(rel - rel.max()); share /= share.sum()
    mix = share @ np.array([E[ix[w]] for w in others])
    old = E[ix[focus]]; new = old + 0.5 * (mix - old)
    near = {w: round(float(np.linalg.norm(new - E[ix[w]])), 2) for w in ("lender", "shore")}
    return {"sentence": sentence, "tokens": toks, "focus": focus, "others": others,
            "relevance": rel.round(2).tolist(), "share": share.round(3).tolist(),
            "old": old.round(3).tolist(), "mix": mix.round(3).tolist(), "new": new.round(3).tolist(),
            "distance_after": near,
            "distance_before": {w: round(float(np.linalg.norm(old - E[ix[w]])), 2) for w in ("lender", "shore")}}

out = {"sentences": SENTS, "stop": sorted(STOP), "words": words, "window": WINDOW, "epochs": EPOCHS,
       "snapshots": {str(k): v.round(3).tolist() for k, v in snaps.items()},
       "loss": [round(losses[0], 3), round(losses[-1], 3)],
       "attention": [attend("the bank raised rates", "bank"), attend("the river flooded the bank", "bank")],
       "cos": {f"{a}-{b}": round(cos(E[ix[a]], E[ix[b]]), 2) for a, b in
               [("bank", "lender"), ("bank", "shore"), ("lender", "shore"), ("rates", "river")]}}
(Path(__file__).parent / "w02_embed_toy.json").write_text(json.dumps(out, indent=1))
for w in words:
    print(f"{w:8} {E[ix[w]].round(2)}")
print("loss", out["loss"], out["cos"])
for a in out["attention"]:
    print(a["sentence"], dict(zip(a["others"], a["share"])), a["old"], "->", a["new"], "before", a["distance_before"], "after", a["distance_after"])
