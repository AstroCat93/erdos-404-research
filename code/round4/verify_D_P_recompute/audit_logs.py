#!/usr/bin/env python3
"""Audit of the round-2 certificate logs cited by Theorem P (note 10.2 table).
For every (p,t,H_t) and each of programs A, B (data/round2/logs_original/R3) and C
(data/round2/review/computation/logs), parse every per-class line and check that the
set of classes K mod p^c reported as covered (0 missing) is exactly the set of all
units mod p^c, and that no line reports a miss.  Header parameters (c, M) are also
checked against c = v_p((H-1)!), M = t + c."""
import glob, os, re, sys
BASE = "/home/user/erdos-404-research/data/round2"
CERT = {7: [4, 7, 19, 26, 28, 34], 11: [5, 10, 18, 22, 30, 33], 13: [6, 10, 19, 24, 32, 35, 39],
        17: [5, 11, 16, 25, 30, 34, 43], 19: [5, 12, 17, 27, 31, 35], 23: [7, 12, 18, 23, 33, 37]}

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def files_for(prog, p, t, H):
    if prog == "A":
        f = glob.glob(f"{BASE}/logs_original/R3/U_p{p}_t{t}_H{H}_A.log")
        if (p, t, H) == (13, 7, 39): f += glob.glob(f"{BASE}/logs_original/R3/R1_A_cov_13_7_39_all.log")
    elif prog == "B":
        f = glob.glob(f"{BASE}/logs_original/R3/U_p{p}_t{t}_H{H}_B*.log")
        if (p, t, H) == (13, 7, 39): f += glob.glob(f"{BASE}/logs_original/R3/R1_B_cov_13_7_39_all_lift1.log")
    else:
        f = glob.glob(f"{BASE}/review/computation/logs/U_p{p}_t{t}_H{H}.log")
        if (p, t, H) == (17, 7, 43): f += glob.glob(f"{BASE}/review/computation/logs/U17_t7_H43_*.log")
    return sorted(set(f))

line_re = re.compile(r"^([ABC]) p=(\d+) t=(\d+) H=(\d+)\b.*?\bK=(\d+)\b.*?\b(missing|notcovered|miss)=(\d+)")
ok_all = True
for p, Hs in CERT.items():
    for t0, H in enumerate(Hs):
        t = t0 + 1
        c = sum(vp(s, p) for s in range(1, H))
        pc = p ** c
        units = {k for k in range(pc) if pc == 1 or k % p}
        if pc == 1: units = {0}
        row = []
        for prog in "ABC":
            fs = files_for(prog, p, t, H)
            seen, bad = set(), 0
            hdr_ok = True
            for f in fs:
                for l in open(f, errors="replace"):
                    if l.startswith("#") and f"p={p} " in l and f" H={H} " in l:
                        m = re.search(r"\bc=(\d+)", l); mm = re.search(r"\bM=(\d+)", l)
                        if (m and int(m.group(1)) != c) or (mm and int(mm.group(1)) != t + c): hdr_ok = False
                    m = line_re.match(l)
                    if not m: continue
                    if (int(m.group(2)), int(m.group(3)), int(m.group(4))) != (p, t, H): continue
                    K, miss = int(m.group(5)), int(m.group(7))
                    if miss: bad += 1
                    else: seen.add(K % pc)
            full = (seen == units) and bad == 0 and hdr_ok and fs
            row.append(f"{prog}: files={len(fs)} classes_covered={len(seen)}/{len(units)} misses={bad} hdr={'ok' if hdr_ok else 'BAD'} {'OK' if full else 'INCOMPLETE'}")
            if not full: ok_all = False
        print(f"Cov({p},{t},{H}) c={c} M={t+c}: " + " | ".join(row))
print("AUDIT", "OK: every cited certificate is present for all unit classes in A, B and C" if ok_all else "NOT COMPLETE")
