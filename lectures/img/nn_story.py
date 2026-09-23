"""One running example for week 1, from a single neuron to an LLM.

"Is this card payment fraud?"  Every number used in the slides, the figures,
the manim clips and the notebook comes from this file, so they cannot drift
apart. Run it to print the story and write nn_story.json next to it.
"""
import json, math
from pathlib import Path

# ---------------------------------------------------------------- 1. the data
# two yes/no questions: large = over EUR 1,000; abroad = paid abroad; fraud = 1
PAYMENTS = [("A", 0, 0, 0), ("B", 1, 0, 0), ("C", 0, 1, 0), ("D", 1, 1, 1)]
# real data is messier: E is a customer on holiday — large, abroad, and genuine
NOISY = PAYMENTS + [("E", 1, 1, 0)]
LR_ETAS = (0.3, 3.0, 20.0)  # too small, about right, too large
START = (1.0, 0.0, -1.0)   # a first guess: only size matters (it blocks nothing yet)
ETA_P = 0.5                # perceptron learning rate

def sig(z): return 1 / (1 + math.exp(-max(min(z, 50), -50)))

# ---------------------------------------------------------------- 2. perceptron by hand
def perceptron(w1=START[0], w2=START[1], b=START[2], eta=ETA_P, max_epochs=10):
    """Step activation: block if score > 0. Rule: w <- w + eta*(y - yhat)*x."""
    trace = []
    for epoch in range(1, max_epochs + 1):
        mistakes = 0
        for name, x1, x2, y in PAYMENTS:
            z = w1 * x1 + w2 * x2 + b
            yhat = 1 if z > 0 else 0
            err = y - yhat
            row = dict(epoch=epoch, name=name, x1=x1, x2=x2, y=y, z=round(z, 2), yhat=yhat, err=err,
                       before=(round(w1, 2), round(w2, 2), round(b, 2)))
            if err:
                w1 += eta * err * x1; w2 += eta * err * x2; b += eta * err
                mistakes += 1
            row["after"] = (round(w1, 2), round(w2, 2), round(b, 2))
            trace.append(row)
        if mistakes == 0:
            break
    return trace, (round(w1, 2), round(w2, 2), round(b, 2))

# ---------------------------------------------------------------- 3. one gradient step by hand (sigmoid + log loss)
def one_step(w1, w2, b, eta, pay):
    name, x1, x2, y = pay
    z = w1 * x1 + w2 * x2 + b
    p = sig(z)
    loss = -math.log(p) if y == 1 else -math.log(1 - p)
    g = p - y                          # dL/dz
    grads = dict(w1=g * x1, w2=g * x2, b=g)
    new = dict(w1=w1 - eta * grads["w1"], w2=w2 - eta * grads["w2"], b=b - eta * grads["b"])
    p_new = sig(new["w1"] * x1 + new["w2"] * x2 + new["b"])
    return dict(pay=name, x1=x1, x2=x2, y=y, w=(w1, w2, b), z=z, p=p, loss=loss, dz=g,
                grads=grads, eta=eta, new=new, p_new=p_new)

def total_loss(w1, w2, b, data=NOISY):
    L = 0
    for _, x1, x2, y in data:
        p = min(max(sig(w1 * x1 + w2 * x2 + b), 1e-12), 1 - 1e-12)
        L += -math.log(p) if y else -math.log(1 - p)
    return L / len(data)

def train(eta, steps=60, w=(0.0, 0.0, 0.0), data=NOISY):
    w1, w2, b = w; hist = []
    for _ in range(steps):
        hist.append(round(total_loss(w1, w2, b, data), 4))
        g1 = g2 = gb = 0
        for _, x1, x2, y in data:
            d = sig(w1 * x1 + w2 * x2 + b) - y
            g1 += d * x1; g2 += d * x2; gb += d
        n = len(data)
        w1 -= eta * g1 / n; w2 -= eta * g2 / n; b -= eta * gb / n
    return hist, (w1, w2, b)

# ---------------------------------------------------------------- 4. a pattern one neuron cannot draw
# card testing: a fraudster tries the card with a tiny amount, then spends a large one.
AMOUNTS = [0.01, 0.02, 0.05, 0.3, 0.6, 0.9, 1.2, 1.5, 2.2, 2.6, 3.0]
FRAUD2  = [1,    1,    1,    0,   0,   0,   0,   0,   1,   1,   1]
# two hidden neurons, set by hand so the story is readable:
#   h_small = sig(-10*(amount - 0.20))   "is it tiny?"
#   h_large = sig( 10*(amount - 1.9))    "is it large?"
#   p = sig(8*h_small + 8*h_large - 4)   "tiny OR large"
HIDDEN = dict(small=(-10.0, 2.0), large=(10.0, -19.0), out=(8.0, 8.0, -4.0))

def hidden_net(a):
    hs = sig(HIDDEN["small"][0] * a + HIDDEN["small"][1])
    hl = sig(HIDDEN["large"][0] * a + HIDDEN["large"][1])
    ws, wl, bo = HIDDEN["out"]
    return hs, hl, sig(ws * hs + wl * hl + bo)

if __name__ == "__main__":
    trace, final = perceptron()
    print(f"PERCEPTRON (eta = {ETA_P}, start at {START})")
    for r in trace:
        mark = "WRONG" if r["err"] else "ok"
        print(f"  epoch {r['epoch']} {r['name']}  z={r['z']:+.2f}  block={r['yhat']}  fraud={r['y']}  {mark:5s}  w {r['before']} -> {r['after']}")
    print("  final", final)

    print("\nSIGMOID at the perceptron's final weights")
    probs = {}
    for name, x1, x2, y in PAYMENTS:
        z = final[0]*x1 + final[1]*x2 + final[2]
        probs[name] = round(sig(z), 2)
        print(f"  {name}: z={z:+.1f}  p={sig(z):.2f}  fraud={y}")
    step = one_step(*final, 1.0, PAYMENTS[3])
    print(f"\nONE GRADIENT STEP on payment D, from w={final}, eta=1.0")
    print(f"  z={step['z']:.2f}  p={step['p']:.2f}  loss={step['loss']:.3f}  dL/dz=p-y={step['dz']:.2f}")
    print("  grads", {k: round(v, 2) for k, v in step["grads"].items()}, " new", {k: round(v, 2) for k, v in step["new"].items()},
          f" p_new={step['p_new']:.2f}")

    # backprop graph for payment D at the perceptron's final weights
    w1, w2, b = final; x1, x2, y = 1, 1, 1
    m1, m2 = x1*w1, x2*w2; s12 = m1 + m2; z = s12 + b; pD = sig(z); L = -math.log(pD)
    dL_dp = -1/pD; dp_dz = pD*(1-pD); dz = dL_dp*dp_dz
    graph = dict(x1=x1, x2=x2, w1=w1, w2=w2, b=b, m1=m1, m2=m2, s=s12, z=z, p=pD, L=L,
                 g_p=dL_dp, g_z=dz, g_b=dz, g_s=dz, g_m1=dz, g_m2=dz, g_w1=dz*x1, g_w2=dz*x2)
    print("\nBACKPROP on D:", {k: round(v, 2) for k, v in graph.items()})

    print("\nLEARNING RATE — average loss over A-E (E: holiday, genuine), from the perceptron's weights")
    lr = {}
    for eta in LR_ETAS:
        h, w = train(eta, steps=30, w=final)
        lr[str(eta)] = h
        print(f"  eta={eta:<5} loss steps 0-9: {h[:10]}  end {h[-1]}")

    print("\nTWO HIDDEN NEURONS on card testing")
    ok = 0
    for a, y in zip(AMOUNTS, FRAUD2):
        hs, hl, p = hidden_net(a)
        ok += (p >= 0.5) == y
        print(f"  amount {a:5.2f}  tiny? {hs:.2f}  large? {hl:.2f}  -> p(fraud) {p:.2f}   fraud={y}")
    print(f"  correct {ok}/{len(AMOUNTS)}; parameters = 2*2 (hidden) + 3 (output) = 7")

    out = dict(payments=PAYMENTS, start=START, eta_p=ETA_P, perceptron=trace, perceptron_final=final,
               probs=probs, step=step, graph=graph,
               lr=lr, amounts=AMOUNTS, fraud2=FRAUD2, hidden=HIDDEN)
    (Path(__file__).parent / "nn_story.json").write_text(json.dumps(out, indent=1))
