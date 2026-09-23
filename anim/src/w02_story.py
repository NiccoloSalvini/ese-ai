"""Week 2 clips. Numbers come from lectures/img/w02_story.json (written by w02_story.py)."""
import json
from pathlib import Path
from manim import *
from common import NAVY, RED, GREY, GOLD, GREEN

S = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_story.json").read_text())
MONO = "Menlo"


def pct(v, d=1):
    return (f"{v*100:+.{d}f}%").replace("-", "−")


class Temperature(Scene):
    """The same five probabilities from week 1, reshaped by temperature."""

    def construct(self):
        T = S["temperature"]
        tokens = T["tokens"]
        title = Text("Temperature reshapes the odds", font_size=32, weight=BOLD).to_edge(UP, buff=0.3)
        ctx = Text("“The ECB left rates …”", font_size=24, color=GREY).next_to(title, DOWN, buff=0.2)
        self.add(title, ctx)
        base_y, H = -1.7, 3.1
        xs = [-4.6 + i * 2.1 for i in range(5)]
        labels = VGroup(*[Text(tok, font_size=22).move_to([x, base_y - 0.32, 0]) for tok, x in zip(tokens, xs)])
        self.add(labels, Line([-5.8, base_y, 0], [5.8, base_y, 0], color=GREY, stroke_width=2))

        def bars(ps, colour):
            g = VGroup()
            for p, x in zip(ps, xs):
                h = max(p * H, 0.02)
                r = Rectangle(width=1.2, height=h, fill_color=colour, fill_opacity=0.85, stroke_width=0).move_to([x, base_y + h / 2, 0])
                v = Text(f"{p:.2f}", font_size=22, color=WHITE).next_to(r, UP, buff=0.08)
                g.add(VGroup(r, v))
            return g

        tlab = Text("T = 1   the model as trained", font_size=26, color=GOLD).move_to([3.2, 1.55, 0])
        cur = bars(T["probs"]["1"], GOLD)
        self.play(FadeIn(cur), FadeIn(tlab), run_time=0.8)
        self.wait(1.5)
        for key, lab, col in [("2", "T = 2   flatter, more surprises", RED), ("0", "T = 0   always the top token", GREEN),
                              ("0.5", "T = 0.5   sharper", NAVY)]:
            new = bars(T["probs"][key], col)
            nl = Text(lab, font_size=26, color=col).move_to([3.2, 1.55, 0])
            self.play(Transform(cur, new), FadeOut(tlab), FadeIn(nl), run_time=1.1)
            tlab = nl
            self.wait(1.3)
        hand = S["temperature_hand"]
        how = VGroup(
            Text("T = 0.5 by hand: raise each probability to 1/T = 2, then divide by the total", font=MONO, font_size=19, color=NAVY),
            Text("0.62² = 0.384   0.15² = 0.023   …   total = " + f"{hand['total']:.3f}", font=MONO, font_size=19),
            Text(f"0.384 / {hand['total']:.3f} = {hand['result'][0]:.2f}   ← “unchanged”, now {hand['result'][0]:.0%}", font=MONO, font_size=19, color=NAVY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, -3.3, 0])
        self.play(FadeIn(how), run_time=0.8)
        self.wait(3.0)


class Compounding(Scene):
    """Up 50%, down 50%: where do you end up?"""

    def construct(self):
        title = Text("Up 50%, then down 50%", font_size=32, weight=BOLD).to_edge(UP, buff=0.35)
        self.add(title)
        ax = Axes(x_range=[0, 2, 1], y_range=[0, 160, 50], x_length=6, y_length=4.2,
                  axis_config={"color": GREY, "include_tip": False}).shift(LEFT * 2.6 + DOWN * 0.4)
        self.play(Create(ax), run_time=0.6)
        pts = [ax.c2p(0, 100), ax.c2p(1, 150), ax.c2p(2, 75)]
        vals = ["€100", "€150", "€75"]
        dots = VGroup()
        for i, (p, v) in enumerate(zip(pts, vals)):
            d = Dot(p, color=GOLD if i < 2 else RED, radius=0.09)
            l = Text(v, font_size=26, color=WHITE if i < 2 else RED, weight=BOLD).next_to(d, UP, buff=0.15)
            dots.add(VGroup(d, l))
        self.play(FadeIn(dots[0]), run_time=0.4)
        self.play(Create(Line(pts[0], pts[1], color=GOLD, stroke_width=4)), FadeIn(dots[1]), run_time=0.8)
        self.play(Create(Line(pts[1], pts[2], color=RED, stroke_width=4)), FadeIn(dots[2]), run_time=0.8)
        right = VGroup(
            Text("added:", font_size=26, color=GREY),
            Text("+50% − 50% = 0%", font=MONO, font_size=24, color=GOLD),
            Text("compounded:", font_size=26, color=GREY),
            Text("1.5 × 0.5 − 1 = −25%", font=MONO, font_size=24, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, 0.6, 0])
        self.play(FadeIn(right[:2]), run_time=0.7)
        self.wait(1.0)
        self.play(FadeIn(right[2:]), run_time=0.7)
        b = S["btc2022"]
        tail = Text(f"Bitcoin in 2022: added {pct(b['added'], 0)}, really {pct(b['true'], 0)}",
                    font_size=26, color=WHITE, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(tail), run_time=0.7)
        self.wait(3.0)


class TenDays(Scene):
    """Ten real days in January 2024: what a join does to two calendars."""

    def construct(self):
        title = Text("Ten real days, two calendars", font_size=32, weight=BOLD).to_edge(UP, buff=0.3)
        self.add(title)
        days = S["ten_days"]
        xs = [-5.5 + i * 1.0 for i in range(len(days))]
        head = VGroup(*[Text(d["date"][:3] + "\n" + d["date"][4:6], font_size=16, color=GREY, line_spacing=0.8).move_to([x, 2.3, 0])
                        for d, x in zip(days, xs)])
        lab_b = Text("BTC", font_size=22, color=GOLD, weight=BOLD).move_to([-6.6, 1.3, 0])
        lab_s = Text("SPY", font_size=22, color=NAVY, weight=BOLD).move_to([-6.6, 0.4, 0])
        def cell(v, colour, x, y, fmt):
            if v is None:
                return VGroup(Rectangle(width=0.9, height=0.62, stroke_color=GREY, stroke_width=1.2), Text("—", font_size=18, color=GREY)).move_to([x, y, 0])
            return VGroup(Rectangle(width=0.9, height=0.62, stroke_color=colour, stroke_width=2, fill_color=colour, fill_opacity=0.2),
                          Text(fmt(v), font_size=15)).move_to([x, y, 0])
        btc = VGroup(*[cell(d["btc"], GOLD, x, 1.3, lambda v: f"{v/1000:.1f}k") for d, x in zip(days, xs)])
        spy = VGroup(*[cell(d["spy"], NAVY, x, 0.4, lambda v: f"{v:.0f}") for d, x in zip(days, xs)])
        self.play(FadeIn(head), FadeIn(lab_b), FadeIn(lab_s), FadeIn(btc), FadeIn(spy), run_time=1.0)
        original = btc.copy()
        n = S["ten_rows"]
        c1 = Text(f"BTC: {n['btc']} days.  SPY: {n['spy']} days — weekends, and Monday 15 Jan was a US holiday.", font_size=23).move_to([0, -0.5, 0])
        self.play(FadeIn(c1), run_time=0.6)
        self.wait(1.8)
        gone = [i for i, d in enumerate(days) if d["spy"] is None]
        note = Text(f"Inner join: keep only days both have → {n['both']} rows", font_size=26, color=GREEN, weight=BOLD).move_to([0, -1.25, 0])
        self.play(FadeIn(note), *[btc[i].animate.set_opacity(0.15) for i in gone], run_time=0.9)
        m = S["monday"]
        mon = [i for i, d in enumerate(days) if d["date"].startswith("Mon 08")][0]
        box = SurroundingRectangle(btc[mon], color=RED, buff=0.06)
        m1 = Text(f"BTC’s ‘Monday return’ is now Friday → Monday: {pct(m['three_days'])} over three days, labelled as one.",
                  font_size=22, color=RED).move_to([0, -1.95, 0])
        self.play(Create(box), FadeIn(m1), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(note), FadeOut(m1), FadeOut(box), *[Transform(btc[i], original[i]) for i in gone], run_time=0.6)
        note2 = Text("Forward fill: copy SPY’s last price into the empty days", font_size=26, color=GOLD, weight=BOLD).move_to([0, -1.25, 0])
        ghosts = VGroup()
        last = None
        for i, d in enumerate(days):
            if d["spy"] is not None:
                last = d["spy"]
            else:
                ghosts.add(VGroup(Rectangle(width=0.9, height=0.62, stroke_color=NAVY, stroke_width=1.5, fill_color=NAVY, fill_opacity=0.08),
                                  Text(f"{last:.0f}", font_size=15, color=GREY)).move_to([xs[i], 0.4, 0]))
        m2 = Text("SPY ‘returned’ exactly 0% on each of those days. It never traded.", font_size=22, color=RED).move_to([0, -1.95, 0])
        self.play(FadeIn(note2), FadeIn(ghosts), run_time=0.9)
        self.play(FadeIn(m2), run_time=0.6)
        self.wait(2.0)
        end = Text("Decide which days exist before you compute anything across assets.", font_size=22, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(end), run_time=0.7)
        self.wait(2.2)
