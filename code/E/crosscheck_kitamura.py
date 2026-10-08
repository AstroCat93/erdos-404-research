"""Cross-check our exact g(a,p) (C pruned DP, capped) against Kitamura's published odd-prime landscape
and p=2 exact table.  Reads the CSVs as plain data (no third-party code is executed)."""
import csv, subprocess, sys, os
EXT = sys.argv[1]          # path to gate-community/ext
OUT = sys.argv[2]          # output dir
here = os.path.dirname(os.path.abspath(__file__))
caps = {3: 20, 5: 12, 7: 10, 11: 8, 13: 8}
def vpf(n, p):
    v = 0
    while n: n //= p; v += n
    return v
rows = list(csv.DictReader(open(f"{EXT}/erdos-404-odd-prime-landscape/data/p35_ignition_landscape.csv"))) + \
       list(csv.DictReader(open(f"{EXT}/erdos-404-odd-prime-landscape/data/high_prime_ignition_landscape.csv")))
byp = {}
for r in rows: byp.setdefault(int(r['p']), []).append(r)
summary = []
for p, rs in sorted(byp.items()):
    amax = max(int(r['a']) for r in rs)
    cap = caps[p]
    out = subprocess.run([f"{here}/gtab", "gtab", str(p), "1", str(amax), str(cap)], capture_output=True, text=True).stdout.split()
    ours = {int(out[i]): int(out[i + 1]) for i in range(0, len(out), 2)}
    with open(f"{OUT}/gtable_p{p}_a1-{amax}_cap{cap}.txt", "w") as fh:
        fh.write(f"# p={p}: a, min(g(a,p),{cap}), v_p(a!)   [g = f - v_p(a!); value {cap} means g >= {cap}]\n")
        for a in range(1, amax + 1): fh.write(f"{a} {ours[a]} {vpf(a,p)}\n")
    agree = dis = 0; notes = []
    for r in rs:
        a = int(r['a']); st = r['status']
        if st in ('finite_exact_positive', 'finite_exact_g0', 'trivial_blocked_exact'):
            if ours[a] == int(r['g']): agree += 1
            else: dis += 1; notes.append((a, st, r['g'], ours[a]))
        elif st == 'ignited_candidate':
            if ours[a] >= cap: agree += 1
            else: dis += 1; notes.append((a, st, r['g'], ours[a]))
    surv = sum(1 for a in ours if ours[a] >= cap)
    summary.append((p, amax, cap, agree, dis, surv, notes[:20]))
    print(p, amax, 'cap', cap, 'agree', agree, 'disagree', dis, 'survivors(g>=cap)', surv, notes[:20]); sys.stdout.flush()
# p = 2 table
rows2 = list(csv.DictReader(open(f"{EXT}/erdos-404-p2-landscape/data/p2_exact_table_1_256.csv")))
out = subprocess.run([f"{here}/gtab", "gtab", "2", "1", "256", "40"], capture_output=True, text=True).stdout.split()
ours = {int(out[i]): int(out[i + 1]) for i in range(0, len(out), 2)}
ag = dis = 0; notes = []
for r in rows2:
    a = int(r['a']); g = int(r['value']) - vpf(a, 2)
    if g < 40:
        if ours[a] == g: ag += 1
        else: dis += 1; notes.append((a, g, ours[a]))
    else:
        if ours[a] == 40: ag += 1
        else: dis += 1; notes.append((a, g, ours[a]))
print('p=2 a<=256 cap 40: agree', ag, 'disagree', dis, notes[:10])
