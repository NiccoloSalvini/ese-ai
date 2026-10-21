"""Hand-drawn figure for week 4 (lectures/04-rag.qmd): where the test sits.
Pure box-and-arrow, no numbers. Run: python figs_w04.py"""
from pathlib import Path

HERE = Path(__file__).parent
RED, GOLDDK, NAVY, GREEN, INK, MUTED, RULE = "#AF1F25", "#a8955a", "#2471a3", "#1e8449", "#363636", "#7a7f85", "#e6e2d8"
NAVY_BG, RED_BG, PAPER, PAPER_LN = "#eaf1f7", "#faeeee", "#fcfbf8", "#c9c4b8"
FONT = "font-family=\"'Source Sans 3','Source Sans Pro',-apple-system,Helvetica,Arial,sans-serif\""
DEFS = f'''  <defs>
    <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{GOLDDK}"/></marker>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>
    <marker id="an" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>
  </defs>'''


def t(x, y, s, size=13, fill=INK, weight="400", anchor="middle"):
    return f'  <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, title, sub="", fill=PAPER, stroke=PAPER_LN, col=INK, sw=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>']
    if sub:
        out += [t(x + w / 2, y + h / 2 - 3, title, 16, col, "700"), t(x + w / 2, y + h / 2 + 17, sub, 12, MUTED)]
    else:
        out += [t(x + w / 2, y + h / 2 + 6, title, 16, col, "700")]
    return out


def arrow(x1, y1, x2, y2, col="ag", stroke=GOLDDK):
    return [f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="2" marker-end="url(#{col})"/>']


W, H = 960, 420
body = []
# ---- row 1: ship first
y1 = 80
body += [t(30, y1 - 14, "SHIP, THEN FIND OUT", 12, RED, "700", "start")]
body += box(30, y1, 170, 64, "build", "a model, a corpus")
body += arrow(206, y1 + 32, 236, y1 + 32)
body += box(244, y1, 170, 64, "ship", "to every customer")
body += arrow(420, y1 + 32, 450, y1 + 32, "ar", RED)
body += box(458, y1, 300, 64, "the test, written by others", "a tribunal, a CEO interview, a refund", RED_BG, RED, RED, 2)
body += [t(930, y1 + 26, "Air Canada, 2024", 12, MUTED, anchor="end"), t(930, y1 + 44, "Klarna, 2025", 12, MUTED, anchor="end")]

body += [f'  <line x1="30" y1="196" x2="930" y2="196" stroke="{RULE}" stroke-width="1"/>']

# ---- row 2: test first
y2 = 232
body += [t(30, y2 - 14, "TEST, THEN SHIP", 12, NAVY, "700", "start")]
body += box(30, y2, 200, 64, "write the test", "questions with known answers", NAVY_BG, NAVY, NAVY, 2)
body += arrow(236, y2 + 32, 266, y2 + 32, "an", NAVY)
body += box(274, y2, 170, 64, "build", "a model, a corpus")
body += arrow(450, y2 + 32, 480, y2 + 32, "an", NAVY)
body += box(488, y2, 170, 64, "run the test", "hits, misses, which kind", NAVY_BG, NAVY, NAVY, 2)
body += arrow(664, y2 + 32, 694, y2 + 32, "an", NAVY)
body += box(702, y2, 150, 64, "ship", "and keep running it")
# loop back from run-the-test to build
body += [f'  <path d="M 573 {y2 + 70} L 573 {y2 + 100} L 359 {y2 + 100} L 359 {y2 + 76}" fill="none" stroke="{NAVY}" stroke-width="2" marker-end="url(#an)"/>']
body += [t(466, y2 + 116, "a miss → change one thing → run it again", 12, NAVY)]
body += [t(930, y2 + 36, "Morgan Stanley, 2023", 12, MUTED, anchor="end")]

body += [t(30, 396, "Same four boxes. The only difference is where the test sits — and who wrote it.", 15, INK, "700", "start")]

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
       f'  <rect width="{W}" height="{H}" fill="#ffffff"/>', DEFS,
       f'  <text x="30" y="34" font-size="13" fill="{MUTED}">the same boxes in a different order</text>'] + body + ['</svg>']
(HERE / "w04-test-first.svg").write_text("\n".join(svg), encoding="utf-8")
print("wrote w04-test-first.svg")
