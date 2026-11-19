# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jackson Fairbanks
# Reference implementation of the closed-form price equation and the
# Distance-to-Coverage-Breach (DCB) in: Fairbanks (2026), "Perpetual
# Preferred Equity Against Bitcoin: A Closed-Form Structural Credit
# Model."
# Pure standard library. Deterministic. No I/O.

import math

def price(bcy, c=10.0, r=0.044, sigma=0.50, alpha=1.0, v_b=None):
    """Closed-form price per $100 face value, eq. (3.7).
    bcy is stated at the kappa = 1 barrier convention (V_0 = bcy * c)."""
    if v_b is None:
        v_b = c                        # eq. (3.3): one forward year of the dividend
    v_0 = bcy * c                      # section 2.4: BCY = V_0 / C, with C = c per $100 face
    if v_0 < v_b:
        raise ValueError("below the coverage barrier: V_0 < V_B")
    beta = 2.0 * r / sigma ** 2        # eq. (3.5)
    breach = (v_b / v_0) ** beta       # breach factor, eq. (3.6)
    recovery = (1.0 - alpha) * v_b     # eq. (3.4)
    return (c / r) * (1.0 - breach) + recovery * breach

def dcb(bcy, sigma=0.50, t=5.0):
    """Distance-to-Coverage-Breach, eq. (3.9). Drift-free by construction."""
    if bcy < 1.0:
        raise ValueError("below the coverage barrier: BCY < 1")
    return math.log(bcy) / (sigma * math.sqrt(t))

def breach_prob(bcy, sigma=0.50, t=5.0):
    """Drift-free breach probability 2*Phi(-DCB), eq. (A.14).
    A structural first-passage quantity, not a default-probability estimate."""
    return math.erfc(dcb(bcy, sigma, t) / math.sqrt(2.0))
