#!/usr/bin/env python3
"""Semantic tamper tests: replace a leaf's n by an n' whose pair (n', n'+1) factors
completely over the primes ASSIGNED on that leaf's path, so only leaf condition 3
(the character sums) can catch it.  Also a positive control: an n' != n that
satisfies all three conditions; a correct checker must ACCEPT that (FORMAT.md:
any n meeting the conditions is acceptable).

Usage: tamper2.py RAW_CERT K L S2 WORKDIR PCHECK CCHECK
"""
import sys, os, random, subprocess, json, time
from array import array

raw, K, L, S2s, work, pcheck, ccheck = sys.argv[1:8]
K = int(K); L = int(L); S2 = [int(x) for x in S2s.split(',')]
rng = random.Random(77)

data = open(raw, 'rb').read()
lines = data.split(b'\n')[:-1]
del data
hdr, tree = lines[:5], lines[5:-1]
NT = len(tree)

# primes and spf (independent little sieve)
N = L + 1
spf = array('i', [0]) * (N + 1)
for i in range(2, N + 1):
    if spf[i] == 0:
        spf[i] = i
        if i * i <= N:
            for j in range(i * i, N + 1, i):
                if spf[j] == 0:
                    spf[j] = i
primes = [i for i in range(2, N + 1) if spf[i] == i]
pidx = {p: i for i, p in enumerate(primes[:400])}


def fac(m):
    out = {}
    while m > 1:
        p = spf[m]; out[p] = out.get(p, 0) + 1; m //= p
    return out


# smooth pairs over the first 70 primes (enough: max depth is 61)
P70 = primes[69]
pairs = []   # (n, maxidx, facn, facn1)
for n in range(1, L + 1):
    a = fac(n); b = fac(n + 1)
    mx = max(list(a) + list(b))
    if mx <= P70:
        pairs.append((n, pidx[mx], a, b))
print(f"{len(pairs)} pairs with n <= L that are {P70}-smooth", flush=True)

# choose target leaves: random leaves at depth >= 8, recording their path assignment
want = set(rng.sample(range(NT), 4000))
targets = []
st = []  # [depth, j]
R = [0] * 200
depth = 0
for i, ln in enumerate(tree):
    if ln == b'B':
        R[depth] = S2[0] if depth == 0 else 0
        st.append([depth, 0]); depth += 1
        continue
    if i in want and ln.startswith(b'L ') and depth >= 8:
        targets.append((i, depth, R[:depth]))
    while st:
        d, j = st[-1]
        nch = len(S2) if d == 0 else K
        if j + 1 < nch:
            st[-1][1] = j + 1
            R[d] = S2[j + 1] if d == 0 else j + 1
            depth = d + 1
            break
        st.pop()
print(f"{len(targets)} candidate target leaves", flush=True)


def fval(f, Rp):
    return sum(e * Rp[pidx[q]] for q, e in f.items()) % K


def find(kind):
    """kind: 'n1_fails', 'n_fails', 'both_fail', 'valid_alt'"""
    rng.shuffle(targets)
    for i, d, Rp in targets:
        n0 = int(tree[i][2:])
        cands = [x for x in pairs if x[1] < d and x[0] != n0]
        rng.shuffle(cands)
        for n, mx, a, b in cands:
            fa, fb = fval(a, Rp), fval(b, Rp)
            ok = {'n1_fails': fa == 0 and fb != 0, 'n_fails': fa != 0 and fb == 0,
                  'both_fail': fa != 0 and fb != 0, 'valid_alt': fa == 0 and fb == 0}[kind]
            if ok:
                return i, d, n0, n, fa, fb
    return None


def run(path):
    p = subprocess.run(['nice', '-n', '10', sys.executable, '-I', pcheck, path, '--k', str(K),
                        '--L', str(L), '--S2', S2s], capture_output=True, text=True)
    d = json.loads(p.stdout)
    py = (d['verdict'], '; '.join(d['reject_reasons']))
    with open(path, 'rb') as f:
        q = subprocess.run(['nice', '-n', '10', ccheck, str(K), str(L), S2s], stdin=f,
                           capture_output=True, text=True)
    c = ('PROOF' if q.returncode == 0 else 'REJECT', q.stdout.strip().splitlines()[-1])
    return py, c


path = os.path.join(work, 'tampered2.raw')
summary = []
for kind, expect in [('n1_fails', 'REJECT'), ('n_fails', 'REJECT'), ('both_fail', 'REJECT'),
                     ('valid_alt', 'PROOF')]:
    r = find(kind)
    if r is None:
        print(json.dumps({'mutation': kind, 'note': 'no suitable leaf found'})); continue
    i, d, n0, n, fa, fb = r
    t = tree[:]; t[i] = b'L %d' % n
    with open(path, 'wb') as fo:
        fo.write(b'\n'.join(hdr + t + [b'end']) + b'\n')
    del t
    py, c = run(path)
    os.remove(path)
    good = py[0] == expect and c[0] == expect
    rec = {'mutation': kind, 'tree_line': i, 'depth': d, 'old_n': n0, 'new_n': n,
           'f(new_n)': fa, 'f(new_n+1)': fb, 'expected': expect, 'python': py, 'c': c,
           'as_expected': good}
    summary.append(good)
    print(json.dumps(rec), flush=True)
print(f"SUMMARY: {sum(summary)}/{len(summary)} semantic mutations behaved as expected", flush=True)
