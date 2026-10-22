"""cm8: Prop D pointwise at the largest exactly computable levels, on random composite windows at
p = 7, 11, 13, 17, 19, 23, with the tiny excesses that make phase 1 cheap at large p compared directly:
   p^K Coll_K(x) - 1  <=  PropD(K) - 1     and     eps(x) = p^K Coll_K - p^D Coll_D  <=  PropD(K) - 1,
and the chi^2 form p^D Coll_D - 1 <= PropD(D) - 1 (window [n, N)).  Exact: signed DP mod p^K over all
H = N' - n elements of the composite window (all digits signed), CRT counts.
x kinds: rand; neg1/neg2/neg3 (gate of depth s at n+1, n+2, n+3: deep gates at window starts);
int (x a small non-negative integer; factorial pattern); deepmid (deep gate at n+p+2).
usage: python3 cm8_propD_window.py p SEED NW KMAX DMAXDEPTH
"""
import sys, random
from fractions import Fraction
import cm_lib as L

p, seed, NW, KMAX, DD = map(int, sys.argv[1:6])
random.seed(seed)
EP = 50
PE = p ** EP
C = L.Consts(p, sx=(5 if p > 13 else 6))
kinds = ["rand", "neg1", "neg2", "neg3", "int", "deepmid"]
cnt = dict(win=0, okK=0, okeps=0, okchi=0)
maxr = 0.0
tries = 0
while cnt["win"] < NW and tries < 40 * NW:
    tries += 1
    kind = kinds[tries % len(kinds)]
    n = random.randrange(2 * p, 8 * p)
    if kind == "rand":
        x = random.randrange(PE)
    elif kind.startswith("neg"):
        d = int(kind[3]); s = random.randrange(1, DD + 1)
        x = (-(n + d) + p ** s * random.randrange(1, PE)) % PE
    elif kind == "int":
        x = random.randrange(0, 3 * p * p)
    else:                       # deepmid: a deep gate one block into the window
        s = random.randrange(2, DD + 2)
        x = (-(n + p + 2) + p ** s * random.randrange(1, PE)) % PE
    # composite window with level exactly K at N' and D at N
    K = random.randrange(2, KMAX + 1)
    gl, lev, Np = [], 0, n
    while lev < K:
        Np += 1
        if (x + Np) % p == 0:
            s = L.vp((x + Np) % PE, p); gl.append((Np, s)); lev += s
    if lev != K or len(gl) < 2:
        continue
    jg = random.randrange(len(gl) - 1)
    D = sum(s for _, s in gl[:jg + 1])
    N = random.randrange(gl[jg][0], gl[jg + 1][0])
    H = Np - n
    npr = 2 if 2 * H < 118 else (3 if 2 * H < 178 else 4)
    dp = L.JointDP(p, K, 0, npr)
    y = 1
    for c in range(H):
        if c >= 1:
            y = y * (x + n + c) % PE
        dp.step(y, 0)
    tot = 4 ** H
    PK = Fraction(p ** K * dp.count(K, 0), tot)
    PDc = Fraction(p ** D * dp.count(D, 0), tot)
    eps = PK - PDc
    b = L.propDE_block(p, gl, n, Np, K, C); bK = Fraction(int(b.numerator), int(b.denominator))
    # chi^2 of [n, N): its own DP (elements c < N - n), level D
    dp2 = L.JointDP(p, D, 0, npr)
    y = 1
    for c in range(N - n):
        if c >= 1:
            y = y * (x + n + c) % PE
        dp2.step(y, 0)
    chi = Fraction(p ** D * dp2.count(D, 0), 4 ** (N - n))
    glD = [(g, s) for g, s in gl if g <= N]
    bD = L.propDE_block(p, glD, n, N, D, C); bDF = Fraction(int(bD.numerator), int(bD.denominator))
    cnt["win"] += 1
    cnt["okK"] += PK <= bK
    cnt["okeps"] += eps <= bK - 1
    cnt["okchi"] += chi <= bDF
    if not (PK <= bK and eps <= bK - 1 and chi <= bDF):
        print(f"PROP D FAIL p={p} kind={kind} x={x} n={n} N={N} N'={Np} gates={gl}: pK={PK} bound={bK} eps={eps} chi={chi} boundD={bDF}")
    if bK > 1:
        maxr = max(maxr, float((PK - 1) / (bK - 1)))
    if cnt["win"] <= 12 or cnt["win"] % 10 == 0:
        print(f"win {cnt['win']} kind={kind} n={n} N={N} N'={Np} D={D} K={K} gates={gl}: p^K Coll_K - 1 = {float(PK - 1):.6e}, eps = {float(eps):.6e}, "
              f"Prop D - 1 = {float(bK - 1):.6e};  chi^2 = {float(chi - 1):.4e} <= {float(bDF - 1):.4e}", flush=True)
print(f"RESULT p={p}: {cnt['win']} windows; p^K Coll_K <= Prop D: {cnt['okK']}; eps <= Prop D - 1: {cnt['okeps']}; chi^2 form: {cnt['okchi']}; "
      f"max (p^K Coll_K - 1)/(Prop D - 1) = {maxr:.6f}")
