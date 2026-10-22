#!/usr/bin/env python3
"""indep.py -- independent checks for the adversarial check of track R3C (round 3, 2026-10-13).
Written from scratch for this check; it imports nothing from code/round2 or code/round3/R3C.

Objects (note.md Theorem 3.12(a)).  For a position N* = p^t K and a block length H let
N1 = N* - H, y_i = (N1+1)(N1+2)...(N1+i) (exact integers, y_0 = 1, 0 <= i < H) and
M = v_p(N*!) - v_p(N1!) (Legendre at the actual position).  The question is whether the 2^H subset
sums of the y_i cover Z/p^M.

Two methods, both without the "fibres by the low k digits" reduction used by programs A, C and D:
  bitcover  -- the reachable set as ONE Python integer of p^M bits; adding y means
               S |= rot(S, y mod p^M).  Exact number of missed residues = p^M - popcount.
               Usable for p^M up to about 6e8.
  mitm      -- decides for ONE residue x whether it is a subset sum: the elements are split in two
               halves, all 2^(H/2) subset sums of each half are enumerated (numpy, exact in int64),
               and x - a (mod p^M) is looked up in the sorted second list.  Exact for any p^M < 2^62.
               With x random it also produces witnesses of covered residues.
usage: python3 indep.py TASK   with TASK in: selftest, scans, lemma, lemma29, negatives, rho0
"""
import random
import sys
import time

import numpy as np


def leg(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def block(p, t, H, K):
    """exact y_i mod p^M at the actual position N* = p^t K; also returns M and the valuations"""
    Ns = p ** t * K
    N1 = Ns - H
    assert N1 >= 0
    M = leg(Ns, p) - leg(N1, p)
    Q = p ** M
    ys, vs = [], []
    prod = 1
    for i in range(H):
        if i:
            prod *= N1 + i
        v = 0
        z = prod
        while z % p == 0:
            z //= p
            v += 1
        ys.append(prod % Q)
        vs.append(v)
    return M, Q, ys, vs


def bitcover(p, t, H, K):
    M, Q, ys, _ = block(p, t, H, K)
    mask = (1 << Q) - 1
    S = 1                                   # the empty sum 0
    for y in ys:
        if y == 0:
            continue
        S = S | (((S << y) | (S >> (Q - y))) & mask)
    return Q - S.bit_count(), M, S


def subset_sums(vals, Q):
    a = np.zeros(1, dtype=np.int64)
    for v in vals:
        a = np.concatenate([a, (a + v) % Q])
    return a


def mitm_prepare(p, t, H, K):
    M, Q, ys, _ = block(p, t, H, K)
    h = len(ys) // 2
    A = subset_sums(ys[:h], Q)
    B = np.sort(subset_sums(ys[h:], Q))
    return M, Q, ys, A, B


def mitm_hit(Q, A, B, x):
    """True iff x is a subset sum (mod Q)"""
    tgt = (x - A) % Q
    idx = np.searchsorted(B, tgt)
    idx[idx == len(B)] = 0
    return bool(np.any(B[idx] == tgt))


def rho0(p):
    e = []
    f = 1
    for u in range(p):
        if u:
            f = f * u % p
        e.append((-1) ** u * pow(f, -1, p) % p)
    for r in range(p):
        S = {0}
        for u in range(r + 1):
            S |= {(s + e[u]) % p for s in S}
        if len(S) == p:
            return r
    return None


def Lp(p, Lmax=6):
    """largest L <= Lmax with Sigma(E_p) mod p^L = Z/p^L (bitset over Z/p^L)"""
    best = 0
    for L in range(1, Lmax + 1):
        Q = p ** L
        if Q > 3 * 10 ** 8:
            break
        f = 1
        S = 1
        mask = (1 << Q) - 1
        for u in range(p):
            if u:
                f = f * u
            y = ((-1) ** u * pow(f, -1, Q)) % Q
            if y:
                S |= ((S << y) | (S >> (Q - y))) & mask
        if S.bit_count() == Q:
            best = L
        else:
            break
    return best


def mitm_set(Q, A, B):
    """boolean array over Z/Q: True where a + b (mod Q) for some a in A, b in B (all residues at once)"""
    hit = np.zeros(Q, dtype=bool)
    step = max(1, (1 << 22) // max(1, len(B)))
    for i in range(0, len(A), step):
        hit[((A[i:i + step, None] + B[None, :]) % Q).ravel()] = True
    return hit


def task_selftest():
    """bitcover against mitm (every residue, vectorised) on small cases, including failing ones"""
    rng = random.Random(20261013)
    n = bad = fails = 0
    for p in (3, 5, 7, 11, 13):
        for t in (1, 2, 3):
            for H in range(2, 2 * p + 3):
                if H > p ** t or H > 26:
                    continue
                c = leg(H - 1, p)
                if p ** (t + c) > 30000:
                    continue
                for K in rng.sample([k for k in range(1, 60) if k % p], 3):
                    miss, M, S = bitcover(p, t, H, K)
                    _, Q, ys, A, B = mitm_prepare(p, t, H, K)
                    hit = mitm_set(Q, A, B)
                    bits = np.array([(S >> x) & 1 for x in range(Q)], dtype=bool)
                    n += 1
                    fails += miss > 0
                    if miss != Q - int(hit.sum()) or not np.array_equal(bits, hit) or M != t + c:
                        bad += 1
                        print("MISMATCH", p, t, H, K, miss, Q - int(hit.sum()), M)
    print(f"selftest: {n} (p,t,H,K) cases, {fails} of them failing; bitcover vs mitm residue by residue: {bad} mismatches")


def task_scans():
    """minimal uniform H_t for t <= 5 at p = 29, 31 (c = 0 there unless H > p): exact miss counts"""
    claim = {29: [7, 13, 19, 24, 29], 31: [7, 14, 19, 25, 30]}
    for p in (29, 31):
        r0 = rho0(p)
        for t in range(1, 6):
            Ht = claim[p][t - 1]
            out = []
            for H in range(2, Ht + 1):
                c = leg(H - 1, p)
                M = t + c
                if 2 ** H < p ** M:
                    continue
                if (H - 1) % p < r0:
                    out.append(f"{H}:L10.11")
                    continue
                K = 5                      # c = 0 here, so the class does not matter (A used K=1, C K=1 or 3, D K=4)
                assert c == 0
                miss, M2, _ = bitcover(p, t, H, K)
                out.append(f"{H}:{miss}")
            print(f"p={p} t={t} claimed H_t={Ht}: H:missed = " + ' '.join(out))


def task_lemma():
    """Lemma R3C.1 for p = 7..23, 2 <= t <= L_p, p^(t+1) <= 7e6, p < H <= 2p, ALL classes K' = 1..p-1"""
    tot = agree = 0
    hold_in = fail_out = 0
    for p in (7, 11, 13, 17, 19, 23):
        r0 = rho0(p)
        L = Lp(p)
        for t in range(2, L + 1):
            if p ** (t + 1) > 7 * 10 ** 6:
                continue
            for H in range(p + 1, 2 * p + 1):
                pred = H >= p + 1 + r0
                res = []
                for Kp in range(1, p):
                    miss, M, _ = bitcover(p, t, H, Kp + 7 * p)     # representative K' + 7p (lift 7)
                    assert M == t + 1
                    res.append(miss == 0)
                obs = all(res)
                uniform = len(set(res)) == 1
                tot += 1
                agree += (obs == pred) and uniform
                hold_in += pred and obs
                fail_out += (not pred) and (not any(res))
                if obs != pred or not uniform:
                    print("LEMMA MISMATCH", p, t, H, res)
        print(f"p={p}: rho0={r0} L_p={L} done", flush=True)
    print(f"lemma: {tot} triples (p,t,H); prediction of Lemma R3C.1 matched, class-independently, in {agree}; "
          f"in range and all classes covered: {hold_in}; below range and NO class covered: {fail_out}")


def task_lemma29():
    """p = 29: Lemma range t = 2..4, H = 30..58 (all 28 classes), and t = 5, H = 36..39 (all classes)"""
    p = 29
    r0 = rho0(p)
    for t in (2, 3, 4):
        bad = []
        for H in range(p + 1, 2 * p + 1):
            pred = H >= p + 1 + r0
            res = [bitcover(p, t, H, Kp + 5 * p)[0] == 0 for Kp in range(1, p)]
            if not (all(res) == pred and len(set(res)) == 1):
                bad.append(H)
        print(f"p=29 t={t} H=30..58, 28 classes each: lemma mismatches {bad}", flush=True)
    for H in (36, 37, 38, 39):
        t0 = time.time()
        miss = [bitcover(p, 5, H, Kp + 5 * p)[0] for Kp in range(1, p)]
        print(f"Cov(29,5,{H}) over the 28 classes K'+5*29: missed counts {sorted(set(miss))} "
              f"-> {'HOLDS' if not any(miss) else 'FAILS'} ({time.time() - t0:.0f}s)", flush=True)


def task_negatives():
    """the listed missed residues of R4 and R6 are NOT subset sums; random residues are"""
    cases = [
        ("R4 (29,6,39) K'=2", 29, 6, 39, 2, [9681558076, 7454824172]),
        ("R4 (31,6,40) K'=2", 31, 6, 40, 2, [25349343487, 3557184957]),
        ("R4 (29,7,44) K''=3", 29, 7, 44, 3, [197789838580, 169097737247]),
        ("R6 (11,7,40) K''=37", 11, 7, 40, 37, [23022655245, 18038488330]),
        ("R6 (7,6,33) K'=5", 7, 6, 33, 5, [241978387, 94559789]),
        ("R6 (13,8,46) K''=1", 13, 8, 46, 1, [781969025359, 35061369029, 404633157615, 290614077358, 660185865944,
                                              1705438603651, 1025677111674, 374671830249, 1291358242475, 892179100205,
                                              219147718723, 1174817272735, 1715757623518, 638848348990, 1578571317867,
                                              739654397667, 1747753231343, 908836311143, 56398885983, 771650005492,
                                              1312590356275, 476099516250, 1595228528805, 320575404724, 1196049386535,
                                              1461730517336]),
    ]
    rng = random.Random(404)
    for name, p, t, H, K, xs in cases:
        t0 = time.time()
        M, Q, ys, A, B = mitm_prepare(p, t, H, K)
        hits = [mitm_hit(Q, A, B, x) for x in xs]
        rnd = [mitm_hit(Q, A, B, rng.randrange(Q)) for _ in range(20)]
        print(f"{name}: M={M} listed residues are subset sums? {hits}; 20 random residues covered: {sum(rnd)}/20 "
              f"({time.time() - t0:.1f}s)", flush=True)


if __name__ == '__main__':
    {'selftest': task_selftest, 'scans': task_scans, 'lemma': task_lemma, 'lemma29': task_lemma29,
     'negatives': task_negatives, 'rho0': lambda: print({p: rho0(p) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)},
                                                         {p: Lp(p) for p in (7, 11, 13, 17, 19, 23, 29, 31)})}[sys.argv[1]]()
