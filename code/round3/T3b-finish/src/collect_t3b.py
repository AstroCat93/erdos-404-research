#!/usr/bin/env python3
"""collect_t3b.py -- T3b-finish (2026-10-21). Independent re-parse of every job log of track T3b-q3-covering
(written from scratch; shares no code with T3b's results_table.py or chain_r3.py).
For each log: program, (p,t,H), requested positions (from '# CMD'), per-position outcome/miss/time,
START/END timestamps, exit status, max RSS, peak footprint. Then an independent coverage/chain check
for f(1,19) >= v_19((19^9-1)!) under note Prop. 10.10, per program family (A/A' vs B vs C/C').
usage: collect_t3b.py T3B_DIR ROUND2_DATA_DIR"""
import glob, os, re, sys, json

T3B, R2 = sys.argv[1], sys.argv[2]

def legendre(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q; q *= p
    return s

def digit_sum(n, p):
    s = 0
    while n: s += n % p; n //= p
    return s

LINE_A = re.compile(r"^A p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+) K=(\d+) missing=(\d+) (\w+) \[([\d.]+)s\]")
LINE_B = re.compile(r"^B p=(\d+) t=(\d+) H=(\d+) M=(\d+) K=(\d+) notcovered=(\d+) (\w+)")
LINE_C = re.compile(r"^C p=(\d+) t=(\d+) H=(\d+) M=(\d+) K=(\d+) Kmodpc=(\d+) miss=(\d+)(\S*) (\w+)(?: ([\d.]+)s)?")

def parse(fn):
    job = dict(file=os.path.relpath(fn, T3B) if fn.startswith(T3B) else fn, cmd=None, start=None, end=None,
               exit=None, rss=None, peak=None, results=[], requested=[])
    for ln in open(fn, errors='replace'):
        ln = ln.rstrip('\n')
        if ln.startswith('# CMD:'):
            job['cmd'] = ln[6:].strip()
            toks = job['cmd'].split()
            if 'pos' in toks: job['requested'] = [int(x) for x in toks[toks.index('pos') + 1:]]
        elif ln.startswith('# START'):
            m = re.search(r"START (\S+ \S+) \S+ unix=(\d+)", ln); job['start'] = (m.group(1), int(m.group(2)))
        elif ln.startswith('# END'):
            m = re.search(r"END (\S+ \S+) \S+ unix=(\d+) exit=(-?\d+)", ln)
            job['end'] = (m.group(1), int(m.group(2))); job['exit'] = int(m.group(3))
        elif ln.strip().endswith('maximum resident set size'):
            job['rss'] = int(ln.split()[0])
        elif ln.strip().endswith('peak memory footprint'):
            job['peak'] = int(ln.split()[0])
        else:
            m = LINE_A.match(ln)
            if m:
                p, t, H, c, M, K, miss = map(int, m.groups()[:7])
                ok = (m.group(8) == 'COVERED')
                job['results'].append(('A', p, t, H, K, miss, ok and miss == 0, float(m.group(9)))); continue
            m = LINE_B.match(ln)
            if m:
                p, t, H, M, K, nc = map(int, m.groups()[:6])
                job['results'].append(('B', p, t, H, K, nc, m.group(7) == 'OK' and nc == 0, None)); continue
            m = LINE_C.match(ln)
            if m:
                p, t, H, M, K, Kpc, miss = map(int, m.groups()[:7])
                ok = (m.group(9) == 'COVERED' and m.group(8) == '' and miss == 0)
                job['results'].append(('C', p, t, H, K, miss, ok, float(m.group(10)) if m.group(10) else None))
    return job

# ---- 1. this track's job logs
jobs = []
for fn in sorted(glob.glob(os.path.join(T3B, 'logs', '*.log'))):
    b = os.path.basename(fn)
    if not (b.startswith('P19_') or b.startswith('U19_') or b.startswith('VAL_')): continue
    j = parse(fn); j['interrupted'] = 'INTERRUPTED' in b; jobs.append(j)

print("# Per-job table (T3b logs). wall = END-START (s); RSS in GB")
print("file | prog | (p,t,H) | requested | reported | covered | uncovered(miss) | start | end | wall | exit | maxRSS GB")
for j in jobs:
    prog = sorted({r[0] for r in j['results']}) or ['?']
    pth = sorted({r[1:4] for r in j['results']})
    cov = sum(1 for r in j['results'] if r[6]); unc = [(r[4], r[5]) for r in j['results'] if not r[6]]
    wall = (j['end'][1] - j['start'][1]) if (j['end'] and j['start']) else None
    print(f"{j['file']} | {''.join(prog)} | {pth} | {len(j['requested'])} | {len(j['results'])} | {cov} | {unc} | "
          f"{j['start'][0] if j['start'] else '-'} | {j['end'][0] if j['end'] else 'NO END'} | {wall} | {j['exit']} | "
          f"{(j['rss'] or 0)/1e9:.3f}" + ("  [INTERRUPTED, excluded]" if j['interrupted'] else ''))
    missing_req = sorted(set(j['requested']) - {r[4] for r in j['results']})
    if missing_req and not j['interrupted']: print(f"   !! requested but not reported: {missing_req}")

# ---- 2. round-2 logs for the uniform t<=6 and depth-7 K''<=18 certificates
r2dirs = [os.path.join(R2, 'logs_original', 'R3'), os.path.join(R2, 'review', 'computation', 'logs')]
r2jobs = []
for d in r2dirs:
    for fn in sorted(glob.glob(os.path.join(d, '*.log'))):
        j = parse(fn); j['interrupted'] = False; r2jobs.append(j)

# certificates: fam -> (p,t,H) -> set of K certified (only completed, non-interrupted jobs with exit 0 or round-2 logs)
cert = {}; fails = {}
for j in jobs + r2jobs:
    if j['interrupted']: continue
    if j in jobs and j['exit'] != 0: continue
    for (fam, p, t, H, K, miss, ok, tm) in j['results']:
        (cert if ok else fails).setdefault(fam, {}).setdefault((p, t, H), {})
        if ok: cert[fam][(p, t, H)].setdefault(K, []).append(j['file'])
        else: fails[fam][(p, t, H)].setdefault(K, []).append((miss, j['file']))

p, D = 19, 9
print("\n# Independent chain check, p=19, D=9 (note Prop. 10.10)")
uniform = {1: 5, 2: 12, 3: 17, 4: 27, 5: 31, 6: 35}
pos = {7: 45, 8: 49}
summary = {}
for t, H in uniform.items():
    c = legendre(H - 1, p); pc = p ** c
    need = {K for K in range(1, pc) if K % p} if c > 0 else {1}
    fams = []
    for fam in 'ABC':
        S = cert.get(fam, {}).get((p, t, H), {})
        have = {K % pc for K in S} if c > 0 else ({1} if S else set())
        if need <= have: fams.append(fam)
    assert H + 1 < p ** t
    summary[f"uniform t={t} H={H} c={c}"] = fams
    print(f"uniform Cov(19,{t},{H}) c={c}: classes {len(need)}; families certifying all: {fams}; "
          f"failures logged: { {f: len(fails.get(f,{}).get((p,t,H),{})) for f in 'ABC'} }")
for t, H in pos.items():
    need = [K for K in range(1, p ** (D - t)) if K % p]
    assert all(p ** t * K - H > 1 for K in need)
    c = legendre(H - 1, p)
    out = {}
    for fam in 'ABC':
        S = cert.get(fam, {}).get((p, t, H), {})
        out[fam] = len([K for K in need if K in S])
    fl = {f: sorted(fails.get(f, {}).get((p, t, H), {}).items()) for f in 'ABC'}
    nfam = {K: [f for f in 'ABC' if K in cert.get(f, {}).get((p, t, H), {})] for K in need}
    by_count = {}
    for K, fs in nfam.items(): by_count.setdefault(len(fs), []).append(K)
    summary[f"positions t={t} H={H} c={c}"] = {"needed": len(need), "covered_per_family": out,
                                               "families_per_class_histogram": {k: len(v) for k, v in by_count.items()},
                                               "failures": fl}
    print(f"positions depth {t} H={H} c={c}: needed {len(need)}; covered per family {out}; "
          f"#families per class: { {k: len(v) for k, v in sorted(by_count.items())} }; failures logged: {fl}")
    if 0 in by_count or 1 in by_count:
        print(f"   classes with <2 families: {sorted(by_count.get(0, []) + by_count.get(1, []))[:50]}")

# failing control case
print("\n(19,8,47) K=1 outcomes:", {f: fails.get(f, {}).get((19, 8, 47), {}) for f in 'AC'})

N = p ** D - 1
v = legendre(N, p); v2 = (N - digit_sum(N, p)) // (p - 1)
print(f"\nLegendre: v_19((19^9-1)!) = {v}; (N - s_19(N))/18 = {v2}; s_19(N) = {digit_sum(N, p)}; old bound v_19((19^8-1)!) = {legendre(p**8-1, p)}")
json.dump(summary, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'collect_summary.json'), 'w'), indent=1, default=str)
