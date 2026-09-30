"""A tiny real run of byte-pair encoding, for the week 2 tokenizer clip (anim/src/w02_bpe.py) -> w02_bpe.json.

Start from single characters (a space is "_"), count neighbouring pairs inside words (never across
a space or a comma, as real tokenizers do), glue the most frequent (ties: the pair seen first),
repeat while some pair appears at least twice. Then cut a new word with the
learned merges, applied in the order they were learned.
"""
import json
from collections import Counter
from pathlib import Path

TEXT = "rates up, rates down, rates up"
NEW_WORD = "ratio"
SEP = {"_", ","}


def merge(seq, a, b):
    out, i = [], 0
    while i < len(seq):
        if i + 1 < len(seq) and seq[i] == a and seq[i + 1] == b:
            out.append(a + b); i += 2
        else:
            out.append(seq[i]); i += 1
    return out


seq = list(TEXT.replace(" ", "_"))
start = seq[:]
letters = sorted(set(seq))
steps = []
while True:
    pairs = [p for p in zip(seq, seq[1:]) if not (set(p) & SEP)]
    if not pairs:
        break
    counts = Counter(pairs)
    first = {p: i for i, p in reversed(list(enumerate(pairs)))}
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], first[kv[0]]))
    (a, b), n = ranked[0]
    if n < 2:
        break
    seq = merge(seq, a, b)
    steps.append({"pair": [a, b], "count": n, "piece": a + b, "top": [[x, y, c] for (x, y), c in ranked[:3]],
                  "seq": seq[:], "length": len(seq)})

cut = list(NEW_WORD)
for st in steps:
    cut = merge(cut, *st["pair"])

out = {"text": TEXT, "start": start, "start_pieces": len(start), "vocab": letters + [s["piece"] for s in steps],
       "steps": steps, "new_word": NEW_WORD, "new_word_pieces": cut}
(Path(__file__).parent / "w02_bpe.json").write_text(json.dumps(out, indent=1))
for s in steps:
    print(s["pair"], s["count"], s["length"], s["top"])
print(out["vocab"], cut)
