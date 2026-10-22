"""t6: the algebra of Lemma Q's proof at deep levels (L up to ~120), exact p-adic arithmetic.
u: random p-adic integer (integer rep mod p^E), optionally with a planted deep gate.
 (0a) Step 0(a): for random signed digit strings (dt_0=1) and every block r with g_r < t:
      v(R_r - R_r^{<g_r}) >= L_r + 1, where R_r = pT' - pH_{g_r}T, R_r^{<g}=sum_{c<g} dt_c pi_c (pH_c - pH_{g_r}).
 (3)  Step 3 (1D block r): pi_{k'}(y) = pi_{k'}(-p) mod p^{s_{r+1}}, y = u + g_r  (and the control mod
      p^{s_{r+1}+1} must fail for some k').
 (4)  Step 4 (2D block r, s_{r+1}=1): the history-independent per-digit congruence
         pi_{g+k'}(u) * sum_{i=k'+1}^{p} p/(y+i)  ==  p^L (omega/alpha) pi_{k'}(-p)   mod p^{L+2}
      (omega = pi_g(u)/p^L, alpha = (y+p)/p), which is exactly R^{<g}_r - (pH_{g+p}-pH_g)T_{<g} - R^{<g+p}_{r+1}
      = p^L (omega/alpha) Ztilde with Ztilde = sum dt pi_{k'}(-p) mod p^2.  Control: mod p^{L+3} must fail.
 Also: the full identity R^{<g}_r - (pH_{g+p}-pH_g)T_{<g} - R^{<g+p}_{r+1} = sum_block dt_c pi_c (pH_{g+p}-pH_c)
 is checked from the definitions for random digit strings (it is where the history cancels).
usage: python3 t6_deep_algebra.py p SEED NU tmax
"""
import sys, random
import vf_lib as L

p = int(sys.argv[1]); seed = int(sys.argv[2]); NU = int(sys.argv[3]); tmax = int(sys.argv[4])
random.seed(seed)
E = 600
cnt = dict(a0=0, a0bad=0, s3=0, s3bad=0, s3ctrl=0, s4=0, s4bad=0, s4ctrl=0, hist=0, histbad=0, maxL=0, nblocks1D=0, nblocks2D=0)
for trial in range(NU):
    u = random.randrange(p ** E)
    if trial % 2 == 1:   # planted deep gate somewhere in [1, tmax/2]
        g0 = random.randint(1, tmax // 2)
        s0 = random.randint(5, 25)
        w = random.randrange(1, p ** 30)
        while w % p == 0:
            w = random.randrange(1, p ** 30)
        u = (-g0 + p ** s0 * w) % p ** E
    gl = L.gates(u, p, E, tmax)
    Mmax = max(s for _, s in gl)
    Vt = sum(s for _, s in gl)
    S = Mmax + 2
    PREC = S + Vt + 10
    MOD = p ** PREC
    # pi_c(u) mod MOD; scaled pH_c := p^S * sum_{i<=c} p/(u+i) mod MOD
    pi = [1]
    for c in range(1, tmax + 1):
        pi.append(pi[-1] * (u + c) % MOD)
    vi = {i: s for i, s in gl}

    def p_over(i):  # p^S * p/(u+i) mod MOD
        v = vi.get(i, 0)
        unit = (u + i) // p ** v
        return p ** (S + 1 - v) * pow(unit % MOD, -1, MOD) % MOD

    pH = [0]
    for c in range(1, tmax + 1):
        pH.append((pH[-1] + p_over(c)) % MOD)

    def vsc(x):  # valuation of the scaled residue minus S
        x %= MOD
        return (PREC if x == 0 else L.vp(x, p)) - S

    G = [g for g, _ in gl]; Sd = [s for _, s in gl]
    Lv = [0]
    for s in Sd:
        Lv.append(Lv[-1] + s)
    cnt["maxL"] = max(cnt["maxL"], Lv[-1])
    t = tmax
    # (0a)
    for rep in range(3):
        dt = [1] + [random.choice((-1, 0, 0, 1)) for _ in range(t - 1)]
        for r in range(1, len(G) + 1):
            g = G[r - 1]
            if g >= t:
                break
            diff = sum(dt[c] * pi[c] * (pH[c] - pH[g]) for c in range(g, t)) % MOD   # scaled
            cnt["a0"] += 1
            if vsc(diff) < Lv[r] + 1:
                cnt["a0bad"] += 1
                print("STEP0a FAIL", p, u % p ** 20, r, g, vsc(diff), Lv[r])
    # blocks r>=1 : [g_r, g_{r+1})
    for r in range(1, len(G)):
        g = G[r - 1]; Lr = Lv[r]; s_next = Sd[r]
        if G[r] != g + p:
            print("GATE SPACING ERROR"); continue
        y = u + g
        # Step 3
        cnt["nblocks1D"] += 1
        ok3 = True; ctrl3 = False
        for k in range(p):
            a = L.pi_at(y, k); b = L.pi_at(-p, k)
            if (a - b) % p ** s_next != 0:
                ok3 = False
            if (a - b) % p ** (s_next + 1) != 0:
                ctrl3 = True
        cnt["s3"] += 1
        cnt["s3bad"] += (not ok3)
        cnt["s3ctrl"] += ctrl3
        if s_next != 1:
            continue
        cnt["nblocks2D"] += 1
        # Step 4: per-digit congruence
        omega = pi[g] // 1
        assert omega % p ** Lr == 0 and (omega // p ** Lr) % p != 0
        om = (omega // p ** Lr) % MOD
        alpha = ((u + g + p) // p) % MOD
        ok4 = True; ctrl4 = False
        for k in range(p):
            lhs = pi[g + k] * ((pH[g + p] - pH[g + k]) % MOD) % MOD          # scaled by p^S
            rhs = p ** (S + Lr) * om * pow(alpha, -1, MOD) * L.pi_at(-p, k) % MOD
            if vsc(lhs - rhs) < Lr + 2:
                ok4 = False
            if vsc(lhs - rhs) < Lr + 3:
                ctrl4 = True
        cnt["s4"] += 1
        cnt["s4bad"] += (not ok4)
        cnt["s4ctrl"] += ctrl4
        if not ok4:
            print("STEP4 FAIL", p, u % p ** 20, r, g, Lr)
        # history cancellation from the definitions, random digits
        dt = [1] + [random.choice((-1, 0, 0, 1)) for _ in range(g + p - 1)]
        Rg = sum(dt[c] * pi[c] * (pH[c] - pH[g]) for c in range(g)) % MOD
        Tg = sum(dt[c] * pi[c] for c in range(g)) % MOD
        Rgp = sum(dt[c] * pi[c] * (pH[c] - pH[g + p]) for c in range(g + p)) % MOD
        lhs = (Rg - (pH[g + p] - pH[g]) * Tg - Rgp) % MOD
        rhs = sum(dt[c] * pi[c] * (pH[g + p] - pH[c]) for c in range(g, g + p)) % MOD
        cnt["hist"] += 1
        if lhs != rhs:
            cnt["histbad"] += 1
print(f"p={p} tmax={tmax}: {cnt}")
print("Step 0(a) failures: %d of %d; Step 3 failures: %d of %d (control mod p^(s+1) fails in %d); "
      "Step 4 failures: %d of %d 2D blocks (control mod p^(L+3) fails in %d); history identity failures: %d of %d"
      % (cnt["a0bad"], cnt["a0"], cnt["s3bad"], cnt["s3"], cnt["s3ctrl"], cnt["s4bad"], cnt["s4"], cnt["s4ctrl"], cnt["histbad"], cnt["hist"]))
