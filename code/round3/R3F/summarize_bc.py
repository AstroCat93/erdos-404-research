#!/usr/bin/env python3
"""summarize_bc.py -- markdown tables for B3 (l2_dp logs) and C4 (kavg_l2 logs).  usage: summarize_bc.py DATA_DIR"""
import sys, glob, os, re

D = sys.argv[1]
print("### B3: exact L^2 shells (l2_dp.py)\n")
print("| p | N0 | K range | L2(K_max) = sum_{k<=K_max} Q(k) | max_k Q(k)/(N_k 2^{-n_k}) (at k) | Q(K_max)/(N 2^{-n}) |")
print("|---|---|---|---|---|---|")
for f in sorted(glob.glob(os.path.join(D, "b_l2dp_*.log")), key=lambda x: (int(re.search(r"_p(\d+)_", x).group(1)), x)):
    rows = []
    p = N0 = None
    for line in open(f):
        m = re.match(r"# l2_dp p=(\d+) N0=(\d+)", line)
        if m:
            p, N0 = m.group(1), m.group(2)
        w = line.split()
        if len(w) == 7 and w[0].isdigit():
            rows.append((int(w[0]), int(w[1]), float(w[2]), float(w[3]), float(w[5])))
    if not rows:
        continue
    km = max(rows, key=lambda r: r[4])
    print(f"| {p} | {N0} | 1..{rows[-1][0]} | {rows[-1][2]:.6g} | {km[4]:.4g} (k={km[0]}) | {rows[-1][4]:.4g} |")
print("\nper-level detail:")
for f in sorted(glob.glob(os.path.join(D, "b_l2dp_*.log"))):
    print(f"\n{os.path.basename(f)}:")
    for line in open(f):
        w = line.split()
        if len(w) == 7 and w[0].isdigit():
            print(f"  K={w[0]:>2} n_K={w[1]:>3} L2cum={float(w[2]):.6e} Q={float(w[3]):.4e} Q/random={float(w[5]):.4g}")

print("\n### C4: K'-averaging (kavg_l2.py)\n")
print("| p | t | H | c | units | failing (exact) | C3 bound on proportion failing | per-class C-S certified | max_K' L2 vs p^-M |")
print("|---|---|---|---|---|---|---|---|---|")
for f in sorted(glob.glob(os.path.join(D, "c_kavg_*.log"))):
    eps = cert = None
    for line in open(f):
        m = re.search(r"C3 bound: proportion of failing unit classes <= ([0-9.e+-]+) .*certified by per-class C-S .*: (\d+/\d+)", line)
        if m:
            eps, cert = m.group(1), m.group(2)
        m = re.match(r"p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=p\^(\d+)\s+units=(\d+)\s+failing\(exact\)=(\d+).*max L2=([0-9.e+-]+) vs p\^-M=([0-9.e+-]+)", line)
        if m:
            p, t, H, c, Me, u, fl, mx, pm = m.groups()
            print(f"| {p} | {t} | {H} | {c} | {u} | {fl} | {float(eps):.3g} | {cert} | {float(mx):.3g} vs {float(pm):.3g} |")
