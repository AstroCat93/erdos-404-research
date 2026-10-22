#!/usr/bin/env python3
"""cm_qtest.py -- runs test_small.py mode Q (exact Lemma Q test) at primes p > 13, where the 3^p enumeration of the
block constants is too slow: the constants are taken from the numpy residue DP of cm_consts.py (q_s for s <= 5,
extended by q_s <= p q_(s-1); P0(g,s) for s <= 5, extended by monotonicity in s).  Only k <= KMAX <= 5 is used,
so the extensions never enter.  (verify_M4A_logic, round 4)
usage: cm_qtest.py p SEED NTEST KMAX FMAX [CTRL]
"""
import sys
from fractions import Fraction

import test_small
from cm_consts import q_dp, P0_dp


def q_consts_dp(p, S):
    base = q_dp(p, 5)
    out = {s: (base[s] if s <= 5 else base[5] * Fraction(p) ** (s - 5)) for s in range(1, S + 1)}
    out['atom'] = None
    return out


def P0_table_dp(p, Smax):
    base = P0_dp(p, 5)
    return {g: [row[min(s, 5)] for s in range(Smax + 1)] for g, row in base.items()}


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    assert a[3] <= 5
    test_small.q_consts = q_consts_dp
    test_small.P0_table = P0_table_dp
    test_small.mode_Q(a[0], a[1], a[2], a[3], a[4], a[5] if len(a) > 5 else 0)
