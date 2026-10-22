"""Supplement to test (1): M4C's deterministic phase on A = p^3 Z_p.

Usage: python3 rl2_p1.py p KMAX

  * recomputes the greedy phase-1 schedule from (6.1) alone
    (b_0 = 3, b_1 = 4, b_{k+1} = largest b <= p^2 - 1 with
     V(b) - V(b_{k-1}) <= V(b_{k-1}) - Mx(b) and Mx(b) < V(b_{k-1}),
     d_j = 1 + v_p(j));
  * checks at random x in p^3 Z_p that V_{bp}(x) = V(b), M_{bp}(x) = Mx(b)
    (Lemma 5.1) and that the linear-regime condition of C3 holds;
  * for k <= KMAX computes eps_k(x) = p^K Coll_K - p^D Coll_D of the composite
    [b_{k-1} p, b_{k+1} p) EXACTLY and compares it with the pointwise
    threshold q_1^{n_1} q_2^{n_2} - 1 of Proposition P1 (q_s exact).
"""
import sys
import random
from fractions import Fraction
from rl2_lib import v_p, Vn, Mn, eps_coll
from rl2_lemmaq import q_dp


def main():
    p, kmax = int(sys.argv[1]), int(sys.argv[2])
    d = lambda j: 1 + v_p(j, p)
    V = lambda b: sum(d(j) for j in range(1, b + 1))
    Mx = lambda b: max(d(j) for j in range(1, b + 1))
    b = [3, 4]
    while True:
        cand = [c for c in range(b[-1] + 1, p * p)
                if V(c) - V(b[-2]) <= V(b[-2]) - Mx(c) and Mx(c) < V(b[-2])]
        if not cand:
            break
        b.append(max(cand))
    print(f"p={p}: greedy phase-1 schedule b = {tuple(b)}  (k_0 = {len(b) - 2})")
    q1, q2 = q_dp(p, 1), q_dp(p, 2)
    rng = random.Random(p)
    ok = True
    for _ in range(3):
        x = p ** 3 * rng.randrange(1, p ** 10)
        for bb in b:
            ok &= Vn(x, bb * p, p) == V(bb) and Mn(x, bb * p, p) == Mx(bb)
        for k in range(1, len(b) - 1):
            m_prev = V(b[k - 1]); K = V(b[k + 1]) - m_prev; M = Mx(b[k + 1])
            ok &= K <= m_prev - M and M < m_prev
    print(f"  Lemma 5.1 valuations and linear regime on the schedule at 3 random x: {ok}")
    for k in range(1, min(kmax, len(b) - 2) + 1):
        n1 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if d(j) == 1)
        n2 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if d(j) == 2)
        thr = q1 ** n1 * q2 ** n2 - 1
        worst = Fraction(0)
        for _ in range(2):
            x = p ** 3 * rng.randrange(1, p ** 10)
            e, D, K = eps_coll(x, b[k - 1] * p, b[k] * p, b[k + 1] * p, p)
            worst = max(worst, e)
            ok &= e <= thr
        print(f"  k={k}: composite blocks ({b[k-1]},{b[k+1]}] D={D} K={K} n1={n1} n2={n2}: "
              f"max eps_k = {float(worst):.6g} <= threshold {float(thr):.6g}: {worst <= thr}")
    print("RESULT:", "PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
