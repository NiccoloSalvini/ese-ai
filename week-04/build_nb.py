"""Builds week-04/session.ipynb with nbformat.
Run:  uv run --with nbformat python build_nb.py   → writes session.ipynb next to this file.

Week 4 is taught in the browser (Gemini Notebook, Google AI Studio, a Google Sheet).
This notebook is an APPENDIX — "under the hood": the call behind AI Studio's *Get code*,
through the same client as week 3, and a cell that scores the golden-set sheet."""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

cells = [
md("""
# Week 4 — Read first, then answer · appendix
**ESE · AI for Business and FinTech · 21 October 2026**

**The lesson does not use this notebook.** Today runs in the browser: Gemini Notebook for the assistant, Google AI Studio for the panels, a Google Sheet for the test. This appendix is for whoever wants to see what *Get code* showed — the same call as week 3, with the documents attached — and to score the sheet with four lines of pandas.

Two cells need a key (Colab ▸ 🔑 *Secrets* ▸ `GEMINI_API_KEY`, see Setup). Without one they print a labelled mock answer and move on.
"""),
code('''
!pip -q install openai pandas
'''),
md("## A1 — The client, as in week 3"),
code('''
import os
from getpass import getpass

PROVIDER = "gemini"          # "gemini" | "openai" | "anthropic"
ENDPOINT = {                 # all three speak the same (OpenAI-style) protocol: one client, three providers
    "gemini":    ("GEMINI_API_KEY",    "https://generativelanguage.googleapis.com/v1beta/openai/", "gemini-2.5-flash"),  # model names change: check AI Studio
    "openai":    ("OPENAI_API_KEY",    None,                                                        "gpt-4.1-mini"),
    "anthropic": ("ANTHROPIC_API_KEY", "https://api.anthropic.com/v1/",                             "claude-haiku-4-5"),
}
KEY_NAME, BASE_URL, MODEL = ENDPOINT[PROVIDER]

key = None
try:
    from google.colab import userdata
    key = userdata.get(KEY_NAME)
except Exception:
    key = os.environ.get(KEY_NAME)
if not key:
    key = getpass(f"{KEY_NAME} (Enter for mock mode): ").strip() or None

MOCK = key is None
if not MOCK:
    from openai import OpenAI
    client = OpenAI(api_key=key, base_url=BASE_URL)
del key
print("MOCK MODE — answers below are NOT from a model" if MOCK else f"live: {PROVIDER} · {MODEL}")
'''),
md("""
## A2 — The document, the instruction, the question
This is *Get code*, written with week 3's client. Three things to notice: the document goes into the **context** as text (that is all "attaching a file" does); the **system instruction** is card 5; **temperature 0** because a quoted fact is not where randomness belongs.
"""),
code('''
import urllib.request

DOC_URL = "https://niccolosalvini.github.io/ese-ai/week-04/data/bitcoin_whitepaper_text.txt"
try:
    document = urllib.request.urlopen(DOC_URL, timeout=20).read().decode("utf-8")
except Exception as e:
    document = ("Bitcoin: A Peer-to-Peer Electronic Cash System. [...] Once a predetermined number of coins have entered "
                "circulation, the incentive can transition entirely to transaction fees and be completely inflation free.")
    print("[snapshot] could not fetch the whitepaper text; using a short excerpt:", type(e).__name__)
print(len(document.split()), "words in the document")

SYSTEM = """Answer only from the attached documents.
If the answer is not in them, reply exactly: "Not in the documents."
Quote the sentence you used, and name the document."""

def ask(question, system=SYSTEM, temperature=0.0, doc=document):
    """One call: the document and the question in the prompt, the rule in the system message."""
    if MOCK:
        return "[MOCK] Not in the documents."
    r = client.chat.completions.create(
        model=MODEL, temperature=temperature,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": f"DOCUMENT (Bitcoin whitepaper):\\n{doc}\\n\\nQUESTION: {question}"}],
    )
    return r.choices[0].message.content

print(ask("What is the maximum number of bitcoins that will ever exist?"))        # T1: the model knows; the document does not say
print()
print(ask("How big is a block header, and how much storage do headers take per year?"))   # G9
'''),
md("""
**Change one thing and run again:** remove the second line of `SYSTEM` and ask T1 again. Then set `system=""`. Then `temperature=2.0` on G9. One change at a time; write what moved.
"""),
md("""
## A3 — Score the sheet
Export your golden-set sheet as CSV into `week-04/` and point the path at it. Two numbers, not one: retrieval hits and generation hits — and the misses listed by name.
"""),
code('''
import pandas as pd

PATH = "golden_set.csv"          # File ▸ Download ▸ CSV from your sheet; or the template to see the columns
try:
    gs = pd.read_csv(PATH)
except FileNotFoundError:
    gs = pd.read_csv("https://niccolosalvini.github.io/ese-ai/week-04/data/golden_set_template.csv")
    print("[template] no golden_set.csv next to the notebook; showing the empty template")

for col in ["retrieval_hit", "generation_hit"]:
    gs[col] = gs[col].astype(str).str.strip().str.lower().isin(["1", "true", "yes", "y", "x"])

core = gs[gs["id"].str.startswith("G")]
print(f"retrieval hits: {core.retrieval_hit.sum()}/{len(core)}   generation hits: {core.generation_hit.sum()}/{len(core)}")
misses = gs[~gs.generation_hit][["id", "question", "note"]]
print(misses.to_string(index=False) if len(misses) else "no misses recorded — either a perfect run, or an empty sheet")
'''),
md("""
---
**Three lines**, in the sheet, not here: one on the test, one on the two kinds of miss, one on memory.
"""),
]

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python"},
                  "colab": {"name": "week-04 — appendix"}}
out = ROOT / "session.ipynb"
nbf.write(nb, out)
print("wrote", out, len(cells), "cells")
