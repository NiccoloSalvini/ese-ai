"""Builds week-10/session.ipynb with nbformat (same style as build_nbs_weeks1-3.py)."""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

cells = [
md("""
# Week 10 — Implementation and operating model; capstone studio
**ESE · AI for Business and FinTech · Monday 30 November 2026**

Lighter notebook than usual: it is a set of calculators and templates you will reuse in your portfolio, plus one **final checks** cell that inspects your repo before you submit. Everything runs offline — no API key, no network. Replace every `# <-- your number` with the figures from your capstone; the defaults are illustrative.

Cells marked **🔍 CHECK** contain something you must verify before moving on.
"""),
code("""
# Nothing new to install this week; pandas/numpy/matplotlib ship with Colab.
# (Kept so the notebook has the same shape as the others: Runtime ▸ Run all must work from a clean runtime.)
import warnings, numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
pd.set_option("display.width", 140); pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
print("pandas", pd.__version__, "| numpy", np.__version__)
"""),

# ------------------------------------------------------------------ Block B
md("## Block B — From prototype to production, as decisions with numbers"),
md("""
### B1. Build / buy / partner — the week-6 table, now for your capstone
Same scoring table as in week 6 (criteria × weight × option score), but the row labels are now the components of *your* pipeline. Score 1–5 per cell. The weights are yours to defend; the arithmetic is not.
"""),
code("""
criteria = pd.DataFrame({
    "weight": [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
}, index=["time to a working pilot", "control over data and prompts", "cost at target volume",
          "vendor / lock-in risk", "auditability (model risk, AI Act)", "skills you actually have"])
scores = pd.DataFrame({                         # 1 = bad, 5 = good      # <-- your numbers
    "build (own code + API model)": [4, 5, 4, 3, 4, 3],
    "buy (SaaS product)":           [5, 2, 2, 2, 3, 5],
    "partner (vendor builds on your data)": [3, 3, 3, 2, 3, 4],
}, index=criteria.index)

weighted = scores.mul(criteria["weight"], axis=0)
table = pd.concat([criteria, scores], axis=1)
table.loc["WEIGHTED TOTAL"] = [criteria["weight"].sum()] + list(weighted.sum())
table
"""),
md("""
**🔍 CHECK.** Change one weight by 0.10 (take it from another row so they still sum to 1). Does the ranking flip? If a decision flips on a 0.10 weight change, the table is not deciding — *you* are, and the memo should say so and give the real reason.
"""),

md("""
### B2. Cost of inference at scale — the calculator
Price is per **million tokens**, and input and output are priced differently. The numbers below are illustrative tiers (check the provider's page on the day you write the memo; they change every few months). Cached input is what providers charge when the same long prefix (system prompt + retrieved documents) is reused — typically a large discount.
"""),
code("""
# USD per 1M tokens — ILLUSTRATIVE tiers, not a quote. Replace with the provider page the day you decide.
PRICES = pd.DataFrame({
    "input":        [0.10, 1.00, 5.00],
    "cached_input": [0.025, 0.25, 1.25],   # ~75% discount on the cached part of the prompt
    "output":       [0.40, 4.00, 15.00],
}, index=["small", "mid", "frontier"])
PRICES
"""),
md("""
### 🔍 CHECK — the assistant's cost estimate
You asked the assistant: *"estimate the monthly cost of my RAG assistant: ~8,000-token prompt (system + 6 retrieved chunks + question), ~300-token answer, 20,000 queries a month on the frontier model."* It produced the cell below. It runs, it prints a plausible number. **It is wrong by roughly an order of magnitude.** Write your bet for the true monthly cost first, then find the error. Ten minutes; one hint after five.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
tokens_out   = 300
queries_month = 20_000
tier = "frontier"

cost_per_query  = tokens_out / 1e6 * PRICES.loc[tier, "output"]
cost_per_month  = cost_per_query * queries_month
print(f"cost per query: ${cost_per_query:.4f}   |   monthly: ${cost_per_month:,.0f}")
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

The estimate prices **only the output tokens**. In a RAG system the prompt is mostly *input*: system instructions plus retrieved chunks plus the question — here 8,000 tokens against 300 of answer. Input is cheaper per token, but there is 27× more of it. The correct figure is

`cost = tokens_in × price_in + tokens_out × price_out` (all per 1M)

= 8,000/1e6 × 5.00 + 300/1e6 × 15.00 = 0.0400 + 0.0045 = **$0.0445 per query**, i.e. **$890/month**, against the assistant's $90. Off by ~10×, and always in the same direction: the assistant's mental model of "a query" is a chat turn, where input and output are similar in size. Yours is a document pipeline, where input dominates.

Rule for the memo: **any cost figure must show tokens_in and tokens_out separately, with the two prices next to them.** If you cannot see both, the number is not verified.
</details>
"""),
code("""
# Corrected: the calculator you will reuse. Input and output priced separately; caching applied to the cached share of input.
def cost_per_query(tokens_in, tokens_out, tier, cache_hit_rate=0.0, cached_share_of_input=0.0, prices=PRICES):
    \"\"\"USD per query.
    cache_hit_rate       : share of queries whose cached prefix is actually served from cache (0..1)
    cached_share_of_input: share of the input tokens that belong to the reusable prefix (system prompt + fixed context)
    \"\"\"
    p = prices.loc[tier]
    cached_tokens   = tokens_in * cached_share_of_input * cache_hit_rate
    uncached_tokens = tokens_in - cached_tokens
    return (uncached_tokens * p["input"] + cached_tokens * p["cached_input"] + tokens_out * p["output"]) / 1e6

tokens_in, tokens_out, queries_month = 8_000, 300, 20_000        # <-- your numbers (count them with tiktoken on your real prompt)
for tier in PRICES.index:
    cq = cost_per_query(tokens_in, tokens_out, tier)
    print(f"{tier:9s}: ${cq:.4f} per query  |  ${cq*queries_month:,.0f} per month  "
          f"(input share of cost: {tokens_in/1e6*PRICES.loc[tier,'input']/cq:.0%})")
"""),
md("""
### B3. Sensitivity: volume × model tier, with and without caching
A sensitivity table is the honest form of a cost estimate: it shows the reader where the number breaks. Two tables — no caching, then with a realistic cache (say 60% of the prompt is a fixed prefix, served from cache 80% of the time).
"""),
code("""
volumes = [1_000, 5_000, 20_000, 100_000, 500_000]         # queries per month
def monthly_table(**kw):
    return pd.DataFrame({tier: [cost_per_query(tokens_in, tokens_out, tier, **kw) * v for v in volumes]
                         for tier in PRICES.index}, index=pd.Index(volumes, name="queries/month")).round(0)

print("Monthly cost (USD), no caching")
display(monthly_table())
print("\\nMonthly cost (USD), 60% of prompt is a cacheable prefix, hit rate 80%")
display(monthly_table(cache_hit_rate=0.8, cached_share_of_input=0.6))
"""),
md("""
### B4. Routing and the break-even value per query
Two decisions hide in every cost line. **Routing**: send the easy queries to the small model and only the hard ones to the frontier one — the cost is a weighted average, the quality is whatever your evals from week 5 say it is. **Break-even**: a query is worth running only if the value it creates exceeds its cost; below the break-even value per query, the system loses money on every call however good it is.

Before running: **write your bet** — at what monthly volume does the frontier model, with no routing, exceed a $2,000/month budget?
"""),
code("""
BUDGET_PER_MONTH = 2_000.0                                  # <-- your number
VALUE_PER_QUERY  = 0.05                                     # <-- your number: what one answered query is worth (time saved × hourly cost, or revenue)

grid = np.logspace(3, 6, 200)                              # 1k .. 1M queries/month
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# left: monthly cost vs volume by tier + a routed mix
routed = lambda v: v * (0.8 * cost_per_query(tokens_in, tokens_out, "small") + 0.2 * cost_per_query(tokens_in, tokens_out, "frontier"))
for tier in PRICES.index:
    ax[0].plot(grid, [cost_per_query(tokens_in, tokens_out, tier) * v for v in grid], label=tier)
ax[0].plot(grid, [routed(v) for v in grid], "--", label="routed 80% small / 20% frontier")
ax[0].axhline(BUDGET_PER_MONTH, color="k", lw=0.8); ax[0].text(1_100, BUDGET_PER_MONTH * 1.15, "budget")
ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("queries / month"); ax[0].set_ylabel("USD / month")
ax[0].set_title("Monthly cost by tier"); ax[0].legend(fontsize=8)

# right: value minus cost per query by tier (break-even = where the bar crosses zero)
margin = pd.Series({t: VALUE_PER_QUERY - cost_per_query(tokens_in, tokens_out, t) for t in PRICES.index})
margin.plot.bar(ax=ax[1], color=["#4c9a2a" if m > 0 else "#c0392b" for m in margin])
ax[1].axhline(0, color="k", lw=0.8); ax[1].set_title(f"Value per query ({VALUE_PER_QUERY:.2f}) minus cost, by tier"); ax[1].set_ylabel("USD / query")
plt.tight_layout(); plt.show()

for tier in PRICES.index:
    be_volume = BUDGET_PER_MONTH / cost_per_query(tokens_in, tokens_out, tier)
    print(f"{tier:9s}: budget exhausted at {be_volume:>10,.0f} queries/month | break-even value per query = ${cost_per_query(tokens_in, tokens_out, tier):.4f}")
print(f"routed   : budget exhausted at {BUDGET_PER_MONTH / (routed(1)):>10,.0f} queries/month")
"""),
md("""
**🔍 CHECK.** Compare the frontier break-even volume with your bet. Then ask the question the chart cannot answer: *is the frontier model actually better on your golden set from week 5?* If the routed mix scores within your tolerance on the evals, the cost line is the decision. If you have no evals, you cannot route — you can only guess.
"""),

md("""
### B5. Latency budget
Users notice latency before they notice quality. Sum the stages; compare with the target for your use case (a chat assistant tolerates ~5 s; a check inside a payment flow tolerates ~300 ms). Generation time is `tokens_out / tokens_per_second`, and it is usually the biggest line.
"""),
code("""
latency = pd.DataFrame({
    "ms": [40, 120, 350, 700, 300 / 60 * 1000, 30],       # <-- your numbers; generation = tokens_out / tokens_per_s * 1000
}, index=["network + auth", "embed the query", "vector search (top-6)", "time to first token (frontier)",
          "generate 300 tokens at 60 tok/s", "post-processing / guardrail"])
latency["cumulative_ms"] = latency["ms"].cumsum()
TARGET_MS = 5_000                                           # <-- your number
display(latency.round(0))
total = latency["ms"].sum()
print(f"total ≈ {total:,.0f} ms vs target {TARGET_MS:,} ms → {'OK' if total <= TARGET_MS else 'OVER BUDGET'}; "
      f"generation is {latency.loc['generate 300 tokens at 60 tok/s','ms']/total:.0%} of the total")
"""),
md("""
**🔍 CHECK.** Halve `tokens_out` (shorter answers, or a structured answer instead of prose). What happens to latency *and* to cost per query at the same time? This is the one lever that improves both — write it in the roadmap.
"""),

# ------------------------------------------------------------------ Block C
md("## Block C — Readiness, roles, roadmap"),
md("""
### C1. Data and technology readiness checklist — as a scored dataframe
Score each item 0 (absent), 1 (partial), 2 (in place) for *your* capstone. The weighted score is not a grade; it is a map of where the pilot will break first. Anything scored 0 with weight ≥ 2 goes into the roadmap as a gate.
"""),
code("""
readiness = pd.DataFrame([
    # area, item, weight (1-3), score (0-2)                                            # <-- your scores
    ("data",       "source of truth identified and access agreed",                     3, 2),
    ("data",       "dated snapshot in repo; refresh procedure written",                2, 2),
    ("data",       "known quality issues listed (missing, units, calendars)",          2, 1),
    ("data",       "personal / confidential data classified; nothing leaves the perimeter", 3, 1),
    ("technology", "notebook restart-and-run-all passes from a clean runtime",         3, 2),
    ("technology", "LLM calls go through one wrapper; provider can be swapped",       2, 2),
    ("technology", "golden set + regression eval exists and runs",                    3, 1),
    ("technology", "logging of prompts, outputs, cost per call",                      2, 0),
    ("technology", "fallback when the API fails (cache, mock, human)",                2, 1),
    ("people",     "an owner who can read the code and the evals",                    3, 1),
    ("people",     "a validator independent of the builder",                          2, 0),
    ("governance", "kill-switch: who can turn it off, and how fast",                  3, 0),
    ("governance", "model-risk / AI Act classification written (week 4, 7, 9)",       2, 1),
], columns=["area", "item", "weight", "score"])
readiness["weighted"] = readiness["weight"] * readiness["score"]
readiness["max"] = readiness["weight"] * 2

by_area = readiness.groupby("area")[["weighted", "max"]].sum()
by_area["readiness_%"] = (by_area["weighted"] / by_area["max"] * 100).round(0)
display(by_area)
print(f"overall readiness: {readiness['weighted'].sum() / readiness['max'].sum():.0%}")
print("\\nGATES (weight ≥ 2 and score 0):")
display(readiness.query("weight >= 2 and score == 0")[["area", "item"]])
"""),
md("""
### C2. Roles and governance — who owns the model, who validates, who can switch it off
One table. Names, not departments. If two cells have the same name in the *owner* and *validator* rows, you do not have validation.
"""),
code("""
roles = pd.DataFrame({
    "role":        ["model owner", "independent validator", "data owner", "kill-switch holder", "user representative", "compliance / model risk"],
    "who (name)":  ["you", "?", "?", "?", "?", "?"],                                    # <-- your names
    "decides":     ["prompt, model, threshold changes", "sign-off before each gate", "access, refresh, retention",
                    "stop the system; rollback", "acceptance criteria, KPI", "classification, documentation, review cadence"],
    "evidence":    ["changelog in repo", "eval report per release", "data sheet + snapshot dates",
                    "runbook: stop in < 1 hour, tested", "signed-off golden set", "canvas (week 9) kept current"],
})
roles
"""),
md("""
### C3. Pilot → production roadmap — the template, rendered as a table
Three gates, 30/60/90 days. A gate is a *criterion that can fail*, with a KPI that shows whether it passed and a rollback that says what happens if it did not. "Continue to phase 2" is not a gate.
"""),
code("""
roadmap = pd.DataFrame({
    "phase":         ["0–30 days · pilot (shadow)",          "30–60 days · limited production",                 "60–90 days · production"],
    "scope":         ["internal users, outputs not acted on", "one team, human approves every output",            "all target users, human samples 5%"],
    "gate criteria": ["eval ≥ baseline on golden set; cost/query ≤ budget; no P1 red-team finding open",
                      "user acceptance ≥ 70%; latency p95 ≤ target; drift monitor running",
                      "30 days without a kill-switch event; validator sign-off; documentation complete"],
    "KPI":           ["accuracy vs golden set; $/query",      "% outputs accepted unchanged; p95 latency",         "cost per outcome vs baseline process; incidents/month"],
    "rollback":      ["stop the pilot; nothing to undo",      "return to shadow mode; owner + validator review",   "kill-switch; previous process resumes within 1 h"],
    "owner":         ["you", "you + validator", "kill-switch holder"],                                            # <-- your names
}).set_index("phase")
pd.set_option("display.max_colwidth", 80)
roadmap.T
"""),
md("""
**🔍 CHECK.** For each gate criterion, point to the cell in your capstone notebook that would produce the number. If there is no cell, the gate is a wish — either add the cell to the roadmap as a deliverable or remove the criterion.
"""),

# ------------------------------------------------------------------ Block D
md("## Block D — Studio: final checks on your repo"),
md("""
This cell inspects a repo folder and reports the mechanical part of the review checklist in `notes.md`. In Colab, mount Drive or clone your repo first, then set `REPO_ROOT` to the `capstone/` folder. If the path does not exist it falls back to the current directory so the cell always runs. It does not judge content — that is the review pass with the tutor.
"""),
code("""
import os, re, json
from pathlib import Path

REPO_ROOT = Path("capstone")                                  # <-- your path, e.g. Path("/content/ese-ai-fintech/capstone")
if not REPO_ROOT.exists():
    print(f"[warn] {REPO_ROOT} not found — inspecting the current directory instead ({Path.cwd()})")
    REPO_ROOT = Path(".")

files = [p for p in REPO_ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and ".ipynb_checkpoints" not in p.parts]
print(f"{len(files)} files under {REPO_ROOT.resolve()}\\n")
for p in sorted(files)[:60]:
    print(f"  {p.relative_to(REPO_ROOT)}  ({p.stat().st_size/1024:,.0f} KB)")

def nb_stats(path):
    \"\"\"(code cells, cells with error outputs, has 'Take-home' cell) for one notebook.\"\"\"
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    n_code = sum(c["cell_type"] == "code" for c in cells)
    n_err = sum(any(o.get("output_type") == "error" for o in c.get("outputs", [])) for c in cells if c["cell_type"] == "code")
    take_home = any("take-home" in "".join(c.get("source", "")).lower() for c in cells)
    return n_code, n_err, take_home

notebooks = [p for p in files if p.suffix == ".ipynb"]
snapshots = [p for p in files if p.suffix == ".csv" and "data" in p.parts]
dated     = [p for p in snapshots if re.search(r"20\\d{2}[-_]?\\d{2}[-_]?\\d{2}", p.name)]
mds       = {p.name.lower() for p in files if p.suffix == ".md"}

checks = pd.DataFrame([
    ("at least one notebook",                   len(notebooks) >= 1,                 f"{len(notebooks)} notebook(s)"),
    ("no error outputs saved in notebooks",     all(nb_stats(p)[1] == 0 for p in notebooks) if notebooks else False,
                                                "; ".join(f"{p.name}: {nb_stats(p)[0]} code cells, {nb_stats(p)[1]} errors" for p in notebooks) or "—"),
    ("data snapshot present in data/",          len(snapshots) >= 1,                 f"{len(snapshots)} csv in data/"),
    ("snapshot file name carries a date",       len(dated) >= 1,                     ", ".join(p.name for p in dated[:3]) or "none dated"),
    ("memo.md present",                         "memo.md" in mds,                    ""),
    ("canvas.md present",                       "canvas.md" in mds,                  ""),
    ("roadmap.md present",                      "roadmap.md" in mds,                 ""),
    ("README.md present",                       "readme.md" in mds,                  ""),
    ("take-home cell in a notebook",            any(nb_stats(p)[2] for p in notebooks), ""),
], columns=["check", "pass", "detail"])
checks["pass"] = checks["pass"].map({True: "PASS", False: "FAIL"})
pd.set_option("display.max_colwidth", 90)
display(checks)
print(f"\\n{(checks['pass']=='PASS').sum()}/{len(checks)} mechanical checks pass. "
      "'PASS' here means the file exists — the review checklist in notes.md decides whether it is good.")
"""),
md("""
**🔍 CHECK.** Every FAIL is a line in your to-do for this week. Two of them are not mechanical and this cell cannot see them: *restart-and-run-all from a clean runtime* (do it now, on the projector) and *time-ordered evaluation with the baseline stated next to it* (open the cell and read it aloud).
"""),

md("""
## Take-home (write three lines)
Three lines, in your own words, at the bottom of this notebook — this week for the **whole course**, not only this session. Then commit (`File ▸ Save a copy in GitHub`, path `week-10/session.ipynb`).

1.
2.
3.

**Homework brief** → see `week-10/homework.md` — the portfolio (60%), due Sunday 6 December 23:59.
"""),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["colab"] = {"provenance": [], "name": "week-10_session.ipynb"}
out = ROOT / "session.ipynb"
nbf.write(nb, out); print("wrote", out)
