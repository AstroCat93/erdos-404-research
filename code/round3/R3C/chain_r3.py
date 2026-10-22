#!/usr/bin/env python3
"""chain_r3.py (round 3, track R3C) -- check the first-failure chain (note.md Proposition 10.10 and
its "first non-excluded multiple" form below) from covering logs, requiring EVERY listed program for
EVERY certificate.  Written from scratch in round 3 (independent of round-2 chain.py / chain_c.py).

Log formats parsed (one line per position/class; only exact COVERED lines with missing 0 count):
  A  fibcov   "A p=.. t=.. H=.. c=.. M=.. K=.. missing=0 COVERED"
  B  fibcov2  "B p=.. t=.. H=.. M=.. K=.. notcovered=0 OK"
  C  covchk   "C p=.. t=.. H=.. M=.. K=.. Kmodpc=.. miss=0 COVERED"   (lines marked '+(partial)' ignored)
  D  covfast  "D p=.. t=.. H=.. c=.. M=.. k=.. K=.. Kmodpc=.. missing=0 COVERED"
Spec file lines:  "p D" (first line), "require A,D", "uniform t H", "pos t H Kmin Kmax".

Argument.  Let N* be the first failure for a = 1 (least N > 1 with not P(1,p,N)); p | N*
(Lemma 1.3(iv)); write N* = p^t K'' with p not | K''.  A depth t is EXCLUDED if a uniform certificate
Cov(p,t,H) (all unit classes K' mod p^c) holds with H + 1 < p^t; then N* - H >= p^t - H > 1 and
Theorem 3.12(a) + Lemma 1.3(iii) give P(1,p,N*-H) => P(1,p,N*), contradicting minimality.  A single
position N* = p^t K'' is excluded by a position certificate with N* - H > 1.  Let N_t = p^t K_t,
K_t the least K'' (p not | K'') that is not excluded at depth t (depths without a uniform
certificate), and N = min(p^D, min_t N_t).  Then N* >= N, so P(1,p,N-1) holds and
f(1,p) >= v_p((N-1)!) (Lemma 1.3(i)).  If N = p^D this is Proposition 10.10's v_p((p^D-1)!).
usage: R3C_LOGS=dir1:dir2 chain_r3.py SPEC
"""
import glob
import os
import re
import sys

PAT = {
    'A': re.compile(r"^A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) (COVERED|NOT_COVERED)"),
    'B': re.compile(r"^B p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) notcovered=(\d+) (OK|FAIL)"),
    'C': re.compile(r"^C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+)(\S*) (COVERED|UNCOVERED)"),
    'D': re.compile(r"^D p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ k=\d+ K=(\d+) Kmodpc=\d+ missing=(\d+) (COVERED|NOT_COVERED)"),
}


def legendre(n, p):
    e = 0
    while n:
        n //= p
        e += n
    return e


def collect(dirs):
    cov = {x: {} for x in PAT}          # prog -> (p,t,H) -> set of K with an exact covered line
    seen = {x: 0 for x in PAT}
    for d in dirs:
        for fn in sorted(glob.glob(os.path.join(d, '*.log'))):
            for line in open(fn, errors='replace'):
                line = line.strip()
                for prog, rx in PAT.items():
                    m = rx.match(line)
                    if not m:
                        continue
                    g = m.groups()
                    p, t, H, K, miss = map(int, g[:5])
                    ok = (miss == 0)
                    if prog == 'C':
                        ok = ok and g[5] == '' and g[6] == 'COVERED'
                    elif prog == 'B':
                        ok = ok and g[5] == 'OK'
                    else:
                        ok = ok and g[5] == 'COVERED'
                    seen[prog] += 1
                    if ok:
                        cov[prog].setdefault((p, t, H), set()).add(K)
    return cov, seen


def uniform_ok(Ks, p, t, H):
    c = legendre(H - 1, p)
    if c == 0:
        return len(Ks) > 0
    pc = p ** c
    need = {K for K in range(1, pc) if K % p}
    return need <= {K % pc for K in Ks}


def main():
    spec = [ln.split() for ln in open(sys.argv[1]) if ln.strip() and not ln.lstrip().startswith('#')]
    dirs = os.environ.get('R3C_LOGS', '.').split(':')
    cov, seen = collect(dirs)
    p, D = int(spec[0][0]), int(spec[0][1])
    req = ['A', 'D']
    uni = {}       # t -> H
    pos = {}       # t -> set of excluded K''
    ok_all = True
    print(f"# chain_r3: p={p} D={D} logs={dirs}")
    print(f"# log lines parsed per program: {seen}")
    for row in spec[1:]:
        if row[0] == 'require':
            req = row[1].split(',')
            print(f"# required programs: {req}")
        elif row[0] == 'uniform':
            t, H = int(row[1]), int(row[2])
            res = {x: uniform_ok(cov[x].get((p, t, H), set()), p, t, H) for x in req}
            cond = H + 1 < p ** t
            print(f"uniform Cov({p},{t},{H}) c={legendre(H-1,p)}: " + ' '.join(f"{x}={res[x]}" for x in req) + f"  H+1<p^t={cond}")
            if all(res.values()) and cond:
                uni[t] = H
            else:
                ok_all = False
        elif row[0] == 'pos':
            t, H, k0, k1 = map(int, row[1:5])
            Ks = [K for K in range(k0, k1 + 1) if K % p]
            good = []
            for K in Ks:
                if all(K in cov[x].get((p, t, H), set()) for x in req) and p ** t * K - H > 1:
                    good.append(K)
            bad = sorted(set(Ks) - set(good))
            print(f"positions depth {t} H={H} K''={k0}..{k1} ({len(Ks)}): certified by all of {req}: {len(good)}"
                  + (f"  NOT certified: {bad[:20]}{' ...' if len(bad) > 20 else ''}" if bad else ''))
            pos.setdefault(t, set()).update(good)
    # first non-excluded multiple of p
    N = p ** D
    for t in range(1, D):
        if t in uni:
            continue
        K = 1
        S = pos.get(t, set())
        while K < p ** (D - t) and (K % p == 0 or K in S):
            K += 1
        if K < p ** (D - t):
            Nt = p ** t * K
            print(f"depth {t}: first non-excluded position K''={K} (N={p}^{t}*{K})")
            N = min(N, Nt)
        else:
            print(f"depth {t}: all {sum(1 for x in range(1, p ** (D - t)) if x % p)} positions below {p}^{D} excluded")
    bound = legendre(N - 1, p)
    if N == p ** D and ok_all:
        print(f"CHAIN OK: no first failure below {p}^{D}; f(1,{p}) >= v_{p}(({p}^{D}-1)!) = {bound}")
    elif N == p ** D:
        print(f"CHAIN OK (some listed certificates failed but were not needed): f(1,{p}) >= v_{p}(({p}^{D}-1)!) = {bound}")
    else:
        print(f"CHAIN PARTIAL: no first failure below N={N}; f(1,{p}) >= v_{p}((N-1)!) = {bound}")


if __name__ == '__main__':
    main()
