# Assemble every number of track T4 into data/results.json (machine-readable).
import os, re, json, glob, csv
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = {"generated": "2026-10-12", "track": "T4-computations (round 3, Erdos #404)",
     "definitions": {
         "M_G": "max{b : v_p(b!) < G}; least cutoff with pi_b(x) == 0 mod p^G for all x in Z_p and all b > M_G (Lemma 1 of writeup)",
         "N_G(x)": "#{B subset [1,M_G] : p^G | 1 + sum_{b in B} pi_b(x)}, exact, depends on x mod p^G",
         "Z_G(x)": "p^G 2^{-M_G} N_G(x)",
         "maxv(x)": "max_{1<=i<=M_G} v_p(x+i)",
         "N(A,G)": "#{1<=a<=A : g_2(a) >= G}",
         "delta_G(2)": "Haar measure of {x in Z_2 : g_2(x) >= G}; Monte Carlo rows are estimates with binomial standard errors",
         "c_p": "max over units xi mod p of prod_{r=0}^{p-1} |cos(pi xi r!/p)|",
         "Lunit(p,i)": "sum over units xi mod p^i of prod_{u<p} |cos(pi xi e_u / p^i)|, e_u = (-1)^u (p-1)!/u!",
         "I_p": "int_0^1 prod_u |cos(pi e_u theta)| dtheta (Gauss-Legendre on unit pieces; exact structure, double precision)",
     }}
# (1) annealed
ann = []
for fn in sorted(glob.glob(W + "/data/annealed_p*_G*.txt")):
    t = open(fn).read(); m = re.search(r"# p=(\d+) G=(\d+) M_G=(\d+) p\^G=(\d+)", t)
    if not m or "total" not in t: continue
    p, G, MG, pG = map(int, m.groups())
    rows = [dict(zip(["maxv", "classes", "surviving", "sumN", "sumN2", "maxN"], map(int, l.split()[1:]))) for l in t.splitlines() if l.startswith("row ")]
    tot = re.search(r"total classes=(\d+) surviving=(\d+) sumN=(\d+) sumN2=(\d+) maxN=(\d+)", t)
    ann.append({"p": p, "G": G, "M_G": MG, "classes": int(tot.group(1)), "surviving": int(tot.group(2)), "sumN": tot.group(3), "sumN2": tot.group(4), "maxN": int(tot.group(5)), "by_maxv": rows})
R["annealed_raw"] = sorted(ann, key=lambda r: (r["p"], r["G"]))
if os.path.exists(W + "/data/annealed_summary.tsv"):
    R["annealed_conditioned"] = list(csv.DictReader(open(W + "/data/annealed_summary.tsv"), delimiter="\t"))
# (2) survivors
if os.path.exists(W + "/data/survivors_NAG.tsv"):
    R["survivors_NAG"] = list(csv.DictReader(open(W + "/data/survivors_NAG.tsv"), delimiter="\t"))
surv = {}
for fn in sorted(glob.glob(W + "/data/surv_cap*.txt")):
    cap = int(fn.split("cap")[1].split(".")[0]); d = {}
    for l in open(fn):
        if l[0] != "#" and l.strip(): a, g = map(int, l.split()); d[a] = g
    if d: surv[cap] = d
if surv:
    top = max(surv); R["g2_capped_a_le_4096"] = {"cap": top, "values": {str(a): g for a, g in sorted(surv[top].items()) if g > 0}}
if os.path.exists(W + "/kitamura/kitamura_N256.txt"):
    R["kitamura_N256_from_exact_table"] = [l.split() for l in open(W + "/kitamura/kitamura_N256.txt") if l[0] != "#"]
# (3) Monte Carlo
if os.path.exists(W + "/data/delta_G2_montecarlo.tsv"):
    R["delta_G2_montecarlo"] = list(csv.DictReader(open(W + "/data/delta_G2_montecarlo.tsv"), delimiter="\t"))
# (4) constants
if os.path.exists(W + "/data/constants_cp.txt"):
    R["c_p"] = [dict(zip(["p", "c_p", "geomean_xi", "argmax_xi", "n_argmax", "(2/pi)^p", "c_p^(1/p)"], l.split())) for l in open(W + "/data/constants_cp.txt") if l[0] != "#"]
gs = []
for fn in sorted(glob.glob(W + "/data/gatesum_p*.txt")):
    for l in open(fn):
        m = re.match(r"p=(\d+) i=(\d+) p\^i=(\d+) Lunit=(\S+) Lall=(\S+) Lunit/units=(\S+) Lall/p\^i=(\S+) maxterm=(\S+) argmax=(\d+) randomphase_budget=(\S+)", l)
        if m: gs.append(dict(zip(["p", "i", "p^i", "Lunit", "Lall", "Lunit_per_unit", "Lall_per_pi", "maxterm", "argmax", "randomphase_budget"], m.groups())))
        m = re.match(r"p=(\d+) integral I_p=(\S+) \(ngl=(\d+)", l)
        if m: gs.append({"p": m.group(1), "I_p": m.group(2), "ngl": m.group(3)})
R["gate_block_sums"] = gs
json.dump(R, open(W + "/data/results.json", "w"), indent=1)
print("wrote results.json with keys", list(R))
