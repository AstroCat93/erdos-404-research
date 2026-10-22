# T4b-finish (2026-10-20): independent final post-processing of track T4 (round 3, Erdos #404).
# Reads ONLY the raw program outputs (data/annealed_p*_G*.txt, data/surv_cap*.txt, data/mc_cap*.txt,
# data/gatesum_p*.txt), the exact p=2 census of the note (review/computation/census_p2_32.out) and
# Kitamura's exact table (kitamura/p2_exact_table_1_256.csv); shares no code with src/*_post.py.
# Writes data/results_final.json and prints every table used in writeup_addendum.md.
import os, re, glob, json, math, csv, sys
from fractions import Fraction as Fr
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = os.path.normpath(os.path.join(W, "..", "..", "publish-erdos404"))
R = {"generated": "2026-10-20 (T4b-finish)", "source_runs": "2026-10-12 (src/*), 2026-10-20 (code/*)"}
def pr(*a): print(*a); sys.stdout.flush()

# ---------------------------------------------------------------- (0) exact p=2 census G<=32
census = {}
for l in open(NOTE + "/review/computation/census_p2_32.out"):
    m = re.match(r"p=2 G=(\d+) count=(\d+)", l)
    if m: census[int(m.group(1))] = Fr(int(m.group(2)), 2 ** int(m.group(1)))
assert census[29] == Fr(60888286, 2 ** 29) and census[32] == Fr(436523876, 2 ** 32)
R["exact_census_p2"] = {str(G): [str(census[G].numerator), float(census[G])] for G in sorted(census)}

# ---------------------------------------------------------------- (1) annealed moments, incl. new G
ann = {}
for fn in sorted(glob.glob(W + "/data/annealed_p*_G*.txt")):
    t = open(fn).read()
    m = re.search(r"# p=(\d+) G=(\d+) M_G=(\d+) p\^G=(\d+)", t)
    tot = re.search(r"total classes=(\d+) surviving=(\d+) sumN=(\d+) sumN2=(\d+) maxN=(\d+)", t)
    if not m or not tot: pr("INCOMPLETE:", fn); continue
    p, G, MG, pG = map(int, m.groups())
    assert pG == p ** G
    # M_G = max{b : v_p(b!) < G}
    def vfact(b):
        s = 0; q = p
        while q <= b: s += b // q; q *= p
        return s
    MGchk = max(b for b in range(0, p * G + 1) if vfact(b) < G); assert MGchk == MG, (p, G, MG, MGchk)
    rows = [tuple(map(int, l.split()[1:])) for l in t.splitlines() if l.startswith("row ")]
    cl, sv, S1, S2, mx = map(int, tot.groups())
    assert sum(r[1] for r in rows) == cl == pG and sum(r[2] for r in rows) == sv and sum(r[3] for r in rows) == S1 and sum(r[4] for r in rows) == S2 and max(r[5] for r in rows) == mx
    ann[(p, G)] = (MG, rows, cl, sv, S1, S2, mx)
def moments(p, G, K=None):
    MG, rows, cl, sv, S1, S2, mx = ann[(p, G)]
    sel = rows if K is None else [r for r in rows if r[0] <= K]
    cnt = sum(r[1] for r in sel); s = sum(r[2] for r in sel); s1 = sum(r[3] for r in sel); s2 = sum(r[4] for r in sel)
    if cnt == 0: return None
    pG = p ** G
    EZ = Fr(s1 * pG, 2 ** MG * cnt); EZ2 = Fr(s2 * pG * pG, 4 ** MG * cnt)
    return dict(measure=Fr(cnt, pG), delta=Fr(s, cnt), EZ=EZ, EZ2=EZ2, ratio=EZ2 / EZ / EZ, EZ2_over_pG4=EZ2 / Fr(pG, 4), maxZ=Fr(max(r[5] for r in sel) * pG, 2 ** MG))
pr("\n== (1a) annealed moments, all classes (exact rationals -> floats)")
pr("p G M_G delta_G EZ EZ2 ratio EZ2/(p^G/4) E[Z|Z>0]")
R["annealed_all"] = []
for (p, G) in sorted(ann):
    m = moments(p, G)
    R["annealed_all"].append(dict(p=p, G=G, M_G=ann[(p, G)][0], delta=float(m["delta"]), delta_exact=f"{ann[(p,G)][3]}/{p}^{G}", EZ=float(m["EZ"]), EZ2=float(m["EZ2"]), ratio=float(m["ratio"]), EZ2_over_pG4=float(m["EZ2_over_pG4"]), EZ_given_surv=float(m["EZ"] / m["delta"]), maxZ=float(m["maxZ"])))
    pr(f"{p} {G} {ann[(p,G)][0]} {float(m['delta']):.7f} {float(m['EZ']):.4f} {float(m['EZ2']):.5g} {float(m['ratio']):.5g} {float(m['EZ2_over_pG4']):.4f} {float(m['EZ']/m['delta']):.2f}")
# Proposition 2 check: EZ2 >= p^G/4 for every case
assert all(moments(p, G)["EZ2_over_pG4"] >= 1 for (p, G) in ann)
pr("Proposition 2 (EZ^2 >= p^G/4) holds in every computed case:", len(ann), "cases")
# linear growth of EZ: slopes between the top two G per p
R["EZ_slopes"] = {}
for p in (2, 3, 5, 7):
    Gs = sorted(G for (q, G) in ann if q == p)
    g1, g2 = Gs[-2], Gs[-1]
    sl = float(moments(p, g2)["EZ"] - moments(p, g1)["EZ"]) / (g2 - g1)
    R["EZ_slopes"][str(p)] = dict(G1=g1, G2=g2, slope=sl)
    pr(f"p={p}: EZ slope between G={g1},{g2}: {sl:.4f}")
# (1b) conditioned moments at the deepest G for each p, several K
pr("\n== (1b) conditioned moments E[.|maxv<=K] at every G, for fixed K (p,K) pairs of writeup 1.5 plus the new G")
R["annealed_conditioned"] = []
plan = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5], 7: [2, 3, 4]}
for p in plan:
    Gs = sorted(G for (q, G) in ann if q == p)
    for K in plan[p]:
        line = []
        for G in Gs:
            m = moments(p, G, K)
            if m is None: continue
            R["annealed_conditioned"].append(dict(p=p, K=K, G=G, measure=float(m["measure"]), delta_cond=float(m["delta"]), EZ=float(m["EZ"]), EZ2=float(m["EZ2"]), ratio=float(m["ratio"])))
            if G >= Gs[-5] if len(Gs) >= 5 else True: line.append(f"G={G}: meas {float(m['measure']):.3f} EZ {float(m['EZ']):.3f} EZ2 {float(m['EZ2']):.4g} ratio {float(m['ratio']):.3f}")
        pr(f"p={p} K={K}: " + " | ".join(line))
# (1c) bucket contributions at the deepest G
pr("\n== (1c) per-maxv bucket contributions to EZ at the deepest G")
R["bucket_contrib_deepest"] = {}
for p in (2, 3, 5, 7):
    G = max(G for (q, G) in ann if q == p); MG, rows = ann[(p, G)][0], ann[(p, G)][1]
    c = {r[0]: float(Fr(r[3], 2 ** MG)) for r in rows}
    R["bucket_contrib_deepest"][str(p)] = dict(G=G, contrib=c)
    pr(f"p={p} G={G}: " + " ".join(f"{v}:{c[v]:.4f}" for v in sorted(c)))

# ---------------------------------------------------------------- (2) survivors N(A,G) and Kitamura
surv = {}
for fn in sorted(glob.glob(W + "/data/surv_cap*.txt")):
    cap = int(re.search(r"cap(\d+)", fn).group(1)); d = {}
    for l in open(fn):
        if l[0] != "#" and l.strip(): a, g = map(int, l.split()); d[a] = g
    surv[cap] = d
caps = sorted(surv); pr("\n== (2) survivor caps:", caps, "entries:", [len(surv[c]) for c in caps])
assert all(len(surv[c]) == 4096 for c in caps)
ovf = {c: [a for a in surv[c] if surv[c][a] < 0] for c in caps}; pr("overflows per cap:", {c: len(v) for c, v in ovf.items()})
mism = 0
for i in range(len(caps)):
    for j in range(i + 1, len(caps)):
        c1, c2 = caps[i], caps[j]
        mism += sum(1 for a in range(1, 4097) if surv[c1][a] != min(surv[c2][a], c1))
pr("cap-consistency mismatches over all cap pairs (g_c1 == min(g_c2,c1)):", mism)
# g_2(a) for odd a is 0 (Lemma: 1 + sum of even terms...). check: all odd a have g=0 at every cap
pr("odd a with g>0 (should be none):", [a for a in range(1, 4097, 2) if surv[4094][a] != 0][:5])
# locality check: for G <= 12, N(A,G)/A == delta_G exactly (A multiple of 2^G)
g = surv[4094]
def N(A, G): return sum(1 for a in range(1, A + 1) if g[a] >= G)
for G in range(1, 13):
    for A in (256, 1024, 4096):
        if A % 2 ** G == 0: assert Fr(N(A, G), A) == census[G], (G, A)
pr("locality check N(A,G)/A == delta_G exact for G<=12 (A multiple of 2^G): OK")
Gs = [1, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1022, 1024, 1536, 2046, 2048, 3072, 4094]
R["survivors_NAG"] = []
pr("G N256 N1024 N4096 | N*G/A (256,1024,4096) | N*sqrtG/A (256,1024,4096) | delta_G exact")
for G in Gs:
    n = [N(A, G) for A in (256, 1024, 4096)]
    row = dict(G=G, N256=n[0], N1024=n[1], N4096=n[2], NG_over_A=[n[i] * G / A for i, A in enumerate((256, 1024, 4096))], NsqrtG_over_A=[n[i] * math.sqrt(G) / A for i, A in enumerate((256, 1024, 4096))], delta_exact=float(census[G]) if G in census else None)
    R["survivors_NAG"].append(row)
    pr(f"{G:5d} {n[0]:4d} {n[1]:4d} {n[2]:4d} | " + " ".join(f"{x:6.3f}" for x in row["NG_over_A"]) + " | " + " ".join(f"{x:6.4f}" for x in row["NsqrtG_over_A"]) + (f" | {float(census[G]):.6f}" if G in census else ""))
deep = sorted(a for a in g if g[a] >= 4094); pr("a<=4096 with g_2(a)>=4094:", deep); R["deep_survivors_cap4094"] = deep
# Kitamura exact table: per-a comparison and N(256,G) comparison
def v2f(a):
    s = 0
    while a: a //= 2; s += a
    return s
kit = {}
for r in csv.DictReader(open(W + "/kitamura/p2_exact_table_1_256.csv")):
    kit[int(r["a"])] = (r["status"], int(r["value"]) - v2f(int(r["a"])))
assert len(kit) == 256
bad = [a for a in kit if kit[a][0] == "exact" and kit[a][1] != g[a] and not (kit[a][1] >= 4094 and g[a] == 4094)]
bad2 = [a for a in kit if kit[a][0] != "exact" and g[a] < 4094]
pr("Kitamura statuses:", sorted(set(s for s, _ in kit.values())), "; non-exact rows:", {a: kit[a] for a in kit if kit[a][0] != "exact"})
pr("per-a mismatches (exact rows, cap 4094):", bad, "; lower-bound rows not survived to 4094:", bad2)
R["kitamura_per_a_check"] = dict(exact_rows=sum(1 for a in kit if kit[a][0] == "exact"), mismatches=bad, lower_bound_rows={str(a): kit[a] for a in kit if kit[a][0] != "exact"}, lower_bound_rows_not_survived=bad2)
R["kitamura_N256_vs_ours"] = []
pr("G  N(256,G) Kitamura  ours(cap4094)")
for G in [1, 2, 4, 8, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048, 4094]:
    nk = sum(1 for a in kit if (kit[a][1] >= G)); no = N(256, G)
    R["kitamura_N256_vs_ours"].append(dict(G=G, kitamura=nk, ours=no)); pr(f"{G:5d} {nk:4d} {no:4d}" + ("" if nk == no else "  MISMATCH"))

# ---------------------------------------------------------------- (3) Monte Carlo
runs = {}
for fn in sorted(glob.glob(W + "/data/mc_cap*.txt")):
    t = open(fn).read(); m = re.search(r"ns=(\d+) seed=(\d+) CAP=(\d+) threads=(\d+) maxpop=(\d+) overflow_samples=(\d+)", t)
    ns, seed, cap, th, mp, ov = map(int, m.groups()); d = {}
    for l in t.splitlines():
        mm = re.match(r"k=(\d+) surv=(\d+) frac=", l)
        if mm: d[int(mm.group(1))] = int(mm.group(2))
    assert len(d) == cap + 1 and d[0] == ns and all(d[k] >= d[k + 1] for k in range(cap)), fn
    runs[cap] = dict(ns=ns, seed=seed, maxpop=mp, overflow=ov, surv=d)
pr("\n== (3) Monte Carlo runs:", {c: (runs[c]["ns"], runs[c]["seed"], runs[c]["maxpop"], runs[c]["overflow"]) for c in sorted(runs)})
assert all(runs[c]["overflow"] == 0 for c in runs)
# (3a) census sanity check at EVERY G<=32 for every run: z = (phat - delta)/sqrt(delta(1-delta)/ns)
zs = []; worst = []
for c in sorted(runs):
    ns, d = runs[c]["ns"], runs[c]["surv"]
    for G in range(1, 33):
        de = float(census[G]); ph = d[G] / ns; z = (ph - de) / math.sqrt(de * (1 - de) / ns); zs.append((abs(z), c, G, ph, de, z))
zs.sort(reverse=True)
R["mc_census_check"] = dict(tests=len(zs), max_abs_z=zs[0][0], n_abs_z_gt2=sum(1 for z in zs if z[0] > 2), n_abs_z_gt3=sum(1 for z in zs if z[0] > 3), worst5=[dict(cap=c, G=G, phat=ph, exact=de, z=z) for _, c, G, ph, de, z in zs[:5]])
pr(f"census check: {len(zs)} (run,G) tests, G=1..32; max|z|={zs[0][0]:.2f}; #|z|>2: {R['mc_census_check']['n_abs_z_gt2']}; #|z|>3: {R['mc_census_check']['n_abs_z_gt3']}")
pr("worst 5:", [(c, G, round(ph, 5), round(de, 5), round(z, 2)) for _, c, G, ph, de, z in zs[:5]])
pr("per run: max|z| over G<=32:", {c: round(max(z[0] for z in zs if z[1] == c), 2) for c in sorted(runs)})
# (3b) estimates: single best run (smallest stderr) and pooled (all runs with cap>=G, independent seeds)
keyG = [64, 96, 126, 128, 192, 256, 384, 512, 768, 1024, 1536, 2046]
best = {}; pooled = {}
for G in keyG:
    cand = [(c, runs[c]) for c in runs if c >= G]
    b = max(cand, key=lambda x: x[1]["ns"]); ph = b[1]["surv"][G] / b[1]["ns"]; se = math.sqrt(ph * (1 - ph) / b[1]["ns"])
    best[G] = (ph, se, b[0])
    S = sum(r["surv"][G] for _, r in cand); n = sum(r["ns"] for _, r in cand); pp = S / n; pooled[G] = (pp, math.sqrt(pp * (1 - pp) / n), n)
R["delta_G2_estimates"] = [dict(G=G, delta_best=best[G][0], stderr_best=best[G][1], run_cap=best[G][2], delta_pooled=pooled[G][0], stderr_pooled=pooled[G][1], pooled_samples=pooled[G][2], delta_G_times_G=best[G][0] * G, delta_G_times_sqrtG=best[G][0] * math.sqrt(G), two_delta_G_times_G=2 * best[G][0] * G) for G in keyG]
pr("G  delta(best run) +- se [cap]   delta(pooled) +- se   delta*G  delta*sqrtG  2*delta*G")
for G in keyG:
    pr(f"{G:5d} {best[G][0]:.5f} +- {best[G][1]:.5f} [{best[G][2]}]  {pooled[G][0]:.5f} +- {pooled[G][1]:.5f}  {best[G][0]*G:.3f} {best[G][0]*math.sqrt(G):.4f} {2*best[G][0]*G:.2f}")
# (3c) fits delta ~ C G^-c, weighted (1/se^2 in log space) and unweighted, on [64,2046] and sub-ranges; best-run values
def fit(Gsel, src):
    xs = [math.log(G) for G in Gsel]; ys = [math.log(src[G][0]) for G in Gsel]
    out = {}
    for name, ws in (("weighted", [(src[G][0] / src[G][1]) ** 2 for G in Gsel]), ("unweighted", [1.0] * len(Gsel))):
        sw = sum(ws); mx = sum(w * x for w, x in zip(ws, xs)) / sw; my = sum(w * y for w, y in zip(ws, ys)) / sw
        sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs)); c = -sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys)) / sxx
        C = math.exp(my + c * mx)
        res = [y - (math.log(C) - c * x) for x, y in zip(xs, ys)]
        chi2 = sum(w * r * r for w, r in zip(ws, res)) if name == "weighted" else None
        out[name] = dict(C=C, c=c, stderr_c=(1 / math.sqrt(sxx) if name == "weighted" else None), chi2=chi2, dof=len(Gsel) - 2, max_abs_resid=max(abs(r) for r in res))
    return out
R["mc_fits"] = {}
for lo in (64, 128, 256, 512):
    sel = [G for G in keyG if G >= lo and G != 126]
    f = fit(sel, best); R["mc_fits"][f"best_run_G>={lo}"] = f
    pr(f"fit on G in [{lo},2046] (best runs, {len(sel)} pts): weighted C={f['weighted']['C']:.3f} c={f['weighted']['c']:.3f}+-{f['weighted']['stderr_c']:.3f} chi2/dof={f['weighted']['chi2']:.1f}/{f['weighted']['dof']}; unweighted C={f['unweighted']['C']:.3f} c={f['unweighted']['c']:.3f}")
    f2 = fit(sel, pooled); R["mc_fits"][f"pooled_G>={lo}"] = f2
    pr(f"      same, pooled estimates: weighted C={f2['weighted']['C']:.3f} c={f2['weighted']['c']:.3f}+-{f2['weighted']['stderr_c']:.3f} chi2/dof={f2['weighted']['chi2']:.1f}/{f2['weighted']['dof']}")
# fit of the form delta = a/G + b/G^2 on G>=256 (unweighted LS in delta*G): delta*G = a + b/G
sel = [G for G in keyG if G >= 256]
xs = [1 / G for G in sel]; ys = [best[G][0] * G for G in sel]; ws = [(G / best[G][1]) ** 2 for G in sel]
sw = sum(ws); mx = sum(w * x for w, x in zip(ws, xs)) / sw; my = sum(w * y for w, y in zip(ws, ys)) / sw
b = sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys)) / sum(w * (x - mx) ** 2 for w, x in zip(ws, xs)); a = my - b * mx
R["mc_fits"]["a_over_G_plus_b_over_G2_G>=256"] = dict(a=a, b=b); pr(f"fit delta*G = a + b/G on G>=256 (weighted): a={a:.3f} b={b:.1f}")
# local exponents between consecutive key G (best runs), with error propagation
loc = []
Gk = [G for G in keyG if G != 126]
for i in range(len(Gk) - 1):
    G1, G2 = Gk[i], Gk[i + 1]; p1, s1 = best[G1][:2]; p2, s2 = best[G2][:2]
    c = -math.log(p2 / p1) / math.log(G2 / G1); sc = math.sqrt((s1 / p1) ** 2 + (s2 / p2) ** 2) / math.log(G2 / G1)
    loc.append(dict(G1=G1, G2=G2, c=c, stderr=sc)); pr(f"local exponent {G1}-{G2}: {c:.3f} +- {sc:.3f}")
R["mc_local_exponents"] = loc

# ---------------------------------------------------------------- (4) gate-block ratios
pr("\n== (4) gate-block L^1 sums")
R["gate_block"] = {}
for p in (5, 7, 11, 13):
    t = open(W + f"/data/gatesum_p{p}.txt").read()
    I = float(re.search(r"integral I_p=(\S+)", t).group(1)); ngl = int(re.search(r"ngl=(\d+)", t).group(1))
    rows = []
    for l in t.splitlines():
        m = re.match(r"p=(\d+) i=(\d+) p\^i=(\d+) Lunit=(\S+) Lall=(\S+)", l)
        if m:
            i = int(m.group(2)); Lu = float(m.group(4)); La = float(m.group(5)); B = p ** i * (1 - 1 / p) * I
            rows.append(dict(i=i, Lunit=Lu, Lall=La, budget=B, ratio_unit=Lu / B, ratio_all=La / (p ** i * I)))
    alt = {}
    for fn in glob.glob(W + f"/data/gatesum_p{p}_ngl*.txt"):
        tt = open(fn).read(); alt[re.search(r"ngl=(\d+)", tt).group(1)] = float(re.search(r"integral I_p=(\S+)", tt).group(1))
    R["gate_block"][str(p)] = dict(I_p=I, ngl=ngl, I_p_alt_ngl=alt, I_over_2pi_p=I / (2 / math.pi) ** p, rows=rows)
    pr(f"p={p}: I_p={I:.10f} (ngl={ngl}; alt {alt}) I_p/(2/pi)^p={I/(2/math.pi)**p:.5f}; Lunit/budget i=1..8: " + ", ".join(f"{r['ratio_unit']:.7f}" for r in rows) + "; Lall/(p^i I_p): " + ", ".join(f"{r['ratio_all']:.5f}" for r in rows))

json.dump(R, open(W + "/data/results_final.json", "w"), indent=1)
pr("\nwrote data/results_final.json keys:", list(R))
