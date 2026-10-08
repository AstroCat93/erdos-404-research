# s7_crosscheck.py -- cross-check the C programs (zdens: U_k, gdens: G_k) against independent Python:
#  U_k via the carry dynamics of s2 (g(a,p)>=k iff f(a,p) >= v_p(a!)+k), for two lifts a of each class;
#  G_k via direct subset sums of prod_{l<=j}(r+l) mod p^k.
import subprocess, sys
from s2_dynamics import ge_K

def vfact(n, p):
    s = 0
    while n: n //= p; s += n
    return s

def run(prog, p, k):
    out = subprocess.run([f"./{prog}", str(p), str(k), "100000"], capture_output=True, text=True).stdout
    sets = {}
    lines = out.strip().split("\n")
    for i, line in enumerate(lines):
        if line.startswith(f"p={p} k="):
            kk = int(line.split()[1][2:])
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if "= {" in nxt:
                body = nxt.split("{")[1].split("}")[0]
                sets[kk] = set(int(x) for x in body.split(",") if x)
    return sets

def G_py(r, p, k):
    M = p ** k; S = {0}; c = 1
    j = 0
    while True:
        if j > 0: c = c * (r + j) % M
        if c == 0: break
        S |= {(s + c) % M for s in S}
        j += 1
    return len(S) == M

ok = True
for p, kmax in [(2, 8), (3, 5), (5, 3), (7, 2)]:
    U = run("zdens", p, kmax); G = run("gdens", p, kmax)
    for k in range(1, kmax + 1):
        for r in range(p ** k):
            for a in (r + p ** k, r + 2 * p ** k):
                inU = ge_K(a, p, vfact(a, p) + k)
                if inU != (r in U.get(k, set())): ok = False; print("U mismatch", p, k, r, a)
            if G_py(r, p, k) != (r in G.get(k, set())): ok = False; print("G mismatch", p, k, r)
    print(f"p={p}: checked k<= {kmax}", "OK" if ok else "MISMATCH")
print("ALL OK" if ok else "SOME MISMATCH")
