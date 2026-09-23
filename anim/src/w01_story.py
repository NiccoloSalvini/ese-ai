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
    """Learning from mistakes, by hand: the old rule meets four payments."""

    def construct(self):
        title = Text("Learning from mistakes, by hand", font_size=34, weight=BOLD).to_edge(UP, buff=0.35)
        self.add(title)

        # the data table, left
        head = ["", "large?", "abroad?", "fraud?"]
        rows = [[n, str(a), str(b), "yes" if y else "no"] for n, a, b, y in S["payments"]]
        xs = [-6.3, -5.2, -4.0, -2.8]
        table = VGroup()
        for r, row in enumerate([head] + rows):
            line = VGroup(*[Text(c, font_size=24, color=GREY if r == 0 else (RED if c == "yes" else WHITE),
                                 weight=BOLD if (r > 0 and j == 0) else NORMAL)
                            for j, c in enumerate(row)])
            for j, m in enumerate(line):
                m.move_to([xs[j], 1.9 - r * 0.62, 0])
            table.add(line)
        self.play(FadeIn(table), run_time=0.8)

        # the weights, top right
        labels = ["w large", "w abroad", "bias"]
        def weights_group(w, colour=GOLD):
            g = VGroup()
            for i, (lab, v) in enumerate(zip(labels, w)):
                t = VGroup(Text(lab, font_size=22, color=GREY), Text(num(v), font_size=34, color=colour, weight=BOLD))
                t.arrange(DOWN, buff=0.12).move_to([0.6 + i * 2.0, 2.0, 0])
                g.add(t)
            return g
        wg = weights_group(S["start"])
        eta = Text(f"learning rate η = {S['eta_p']:g}", font_size=22, color=GREY).move_to([2.6, 1.05, 0])
        self.play(FadeIn(wg), FadeIn(eta), run_time=0.8)

        LEFT_X = -1.4
        def at(m, y):
            return m.move_to([LEFT_X, y, 0], aligned_edge=LEFT)

        calc = verdict = rnd = None
        pointer = None
        for r in [r for r in S["perceptron"] if r["epoch"] <= 2]:
            idx = "ABCD".index(r["name"]) + 1
            anims = []
            if rnd is None or r["name"] == "A":
                new_rnd = Text(f"round {r['epoch']}", font_size=24, color=GOLD).move_to([-4.5, -1.35, 0])
                anims += [FadeOut(rnd)] if rnd else []
                anims += [FadeIn(new_rnd)]
                rnd = new_rnd
            box = SurroundingRectangle(table[idx], color=GOLD, buff=0.1, stroke_width=3)
            anims += [ReplacementTransform(pointer, box)] if pointer else [Create(box)]
            pointer = box
            b1, b2, bb = r["before"]
            new_calc = at(Text(f"score = {b1:g}·{r['x1']} + {b2:g}·{r['x2']} {fmt(bb)} = {num(r['z'])}", font=MONO, font_size=22), 0.15)
            anims += [FadeOut(calc)] if calc else []
            anims += [FadeOut(verdict)] if verdict else []
            anims += [FadeIn(new_calc)]
            calc = new_calc
            self.play(*anims, run_time=0.55)
            ok = r["err"] == 0
            decision = "block" if r["yhat"] else "don’t block"
            verdict = at(Text(f"→ {decision}   " + ("✓" if ok else "✗ " + ("missed fraud" if r["y"] else "false alarm")),
                              font_size=28, color=GREEN if ok else RED, weight=BOLD), -0.6)
            self.play(FadeIn(verdict), run_time=0.35)
            if ok:
                self.wait(0.5)
                continue
            a1, a2, ab = r["after"]
            upd = VGroup(
                Text(f"w ← w + η · (fraud − decision) · x", font=MONO, font_size=20, color=GOLD),
                Text(f"  = w + {S['eta_p']:g} · ({r['err']:+d}) · ({r['x1']}, {r['x2']}, 1)", font=MONO, font_size=20, color=GOLD),
                Text(f"  → ({num(a1)}, {num(a2)}, {num(ab)})", font=MONO, font_size=20, color=GOLD, weight=BOLD),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            at(upd, -1.9)
            self.play(FadeIn(upd), run_time=0.5)
            self.wait(0.6)
            new_w = weights_group([a1, a2, ab], RED)
            self.play(FadeOut(wg), FadeIn(new_w), run_time=0.6)
            wg = new_w
            self.wait(1.2)
            calm = weights_group([a1, a2, ab])
            self.play(FadeOut(upd), FadeOut(wg), FadeIn(calm), run_time=0.4)
            wg = calm

        done = Text("round 3: four payments, no mistakes — the rule is learned", font_size=26, color=GREEN, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeOut(calc), FadeOut(verdict), FadeOut(pointer), FadeIn(done), run_time=0.6)
        self.wait(2.0)


class LearningRate(Scene):
    """The same data, three step sizes."""

    def construct(self):
        title = Text("The learning rate: how big each nudge is", font_size=32, weight=BOLD).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 29, 5], y_range=[0, 2.6, 0.5], x_length=10.5, y_length=4.6,
                  axis_config={"color": GREY, "include_tip": False}).shift(DOWN * 0.3)
        xl = Text("training steps", font_size=20, color=GREY).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = Text("how wrong (loss)", font_size=20, color=GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.25)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        styles = {"0.3": (GOLD, "η = 0.3   too small: slow"), "3.0": (GREEN, "η = 3   about right"),
                  "20.0": (RED, "η = 20   too big: overshoots")}
        legend = VGroup()
        for i, (k, (col, lab)) in enumerate(styles.items()):
            h = S["lr"][k]
            pts = [ax.c2p(j, min(v, 2.6)) for j, v in enumerate(h)]
            curve = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
            dot = Dot(pts[-1], color=col)
            lg = Text(lab, font_size=22, color=col).move_to([3.4, 2.3 - i * 0.45, 0])
            legend.add(lg)
            self.play(Create(curve), FadeIn(lg), run_time=2.2, rate_func=linear)
            self.add(dot)
        self.wait(2.0)
