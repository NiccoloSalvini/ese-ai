"""Week 2 clips — how word vectors are built, and how context moves them (attention).

White stage, slow, for a non-technical reader. Every number from lectures/img/w02_embed_toy.json
(written by lectures/img/w02_embed_toy.py): a real toy run of the training loop on 12 sentences,
then a simplified attention step on two of them. Both clips share one map scaling, so the last
frame of BuildEmbeddings is the first map of ContextMoves.
"""
import json
from pathlib import Path
import numpy as np
from manim import *

D = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_embed_toy.json").read_text())
WORDS = D["words"]
IX = {w: i for i, w in enumerate(WORDS)}

INK, MUTED, RULE = "#363636", "#7a7f85", "#e6e2d8"
ERED, ENAVY, EGREEN = "#AF1F25", "#2471a3", "#1e8449"
SANS = "Helvetica Neue"
MONEY = ["lender", "loan", "rates", "raised", "cut", "gave"]
RIVER = ["river", "water", "shore", "flooded", "covered", "sat"]

# one map for both clips: data -> screen
S, DX, DY, CX, CY = 1.08, -0.85, 0.8, 2.2, 0.1
FRAME = (-1.55, -3.0, 6.85, 3.25)          # x0, y0, x1, y1 of the map panel


def colour(w):
    return ERED if w == "bank" else ENAVY if w in MONEY else EGREEN


def scr(p):
    return np.array([CX + S * (p[0] - DX), CY + S * (p[1] - DY), 0.0])


def T(s, size=26, color=INK, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def caption(s, **kw):
    c = T(s, 26, INK, **kw)
    if c.width > 13.2:
        c.scale_to_fit_width(13.2)
    return c.move_to([0, -3.55, 0])


def snap(key):
    return [scr(p) for p in D["snapshots"][key]]


# ------------------------------------------------------------------ labels that never overlap
def _overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def map_group(pts, avoid=(), size=24):
    """Dots + labels + (invisible unless needed) leader lines, one VGroup per word, same order as WORDS.
    Words sitting on the same spot share one label ("rates, loan, gave") — same company, same place."""
    pad = 0.05
    n = len(WORDS)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(pts[i] - pts[j]) < 0.28:
                parent[find(j)] = find(i)
    clusters = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)

    dot_boxes = [(p[0] - 0.12, p[1] - 0.12, p[0] + 0.12, p[1] + 0.12) for p in pts]
    placed = list(avoid)
    heads = sorted(clusters, key=lambda k: -sum(np.linalg.norm(pts[k] - q) < 0.8 for q in pts))
    chosen = {}
    for k in heads:
        members = clusters[k]
        ws = [WORDS[i] for i in members]
        txt = ", ".join(ws)
        lab = T(txt, size, colour(ws[0]), t2c={w: colour(w) for w in ws},
                weight=BOLD if ws == ["bank"] else NORMAL)
        lw, lh = lab.width, lab.height
        p = np.mean([pts[i] for i in members], axis=0)
        best = None
        for r in (0.14, 0.3, 0.5, 0.75, 1.0, 1.3):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
                cx = p[0] + dx * (r + lw / 2)
                cy = p[1] + dy * (r + lh / 2)
                box = (cx - lw / 2 - pad, cy - lh / 2 - pad, cx + lw / 2 + pad, cy + lh / 2 + pad)
                score = sum(_overlap(box, b) for b in placed) * 10
                score += sum(_overlap(box, b) for j, b in enumerate(dot_boxes) if j not in members) * 10
                out = max(0, FRAME[0] + 0.1 - box[0]) + max(0, box[2] - FRAME[2] + 0.1) \
                    + max(0, FRAME[1] + 0.1 - box[1]) + max(0, box[3] - FRAME[3] + 0.1)
                score += out * 20 + r * 0.08 + (0.02 if dx == 0 or dy != 0 else 0)
                if best is None or score < best[0]:
                    best = (score, cx, cy, dx, dy, r, box)
        _, cx, cy, dx, dy, r, box = best
        placed.append(box)
        lab.move_to([cx, cy, 0])
        end = np.array([cx - dx * (lw / 2 + 0.04), cy - dy * (lh / 2 + 0.04), 0])
        v = end - p
        start = p + (v / (np.linalg.norm(v) + 1e-9)) * 0.1
        for m_i, i in enumerate(members):
            w = WORDS[i]
            if m_i == 0:
                lb, op = lab, (0.7 if r >= 0.45 else 0.0)
            else:                                   # the shared label carries this word; keep a hidden stand-in
                lb, op = T(w, size, colour(w)).move_to(lab).set_opacity(0), 0.0
            lead = Line(start, end if np.linalg.norm(v) > 0.12 else start + 0.001 * RIGHT, stroke_width=1.2,
                        color=MUTED, stroke_opacity=op)
            chosen[i] = VGroup(Dot(pts[i], radius=0.09, color=colour(w)), lb, lead)
    return VGroup(*[chosen[i] for i in range(n)])


def map_frame():
    x0, y0, x1, y1 = FRAME
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=RULE, stroke_width=2).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def legend():
    a = VGroup(Dot(radius=0.09, color=ENAVY), T("money words", 24, ENAVY)).arrange(RIGHT, buff=0.15)
    b = VGroup(Dot(radius=0.09, color=EGREEN), T("river words", 24, EGREEN)).arrange(RIGHT, buff=0.15)
    return VGroup(a, b).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-4.35, -2.35, 0])


def nearest(group):
    """The money word and the river word closest to "bank" on the final map (computed, not chosen)."""
    P = D["snapshots"]["400"]
    b = np.array(P[IX["bank"]])
    return min(group, key=lambda w: np.linalg.norm(np.array(P[IX[w]]) - b))


MOVED = [("bank (raised rates)", "new", DOWN), ("bank (river flooded)", "new", DOWN)]


def moved_labels():
    """The two in-context "bank" labels, positioned where ContextMoves puts them."""
    out = []
    for (txt, key, d), A in zip(MOVED, D["attention"]):
        lab = T(txt, 24, ERED, weight=BOLD)
        dot = Dot(scr(A[key]), radius=0.11)
        lab.next_to(dot, d, buff=0.18)
        out.append(lab)
    return out


def keep_clear():
    boxes = []
    for lab, A in zip(moved_labels(), D["attention"]):
        c = lab.get_center()
        boxes.append((c[0] - lab.width / 2 - 0.05, c[1] - lab.height / 2 - 0.05, c[0] + lab.width / 2 + 0.05, c[1] + lab.height / 2 + 0.05))
        q = scr(A["new"])
        boxes.append((q[0] - 0.15, q[1] - 0.15, q[0] + 0.15, q[1] + 0.15))
    return boxes


# ------------------------------------------------------------------ clip 1
class BuildEmbeddings(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        head = T("the training text", 24, MUTED).move_to([-4.35, 2.75, 0])
        shown = ["the bank raised rates", "the lender raised rates", "the river flooded the bank",
                 "water covered the shore"]
        rows = VGroup()
        for k, s in enumerate(shown):
            r = T(s, 24, INK, t2c={"bank": ERED})
            r.move_to([-4.35, 2.1 - k * 0.62, 0])
            rows.add(r)
        more = T(f"… {len(D['sentences']) - len(shown)} more", 24, MUTED).move_to([-4.35, 2.1 - 4 * 0.62, 0])
        cap = caption("The training text: 12 short sentences. Note: “bank” appears with money AND with rivers.",
                      t2c={"bank": ERED})
        self.play(FadeIn(head), FadeIn(rows, lag_ratio=0.3), FadeIn(more), run_time=2.2)
        self.play(FadeIn(cap), run_time=1.0)
        self.wait(3.0)

        # 2 · random start
        frame = map_frame()
        counter = T("round 0", 26, MUTED).move_to([5.9, 3.6, 0])
        G = map_group(snap("0"))
        cap2 = caption("Every word starts at a random place on the map.")
        self.play(Create(frame), run_time=1.2)
        self.play(FadeIn(G, lag_ratio=0.08), FadeIn(counter), FadeTransform(cap, cap2), run_time=2.2)
        self.wait(3.0)

        # 3 · one nudge: lender, next to rates in "the lender raised rates"
        hl = SurroundingRectangle(rows[1], color=ENAVY, buff=0.08, stroke_width=2)
        li, ri = IX["lender"], IX["rates"]
        ring_l = Circle(radius=0.22, color=ENAVY, stroke_width=3).move_to(G[li][0])
        ring_r = Circle(radius=0.22, color=ENAVY, stroke_width=3).move_to(G[ri][0])
        cap3 = caption("The loop from last week: guess which words appear nearby, see how wrong, nudge the place.")
        self.play(Create(hl), Create(ring_l), Create(ring_r), FadeTransform(cap2, cap3), run_time=2.0)
        self.wait(1.5)
        p0, p20 = snap("0")[li], snap("20")[li]
        nudge = Arrow(p0, p20, buff=0.05, color=ERED, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        tag = T("pushed this way", 24, ERED).next_to(nudge.get_end(), DOWN + LEFT, buff=0.12)
        self.play(GrowArrow(nudge), FadeIn(tag), run_time=2.0)
        self.wait(3.0)

        # 4 · rounds
        cap4 = caption("Round after round, words that keep the same company end up close.")
        self.play(FadeOut(nudge), FadeOut(tag), FadeOut(ring_l), FadeOut(ring_r), FadeOut(hl), FadeTransform(cap3, cap4),
                  run_time=1.2)
        for key in ["5", "20", "60", "150", "400"]:
            new_counter = T(f"round {key}", 26, MUTED).move_to(counter)
            self.play(Transform(G, map_group(snap(key), avoid=keep_clear() if key == "400" else ())), FadeTransform(counter, new_counter), run_time=2.5)
            counter = new_counter
            self.wait(1.4)

        # 5 · bank in between: its nearest money word and its nearest river word
        L = legend()
        nm, nr = nearest(MONEY), nearest(RIVER)
        pb = G[IX["bank"]][0].get_center()
        ln_m = DashedLine(pb, G[IX[nm]][0].get_center(), color=ENAVY, stroke_width=3)
        ln_r = DashedLine(pb, G[IX[nr]][0].get_center(), color=EGREEN, stroke_width=3)
        close = VGroup(T("closest to “bank”:", 24, INK, t2c={"bank": ERED}),
                       T(f"{nr} and {nm}", 24, INK, t2c={nr: EGREEN, nm: ENAVY})).arrange(DOWN, buff=0.12) \
            .move_to([-4.35, 2.1 - 5.4 * 0.62, 0])
        cap5 = caption("“bank” lands in between: one place for two meanings. Nobody drew this map.", t2c={"bank": ERED})
        self.play(FadeIn(L), FadeTransform(cap4, cap5), run_time=2.0)
        self.play(Create(ln_m), Create(ln_r), FadeIn(close), run_time=2.0)
        b = G[IX["bank"]][0]
        self.play(b.animate.scale(1.6), run_time=0.8)
        self.play(b.animate.scale(1 / 1.6), run_time=0.8)
        self.wait(4.0)


# ------------------------------------------------------------------ clip 2
class ContextMoves(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        A0, A1 = D["attention"]
        frame = map_frame()
        G = map_group(snap("400"), avoid=keep_clear())
        R = legend()
        bank = G[IX["bank"]]
        cap = caption("One place for “bank” — wrong in both of these sentences.", t2c={"bank": ERED})
        self.play(Create(frame), FadeIn(R), FadeIn(G), run_time=2.0)
        self.play(FadeIn(cap), Indicate(bank[0], color=ERED, scale_factor=1.8), run_time=1.8)
        self.wait(3.0)

        old = scr(A0["old"])
        ghost = Dot(old, radius=0.09, color=ERED, fill_opacity=0.25)

        def attend(A, top_y, col, moved_label_pos):
            sent = T(A["sentence"], 26, INK, t2c={"bank": ERED}).move_to([-4.35, top_y, 0])
            lines, pcts, rows = VGroup(), VGroup(), VGroup()
            dirs = [scr(D["snapshots"]["400"][IX[w]]) - old for w in A["others"]]
            for k, (w, sh) in enumerate(zip(A["others"], A["share"])):
                q = scr(D["snapshots"]["400"][IX[w]])
                ln = Line(old, q, color=col, stroke_width=3 + 14 * sh, stroke_opacity=0.55)
                lines.add(ln)
                mid = old * 0.62 + q * 0.38
                v = (q - old) / np.linalg.norm(q - old)
                nrm = np.array([-v[1], v[0], 0.0])
                other = dirs[1 - k] / np.linalg.norm(dirs[1 - k])
                nrm = -nrm if nrm @ other > 0 else nrm          # each % on the outer side, away from the other line
                pc = T(f"{sh:.0%}", 24, col, weight=BOLD).move_to(mid + nrm * 0.32)
                pcts.add(pc)
                rows.add(T(f"{w}  {sh:.0%}", 24, col).move_to([-4.35, top_y - 0.6 - k * 0.5, 0]))
            return sent, lines, pcts, rows

        # 2 · sentence 1: how much each neighbour matters
        s1, l1, p1, r1 = attend(A0, 2.75, ENAVY, None)
        cap2 = caption("Attention: how much does each neighbour matter to “bank”? (shares of 100%)", t2c={"bank": ERED})
        self.play(FadeIn(s1), run_time=1.5)
        self.play(Create(l1), FadeTransform(cap, cap2), run_time=2.2)
        self.play(FadeIn(p1), FadeIn(r1), run_time=1.5)
        self.wait(3.0)

        # 3 · bank keeps its place and adds a mix of its neighbours
        new0 = scr(A0["new"])
        c1 = Dot(old, radius=0.11, color=ERED)
        cap3 = caption("“bank” keeps its place and adds a mix of its neighbours → it moves towards money.",
                       t2c={"bank": ERED, "money": ENAVY})
        self.add(ghost)
        self.play(FadeTransform(cap2, cap3), run_time=1.0)
        self.play(c1.animate.move_to(new0), FadeOut(p1), l1.animate.set_stroke(opacity=0.18), run_time=2.5)
        lab1 = moved_labels()[0]
        self.play(FadeIn(lab1), run_time=1.0)
        self.wait(3.0)

        # 4 · sentence 2
        self.play(FadeOut(l1), s1.animate.set_opacity(0.35), r1.animate.set_opacity(0.35), run_time=1.0)
        s2, l2, p2, r2 = attend(A1, 0.85, EGREEN, None)
        cap4 = caption("Same word, other sentence → it moves towards the river.", t2c={"river": EGREEN})
        self.play(FadeIn(s2), run_time=1.5)
        self.play(Create(l2), FadeIn(p2), FadeIn(r2), FadeTransform(cap3, cap4), run_time=2.2)
        self.wait(2.5)
        new1 = scr(A1["new"])
        c2 = Dot(old, radius=0.11, color=ERED)
        self.play(c2.animate.move_to(new1), FadeOut(p2), l2.animate.set_stroke(opacity=0.18), run_time=2.5)
        lab2 = moved_labels()[1]
        self.play(FadeIn(lab2), run_time=1.0)
        self.wait(3.0)

        # 5 · one place per word in this sentence
        self.play(FadeOut(l2), s1.animate.set_opacity(1), r1.animate.set_opacity(1), run_time=1.0)
        l1_ = T("Before attention: one place per word.", 26, INK)
        l2_ = T("After: one place per word in this sentence. That is what attention does.", 26, INK,
                t2s={"in this sentence": ITALIC}, t2c={"in this sentence": ERED})
        cap5 = VGroup(l1_, l2_).arrange(DOWN, buff=0.12).move_to([0, -3.52, 0])
        self.play(FadeTransform(cap4, cap5), Indicate(c1, color=ERED, scale_factor=1.6),
                  Indicate(c2, color=ERED, scale_factor=1.6), run_time=2.0)
        self.wait(6.0)
