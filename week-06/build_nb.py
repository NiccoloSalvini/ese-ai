"""Builds week-06 session notebook with nbformat. Run: python build_nb.py"""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

UTILS = r'''
# --- course helper: price loader with fallbacks (run this cell once per session) ---
import warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")

def load_prices(tickers, start="2022-01-01", end=None, cache_dir="data"):
    """Daily close prices, one column per ticker.
    1) try yfinance (live)  2) try a CSV snapshot in data/  3) synthetic random walk (pipeline test only)."""
    import os
    os.makedirs(cache_dir, exist_ok=True)
    key = "_".join(t.replace("^", "") for t in tickers)
    snap = os.path.join(cache_dir, f"prices_{key}.csv")
    try:
        import yfinance as yf
        raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
        px = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].rename(columns={"Close": tickers[0]})
        px = px.dropna(how="all")
        if len(px) < 50:
            raise RuntimeError("empty download")
        px.to_csv(snap)
        print(f"[live] {px.shape[0]} rows from yfinance; snapshot saved to {snap}")
        return px
    except Exception as e:
        print(f"[warn] yfinance failed ({type(e).__name__}); trying snapshot")
    if os.path.exists(snap):
        px = pd.read_csv(snap, index_col=0, parse_dates=True)
        print(f"[snapshot] {px.shape[0]} rows from {snap}")
        return px
    print("[SYNTHETIC] no network and no snapshot: generating a random walk. Numbers below are NOT real.")
    rng = np.random.default_rng(0)
    idx = pd.bdate_range(start, end or pd.Timestamp.today().normalize())
    px = pd.DataFrame({t: 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.02 if "USD" in t else 0.011, len(idx))))
                       for t in tickers}, index=idx)
    return px
'''

LLM = r'''
# --- course helper: one LLM wrapper, guarded. Works with Gemini if GEMINI_API_KEY is in Colab Secrets; otherwise a deterministic MOCK. ---
import os, json
API_KEY = None
try:
    from google.colab import userdata
    API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    API_KEY = os.environ.get("GEMINI_API_KEY")

def _mock(prompt, json_schema):
    """Deterministic stand-in so the notebook runs end-to-end without a key. Outputs are labelled [MOCK]."""
    if json_schema and "candidates" in json.dumps(json_schema):
        return {"candidates": [
            {"question": "Does a volatility-regime signal on BTC, hedged with a cost model, beat buy-and-hold on risk-adjusted terms 2020-2026?",
             "data": "BTC-USD daily (yfinance), FRED DGS10, blockchain.com active addresses", "method": "week-3 classifier + week-7 walk-forward backtest with costs",
             "deliverable": "notebook pipeline + memo with cost-weighted KPI", "risk": "signal too weak after costs; result is a well-evidenced negative"},
            {"question": "Which DeFi lending protocol offered the best risk-adjusted stablecoin yield 2023-2026, net of exploits and depegs?",
             "data": "DefiLlama yields and TVL API, CoinGecko prices, DeFi exploit list", "method": "week-8 protocol analysis + week-3 evaluation discipline",
             "deliverable": "ranked table with drawdown-adjusted yield + memo", "risk": "API history incomplete; yields survivorship-biased (dead pools vanish)"},
            {"question": "Can an LLM-extracted 'risk tone' score from 10-K risk sections add anything to a volatility forecast for 10 US stocks?",
             "data": "SEC EDGAR 10-K filings, yfinance prices", "method": "week-4 RAG/extraction + week-7 honest test of an LLM feature",
             "deliverable": "feature pipeline, walk-forward test, memo", "risk": "filings yearly: few observations; LLM cost at scale"},
        ]}
    if "adverse action" in prompt.lower() or "reason" in prompt.lower():
        return ("[MOCK] Your application was declined mainly because your monthly debt payments are high relative to income, "
                "and your credit history is short. Reducing outstanding debt or building a longer repayment record would improve the outcome. "
                "You have the right to ask for a human review of this decision.")
    return "[MOCK] no API key — deterministic placeholder answer."

def llm(prompt, system=None, json_schema=None, temperature=0):
    """Single entry point for every LLM call in the course. Returns text, or a dict when json_schema is given."""
    if not API_KEY:
        return _mock(prompt, json_schema)
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=API_KEY)
    cfg = dict(temperature=temperature)
    if system: cfg["system_instruction"] = system
    if json_schema: cfg.update(response_mime_type="application/json", response_schema=json_schema)
    r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=types.GenerateContentConfig(**cfg))
    return json.loads(r.text) if json_schema else r.text

print("LLM mode:", "Gemini (live)" if API_KEY else "MOCK (no key found — outputs are placeholders)")
'''

cells = [
md("""
# Week 6 — Where AI earns money in fintech; capstone scoping
**ESE · AI for Business and FinTech · 2 November 2026**

Three parts. First hour: your minor case presentation (nothing to run). Then a lab through three fintech decisions where models make or lose money — fraud, credit, build/buy/partner — each with a small dataset you generate here. Last part: scope your capstone and prove its data exists.

**Why the datasets are synthetic today.** There is no public, labelled fraud or loan dataset with realistic structure (0.5% fraud, real customer behaviour, demographic proxies) that fits in a session and that we could lawfully use. So we generate them with a fixed seed: the *structure* is realistic, the *numbers* are not evidence about any real bank. Every conclusion today is about the method, not the world. Your capstone must use real data — that is what the last block is for.
"""),
code("!pip -q install yfinance google-genai"),
code(UTILS),
code(LLM),

# ------------------------------------------------------------------ Block B: fraud
md("## Block B — Fraud detection: why accuracy is useless here"),
md("""
A card issuer sees ~100,000 transactions a day. About 0.5% are fraudulent. A model scores each transaction; above a threshold, the transaction is blocked and the customer gets a text message. Two errors, two very different costs: a **missed fraud** costs the amount (the issuer refunds the customer); a **blocked good customer** costs a call-centre contact, a failed purchase, and some probability the customer moves their card to a competitor.

We generate the transactions with a seed. Fraud looks different from normal traffic in ways that real fraud does: larger amounts, night hours, foreign merchants, new devices, bursts of activity.
"""),
code("""
rng = np.random.default_rng(6)
N, FRAUD_RATE = 40_000, 0.005
is_fraud = rng.random(N) < FRAUD_RATE

tx = pd.DataFrame({
    "amount":        np.exp(rng.normal(np.where(is_fraud, 5.3, 3.8), np.where(is_fraud, 1.0, 0.9))).round(2),
    "hour":          np.where(is_fraud, rng.choice(24, N, p=np.r_[np.full(6, 0.10), np.full(18, 0.4/18)]), rng.choice(24, N, p=np.r_[np.full(6, 0.02), np.full(18, 0.88/18)])),
    "foreign":       (rng.random(N) < np.where(is_fraud, 0.55, 0.08)).astype(int),
    "new_device":    (rng.random(N) < np.where(is_fraud, 0.60, 0.10)).astype(int),
    "tx_last_24h":   rng.poisson(np.where(is_fraud, 6, 2)),
    "merchant_risk": rng.beta(np.where(is_fraud, 4, 2), np.where(is_fraud, 2, 6)).round(3),
    "is_fraud":      is_fraud.astype(int),
})
print(tx.shape, "| fraud rate: %.4f  (%d fraud cases)" % (tx.is_fraud.mean(), tx.is_fraud.sum()))
tx.groupby("is_fraud").mean().round(2).T
"""),
md("""
**Bet 1 (write it down first):** a rule that *never flags anything* — what accuracy does it score on this data? A number, before running.
"""),
code("""
never_flag = np.zeros(len(tx), dtype=int)
print("accuracy of 'never flag': %.4f" % (never_flag == tx.is_fraud).mean())
print("frauds caught by 'never flag':", ((never_flag == 1) & (tx.is_fraud == 1)).sum())
"""),
md("""
### 🔍 CHECK — the assistant's fraud model
Asked to "train a fraud model and evaluate it", the assistant produced the cell below. It runs. It reports an excellent number. **There are two problems in it** — find both before opening the solution. Ten minutes; the second hint comes only after you have found one.

**Bet 2 (before running):** the assistant holds out 400 random transactions for testing. How many fraud cases will be in that test set?
""" ),
code("""
# --- as produced by the assistant (do not trust) ---
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

features = ["amount", "hour", "foreign", "new_device", "tx_last_24h", "merchant_risk"]
X, y = tx[features], tx["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=400, random_state=7)   # hold out a small test set for a quick check
clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
acc = accuracy_score(y_test, clf.predict(X_test))
print(f"Test accuracy: {acc:.3%} — excellent, the model is ready for production.")
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **Accuracy on a 0.5%-fraud dataset is meaningless.** "Never flag" scores 99.5% (Bet 1). The assistant's 99.5–99.8% is the majority baseline wearing a suit. The number that matters is how many frauds the model catches (recall) at how many good customers blocked (false positives), at a threshold chosen on costs — exactly the week-3 logic, with a much worse imbalance.
2. **The split stratifies by nothing and the test set is tiny.** 400 random rows at 0.5% contain about 2 fraud cases (Bet 2; run `y_test.sum()`). Any recall you compute is 0/2, 1/2 or 2/2. No model can be evaluated on two positives. Fix: `stratify=y` and a test set large enough to hold at least ~50 positives — here 30% gives ~60.

Both errors are silent: no warning, a green checkmark, a confident sentence. This is the most common shape of an assistant error in classification: the code is right, the *evaluation design* is wrong.
</details>
"""),
code("""
print("fraud cases in the assistant's test set:", int(y_test.sum()), "of", len(y_test))
print("majority baseline on that test set: %.3f" % (1 - y_test.mean()))
"""),
code("""
# Corrected: stratified split, enough positives, and the metrics that price the errors
from sklearn.metrics import precision_score, recall_score, roc_auc_score, confusion_matrix

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=7, stratify=y)
clf = LogisticRegression(max_iter=2000).fit(X_train, y_train)
p = clf.predict_proba(X_test)[:, 1]
print("test rows:", len(y_test), "| fraud cases in test:", int(y_test.sum()))
print("AUC: %.3f  (ranking quality — the model does separate fraud from normal)" % roc_auc_score(y_test, p))

cm = confusion_matrix(y_test, p > 0.5)
pd.DataFrame(cm, index=["actual normal", "actual fraud"], columns=["predicted normal", "predicted fraud"])
"""),
md("""
At the default threshold of 0.5 the model flags almost nothing — with 0.5% positives, few transactions ever reach a 50% probability. The threshold must come from costs, not from 0.5. Below: the trade-off between fraud caught and good customers blocked, scaled to **100,000 transactions per day**.

**Bet 3 (before running):** if we accept a 1% false-positive rate, how many *good customers per day* get blocked at 100k transactions/day?
"""),
code("""
DAILY_TX, COST_FP, COST_FN = 100_000, 15.0, None   # COST_FP: one blocked good customer (contact + churn risk, EUR). COST_FN: the fraud amount itself.
amt_test = tx.loc[X_test.index, "amount"]

rows = []
for thr in [0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02, 0.01, 0.005]:
    flag = p > thr
    fp = (flag & (y_test == 0)); fn = (~flag & (y_test == 1))
    fpr = fp.sum() / (y_test == 0).sum()
    rec = recall_score(y_test, flag); prec = precision_score(y_test, flag, zero_division=0)
    # scale to one day of traffic
    good_blocked_per_day = DAILY_TX * (1 - FRAUD_RATE) * fpr
    fraud_missed_eur_per_day = DAILY_TX * FRAUD_RATE * (1 - rec) * amt_test[y_test == 1].mean()
    cost_per_day = good_blocked_per_day * COST_FP + fraud_missed_eur_per_day
    rows.append([thr, rec, prec, fpr, good_blocked_per_day, fraud_missed_eur_per_day, cost_per_day])

thr_tab = pd.DataFrame(rows, columns=["threshold", "recall", "precision", "FPR", "good customers blocked/day", "fraud missed EUR/day", "total cost EUR/day"]).round(3)
print("cost of 'never flag' per day: EUR %.0f" % (DAILY_TX * FRAUD_RATE * amt_test[y_test == 1].mean()))
thr_tab
"""),
code("""
# The row closest to FPR = 1%: this is the answer to Bet 3
row = thr_tab.iloc[(thr_tab["FPR"] - 0.01).abs().argmin()]
print("at threshold %.3f: FPR %.3f -> %.0f good customers blocked per day, recall %.2f" % (row.threshold, row.FPR, row["good customers blocked/day"], row.recall))
print("arithmetic check: 100,000 × 0.995 × 0.01 =", 100_000 * 0.995 * 0.01)
"""),
md("""
Read the table as a manager, not as a data scientist: the threshold that minimises cost per day depends on `COST_FP`. At €15 per blocked customer the optimum sits at a low threshold; if churn is expensive (a premium card) and `COST_FP` is €60, the optimum moves. **Change `COST_FP` and re-run.** The model did not change; the business decision did. This table — not accuracy, not even AUC — is what goes to the fraud committee.
"""),

# ------------------------------------------------------------------ Block B: credit
md("## Block B — Credit scoring: the decision must be explainable, and the fairness check"),
md("""
A lender scores applicants for a personal loan. Unlike fraud, here (a) the applicant has a **right to know why** they were rejected, and (b) a regulator will ask whether the model treats groups differently. We use logistic regression on purpose: its coefficients *are* the explanation. Gradient boosting will need SHAP for the same job — week 9.

Synthetic again: two regions A and B. Region B applicants have on average lower income and shorter credit history. The **region itself does not affect repayment** in the generator — only the financial features do. Keep that in mind for Bet 5.
"""),
code("""
rng = np.random.default_rng(66)
n = 6_000
region = rng.choice(["A", "B"], n, p=[0.7, 0.3]); B = region == "B"

loans = pd.DataFrame({
    "region":         region,
    "income":         np.exp(rng.normal(np.where(B, 10.2, 10.6), 0.45)).round(0),      # EUR / year
    "dti":            np.clip(rng.normal(0.32, 0.12, n), 0.02, 0.90).round(3),        # debt payments / income
    "history_years":  np.clip(rng.normal(np.where(B, 5, 9), 4), 0, 30).round(1),
    "late_payments":  rng.poisson(np.where(B, 0.9, 0.6)),
    "employment_yrs": np.clip(rng.normal(np.where(B, 4, 7), 3), 0, 35).round(1),
})
logit = (-2.2 + 3.5 * loans.dti - 0.08 * loans.history_years + 0.6 * loans.late_payments
         - 0.5 * (np.log(loans.income) - 10.5) - 0.04 * loans.employment_yrs)          # region is NOT here
loans["default"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
print(loans.shape, "| default rate: %.3f" % loans.default.mean())
loans.groupby("region")[["income", "dti", "history_years", "late_payments", "employment_yrs", "default"]].mean().round(2)
"""),
code("""
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

credit_features = ["income", "dti", "history_years", "late_payments", "employment_yrs"]
Xc, yc = loans[credit_features], loans["default"]
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, test_size=0.3, random_state=0, stratify=yc)

scorer = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xc_tr, yc_tr)
p_default = pd.Series(scorer.predict_proba(Xc_te)[:, 1], index=Xc_te.index)
print("AUC on test: %.3f | base default rate: %.3f" % (roc_auc_score(yc_te, p_default), yc_te.mean()))

coefs = pd.Series(scorer[-1].coef_[0], index=credit_features).round(3)
print("\\ncoefficients on standardised features (positive = raises probability of default):"); print(coefs.sort_values())
"""),
md("""
**Policy:** approve if predicted default probability < 20%. The threshold is a business choice (loss rate the lender tolerates given the interest margin) — same logic as the fraud table, and you can move it.

**Explaining one rejection.** For a logistic model, the log-odds of default is a *sum* of `coefficient × standardised feature`. The largest positive terms are the reasons. This is the "adverse action" reason list the applicant is entitled to.
"""),
code("""
THR_APPROVE = 0.20
approved = p_default < THR_APPROVE
print("approval rate on test set: %.3f" % approved.mean())

# pick one rejected applicant and decompose the decision
rejected_idx = p_default[~approved].sort_values().index[len(p_default[~approved]) // 2]   # a median rejection, not an extreme one
z = pd.Series(scorer[0].transform(Xc_te.loc[[rejected_idx]])[0], index=credit_features)
contrib = (z * coefs).round(3)
explain = pd.DataFrame({"applicant value": Xc_te.loc[rejected_idx], "z-score": z.round(2), "coef": coefs, "contribution to log-odds": contrib}).sort_values("contribution to log-odds", ascending=False)
print("applicant", rejected_idx, "| region", loans.loc[rejected_idx, "region"], "| p(default) = %.3f  -> REJECTED" % p_default[rejected_idx])
explain
"""),
code("""
# From contributions to a sentence the applicant can act on. (Gemini if a key is set; MOCK otherwise.)
top = explain[explain["contribution to log-odds"] > 0].head(2)
reasons = "; ".join(f"{f} = {explain.loc[f, 'applicant value']} (pushes toward rejection by {explain.loc[f, 'contribution to log-odds']:+.2f} log-odds)" for f in top.index)
notice = llm(
    f"Write a 3-sentence adverse action notice for a declined personal loan. Plain English, no jargon, no apology, no legal threats. "
    f"Principal reasons, in order: {reasons}. End by stating the right to request a human review.",
    system="You write customer communications for a regulated EU lender.")
print(notice)
"""),
md("""
**🔍 CHECK.** Is the sentence *true to the model*? Compare it with the contribution table: does it name the two largest positive contributions, and nothing the model did not use? An explanation that is more persuasive than the model is a compliance problem, not a feature.

**Bet 4 (before running):** the model does not see `region`. Will the approval rate differ between A and B? Same, or a gap — and if a gap, how many percentage points?
"""),
code("""
fair = pd.DataFrame({
    "approval rate": approved.groupby(loans.loc[Xc_te.index, "region"]).mean(),
    "actual default rate (all applicants)": yc_te.groupby(loans.loc[Xc_te.index, "region"]).mean(),
    "default rate among approved": yc_te[approved].groupby(loans.loc[Xc_te.index[approved], "region"]).mean(),
    "n": Xc_te.groupby(loans.loc[Xc_te.index, "region"]).size(),
}).round(3)
gap = fair.loc["A", "approval rate"] - fair.loc["B", "approval rate"]
print("approval-rate gap A − B: %.1f percentage points" % (100 * gap))
fair
"""),
md("""
**Bet 5 (before running):** an assistant suggests "remove any proxy for region from the features to make it fair". Here region is *already absent*. Suppose instead we drop the two features most correlated with region (`income`, `history_years`). Does the gap close? Bigger, smaller, same?
"""),
code("""
corr_with_B = loans[credit_features].corrwith(pd.Series(B.astype(int), index=loans.index)).round(3)
print("correlation of each feature with region B:"); print(corr_with_B.sort_values())

reduced = [f for f in credit_features if f not in ("income", "history_years")]
scorer2 = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xc_tr[reduced], yc_tr)
p2 = pd.Series(scorer2.predict_proba(Xc_te[reduced])[:, 1], index=Xc_te.index)
appr2 = p2 < THR_APPROVE
rate2 = appr2.groupby(loans.loc[Xc_te.index, "region"]).mean()
print("\\nreduced model — AUC %.3f (was %.3f)" % (roc_auc_score(yc_te, p2), roc_auc_score(yc_te, p_default)))
print("approval rate A %.3f, B %.3f -> gap %.1f pp (was %.1f pp)" % (rate2["A"], rate2["B"], 100 * (rate2["A"] - rate2["B"]), 100 * gap))
"""),
md("""
Three things to read from the two tables:
1. **A gap appears without the group variable.** Features carry the group. Removing the variable is not a fairness control; it is cosmetics.
2. **Dropping correlated features shrinks the gap and the AUC together.** Fairness by feature removal is paid for in accuracy, and the remaining features (`late_payments`, `dti`) also correlate with the group. There is no feature set that makes the gap vanish here — because the *base default rates differ* (second column).
3. **"Default rate among approved" is close across groups.** The model is roughly *calibrated by group*: a B applicant approved at p<20% defaults about as often as an A applicant. That is one legitimate definition of fairness. Equal approval rates is another. They contradict each other whenever base rates differ — this is a theorem, not an opinion. The lender has to choose, write the choice down, and be ready to defend it to a regulator. That written choice is what week 9's risk and controls canvas asks for.
"""),

# ------------------------------------------------------------------ Block B: build/buy/partner
md("## Block B — Build, buy, or partner: a scoring table you will reuse in week 10"),
md("""
The fraud model above would take a bank team six months to build well and would still lack the cross-bank signals a vendor sees (a device seen in fraud at another issuer). Credit scoring is closer to core: the bank owns the data, is accountable to the regulator for every rejection, and cannot outsource the explanation. The decision is not technical; it is a weighted table — and the weights are the argument. Edit them.
"""),
code("""
criteria = {                     # weight 1–5: how much this matters for THIS decision
    "time to value (months, lower better)": 3,
    "control over model & data":            4,
    "explainability to regulator":          5,
    "cost year 1 (EUR k, lower better)":    2,
    "cost year 3 cumulative (lower better)":3,
    "cross-institution signal":             3,
    "vendor lock-in risk (lower better)":   2,
}
# raw scores 1–5 for each option (5 = best on that criterion). Scores are illustrative; the exercise is arguing them.
options = pd.DataFrame({
    "build in-house":       [1, 5, 5, 2, 3, 1, 5],
    "buy vendor score":     [5, 1, 2, 4, 2, 5, 1],
    "partner (co-develop)": [3, 3, 4, 3, 4, 3, 3],
}, index=list(criteria))

w = pd.Series(criteria)
scores = options.mul(w, axis=0).sum() / w.sum()
print("weighted score (out of 5):"); print(scores.round(2).sort_values(ascending=False))
print("\\nsensitivity: if 'explainability to regulator' weight goes to 1 →")
w2 = w.copy(); w2["explainability to regulator"] = 1
print((options.mul(w2, axis=0).sum() / w2.sum()).round(2).sort_values(ascending=False))
"""),
md("""
**🔍 CHECK.** Re-score the *fraud* decision instead of the credit one: which weights change, and does the winner flip? Write the one criterion that decided it. That sentence is the executive summary of a build/buy memo; everything else is appendix.
"""),

# ------------------------------------------------------------------ Block C: capstone
md("## Block C — Capstone scoping workshop"),
md("""
Four weeks of building remain (7–10), one weekend each. The capstone is 60% of the mark and is assessed on: technical execution and reproducibility; validity of method (no leakage, honest backtest/eval); financial-domain reasoning; product framing and roadmap; communication.

Every candidate topic is written in the same template so they can be compared. The LLM proposes three from your interests; you edit them until they are yours — a generated candidate is a starting point, never a proposal.
"""),
code("""
CANDIDATE_SCHEMA = {
    "type": "object",
    "properties": {"candidates": {"type": "array", "minItems": 3, "maxItems": 3, "items": {
        "type": "object",
        "properties": {k: {"type": "string"} for k in ["question", "data", "method", "deliverable", "risk"]},
        "required": ["question", "data", "method", "deliverable", "risk"]}}},
    "required": ["candidates"],
}
interests = "stock trading, crypto and DeFi, AI for product and investment decisions; experience in startup scouting and BI/KPI work"
toolkit = "pandas, logistic regression and gradient boosting with time-ordered validation, threshold on costs, RAG and structured extraction with an LLM, agents with tools and evals, walk-forward backtest with costs (week 7), AMM/lending simulation with DefiLlama/CoinGecko data (week 8), SHAP and a risk canvas (week 9)"
out = llm(
    f"Propose exactly three capstone topics for a 4-week, one-person project. Interests: {interests}. Toolkit available: {toolkit}. "
    f"Each topic must be a *decision question* answerable with free public data (yfinance, FRED, SEC EDGAR, DefiLlama, CoinGecko, blockchain.com). "
    f"Fields: question (one sentence, specific asset/period), data (named sources), method (from the toolkit), deliverable, risk (the most likely way it fails).",
    json_schema=CANDIDATE_SCHEMA)
cands = pd.DataFrame(out["candidates"])
pd.set_option("display.max_colwidth", 120)
cands.T
"""),
md("""
**Edit the three candidates in the cell below** — replace anything you would not defend. Then fill the weekly plan: what exists at the end of each weekend. If a week says "explore", the plan is not ready.
"""),
code("""
# Your three candidates, in the template. Overwrite the generated text.
template_keys = ["question", "data", "method", "deliverable", "risk", "wk7", "wk8", "wk9", "wk10"]
my_candidates = {
    "C1": dict(zip(template_keys, list(cands.iloc[0]) + ["feature + backtest skeleton", "add second data source", "risk canvas + SHAP", "memo + rehearsal"])),
    "C2": dict(zip(template_keys, list(cands.iloc[1]) + ["data pull works, snapshot saved", "quantitative element", "canvas + red-team", "memo + rehearsal"])),
    "C3": dict(zip(template_keys, list(cands.iloc[2]) + ["extraction pipeline on 3 filings", "scale to 10, evaluate", "canvas + SHAP", "memo + rehearsal"])),
}
pd.DataFrame(my_candidates)
"""),
code("""
# Feasibility scoring — 1 (bad) to 5 (good). Be honest; the weights are the tutor's.
feas_weights = {
    "data obtainable this week (proved by data_check)": 5,
    "method covered by week 9":                         4,
    "fits 4 weekends":                                  4,
    "answer is useful even if negative":                3,
    "connects to your next job":                        2,
}
feas = pd.DataFrame({"C1": [4, 5, 4, 5, 3], "C2": [3, 4, 3, 4, 5], "C3": [3, 4, 2, 3, 4]}, index=list(feas_weights))
fw = pd.Series(feas_weights)
print("feasibility (out of 5):"); print((feas.mul(fw, axis=0).sum() / fw.sum()).round(2).sort_values(ascending=False))
"""),
md("""
### The data check — the only part of the proposal that can fail before it starts
A proposal whose data cannot be loaded by Sunday is not a proposal. The homework asks for `data_check.ipynb`; this is the pattern. Loads the series, prints shape and date range, saves a dated snapshot. Adapt the loader to whichever source your candidate needs (FRED, DefiLlama, SEC EDGAR — same three tiers).
"""),
code("""
import datetime as dt, os
px = load_prices(["BTC-USD"], start="2020-01-01")
print("shape:", px.shape, "| range:", px.index.min().date(), "→", px.index.max().date())
print("missing values:", int(px.isna().sum().sum()), "| last value:", float(px.iloc[-1, 0]))
os.makedirs("data", exist_ok=True)
snap = f"data/capstone_check_{dt.date.today().isoformat()}.csv"; px.to_csv(snap); print("snapshot saved:", snap)
"""),
md("""
**🔍 CHECK.** If the first line printed `[SYNTHETIC]`, the check has *failed*: a random walk proves nothing about your data. The homework check passes only with `[live]` or `[snapshot]` from a real download.
"""),

# ------------------------------------------------------------------ closing
md("""
## Take-home (write three lines)
Three sentences in your own words, then `File ▸ Save a copy in GitHub` → `week-06/session.ipynb`.

1. _
2. _
3. _

**Homework brief** → `week-06/homework.md` (capstone proposal + data check, due Sunday 8 November).
"""),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["colab"] = {"provenance": [], "name": "week-06_session.ipynb"}
out = ROOT / "session.ipynb"
nbf.write(nb, out); print("wrote", out, "| code cells:", sum(c.cell_type == "code" for c in cells))
