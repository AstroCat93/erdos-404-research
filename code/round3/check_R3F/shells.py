"""shells.py -- driver for shellchk.c (check of R3F, round 3).  Independent of all R3F code.

Families of element lists (all residues mod M = p^k):
  gate p d       : sigma_i = (-1)^i (p-1)!/(p-1-i)!, 0 <= i < p                         (R3F Lemma A1)
  tail p N0 k    : x'_n = n!/p^{e0}, e0 = v_p(N0!), n >= N0 with v_p(x'_n) < k            (note 10.4, R3F (e))
  fact p k       : i!, i >= 0 with v_p(i!) < k                                           (R3F B4)
Output: certified enclosures [lo, hi] of S1 (L^1 shell) and S2 (L^2 shell) at exact level k.

usage: python3 -I shells.py FAMILY p [N0] k [--brute] [--chunks C]
"""
import os
import subprocess
import sys
import time
from math import factorial

import mpmath
from mpmath import iv

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = '/tmp/r3_check_R3F'
BIN = os.path.join(SCR, 'bin', 'shellchk')
sys.path.insert(0, HERE)
import gen_tables  # noqa: E402


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def elems_gate(p, k):
    M = p ** k
    f = factorial(p - 1)
    return [((-1) ** i * (f // factorial(p - 1 - i))) % M for i in range(p)]


def elems_tail(p, N0, k):
    M = p ** k
    e0 = vp_fact(N0, p)
    out = []
    n = N0
    while True:
        v = vp_fact(n, p) - e0
        if v >= k and n > N0 + p * (k + 2):
            break
        if v < k:
            x = factorial(n) // p ** e0
            out.append(x % M)
        n += 1
    return out


def elems_fact(p, k):
    M = p ** k
    out = []
    i = 0
    while vp_fact(i, p) < k:
        out.append(factorial(i) % M)
        i += 1
    return out


def table_for(M):
    os.makedirs(os.path.join(SCR, 'tables'), exist_ok=True)
    fn = os.path.join(SCR, 'tables', f'{M}.bin')
    if not os.path.exists(fn):
        gen_tables.gen(M, fn)
    return fn


def run_shell(p, k, xs, chunks=1, tag=''):
    M = p ** k
    tf = table_for(M)
    ef = os.path.join(SCR, f'elem_{tag}_{p}_{k}.txt')
    with open(ef, 'w') as f:
        f.write(f'{len(xs)}\n' + '\n'.join(str(x) for x in xs) + '\n')
    half = (M - 1) // 2
    tot = [mpmath.mpf(0)] * 4
    units = 0
    bounds = [1 + (half * j) // chunks for j in range(chunks)] + [half + 1]
    for j in range(chunks):
        a, b = bounds[j], bounds[j + 1] - 1
        if b < a:
            continue
        out = subprocess.run(['nice', '-n', '10', BIN, tf, ef, str(p), str(a), str(b)],
                             capture_output=True, text=True, check=True).stdout.split()
        units += int(out[4])
        for i in range(4):
            tot[i] += mpmath.mpf(out[5 + i])
    # totals = 2 x half sums; rigorous margins (see shellchk.c header)
    u = mpmath.mpf(2) ** -53
    n = len(xs)
    L = 4096
    nb = half // L + 2 * chunks + 2
    gam = (L - 1) * u / (1 - (L - 1) * u)
    gl = nb * mpmath.mpf(2) ** -64 * (1 + mpmath.mpf(2) ** -60)
    up = (1 - u) ** (-(2 * n - 1)) / (1 - gam) / (1 - gl) * (1 + mpmath.mpf('1e-19'))
    lo = (1 + u) ** (-(2 * n - 1)) * (1 - gam) * (1 - gl) * (1 - mpmath.mpf('1e-19'))
    S1 = (2 * tot[1] * lo, 2 * tot[0] * up)
    S2 = (2 * tot[3] * lo, 2 * tot[2] * up)
    assert 2 * units == M - M // p, (units, M)
    return S1, S2


def brute(p, k, xs):
    mpmath.mp.dps = 40
    M = p ** k
    s1 = s2 = mpmath.mpf(0)
    for u in range(1, M):
        if u % p == 0:
            continue
        pr = mpmath.mpf(1)
        for x in xs:
            pr *= abs(mpmath.cospi(mpmath.mpf(u * x % M) / M))
        s1 += pr
        s2 += pr * pr
    mpmath.mp.dps = 30
    return s1, s2


def main():
    mpmath.mp.dps = 30
    fam = sys.argv[1]
    p = int(sys.argv[2])
    args = [a for a in sys.argv[3:] if not a.startswith('--')]
    chunks = 1
    if '--chunks' in sys.argv:
        chunks = int(sys.argv[sys.argv.index('--chunks') + 1])
        args = [a for a in args if a != str(chunks)] if False else args
    if fam == 'gate':
        ks = [int(a) for a in args[:1]] if len(args) == 1 else [int(a) for a in args[:2]]
        N0 = None
    elif fam == 'tail':
        N0 = int(args[0]); ks = [int(args[1])]
    else:
        N0 = None; ks = [int(args[0])]
    k = ks[0]
    xs = {'gate': lambda: elems_gate(p, k), 'tail': lambda: elems_tail(p, N0, k), 'fact': lambda: elems_fact(p, k)}[fam]()
    t0 = time.time()
    S1, S2 = run_shell(p, k, xs, chunks=chunks, tag=fam)
    wall = time.time() - t0
    N = p ** k - p ** (k - 1)
    twopi = iv.mpf(2) / iv.pi
    rnd = N * twopi ** (p if fam == 'gate' else len(xs))
    rho_hi = S1[1] / mpmath.mpf(rnd.a)
    line = (f'{fam} p={p} N0={N0} k={k} n={len(xs)}  S1 in [{mpmath.nstr(S1[0], 15)}, {mpmath.nstr(S1[1], 15)}]  '
            f'S2 in [{mpmath.nstr(S2[0], 15)}, {mpmath.nstr(S2[1], 15)}]  S1/(N (2/pi)^n)<= {mpmath.nstr(rho_hi, 10)}  wall={wall:.1f}s')
    print(line, flush=True)
    if '--brute' in sys.argv:
        b1, b2 = brute(p, k, xs)
        ok = S1[0] <= b1 <= S1[1] and S2[0] <= b2 <= S2[1]
        print(f'   brute (mpmath 40 digits): S1={mpmath.nstr(b1, 20)} S2={mpmath.nstr(b2, 20)}  inside enclosure: {ok}', flush=True)


if __name__ == '__main__':
    main()
