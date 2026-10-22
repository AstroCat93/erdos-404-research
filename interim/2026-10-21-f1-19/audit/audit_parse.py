#!/usr/bin/env python3
"""Interim audit (2026-10-21): fresh log parser + requirement check for f(1,19) >= v_19((19^9-1)!).
Written independently of chain.py / chain_r3.py / collect_t3b.py.

Requirements are derived from note Prop. 10.10 + Thm 3.12(a) with p=19, D=9, a=1 (see derive()).
A per-K record counts only if it comes from a COMPLETED run:
  round-3 logs: file has a '# END' line, a program trailer (SUMMARY A' / END C'), and name lacks INTERRUPTED;
  round-2 logs (no '# END' wrapper): file has the program trailer (SUMMARY A / SUMMARY B / END C).
Program families: A-family {A (fibcov.c), A' (fibcov_ip.c)}, B {fibcov2.c}, C-family {C (covchk.c), C' (covchk_ip.c)}.
"""
import os, re, sys, glob, json
from collections import defaultdict

BASE = sys.argv[1]
R2 = os.path.join(BASE, 'publish-erdos404/data/round2')
R3 = os.path.join(BASE, 'e404r3/T3b-q3-covering/logs')
DIRS = [(os.path.join(R2, 'logs_original/R3'), 'r2'), (os.path.join(R2, 'outputs/R3'), 'r2'),
        (os.path.join(R2, 'review/computation/logs'), 'r2'), (R3, 'r3')]
P = 19; D = 9

def leg(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

# ---------- (1) requirements ----------
UNIFORM = {1: 5, 2: 12, 3: 17, 4: 27, 5: 31, 6: 35}   # claimed uniform windows
POSH = {7: 45, 8: 49}                                   # claimed position windows
def derive():
    req = []  # (t, H, class_mod, residue_class)  each must be certified
    problems = []
    for t in range(1, D):
        if t in UNIFORM:
            H = UNIFORM[t]; c = leg(H - 1, P)
            if not (H + 1 < P ** t): problems.append(f'uniform t={t} H={H}: H+1<p^t fails')
            if not (H <= P ** t): problems.append(f'uniform t={t} H={H} > p^t')
            pc = P ** c
            classes = [1] if c == 0 else [K for K in range(1, pc) if K % P]
            for K in classes: req.append((t, H, pc, K % pc))
        else:
            H = POSH[t]; c = leg(H - 1, P); pc = P ** c
            if not (H <= P ** t): problems.append(f'pos t={t} H={H} > p^t')
            for K in range(1, P ** (D - t)):
                if K % P == 0: continue
                if not (P ** t * K - H > 1): problems.append(f'pos t={t} K={K}: N*-H<=1')
                req.append((t, H, pc, K % pc))
    return req, problems

# ---------- (2) parser ----------
RE_HDR = {
    'A':  re.compile(r'^# fibcov\(A\) p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+)'),
    "A'": re.compile(r"^# fibcov_ip\(A'\) p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+)"),
    'B':  re.compile(r'^# fibcov2\(B\) p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) kb=(\d+)'),
    'C':  re.compile(r'^# covchk\(C\) p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+)'),
    "C'": re.compile(r"^# covchk_ip\(C'\) p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) k=(\d+)"),
}
RE_A = re.compile(r'^A p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) K=(\d+) missing=(\d+) (COVERED|NOT_COVERED) \[')
RE_B = re.compile(r'^B p=(\d+) t=(\d+) H=(\d+) M=(\d+) K=(\d+) notcovered=(\d+) (OK|FAIL) \[')
RE_C = re.compile(r'^C p=(\d+) t=(\d+) H=(\d+) M=(\d+) K=(\d+) Kmodpc=(\d+) miss=(\d+)(\S*) (COVERED|UNCOVERED) ')
TRAILER = {'A': re.compile(r'^SUMMARY A p='), "A'": re.compile(r"^SUMMARY A' p="), 'B': re.compile(r'^SUMMARY B p='),
           'C': re.compile(r'^END C p='), "C'": re.compile(r"^END C' p=")}
FAM = {'A': 'A', "A'": 'A', 'B': 'B', 'C': 'C', "C'": 'C'}

def parse():
    recs = []      # dicts
    files = []     # (path, prog, status)
    anomalies = []
    for d, rnd in DIRS:
        for fn in sorted(glob.glob(os.path.join(d, '*'))):
            if fn.endswith('.gz') or os.path.isdir(fn): continue
            try: lines = open(fn, errors='replace').read().splitlines()
            except Exception as e: anomalies.append(f'unreadable {fn}: {e}'); continue
            prog = None; hdr = None
            for ln in lines:
                for pn, rx in RE_HDR.items():
                    m = rx.match(ln)
                    if m:
                        if prog is not None and prog != pn: anomalies.append(f'two programs in {fn}')
                        prog = pn; hdr = tuple(map(int, m.groups()))
            body = []
            for ln in lines:
                m = RE_A.match(ln)
                if m:
                    p, t, H, c, M, K, miss = map(int, m.groups()[:7]); out = m.group(8)
                    body.append(('A?', p, t, H, M, K, miss, out == 'COVERED', c)); continue
                m = RE_B.match(ln)
                if m:
                    p, t, H, M, K, miss = map(int, m.groups()[:6]); out = m.group(7)
                    body.append(('B', p, t, H, M, K, miss, out == 'OK', None)); continue
                m = RE_C.match(ln)
                if m:
                    p, t, H, M, K, Kpc, miss = map(int, m.groups()[:7]); flag = m.group(8); out = m.group(9)
                    body.append(('C?', p, t, H, M, K, miss, out == 'COVERED' and flag == '', Kpc)); continue
            if not body: continue
            if prog is None:
                anomalies.append(f'records without recognised header: {os.path.relpath(fn, BASE)} ({len(body)} recs)')
                continue
            has_trailer = any(TRAILER[prog].match(ln) for ln in lines)
            has_end = any(ln.startswith('# END ') for ln in lines)
            interrupted = 'INTERRUPTED' in os.path.basename(fn)
            if rnd == 'r3': complete = has_trailer and has_end and not interrupted
            else: complete = has_trailer and not interrupted
            files.append((os.path.relpath(fn, BASE), prog, complete, len(body)))
            for (tag, p, t, H, M, K, miss, ok, extra) in body:
                if tag[0] != prog[0]: anomalies.append(f'{fn}: record {tag} under header {prog}')
                c = leg(H - 1, p)
                if M != t + c: anomalies.append(f'{fn}: M={M} != t+c={t+c} (t={t},H={H})')
                if tag == 'A?' and extra != c: anomalies.append(f'{fn}: c mismatch')
                if tag == 'C?' and extra != K % (p ** c): anomalies.append(f'{fn}: Kmodpc mismatch K={K}')
                if ok and miss != 0: anomalies.append(f'{fn}: covered with miss {miss}')
                if (not ok) and miss == 0: anomalies.append(f'{fn}: not-covered with miss 0 (partial?) K={K}')
                if K % p == 0: anomalies.append(f'{fn}: K={K} divisible by p')
                recs.append(dict(file=os.path.relpath(fn, BASE), prog=prog, fam=FAM[prog], complete=complete,
                                 p=p, t=t, H=H, K=K, miss=miss, ok=ok))
    return recs, files, anomalies

def main():
    req, problems = derive()
    recs, files, anomalies = parse()
    out = {}
    print(f'requirements: {len(req)} (t,H,class) certificates; hypothesis problems: {problems or "none"}')
    from collections import Counter
    print('requirement count by depth:', dict(Counter(r[0] for r in req)))
    # index complete covered records by (t,H,class)
    cov = defaultdict(lambda: defaultdict(set))   # (t,H,cls) -> fam -> set(files)
    neg = defaultdict(list)
    for r in recs:
        if r['p'] != P: continue
        c = leg(r['H'] - 1, P); cls = r['K'] % (P ** c)
        key = (r['t'], r['H'], cls if c else 1)
        if r['complete'] and r['ok']: cov[key][r['fam']].add((r['prog'], r['file']))
        if not r['ok']: neg[key].append((r['prog'], r['file'], r['miss'], r['complete']))
    gaps = []; fams_hist = Counter(); conflicts = []
    for (t, H, pc, cls) in req:
        key = (t, H, cls if pc > 1 else 1)
        fams = {f for f in cov[key]}
        fams_hist[(t, tuple(sorted(fams)))] += 1
        if len(fams) < 2: gaps.append((t, H, cls, sorted(fams)))
        if neg.get(key): conflicts.append((t, H, cls, neg[key]))
    print('families per requirement (depth, families): count')
    for k_, v in sorted(fams_hist.items()): print('  ', k_, v)
    print('GAPS (<2 families):', gaps if gaps else 'none')
    print('CONFLICTS (a NOT_COVERED record on a required (t,H,class)):', conflicts if conflicts else 'none')
    # per-program detail for the round-3 portion
    det = defaultdict(set)
    for r in recs:
        if r['p'] == P and r['complete'] and r['ok'] and r['t'] in (7, 8) and r['H'] in (45, 49):
            det[(r['t'], r['H'], r['prog'])].add(r['K'])
    for k_ in sorted(det):
        Ks = sorted(det[k_]); print(f'  covered set {k_}: n={len(Ks)} min={Ks[0]} max={Ks[-1]}')
    # (19,8,47) K=1
    f47 = [(r['prog'], r['file'], r['miss'], r['complete']) for r in recs if r['p'] == 19 and r['t'] == 8 and r['H'] == 47]
    print('(19,8,47) records:', f47)
    inc = [f for f in files if not f[2]]
    print('incomplete files (excluded):', inc)
    print('ANOMALIES:', anomalies if anomalies else 'none')
    if not gaps and not conflicts and not problems:
        print(f'AUDIT CHAIN OK: f(1,19) >= v_19((19^9-1)!) = {leg(19**9-1, 19)} (>=2 program families per certificate)')
    else:
        print('AUDIT CHAIN NOT OK')

main()
