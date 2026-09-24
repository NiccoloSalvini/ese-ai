"""Week 2 clips — inside an LLM. Numbers from lectures/img/w02_llm_story.json."""
import json
from pathlib import Path
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN

S = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_llm_story.json").read_text())
MONO = "Menlo"


class AttentionByHand(Scene):
    """'it' asks a question; every token answers with a score; the scores become weights; the values are mixed."""

    def construct(self):
        A = S["toy_attention"]
        title = Text("Attention, by hand", font_size=32, weight=BOLD).to_edge(UP, buff=0.3)
        self.add(title)
        xs = [-5.4 + i * 2.15 for i in range(len(A["tokens"]))]
        words = VGroup(*[Text(tk, font_size=28, weight=BOLD if tk in ("it", "bank") else NORMAL,
                              color=GOLD if tk == "it" else WHITE).move_to([x, 2.2, 0]) for tk, x in zip(A["tokens"], xs)])
        self.play(FadeIn(words), run_time=0.7)
        q = Text(f"“it” asks — query ({A['query'][0]:g}, {A['query'][1]:g}): who can fear?", font_size=24, color=GOLD).move_to([0, 1.45, 0])
        self.play(FadeIn(q), run_time=0.6)
        keys = VGroup(*[Text(f"key ({k[0]:g}, {k[1]:g})", font=MONO, font_size=16, color=GREY).move_to([x, 0.8, 0]) for k, x in zip(A["keys"], xs)])
        self.play(FadeIn(keys), run_time=0.6)
        self.wait(0.6)
        scores = VGroup(*[Text(f"score {s:g}", font=MONO, font_size=18, color=RED if tk == "bank" else WHITE).move_to([x, 0.3, 0])
                          for s, tk, x in zip(A["scores"], A["tokens"], xs)])
        how = Text("score = query · key = 1.5 × first + 0 × second   (multiply and add: a neuron)", font_size=20, color=GREY).move_to([0, -0.3, 0])
        self.play(FadeIn(scores), FadeIn(how), run_time=0.9)
        self.wait(1.4)
        base = -2.3
        bars = VGroup()
        for w, tk, x in zip(A["weights"], A["tokens"], xs):
            h = max(w * 2.0, 0.03)
            r = Rectangle(width=1.1, height=h, fill_color=RED if tk == "bank" else NAVY, fill_opacity=0.85, stroke_width=0).move_to([x, base + h / 2, 0])
            lab = Text(f"{w:.0%}", font_size=20).next_to(r, UP, buff=0.06)
            bars.add(VGroup(r, lab))
        how2 = Text("weights = e^score ÷ total   (the knobs from last week)", font_size=20, color=GREY).move_to([0, -0.3, 0])
        self.play(FadeOut(how), FadeIn(how2), FadeIn(bars), run_time=1.0)
        self.wait(1.6)
        m = A["mixed"]
        res = Text(f"new “it” = 70% × bank’s value + 16% × rates’ value + … = ({m[0]:.2f}, {m[1]:.2f})  →  mostly “bank”",
                   font_size=21, color=GOLD, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(res), run_time=0.8)
        self.wait(3.0)
