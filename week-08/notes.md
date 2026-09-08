# Week 8 — Digital assets, on-chain data and DeFi; MiCA/ESMA
**Monday 16 November 2026, 09:00–12:00 · ESE Florence**

## Learning objectives
By the end of the session the student can:
1. Explain, from the ledger up, what a wallet, a transaction, a block, a fee and a smart contract are, and why a stablecoin is a claim while a governance token is not.
2. Derive the price, the execution price and the price impact of a swap from the single equation x·y = k, and simulate a pool in code.
3. Compute an LP position's value against the *correct* benchmark (holding), quantify impermanent loss and the fee income that must cover it, and recognise a wrong denominator when an assistant produces one.
4. Read protocol business-model ratios (fees/TVL, take rate, revenue/mcap, concentration) from public APIs with snapshots, and use an LLM summary of a governance text only with a mechanical source check.
5. Place a protocol in a five-lens risk canvas and classify its assets under MiCA with an article-level justification.

## Session plan

| Time | Block | Mode |
|---|---|---|
| 09:00–09:20 | **HW7 walkthrough** | he presents |
| 09:20–10:00 | **A. Ledger to pool** | whiteboard + bets |
| 10:00–10:50 | **B. Lab 1: constant-product pool** | hands-on, notebook B |
| 10:50–11:00 | break | |
| 11:00–11:30 | **C. Lab 2: protocol data + LLM summary** | hands-on, notebook C |
| 11:30–12:00 | **D. Protocol risk lenses** (canvas, 20') → **E. MiCA/ESMA reading** (30' incl. prompts) → **Homework brief** | canvas + reading |

*The plan compresses D+E+brief into the last 30' on paper; in practice Lab 2 must end by 11:25 and D takes 15', E takes 20' with the reading assigned as pre-read on Friday (see Tutor's notes). If the reading was not done, E becomes the homework's first step and D gets the time.*

### HW7 walkthrough (20')
He presents the backtest memo. Two questions only: where in the notebook is the line that guarantees the signal at t is executed at t+1, and what happened to the Sharpe when costs went in. Then the model-risk question from week 7: what would trigger a review of this strategy if it were live.

### A. Ledger to pool (40', whiteboard)
Draw, do not define. A table with three columns (address, balance, nonce) is the ledger; a wallet is the key that can sign a row change, nothing more — no key, no coins. A transaction is a signed row change; a block is a batch of them with a hash of the previous batch; the fee is what you pay the batch-maker for inclusion, and it rises with congestion because block space is scarce. Draw one stablecoin two ways: a bank balance off-chain with a token on-chain (a claim — this is what MiCA will regulate in block E) and a vault of ETH with a token borrowed against it (a position). A smart contract is a row in the ledger that owns money and runs code when called: the code is the counterparty. [card 1]

Then the pool [card 2]: two reserves, one rule (x·y = k), and derive on the board: spot price y/x, output for input dx, execution price, pool price after. Draw the hyperbola; slippage is the curve, not a fee. Bets 1 and 2 are written here, before Lab 1. Then impermanent loss: the arbitrageur moves the pool, the LP ends with more of the loser. Derive 2√r/(1+r) on the board [card 3], but only after his bet.

His experience: at the Innovation Cluster he priced pilots with a fixed price list; a pool has no price list, only inventory. Ask him what a market maker in his BI dashboards would be measured on (turnover, spread capture) and map each one to fee yield and impermanent loss.

### B. Lab 1: constant-product pool (50', notebook)
The `Pool` class is shown, explained in 30", he runs it. Bet 1 verified on the 10%-of-reserve trade, then the impact table and chart.

🔍 CHECK — **the assistant's swap function** (planted bug 1). Two errors in six lines: `dy = dx * price` (linear quote: no curvature, zero slippage, pool can go negative) and `fee=0.3` (30%, percent vs decimal — the same silent error as the FRED yields in week 2). Ten minutes alone; the hint at five minutes is on the script. Corrected cell adds the two tests that always catch it: a trade of size zero and a trade the size of the reserve.

LP vs hold: bet 2 verified two ways (formula and reserves). 🔍 CHECK — **the assistant's impermanent-loss curve** (planted bug 2): it divides by the *initial* deposit value instead of the value of *holding*, so IL at 2× shows +41% instead of −5.7%. This is the bug of the session: a return is relative to something and the assistant picks the easiest denominator. Bet 3 (sign only) on fees vs IL, then the fee table and the real-path LP chart. On the synthetic fallback the ETH path is a random walk; say so and move on — the chart shape (LP below hold without fees, fee line crossing) is the same.

### C. Lab 2: protocol data + LLM summary (30', notebook)
Three-tier loader for DefiLlama + CoinGecko. Bet 4 before the ratio table: highest fees/TVL, highest revenue/mcap. Read the table as a SaaS dashboard: fees/TVL is asset turnover, take rate is what the protocol keeps, revenue/mcap is one over P/S. The ratios differ by an order of magnitude because the businesses differ (exchange vs lender vs staking). Then the TVL concentration cell and bet 5 (top-10 share), with the double-counting question (stETH counted in Lido and again as collateral in Aave).

Governance proposal: `llm()` summarises AIP-412, then the number-check cell. In mock mode the summary deliberately says 80% where the source says 79.5% and the check catches it; with a live key it may catch nothing, which is the moment to ask what the check *cannot* catch (wrong parameter attached, wrong direction). Same lesson as the RAG evals in week 4: necessary, not sufficient.

### D. Protocol risk lenses (15–20', canvas)
Five rows: smart-contract, oracle, governance, depeg/collateral, liquidity [card 6]. He fills the canvas for one protocol from the metrics table with a fact per cell, not an adjective. Then the historical cases card [card 7]: he places each case in a row — most fit two, and saying which two is the exercise. This canvas is the risk section of the homework and of the portfolio.

### E. MiCA/ESMA in practice (20–30', reading + prompts)
Reading is at the end of this file (`## Reading — MiCA and ESMA`); ideally pre-read. Three prompts, discussed at the table, then the notebook's structured-output cell that classifies USDC, stETH and UNI: the LLM output is a hypothesis and he must attach an article or definition from the reading to each line before accepting it. The stETH line is the interesting one: the token is barely regulated, the *service* (staking for clients, custody) is what needs a CASP authorisation.

### Homework brief (5–10')
`homework.md`. Emphasise: real data with a snapshot committed; the risk canvas is the deliverable; the MiCA classification needs a justification, not a label.

## Script

### HW7 walkthrough
- Opening: "Show me the line that moves the signal one day forward. Then show me the Sharpe before and after costs."
- Closing: "What would make you switch this strategy off if it were running with real money? That question is the model-risk policy from last week in one sentence."

### A. Ledger to pool [cards 1–3]
- Opening: "If I show you a spreadsheet with address, balance and nonce — what is missing for it to be Bitcoin?" He should get to *who is allowed to edit a row*, which is the key.
- "What is a fee paying for? Who receives it?" Discovery: block space is scarce; the batch-maker is paid, not the network.
- **Bet 1** (written): "A pool has 1,000 ETH and 3,000,000 USDC. You sell 100 ETH — 10% of the reserve. What average price do you get versus the spot 3,000, and where does the pool price sit after? Two numbers."
- **Bet 2** (written): "You deposited 1 ETH plus 3,000 USDC into that pool. ETH doubles. Is your LP position worth more, the same or less than if you had held the two coins — and by what percentage?"
- Discover before the tutor speaks: from x·y = k alone, that the output for dx is y − k/(x+dx), so the price paid gets worse as dx grows; and that after a price move the pool holds more of the loser.
- Hint if stuck: "Write k before and after the trade. Nothing else changes."
- Closing: "The curve is the market maker. There is no order book and no price list — only inventory and one equation."

### B. Lab 1 [cards 2–4]
- Opening: "Run the Pool cell. Then run the 100 ETH trade. Compare with your bet 1 — were you closer on the execution price or on the price after?"
- 🔍 CHECK swap function: "Same trade, the assistant's function. Two things are wrong. Do not read the solution; compare three numbers with the Pool class." Hint at 5': "Sell 100,000 ETH with the assistant's function. Then look at the fee as a number, not a name."
- Closing for the bug: "Whenever a function returns money, test it on zero and on the whole reserve."
- **Bet 3** (written, sign only): "Pool turns over 20% of its value per day, fee 0.3%, one year, ETH ends at 2×. Ahead of holding or behind? Write + or −."
- 🔍 CHECK IL curve: "The assistant's chart says you are +41% at 2×. Your cell above says −5.7%. Same pool, same price. Which line in the assistant's cell makes the difference?" Hint at 5': "Compared to what? Look at the denominator."
- Discover: the benchmark is holding, not the initial deposit.
- Closing: "Every percentage has a denominator. Ask 'compared to what' before you ask 'how much'." He writes this down.

### C. Lab 2 [card 5]
- Opening: "Three businesses: an exchange, a lender, a staking service. Without the data — which one makes its capital work hardest?"
- **Bet 4** (written): "Highest annualised fees/TVL: Uniswap, Aave or Lido? Highest revenue/market cap? Two names."
- **Bet 5** (written): "Top-10 protocols hold what share of total DeFi TVL — under 40%, 40–60%, over 60%?"
- Discover before the tutor speaks: fees/TVL of an exchange is an order of magnitude above a lender's, and that is turnover, not quality; and that the concentration number is inflated by the same ETH being counted in two layers.
- Hint if stuck (ratios): "Which of these protocols touches the same dollar many times a day?"
- LLM summary: "Read the summary, then run the check. What did it catch? Now tell me a wrong summary the check would pass." He should produce a wrong-direction or wrong-parameter example himself.
- Closing: "A number check is a floor, not a ceiling. It is the week-4 eval again: cheap, mechanical, necessary."

### D. Risk lenses [cards 6–7]
- Opening: "Pick one protocol from the table. For each of the five rows, one fact you can link to. No adjectives."
- Then the cases card: "Put each case in a row. Most fit two — which two, and in what order did they happen?"
- Hint if stuck: "Where did the money physically leave: through code, through a price, through a vote, through a redemption queue?"
- Closing: "The canvas is what you will hand in for the homework and again in the portfolio. Rows do not change; the evidence does."

### E. MiCA/ESMA [card 8]
- Opening: "You have read one page. In one sentence: what does MiCA regulate — the token, the issuer, or the service?" (All three, differently; he should reach that.)
- Prompts 1–3 from the reading section, 5' each.
- Then the notebook classification cell: "The model says EMT, other, other. For each line, name the definition from the reading that supports it. If you cannot, it is the model's classification, not yours."
- Closing: "For your homework protocol: the asset gets a category, the service gets an authorisation question, and both go in the memo with the article number."

### Take-home
"Three lines: something you can compute now that you could not at nine. Save a copy to GitHub, `week-08/session.ipynb`."

## Key concepts, in one line each
- Ledger / wallet / transaction / block / fee: a shared table; the key that may edit a row; a signed edit; a batch of edits chained by hash; the price of inclusion.
- Stablecoin: a token that references a fiat value — either a claim on an off-chain reserve (EMT/ART under MiCA) or a position against on-chain collateral.
- Smart contract: a ledger account that owns money and runs code when called; the code is the counterparty.
- Constant product x·y = k: the pool's only rule; spot price y/x; output y − k/(x+dx).
- Execution price vs pool price after: what you got on average; where the pool sits next. Both are the curve, neither is a fee.
- Impermanent loss: LP value ÷ hold value − 1 = 2√r/(1+r) − 1; always ≤ 0; benchmark is holding, never the initial deposit.
- Fee yield: fee × (daily volume / TVL) × 365; what the LP is paid to bear IL.
- TVL / fees / revenue / take rate: capital parked; what users pay; what the protocol keeps; revenue ÷ fees.
- Concentration (HHI, top-n share): sum of squared shares; inflated by the same collateral counted across layers.
- Oracle: the price feed a contract trusts; wrong for ten minutes is enough.
- Governance: who can change parameters, how fast, with what quorum.
- Depeg: the backing trades below the token; a collateral problem becomes a liquidity problem.
- MiCA: ART / EMT / other crypto-asset; CASP authorisation for services; ESMA and EBA guidelines and the transitional period.

## Tutor's notes
- **Live data:** `load_prices(["ETH-USD"])` (yfinance), DefiLlama (`api.llama.fi/tvl`, `/summary/fees`, `/protocols`) and CoinGecko `simple/price`. All three degrade to snapshot then labelled SYNTHETIC. Run the notebook on Friday on the ESE network and commit `data/` so the snapshot tier works on Monday if Yahoo or CoinGecko rate-limit (CoinGecko free tier can 429 — the loader treats it as a failure and falls to snapshot).
- **API key:** `llm()` needs `GEMINI_API_KEY` in Colab Secrets; without it the mock summary has the planted 80%/79.5% error, which is actually the better teaching case. With a live key, if the check catches nothing, use the "what would it not catch" question.
- **Synthetic fallback caveat:** the real-path LP chart on a random walk has no story; the fee-line crossing depends only on `vol_over_tvl`. The bet-4 answer on synthetic data (Uniswap on fees/TVL, Aave on revenue/mcap) is illustrative only — say so before he compares with his bet.
- **Cut if behind:** the real-path LP cell (keep the table), the TVL concentration cell (keep bet 5 as a discussion), and the notebook MiCA classification cell (do it verbally with the reading). Never cut the two planted bugs or bets 1–2.
- **Energy:** Lab 1 is dense; bet 3 (sign only) is the light moment — make it a race. Block D on the canvas is standing-up work at the whiteboard, not the laptop.
- Pre-read: send the MiCA reading on Friday with the three prompts; if he arrives without it, swap E and D order and read at the table for 8'.
- Do not get pulled into Uniswap v3 concentrated liquidity or MEV; both are one-sentence mentions ("v3 lets an LP choose a price range — same equation, sliced") and a homework extension.

## Reading — MiCA and ESMA

**What it is.** MiCA, Regulation (EU) 2023/1114 on Markets in Crypto-Assets, is the first EU-wide regime for crypto-assets that are not already financial instruments. It applies directly in all member states: the stablecoin titles (III and IV) since 30 June 2024, the rest — including the rules for service providers — since 30 December 2024. National regimes that existed before it (registration lists, local licences) are being replaced through a transitional period that ends by 1 July 2026 at the latest; from then a single MiCA authorisation passports across the EU.

**Three categories of asset.** MiCA sorts a crypto-asset by what it references. An *asset-referenced token* (ART, Title III) claims to keep a stable value by referencing several currencies, commodities, other crypto-assets or a basket; the issuer needs authorisation, a reserve, and redemption rights for holders at any time. An *e-money token* (EMT, Title IV) references one official currency one-to-one; only a credit institution or an electronic-money institution may issue it, and it is treated like electronic money — holders have a claim at par. Everything else is *other crypto-asset* (Title II): utility and governance tokens, unbacked coins. For those, there is no authorisation of the issuer, but a public offer or a listing requires a white paper notified to a national authority, with liability for misleading content. Assets that are already financial instruments under MiFID (a tokenised share, for instance), and fully decentralised services with no identifiable intermediary, are out of scope — a boundary that ESMA has said must be checked case by case, not assumed.

**Service providers.** Anyone who provides a crypto-asset service — custody, exchange, an order book, execution, advice, portfolio management, transfer — as a business in the EU must be authorised as a *crypto-asset service provider* (CASP, Title V). The authorisation carries capital, governance, custody segregation, complaints handling, and market-abuse rules (Title VI: insider dealing and manipulation now apply to crypto).

**Who supervises.** National competent authorities (in Italy, Consob for conduct and Banca d'Italia for prudential matters) authorise and supervise. ESMA (markets) and EBA (banks, and the significant stablecoin issuers) write the technical standards and guidelines that fill in the regulation — on what counts as a financial instrument, on the white-paper format, on how to assess reverse solicitation from outside the EU. ESMA also publishes a register of authorised CASPs and of non-compliant entities.

**What it does not do.** MiCA does not regulate DeFi protocols with no intermediary, NFTs that are truly unique, or lending and staking as such — the Commission owes a report on these. It also does not resolve the question that matters for a protocol analyst: when a "decentralised" front-end, a foundation or a multisig looks like an identifiable intermediary, the exemption may not hold.

**Three discussion prompts.**
1. USDC references one currency at par; DAI references the dollar but is backed by on-chain collateral and issued by a protocol. Under MiCA definitions, are they the same category? What is the issuer of DAI, and does the answer change the category or the enforceability?
2. A Lido stETH holder in Florence: which part of what happened — buying ETH on an exchange, staking through the protocol, holding stETH in a self-custody wallet — falls under a CASP authorisation, and which falls outside MiCA? Name the service, not the token.
3. A CASP lists UNI. Which MiCA obligations attach to the listing (white paper, market-abuse), and which risk lenses from block D would a compliance team need evidence for before listing? Where does the AI Act (week 4) bite if the listing decision uses a model?
