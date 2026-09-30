"""Week 2 clip — how a tokenizer is built. Numbers from lectures/img/w02_bpe.json (w02_bpe.py).

White stage, slow: letters as tiles, count neighbour pairs, glue the most frequent pair,
repeat until a frequent word is one tile; then a new word stays in fragments.
"""
import json
from pathlib import Path
from manim import *

S = json.loads((Path(__file__).resolve().parents[2] / "lectures/img/w02_bpe.json").read_text())

INK, ERED, EGOLD, ENAVY, MUTED = "#363636", "#AF1F25", "#CDBA80", "#2471a3", "#7a7f85"
SANS = "Helvetica Neue"
U, PAD, GAP, H = 0.30, 0.10, 0.045, 0.62     # per-letter width, tile padding, gap, tile height
ROW_Y = 2.0


def T(s, size=28, color=INK, **kw):
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def show(piece):
    return piece.replace("_", "·")


def tile(piece, stroke=ENAVY, fill="#ffffff"):
    w = U * len(piece) + PAD
    box = Rectangle(width=w, height=H, stroke_color=stroke, stroke_width=2.2, fill_color=fill, fill_opacity=1)
    col = MUTED if piece in ("_", ",") else INK
    lab = T(show(piece), 30, col)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def layout(pieces, y=ROW_Y):
    widths = [U * len(p) + PAD for p in pieces]
    total = sum(widths) + GAP * (len(pieces) - 1)
    x = -total / 2
    xs = []
    for w in widths:
        xs.append(x + w / 2)
        x += w + GAP
    return [np.array([cx, y, 0]) for cx in xs]


class BuildTokenizer(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        def caption(s):
            return T(s, 28).to_edge(DOWN, buff=0.4)

        # 1 · single letters
        pieces = list(S["start"])
        tiles = [tile(p).move_to(pos) for p, pos in zip(pieces, layout(pieces))]
        row = VGroup(*tiles)
        cap = caption("1 · Start from single letters.")
        count = T(f"{len(pieces)} pieces", 28, ENAVY).move_to([4.6, 0.9, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=0.15 * DOWN) for t in tiles], lag_ratio=0.04), FadeIn(cap), run_time=2.5)
        self.play(FadeIn(count), run_time=1.0)
        self.wait(2.5)

        # vocabulary panel (starts with the letters)
        letters = "  ".join(show(p) for p in S["vocab"][: len(S["vocab"]) - len(S["steps"])])
        vlab = T("vocabulary", 24, MUTED).move_to([0.9, -0.35, 0], aligned_edge=LEFT)
        vlet = T(letters, 24, INK).next_to(vlab, DOWN, buff=0.18, aligned_edge=LEFT)
        self.play(FadeIn(vlab), FadeIn(vlet), run_time=1.5)
        self.wait(1.5)
        vocab_tail = vlet

        # counter panel
        clab = T("most frequent neighbours", 24, MUTED).move_to([-6.2, 0.9, 0], aligned_edge=LEFT)

        for k, st in enumerate(S["steps"]):
            slow = k < 2
            rt = 1.8 if slow else 1.1
            wt = 2.2 if slow else 1.0

            if k == 0:
                self.play(Transform(cap, caption("2 · Count which pair of neighbours appears most often.")), FadeIn(clab), run_time=1.5)
            lines = VGroup(*[T(f"{show(a)} + {show(b)}   ×{c}", 28, INK) for a, b, c in st["top"]])
            lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(clab, DOWN, buff=0.25, aligned_edge=LEFT)

            # occurrences of the winning pair in the current row
            a, b = st["pair"]
            occ = [i for i in range(len(pieces) - 1) if pieces[i] == a and pieces[i + 1] == b]
            # non-overlapping, left to right (the same rule as the merge)
            keep, last = [], -2
            for i in occ:
                if i > last + 1:
                    keep.append(i); last = i
            occ = keep

            if slow:
                # sweep: underline each of the top pairs' occurrences in gold, one pair at a time
                for li, (pa, pb, c) in enumerate(st["top"]):
                    idx = [i for i in range(len(pieces) - 1) if pieces[i] == pa and pieces[i + 1] == pb]
                    marks = VGroup(*[Line(tiles[i].get_corner(DL) + 0.08 * DOWN, tiles[i + 1].get_corner(DR) + 0.08 * DOWN,
                                          color=EGOLD, stroke_width=6) for i in idx])
                    self.play(FadeIn(lines[li]), Create(marks), run_time=1.2)
                    self.wait(0.6)
                    self.play(FadeOut(marks), run_time=0.5)
            else:
                self.play(FadeIn(lines), run_time=0.8)

            # the winner turns red, in the counter and in the text
            self.play(lines[0].animate.set_color(ERED),
                      *[tiles[i][0].animate.set_stroke(ERED, width=4) for i in occ],
                      *[tiles[i + 1][0].animate.set_stroke(ERED, width=4) for i in occ],
                      run_time=rt)
            if k == 0:
                self.play(Transform(cap, caption("3 · Glue it into one new piece. Add it to the vocabulary.")), run_time=1.2)
            if k == 2:
                self.play(Transform(cap, caption("4 · Repeat. Frequent words end up as a single piece.")), run_time=1.0)
            self.wait(wt * 0.6)

            # merge: the two tiles glide together and fuse; then everything re-packs
            new_pieces = st["seq"]
            new_pos = layout(new_pieces)
            new_tiles, anims, j, i = [], [], 0, 0
            while i < len(pieces):
                if i in occ:
                    nt = tile(st["piece"], stroke=ERED, fill="#fbeeee").move_to(new_pos[j])
                    anims.append(ReplacementTransform(VGroup(tiles[i], tiles[i + 1]), nt))
                    new_tiles.append(nt); i += 2
                else:
                    anims.append(tiles[i].animate.move_to(new_pos[j]))
                    new_tiles.append(tiles[i]); i += 1
                j += 1
            vt = tile(st["piece"], stroke=ERED, fill="#fbeeee").scale(0.8)
            vt.next_to(vocab_tail, RIGHT if k else DOWN, buff=0.15, aligned_edge=LEFT if not k else ORIGIN)
            if k == 0:
                vt.next_to(vlet, DOWN, buff=0.2, aligned_edge=LEFT)
            new_count = T(f"{len(new_pieces)} pieces", 28, ENAVY).move_to(count)
            self.play(*anims, FadeIn(vt, shift=0.2 * UP), Transform(count, new_count), run_time=rt + 0.4)
            # settle colours back to navy, keep the newest piece red for a moment
            self.wait(wt * 0.5)
            self.play(*[t[0].animate.set_stroke(ENAVY, width=2.2).set_fill("#ffffff") for t in new_tiles],
                      vt[0].animate.set_stroke(ENAVY, width=2.2).set_fill("#ffffff"),
                      FadeOut(lines), run_time=0.7)
            tiles, pieces, vocab_tail = new_tiles, list(new_pieces), vt
            self.wait(wt * 0.4)

        # the word is one piece now: emphasise the three "rates"
        full = [t for t, p in zip(tiles, pieces) if p == "rates"]
        start_n, end_n = S["start_pieces"], len(pieces)
        self.play(*[t[0].animate.set_stroke(ERED, width=4) for t in full], FadeOut(clab),
                  Transform(count, T(f"{start_n} pieces → {end_n}", 28, ENAVY).move_to(count)), run_time=1.6)
        self.wait(3.0)

        # 5 · a new word, cut with the learned pieces
        nw = S["new_word"]
        nlab = T(f"a new word: “{nw}”", 28, INK).move_to([-6.2, 0.9, 0], aligned_edge=LEFT)
        letters_row = [tile(c) for c in nw]
        lpos = layout(list(nw), y=-0.3)
        for t, p in zip(letters_row, lpos):
            t.move_to(p + np.array([-3.3, 0, 0]))
        self.play(FadeIn(nlab), *[t[0].animate.set_stroke(ENAVY, width=2.2) for t in full],
                  LaggedStart(*[FadeIn(t) for t in letters_row], lag_ratio=0.15), run_time=2.0)
        self.wait(1.5)
        cut = S["new_word_pieces"]
        cpos = layout(cut, y=-0.3)
        cut_tiles = [tile(p, stroke=EGOLD).move_to(pp + np.array([-3.3, 0, 0])) for p, pp in zip(cut, cpos)]
        # group the letters that fuse into each learned piece
        groups, i = [], 0
        for p in cut:
            groups.append(VGroup(*letters_row[i:i + len(p)])); i += len(p)
        self.play(*[ReplacementTransform(g, ct) for g, ct in zip(groups, cut_tiles)],
                  Transform(cap, caption("Rare words stay in fragments: more pieces, more cost.")), run_time=2.2)
        note = T(f"1 word → {len(cut)} pieces", 28, EGOLD).next_to(VGroup(*cut_tiles), DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=1.2)
        self.wait(3.0)

        # 6 · scale
        fin = VGroup(T("Real tokenizers repeat this on huge amounts of text.", 28),
                     T("gpt-oss’s vocabulary has about 200,000 pieces.", 28, ERED)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(FadeOut(cap), FadeIn(fin), run_time=1.8)
        self.wait(4.0)
