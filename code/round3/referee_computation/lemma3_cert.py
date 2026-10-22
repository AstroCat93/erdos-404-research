#!/usr/bin/env python3
"""Round-3 computational referee: independent exhaustive re-run of R3Q Lemma 3 (note Lemma 11.5).

Method (shares no code with R3Q or its checker):
  * S_e(x) = sum_{j<n0} e_j pi_j(x), pi_j(x) = prod_{i=1}^j (x+i), evaluated at an INTEGER
    representative x of each residue class, in exact integers.
  * The derivative is never formed symbolically: for an integer polynomial S and h = 2^H,
    (S(x+h) - S(x))/h = S'(x) + h*S^[2](x) + h^2*S^[3](x) + ...  ==  S'(x)  (mod 2^H),
    so v(S'(x)) is read off this divided difference whenever it is < H (we use H = 40).
  * Each residue class is tested at two different integer representatives (r and r + 2^c * 7919),
    which must give the same verdicts (the reduction says S mod 2^c and S' mod 2^(lam+1)
    depend only on x mod 2^c).
Finite checks (from R3Q.md Lemma 3):
  (a) x = 0 mod 8,   x mod 2^4,  n0 = 6:  2^4  | S  =>  v(S') = 1
  (b) x = 2 mod 16,  x mod 2^7,  n0 = 8:  2^7  | S  =>  v(S') = 3
  (c) x = 6 mod 16,  x mod 2^11, n0 = 10: 2^11 | S  =>  v(S') = 3
  (d) x = 10 mod 16, x mod 2^7,  n0 = 6:  no word has 2^7 | S
  (e) x = 4 mod 8,   x mod 2^4,  n0 = 4:  no word has 2^4 | S
Second part (consequence test, not part of the certificate): for random 2-adic x in each class
(random 64-bit integer representatives), enumerate ALL paths alive at every n <= NMAX by
exhaustive DFS, and check the slope claims (i)-(iii) at every n >= n0 and the bounds (iv)
g_2 <= 6 on 10+16Z, g_2 <= 3 on 4+8Z via the truncation criterion.
"""
import sys, itertools, random, time

H = 40


def v2(x):
    if x == 0:
        return 10 ** 9
    return (x & -x).bit_length() - 1


def pis(x, n):
    out, p = [], 1
    for j in range(n):
        out.append(p)          # pi_j(x)
        p *= (x + j + 1)
    return out


def check(name, res, mod, c, n0, lam, rep_shift):
    """Return (#qualifying (x,e) pairs, #violations) over residues res mod 2^c."""
    qual = viol = 0
    for r in range(1 << c):
        if r % res[1] != res[0]:
            continue
        x = r + rep_shift
        P0, P1 = pis(x, n0), pis(x + (1 << H), n0)
        for bits in itertools.product((0, 1), repeat=n0 - 1):
            e = (1,) + bits
            s0 = sum(p for p, b in zip(P0, e) if b)
            if s0 % (1 << c):
                continue
            qual += 1
            if lam is None:
                viol += 1
                continue
            s1 = sum(p for p, b in zip(P1, e) if b)
            dd = (s1 - s0) >> H
            assert (s1 - s0) % (1 << H) == 0
            if v2(dd % (1 << H)) != lam:
                viol += 1
    return qual, viol


def consequence_test(rng, nsamp, NMAX):
    """Exhaustive DFS of alive paths for random x; returns failure count."""
    classes = [("C0", 0, 8, 6, 1), ("C2", 2, 16, 8, 3), ("C6", 6, 16, 10, 3)]
    fails = 0
    stats = {}
    for name, r, m, n0, lam in classes:
        cnt = 0
        for _ in range(nsamp):
            x = r + m * rng.getrandbits(60)
            P = pis(x, NMAX + 1)
            Vn = [v2(p) if p else 0 for p in P]   # V_n = v(pi_n)
            # derivative of pi_j via divided difference at h = 2^H
            P1 = pis(x + (1 << H), NMAX + 1)
            D = [((b - a) >> H) % (1 << H) for a, b in zip(P, P1)]
            # DFS over prefixes: state (n, S, Sprime_mod)
            stack = [(1, P[0], D[0])]
            while stack:
                n, S, Sd = stack.pop()
                if n >= n0:
                    cnt += 1
                    if v2(Sd) != lam:
                        fails += 1
                if n == NMAX:
                    continue
                for b in (0, 1):
                    S2 = S + b * P[n]
                    Sd2 = (Sd + b * D[n]) % (1 << H)
                    if v2(S2) >= Vn[n + 1]:
                        stack.append((n + 1, S2, Sd2))
        stats[name] = cnt
    # (iv): g_2 <= 6 on 10+16Z: no word of length N (any N <= NMAX) with v(S) >= min(7, V_N);
    #       g_2 <= 3 on 4+8Z:  no word with v(S) >= min(4, V_N)
    for name, r, m, G in (("10+16Z", 10, 16, 7), ("4+8Z", 4, 8, 4)):
        bad = 0
        for _ in range(nsamp):
            x = r + m * rng.getrandbits(60)
            P = pis(x, NMAX + 1)
            for N in range(1, NMAX + 1):
                thr = min(G, v2(P[N]))
                if thr < G:
                    continue           # criterion only bites once V_N >= G
                for bits in itertools.product((0, 1), repeat=N - 1):
                    s = P[0] + sum(p for p, b in zip(P[1:N], bits) if b)
                    if v2(s) >= G:
                        bad += 1
                break
        stats[name] = bad
        fails += bad
    return fails, stats


def main():
    t0 = time.time()
    checks = [("(a) x=0 mod 8 ", (0, 8), 4, 6, 1),
              ("(b) x=2 mod 16", (2, 16), 7, 8, 3),
              ("(c) x=6 mod 16", (6, 16), 11, 10, 3),
              ("(d) x=10 mod 16", (10, 16), 7, 6, None),
              ("(e) x=4 mod 8 ", (4, 8), 4, 4, None)]
    total_viol = 0
    for name, res, c, n0, lam in checks:
        out = []
        for shift in (0, (1 << c) * 7919):
            out.append(check(name, res, None, c, n0, lam, shift))
        q, vv = out[0]
        same = out[0] == out[1]
        total_viol += vv + (0 if same else 1)
        print("%s  modulus 2^%d, n0=%d: qualifying (x,e) pairs=%d violations=%d  second representative agrees=%s"
              % (name, c, n0, q, vv, same))
    print("CERTIFICATE", "PASS" if total_viol == 0 else "FAIL")
    rng = random.Random(11)
    fails, stats = consequence_test(rng, 200, 24)
    print("consequence test (200 random x per class, all alive paths to n=24):", stats, "failures", fails)
    print("time %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
