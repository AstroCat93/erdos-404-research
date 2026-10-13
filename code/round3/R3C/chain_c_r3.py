#!/usr/bin/env python3
"""chain_c_r3.py (round 3, track R3C) -- the round-2 computational referee's chain check
(code/round2/review/computation/chain_c.py) with three changes and no change to its logic:
  (1) the plan (p, D, uniform H_t, position H_t) is read from the command line instead of the
      hard-coded `plans` dictionary;
  (2) the log directories come from $R3C_LOGS (colon separated) instead of ./logs;
  (3) the program whose logs are used is selectable (A = fibcov, C = covchk, D = covfast); the chain
      is checked for ONE program at a time, so a two-program certificate is checked by running this
      script once per program.
Logic (unchanged from chain_c.py): every N = p^t K'' < p^D (t >= 1, p not | K'') must be excluded
either by a uniform certificate Cov(p,t,H) over ALL unit classes mod p^c with H+1 < p^t, or by a
position certificate for exactly that K'' with N - H > 1.
usage: chain_c_r3.py PROG p D "t:H,t:H,..." "t:H[:Kexc=Hexc],..."
   e.g. chain_c_r3.py A 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"
"""
import glob
import os
import re
import sys

PATS = {
    'A': re.compile(r"A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) (COVERED|NOT_COVERED)"),
    'C': re.compile(r"C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+)(\S*) (COVERED|UNCOVERED)"),
    'D': re.compile(r"D p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ k=\d+ K=(\d+) Kmodpc=\d+ missing=(\d+) (COVERED|NOT_COVERED)"),
}


def leg(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


prog = sys.argv[1]
p, D = int(sys.argv[2]), int(sys.argv[3])
uni = {int(a): int(b) for a, b in (x.split(':')[:2] for x in sys.argv[4].split(',') if x)}
posH = {}
exc = {}
for x in sys.argv[5].split(','):
    if not x:
        continue
    f = x.split(':')
    posH[int(f[0])] = int(f[1])
    for e in f[2:]:
        K, Hx = e.split('=')
        exc[(int(f[0]), int(K))] = int(Hx)

cov = {}
for d in os.environ.get('R3C_LOGS', '.').split(':'):
    for fn in glob.glob(os.path.join(d, '*.log')):
        for ln in open(fn, errors='replace'):
            m = PATS[prog].match(ln.strip())
            if not m:
                continue
            g = m.groups()
            pp, t, H, K, miss = map(int, g[:5])
            if prog == 'C':
                good = miss == 0 and g[5] == '' and g[6] == 'COVERED'
            else:
                good = miss == 0 and g[5] == 'COVERED'
            c = leg(H - 1, pp)
            dd = cov.setdefault((pp, t, H), {'K': set(), 'Kpc': set(), 'bad': set()})
            if good:
                dd['K'].add(K)
                dd['Kpc'].add(K % (pp ** c) if c else 0)
            else:
                dd['bad'].add(K)


def uniform(p, t, H):
    c = leg(H - 1, p)
    pc = p ** c
    d = cov.get((p, t, H))
    if not d:
        return False
    need = {K for K in range(1, pc) if K % p} if c > 0 else {0}
    return need <= d['Kpc'] and H + 1 < p ** t


def position(p, t, H, K):
    d = cov.get((p, t, H))
    return bool(d) and K in d['K'] and p ** t * K - H > 1


ok = True
notes = []
for t in range(1, D):
    if t in uni:
        if not uniform(p, t, uni[t]):
            ok = False
            notes.append(f"uniform t={t} H={uni[t]} missing")
        continue
    if t not in posH:
        ok = False
        notes.append(f"depth {t}: no certificate given")
        continue
    for K in range(1, p ** (D - t)):
        if K % p == 0:
            continue
        H = exc.get((t, K), posH[t])
        if position(p, t, H, K):
            continue
        ok = False
        notes.append(f"pos t={t} K={K}")
print(f"[{prog}] p={p} D={D}: {'CHAIN OK  f(1,p) >= ' + str(leg(p**D - 1, p)) if ok else 'INCOMPLETE'} "
      f"{notes[:8]}{' ...' if len(notes) > 8 else ''}")
