"""Week 2 clip — the same 0.5B model before and after post-training. Real outputs from
lectures/img/w02_base_vs_chat.json (Qwen2.5-0.5B vs Qwen2.5-0.5B-Instruct, greedy)."""
import json, textwrap
from pathlib import Path
from manim import *

D = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_base_vs_chat.json").read_text())
INK, RED, GOLD, NAVY, MUTED = "#363636", "#AF1F25", "#CDBA80", "#2471a3", "#7a7f85"
FONT = "Helvetica Neue"
COLX = (-3.55, 3.55)
WRAP = 36


def clip(s, n):
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + " …"


def para(s, color=INK, size=24):
    lines = textwrap.wrap(s, WRAP)
    return VGroup(*[Text(l, font=FONT, font_size=size, color=color) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)


class BaseVsChat(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        rows = {r["question"]: r for r in D["rows"]}
        france = rows["What is the capital of France?"]
        btc = rows["Should I buy Bitcoin today?"]

        # headers: the same model, twice
        h = []
        for x, top, sub, col in [(COLX[0], "after pre-training only", "the base model", MUTED),
                                 (COLX[1], "after post-training", "the assistant", NAVY)]:
            t1 = Text(top, font=FONT, font_size=26, weight=BOLD, color=col)
            t2 = Text(sub + " · Qwen2.5, 0.5B", font=FONT, font_size=22, color=MUTED)
            g = VGroup(t1, t2).arrange(DOWN, buff=0.1).move_to([x, 2.25, 0])
            h.append(g)
        rule = Line([0, 2.7, 0], [0, -2.7, 0], color=GOLD, stroke_width=2)
        same = Text("same model, same size, same pre-training", font=FONT, font_size=22, color=MUTED).to_edge(UP, buff=0.95)

        def ask(q):
            return Text(f"“{q}”", font=FONT, font_size=32, weight=BOLD, color=INK).to_edge(UP, buff=0.3)

        def caption(s):
            return Text(s, font=FONT, font_size=24, color=INK).to_edge(DOWN, buff=0.35)

        def answer(s, x, color):
            p = para(s, color)
            p.next_to([x - 3.1, 1.55, 0], DOWN, buff=0, aligned_edge=LEFT).align_to([x - 3.1, 0, 0], LEFT)
            return p

        def type_out(p, rt):
            self.play(AnimationGroup(*[AddTextLetterByLetter(l, run_time=rt * len(l.text) / max(1, sum(len(k.text) for k in p)))
                                       for l in p], lag_ratio=1.0), run_time=rt)

        # ---- part 1: a fact
        q = ask(france["question"])
        self.play(FadeIn(q), run_time=1.5)
        self.play(FadeIn(same), FadeIn(h[0]), FadeIn(h[1]), Create(rule), run_time=2.0)
        self.wait(2.0)
        a0 = answer(clip(france["base"], 120), COLX[0], INK)
        type_out(a0, 2.0)
        self.wait(1.0)
        a1 = answer(clip(france["chat"], 120), COLX[1], NAVY)
        type_out(a1, 2.0)
        c = caption("A fact: both know it. The knowledge comes from pre-training.")
        self.play(FadeIn(c), run_time=1.5)
        self.wait(3.0)

        # ---- part 2: a question with no single answer
        q2 = ask(btc["question"])
        self.play(FadeOut(a0), FadeOut(a1), FadeOut(c), ReplacementTransform(q, q2), run_time=1.8)
        self.wait(1.5)
        b0 = answer(clip(btc["base"], 150), COLX[0], INK)
        c1 = caption("Left: it only learned to continue documents — so it writes one.")
        self.play(FadeIn(c1), run_time=1.5)
        type_out(b0, 5.0)
        self.wait(3.0)
        b1 = answer(clip(btc["chat"], 150), COLX[1], NAVY)
        c2 = caption("Right: the same model after post-training — it learned to answer.")
        self.play(FadeOut(c1), FadeIn(c2), run_time=1.5)
        type_out(b1, 5.0)
        self.wait(3.0)

        end = Text("Post-training does not add knowledge. It adds a role.", font=FONT, font_size=30,
                   weight=BOLD, color=RED).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(c2), FadeIn(end), run_time=2.0)
        self.wait(4.0)
