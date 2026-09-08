---
marp: true
theme: default
paginate: false
---

<!-- card 1 -->
# The ledger, from the bottom

```
 address        balance   nonce        who may edit the row?  -> the holder of the KEY
 0xA1...        12.40 ETH   57         a signed edit          -> a TRANSACTION
 0xB7...         0.05 ETH    3         a batch of edits       -> a BLOCK, chained by hash
 0xC3 (code)   900.00 ETH  ---         a row that runs code   -> a SMART CONTRACT
                                       price of inclusion     -> the FEE (scarce block space)
```

A wallet is not a place where coins are; it is the key that may edit one row.

---

<!-- card 2 -->
# One equation, everything else follows

$$x \cdot y = k \qquad p_{spot} = \frac{y}{x}$$

Sell $dx$: the pool must keep $k$, so $(x+dx)(y-dy) = k$

$$dy = y - \frac{k}{x+dx} = \frac{y\,dx}{x+dx} \qquad p_{exec} = \frac{dy}{dx} = p_{spot}\cdot\frac{x}{x+dx} \qquad p_{after} = \frac{y-dy}{x+dx} = p_{spot}\cdot\frac{x^2}{(x+dx)^2}$$

For $dx = 10\%$ of $x$: execution $-9.1\%$, pool price after $-17.4\%$. The curve is the market maker; slippage is geometry, not a fee.

---

<!-- card 3 -->
# LP value versus holding

Price moves from $p_0$ to $p_1 = r\,p_0$. Arbitrage resets the reserves to $x_1 = \sqrt{k/p_1}$, $y_1 = \sqrt{k\,p_1}$.

$$\text{LP} = y_1 + x_1 p_1 = 2\sqrt{k\,p_1} \qquad \text{hold} = y_0 + x_0 p_1 = \sqrt{k p_0}\,(1+r)$$

$$\frac{\text{LP}}{\text{hold}} = \frac{2\sqrt{r}}{1+r} \;\le\; 1 \quad\text{for every } r$$

At $r=2$: $0.943$, a loss of $5.7\%$ against holding. Divide by the initial deposit instead and it reads $+41\%$ — same position, wrong denominator.

---

<!-- card 4 -->
# What the LP is paid to bear it

| price ratio $r$ | 0.5 | 0.8 | 1.0 | 1.25 | 2 | 3 | 5 |
|---|---|---|---|---|---|---|---|
| LP / hold − 1 | −5.7% | −0.6% | 0 | −0.6% | −5.7% | −13.4% | −25.5% |
| daily volume/TVL to cover it in a year at 0.3% fee | 5.2% | 0.6% | 0 | 0.6% | 5.2% | 12.2% | 23.3% |

Fee yield ≈ fee × (daily volume ÷ TVL) × 365. Providing liquidity is a race between that yield and the price path.

---

<!-- card 5 -->
# Three businesses, one dashboard

| ratio | reads as | exchange (Uniswap) | lender (Aave) | staking (Lido) |
|---|---|---|---|---|
| fees ÷ TVL | asset turnover | high — capital touched daily | low — capital sits, earns spread | low — capital sits, earns yield |
| revenue ÷ fees | take rate | near 0 (LPs keep fees) | ~15% | ~10% |
| revenue ÷ market cap | 1 ÷ price-to-sales | | | |

The ratios differ by an order of magnitude because the businesses differ, not because one is better.

---

<!-- card 6 -->
# Five lenses, one protocol

| lens | the question | evidence looks like |
|---|---|---|
| smart-contract | can the code lose the money? | audit dates, upgrade keys, bug history |
| oracle | where do prices come from; what if wrong for 10'? | feed name, heartbeat, deviation threshold |
| governance | who changes parameters, how fast, what quorum? | timelock hours, quorum %, top-5 voter share |
| depeg / collateral | what backs the assets; what if backing trades at a discount? | reserve attestation, peg history, LTV |
| liquidity | if 20% of TVL leaves today, does it keep working? | utilisation, exit queue, largest depositor share |

A cell holds a fact with a link, never an adjective.

---

<!-- card 7 -->
# Cases, one line each — place them in the rows

```
2016  The DAO            re-entrancy in the contract drained a third of its ETH; Ethereum forked to undo it
2020  bZx / Harvest      flash loans moved a pool price; a lending contract trusted that price as its oracle
2021  Poly Network       cross-chain bridge key logic exploited, 600M USD moved, mostly returned
2022  Terra / UST        algorithmic peg broke; LUNA minted to defend it, both went to zero in a week
2022  Ronin bridge       five of nine validator keys compromised, 600M USD out
2022  Mango Markets      manipulated its own token's oracle price, borrowed against it, then voted on its own settlement
2023  Euler              donation attack on a lending contract, 200M USD, returned after negotiation
2023  USDC / SVB         3.3bn USD of reserves at a failed bank; USDC traded at 0.88 for a weekend
2023  Curve              compiler bug in Vyper hit pools; contagion through Curve-collateralised loans
2024  Ethena             on-chain data flagged funding-rate dependence of the yield before any stress; a design question, not a loss
```

---

<!-- card 8 -->
# MiCA in one table

| object | category | what is required | title |
|---|---|---|---|
| token referencing one fiat currency 1:1 | EMT | credit institution or EMI issuer; claim at par | IV |
| token referencing a basket or other assets | ART | authorised issuer; reserve; redemption at any time | III |
| any other crypto-asset (utility, governance, unbacked) | other | white paper notified; liability for content | II |
| custody, exchange, execution, advice, transfer, as a business | CASP service | authorisation, capital, segregation, market-abuse rules | V–VI |
| tokenised financial instrument; fully decentralised service with no intermediary | out of MiCA scope | MiFID applies; or nothing yet — case by case per ESMA | — |

The asset gets a category; the service gets an authorisation question; write both with the article.
