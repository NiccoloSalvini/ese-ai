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


class AttentionForHumans(Scene):
    """The same numbers as AttentionByHand, told without jargon, on a white stage.

    The meaning map is the 2D `values` from the JSON: bank = (1, 0), rates = (0, 1),
    the other words = (0, 0). "it" starts at its own value (0, 0) and moves to `mixed`.
    """

    def construct(self):
        self.camera.background_color = WHITE
        INK, ERED, EGOLD, ENAVY, FAINT = "#363636", "#AF1F25", "#CDBA80", "#2471a3", "#b5b5b5"
        SANS = "Helvetica Neue"
        A = S["toy_attention"]
        toks, W = A["tokens"], A["weights"]
        it_i = toks.index("it")

        def T(s, size=28, color=INK, **kw):
            return Text(s, font=SANS, font_size=size, color=color, **kw)

        cap = T("Every word starts with a fixed meaning — the same in every sentence.", 28)
        cap.to_edge(DOWN, buff=0.35)

        def recap(s, size=28):
            new = T(s, size).to_edge(DOWN, buff=0.35)
            return new

        # 1 · the sentence; "feared inflation." is not written yet when "it" is produced
        shown = toks + ["feared", "inflation."]
        words = VGroup(*[T(w, 36, INK if i < len(toks) else FAINT) for i, w in enumerate(shown)])
        words.arrange(RIGHT, buff=0.42).move_to([0, 2.1, 0])
        self.play(FadeIn(words), FadeIn(cap), run_time=2.0)
        self.wait(3.0)

        # 2 · "it" alone
        c2 = recap("“it” alone means nothing. It reads the words before it.")
        self.play(words[it_i].animate.set_color(ERED).scale(1.15), Transform(cap, c2), run_time=2.0)
        note = T("not written yet", 22, FAINT).next_to(VGroup(words[-2], words[-1]), DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=1.2)
        self.wait(2.5)

        # 3 · how much each word matters to "it"
        c3 = recap("How relevant is each word to me? The answers add up to 100%.")
        arcs, pcts = VGroup(), VGroup()
        src = words[it_i].get_top() + UP * 0.1
        for i, w in enumerate(W):
            if i == it_i:
                continue
            dst = words[i].get_top() + UP * 0.1
            col = ERED if toks[i] == "bank" else ENAVY
            arcs.add(ArcBetweenPoints(src, dst, angle=PI / 3 if i < it_i else -PI / 3,
                                      stroke_color=col, stroke_width=2 + 22 * w,
                                      stroke_opacity=0.35 + 0.65 * w / max(W)))
        for i, w in enumerate(W):
            col = ERED if toks[i] == "bank" else INK
            pcts.add(T(f"{w:.0%}", 28, col, weight=BOLD if toks[i] == "bank" else NORMAL)
                     .next_to(words[i], DOWN, buff=0.3))
        self.play(Transform(cap, c3), FadeOut(note), run_time=1.5)
        self.play(Create(arcs), run_time=2.5)
        self.wait(1.0)
        self.play(FadeIn(pcts, shift=DOWN * 0.1), run_time=2.0)
        self.wait(3.0)

        # 4 · the meaning map, from the JSON values
        O, U = np.array([-2.2, -1.95, 0]), 2.4

        def at(v):
            return O + np.array([v[0] * U, v[1] * U, 0])

        axes = VGroup(Arrow(at((0, 0)), at((1.35, 0)), buff=0, color=FAINT, stroke_width=3),
                      Arrow(at((0, 0)), at((0, 1.15)), buff=0, color=FAINT, stroke_width=3))
        ax_x = T("about a bank →", 24, FAINT).next_to(at((1.35, 0)), RIGHT, buff=0.15)
        ax_y = T("about interest rates ↑", 24, FAINT).next_to(at((0, 1.15)), RIGHT, buff=0.25)
        vals = A["values"]
        bank_d = Dot(at(vals[toks.index("bank")]), radius=0.13, color=ERED)
        bank_l = T("bank", 28, ERED).next_to(bank_d, DOWN, buff=0.15)
        rates_d = Dot(at(vals[toks.index("rates")]), radius=0.13, color=ENAVY)
        rates_l = T("rates", 28, ENAVY).next_to(rates_d, LEFT, buff=0.2)
        rest_l = T("The, raised, because", 24, FAINT).next_to(at((0, 0)), LEFT, buff=0.25)
        it_d = Circle(radius=0.15, stroke_color=FAINT, stroke_width=4).move_to(at(vals[it_i]))
        it_l = T("it", 30, FAINT).next_to(it_d, UP + RIGHT, buff=0.05)
        c4a = recap("A map of meaning. “it”, on its own, sits in the middle: empty.")
        self.play(FadeOut(arcs), Transform(cap, c4a), run_time=1.5)
        self.play(Create(axes), FadeIn(ax_x), FadeIn(ax_y), run_time=2.0)
        self.play(FadeIn(bank_d), FadeIn(bank_l), FadeIn(rates_d), FadeIn(rates_l), FadeIn(rest_l), run_time=2.0)
        self.play(FadeIn(it_d), FadeIn(it_l), run_time=1.5)
        self.wait(2.5)

        m = A["mixed"]
        wb, wr = W[toks.index("bank")], W[toks.index("rates")]
        c4b = recap(f"New meaning of “it” = {wb:.0%} bank + {wr:.0%} rates + … → it now means the bank.", 27)
        it_new = Dot(at(m), radius=0.15, color=ERED)
        self.play(Transform(cap, c4b), run_time=1.5)
        self.play(Transform(it_d, it_new), it_l.animate.set_color(ERED).next_to(it_new, UP + LEFT, buff=0.05),
                  run_time=3.0)
        self.wait(3.0)

        # 5 · the general statement
        c5 = recap("Every word does this, at the same time, with every other word —\nin every layer. That is attention.", 27)
        self.play(Transform(cap, c5), run_time=2.0)
        self.wait(4.5)
