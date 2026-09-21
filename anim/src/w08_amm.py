"""Week 8 — one equation runs an automated market maker, and it explains the slippage.

    manim -qm src/w08_amm.py ConstantProduct -o w08_amm.mp4
"""
import numpy as np
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption

K = 100.0 * 6_000_000.0          # 100 ETH against 6M USDC
X0 = 100.0


def curve(x): return K / max(x, 1e-6)


class ConstantProduct(Scene):
    def construct(self):
        ax = Axes(x_range=[40, 200, 40], y_range=[2_000_000, 16_000_000, 4_000_000],
                  x_length=8.2, y_length=4.2,
                  axis_config={"include_numbers": True, "font_size": 19},
                  y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "group_with_commas": True}}
                  ).shift(UP * 0.25 + LEFT * 1.1)
        xl = Tex("ETH in the pool", font_size=24).next_to(ax, DOWN, buff=0.15)
        yl = Tex("USDC in the pool", font_size=24).rotate(90 * DEGREES).next_to(ax, LEFT, buff=0.12)
        eq = MathTex(r"x \cdot y = k", font_size=44, color=NAVY).to_edge(UP, buff=0.3)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Write(eq), run_time=1.5)

        c = ax.plot(curve, x_range=[45, 195], color=NAVY, stroke_width=5)
        self.play(Create(c), run_time=1.3)

        x = ValueTracker(X0)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), curve(x.get_value())), color=GOLD, radius=0.1))
        readout = always_redraw(lambda: VGroup(
            Tex(rf"pool price  \texttt{{{curve(x.get_value())/x.get_value():,.0f}}} USDC/ETH", font_size=25, color=GOLD),
            Tex(rf"ETH bought  \texttt{{{X0 - x.get_value():,.1f}}}", font_size=25, color=WHITE),
            Tex(rf"paid on average  \texttt{{{(curve(x.get_value()) - curve(X0)) / max(X0 - x.get_value(), 1e-9):,.0f}}}",
                font_size=25, color=RED) if x.get_value() < X0 - 0.05 else Tex(" ", font_size=25),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.16).to_corner(UR, buff=0.35))
        self.add(dot, readout)
        self.wait(0.6)

        start = Tex(r"start: 60{,}000 USDC per ETH", font_size=24, color=GREY).next_to(ax.c2p(X0, curve(X0)), RIGHT, buff=0.25)
        self.play(FadeIn(start), run_time=0.6)
        self.play(x.animate.set_value(62), run_time=4.2, rate_func=smooth)
        self.wait(0.5)

        gap = Tex(r"\textbf{That gap is the slippage} --- not a fee. You moved the price by trading.",
                  font_size=27, color=RED).to_edge(DOWN, buff=0.3)
        self.play(Write(gap), run_time=1.4)
        self.wait(1.4)
