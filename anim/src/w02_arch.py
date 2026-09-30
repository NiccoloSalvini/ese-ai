"""Week 2 clip B — a sentence travelling through a GPT. White stage, slow, for a non-technical reader.

Layout follows lectures/img/w02-block.svg (figs_w02llm.block): words → vectors → one block
(attention, neurons) → stacked → last vector → the knobs. Numbers from w02_llm_story.json.
"""
import json
from pathlib import Path
from manim import *

S = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_llm_story.json").read_text())
V = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_vectors.json").read_text())
INK, RED, NAVY, GOLD, MUTED, PAPER = "#363636", "#AF1F25", "#2471a3", "#CDBA80", "#7a7f85", "#f7f5ef"
GOLDDK = "#a8955a"
SANS = "Helvetica Neue"
MONO = "Menlo"


def T(s, size=26, color=INK, weight=NORMAL, font=SANS):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


class Architecture(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        g = S["gpt2"]
        words = [w.strip() for w in S["prompt_tokens"]]
        ids = S["prompt_ids"]
        xs = [-5.0, -3.0, -1.0, 1.0]

        cap = T("", 26)

        def caption(s):
            nonlocal cap
            new = T(s, 26).move_to([0, -3.55, 0])
            if new.width > 13.4:
                new.scale_to_fit_width(13.4)
            anims = [FadeOut(cap)] if len(cap) else []
            self.play(*anims, FadeIn(new), run_time=1.2)
            cap = new

        # 1 · tokens and ids
        wd = VGroup(*[T(w, 34, INK, BOLD).move_to([x, 3.68, 0]) for w, x in zip(words, xs)])
        idt = VGroup(*[T(str(i), 24, MUTED, font=MONO).move_to([x, 3.2, 0]) for i, x in zip(ids, xs)])
        self.play(FadeIn(wd), run_time=1.8)
        caption("1 · The text is cut into pieces — tokens — and each gets a number.")
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.2) for i in idt], lag_ratio=0.3), run_time=2.2)
        self.wait(2.5)

        # 2 · vectors
        vecs = VGroup()
        for tk, x in zip(V["tokens"], xs):
            rows = VGroup(*[T(f"{v:.2f}".replace("-", "−"), 22, NAVY, font=MONO) for v in tk["first4"]],
                          T("…", 22, NAVY, font=MONO))
            rows.arrange(DOWN, buff=0.08)
            box = SurroundingRectangle(rows, color=NAVY, stroke_width=1.5, buff=0.08)
            vecs.add(VGroup(box, rows).move_to([x, 2.52, 0]))
        more = VGroup(T(f"{V['width']} numbers each —", 22, NAVY), T("the first four shown", 22, NAVY)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        more.move_to([4.7, 2.7, 0])
        pos = T("+ one for “where am I”", 22, MUTED).move_to([4.7, 2.05, 0])
        caption("2 · Each token becomes a list of numbers: its place on the map of meaning.")
        self.play(*[ReplacementTransform(i, v) for i, v in zip(idt, vecs)], run_time=2.2)
        self.play(FadeIn(more), run_time=1.2)
        self.play(FadeIn(pos), run_time=1.0)
        self.wait(2.5)

        # 3 · block + attention
        frame = Rectangle(width=8.0, height=2.35, stroke_color=INK, stroke_width=2.5,
                          fill_color=PAPER, fill_opacity=1).move_to([-2.0, 0.35, 0])
        blabel = T("ONE BLOCK", 22, GOLDDK, BOLD).next_to(frame, RIGHT, buff=0.55).align_to(frame, UP)
        att = Rectangle(width=7.5, height=0.9, stroke_color=RED, stroke_width=2.5, fill_color=WHITE,
                        fill_opacity=1).move_to([-2.0, 0.95, 0])
        attl = T("attention — tokens exchange information", 24, RED, BOLD).move_to([-2.0, 0.68, 0])
        self.play(FadeIn(frame), FadeIn(blabel), run_time=1.6)
        self.play(Create(att), run_time=1.4)
        caption("3 · Attention: every token looks at the others and borrows meaning from them.")
        dots = VGroup(*[Dot([x, 1.28, 0], radius=0.07, color=NAVY) for x in xs])
        drops = VGroup(*[Line([x, vecs[0].get_bottom()[1], 0], [x, 1.36, 0], color=MUTED, stroke_width=2) for x in xs])
        self.play(Create(drops), FadeIn(dots), run_time=1.2)
        arcs = VGroup()
        for a in range(4):
            for b in range(a + 1, 4):
                arcs.add(ArcBetweenPoints([xs[a], 1.28, 0], [xs[b], 1.28, 0], angle=PI / 6,
                                          color=RED, stroke_width=2.5, stroke_opacity=0.75))
        self.play(LaggedStart(*[Create(c) for c in arcs], lag_ratio=0.25), run_time=2.5)
        self.play(FadeIn(attl), run_time=1.0)
        self.wait(2.5)

        # 4 · neurons, one token at a time
        neu = Rectangle(width=7.5, height=1.0, stroke_color=NAVY, stroke_width=2.5, fill_color=WHITE,
                        fill_opacity=1).move_to([-2.0, -0.26, 0])
        neul = T("neurons — each token thinks on its own", 22, NAVY, BOLD).move_to([-2.0, -0.56, 0])
        self.play(Create(neu), run_time=1.4)
        caption("4 · Neurons — the network from last week — each token thinks on its own.")
        nets = VGroup()
        for x in xs:
            a, b, c = Dot([x - 0.3, 0.12, 0], radius=0.055, color=NAVY), Dot([x - 0.3, -0.12, 0], radius=0.055, color=NAVY), \
                Dot([x + 0.3, 0.0, 0], radius=0.065, color=NAVY)
            nets.add(VGroup(Line(a.get_center(), c.get_center(), color=NAVY, stroke_width=2),
                            Line(b.get_center(), c.get_center(), color=NAVY, stroke_width=2), a, b, c))
        self.play(FadeIn(nets), run_time=1.2)
        for n in nets:
            pulse = Dot(n[2].get_center() + LEFT * 0.6 + UP * 0.02, radius=0.09, color=GOLDDK)
            self.play(MoveAlongPath(pulse, Line(n[2].get_center() + LEFT * 0.6, n[4].get_center())), run_time=0.9)
            self.play(n[4].animate.set_color(GOLDDK), FadeOut(pulse), run_time=0.5)
        self.play(FadeIn(neul), run_time=1.0)
        self.wait(2.5)

        # 5 · stacked
        block = VGroup(frame, att, neu, dots, drops, arcs, nets, attl, neul)
        ghosts = VGroup(*[frame.copy().set_fill(PAPER, 1).set_stroke(MUTED, 1.5) for _ in range(3)])
        caption("This block, stacked again and again: that is a Transformer.")
        for k, gh in enumerate(ghosts):
            gh.move_to(frame).shift((k + 1) * np.array([0.14, -0.14, 0]))
            gh.set_z_index(-1 - k)
        block.set_z_index(1)
        self.play(LaggedStart(*[FadeIn(gh, shift=DR * 0.1) for gh in ghosts], lag_ratio=0.4), run_time=2.2)
        count = T(f"× {g['layers']} in GPT-2 small  ·  × 36 in gpt-oss-120b", 26, INK, BOLD).move_to([-2.0, -1.4, 0])
        self.play(FadeIn(count), run_time=1.4)
        self.wait(3.0)

        # 6 · last vector → knobs
        caption("5 · The last token's vector becomes a knob for every possible next piece.")
        out = Rectangle(width=7.5, height=0.72, stroke_color=GOLDDK, stroke_width=2.5).move_to([-2.0, -2.35, 0])
        outl = T(f"last vector → {g['vocab']:,} scores → the knobs", 24, INK, BOLD).move_to(out)
        hl = SurroundingRectangle(wd[3], color=GOLDDK, buff=0.1, stroke_width=3)
        self.play(Create(hl), run_time=1.2)
        path = Arrow([xs[3], -1.75, 0], [xs[3], -1.98, 0], color=GOLDDK, buff=0, stroke_width=5,
                     max_tip_length_to_length_ratio=0.6)
        self.play(GrowArrow(path), Create(out), run_time=1.6)
        self.play(FadeIn(outl), run_time=1.0)
        self.wait(1.5)
        K = S["knobs"][:5]
        top = 1.35
        rows = VGroup()
        for i, k in enumerate(K):
            y = top - i * 0.62
            lab = T(k["token"].strip(), 26, INK, BOLD if i == 0 else NORMAL).move_to([3.6, y, 0], aligned_edge=RIGHT)
            lab.align_to([4.3, 0, 0], RIGHT)
            bar = Rectangle(width=max(k["p"] * 4.5, 0.05), height=0.36, stroke_width=0,
                            fill_color=RED if i == 0 else GOLD, fill_opacity=1)
            bar.move_to([4.45, y, 0], aligned_edge=LEFT)
            pct = T(f"{k['p']:.0%}", 24, INK).next_to(bar, RIGHT, buff=0.12)
            rows.add(VGroup(lab, bar, pct))
        head = T("next piece?", 24, MUTED).move_to([5.3, 1.95, 0])
        link = Arrow(out.get_right(), [3.2, 0.2, 0], color=GOLDDK, buff=0.1, stroke_width=4)
        self.play(FadeOut(more), FadeOut(pos), FadeOut(blabel), run_time=0.6)
        self.play(GrowArrow(link), FadeIn(head), run_time=1.4)
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in rows], lag_ratio=0.35), run_time=2.5)
        self.wait(4.0)
