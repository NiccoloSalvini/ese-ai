"""Week 4 — why retrieval finds a paraphrase that word-matching cannot.

    manim -qm src/w04_retrieval.py MeaningIsAPlace -o w04_retrieval.mp4
"""
import numpy as np
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption

# Hand-placed so the clusters read: revenue talk, risk talk, and one query.
CHUNKS = [
    ("revenue fell in Q3",      -2.6,  1.15, NAVY),
    ("takings were well down",  -2.05, 1.55, NAVY),
    ("sales declined sharply",  -3.1,  1.6,  NAVY),
    ("supply chain disruption",  1.9, -0.5,  GREY),
    ("cyber risk exposure",      2.7,  0.55, GREY),
    ("board approved dividend",  0.6,  2.0,  GREY),
]
QUERY = ("how bad was Q3?", -2.55, 0.55)


class MeaningIsAPlace(Scene):
    def construct(self):
        title = Tex(r"Every passage becomes a point. Meaning becomes distance.",
                    font_size=32, color=NAVY).to_edge(UP, buff=0.3)
        plane = NumberPlane(x_range=[-5, 5, 1], y_range=[-2.2, 2.8, 1],
                            x_length=11, y_length=5.2,
                            background_line_style={"stroke_color": GREY, "stroke_width": 1,
                                                   "stroke_opacity": 0.22}).shift(DOWN * 0.35)
        self.play(Write(title), Create(plane), run_time=1.4)

        dots, labels = VGroup(), VGroup()
        for text, x, y, col in CHUNKS:
            d = Dot(plane.c2p(x, y), radius=0.1, color=col)
            l = Tex(text, font_size=21, color=col).next_to(d, UP, buff=0.12)
            dots.add(d); labels.add(l)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(d), FadeIn(l)) for d, l in zip(dots, labels)],
                              lag_ratio=0.18), run_time=2.2)
        self.wait(0.4)

        qt, qx, qy = QUERY
        q = Dot(plane.c2p(qx, qy), radius=0.13, color=GOLD)
        ql = Tex(qt, font_size=24, color=GOLD).next_to(q, DOWN, buff=0.15)
        self.play(FadeIn(q, scale=2), Write(ql), run_time=1.0)

        near = sorted(range(len(CHUNKS)), key=lambda i: (CHUNKS[i][1] - qx) ** 2 + (CHUNKS[i][2] - qy) ** 2)[:3]
        lines = VGroup(*[Line(plane.c2p(qx, qy), plane.c2p(CHUNKS[i][1], CHUNKS[i][2]),
                              color=GOLD, stroke_width=3) for i in near])
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2), run_time=1.3)
        halo = VGroup(*[Circle(radius=0.24, color=GOLD, stroke_width=3).move_to(dots[i]) for i in near])
        self.play(FadeIn(halo), run_time=0.6)

        note = Tex(r"\textbf{not one word in common} --- and still the three nearest",
                   font_size=28, color=GOLD).to_edge(DOWN, buff=1.05)
        self.play(Write(note), run_time=1.1)
        self.wait(0.9)
        self.play(Write(caption(r"Retrieval is this: embed the question, take the nearest passages, and answer only from them.")), run_time=1.4)
        self.wait(0.8)
