"""One running example for week 1, from a single neuron to an LLM.

"Is this card payment fraud?"  Every number used in the slides, the figures,
the manim clips and the notebook comes from this file, so they cannot drift
apart. Run it to print the story and write nn_story.json next to it.
"""
import json, math
from pathlib import Path

# ---------------------------------------------------------------- 1. the data
# three yes/no red flags; the hidden truth is "fraud when at least two are on"
FEATURES = ["large", "abroad", "new device"]
PAYMENTS = [("A", (0, 0, 0), 0), ("B", (1, 0, 0), 0), ("C", (0, 1, 0), 0), ("D", (0, 0, 1), 0),
            ("E", (1, 1, 0), 1), ("F", (1, 0, 1), 1), ("G", (0, 1, 1), 1), ("H", (1, 1, 1), 1)]
# real data is messier: I is a customer on holiday — large, abroad, genuine
NOISY = PAYMENTS + [("I", (1, 1, 0), 0)]
START = ((1.0, 0.0, 0.0), -1.0)   # a first guess: only size matters
ETA_P = 0.5                       # perceptron learning rate
LR_ETAS = (0.3, 3.0, 20.0)        # too small, about right, too large


def sig(z): return 1 / (1 + math.exp(-max(min(z, 50), -50)))
def dot(w, x): return sum(a * b for a, b in zip(w, x))


# ---------------------------------------------------------------- 2. perceptron by hand
def perceptron(w=START[0], b=START[1], eta=ETA_P, max_epochs=10):
    """Step activation: block if score > 0. Rule: w <- w + eta*(fraud - decision)*x."""
    w, trace = list(w), []
    for epoch in range(1, max_epochs + 1):
        mistakes = 0
        for name, x, y in PAYMENTS:
            z = dot(w, x) + b
            yhat = 1 if z > 0 else 0
            err = y - yhat
            row = dict(epoch=epoch, name=name, x=x, y=y, z=round(z, 2), yhat=yhat, err=err,
                       before=[round(v, 2) for v in w] + [round(b, 2)])
            if err:
                w = [wi + eta * err * xi for wi, xi in zip(w, x)]
                b += eta * err
                mistakes += 1
            row["after"] = [round(v, 2) for v in w] + [round(b, 2)]
            trace.append(row)
        if mistakes == 0:
            break
    return trace, [round(v, 2) for v in w] + [round(b, 2)]


# ---------------------------------------------------------------- 3. loss, gradient, training
def probs(wb, data=PAYMENTS):
    *w, b = wb
    return {n: sig(dot(w, x) + b) for n, x, _ in data}

def loss_one(p, y):
    p = min(max(p, 1e-12), 1 - 1e-12)
    return -math.log(p) if y else -math.log(1 - p)

def mean_loss(wb, data=PAYMENTS):
    ps = probs(wb, data)
    return sum(loss_one(ps[n], y) for n, _, y in data) / len(data)

def one_step(wb, eta, pay):
    *w, b = wb
    name, x, y = pay
    p = sig(dot(w, x) + b)
    g = p - y
    grads = [g * xi for xi in x] + [g]
    new = [v - eta * gv for v, gv in zip(list(w) + [b], grads)]
    return dict(pay=name, x=x, y=y, before=list(w) + [b], z=dot(w, x) + b, p=p, loss=loss_one(p, y), dz=g,
                grads=grads, eta=eta, new=new, p_new=sig(dot(new[:-1], x) + new[-1]))

def train(eta, steps, wb, data=PAYMENTS):
    *w, b = wb
    hist = []
    for _ in range(steps):
        hist.append(round(mean_loss(list(w) + [b], data), 4))
        gw, gb = [0.0] * len(w), 0.0
        for _, x, y in data:
            d = sig(dot(w, x) + b) - y
            gw = [g + d * xi for g, xi in zip(gw, x)]
            gb += d
        n = len(data)
        w = [wi - eta * g / n for wi, g in zip(w, gw)]
        b -= eta * gb / n
    return hist, list(w) + [b]


# ---------------------------------------------------------------- 4. a pattern one neuron cannot draw
# card testing: a fraudster tries the card with a tiny amount, then spends a large one.
AMOUNTS = [0.01, 0.02, 0.05, 0.3, 0.6, 0.9, 1.2, 1.5, 2.2, 2.6, 3.0]
FRAUD2  = [1,    1,    1,    0,   0,   0,   0,   0,   1,   1,   1]
HIDDEN = dict(small=(-10.0, 2.0), large=(10.0, -19.0), out=(8.0, 8.0, -4.0))

def hidden_net(a):
    hs = sig(HIDDEN["small"][0] * a + HIDDEN["small"][1])
    hl = sig(HIDDEN["large"][0] * a + HIDDEN["large"][1])
    ws, wl, bo = HIDDEN["out"]
    return hs, hl, sig(ws * hs + wl * hl + bo)


if __name__ == "__main__":
    trace, final = perceptron()
    print(f"PERCEPTRON  start {START}  eta {ETA_P}")
    for r in trace:
        if r["err"]:
            print(f"  round {r['epoch']} {r['name']}{r['x']} score {r['z']:+.1f} -> {'block' if r['yhat'] else 'pass'}"
                  f"  fraud={r['y']}  {'missed fraud' if r['y'] else 'false alarm'}  -> {r['after']}")
    rounds = max(r["epoch"] for r in trace)
    print(f"  round {rounds}: no mistakes. final {final}")

    p_final = probs(final)
    loss_before = {n: loss_one(p_final[n], y) for n, _, y in PAYMENTS}
    avg_before = mean_loss(final)
    TRAIN_ETA, TRAIN_STEPS = 3.0, 200
    _, trained = train(TRAIN_ETA, TRAIN_STEPS, final)
    p_trained = probs(trained)
    avg_after = mean_loss(trained)
    print("\nSIGMOID + LOSS at the perceptron's weights, and after training")
    for n, x, y in PAYMENTS:
        print(f"  {n}{x} fraud={y}  p={p_final[n]:.2f}  loss={loss_before[n]:.2f}   | trained p={p_trained[n]:.2f}")
    print(f"  average loss {avg_before:.2f} -> {avg_after:.2f} after {TRAIN_STEPS} steps at eta {TRAIN_ETA}; trained weights {[round(v,2) for v in trained]}")

    step = one_step(final, 1.0, PAYMENTS[4])  # payment E
    print(f"\nONE STEP on E, eta 1: p={step['p']:.2f} dz={step['dz']:.2f} grads {[round(g,2) for g in step['grads']]} "
          f"new {[round(v,2) for v in step['new']]} p_new={step['p_new']:.2f}")

    *w, b = final; x = PAYMENTS[4][1]; y = PAYMENTS[4][2]
    m = [wi * xi for wi, xi in zip(w, x)]; s = sum(m); z = s + b; p = sig(z); L = -math.log(p)
    dz = p - y
    graph = dict(x=x, w=w, b=b, m=m, s=s, z=z, p=p, L=L, g_p=-1 / p, g_z=dz, g_b=dz, g_s=dz,
                 g_m=[dz] * 3, g_w=[dz * xi for xi in x])
    print("BACKPROP on E:", {k: (v if not isinstance(v, float) else round(v, 2)) for k, v in graph.items()})

    print("\nLEARNING RATE on the 9 payments (I: holiday, genuine), from the perceptron's weights")
    lr = {}
    for eta in LR_ETAS:
        h, _ = train(eta, 30, final, NOISY)
        lr[str(eta)] = h
        print(f"  eta={eta:<5} {h[:10]} ... {h[-1]}")

    print("\nTWO HIDDEN NEURONS on card testing")
    ok = sum((hidden_net(a)[2] >= 0.5) == y for a, y in zip(AMOUNTS, FRAUD2))
    print(f"  correct {ok}/{len(AMOUNTS)}; parameters 2*2 + 3 = 7")

    out = dict(features=FEATURES, payments=PAYMENTS, start=START, eta_p=ETA_P, perceptron=trace,
               rounds=rounds, perceptron_final=final,
               probs={n: round(v, 4) for n, v in p_final.items()}, loss_before={n: round(v, 4) for n, v in loss_before.items()},
               avg_before=avg_before, trained=trained, train_eta=TRAIN_ETA, train_steps=TRAIN_STEPS,
               probs_trained={n: round(v, 4) for n, v in p_trained.items()}, avg_after=avg_after,
               step=step, graph=graph, lr=lr, amounts=AMOUNTS, fraud2=FRAUD2, hidden=HIDDEN)
    (Path(__file__).parent / "nn_story.json").write_text(json.dumps(out, indent=1))
