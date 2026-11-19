"""Reproduce every numeric cell of Tables 1-5 and Table C.1 from dcb_model.py.

Paper: Fairbanks (2026), "Perpetual Preferred Equity Against Bitcoin: A
Closed-Form Structural Credit Model."

Method, as stated in Appendix D.5: each cell is recomputed at full double
precision, rounded half to even at the printed precision, and compared with
the printed value. Any disagreement is reported as a discrepancy. Neither
side is silently corrected.

The printed values below are the paper's own tables. The first number in each
row is BCY_0, the starting Bitcoin Coverage Years. The remaining numbers are
the table's columns in the order printed. 231 cells in total:
60 + 36 + 48 + 48 + 9 + 30.

Run:  python3 verify_tables.py
Exit code 0 if all 231 cells match, 1 otherwise.
"""
from decimal import Decimal, ROUND_HALF_EVEN

from dcb_model import price, dcb, breach_prob


def printed_form(x, like):
    """Round the exact value of the float x half to even, to as many decimals as `like` shows."""
    decimals = len(like.split(".")[1])
    return str(Decimal(x).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_EVEN))


# Table 1. Price ($ per $100 face value) across alpha, at r = 4.4%, sigma = 50%.
# Columns: alpha = 0.0, 0.25, 0.5, 0.75, 1.0
TABLE_1 = """
   1    10.000     7.500     5.000     2.500     0.000
   2    57.040    55.081    53.123    51.164    49.205
   3    79.682    77.984    76.286    74.588    72.889
   5   103.971   102.553   101.134    99.715    98.296
   7   117.743   116.483   115.223   113.963   112.702
  10   130.666   129.555   128.443   127.332   126.220
  15   143.516   142.552   141.588   140.625   139.661
  20   151.582   150.711   149.840   148.969   148.098
  25   157.300   156.495   155.689   154.884   154.079
  30   161.649   160.894   160.139   159.384   158.629
  40   167.969   167.287   166.605   165.922   165.240
  50   172.449   171.818   171.187   170.557   169.926
"""

# Table 2. Price ($ per $100 face value) across sigma, at alpha = 1.0, r = 4.4%.
# Columns: sigma = 40%, 50%, 60%
TABLE_2 = """
   1     0.000     0.000     0.000
   2    72.041    49.205    35.423
   3   103.070    72.889    53.526
   5   133.492    98.296    73.921
   7   149.336   112.702    86.029
  10   163.219   126.220    97.822
  15   176.022   139.661   110.037
  20   183.522   148.098   117.998
  25   188.575   154.079   123.799
  30   192.268   158.629   128.310
  40   197.390   165.240   135.030
  50   200.842   169.926   139.927
"""

# Table 3. Price ($ per $100 face value) across r, at alpha = 1.0, sigma = 50%.
# Columns: r = 3.0%, 4.4%, 6.0%, 8.0%
TABLE_3 = """
   1     0.000     0.000     0.000     0.000
   2    51.085    49.205    47.170    44.786
   3    77.257    72.889    68.304    63.120
   5   106.803    98.296    89.693    80.376
   7   124.377   112.702   101.173    89.021
  10   141.520   126.220   111.478    96.364
  15   159.306   139.661   121.239   102.909
  20   170.916   148.098   127.098   106.624
  25   179.386   154.079   131.117   109.070
  30   185.977   158.629   134.096   110.824
  40   195.807   165.240   138.297   113.208
  50   202.979   169.926   141.178   114.777
"""

# Table 4. DCB across horizon T (years), at sigma = 50%.
# Columns: T = 1, 3, 5, 10
TABLE_4 = """
   1   0.000   0.000   0.000   0.000
   2   1.386   0.800   0.620   0.438
   3   2.197   1.269   0.983   0.695
   5   3.219   1.858   1.440   1.018
   7   3.892   2.247   1.740   1.231
  10   4.605   2.659   2.059   1.456
  15   5.416   3.127   2.422   1.713
  20   5.991   3.459   2.679   1.895
  25   6.438   3.717   2.879   2.036
  30   6.802   3.927   3.042   2.151
  40   7.378   4.260   3.299   2.333
  50   7.824   4.517   3.499   2.474
"""

# Table 5. Price ($ per $100 face value) across the barrier convention kappa, base case.
# Coverage is stated at the kappa = 1 convention, so V_B = kappa * c with c = 10.
# Columns: kappa = 0.5, 1, 2
TABLE_5 = """
   2    87.757    49.205    0.000
   5   126.220    98.296   62.657
  10   148.098   126.220   98.296
"""

# Table C.1. Integrated model outputs at base case.
# Columns: price, DCB at T = 5, then 2*Phi(-DCB) at T = 1, 5, 10
TABLE_C1 = """
   1     0.000   0.000   1.0000   1.0000   1.0000
   2    49.205   0.620   0.1657   0.5353   0.6611
   5    98.296   1.440   0.0013   0.1500   0.3087
  10   126.220   2.059   0.0000   0.0394   0.1453
  20   148.098   2.679   0.0000   0.0074   0.0581
  50   169.926   3.499   0.0000   0.0005   0.0134
"""


# One entry per table: (name, printed rows, one function per column mapping BCY_0 to the value).
CHECKS = [
    ("Table 1", TABLE_1, [
        lambda b: price(b, alpha=0.0),
        lambda b: price(b, alpha=0.25),
        lambda b: price(b, alpha=0.5),
        lambda b: price(b, alpha=0.75),
        lambda b: price(b, alpha=1.0),
    ]),
    ("Table 2", TABLE_2, [
        lambda b: price(b, sigma=0.40),
        lambda b: price(b, sigma=0.50),
        lambda b: price(b, sigma=0.60),
    ]),
    ("Table 3", TABLE_3, [
        lambda b: price(b, r=0.030),
        lambda b: price(b, r=0.044),
        lambda b: price(b, r=0.060),
        lambda b: price(b, r=0.080),
    ]),
    ("Table 4", TABLE_4, [
        lambda b: dcb(b, t=1.0),
        lambda b: dcb(b, t=3.0),
        lambda b: dcb(b, t=5.0),
        lambda b: dcb(b, t=10.0),
    ]),
    ("Table 5", TABLE_5, [
        lambda b: price(b, v_b=5.0),     # kappa = 0.5
        lambda b: price(b, v_b=10.0),    # kappa = 1
        lambda b: price(b, v_b=20.0),    # kappa = 2
    ]),
    ("Table C.1", TABLE_C1, [
        lambda b: price(b),
        lambda b: dcb(b, t=5.0),
        lambda b: breach_prob(b, t=1.0),
        lambda b: breach_prob(b, t=5.0),
        lambda b: breach_prob(b, t=10.0),
    ]),
]

EXPECTED_CELLS = 231


def main():
    total = matched = 0
    for name, printed_rows, columns in CHECKS:
        cells = ok = 0
        for line in printed_rows.strip().splitlines():
            fields = line.split()
            bcy, printed_values = int(fields[0]), fields[1:]
            if len(printed_values) != len(columns):
                print(f"DISCREPANCY  {name}, BCY_0 = {bcy}: {len(printed_values)} printed values, {len(columns)} columns")
                cells += len(columns)
                continue
            for number, (printed, compute) in enumerate(zip(printed_values, columns), start=1):
                got = printed_form(compute(bcy), printed)
                cells += 1
                if got == printed:
                    ok += 1
                else:
                    print(f"DISCREPANCY  {name}, BCY_0 = {bcy}, column {number}: computed {got}, printed {printed}")
        print(f"{name:<10} {ok:>3}/{cells:<3} cells match")
        total += cells
        matched += ok
    print(f"{matched}/{total} cells reproduce the printed values.")
    if total != EXPECTED_CELLS:
        print(f"DISCREPANCY  expected {EXPECTED_CELLS} cells, found {total}")
    return 0 if matched == total == EXPECTED_CELLS else 1


if __name__ == "__main__":
    raise SystemExit(main())
