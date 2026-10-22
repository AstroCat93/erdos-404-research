#!/usr/bin/env python3
"""Round-3 computational referee: independent recomputation of R3F's single-gate-block shells
(note Theorem 11.17 = R3F Theorem A2, Theorem 11.19 = R3F Theorem A5, Lemma 11.16 = R3F Lemma A1).

Part 1 (A5 table entries).  sigma_i = (-1)^i (p-1)!/(p-1-i)!, i < p.
   S_d(p) = sum_{u in (Z/p^d)^x} prod_i |cos(pi * (u*sigma_i mod p^d) / p^d)|,
   rho_d  = S_d / (N_d (2/pi)^p),  N_d = p^d - p^(d-1).
   Computed with mpmath at 40 significant digits (exact integer phase reduction first), for
   p = 7, d <= 6 and p = 13, d <= 4; and in float64 (numpy, math.fsum per level) for
   p = 7, d <= 8 and p = 13, d <= 6 as an extension.
Part 2 (Lemma A1 spot check).  For actual gate blocks y_i(K') = prod_{s=1}^i (p^t K' - (p-s))
   with t = d_max, several K', the shells at every d <= t equal those of sigma.
Part 3 (A2).  Enumerate all delta in {-1,0,1}^p (p = 7, 11; also 13), list every nonzero delta
   with <delta,sigma> = 0, and evaluate sum_{<delta,sigma>=0} 2^{z(delta)} / 2^p (claimed 3/2).
   Then compute Q_d = sum_{u unit} prod_i cos^2(pi u sigma_i / p^d) DIRECTLY (float64) at levels
   in the archimedean regime p^(d-1) > R_p = floor(e (p-1)!) and compare Q_d / (N_d 2^-p) with 3/2:
   p = 7, d = 5, 6, 7;  p = 11, d = 8 (11^8 = 214358881 points, chunked).
"""
import sys, time, math, itertools
import numpy as np
import mpmath as mp

mp.mp.dps = 40


def sigma(p):
    f = math.factorial(p - 1)
    return [(-1) ** i * (f // math.factorial(p - 1 - i)) for i in range(p)]


def shell_mp(p, d, ys):
    M = p ** d
    tot = mp.mpf(0)
    pim = mp.pi / M
    for u in range(1, M):
        if u % p == 0:
            continue
        prod = mp.mpf(1)
        for y in ys:
            r = (u * y) % M
            prod *= abs(mp.cos(pim * r))
        tot += prod
    return tot


def shell_np(p, d, ys, sq=False, chunk=1 << 22):
    M = p ** d
    parts = []
    ysm = np.array([y % M for y in ys], dtype=np.int64)
    for lo in range(0, M, chunk):
        u = np.arange(lo, min(M, lo + chunk), dtype=np.int64)
        u = u[u % p != 0]
        prod = np.ones(u.shape, dtype=np.float64)
        for y in ysm:
            r = (u * y) % M            # u*y < 2^63 for all sizes used here
            c = np.cos(np.pi * (r.astype(np.float64) / M))
            prod *= (c * c) if sq else np.abs(c)
        parts.append(math.fsum(prod.tolist()) if prod.size < 5_000_000 else float(np.sum(prod, dtype=np.float64)))
    return math.fsum(parts)


def gate_block(p, t, Kp):
    return [math.prod((p ** t * Kp - (p - s)) for s in range(1, i + 1)) for i in range(p)]


def main():
    t0 = time.time()
    claimed = {7: [0.7989, 0.6276, 1.1733, 1.1760, 1.1699, 1.1705, 1.1705, 1.1705],
               13: [0.2303, 1.1272, 1.0157, 1.2064, 1.1703, 1.1729]}
    print("Part 1: rho_d of a single gate block (claimed values: R3F Theorem A5 table, rounded up in the 4th decimal)")
    res = {}
    for p, dmp, dnp in ((7, 6, 8), (13, 4, 6)):
        sg = sigma(p)
        print(" p=%d sigma=%s" % (p, sg))
        for d in range(1, dnp + 1):
            Nd = p ** d - p ** (d - 1)
            denom = Nd * (2 / math.pi) ** p
            snp = shell_np(p, d, sg)
            line = "  d=%d  S_d(float64)=%.12g rho=%.7f" % (d, snp, snp / denom)
            if d <= dmp:
                smp = shell_mp(p, d, sg)
                rmp = smp / (Nd * (2 / mp.pi) ** p)
                res[(p, d)] = rmp
                line += "  | S_d(mpmath)=%s rho=%s" % (mp.nstr(smp, 15), mp.nstr(rmp, 12))
                rho = float(rmp)
            else:
                rho = snp / denom
            cl = claimed[p][d - 1]
            ok = (cl >= rho - 1e-12) and (cl - rho < 1e-4 + 1e-12)
            line += "  claimed<=%.4f %s" % (cl, "consistent" if ok else "MISMATCH")
            print(line, flush=True)

    print("Part 2: Lemma A1 spot check (actual gate blocks, shells at d <= t equal sigma's)")
    for p, t, Ks in ((7, 6, (1, 3, 5, 12)), (13, 4, (1, 2, 7))):
        sg = sigma(p)
        worst = 0.0
        for Kp in Ks:
            y = gate_block(p, t, Kp)
            for d in range(1, t + 1):
                assert all((a - b) % p ** d == 0 for a, b in zip(y, sg))
                a1, b1 = shell_np(p, d, y), shell_np(p, d, sg)
                worst = max(worst, abs(a1 - b1) / b1)
        print("  p=%d t=%d K' in %s: y_i = sigma_i mod p^d for all d<=t; max relative shell difference %.2e" % (p, t, Ks, worst))

    print("Part 3: Theorem A2")
    for p in (7, 11, 13):
        sg = sigma(p)
        Rp = sum(abs(s) for s in sg)
        rel, wsum = [], 0
        for dl in itertools.product((-1, 0, 1), repeat=p):
            if sum(a * b for a, b in zip(dl, sg)) == 0:
                wsum += 2 ** dl.count(0)
                if any(dl):
                    rel.append(dl)
        print("  p=%d R_p=%d (floor(e(p-1)!)=%d): nonzero relations %s ; sum 2^z / 2^p = %s"
              % (p, Rp, math.floor(math.e * math.factorial(p - 1)), rel, str(wsum / 2 ** p)), flush=True)
    for p, ds in ((7, (4, 5, 6, 7)), (11, (8,))):
        sg = sigma(p)
        Rp = sum(abs(s) for s in sg)
        for d in ds:
            Nd = p ** d - p ** (d - 1)
            q = shell_np(p, d, sg, sq=True)
            print("  p=%d d=%d (p^(d-1)=%d %s R_p=%d): Q_d/(N_d 2^-p) = %.12f  (Theorem A2(iii): = 3/2 whenever p^(d-1) > R_p)"
                  % (p, d, p ** (d - 1), ">" if p ** (d - 1) > Rp else "<=", Rp, q / (Nd * 2.0 ** -p)), flush=True)
    print("time %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
