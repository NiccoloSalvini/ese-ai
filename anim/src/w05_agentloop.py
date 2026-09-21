"""Week 5 — the agent loop, and the budget that stops it.

    manim -qm src/w05_agentloop.py AgentLoop -o w05_agentloop.mp4
"""
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN, caption


class AgentLoop(Scene):
    def construct(self):
        title = Tex(r"An agent is a loop. There is nothing else in the word.",
                    font_size=32, color=NAVY).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.0)

        model = VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.12,
                                        stroke_color=NAVY, stroke_width=3, fill_color=NAVY, fill_opacity=0.12),
                       Tex("the model", font_size=28, color=NAVY)).move_to([-3.2, 1.55, 0])
        code = VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.12,
                                       stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12),
                      Tex("your code", font_size=28, color=GREEN)).move_to([3.2, 1.55, 0])
        ctx = VGroup(RoundedRectangle(width=8.6, height=1.15, corner_radius=0.1,
                                      stroke_color=GREY, stroke_width=2.5),
                     Tex("the context window --- everything so far, re-sent every turn",
                         font_size=24, color=GREY)).move_to([0, -0.5, 0])
        self.play(FadeIn(model), FadeIn(code), FadeIn(ctx), run_time=1.1)

        out = CurvedArrow(model[0].get_right() + RIGHT * 0.05, code[0].get_left() + LEFT * 0.05,
                          angle=-0.55, color=GOLD, stroke_width=4)
        out_l = Tex(r'\texttt{get\_price("BTC")}', font_size=23, color=GOLD).next_to(out, UP, buff=0.08)
        back = CurvedArrow(code[0].get_bottom() + DOWN * 0.05, ctx[0].get_right() + RIGHT * 0.02,
                           angle=0.5, color=GREEN, stroke_width=4)
        back_l = Tex(r"\texttt{62{,}410.55}", font_size=23, color=GREEN).next_to(back, RIGHT, buff=0.08)
        feed = CurvedArrow(ctx[0].get_left() + LEFT * 0.02, model[0].get_bottom() + DOWN * 0.05,
                           angle=0.5, color=GREY, stroke_width=4)

        steps = VGroup(*[Tex(s, font_size=23, color=WHITE) for s in (
            r"1. the model asks for a tool, as structured text",
            r"2. \textbf{your} code runs it --- the model touches nothing",
            r"3. the result goes back into the context",
            r"4. round again, until it has an answer")]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -2.1, 0])

        self.play(Create(out), Write(out_l), FadeIn(steps[0]), run_time=1.1)
        self.play(FadeIn(steps[1]), run_time=0.6)
        self.play(Create(back), Write(back_l), FadeIn(steps[2]), run_time=1.1)
        self.play(Create(feed), FadeIn(steps[3]), run_time=1.0)

        counter = VGroup(
            Tex("step 1 of 6", font_size=26, color=WHITE),
            Tex(r"\texteuro 0.004", font_size=26, color=GOLD),
        ).arrange(DOWN, buff=0.12).to_corner(UR, buff=0.4)
        self.add(counter)
        for n, cost in ((2, 0.009), (3, 0.017), (4, 0.028)):
            new = VGroup(Tex(f"step {n} of 6", font_size=26, color=WHITE),
                         Tex(rf"\texteuro {cost:.3f}", font_size=26, color=GOLD)
                         ).arrange(DOWN, buff=0.12).to_corner(UR, buff=0.4)
            self.play(Transform(counter, new), Flash(out, color=GOLD, line_length=0.15), run_time=0.55)

        stop = Tex(r"every loop needs a stop: a step budget, a cost ceiling, a repeat-call guard",
                   font_size=27, color=RED).move_to([0, -2.1, 0])
        self.play(FadeOut(steps), run_time=0.4)
        self.play(Write(stop), run_time=1.3)
        self.wait(1.2)
