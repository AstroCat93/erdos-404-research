#!/usr/bin/env python3
"""logaudit.py -- check of track R3C (round 3, 2026-10-13): read every log behind R1, R3, R4, R8
and verify, line by line, that it says what the report says, with the stated parameters and program.

For each certificate the expected (p, t, H) come from the report; c = v_p((H-1)!) and M = t + c are
recomputed here, and the class/position sets are recomputed:
  A (fibcov,  scans):  K = K'           (all units K' mod p^c; K = 1 when c = 0)
  C (covchk,  scans):  K = K' + 2 p^c   (K = 3 when c = 0)
  D (covfast, U29_D):  K = K' + 3 p^c   (K = 4 when c = 0)
  depth 7:             K = K'' = 1..28, H = 45, programs A and D, one log per (program, K'')
Every line of every audited log must be of a known kind (comment, result, summary, scan verdict);
anything else (an error message, say) is printed.
usage: python3 logaudit.py   (from the repository root)
"""
import os
import re
import sys

R = 'data/round3/R3C'
problems = []


def leg(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def units(p, c):
    return list(range(1, p ** c)) if c else [0]


def prob(msg):
    problems.append(msg)
    print('  PROBLEM: ' + msg)


A_RE = re.compile(r'^A p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) K=(\d+) missing=(\d+) (COVERED|NOT_COVERED) \[[\d.]+s\]$')
C_RE = re.compile(r'^C p=(\d+) t=(\d+) H=(\d+) M=(\d+) K=(\d+) Kmodpc=(\d+) miss=(\d+)(\S*) (COVERED|UNCOVERED) [\d.]+s$')
D_RE = re.compile(r'^D p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+) K=(\d+) Kmodpc=(\d+) missing=(\d+) (COVERED|NOT_COVERED) \[[\d.]+s\]$')
SA_RE = re.compile(r'^SUMMARY A p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+) mode=(\w+) nK=(\d+) fail=(\d+) worst_missing=(\d+) (ALL_COVERED|SOME_NOT_COVERED) total=[\d.]+s$')
SD_RE = re.compile(r'^SUMMARY D p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+) mode=(\w+) nK=(\d+) fail=(\d+) worst_missing=(\d+) (ALL_COVERED|SOME_NOT_COVERED) total=[\d.]+s$')
EC_RE = re.compile(r'^END C p=(\d+) t=(\d+) H=(\d+) nK=(\d+) bad=(\d+) (ALL_COVERED|SOME_UNCOVERED) [\d.]+s$')


def parse_results(lines, p, t, H):
    """per-K results for (p,t,H) of each program, from (possibly indented) lines"""
    c = leg(H - 1, p)
    M = t + c
    res = {'A': {}, 'C': {}, 'D': {}}
    for ln in lines:
        s = ln.strip()
        m = A_RE.match(s)
        if m and tuple(map(int, m.groups()[:3])) == (p, t, H):
            if (int(m.group(4)), int(m.group(5))) != (c, M):
                prob(f'A line with wrong c/M: {s}')
            res['A'][int(m.group(6))] = (int(m.group(7)), m.group(8))
        m = C_RE.match(s)
        if m and tuple(map(int, m.groups()[:3])) == (p, t, H):
            if int(m.group(4)) != M or (c and int(m.group(6)) != int(m.group(5)) % p ** c):
                prob(f'C line with wrong M/Kmodpc: {s}')
            res['C'][int(m.group(5))] = (int(m.group(7)), m.group(9) + m.group(8))
        m = D_RE.match(s)
        if m and tuple(map(int, m.groups()[:3])) == (p, t, H):
            if (int(m.group(4)), int(m.group(5))) != (c, M):
                prob(f'D line with wrong c/M: {s}')
            res['D'][int(m.group(7))] = (int(m.group(9)), m.group(10))
    return res


def all_covered(d, Ks):
    return set(d) == set(Ks) and all(v == (0, 'COVERED') for v in d.values())


def scan_cert(p, t, H, fn):
    c = leg(H - 1, p)
    M = t + c
    L = open(os.path.join(R, fn)).read().splitlines()
    cmd = [x for x in L if x.startswith('# command:')]
    ok_cmd = cmd and 'R3C_BIN=/tmp/r3_R3C/bin' in cmd[0] and f'scan_r3.py {p} {t} ' in cmd[0]
    verdict = [x for x in L if re.match(rf'p={p} t={t} H={H} c={c} M={M} k=\d+: HOLDS$', x)]
    k = int(re.search(r'k=(\d+)', verdict[0]).group(1)) if verdict else None
    nK = len(units(p, c)) if c else 1
    sa = [x.strip() for x in L if x.strip().startswith(f'SUMMARY A p={p} t={t} H={H} ')]
    ec = [x.strip() for x in L if x.strip().startswith(f'END C p={p} t={t} H={H} ')]
    sa_ok = sa and SA_RE.match(sa[0]) and SA_RE.match(sa[0]).groups()[3:] == (str(c), str(M), str(k), 'all', str(nK), '0', '0', 'ALL_COVERED')
    ec_ok = ec and EC_RE.match(ec[0]) and EC_RE.match(ec[0]).groups()[3:] == (str(nK), '0', 'ALL_COVERED')
    res = parse_results(L, p, t, H)
    KA = [1] if c == 0 else units(p, c)
    KC = [3] if c == 0 else [u + 2 * p ** c for u in units(p, c)]
    okA, okC = all_covered(res['A'], KA), all_covered(res['C'], KC)
    end = any(x.startswith('# end:') for x in L)
    good = bool(ok_cmd and verdict and sa_ok and ec_ok and okA and okC and end)
    print(f"uniform Cov({p},{t},{H}) c={c} M={M} k={k} in {fn}: command ok={bool(ok_cmd)} HOLDS-line={bool(verdict)} "
          f"SUMMARY A ok={bool(sa_ok)} END C ok={bool(ec_ok)} A classes {len(res['A'])}/{len(KA)} covered={okA} "
          f"C classes {len(res['C'])}/{len(KC)} covered={okC} end-line={end} -> {'OK' if good else 'NOT OK'}")
    if not good:
        prob(f'scan certificate ({p},{t},{H}) in {fn}')
    return good


def unexpected_lines(L):
    out = []
    for x in L:
        s = x.strip()
        if not s or s.startswith('#') or A_RE.match(s) or C_RE.match(s) or D_RE.match(s) or SA_RE.match(s) \
                or SD_RE.match(s) or EC_RE.match(s) or s.startswith('MISS ') or s.startswith('(fibres ending'):
            continue
        out.append(s)
    return out


def d_uniform(p, t, H, k, fn):
    c = leg(H - 1, p)
    M = t + c
    L = open(os.path.join(R, fn)).read().splitlines()
    cmd = L[0]
    ok_cmd = cmd == f'# command: /tmp/r3_R3C/bin/covfast {p} {t} {H} {k} cls 3'
    hdr = [x for x in L if x.startswith('# covfast(D)')]
    ok_hdr = hdr and f'p={p} t={t} H={H} c={c} M={M} k={k} ' in hdr[0]
    KD = [4] if c == 0 else [u + 3 * p ** c for u in units(p, c)]
    res = parse_results(L, p, t, H)
    okD = all_covered(res['D'], KD)
    sd = [x for x in L if x.startswith('SUMMARY D')]
    sd_ok = sd and SD_RE.match(sd[0]) and SD_RE.match(sd[0]).groups()[3:] == (str(c), str(M), str(k), 'cls', str(len(KD)), '0', '0', 'ALL_COVERED')
    end = any(x.startswith('# end:') for x in L)
    unk = unexpected_lines(L)
    good = bool(ok_cmd and ok_hdr and okD and sd_ok and end and not unk)
    print(f"uniform Cov({p},{t},{H}) program D in {fn}: command ok={ok_cmd} header ok={bool(ok_hdr)} classes "
          f"{len(res['D'])}/{len(KD)} covered={okD} SUMMARY ok={bool(sd_ok)} end={end} other lines={unk} -> {'OK' if good else 'NOT OK'}")
    if not good:
        prob(f'D uniform ({p},{t},{H}) in {fn}')


def depth7(prog, K, H=45, sub='p29_t7'):
    fn = f'{sub}/P29_t7_H{H}_{prog}_K{K}.log'
    L = open(os.path.join(R, fn)).read().splitlines()
    if prog == 'A':
        ok_cmd = L[0] == f'# command: /tmp/r3_R3C/bin/fibcov 29 7 {H} 1 pos {K}'
        ok_hdr = any(x.startswith(f'# fibcov(A) p=29 t=7 H={H} c=1 M=8 k=1 ') for x in L)
        S = [x for x in L if SA_RE.match(x)]
    else:
        ok_cmd = L[0] in (f'# command: env COVFAST_ZMAX=16777216 /tmp/r3_R3C/bin/covfast 29 7 {H} 1 pos {K}',
                          f'# command: env COVFAST_ZMAX=16777216 COVFAST_VERBOSE=1 /tmp/r3_R3C/bin/covfast 29 7 {H} 1 pos {K}')
        ok_hdr = any(x.startswith(f'# covfast(D) p=29 t=7 H={H} c=1 M=8 k=1 ') and 'ZMAX=16777216' in x for x in L)
        S = [x for x in L if SD_RE.match(x)]
    res = parse_results(L, 29, 7, H)[prog]
    ok_res = res == {K: (0, 'COVERED')}
    ok_sum = len(S) == 1 and S[0].split()[9:12] == ['nK=1', 'fail=0', 'worst_missing=0'] and 'ALL_COVERED' in S[0]
    end = [x for x in L if x.startswith('# end:')]
    start = [x for x in L if x.startswith('# start:')]
    wall = re.search(r'wall=([\d.]+)', '\n'.join(L))
    unk = unexpected_lines(L)
    good = ok_cmd and ok_hdr and ok_res and ok_sum and bool(end) and not unk
    if not good:
        prob(f'depth-7 log {fn}: cmd={ok_cmd} hdr={ok_hdr} res={res} sum={ok_sum} end={bool(end)} other={unk}')
    return good, float(wall.group(1)) if wall else None, start[0][9:] if start else '', end[0][7:] if end else ''


def main():
    print('## 1. Uniform certificates t <= 6 at p = 29 (programs A and C, scan logs)')
    Ht29 = [7, 13, 19, 24, 29, 40]
    for t, H in enumerate(Ht29, 1):
        scan_cert(29, t, H, f'scan_p29_t{t}.log')
    print('## 2. Uniform certificates t <= 6 at p = 29 (program D)')
    for t, H, k in [(1, 7, 0), (2, 13, 0), (3, 19, 0), (4, 24, 0), (5, 29, 0), (6, 40, 1)]:
        d_uniform(29, t, H, k, f'U29_D_t{t}_H{H}.log')
    print('## 3. Depth-7 positions K\'\' = 1..28, H = 45 (programs A and D)')
    tot = {'A': 0.0, 'D': 0.0}
    rng = {'A': [], 'D': []}
    nok = 0
    for K in range(1, 29):
        for prog in 'AD':
            g, w, s, e = depth7(prog, K)
            nok += g
            tot[prog] += w or 0
            rng[prog].append(w)
    print(f"   {nok}/56 logs OK (command, header c=1 M=8 k=1, K'' line 'missing=0 COVERED', SUMMARY nK=1 fail=0 ALL_COVERED, end line, no other output)")
    for prog in 'AD':
        print(f"   program {prog}: wall {min(rng[prog]):.0f}-{max(rng[prog]):.0f} s per position, total {tot[prog] / 3600:.2f} h")
    print('## 4. Uniform certificates t <= 6 at p = 31 (programs A and C)')
    for t, H in enumerate([7, 14, 19, 25, 30, 41], 1):
        scan_cert(31, t, H, f'scan_p31_t{t}.log')
    print('## 5. Holds above the minimum (scanall logs, A and C over all classes)')
    for p, t, Hs in [(29, 2, [13, 14, 15, 16]), (29, 3, [20, 21]), (29, 4, [25, 26]), (29, 5, [29, 36, 37, 38, 39]),
                     (31, 2, [15, 16]), (31, 3, [20, 21]), (31, 4, [26, 27]), (31, 5, [30, 31, 38, 39])]:
        for H in Hs:
            scan_cert(p, t, H, f'scanall_p{p}_t{t}.log')
    print(f'## problems: {len(problems)}')
    for x in problems:
        print('   ' + x)


if __name__ == '__main__':
    sys.exit(main())
