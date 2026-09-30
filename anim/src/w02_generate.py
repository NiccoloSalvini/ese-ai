"""Week 2 clip — how text is generated: read, knobs, pick, append, run again.

White stage, slow, for a non-technical reader. Real GPT-2 small numbers from
lectures/img/w02_generate.json (written by lectures/img/w02_generate.py).
"""
import json
from pathlib import Path
from manim import *

G = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_generate.json").read_text())

INK, ERED, EGOLD, ENAVY, MUTED, PANEL = "#363636", "#AF1F25", "#CDBA80", "#2471a3", "#7a7f85", "#f3f1ea"
SANS = "Helvetica Neue"
LEFT_X, SENT_Y = -6.6, 2.85
BAR_X, BAR_MAX, ROWS = 1.75, 3.9, [1.35, 0.65, -0.05, -0.75, -1.45]


def T(s, size=28, color=INK, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def glyphs(s):
    return len(s.replace(" ", ""))


class Generate(Scene):
    def sentence(self, text, n_prompt):
        """The running text; prompt pieces in ink, generated pieces in red. Left edge fixed."""
        m = T(text, 32)
        m.move_to([0, SENT_Y, 0]).align_to([LEFT_X, 0, 0], LEFT)
        m[:n_prompt].set_color(INK)
        m[n_prompt:].set_color(ERED)
        return m

    def bars(self, knobs):
        grp = VGroup()
        for i, (k, y) in enumerate(zip(knobs, ROWS)):
            lab = T("“" + k["token"].strip() + "”", 28).move_to([0, y, 0]).align_to([BAR_X - 0.2, 0, 0], RIGHT)
            w = max(k["p"] * BAR_MAX, 0.04)
            bar = Rectangle(width=w, height=0.46, fill_color=ENAVY, fill_opacity=0.85, stroke_width=0)
            bar.move_to([BAR_X + w / 2, y, 0])
            pct = T(f"{k['p']:.0%}" if k["p"] >= 0.01 else "<1%", 26, MUTED).next_to(bar, RIGHT, buff=0.15)
            grp.add(VGroup(lab, bar, pct))
        return grp

    def say(self, old, text, wait=2.5):
        new = T(text, 26, INK).move_to([0, -3.15, 0])
        if new.width > 13.4:
            new.scale_to_fit_width(13.4)
        self.play(FadeOut(old), FadeIn(new), run_time=1.0)
        if wait > 0:
            self.wait(wait)
        return new

    def construct(self):
        self.camera.background_color = WHITE
        prompt = G["prompt"]
        n_prompt = glyphs(prompt)
        steps = G["steps"]

        # 1 · the text and the model
        sent = self.sentence(prompt, n_prompt)
        model = VGroup(
            RoundedRectangle(corner_radius=0.08, width=3.3, height=1.7, fill_color=PANEL, fill_opacity=1, stroke_color=MUTED, stroke_width=3),
        ).move_to([-4.1, 0, 0])
        model.add(T("the model", 30, INK).move_to(model[0]))
        down = Arrow([-4.1, SENT_Y - 0.45, 0], [-4.1, 0.95, 0], color=MUTED, stroke_width=5, buff=0)
        right = Arrow([-2.35, 0, 0], [-0.5, 0, 0], color=MUTED, stroke_width=5, buff=0)
        cap = T("The model reads the whole text…", 26).move_to([0, -3.15, 0])
        self.play(FadeIn(sent), run_time=1.5)
        self.play(GrowArrow(down), FadeIn(model), FadeIn(cap), run_time=2.0)
        self.wait(2.5)

        # 2 · the knobs
        bars = self.bars(steps[0]["knobs"])
        cap = self.say(cap, "…and turns every possible next piece into a knob: how likely it comes next.", wait=0)
        self.play(GrowArrow(right), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bars], lag_ratio=0.25), run_time=2.5)
        self.wait(3.0)

        # 3 · pick and append — slow the first time, quicker after
        for i, step in enumerate(steps):
            if i > 0:
                cap_text = "Then run the whole model again, on the longer text. One piece at a time."
                if i == 1:
                    cap = self.say(cap, cap_text, wait=0.5)
                self.play(Indicate(down, color=ERED, scale_factor=1.0), Indicate(model[0], color=ERED, scale_factor=1.05), run_time=1.5)
                new_bars = self.bars(step["knobs"])
                self.play(FadeOut(bars), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in new_bars], lag_ratio=0.2), run_time=1.8)
                bars = new_bars
                self.wait(2.0 if i < 3 else 2.5)
            else:
                cap = self.say(cap, "Pick one — here always the top one — and add it to the text.", wait=0.5)

            top = bars[0]
            self.play(top[1].animate.set_fill(ERED), top[0].animate.set_color(ERED), run_time=1.0)
            piece = step["knobs"][0]["token"]
            longer = self.sentence(step["text"] + piece, n_prompt)
            start = glyphs(step["text"])
            target = longer[start:]
            flying = T(piece.strip(), 28, ERED).move_to(top[0])
            self.play(FadeOut(top[0]), FadeIn(flying), run_time=0.4)
            self.play(Transform(flying, target.copy()), run_time=2.0 if i == 0 else 1.5)
            self.remove(flying, sent)
            self.add(longer)
            sent = longer
            self.wait(2.5 if i == 0 else 1.5)

        # 4 · and so on, to the end of the greedy sentence
        cap = self.say(cap, "And so on — twelve pieces later:", wait=0.5)
        full_text = prompt + G["greedy"]
        full = self.sentence(full_text, n_prompt)
        done = glyphs(steps[-1]["text"] + steps[-1]["knobs"][0]["token"])
        self.play(FadeOut(bars), FadeOut(right), FadeIn(full[done:], lag_ratio=0.15), run_time=2.5)
        self.remove(sent)
        self.add(full)
        self.wait(2.0)

        # 5 · the made-up fact
        i0 = full_text.index("0.5 percent in June")
        a = glyphs(full_text[:i0])
        b = a + glyphs("0.5 percent in June")
        span = full[a:b]
        line = Line(span.get_corner(DL) + DOWN * 0.12, span.get_corner(DR) + DOWN * 0.12, color=ERED, stroke_width=6)
        cap = self.say(cap, "Nothing was looked up. “0.5 percent in June” is a number that fits — not a fact.", wait=0)
        self.play(Create(line), run_time=1.5)
        self.wait(4.0)
