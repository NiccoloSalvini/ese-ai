"""Builds week-04/session.ipynb with nbformat (same style as build_nbs_weeks1-3.py).
Run:  python build_nb.py   → writes session.ipynb next to this file."""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).parent

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

# --- course helper, reused verbatim from weeks 1-3 (prices are used in the cost block) ---
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

# ---------------------------------------------------------------------------------------------
# Fixed demo corpus. Three SYNTHETIC excerpts in the style of 10-K Item 1A risk factors (the
# companies do not exist) plus the abstract of the Bitcoin whitepaper (Nakamoto 2008, public).
# The Nordwind text is tuned so that a 500-character fixed chunker cuts "$1,250 million" and
# separates "11 hours" from "2.3 million" — see corpus_check.py.
# ---------------------------------------------------------------------------------------------
SYNTHETIC_CORPUS = {
"Nordwind Digital Assets, Inc. — 10-K FY2025, Item 1A (SYNTHETIC)": (
"SYNTHETIC EXCERPT written for teaching in the style of a 10-K risk-factor section. Nordwind Digital Assets, Inc. does not exist. "
"The risks described below are not the only ones we face; additional risks that we are not aware of, or that we currently consider immaterial, could also harm our business, financial condition and results of operations. "
"Investors should read this section together with our financial statements and related notes. "
"Our business is highly dependent on the prices of crypto assets and on the volume of transactions on our platform. "
"During the year ended December 31, 2025, approximately 61% of our net revenue was derived from transaction fees, and Bitcoin and Ethereum together accounted for approximately 47% of the trading volume on our platform. "
"A decline in prices or in trading activity, as occurred in 2022, would reduce our revenue and could adversely affect our results of operations. "
"We have a substantial amount of indebtedness. As of December 31, 2025, we had $1,250 million aggregate principal amount of convertible senior notes outstanding, of which $400 million matures in 2028 and $850 million matures in 2030. "
"Our ability to service this debt depends on our future performance, which is subject to market conditions that we do not control. "
"Our platform has experienced, and may in the future experience, service interruptions. On March 14, 2025, our trading platform was unavailable for approximately 11 hours, during which customers could not place orders or withdraw assets; the incident affected approximately 2.3 million customer accounts and we recorded $18 million of customer credits and remediation costs in the first quarter of 2025. "
"Any future interruption could damage our reputation, expose us to litigation and regulatory action, and cause customers to move their assets to competitors. "
"We hold crypto assets on behalf of customers in custody. As of December 31, 2025, we safeguarded approximately $94 billion of customer crypto assets. A loss of private keys, whether through cyberattack, employee error or fraud, could result in losses that are not insured and that we may be unable to reimburse. "
"We are subject to an evolving and uncertain regulatory landscape. In the European Union, the Markets in Crypto-Assets Regulation (MiCA) applies to crypto-asset service providers, and we obtained a MiCA authorisation in Ireland in July 2025. "
"In the United States, we are registered as a money services business and hold state money transmitter licences in 44 states. Failure to obtain or maintain licences, or the adoption of new requirements, could restrict our ability to operate in key markets. "
"We rely on third-party banking partners for fiat deposits and withdrawals. During 2025, two banking partners accounted for approximately 78% of our fiat transaction volume. The loss of either partner would materially disrupt our operations until a replacement is onboarded, which historically has taken three to six months. "
"We use machine learning models, including large language models, in customer support and in transaction monitoring. These systems may produce inaccurate or misleading outputs, and their use is increasingly regulated, including under the EU Artificial Intelligence Act, which may require additional documentation, human oversight and transparency measures."
),
"Lumen Payments Corp. — 10-K FY2025, Item 1A (SYNTHETIC)": (
"SYNTHETIC EXCERPT written for teaching in the style of a 10-K risk-factor section. Lumen Payments Corp. does not exist. "
"We generate most of our revenue from fees on payment transactions. In 2025 we processed $412 billion of total payment volume across 31 countries, and our take rate was approximately 1.9%. "
"A significant portion of our revenue depends on interchange fees set by card networks; regulatory caps on interchange, such as those in force in the European Union under the Interchange Fee Regulation, have reduced and may further reduce our margins. "
"We are exposed to losses from chargebacks and merchant fraud. In 2025 transaction and credit losses were $611 million, or 0.15% of total payment volume, compared with 0.12% in 2024. An increase in fraud, including fraud enabled by generative AI tools that produce convincing synthetic identities, could increase these losses. "
"Our business is subject to extensive regulation. We hold an electronic money institution licence from the Central Bank of Ireland, which allows us to operate across the European Economic Area under passporting rules, and we are registered as a money transmitter in the United States. "
"The revised Payment Services Directive (PSD2), its proposed successor PSD3 and the Payment Services Regulation impose strong customer authentication and open-banking obligations whose implementation costs are significant. "
"We use automated systems, including machine learning models, to approve or decline transactions and to onboard merchants. Errors in these models could result in declining legitimate transactions, which harms merchants, or approving fraudulent ones, which increases our losses. "
"Because some of these models assess the creditworthiness of small businesses for our working-capital product, they may be classified as high-risk AI systems under the EU Artificial Intelligence Act, which would require conformity assessment, risk management and human oversight. "
"We depend on a small number of large merchants. Our ten largest merchants represented approximately 22% of total payment volume in 2025, and our contracts with them generally may be terminated on 90 days' notice. "
"Our systems process personal data of more than 190 million consumers, and a data breach could result in fines under the General Data Protection Regulation of up to 4% of worldwide annual turnover, in addition to litigation and loss of trust. "
"We hold customer funds in safeguarding accounts at partner banks; at December 31, 2025 these balances were approximately $7.4 billion. A failure of a partner bank could delay customer access to funds even where the funds are legally protected."
),
"Arno Valley Bancorp — 10-K FY2025, Item 1A (SYNTHETIC)": (
"SYNTHETIC EXCERPT written for teaching in the style of a 10-K risk-factor section. Arno Valley Bancorp does not exist. "
"Our deposit base is concentrated. At December 31, 2025, uninsured deposits represented approximately 38% of total deposits of $19.6 billion, and our 25 largest depositors accounted for 11% of total deposits. "
"Events in the banking sector in 2023 demonstrated that deposit outflows can occur within hours when confidence is lost, accelerated by social media and by the ease of moving funds through mobile applications. "
"We have significant exposure to commercial real estate. Commercial real estate loans totalled $3.1 billion, or 42% of total loans, at December 31, 2025, including $860 million of office loans. Higher vacancy rates and higher refinancing costs could increase defaults and require additional provisions for credit losses. "
"Changes in interest rates affect our net interest income and the value of our securities portfolio. At December 31, 2025 our available-for-sale securities had unrealised losses of $310 million, and a 100 basis point increase in rates would reduce the fair value of the portfolio by a further estimated $190 million. "
"We use models, including machine learning models, in credit underwriting, in the allowance for credit losses and in anti-money-laundering monitoring. Model error, poor data quality or changes in borrower behaviour could cause these models to perform worse than expected. "
"Our credit-scoring models for consumer loans evaluate the creditworthiness of natural persons and are therefore expected to be treated as high-risk AI systems under the EU Artificial Intelligence Act in our European operations, and are subject to fair-lending laws in the United States. "
"We are subject to extensive supervision, including capital requirements. Our common equity tier 1 ratio was 10.8% at December 31, 2025, against a regulatory minimum of 7.0% including the capital conservation buffer. A deterioration in asset quality could reduce our ratio and restrict dividends and growth. "
"We depend on third-party technology providers for our core banking system and for our digital channels; the failure of a provider, or a cyberattack against one, could interrupt our services. In 2025 we spent $84 million on information security, an increase of 19% over 2024. "
"We face competition from larger banks and from non-bank financial technology companies that are not subject to the same regulatory requirements, which may offer products at lower prices or with faster onboarding."
),
"Bitcoin whitepaper — Abstract (Nakamoto, 2008; public)": (
"A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without going through a financial institution. "
"Digital signatures provide part of the solution, but the main benefits are lost if a trusted third party is still required to prevent double-spending. "
"We propose a solution to the double-spending problem using a peer-to-peer network. The network timestamps transactions by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be changed without redoing the proof-of-work. "
"The longest chain not only serves as proof of the sequence of events witnessed, but proof that it came from the largest pool of CPU power. "
"As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers. "
"The network itself requires minimal structure. Messages are broadcast on a best effort basis, and nodes can leave and rejoin the network at will, accepting the longest proof-of-work chain as proof of what happened while they were gone."
),
}

# The corpus is embedded in the notebook as a literal so the notebook is self-contained.
CORPUS_LITERAL = "SYNTHETIC_CORPUS = {\n" + "".join(
    f"    {k!r}:\n        ({' '.join(v.split())!r}),\n" for k, v in SYNTHETIC_CORPUS.items()) + "}"

cells = [
md("""
# Week 4 — LLM applications I: API, structured output, embeddings, RAG
**ESE · AI for Business and FinTech · 12 October 2026**

Today you call a language model from Python and build the simplest system that makes a model answer *from your documents instead of from its memory*: retrieval-augmented generation (RAG). Every call is logged with its cost and latency, because from today the model is a component with a price, not a chat window.

**Mock mode.** If `GEMINI_API_KEY` is not in Colab Secrets, every model call returns a deterministic canned answer and embeddings fall back to TF-IDF. The pipeline runs end-to-end, and the banner below says so loudly. Retrieval numbers are real in both modes; *generated* answers are only meaningful with a key.
"""),
code("""
!pip -q install google-genai tiktoken pydantic
# Optional, only if you have NO key and want neural embeddings instead of TF-IDF (2-3 min, downloads a model):
# !pip -q install sentence-transformers
"""),
code(UTILS),

# ------------------------------------------------------------------ Block A
md("## Block A — Calling a model from Python"),
md("""
Everything goes through one function, `llm()`, so the rest of the notebook (and your homework, and your capstone) never depends on a provider. Its arguments are the four things that matter in any API: the **prompt**, the **system** instruction (who the model is and what it may not do), the **temperature** (0 for extraction, higher for variety) and an optional **JSON schema** that forces the answer into a fixed shape you can check in code.

Every call appends a row to `CALL_LOG`: tokens in, tokens out, latency, cost.
""" ),
code("""
import os, re, json, time, hashlib
import numpy as np, pandas as pd

API_KEY = None
try:
    from google.colab import userdata
    API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    API_KEY = os.environ.get("GEMINI_API_KEY")

MOCK = not API_KEY
MODEL = "gemini-2.5-flash"
PRICE_PER_1M = {"input": 0.30, "output": 2.50}   # USD, illustrative for a small model in 2025-26 — check the provider's price page

if MOCK:
    print("=" * 78)
    print("  MOCK MODE: no GEMINI_API_KEY found in Colab Secrets.")
    print("  llm() returns deterministic canned text; embeddings use TF-IDF.")
    print("  The pipeline runs end-to-end, but GENERATED ANSWERS ARE NOT FROM A MODEL.")
    print("=" * 78)
else:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=API_KEY)
    print(f"API key found — live calls to {MODEL}")

try:
    import tiktoken
    _enc = tiktoken.get_encoding("o200k_base")
    def n_tokens(s): return len(_enc.encode(s))
except Exception:
    def n_tokens(s): return max(1, len(s) // 4)
"""),
code("""
CALL_LOG = []   # one dict per call

def _mock_llm(prompt, system, json_schema):
    \"\"\"Deterministic stand-in. If the prompt carries a CONTEXT block, echo the first sentence of the first passage,
    so the RAG pipeline visibly depends on what was retrieved. Otherwise, admit it is answering from 'memory'.\"\"\"
    if json_schema is not None:
        # prefer figures written with a currency sign, then any number (a dumb rule — a real model reads the sentence)
        nums = [float(x.replace(",", "")) for x in re.findall(r"\\$\\s?(\\d[\\d,]*\\.?\\d*)", prompt)] or \\
               [float(x.replace(",", "")) for x in re.findall(r"\\d[\\d,]*\\.?\\d*", prompt)]
        out = {}
        for name, field in json_schema.model_fields.items():
            t = field.annotation
            out[name] = (nums[0] if nums else 0.0) if t in (float, int) else ("MOCK-" + name if t is str else None)
        return out
    m = re.search(r"CONTEXT:\\n(.*?)\\n\\nQUESTION:", prompt, re.S)
    ctx = m.group(1).strip() if m else ""
    if ctx:
        first_passage = re.sub(r"^\\[\\d+\\][^\\n]*?\\n", "", ctx.split("\\n\\n")[0]).strip()
        sentence = re.split(r"(?<=[.!?])\\s+", first_passage)[0]
        return f"[MOCK answer, from passage [1]]: {sentence}"
    return "[MOCK answer] No CONTEXT block was supplied, so a real model would answer from memory — plausible, unverifiable."

def llm(prompt, system=None, json_schema=None, temperature=0):
    \"\"\"One call to the model. Returns text, or a dict if json_schema (a pydantic class) is given.
    Logs tokens, latency and cost in CALL_LOG. Ports to any provider: change only the body of the else-branch.\"\"\"
    t0 = time.time()
    if MOCK:
        out = _mock_llm(prompt, system, json_schema)
        tin, tout = n_tokens((system or "") + prompt), n_tokens(json.dumps(out) if isinstance(out, dict) else out)
    else:
        cfg = dict(temperature=temperature, system_instruction=system)
        if json_schema is not None:
            cfg.update(response_mime_type="application/json", response_schema=json_schema)
        r = client.models.generate_content(model=MODEL, contents=prompt, config=types.GenerateContentConfig(**cfg))
        out = json_schema.model_validate_json(r.text).model_dump() if json_schema is not None else r.text.strip()
        tin, tout = r.usage_metadata.prompt_token_count, r.usage_metadata.candidates_token_count or 0
    cost = tin / 1e6 * PRICE_PER_1M["input"] + tout / 1e6 * PRICE_PER_1M["output"]
    CALL_LOG.append(dict(t=time.strftime("%H:%M:%S"), tokens_in=tin, tokens_out=tout,
                         latency_s=round(time.time() - t0, 2), cost_usd=round(cost, 6), prompt=prompt, mock=MOCK))
    return out

print(llm("In one sentence, what is a 10-K filing?", system="You are a concise financial analyst."))
pd.DataFrame(CALL_LOG).drop(columns="prompt")
"""),
md("""
### A1. Temperature — bet first
**Bet (write it down):** at temperature 0, are two calls with the same prompt identical, character for character? And at temperature 1?
"""),
code("""
q = "Name three risk factors typically listed by a crypto exchange in its 10-K. One line."
a1 = llm(q, temperature=0); a2 = llm(q, temperature=0)
b1 = llm(q, temperature=1); b2 = llm(q, temperature=1)
print("T=0 identical:", a1 == a2); print("  ", a1[:150])
print("T=1 identical:", b1 == b2); print("  ", b1[:150]); print("  ", b2[:150])
if MOCK: print("\\n(mock mode: the canned answer is always identical — the real API is *almost* deterministic at T=0, not guaranteed)")
"""),
md("""
### A2. Structured output — the model as a parser
Free text is for humans. When the model's output goes into *code* (a table, a filter, a decision), ask for a fixed shape and validate it. `pydantic` describes the shape; the API is told to return JSON that matches it; the wrapper validates and returns a dict. If the shape is wrong, you get an exception, not a silent bad row.
"""),
code("""
from pydantic import BaseModel

class DebtFact(BaseModel):
    company: str
    metric: str
    value_usd_millions: float
    as_of: str

sentence = ("As of December 31, 2025, Nordwind Digital Assets had $1,250 million aggregate principal amount "
            "of convertible senior notes outstanding.")
fact = llm(f"Extract the debt figure from this sentence.\\n\\n{sentence}",
           system="Return only the fields requested. Use the company's name as written.", json_schema=DebtFact)
print(fact)
assert isinstance(fact["value_usd_millions"], float) and fact["value_usd_millions"] == 1250.0, "wrong number or type"
print("OK — a number you can put in a DataFrame, not a sentence you must read")
"""),
md("""
**🔍 CHECK.** Ask for the same extraction with the value in *dollars* instead of millions (change the field name). Does the model convert, or does it copy 1,250? Either way: the schema guarantees the *type*, not the *truth* — you still verify the number against the source, exactly as in week 1.
"""),

# ------------------------------------------------------------------ Block B
md("## Block B — Lab: a RAG pipeline, step by step"),
md("""
The problem: a model knows nothing about *your* documents — a 10-K filed last month, an internal policy, a whitepaper. Putting a whole 10-K in every call is possible (1M-token windows exist) but slow, expensive and noisy. RAG does the obvious thing: **chunk** the documents, **embed** each chunk, at question time **retrieve** the few chunks closest to the question, and **generate** the answer from those chunks only, with citations.

### B1. Corpus — three tiers
1. live: Item 1A "Risk Factors" from recent 10-K filings on SEC EDGAR (needs network; EDGAR requires a User-Agent);
2. snapshot: `data/edgar_*.txt` saved by a previous run;
3. **SYNTHETIC** excerpts written for this course in 10-K style (companies that do not exist) plus the Bitcoin whitepaper abstract (public).

The synthetic set is *always* loaded, because the planted bugs below depend on exact text; live filings are added on top when available.
"""),
code(CORPUS_LITERAL),
code("""
import requests, os, html as _html

EDGAR_TARGETS = {"Coinbase Global": "0001679788", "PayPal Holdings": "0001633917", "Block, Inc.": "0001512673"}
HEADERS = {"User-Agent": "ESE course notebook student@example.com"}   # EDGAR blocks requests without a contact

def fetch_risk_factors(cik, name, cache_dir="data", max_chars=60_000):
    \"\"\"Item 1A of the latest 10-K for one company: live EDGAR -> snapshot -> None.\"\"\"
    os.makedirs(cache_dir, exist_ok=True); snap = f"{cache_dir}/edgar_{cik}_1A.txt"
    try:
        sub = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=HEADERS, timeout=20).json()
        f = sub["filings"]["recent"]; i = f["form"].index("10-K")
        acc = f["accessionNumber"][i].replace("-", ""); doc = f["primaryDocument"][i]
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"
        raw = requests.get(url, headers=HEADERS, timeout=60).text
        text = _html.unescape(re.sub(r"<[^>]+>", " ", raw)); text = re.sub(r"\\s+", " ", text)
        starts = [m.start() for m in re.finditer(r"Item\\s*1A\\.?\\s*Risk Factors", text, re.I)]
        start = starts[1] if len(starts) > 1 else starts[0]            # first hit is the table of contents
        end = re.search(r"Item\\s*1B\\.?\\s*Unresolved", text[start:], re.I)
        sect = text[start: start + (end.start() if end else max_chars)][:max_chars]
        if len(sect) < 5000: raise RuntimeError("section too short — parsing failed")
        open(snap, "w").write(sect); print(f"[live] {name}: {len(sect):,} chars from {f['filingDate'][i]} 10-K; snapshot saved"); return sect
    except Exception as e:
        print(f"[warn] EDGAR failed for {name} ({type(e).__name__}); trying snapshot")
    if os.path.exists(snap):
        sect = open(snap).read(); print(f"[snapshot] {name}: {len(sect):,} chars"); return sect
    return None

DOCS = dict(SYNTHETIC_CORPUS)
for name, cik in EDGAR_TARGETS.items():
    s = fetch_risk_factors(cik, name)
    if s: DOCS[f"{name} — 10-K Item 1A (EDGAR)"] = s
if len(DOCS) == len(SYNTHETIC_CORPUS):
    print("[SYNTHETIC] no live filings and no snapshot: corpus is the bundled synthetic set only.")
pd.DataFrame({"chars": {k: len(v) for k, v in DOCS.items()}, "tokens": {k: n_tokens(v) for k, v in DOCS.items()}})
"""),
md("""
### B2. Chunking — bet first
**Bet:** a 60-page 10-K (assume 3,000 characters per page). At 500 tokens per chunk, how many chunks? Write the number before running.
"""),
code("""
chars = sum(len(v) for v in DOCS.values()); toks = sum(n_tokens(v) for v in DOCS.values())
cpt = chars / toks
pages, chars_per_page, chunk_tokens = 60, 3000, 500
print(f"corpus: {chars:,} chars, {toks:,} tokens -> {cpt:.2f} chars per token")
print(f"60-page 10-K ≈ {pages*chars_per_page:,} chars ≈ {pages*chars_per_page/cpt:,.0f} tokens ≈ {pages*chars_per_page/cpt/chunk_tokens:.0f} chunks of {chunk_tokens} tokens")
"""),
md("""
### 🔍 CHECK — the assistant's chunker
Asked for "a function that splits documents into chunks of 500 tokens", the assistant wrote the cell below. It runs. **It contains two mistakes.** Find them (10 minutes; hint after 5). Then look at what happened to the sentence about Nordwind's convertible notes.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
CHUNK_TOKENS = 500

def chunk_bad(docs):
    chunks = []
    for doc_name, text in docs.items():
        for i in range(0, len(text), CHUNK_TOKENS):
            chunks.append({"doc": doc_name, "text": text[i:i + CHUNK_TOKENS]})
    return chunks

chunks = chunk_bad(DOCS)
print(len(chunks), "chunks | mean tokens per chunk:", round(np.mean([n_tokens(c["text"]) for c in chunks])))
hits = [c for c in chunks if "1,2" in c["text"] and "Nordwind" in c["doc"]]
for c in hits: print("\\n...", repr(c["text"][-80:]))
nxt = chunks[chunks.index(hits[-1]) + 1]; print("\\nnext chunk starts:", repr(nxt["text"][:60]))
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **Units.** `CHUNK_TOKENS = 500` is applied to *characters*: `text[i:i+500]`. One token is ~4 characters of English, so the chunks are about 120 tokens, a quarter of the size asked for. Same family as percent-vs-decimal in week 2: a number with the wrong unit, silently.
2. **Boundaries.** The split ignores sentences, and there is no overlap. The chunk boundary fell inside a number: one chunk ends with `$1,2` and the next begins with `50 million`. Neither chunk contains "$1,250 million". No embedding, however good, can retrieve a fact that no longer exists in any chunk. The same cut separates "11 hours" from "2.3 million customer accounts": a question that needs both now needs two chunks.

The correction is not clever: split on sentence ends, fill up to a token budget, and repeat the last sentence at the start of the next chunk (overlap).
</details>
"""),
code("""
# Corrected: sentence-aware chunks with a token budget and one-sentence overlap
def chunk_docs(docs, max_tokens=150, overlap_sentences=1):
    chunks = []
    for doc_name, text in docs.items():
        sents = re.split(r"(?<=[.!?])\\s+", text.strip()); buf = []; k = 0
        for s in sents:
            if buf and n_tokens(" ".join(buf + [s])) > max_tokens:
                chunks.append({"doc": doc_name, "id": f"{doc_name[:12]}#{k}", "text": " ".join(buf)}); k += 1
                buf = buf[-overlap_sentences:]
            buf.append(s)
        if buf: chunks.append({"doc": doc_name, "id": f"{doc_name[:12]}#{k}", "text": " ".join(buf)})
    return chunks

chunks = chunk_docs(DOCS, max_tokens=150)
print(len(chunks), "chunks | tokens per chunk: mean", round(np.mean([n_tokens(c["text"]) for c in chunks])), "max", max(n_tokens(c["text"]) for c in chunks))
print("chunks containing the full figure:", sum("$1,250 million" in c["text"] for c in chunks))
print("chunks containing both '11 hours' and '2.3 million':", sum("11 hours" in c["text"] and "2.3 million" in c["text"] for c in chunks))
"""),
md("""
### B3. Embeddings — three tiers, one interface
An embedding maps text to a vector; cosine similarity between vectors is the search key. Three tiers, same interface: Gemini `text-embedding-004` (key) → `sentence-transformers` (downloaded model, no key) → TF-IDF (week 1's bag of words, labelled as the fallback it is). All vectors are L2-normalised so cosine similarity is a dot product.
"""),
code("""
class Embedder:
    def __init__(self, corpus_texts):
        self.kind = None
        if not MOCK:
            try:
                self._gem(["test"], "RETRIEVAL_DOCUMENT"); self.kind = "gemini/text-embedding-004"
            except Exception as e: print("[warn] Gemini embeddings failed:", type(e).__name__)
        if self.kind is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.st = SentenceTransformer("all-MiniLM-L6-v2"); self.kind = "sentence-transformers/all-MiniLM-L6-v2"
            except Exception as e: print("[warn] sentence-transformers unavailable:", type(e).__name__)
        if self.kind is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.tfidf = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit(corpus_texts); self.kind = "TF-IDF (FALLBACK — word overlap, not meaning)"
        print("embedder:", self.kind)

    def _gem(self, texts, task):
        out = []
        for i in range(0, len(texts), 100):
            r = client.models.embed_content(model="text-embedding-004", contents=texts[i:i+100], config=types.EmbedContentConfig(task_type=task))
            out += [e.values for e in r.embeddings]
        return np.array(out, dtype=float)

    def encode(self, texts, kind="document"):
        if self.kind.startswith("gemini"):   v = self._gem(texts, "RETRIEVAL_QUERY" if kind == "query" else "RETRIEVAL_DOCUMENT")
        elif self.kind.startswith("sentence"): v = np.asarray(self.st.encode(texts))
        else:                                 v = self.tfidf.transform(texts).toarray()
        return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-12)   # same normalisation for corpus and query

emb = Embedder([c["text"] for c in chunks])
CHUNK_VECS = emb.encode([c["text"] for c in chunks])
print(CHUNK_VECS.shape, "= (chunks, dimensions)")
"""),
code("""
def retrieve(question, k=3):
    qv = emb.encode([question], kind="query")[0]
    sims = CHUNK_VECS @ qv
    top = np.argsort(-sims)[:k]
    return [dict(chunks[i], score=float(sims[i])) for i in top]

for h in retrieve("How much convertible debt does Nordwind have?", k=3):
    print(f"{h['score']:.3f}  {h['id']:18s} {h['text'][:110]}...")
"""),
md("""
**🔍 CHECK.** Rephrase the question without the words "convertible" and "debt" (e.g. "What does Nordwind owe bondholders?"). With TF-IDF the top score collapses — word overlap, not meaning; with a neural embedding it should survive. This is the week-1 gap, now with a business consequence: *your customers do not use your vocabulary*.
"""),
md("""
### B4. Generation with citations — bet first
**Bet:** ask the outage question (duration *and* number of accounts) with `k=1` on the **bad** chunks, where the two facts sit in different chunks. Will the answer be (a) complete, (b) partial and honest, (c) partial and confidently wrong?
"""),
code("""
SYSTEM = ("You answer questions about company filings using ONLY the context passages. "
          "Cite passages as [1], [2]. If the context does not contain the answer, say 'Not in the provided context.'")

def build_prompt(question, hits):
    context = "\\n\\n".join(f"[{i+1}] ({h['doc'][:40]})\\n{h['text']}" for i, h in enumerate(hits))
    return f"CONTEXT:\\n{context}\\n\\nQUESTION: {question}\\nANSWER:"

def answer(question, k=3):
    hits = retrieve(question, k)
    return llm(build_prompt(question, hits), system=SYSTEM), hits

# 1) the bet: bad chunks, k=1
bad_chunks = chunk_bad(DOCS); bad_vecs = emb.encode([c["text"] for c in bad_chunks])
q = "How long was Nordwind's March 2025 outage and how many customer accounts were affected?"
qv = emb.encode([q], kind="query")[0]; top = bad_chunks[int(np.argmax(bad_vecs @ qv))]
print("retrieved (bad chunker, k=1):", repr(top["text"][-120:]))
print("\\nanswer:", llm(build_prompt(q, [top]), system=SYSTEM))
"""),
code("""
# 2) the same question on the corrected chunks, k=3
ans, hits = answer(q, k=3)
print(ans); print("\\nsources:", [h["id"] for h in hits])
"""),
md("""
### 🔍 CHECK — the assistant's "refactored" answer function
He asked the assistant to "make `answer()` self-contained and add a `context` parameter for extra notes". The result runs, and in live mode the answers read well. **Two mistakes.** Prove whether the model actually saw the retrieved passages — `CALL_LOG` keeps every prompt.
"""),
code("""
# --- as produced by the assistant (do not trust) ---
def answer_v2(question, k=3, context=""):
    qv = emb.encode([question], kind="query")[0]
    sims = CHUNK_VECS @ qv
    hits = [chunks[i] for i in np.argsort(sims)[:k]]
    ctx = "\\n\\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))
    prompt = f"CONTEXT:\\n{context}\\n\\nQUESTION: {question}\\nANSWER:"
    return llm(prompt, system=SYSTEM), hits

ans, hits = answer_v2("What share of Nordwind's net revenue comes from transaction fees?")
print(ans)
print("\\nretrieved ids:", [h["id"] for h in hits])
"""),
md("""
<details><summary>Solution (open after you have tried)</summary>

1. **Shadowing.** The passages are assembled into `ctx`, but the prompt is formatted with `context` — the new *parameter*, which defaults to `""`. The model receives an empty CONTEXT block. In mock mode the canned answer says so; a real model either refuses (if the system prompt is strict) or **answers from memory** — fluent, uncited, unverifiable. Check: `"transaction fees" in CALL_LOG[-1]["prompt"]` is `False`.
2. **Sort direction.** `np.argsort(sims)[:k]` takes the *least* similar chunks. Correct is `np.argsort(-sims)[:k]` (or `[::-1]`). Look at `retrieved ids`: they are from the wrong documents. This bug is invisible when the context is also dropped — bugs hide each other; that is why you log the prompt.

Rule: **log every prompt** and, in tests, assert that the retrieved text is inside it.
</details>
"""),
code("""
# Corrected — and a test that would have caught both bugs
def answer_v3(question, k=3, extra_notes=""):
    hits = retrieve(question, k)
    prompt = build_prompt(question, hits) + (f"\\nNOTES: {extra_notes}" if extra_notes else "")
    out = llm(prompt, system=SYSTEM)
    assert all(h["text"][:60] in CALL_LOG[-1]["prompt"] for h in hits), "retrieved text is not in the prompt"
    return out, hits

ans, hits = answer_v3("What share of Nordwind's net revenue comes from transaction fees?")
print(ans); print("\\nsources:", [h["id"] for h in hits])
print("\\ncontext really in the prompt:", "transaction fees" in CALL_LOG[-1]["prompt"])

# extra_notes is the door for live data: a price next to a filing figure (load_prices = the course helper)
px = load_prices(["BTC-USD"], start="2025-06-01")
note = f"BTC-USD close on {px.index[-1].date()}: {px['BTC-USD'].iloc[-1]:,.0f} USD"
ans, hits = answer_v3("Which of Nordwind's revenues would a fall in Bitcoin's price hit first?", extra_notes=note)
print("\\nwith a live note ->", ans); print("note in prompt:", note in CALL_LOG[-1]["prompt"])
"""),
md("""
### B5. A small test set: retrieval failure vs generation failure — bet first
Ten questions with expected answers is what your homework asks for. Here are six. Two columns: did the expected string appear in the **retrieved chunks** (retrieval hit) and in the **answer** (answer hit)? A miss in the first column is a chunking/embedding problem; a miss only in the second is a generation problem — different fixes.

**Bet:** how many of the six will be retrieval hits at k=3 with this embedder? (In mock mode read only the retrieval column — the "answer" is canned.)
"""),
code("""
TESTS = [
    ("How much convertible debt did Nordwind have outstanding at the end of 2025?", ["1,250"]),
    ("How long was Nordwind's March 2025 outage and how many accounts were affected?", ["11 hours", "2.3 million"]),
    ("What share of Nordwind's revenue came from transaction fees?", ["61%"]),
    ("What total payment volume did Lumen process in 2025?", ["412 billion"]),
    ("What percentage of Arno Valley's deposits were uninsured?", ["38%"]),
    ("How does the Bitcoin network prevent double-spending?", ["proof-of-work"]),
]
rows = []
for q, expected in TESTS:
    ans, hits = answer_v3(q, k=3)
    ctx = " ".join(h["text"] for h in hits)
    rows.append(dict(question=q[:60], retrieval_hit=all(e in ctx for e in expected), answer_hit=all(e in str(ans) for e in expected),
                     top_score=round(hits[0]["score"], 3), answer=str(ans)[:90]))
res = pd.DataFrame(rows); print("retrieval hits:", res.retrieval_hit.sum(), "/", len(res), "| answer hits:", res.answer_hit.sum(), "/", len(res), "(mock: ignore)")
res
"""),
md("""
**🔍 CHECK.** For each miss, write one word: *retrieval* or *generation*. Then re-run B5 with `k=1` and with `max_tokens=60` chunks (re-run B2's corrected cell and B3). Which knob moved which column? That table — questions × (retrieval hit, answer hit) — is the evaluation your homework must contain.
"""),
md("""
### B6. What it costs — bet first
**Bet:** the fintech assistant answers 1,000 customer questions a day with k=3 chunks. Cost per day, in dollars? Write a number.
"""),
code("""
log = pd.DataFrame(CALL_LOG).drop(columns="prompt")
rag = log[log.tokens_in > 300]                                  # calls that carried a context block
per_call = rag[["tokens_in", "tokens_out", "latency_s", "cost_usd"]].mean()
print(per_call.round(4).to_string())
print(f"\\n1,000 questions/day ≈ ${per_call.cost_usd*1000:.2f}/day ≈ ${per_call.cost_usd*1000*365:,.0f}/year at these prices")
print(f"…and a 10x larger 'frontier' model ≈ ${per_call.cost_usd*1000*365*10:,.0f}/year. Latency per answer ≈ {per_call.latency_s:.1f}s")
log.tail(8)
"""),

# ------------------------------------------------------------------ Block C
md("## Block C — EU AI Act (discussion; reading in `notes.md`)"),
md("""
No code. Read the one-page text in `week-04/notes.md` and take the three prompts to the whiteboard. One factual anchor from the corpus: three of the four documents above mention the AI Act — Lumen and Arno Valley expect their **creditworthiness** models to be high-risk; Nordwind expects **transparency and oversight** duties for its LLM support bot. Same law, different tiers, decided by *use*, not by technology.
"""),
code("""
for h in retrieve("Which AI systems does the EU AI Act treat as high-risk in this company?", k=3):
    print(f"{h['score']:.3f}  {h['id']:18s} {h['text'][:140]}...")
"""),

# ------------------------------------------------------------------ Close
md("""
## Take-home (write three lines)
Before committing, write in the cell below the three things you would tell a colleague who wants to "add an AI assistant" to a product this quarter. Then `File ▸ Save a copy in GitHub` → `week-04/session.ipynb`.

**Homework brief** → see `week-04/homework.md`.
"""),
md("""
_1._

_2._

_3._
"""),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["colab"] = {"provenance": [], "name": "week-04_session.ipynb"}
out = ROOT / "session.ipynb"
nbf.write(nb, out); print("wrote", out, "|", sum(c.cell_type == "code" for c in cells), "code cells")
