"""The four test vectors of Appendix D.5.

Paper: Fairbanks (2026), "Perpetual Preferred Equity Against Bitcoin: A
Closed-Form Structural Credit Model."

Method, as stated in Appendix D.5: each call is recomputed from dcb_model.py
at full double precision, rounded half to even at the printed precision, and
must reproduce the printed value exactly. Any disagreement is reported as a
discrepancy. Neither side is silently corrected.

Run:  python3 test_vectors.py
Exit code 0 if all four vectors match, 1 otherwise.
"""
from decimal import Decimal, ROUND_HALF_EVEN

from dcb_model import price, dcb, breach_prob


def printed_form(x, like):
    """Round the exact value of the float x half to even, to as many decimals as `like` shows."""
    decimals = len(like.split(".")[1])
    return str(Decimal(x).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_EVEN))


# (call as printed in Appendix D.5, value computed here, printed value, source in the paper)
VECTORS = [
    ("price(5)",              price(5),              "98.296", "Table C.1, BCY_0 = 5, base case"),
    ("price(5, v_b=20.0)",    price(5, v_b=20.0),    "62.657", "Table 5, BCY_0 = 5, kappa = 2"),
    ("dcb(10)",               dcb(10),               "2.059",  "Table C.1, BCY_0 = 10, T = 5"),
    ("breach_prob(2, t=1.0)", breach_prob(2, t=1.0), "0.1657", "Table C.1, BCY_0 = 2, T = 1"),
]


def main():
    failures = 0
    print("Appendix D.5 test vectors")
    for call, value, printed, source in VECTORS:
        got = printed_form(value, printed)
        ok = got == printed
        failures += not ok
        status = "PASS" if ok else "DISCREPANCY"
        print(f"  {status:<11}  {call:<22} computed {got:>7}   printed {printed:>7}   {source}")
    passed = len(VECTORS) - failures
    print(f"{passed}/{len(VECTORS)} test vectors reproduce the printed values.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
