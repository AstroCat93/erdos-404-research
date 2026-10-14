#!/usr/bin/env python3
"""b2_gate_split_check.py -- exact test of Proposition B2 (gate splitting of the fine-scale mass).

For a composite window [n,N') = [n,N) u [N,N') and a split point n+d (1 <= d <= N-n), with
g = V_{n+d} - V_n, pre-sum A = sum_{n<=j<n+d} delta_j y_j, post signed law B' of the window
[n+d, N') (elements pi_j/pi_{n+d}), rho'_k(r) = p^k P(B' == r mod p^k), u = y_{n+d}/p^g:

  (B2.1)  eps(W,W') = p^g sum_{a mod p^K, p^g | a} P(A == a mod p^K) [rho'_{K-g}(r_a) - rho'_{D-g}(r_a)],
          r_a = -(a/p^g) u^{-1};
  (B2.2)  rho'_{K-g}(0) - rho'_{D-g}(0) = eps_post := eps([n+d,N),[N,N'))  (computed independently);
  (B2.3)  |rho'_{K-g}(r) - rho'_{D-g}(r)| <= eps_post for every r;
  (B2.4)  eps <= p^g Coll^pre_g eps_post,  Coll^pre_g = P(A == 0 mod p^g);
  (B2.5)  |eps - p^g P(A == 0 mod p^K) eps_post| <= p^g (Coll^pre_g - P(A == 0 mod p^K)) eps_post.
All quantities are exact rationals.  Mode 'rand': x Haar-random; mode 'gate': v(x+n+dg) = s forced.
usage: [NEG=1] b2_gate_split_check.py p SEED NX n H H2 KMAX [gate dg s]   (NEG=1: negative control)
"""
import os
import random
import sys
from fractions import Fraction

NEG = os.environ.get('NEG') == '1'

from m4b_lib import Ctx, valuations, window_elems, signed_dist, fold, eps_composite, forced_gate_x


def check_one(C, x, n, N, N2, KMAX, dlist=None):
    p = C.p
    vals, V = valuations(C, x, N2)
    D, K = V[N] - V[n], V[N2] - V[n]
    if K > KMAX or D < 1:
        return None
    y = window_elems(C, x, n, N2)
    eps = eps_composite(y, p, D, K)
    fails = 0
    nsplit = 0
    ratios = []
    for d in (dlist or range(1, N - n + 1)):
        if d > N - n:
            continue
        g = V[n + d] - V[n]
        pre = y[:d]
        post = window_elems(C, x, n + d, N2)          # pi_j/pi_{n+d}, n+d <= j < N2
        Lpre, Lpost = len(pre), len(post)
        # pre signed law mod p^K
        wpre = signed_dist(pre, p ** K)
        # post signed law mod p^{K-g}
        Kg, Dg = K - g, D - g
        wpost = signed_dist(post, p ** Kg)
        wpostD = fold(wpost, p ** Dg)
        u = (y[d] // p ** g) if d < len(y) else None
        assert u is not None and u % p and y[d] % p ** g == 0 and (y[d] // p ** g) % p
        uinv = pow(u, -1, p ** Kg) if Kg > 0 else 0
        if NEG:
            uinv = 1  # negative control: drop the unit u (identity should then fail when u != 1)
        T4pre, T4post = 4 ** Lpre, 4 ** Lpost

        def rho(k, r):
            if k == 0:
                return Fraction(1)
            if k == Kg:
                return Fraction(p ** k * int(wpost[r % p ** k]), T4post)
            return Fraction(p ** k * int(wpostD[r % p ** k]), T4post)

        rhs = Fraction(0)
        coll_g = Fraction(0)
        maxdelta = Fraction(0)
        for a in range(0, p ** K, p ** g):
            w = int(wpre[a])
            if w == 0:
                continue
            coll_g += Fraction(w, T4pre)
            ra = (-(a // p ** g) * uinv) % (p ** Kg) if Kg > 0 else 0
            delta = rho(Kg, ra) - rho(Dg, ra)
            maxdelta = max(maxdelta, abs(delta))
            rhs += Fraction(w, T4pre) * delta
        rhs *= p ** g
        eps_post_direct = eps_composite(post, p, Dg, Kg)
        eps_post_rho = rho(Kg, 0) - rho(Dg, 0)
        P0K = Fraction(int(wpre[0]), T4pre)
        ok1 = (rhs == eps)
        ok2 = (eps_post_direct == eps_post_rho)
        ok3 = (maxdelta <= eps_post_direct)
        ok4 = (eps <= p ** g * coll_g * eps_post_direct)
        ok5 = (abs(eps - p ** g * P0K * eps_post_direct) <= p ** g * (coll_g - P0K) * eps_post_direct)
        nsplit += 1
        if not (ok1 and ok2 and ok3 and ok4 and ok5):
            fails += 1
            print(f"MISMATCH x={x % p**12} d={d} g={g} ok={ok1,ok2,ok3,ok4,ok5} eps={float(eps)} rhs={float(rhs)}")
        if eps_post_direct > 0:
            main = Fraction(p ** g, 2 ** d) * eps_post_direct
            ratios.append((d, g, vals[n + d], float(eps / main) if main else None,
                           float(P0K * 2 ** d), float(coll_g * 2 ** d)))
    return D, K, eps, nsplit, fails, ratios


def main():
    p, seed, NX, n, H, H2, KMAX = (int(a) for a in sys.argv[1:8])
    mode = sys.argv[8] if len(sys.argv) > 8 else 'rand'
    C = Ctx(p)
    rnd = random.Random(seed)
    N, N2 = n + H, n + H + H2
    done = tot_split = tot_fail = 0
    tries = 0
    while done < NX and tries < 20000:
        tries += 1
        if mode == 'gate':
            dg, s = int(sys.argv[9]), int(sys.argv[10])
            x = forced_gate_x(C, rnd, n + dg, s)
            dlist = [dg] + [d for d in (1, 2, 3, H) if d != dg]
        else:
            x = rnd.randrange(C.mod)
            dlist = None
        r = check_one(C, x, n, N, N2, KMAX, dlist)
        if r is None:
            continue
        D, K, eps, ns, nf, ratios = r
        done += 1
        tot_split += ns
        tot_fail += nf
        rs = "; ".join(f"d={d},g={g},v={vv}: eps/main={q:.4g}, 2^d P(A=0 mod p^K)={a:.4g}, 2^d Coll_g={b:.4g}"
                       for (d, g, vv, q, a, b) in ratios[:4] if q is not None)
        print(f"  x#{done}: D={D} K={K} eps={float(eps):.5g} splits={ns} fails={nf} | {rs}", flush=True)
    print(f"RESULT p={p} n={n} H={H} H2={H2} mode={mode} {' '.join(sys.argv[9:])}: "
          f"{done} samples, {tot_split} (sample,split) pairs, (B2.1)-(B2.5) failures: {tot_fail}")


if __name__ == "__main__":
    main()
