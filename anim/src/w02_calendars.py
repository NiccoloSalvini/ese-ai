"""Week 2 — two calendars that do not line up, and what a join does to them.

    manim -qm src/w02_calendars.py Calendars -o w02_calendars.mp4
"""
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon"]


class Calendars(Scene):
    def construct(self):
        title = Tex(r"One week of prices, two markets", font_size=34, color=NAVY).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.9)

        def row(label, has, colour, y):
            lab = Tex(label, font_size=26, color=colour).move_to([-6.0, y, 0])
            cells = VGroup()
            for i, d in enumerate(DAYS):
                x = -4.3 + i * 1.28
                if has[i]:
                    c = Rectangle(width=1.1, height=0.72, fill_color=colour, fill_opacity=0.28,
                                  stroke_color=colour, stroke_width=2).move_to([x, y, 0])
                    txt = Tex(r"\checkmark", font_size=26, color=colour).move_to([x, y, 0])
                else:
                    c = Rectangle(width=1.1, height=0.72, fill_color=BLACK, fill_opacity=1,
                                  stroke_color=GREY, stroke_width=1.5).move_to([x, y, 0])
                    txt = Tex("--", font_size=24, color=GREY).move_to([x, y, 0])
                cells.add(VGroup(c, txt))
            return VGroup(lab, cells)

        head = VGroup(*[Tex(d, font_size=22, color=WHITE).move_to([-4.3 + i * 1.28, 2.1, 0])
                        for i, d in enumerate(DAYS)])
        crypto = row("BTC", [1] * 8, GOLD, 1.25)
        equity = row("SPY", [1, 1, 1, 1, 1, 0, 0, 1], NAVY, 0.25)
        self.play(FadeIn(head), run_time=0.5)
        self.play(FadeIn(crypto), run_time=0.8)
        self.play(FadeIn(equity), run_time=0.8)
        self.wait(0.6)

        # inner join: keep only the days both have
        note = Tex(r"\textbf{Inner join} --- keep only days present in both", font_size=28, color=GREEN).move_to([0, -0.9, 0])
        self.play(Write(note), run_time=0.9)
        drop = VGroup(crypto[1][5], crypto[1][6])
        self.play(drop.animate.set_opacity(0.18), run_time=0.9)
        lost = Tex(r"the weekend is gone --- and with it, real moves", font_size=26, color=RED).move_to([0, -1.7, 0])
        self.play(FadeIn(lost), run_time=0.8)
        self.wait(1.1)

        # forward fill: invent the missing days instead
        self.play(FadeOut(note), FadeOut(lost), drop.animate.set_opacity(1.0), run_time=0.7)
        note2 = Tex(r"\textbf{Forward fill} --- carry Friday's price through the weekend", font_size=28, color=GOLD).move_to([0, -0.9, 0])
        self.play(Write(note2), run_time=0.9)
        ghosts = VGroup(*[
            Rectangle(width=1.1, height=0.72, fill_color=NAVY, fill_opacity=0.12,
                      stroke_color=NAVY, stroke_width=2, stroke_opacity=0.5).move_to([-4.3 + i * 1.28, 0.25, 0])
            for i in (5, 6)])
        self.play(FadeIn(ghosts), run_time=0.8)

        box = SurroundingRectangle(VGroup(crypto[1][7], equity[1][7]), color=RED, buff=0.12)
        warn = Tex(r"Monday's BTC return is now measured against a price that never traded",
                   font_size=26, color=RED).move_to([0, -1.75, 0])
        self.play(Create(box), FadeIn(warn), run_time=1.2)
        self.wait(1.0)
        self.play(Write(caption(r"Decide which days exist \emph{before} you compute anything across assets.")), run_time=1.3)
        self.wait(0.8)
