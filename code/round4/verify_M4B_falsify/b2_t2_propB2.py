"""b2_t2_propB2.py -- exact test of M4B Proposition B2 (gate splitting), on which Cor B2' rests.

For random composite windows [n,N) u [N,N') and random cylinders x (Haar, and x close to -k,
including n = 0 with x close to -1, -2), at p = 3, 5, 7, and for EVERY split point n+d,
1 <= d <= N-n, it checks exactly (Fractions / Python ints):
  (E)    eps computed three ways: signed collisions by meet in the middle (b2_lib.eps), signed
         collisions from a full numpy law, and the R3M definition sum_r nu_k(r)^2 with nu the
         uniform subset-sum law (unsigned digits);
  (B2.1) eps = p^g sum_{a in p^g Z_p} P(A=a) Delta(r_a),  r_a = -(a/p^g) u^{-1};
  (B2.2) Delta(0) = eps^post := eps([n+d,N),[N,N'))  (computed independently, from scratch);
  (B2.3) |Delta(r)| <= Delta(0) and Delta(-r) = Delta(r) for ALL r mod p^{K-g};
  (B2.4) eps <= p^g Coll^pre_g eps^post;
  (B2.5) |eps - p^g P(A==0 mod p^K) eps^post| <= p^g (Coll^pre_g - P(A==0 mod p^K)) eps^post.
Negative control: (B2.1) with u^{-1} replaced by 1.
usage: b2_t2_propB2.py SEED NSAMPLES
"""
import random
import sys
from fractions import Fraction as Fr

import numpy as np

from b2_lib import PREC, Vrel, elems, eps, rand_unit, signed_array, coll_unsigned, vx

CAP = {3: 3 ** 11, 5: 5 ** 7, 7: 7 ** 6}


def fold(arr, mod):
    """counts mod `mod` from counts mod len(arr) (mod | len(arr))."""
    if mod == 1:
        return np.array([arr.sum()], dtype=object)
    return arr.reshape(-1, mod).sum(axis=0)


def sample(rnd):
    p = rnd.choice((3, 5, 7))
    n = rnd.choice([0, 0, 1, 2] + list(range(3, 41)))
    L1 = rnd.randint(1, 13)
    L2 = rnd.randint(1, 13)
    N, Np = n + L1, n + L1 + L2
    kind = rnd.random()
    if kind < 0.55:
        x = rnd.randrange(p ** PREC)
        tag = "haar"
    else:
        k = rnd.randint(1, Np + 3)
        s = rnd.randint(1, 4)
        x = (-k + p ** s * rand_unit(p, rnd, PREC - s - 5)) % p ** PREC
        tag = f"x~-{k}(s={s})"
    return p, n, N, Np, x, tag


def main():
    seed, NS = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    stats = dict(samples=0, pairs=0, fail=0, neg_differs=0, neg_pairs=0, eps_pos=0, unsigned_checked=0)
    tried = 0
    khist = {}
    while stats["samples"] < NS:
        tried += 1
        p, n, N, Np, x, tag = sample(rnd)
        D = Vrel(x, n, N, p)
        K = Vrel(x, n, Np, p)
        if p ** K > CAP[p] or Np - n > 26:
            continue
        ys = elems(x, n, Np)
        m = len(ys)
        e_mitm, _, _ = eps(x, n, N, Np, p)
        arr = signed_array(ys, p ** K)
        e_np = Fr(p ** K * int(arr[0::p ** K].sum()) - p ** D * int(arr[0::p ** D].sum()), 4 ** m)
        bad = []
        if e_np != e_mitm:
            bad.append("eps mitm!=np")
        if stats["samples"] % 4 == 0 and m <= 26:
            e_uns = p ** K * coll_unsigned(ys, p, K, K) - p ** D * coll_unsigned(ys, p, D, K)
            stats["unsigned_checked"] += 1
            if e_uns != e_mitm:
                bad.append("eps unsigned(R3M def)!=signed")
        if e_mitm < 0:
            bad.append("eps<0")
        if e_mitm > 0:
            stats["eps_pos"] += 1
        for d in range(1, N - n + 1):
            g = Vrel(x, n, n + d, p)
            pre = ys[:d]
            pre_arr = signed_array(pre, p ** K)          # law of A mod p^K, total 4^d
            post = elems(x, n + d, Np)                     # z_j = pi_j/pi_{n+d}, n+d <= j < N'
            mp = len(post)
            Kg, Dg = K - g, D - g
            assert Kg == Vrel(x, n + d, Np, p) and Dg == Vrel(x, n + d, N, p)
            post_arr = signed_array(post, p ** Kg).astype(object)   # total 4^mp
            fD = fold(post_arr, p ** Dg)
            # Delta(r) * 4^mp, for all r mod p^Kg
            idx = np.arange(p ** Kg) % (p ** Dg)
            Dl = post_arr * (p ** Kg) - fD[idx] * (p ** Dg)
            eps_post_direct, _, _ = eps(x, n + d, N, Np, p)
            Delta0 = Fr(int(Dl[0]), 4 ** mp)
            u = ys[d] // p ** g
            assert ys[d] % p ** g == 0 and u % p != 0
            modKg = p ** Kg
            uinv = pow(u, -1, modKg) if Kg > 0 else 0
            rhs = 0
            rhs_neg = 0
            for a in range(0, p ** K, p ** g):
                c = int(pre_arr[a])
                if c:
                    ra = (-(a // p ** g) * uinv) % modKg if Kg > 0 else 0
                    rn = (-(a // p ** g)) % modKg if Kg > 0 else 0
                    rhs += c * int(Dl[ra])
                    rhs_neg += c * int(Dl[rn])
            rhs = Fr(p ** g * rhs, 4 ** d * 4 ** mp)
            rhs_neg = Fr(p ** g * rhs_neg, 4 ** d * 4 ** mp)
            if rhs != e_mitm:
                bad.append(f"B2.1 d={d}")
            if Delta0 != eps_post_direct:
                bad.append(f"B2.2 d={d}")
            Dabs = np.abs(Dl)
            if int(Dabs.max()) > int(Dl[0]):
                bad.append(f"B2.3 bound d={d}")
            neg_idx = (-np.arange(p ** Kg)) % (p ** Kg)
            if not np.array_equal(Dl, Dl[neg_idx]):
                bad.append(f"B2.3 even d={d}")
            coll_pre = Fr(int(pre_arr[0::p ** g].sum()), 4 ** d)
            pK = Fr(int(pre_arr[0]), 4 ** d)
            if e_mitm > p ** g * coll_pre * eps_post_direct:
                bad.append(f"B2.4 d={d}")
            if abs(e_mitm - p ** g * pK * eps_post_direct) > p ** g * (coll_pre - pK) * eps_post_direct:
                bad.append(f"B2.5 d={d}")
            stats["pairs"] += 1
            if u % modKg != 1 % modKg if Kg > 0 else False:
                stats["neg_pairs"] += 1
                if rhs_neg != e_mitm:
                    stats["neg_differs"] += 1
        stats["samples"] += 1
        khist[(p, K)] = khist.get((p, K), 0) + 1
        if bad:
            stats["fail"] += 1
            print(f"FAIL p={p} n={n} N={N} N'={Np} {tag} x={x % p**30} D={D} K={K}: {bad}", flush=True)
        if stats["samples"] % 25 == 0:
            print(f"progress: samples {stats['samples']} (tried {tried}) pairs {stats['pairs']} "
                  f"failures {stats['fail']} eps>0 in {stats['eps_pos']}", flush=True)
    print("histogram of (p,K):", dict(sorted(khist.items())))
    print("RESULT propB2:", stats)


if __name__ == "__main__":
    main()
