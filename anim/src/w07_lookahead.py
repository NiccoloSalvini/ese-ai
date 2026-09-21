"""Week 7 — the same strategy, one line apart: a backtest that lies and one that does not.

    manim -qm src/w07_lookahead.py LookAhead -o w07_lookahead.mp4
"""
import numpy as np
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption

rng = np.random.default_rng(48)
N = 120
RET = rng.normal(0.0004, 0.012, N)                  # six months of daily returns
SIG = np.sign(np.concatenate([[0], RET[:-1]]))      # yesterday's sign: a momentum signal

# Honest: the position is held from the day AFTER the signal.
HONEST = np.cumprod(1 + np.concatenate([[0], SIG[:-1] * RET[1:]]))
# Leaked: the position earns the return of the very day that produced the signal.
LEAKED = np.cumprod(1 + np.sign(RET) * RET)


def honest(i): return float(HONEST[int(np.clip(i, 0, N - 1))])
def leaked(i): return float(LEAKED[int(np.clip(i, 0, N - 1))])


class LookAhead(Scene):
    def construct(self):
        ax = Axes(x_range=[0, N, 30], y_range=[0.8, 3.4, 0.5], x_length=9.2, y_length=4.0,
                  axis_config={"include_numbers": True, "font_size": 20}).shift(UP * 0.2)
        xl = Tex("trading days", font_size=24).next_to(ax, DOWN, buff=0.15)
        yl = Tex(r"\texteuro 1 becomes", font_size=24).rotate(90 * DEGREES).next_to(ax, LEFT, buff=0.15)
        code = VGroup(
            Tex(r"\texttt{position = signal.shift(1)}", font_size=25, color=GREEN),
            Tex(r"\texttt{position = signal}", font_size=25, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.3)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(Write(code[0]), run_time=0.7)

        h = ax.plot(honest, x_range=[0, N - 1], color=GREEN, stroke_width=5, use_smoothing=False)
        self.play(Create(h), run_time=2.0)
        hs = Tex(rf"Sharpe {np.mean(SIG[:-1]*RET[1:])/np.std(SIG[:-1]*RET[1:])*np.sqrt(252):.2f}",
                 font_size=28, color=GREEN).next_to(ax.c2p(N - 1, honest(N - 1)), RIGHT, buff=0.15)
        self.play(FadeIn(hs), run_time=0.6)
        self.wait(0.5)

        self.play(Write(code[1]), run_time=0.7)
        lk = ax.plot(leaked, x_range=[0, N - 1], color=RED, stroke_width=5, use_smoothing=False)
        self.play(Create(lk), run_time=2.0)
        ls = Tex(rf"Sharpe {np.mean(np.sign(RET)*RET)/np.std(np.sign(RET)*RET)*np.sqrt(252):.2f}",
                 font_size=28, color=RED).next_to(ax.c2p(N - 1, leaked(N - 1)), RIGHT, buff=0.15)
        self.play(FadeIn(ls), run_time=0.6)

        note = Tex(r"one missing \texttt{shift(1)} --- the position earns the very return that produced it",
                   font_size=27, color=RED).to_edge(DOWN, buff=0.62)
        self.play(Write(note), run_time=1.2)
        self.play(Write(caption(r"A backtest this good is not a discovery. It is a bug you have not found yet.", 26)), run_time=1.3)
        self.wait(1.0)
