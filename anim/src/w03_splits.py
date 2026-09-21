"""Week 3 — a shuffled split on a time series puts the future in the training set.

    manim -qm src/w03_splits.py Splits -o w03_splits.mp4
"""
import random
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption

random.seed(7)
N = 28


class Splits(Scene):
    def construct(self):
        title = Tex(r"The same data, split two ways", font_size=34, color=NAVY).to_edge(UP, buff=0.35)
        axis = Line([-5.8, 0.9, 0], [5.8, 0.9, 0], color=GREY, stroke_width=3)
        arrow = Triangle(color=GREY, fill_opacity=1).scale(0.09).rotate(-90 * DEGREES).move_to([5.9, 0.9, 0])
        tlab = Tex("time", font_size=24, color=GREY).next_to(arrow, DOWN, buff=0.22)
        self.play(Write(title), Create(axis), FadeIn(arrow), FadeIn(tlab), run_time=1.1)

        xs = [-5.6 + i * (11.2 / (N - 1)) for i in range(N)]
        dots = VGroup(*[Dot([x, 0.9, 0], radius=0.11, color=GREY) for x in xs])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), run_time=1.0)

        # shuffled split
        shuffled = Tex(r"\textbf{Shuffled split} --- test rows picked at random", font_size=28, color=RED).move_to([0, 2.0, 0])
        self.play(Write(shuffled), run_time=0.8)
        test_idx = sorted(random.sample(range(N), 8))
        self.play(*[dots[i].animate.set_color(RED) for i in test_idx],
                  *[dots[i].animate.set_color(NAVY) for i in range(N) if i not in test_idx], run_time=1.0)
        legend = VGroup(
            VGroup(Dot(color=NAVY, radius=0.1), Tex("train", font_size=24, color=NAVY)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=RED, radius=0.1), Tex("test", font_size=24, color=RED)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.7).move_to([0, -0.15, 0])
        self.play(FadeIn(legend), run_time=0.5)

        j = test_idx[2]
        later = [i for i in range(N) if i > j and i not in test_idx][:6]
        braces = VGroup(*[Arrow(dots[i].get_center() + DOWN * 0.55, dots[j].get_center() + DOWN * 0.18,
                                color=GOLD, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.12)
                          for i in later])
        leak = Tex(r"the model trains on days \emph{after} the day it is tested on", font_size=27, color=GOLD).move_to([0, -1.5, 0])
        self.play(LaggedStart(*[GrowArrow(b) for b in braces], lag_ratio=0.12), Write(leak), run_time=1.6)
        score = Tex(r"accuracy 0.71 --- and meaningless", font_size=30, color=RED).move_to([0, -2.35, 0])
        self.play(FadeIn(score), run_time=0.7)
        self.wait(1.0)

        # time-ordered split
        self.play(FadeOut(braces), FadeOut(leak), FadeOut(score), FadeOut(shuffled), run_time=0.6)
        ordered = Tex(r"\textbf{Time-ordered split} --- test is always the future", font_size=28, color=GREEN).move_to([0, 2.0, 0])
        cut = int(N * 0.72)
        self.play(Write(ordered),
                  *[dots[i].animate.set_color(NAVY) for i in range(cut)],
                  *[dots[i].animate.set_color(GREEN) for i in range(cut, N)], run_time=1.1)
        wall = DashedLine([xs[cut] - 0.2, 1.7, 0], [xs[cut] - 0.2, 0.1, 0], color=WHITE, stroke_width=3)
        wlab = Tex("the wall", font_size=24, color=WHITE).next_to(wall, UP, buff=0.1)
        honest = Tex(r"accuracy 0.53 --- and true", font_size=30, color=GREEN).move_to([0, -1.5, 0])
        self.play(Create(wall), FadeIn(wlab), FadeIn(honest), run_time=1.2)
        self.wait(0.8)
        self.play(Write(caption(r"Nothing on the right of the wall may be used to fit what is on the left.")), run_time=1.3)
        self.wait(0.8)
