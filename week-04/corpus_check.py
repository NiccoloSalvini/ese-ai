"""Helper used while writing build_nb.py: checks where 500-char boundaries fall in the fixed demo document."""
import re, sys
sys.path.insert(0, "/root/work/course/week-04")
from build_nb import SYNTHETIC_CORPUS

doc = SYNTHETIC_CORPUS["Nordwind Digital Assets, Inc. — 10-K FY2025, Item 1A (SYNTHETIC)"]
print("len", len(doc))
for pat in [r"\$1,250 million", r"11 hours", r"2\.3 million"]:
    m = re.search(pat, doc)
    print(pat, "at", m.start(), "-", m.end(), "| boundaries nearby:", [b for b in range(0, len(doc), 500) if abs(b - m.start()) < 120])
