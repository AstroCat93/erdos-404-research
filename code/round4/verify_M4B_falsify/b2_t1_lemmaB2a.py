"""b2_t1_lemmaB2a.py -- exhaustive exact test of M4B Lemma B2a (factorial cancellation).

Claim: eps_0..eps_{d-1} in {-1,0,1}, sum_{k<d} eps_k/k! = 0  ==>  eps_k = 0 (k>=2), eps_0 = -eps_1.
Test 1 (integer form): all 3^d vectors, by meet in the middle on sum_k eps_k (d-1)!/k! (exact ints),
         for every d <= DMAX.  Expected solution set: {0, (1,-1,0,..), (-1,1,0,..)} (d>=2), {0} (d=1).
Test 2 (the form used in Cor B2'(b)): A_0 = sum_{i<d} delta_i (-1)^i (d-1)!/(d-1-i)!; expected
         solutions delta = 0 and delta = +-(e_{d-2}+e_{d-1}).
Test 3 (sharpness of the hypothesis p^s > e (d-1)!): for p in {3,5,7} and every d <= DMAX3 and s,
         count delta with A_0 == 0 mod p^s; report the least s for which only the 3 trivial
         solutions remain, against the least s with p^s > e (d-1)!.
Also checks the two numeric inequalities in the written proof for k* <= 60.
usage: b2_t1_lemmaB2a.py DMAX DMAX3
"""
import itertools
import math
import sys
from collections import defaultdict
from fractions import Fraction as Fr

from b2_lib import hyp_deep


def mitm_solutions(coeffs, modulus=None, keep=12):
    """all sign vectors e in {-1,0,1}^len with sum e_k coeffs_k == 0 (or == 0 mod modulus).
    returns (count, list of up to `keep` solutions)."""
    L = len(coeffs)
    h = L // 2
    left = defaultdict(list)
    for e in itertools.product((-1, 0, 1), repeat=h):
        sm = sum(a * b for a, b in zip(e, coeffs[:h]))
        if modulus:
            sm %= modulus
        left[sm].append(e)
    cnt = 0
    sols = []
    for e in itertools.product((-1, 0, 1), repeat=L - h):
        sm = sum(a * b for a, b in zip(e, coeffs[h:]))
        key = (-sm) % modulus if modulus else -sm
        lst = left.get(key)
        if lst:
            cnt += len(lst)
            if len(sols) < keep:
                for e1 in lst:
                    if len(sols) < keep:
                        sols.append(tuple(e1) + tuple(e))
    return cnt, sols


def main():
    DMAX, DMAX3 = int(sys.argv[1]), int(sys.argv[2])
    fails = 0
    # proof inequalities
    for ks in range(2, 61):
        tail = sum(Fr(1, math.factorial(k)) for k in range(ks + 1, ks + 80))
        bound = Fr(1, math.factorial(ks + 1)) * Fr(ks + 2, ks + 1)
        if not (tail <= bound + Fr(1, 10 ** 100) and bound < Fr(1, math.factorial(ks))):
            print("PROOF-INEQ FAIL", ks)
            fails += 1
    print("proof inequalities (k*=2..60): tail<=bound<1/k*!  checked; fails so far", fails)

    for d in range(1, DMAX + 1):
        f = math.factorial(d - 1)
        c1 = [f // math.factorial(k) for k in range(d)]                     # eps_k form
        c2 = [(-1) ** i * (f // math.factorial(d - 1 - i)) for i in range(d)]  # delta_i form (A_0)
        n1, s1 = mitm_solutions(c1)
        n2, s2 = mitm_solutions(c2)
        exp1 = {tuple([0] * d)}
        exp2 = {tuple([0] * d)}
        if d >= 2:
            exp1 |= {tuple([1, -1] + [0] * (d - 2)), tuple([-1, 1] + [0] * (d - 2))}
            exp2 |= {tuple([0] * (d - 2) + [1, 1]), tuple([0] * (d - 2) + [-1, -1])}
        ok1 = (n1 == len(exp1) and set(s1) == exp1)
        ok2 = (n2 == len(exp2) and set(s2) == exp2)
        if not (ok1 and ok2):
            fails += 1
        print(f"d={d:2d}: 3^d={3**d}  eps-form solutions={n1} {'OK' if ok1 else 'FAIL '+str(s1)}; "
              f"A0-form solutions={n2} {'OK' if ok2 else 'FAIL '+str(s2)}", flush=True)

    print("\n# sharpness of p^s > e(d-1)!: least s with only the trivial solutions of A_0 == 0 mod p^s")
    for p in (3, 5, 7):
        for d in range(2, DMAX3 + 1):
            f = math.factorial(d - 1)
            c2 = [(-1) ** i * (f // math.factorial(d - 1 - i)) for i in range(d)]
            s_hyp = next(s for s in range(1, 200) if hyp_deep(p, s, d))
            row = []
            s_min_triv = None
            for s in range(1, s_hyp + 1):
                n, _ = mitm_solutions(c2, modulus=p ** s, keep=0)
                row.append(f"s={s}:{n}")
                if n == 3 and s_min_triv is None:
                    s_min_triv = s
                if s == s_hyp and n != 3:
                    fails += 1
                    row.append("FAIL(hyp holds but extra solutions)")
            print(f"p={p} d={d:2d}: s_hyp={s_hyp} least s with 3 solutions={s_min_triv}  [{' '.join(row)}]",
                  flush=True)
    print(f"RESULT lemmaB2a: failures {fails}")


if __name__ == "__main__":
    main()
