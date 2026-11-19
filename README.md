# Perpetual Preferred Against Bitcoin Structural Credit Model

Reference implementation and test vectors for the paper **"Perpetual Preferred Equity Against Bitcoin: A Closed-Form Structural Credit Model"** (Jackson Fairbanks, 2026).

Read the paper at True North: <https://tnorth.com/research/perpetual-preferred-equity-against-bitcoin-structural-credit-model/>

Repository: <https://github.com/jacksonfairbanks/perpetual-preferred-against-bitcoin-structural-credit-model>

License: MIT for the code in this repository (see `LICENSE`). The paper files (the PDF, the Markdown and the figures) and the abstract quoted below are all rights reserved and are not covered by the MIT license.

## Paper

**Perpetual Preferred Equity Against Bitcoin: A Closed-Form Structural Credit Model.** Jackson Fairbanks, Strive, Inc. True North Research Report No. TNR-2026-05, Version 1.0. Written August 2026. Posted November 17, 2026.

- True North, the home of the paper: <https://tnorth.com/research/perpetual-preferred-equity-against-bitcoin-structural-credit-model/>
- In this repository, PDF: [perpetual-preferred-equity-against-bitcoin-structural-credit-model.pdf](perpetual-preferred-equity-against-bitcoin-structural-credit-model.pdf)
- In this repository, Markdown: [perpetual-preferred-equity-against-bitcoin-structural-credit-model.md](perpetual-preferred-equity-against-bitcoin-structural-credit-model.md)

**Abstract.** This paper develops a closed-form structural credit model for perpetual preferred equity issued against a Bitcoin reserve. The instrument is perpetual equity. It has no maturity and is not debt. Its only payment is the preferred dividend. No redemption of the notional is scheduled, and no coverage level requires it. Solvency therefore turns on coverage of the dividend payments, not redemption of the notional. The model inherits the Black and Cox (1976) perpetual-claim closed form. Two reinterpretations adapt it to the instrument. First, both structural inputs are read off the market: the reserve value observed directly, and its volatility estimable from market data. Second, breach occurs at first passage of the reserve to an exogenous coverage barrier rather than an endogenous default boundary. The model produces two outputs. The first is a closed-form price equation for the instrument across the coverage domain: the present value of the dividend payments until the reserve first reaches the barrier. Recovery is zero because the contract provides for none. The second is the Distance-to-Coverage-Breach (DCB): the vol-scaled log-distance of the current reserve from the barrier, a single scalar invariant to the discount rate and the recovery assumption. The model extends to a multi-tranche preferred stack, where seniority is priced through ordered survival rather than recovery. The coverage barrier modeled in this paper sits by convention at one year of forward coverage, well above the level at which the reserve is exhausted. Neither output estimates where distress begins. They serve as a structural reference for market pricing, coverage monitoring, and future calibration.

## What this is

The model prices perpetual preferred equity issued against a Bitcoin reserve as the present value of its dividend payments until the reserve first reaches a coverage barrier. It produces two outputs: a closed-form price, and the Distance-to-Coverage-Breach (DCB), a vol-scaled log-distance from current coverage to the barrier.

This repository holds the paper's Appendix D as runnable files, and the paper itself.

| File | What it is |
|---|---|
| `dcb_model.py` | The listing printed in Appendix D.4, character for character. Three functions: `price`, `dcb`, `breach_prob`. Pure Python standard library, deterministic, no input or output. |
| `test_vectors.py` | The four test vectors of Appendix D.5. |
| `verify_tables.py` | Recomputes all 231 numeric cells of Tables 1 through 5 and Table C.1. |
| `perpetual-preferred-equity-against-bitcoin-structural-credit-model.pdf` | The paper as published, Version 1.0, 35 pages. |
| `perpetual-preferred-equity-against-bitcoin-structural-credit-model.md` | The paper's full text in Markdown, from the author's source file. Equation markup is adapted so GitHub displays it, and each equation number follows its equation. |
| `figures/` | The paper's four figures as SVG files. The Markdown file displays them. |
| `CITATION.cff` | Citation metadata, with the paper as the preferred citation. |
| `LICENSE` | MIT, code only. |

The home of the paper is True North. If a paper file here ever differs from True North, True North governs. Equations in the Markdown file are written in LaTeX, and GitHub may not display all of them. The PDF is the typeset version.

Terms, as the paper defines them:

- **Bitcoin Coverage Years (BCY).** Reserve value over annual dividend payments. BCY = 3 means the reserve equals three years of dividend payments (Section 2.4).
- **Coverage barrier.** BCY = 1, the level at which the reserve no longer covers one forward year of dividend payments. Reaching the barrier is the coverage breach (Section 2.5).
- **Breach factor.** `(V_B / V_0) ** beta` with `beta = 2r / sigma^2`. It is the present value of one dollar paid at the first time the reserve touches the barrier (Section 3.3).
- **Distance-to-Coverage-Breach (DCB).** `ln(BCY) / (sigma * sqrt(T))`. It is invariant to the discount rate and the recovery assumption (Section 3.6).

## Quickstart

```
git clone https://github.com/jacksonfairbanks/perpetual-preferred-against-bitcoin-structural-credit-model.git
cd perpetual-preferred-against-bitcoin-structural-credit-model
python3 test_vectors.py       # the four test vectors of Appendix D.5
python3 verify_tables.py      # all 231 cells of Tables 1-5 and Table C.1
```

Python 3, standard library only. No dependencies and no install step. Tested on Python 3.12.

## Usage

```python
from dcb_model import price, dcb, breach_prob

price(5)                  # 98.29643677461263    price per $100 face value at BCY = 5, base case
price(5, sigma=0.60)      # 73.9212411315256     same coverage at 60% reserve volatility
price(5, v_b=20.0)        # 62.656577213143244   barrier at two forward years of the dividend
dcb(10)                   # 2.0594947167649447   DCB at BCY = 10, horizon T = 5 years
breach_prob(2, t=1.0)     # 0.165657038003397    drift-free breach probability at BCY = 2, T = 1 year
```

| Function | Returns | Paper |
|---|---|---|
| `price(bcy, c=10.0, r=0.044, sigma=0.50, alpha=1.0, v_b=None)` | Closed-form price per $100 face value | eq. (3.7) |
| `dcb(bcy, sigma=0.50, t=5.0)` | Distance-to-Coverage-Breach | eq. (3.9) |
| `breach_prob(bcy, sigma=0.50, t=5.0)` | Drift-free breach probability `2*Phi(-DCB)` | eq. (A.14) |

| Input | Meaning | Base case |
|---|---|---|
| `bcy` | Current Bitcoin Coverage Years: reserve value over annual dividend payments | none |
| `c` | Dollar dividend per year per $100 face value | 10.0 |
| `r` | Continuously compounded risk-free rate per year | 0.044 |
| `sigma` | Annualized volatility of the reserve | 0.50 |
| `alpha` | Recovery-loss fraction at breach. 1.0 is zero recovery | 1.0 |
| `v_b` | Coverage barrier in $ per $100 face value. Defaults to `c`, one forward year of the dividend. Exposed only for the barrier sweep of Section 4.5 | `c` |
| `t` | Reporting horizon in years, for DCB and the breach probability | 5.0 |

The valid domain is `V_0` at or above `V_B`, which is BCY at or above 1 at the one-forward-year barrier convention. Below the coverage barrier the functions raise `ValueError`. The model prices no state there.

## Equations

```
Price    P_0  = (c/r) * [1 - (V_B/V_0)^beta] + R * (V_B/V_0)^beta      eq. (3.7)
         beta = 2r / sigma^2                                            eq. (3.5)
         R    = (1 - alpha) * V_B                                       eq. (3.4)
DCB      DCB  = ln(BCY_0) / (sigma * sqrt(T))                           eq. (3.9)
Breach   Pr(tau <= T) at zero drift = 2 * Phi(-DCB)                     eq. (A.14)
```

`V_B / V_0 = 1 / BCY_0` at the one-forward-year barrier convention. `Phi` is the standard normal cumulative distribution function. Derivations are in Appendices A and B of the paper.

## Test vectors

From Appendix D.5. Each call is recomputed at full double precision, rounded half to even at the printed precision, and must reproduce the printed value exactly.

| Call | Printed value | Source |
|---|---|---|
| `price(5)` | 98.296 | Table C.1, BCY = 5, base case |
| `price(5, v_b=20.0)` | 62.657 | Table 5, BCY = 5, kappa = 2 |
| `dcb(10)` | 2.059 | Table C.1, BCY = 10, T = 5 |
| `breach_prob(2, t=1.0)` | 0.1657 | Table C.1, BCY = 2, T = 1 |

Expected output:

```
$ python3 test_vectors.py
Appendix D.5 test vectors
  PASS         price(5)               computed  98.296   printed  98.296   Table C.1, BCY_0 = 5, base case
  PASS         price(5, v_b=20.0)     computed  62.657   printed  62.657   Table 5, BCY_0 = 5, kappa = 2
  PASS         dcb(10)                computed   2.059   printed   2.059   Table C.1, BCY_0 = 10, T = 5
  PASS         breach_prob(2, t=1.0)  computed  0.1657   printed  0.1657   Table C.1, BCY_0 = 2, T = 1
4/4 test vectors reproduce the printed values.

$ python3 verify_tables.py
Table 1     60/60  cells match
Table 2     36/36  cells match
Table 3     48/48  cells match
Table 4     48/48  cells match
Table 5      9/9   cells match
Table C.1   30/30  cells match
231/231 cells reproduce the printed values.
```

Any disagreement is printed as a `DISCREPANCY` line and the script exits with code 1. Neither side is silently corrected.

SHA-256 of `dcb_model.py`: `651b16d65d0514bef0145605ddf5bdd2f007109c583c753920272dd14993e66a`

## What the outputs are not

- The price is a structural reference for market pricing. It is not a forecast of market price.
- `breach_prob` is a structural first-passage quantity under a drift-free convention. It is not a default-probability estimate.
- Neither output estimates where distress begins. The coverage barrier sits by convention at one forward year of coverage.
- The model captures coverage-breach risk only. Section 6.3 of the paper sets out the limitations and the model-vs-market gap.

## Citation

If you use this code or the model, cite the paper:

```
Jackson Fairbanks, 2026. Perpetual Preferred Equity Against Bitcoin: A Closed-Form Structural Credit Model. True North Research Report No. TNR-2026-05. https://tnorth.com/research/perpetual-preferred-equity-against-bitcoin-structural-credit-model/
```

```bibtex
@techreport{fairbanks2026structural,
  author      = {Fairbanks, Jackson},
  title       = {Perpetual Preferred Equity Against Bitcoin: A Closed-Form Structural Credit Model},
  institution = {True North},
  type        = {True North Research Report},
  number      = {TNR-2026-05},
  year        = {2026},
  url         = {https://tnorth.com/research/perpetual-preferred-equity-against-bitcoin-structural-credit-model/}
}
```

Machine-readable citation metadata: `CITATION.cff`.

## Related

- Backtest paper: "Perpetual Preferred Equity Against Bitcoin: Required Coverage Across Observed Drawdowns" (Fairbanks, 2026). It develops Bitcoin Coverage Years empirically and is cited in this paper. Paper at True North: <https://tnorth.com/research/perpetual-preferred-equity-against-bitcoin-required-coverage/>. Replication repository: <https://github.com/jacksonfairbanks/perpetual-preferred-against-bitcoin-backtest>.

## Contact

Code-level bugs and replication issues: <https://github.com/jacksonfairbanks/perpetual-preferred-against-bitcoin-structural-credit-model/issues>

Paper discussion and feedback: [@LongGamma](https://x.com/LongGamma) on X.
