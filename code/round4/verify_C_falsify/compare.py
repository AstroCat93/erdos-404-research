#!/usr/bin/env python3
"""Compare the independent recomputations (cert.log, qconst_indep.log) with the
numbers printed in M4C.md (§4.3 table, §7.3 table, headline) and assemble.log.
Pure text comparison; no computation shared with M4C code."""
import re, sys

R = '/home/user/erdos-404-research/'
rep = open(R + 'data/round4/reports/M4C.md').read()
cert = open(R + 'data/round4/verify_C_falsify/cert.log').read()
qlog = open(R + 'data/round4/verify_C_falsify/qconst_indep.log').read()
alog = open(R + 'data/round4/M4C/assemble.log').read()
alog = alog[alog.index("re-run after the remainder fix"):]


def num(s):
    s = s.strip().replace('$', '').replace('\\cdot', '*').replace('{', '').replace('}', '').replace(' ', '')
    m = re.match(r'^([0-9.]+)\*10\^(-?[0-9]+)$', s)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    return float(s)


# --- §4.3 q table
qtab = {}
for line in rep.splitlines():
    m = re.match(r'^\| (\d+) \| (yes|no) \| (.*) \| (.*) \| (.*) \|$', line)
    if m:
        qtab[int(m.group(1))] = (num(m.group(3)), num(m.group(4)), num(m.group(5)))
mine_q = {}
for m in re.finditer(r'p=(\d+)\s+q1-1=([0-9.e+-]+) .*?q2-1=([0-9.e+-]+) .*?q3-1=([0-9.e+-]+)', qlog):
    mine_q[int(m.group(1))] = tuple(float(m.group(i)) for i in (2, 3, 4))
bad = 0
for p in sorted(mine_q):
    if p not in qtab:
        continue
    for i in range(3):
        a = qtab[p][i]; b = mine_q[p][i]
        # printed values are rounded to 3 significant digits
        if abs(a - b) > 0.0051 * abs(b):
            bad += 1
            print("q-table mismatch p=%d q%d-1: report %.3e, recomputed %.6e" % (p, i + 1, a, b))
print("§4.3: compared %d primes x 3 constants; mismatches beyond 3-digit rounding: %d" % (len([p for p in mine_q if p in qtab]), bad))

# AC(p) of §9.2
for p in sorted(mine_q):
    q1m, q2m, q3m = mine_q[p]
    ac = (q1m <= p ** -3) and (q2m <= 1 / p) and (q3m + 1 <= 2)
    if (p >= 13) != ac:
        print("AC(p) claim mismatch at p=%d: AC holds=%s" % (p, ac))
print("§9.2 AC(p): holds exactly for p>=13 in the list and fails at p=11:", all(((p >= 13) == ((mine_q[p][0] <= p ** -3) and (mine_q[p][1] <= 1 / p) and (mine_q[p][2] <= 1))) for p in mine_q))

# --- §7.3 table
tab = {}
for line in rep.splitlines():
    m = re.match(r'^\| (\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (\d+) \| agrees \|$', line)
    if m:
        tab[int(m.group(1))] = dict(logPi=num(m.group(2)), delta=num(m.group(3)), cp=num(m.group(4)),
                                    mu=num(m.group(5)), kappa=num(m.group(6)), lstar=int(m.group(7)))
mine = {}
for m in re.finditer(r'RESULT p=(\d+): log Pi_A=([0-9.e+-]+) Pi_A=([0-9.e+-]+) delta_A=([0-9.e+-]+) .*? c_p=([0-9.e+-]+) mu\(K_p\)>=([0-9.e+-]+)', cert):
    mine[int(m.group(1))] = dict(logPi=float(m.group(2)), Pi=float(m.group(3)), delta=float(m.group(4)),
                                 cp=float(m.group(5)), mu=float(m.group(6)))
for m in re.finditer(r'l\*=(\d+) l\*-k0=(\d+)', cert):
    pass
lst = re.findall(r'l\*=\d+ l\*-k0=(\d+)', cert)
for p, l in zip(sorted(mine), lst):
    mine[p]['lstar'] = int(l)
print("§7.3 table vs independent recomputation:")
nb = 0
for p in sorted(tab):
    t = tab[p]; c = mine[p]
    checks = []
    checks.append(('logPi upper', c['logPi'] <= t['logPi']))
    checks.append(('delta upper', c['delta'] <= t['delta']))
    checks.append(('c_p lower', t['cp'] <= c['cp']))
    checks.append(('mu lower', t['mu'] <= c['mu']))
    checks.append(('mu = c_p/p^3', abs(c['mu'] - c['cp'] / p ** 3) < 1e-5 * c['mu']))
    checks.append(('l*-k0', t['lstar'] == c['lstar']))
    # tightness: printed c_p is the rounding down (3 sig. digits, or 4 at p=11)
    fails = [n for n, ok in checks if not ok]
    if fails:
        nb += 1
    print("  p=%2d logPi %.4g<=%.3g delta %.6f<=%.4g c_p %.6f>=%.4g mu %.5e>=%.3g l*-k0 %d=%d  %s" % (
        p, c['logPi'], t['logPi'], c['delta'], t['delta'], c['cp'], t['cp'], c['mu'], t['mu'], c['lstar'], t['lstar'],
        "OK" if not fails else "FAIL " + str(fails)))
print("§7.3: %d rows, %d with a failed check" % (len(tab), nb))

# --- assemble.log RESULT lines (after the fix)
for m in re.finditer(r'RESULT p=(\d+): Pi_A <= ([0-9.e+-]+); delta_A <= ([0-9.e+-]+)', alog):
    p = int(m.group(1)); Pi = float(m.group(2)); de = float(m.group(3))
    c = mine[p]
    agree = abs(c['Pi'] - Pi) < 1e-13 * Pi and abs(c['delta'] - de) < 1e-9 * de
    upper = (c['delta'] <= de)
    print("  assemble.log p=%d: Pi_A %.15g vs mine %.15g; delta_A %.11g vs mine %.13g  %s; printed delta is >= recomputed: %s" % (
        p, Pi, c['Pi'], de, c['delta'], "agree to all printed digits" if agree else "DIFFER", upper))

# --- schedules and explicit phase-2 windows, line by line against assemble.log
c = cert
pa = re.findall(r'assemble p=(\d+).*?phase 1: blocks (\[[^\]]*\]); k0 = (\d+)', alog, re.S)
pc = re.findall(r'p=(\d+) q1-1.*?phase1 b=(\[[^\]]*\]) k0=(\d+)', c, re.S)
print("phase-1 schedules and k0 identical for all %d primes: %s" % (len(pa), pa == pc))
wa = re.findall(r'l= *(\d+) blocks \((\d+),(\d+),(\d+)\] s=(\d+) N_W=(\d+) N=(\d+) I=(\d+): mu\(G\^c\)<=([0-9.e-]+) Bfr<=[0-9.e+-]+ ebar=([0-9.e+-]+)', alog)
wc = re.findall(r'l=(\d+) ph2 \((\d+),(\d+),(\d+)\] s=(\d+) N_W=(\d+) N=(\d+) I=(\d+) mu\(G\^c\)<=([0-9.e-]+) sqrtB=([0-9.e+-]+)', c)
same_int = len(wa) == len(wc) and all(x[:8] == y[:8] for x, y in zip(wa, wc))
badf = [(x, y) for x, y in zip(wa, wc) if abs(float(x[8]) - float(y[8])) > 2e-3 * float(y[8]) or abs(float(x[9]) - float(y[9])) > 2e-3 * float(y[9])]
print("explicit phase-2 windows: %d in assemble.log, %d recomputed; (l, blocks, s, N_W, N, I) identical: %s; mu(G^c) and eps_bar agree to printed precision in all but %d" % (
    len(wa), len(wc), same_int, len(badf)))
