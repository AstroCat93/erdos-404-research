#!/usr/bin/env python3
"""qdp_check.py -- validates the residue-DP versions of the block constants (bounds.qconsts_dp, block0_table_dp)
against the full enumerations (bounds.qconsts, block0_table) for small p.  usage: qdp_check.py"""
from bounds import qconsts, qconsts_dp, block0_table, block0_table_dp
for p in (3, 5, 7, 11, 13):
    S = 4
    a, b = qconsts(p, S), qconsts_dp(p, S)
    P, Q = block0_table(p, S), block0_table_dp(p, S)
    print(f"RESULT p={p}: q_s (s<={S}) equal: {a == b};  P0 table equal: {P == Q}")
