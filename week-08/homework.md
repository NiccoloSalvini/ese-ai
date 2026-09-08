# Homework 8 — One protocol through three lenses
**Due: Sunday 22 November 2026, 23:59 · folder `week-08/hw/` in your repo**

## Goal
Take one DeFi protocol and analyse it the way you would analyse a fintech before a partnership: as a business (what it sells, what it keeps), through its data (real, with a snapshot), and through its risks (the five-lens canvas). Finish with its MiCA classification and a justification you could defend to a compliance officer.

## Pick a protocol (one)
- An exchange (Uniswap, Curve, PancakeSwap, a Solana DEX) — quantitative element: price impact or LP-vs-hold on one of its real pools.
- A lender (Aave, Compound, Morpho, Spark) — quantitative element: utilisation and interest-rate curve, or bad-debt exposure under a price shock.
- A staking or restaking service (Lido, Rocket Pool, EigenLayer, Jito) — quantitative element: staked share, exit-queue depth, or the stETH/ETH discount history.
- A stablecoin issuer (Sky/DAI, Ethena, Frax) — quantitative element: collateral composition and peg deviation history.
- Your own, if DefiLlama has fees and TVL for it. Message me first if it is not on that list; your capstone protocol is the obvious choice.

## Deliverables (in `week-08/hw/`)
1. `protocol.ipynb` — runs from a clean runtime. Must contain, in this order:
   - data acquisition through the three-tier loader (live → dated snapshot in `data/` → labelled synthetic); the **snapshot must be committed** so I can run it without network;
   - business-model table: TVL, annualised fees, annualised revenue, market cap, and the ratios fees/TVL, take rate, revenue/mcap, with a sentence per ratio saying what it means *for this business*;
   - at least **one quantitative element** specific to the protocol type (see the list above), computed from real data, with a chart whose title states the conclusion;
   - a comparison against one peer on the same ratios (a second DefiLlama slug is enough);
   - the risk canvas as a DataFrame with the five lenses, one fact and one link per row, and a severity 1–5 with a sentence justifying it;
   - a governance or documentation text summarised by `llm()` (mock allowed) followed by the number-check cell, with your own example of a wrong summary the check would pass.
2. `memo.md` (500–700 words) with these headings:
   - **What it sells and what it keeps** (the business-model ratios in one paragraph)
   - **The number that matters** (your quantitative element: what it shows and what would change your view)
   - **Risk canvas** (the five rows, one line each, and the one row you would act on first)
   - **MiCA classification** — category of the protocol's main token (ART / EMT / other / out of scope), the article or definition that supports it, and the service (if any) that would need a CASP authorisation in the EU
   - **What the assistant got wrong** (at least one: denominator, percent vs decimal, a hallucinated number, a category with no article)
   - **AI-use disclosure**

## Constraints
- Real data, with the snapshot committed. Synthetic fallback is allowed only as a labelled pipeline test and never as a number in the memo.
- Every percentage in the memo has a denominator stated next to it. "Impermanent loss of 5%" without "versus holding" is a mistake.
- The MiCA paragraph must cite the reading or the regulation text; a category with no justification scores as absent.
- Fees and revenue are DefiLlama's definitions; say which `dataType` you used.

## Scope
4–6 hours. The canvas and the MiCA paragraph are the part I will read most carefully; the notebook is the evidence for them. If the protocol's data is thin (no fees endpoint, no governance text), say so and use what exists — a canvas row that says "no public audit found, severity 5" is a valid finding.

## Self-check
- [ ] Restart and run all: no errors, with and without network.
- [ ] Snapshot CSVs in `week-08/hw/data/` and committed.
- [ ] Ratio table with a one-sentence reading per ratio.
- [ ] Quantitative element from real data; chart title states the conclusion.
- [ ] Peer comparison present.
- [ ] Risk canvas: five rows, fact + link + severity each.
- [ ] Number-check on the LLM summary, plus your own uncaught-error example.
- [ ] MiCA category with article/definition; CASP service named or ruled out.
- [ ] Denominator stated next to every percentage; AI-use disclosure present.

## How this feeds the capstone
The protocol analysis is a full chapter of the portfolio: the business-model table becomes the domain section of the decision memo, the canvas is the first draft of the risk and controls canvas (week 9 adds model risk and the AI Act rows), and the MiCA paragraph is the regulation section. If your capstone is on a digital-asset question, do this homework on that protocol and reuse everything.
