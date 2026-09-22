"""Week 1 — the same Russian sentence under two tokenizers of the same model family.

    manim -qm src/w01_tokens.py TwoTokenizers -o w01_tokens.mp4

Token strings are the real output of tiktoken 0.14 (cl100k_base, o200k_base).
Text() and not Tex(): manim's default LaTeX template has no Cyrillic, Pango does.
"""
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN

EN = ["The", "quarterly", "margin", "came", "in", "below", "the",
      "guidance", "we", "gave", "investors", "."]

# cl100k_base — the GPT-3.5 / GPT-4 tokenizer. 33 pieces.
OLD = ["К", "в", "арт", "аль", "ная", " м", "ар", "ж", "а", " о", "каз", "ал",
       "ас", "ь", " н", "и", "же", " пр", "ог", "н", "оз", "а", ",", " который",
       " мы", " д", "али", " ин", "в", "ест", "ор", "ам", "."]

# o200k_base — the GPT-4o tokenizer. 18 pieces of the identical sentence.
NEW = ["К", "варт", "альная", " мар", "жа", " оказ", "алась", " ниже", " прог",
       "н", "оза", ",", " который", " мы", " дали", " инвест", "орам", "."]


def groups(old, new):
    """Which old pieces make up each new piece, by walking character offsets.

    Both lists spell the same string, so the grouping is forced: consume old
    pieces until their lengths reach the end of the current new piece. Computing
    it beats hard-coding it — if a token list is ever edited the merge follows.
    """
    out, i, pos = [], 0, 0
    for tok in new:
        end, g = pos + len(tok), []
        while pos < end:
            g.append(i); pos += len(old[i]); i += 1
        out.append(g)
    assert i == len(old) and "".join(old) == "".join(new)
    return out


def chips(tokens, colour, font_size, rows, y_top, row_gap, pad=0.09):
    """Lay tokens out as boxed chips, wrapped into `rows` lines centred on screen."""
    per = -(-len(tokens) // rows)
    lines, k = VGroup(), 0
    for r in range(rows):
        line = VGroup()
        for tok in tokens[k:k + per]:
            label = Text(tok.strip() or "␣", font_size=font_size, color=colour)
            box = Rectangle(width=label.width + 2 * pad, height=label.height + 2 * pad,
                            stroke_color=colour, stroke_width=2,
                            fill_color=colour, fill_opacity=0.10)
            line.add(VGroup(box, label.move_to(box)))
        line.arrange(RIGHT, buff=0.07)
        if line.width > 12.6:
            line.scale(12.6 / line.width)
        line.move_to([0, y_top - r * row_gap, 0])
        lines.add(line)
        k += per
    return lines


class TwoTokenizers(Scene):
    def construct(self):
        title = Text("One sentence. One model family. Two tokenizers.",
                     font_size=30, color=NAVY).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)

        en_lbl = Text("English", font_size=22, color=GREY).move_to([-6.2, 2.45, 0], LEFT)
        en = chips(EN, GREY, 20, 1, 2.45, 0)[0].scale(0.88).move_to([-0.7, 2.45, 0])
        en_n = Text("12 tokens", font_size=22, color=GREY).move_to([6.35, 2.45, 0], RIGHT)
        self.play(FadeIn(en_lbl), LaggedStart(*[FadeIn(c) for c in en], lag_ratio=0.05),
                  run_time=1.6)
        self.play(FadeIn(en_n), run_time=0.4)

        ru = Text("Квартальная маржа оказалась ниже прогноза, который мы дали инвесторам.",
                  font_size=24, color=NAVY).move_to([0, 1.5, 0])
        self.play(FadeIn(ru), run_time=1.0)

        tag = Text("GPT-4 tokenizer  (cl100k)", font_size=22, color=RED).move_to([-6.2, 0.55, 0], LEFT)
        old_rows = chips(OLD, RED, 19, 2, 0.0, 0.85)
        old_flat = VGroup(*[c for row in old_rows for c in row])
        self.play(FadeIn(tag), LaggedStart(*[FadeIn(c) for c in old_flat], lag_ratio=0.035),
                  run_time=2.1)

        count = Text("33 tokens  ·  2.75× the English bill", font_size=28, color=RED).move_to([0, -1.35, 0])
        self.play(Write(count), run_time=0.9)
        self.wait(0.6)

        tag2 = Text("GPT-4o tokenizer  (o200k)", font_size=22, color=GREEN).move_to([-6.2, 0.55, 0], LEFT)
        new_row = chips(NEW, GREEN, 19, 1, -0.05, 0)[0]
        merges = [ReplacementTransform(VGroup(*[old_flat[i] for i in g]).copy(), new_row[j])
                  for j, g in enumerate(groups(OLD, NEW))]
        count2 = Text("18 tokens  ·  1.50× the English bill", font_size=28, color=GREEN).move_to([0, -1.35, 0])
        self.play(FadeOut(old_flat), Transform(tag, tag2),
                  LaggedStart(*merges, lag_ratio=0.05), run_time=1.9)
        self.play(Transform(count, count2), run_time=0.7)

        note = Text("Nothing about the model got smarter. The same document halved in price.",
                    font_size=27, color=GOLD).to_edge(DOWN, buff=0.45)
        self.play(Write(note), run_time=1.4)
        self.wait(0.9)
