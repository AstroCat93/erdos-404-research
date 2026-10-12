#!/usr/bin/env python3
"""Driver: uniform Cov(p,t,H) over all unit classes (lift parameter chosen != 0 so that the
representatives differ from those used by programs A/B), and minimality scans.
usage: scan.py holds p t H [lift]        -> full uniform check, prints summary
       scan.py minimal p t Hmax          -> for every H < Hmax: refute Cov(p,t,H) by counting or
                                            by finding a failing class (stop at first)"""
import subprocess, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
def leg(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s
def choose_k(p, t, H):
    c = leg(H - 1, p); M = t + c
    best = None
    for k in range(0, M + 1):
        vals = [leg(H - 1, p) - leg(H - 1 - i, p) for i in range(H)]
        nlo = sum(1 for v in vals if v < k); nhi = H - nlo
        F = p ** (M - k)
        if F > 2 ** 33 or nlo > 34:
            continue
        cost = 2.0 ** nlo * 3 + nhi * p ** M / 64.0 + p ** k * 2.0 ** max(0, nlo - 22)
        if best is None or cost < best[0]:
            best = (cost, k)
    return best[1]
def run(args, env=None):
    e = dict(os.environ); e.update(env or {})
    return subprocess.run([os.path.join(HERE, 'covchk')] + [str(a) for a in args], capture_output=True, text=True, env=e).stdout
mode = sys.argv[1]
p, t = int(sys.argv[2]), int(sys.argv[3])
if mode == 'holds':
    H = int(sys.argv[4]); lift = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    k = choose_k(p, t, H)
    out = run([p, t, H, k, 'cls', lift])
    print(out.strip().splitlines()[0]); print(out.strip().splitlines()[-1])
    bad = [l for l in out.splitlines() if 'UNCOVERED' in l and l.startswith('C ')]
    for l in bad[:5]:
        print('  ', l)
elif mode == 'minimal':
    Hmax = int(sys.argv[4])
    for H in range(1, Hmax):
        if H > p ** t:
            break
        c = leg(H - 1, p); M = t + c
        if 2 ** H < p ** M:
            print(f"H={H}: fails by counting (2^{H} < {p}^{M})"); continue
        k = choose_k(p, t, H)
        out = run([p, t, H, k, 'cls', 1], {'STOPFIRST': '1', 'STOPFIBRE': '1'})
        bad = [l for l in out.splitlines() if l.startswith('C ') and 'UNCOVERED' in l]
        if bad:
            f = dict(x.split('=') for x in bad[0].split() if '=' in x)
            print(f"H={H}: fails (class K'={f['Kmodpc']}, rho=(H-1) mod p={(H-1) % p})")
        else:
            print(f"H={H}: HOLDS over all classes  (rho={(H-1) % p})  <-- contradicts minimality if H < claimed H_t")
    sys.stdout.flush()
