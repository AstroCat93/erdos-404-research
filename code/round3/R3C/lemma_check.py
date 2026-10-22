#!/usr/bin/env python3
"""lemma_check.py (round 3, track R3C) -- numerical check of Lemma R3C.1 (report R3C.md):
for odd p, 2 <= t <= L_p and p+1+rho0(p) <= H <= 2p, Cov(p,t,H) holds, i.e. for every unit class
K' mod p (c = 1) the block ending at N* = p^t K' covers Z/p^(t+1).  Uses the independent big-integer
brute force bigbrute.py on every class.  Also reports, for H just below p+1+rho0 (where the lemma does
not apply), whether coverage holds (it must fail when (H-1) mod p < rho0, by Lemma 10.11(c)).
L_p values from note.md 3.5 (R8): L=2 for p=7,11,13; 3 for 17,19; 4 for 23."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bigbrute import missing  # noqa: E402
from predict import rho0  # noqa: E402

LP = {7: 2, 11: 2, 13: 2, 17: 3, 19: 3, 23: 4}
bad = 0
checked = 0
for p, L in LP.items():
    r0 = rho0(p)
    for t in range(2, L + 1):
        if p ** (t + 1) > 7_000_000:
            continue
        for H in range(p + 1, 2 * p + 1):
            res = [missing(p, t, H, K)[1] for K in range(1, p)]
            inlemma = H >= p + 1 + r0
            holds = all(m == 0 for m in res)
            if inlemma:
                checked += 1
                if not holds:
                    bad += 1
            print(f"p={p} t={t} H={H} rho={(H-1)%p} rho0={r0} lemma_applies={inlemma} holds={holds} max_missing={max(res)}")
print(f"LEMMA CHECK: (p,t,H) triples covered by the lemma: {checked}, violations: {bad}")
