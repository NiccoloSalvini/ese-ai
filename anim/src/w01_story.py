"""Week 1 clips for the running example — "is this card payment fraud?".

Numbers come from lectures/img/nn_story.json, written by nn_story.py, so the
clip shows exactly the arithmetic on the slides and in the notebook.
"""
import json
from pathlib import Path
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN

S = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/nn_story.json").read_text())
MONO = "Menlo"


def fmt(v):
    """signed term for a sum: '+ 0.5', '− 1'"""
    return ("− " if v < 0 else "+ ") + f"{abs(v):g}"


def num(v):
    return ("−" if v < 0 else "") + f"{abs(v):g}"


class PerceptronPayments(Scene):
    """Learning from mistakes, by hand: a first guess meets eight payments."""

    def construct(self):
        title = Text("Learning from mistakes, by hand", font_size=32, weight=BOLD).to_edge(UP, buff=0.3)
        self.add(title)

        head = ["", "large", "abroad", "device", "fraud"]
        rows = [[n] + [str(v) for v in x] + ["yes" if y else "no"] for n, x, y in S["payments"]]
        xs = [-6.4, -5.5, -4.5, -3.5, -2.5]
        table = VGroup()
        for r, row in enumerate([head] + rows):
            line = VGroup(*[Text(c, font_size=21, color=GREY if r == 0 else (RED if c == "yes" else WHITE),
                                 weight=BOLD if (r > 0 and j == 0) else NORMAL) for j, c in enumerate(row)])
            for j, m in enumerate(line):
                m.move_to([xs[j], 2.45 - r * 0.5, 0])
            table.add(line)
        self.play(FadeIn(table), run_time=0.8)

        labels = ["w large", "w abroad", "w device", "bias"]
        def weights_group(w, colour=GOLD):
            g = VGroup()
            for i, (lab, v) in enumerate(zip(labels, w)):
                t = VGroup(Text(lab, font_size=20, color=GREY), Text(num(v), font_size=32, color=colour, weight=BOLD))
                t.arrange(DOWN, buff=0.1).move_to([-0.6 + i * 1.75, 2.35, 0])
                g.add(t)
            return g
        wg = weights_group(list(S["start"][0]) + [S["start"][1]])
        eta = Text(f"learning rate η = {S['eta_p']:g}", font_size=20, color=GREY).move_to([2.0, 1.45, 0])
        self.play(FadeIn(wg), FadeIn(eta), run_time=0.8)

        LEFT_X = -1.5
        def at(m, y):
            return m.move_to([LEFT_X, y, 0], aligned_edge=LEFT)

        calc = verdict = rnd = pointer = None
        for r in S["perceptron"]:
            if r["epoch"] > S["rounds"] - 1:
                break
            idx = "ABCDEFGH".index(r["name"]) + 1
            anims = []
            if rnd is None or r["name"] == "A":
                new_rnd = Text(f"round {r['epoch']}", font_size=24, color=GOLD).move_to([-4.4, -2.35, 0])
                anims += ([FadeOut(rnd)] if rnd else []) + [FadeIn(new_rnd)]
                rnd = new_rnd
            box = SurroundingRectangle(table[idx], color=GOLD, buff=0.07, stroke_width=3)
            anims += [ReplacementTransform(pointer, box)] if pointer else [Create(box)]
            pointer = box
            *w, b = r["before"]
            terms = " + ".join(f"{num(wi)}·{xi}" for wi, xi in zip(w, r["x"]))
            new_calc = at(Text(f"score = {terms} {fmt(b)} = {num(r['z'])}", font=MONO, font_size=19), 0.75)
            anims += ([FadeOut(calc)] if calc else []) + ([FadeOut(verdict)] if verdict else []) + [FadeIn(new_calc)]
            calc = new_calc
            ok = r["err"] == 0
            self.play(*anims, run_time=0.3 if ok else 0.5)
            decision = "block" if r["yhat"] else "don’t block"
            verdict = at(Text(f"→ {decision}   " + ("✓" if ok else "✗ " + ("missed fraud" if r["y"] else "false alarm")),
                              font_size=24, color=GREEN if ok else RED, weight=BOLD), 0.1)
            self.play(FadeIn(verdict), run_time=0.2 if ok else 0.35)
            if ok:
                self.wait(0.15)
                continue
            *a, ab = r["after"]
            e = r["err"]
            lines = [f"weight ← weight + η·(fraud − decision)·answer"]
            for lab, wi, xi, ai in zip(["w large ", "w abroad", "w device"], w, r["x"], a):
                lines.append(f"{lab} = {num(wi)} + {S['eta_p']:g}·({e:+d})·{xi} = {num(ai)}")
            lines.append(f"bias     = {num(b)} + {S['eta_p']:g}·({e:+d})   = {num(ab)}")
            upd = VGroup(*[Text(l, font=MONO, font_size=17, color=GOLD, weight=BOLD if k == 0 else NORMAL)
                           for k, l in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            at(upd, -1.45)
            self.play(FadeIn(upd), run_time=0.45)
            new_w = weights_group(a + [ab], RED)
            self.play(FadeOut(wg), FadeIn(new_w), run_time=0.5)
            wg = new_w
            self.wait(1.4)
            calm = weights_group(a + [ab])
            self.play(FadeOut(upd), FadeOut(wg), FadeIn(calm), run_time=0.35)
            wg = calm

        done = Text(f"round {S['rounds']}: eight payments, no mistakes — the rule is learned",
                    font_size=24, color=GREEN, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeOut(calc), FadeOut(verdict), FadeOut(pointer), FadeIn(done), run_time=0.6)
        self.wait(2.2)


class LearningRate(Scene):
    """The same data, three step sizes."""

    def construct(self):
        title = Text("The learning rate: how big each nudge is", font_size=32, weight=BOLD).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 29, 5], y_range=[0, 5, 1], x_length=10.5, y_length=4.6,
                  axis_config={"color": GREY, "include_tip": False}).shift(DOWN * 0.3)
        xl = Text("training steps", font_size=20, color=GREY).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = Text("how wrong (loss)", font_size=20, color=GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.25)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        styles = {"0.3": (GOLD, "η = 0.3   too small: slow"), "3.0": (GREEN, "η = 3   about right"),
                  "20.0": (RED, "η = 20   too big: overshoots")}
        legend = VGroup()
        for i, (k, (col, lab)) in enumerate(styles.items()):
            h = S["lr"][k]
            pts = [ax.c2p(j, min(v, 5)) for j, v in enumerate(h)]
            curve = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
            dot = Dot(pts[-1], color=col)
            lg = Text(lab, font_size=22, color=col).move_to([3.4, 2.3 - i * 0.45, 0])
            legend.add(lg)
            self.play(Create(curve), FadeIn(lg), run_time=2.2, rate_func=linear)
            self.add(dot)
        self.wait(2.0)


class Faders(Scene):
    """The same nudge on text: one knob per possible next token."""

    def construct(self):
        F = S["faders"]
        toks = F["tokens"]
        title = Text("“… left rates” → ?   one knob per next token", font_size=30, weight=BOLD).to_edge(UP, buff=0.3)
        self.add(title)
        top, bot = 2.1, -1.9
        xs = [0.3 + i * 1.35 for i in range(len(toks))]
        cols = [RED, NAVY, NAVY, GREY, GREY]
        rails = VGroup(*[Line([x, bot, 0], [x, top, 0], color=GREY, stroke_width=6, stroke_opacity=0.35) for x in xs])
        names = VGroup(*[Text(tk, font_size=20).move_to([x, bot - 0.35, 0]) for tk, x in zip(toks, xs)])
        self.add(rails, names)

        def rects(ps):
            return VGroup(*[RoundedRectangle(width=0.7, height=0.28, corner_radius=0.05, fill_color=c, fill_opacity=1,
                                             stroke_width=0).move_to([x, bot + p * (top - bot), 0]) for p, x, c in zip(ps, xs, cols)])
        def labels(ps):
            return VGroup(*[Text(f"{p:.0%}", font_size=18).move_to([x + 0.62, bot + p * (top - bot), 0]) for p, x in zip(ps, xs)])

        r, l = rects(F["snaps"][0]["p"]), labels(F["snaps"][0]["p"])
        self.play(FadeIn(r), FadeIn(l), run_time=0.6)
        lines = VGroup(*[Text(f"{ctx} {y}", font_size=23, color=GREY) for ctx, y in F["sentences"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-4.3, 0.4, 0])
        self.add(lines)
        self.wait(0.8)
        for i, st in enumerate(F["steps"]):
            hl = lines[i].copy().set_color(RED if st["answer"] == "unchanged" else NAVY)
            nl = labels(st["p"])
            self.play(Transform(lines[i], hl), Transform(r, rects(st["p"])), FadeOut(l), run_time=0.9)
            self.play(FadeIn(nl), run_time=0.25)
            l = nl
            self.wait(0.5)
        fast = Text("… 40 passes over the same five sentences", font_size=22, color=GOLD).move_to([-4.3, -1.9, 0])
        nl = labels(F["snaps"][-1]["p"])
        self.play(FadeIn(fast), Transform(r, rects(F["snaps"][-1]["p"])), FadeOut(l), run_time=2.2)
        self.play(FadeIn(nl), run_time=0.3)
        end = Text("The knobs end where the text is: 3 in 5 said “unchanged”. Never seen → zero.", font_size=22, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(end), run_time=0.6)
        self.wait(2.5)
