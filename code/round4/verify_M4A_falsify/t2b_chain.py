"""t2b: exact tests, on composite windows [n,N,N') and balls B = x0 + p^b Z_p with a constant gate
pattern, of M4A Theorem 1 (identity), Lemma F, Prop D (pointwise, and for chi^2), Prop E (averaged)
and Prop E' >= Prop E.  Props D/E are evaluated by two independent code paths
(per-c Lemma Q, and the block/Suf form) which must agree exactly.

 eps(x) = p^K Coll_K(x) - p^D Coll_D(x);   Coll_j = P(sum_{c<H} d_c y_c(x) = 0 mod p^j), d signed.
 Thm 1:  E_B eps = E_B[ p^K P(S=0 (p^K), S'=0 (p^theta)) - p^D P(S=0 (p^D), S'=0 (p^theta)) ]
         theta = min(ceil(D/2), D-b+1)   (the 2^-H(p^K-p^D) term is the delta=0 part of the right side)
 Lemma F (needs M_W <= K-theta):
   p^K P(delta!=0, v(S)>=K, v(S')>=theta) <= sum_{a_c>=K} 2^{-c-1}p^K
                                            + sum_{a_c<K} 2^{-c-1} p^{a_c} sup_x G(x+n+c; H-c, K-a_c, theta-a_c)
   (the sup is taken over a subset of B: this makes the test stronger)

usage: python3 t2b_chain.py p SEED NB KIND Kmax maxpts statemax
  KIND: rand | deep (gate of depth s>=2 at distance g in {1,2,3,4,p+2} from the window start) | int
"""
import sys, random
from fractions import Fraction
import vf_lib as L

p = int(sys.argv[1]); seed = int(sys.argv[2]); NB = int(sys.argv[3]); KIND = sys.argv[4]
Kmax = int(sys.argv[5]); maxpts = int(sys.argv[6]); statemax = int(sys.argv[7])
random.seed(seed)
E = 40
C = L.eprime_consts(p)
cnt = dict(balls=0, thm1_ok=0, thm1_bad=0, F_ok=0, F_bad=0, F_skip=0, D_ok=0, D_bad=0, chi_ok=0, chi_bad=0,
           E_ok=0, E_bad=0, path_agree=0, path_disagree=0, Ep_ok=0, Ep_bad=0, theta_pos=0)
maxr = dict(D=0.0, E=0.0, F=0.0, chi=0.0)
tries = 0
while cnt["balls"] < NB and tries < 200 * NB:
    tries += 1
    n = random.randint(2 * p, 6 * p)
    H1 = random.randint(p, 3 * p)
    H2 = random.randint(p, 3 * p)
    N = n + H1; Np = N + H2; H = Np - n
    if KIND == "rand":
        x0 = random.randrange(p ** E)
    elif KIND == "int":
        x0 = random.randint(0, p ** 3)
    else:
        g = random.choice((1, 2, 3, 4, p + 2))
        s = random.randint(2, 4)
        w = random.randrange(1, p ** 8)
        while w % p == 0:
            w = random.randrange(1, p ** 8)
        x0 = (-n - g + p ** s * w) % p ** E
    gl = [(i, L.vmod(x0 + i, p, E)) for i in range(n + 1, Np + 1) if (x0 + i) % p == 0]
    if not gl:
        continue
    MW = max(s for _, s in gl)
    K = sum(s for _, s in gl)
    D = sum(s for i, s in gl if i <= N)
    if K > Kmax or D < 2:
        continue
    b = MW + 1 + random.choice((0, 0, 1))
    if K - b < 0 or p ** (K - b) > maxpts:
        continue
    theta = min(-(-D // 2), D - b + 1)
    th = max(theta, 0)
    if p ** (K + th) > statemax:
        continue
    cnt["balls"] += 1
    if theta >= 1:
        cnt["theta_pos"] += 1
    pts = [(x0 + p ** b * j) % p ** K for j in range(p ** (K - b))]
    # exact per-point quantities
    sum_eps = Fraction(0); sum_rhs = Fraction(0); sum_hs = Fraction(0)
    maxColl = Fraction(0); maxCollD = Fraction(0); max_eps = None
    for x in pts:
        Y, Yd = L.window_elems(x, n, H, p ** K)
        dp = L.SignedDP(p, K, th, first_fixed=False)
        for c in range(H):
            dp.step(Y[c], Yd[c])
        tot = 4 ** H
        cK, _ = dp.count_zero_fast(K, 0)
        cD, _ = dp.count_zero_fast(D, 0)
        jK, _ = dp.count_zero_fast(K, th)
        jD, _ = dp.count_zero_fast(D, th)
        eps = Fraction(p ** K * cK - p ** D * cD, tot)
        sum_eps += eps
        sum_rhs += Fraction(p ** K * jK - p ** D * jD, tot)
        sum_hs += Fraction(p ** K * (jK - 2 ** H), tot)   # delta != 0 high-slope mass at scale K (delta=0 has weight 2^H of 4^H)
        maxColl = max(maxColl, Fraction(p ** K * cK, tot))
        maxCollD = max(maxCollD, Fraction(p ** D * cD, tot))
        max_eps = eps if max_eps is None else max(max_eps, eps)
    npts = len(pts)
    EB = sum_eps / npts
    # Theorem 1
    if sum_eps == sum_rhs:
        cnt["thm1_ok"] += 1
    else:
        cnt["thm1_bad"] += 1
        print("THM1 FAIL", p, x0, n, N, Np, b, D, K, theta, float(sum_eps / npts), float(sum_rhs / npts))
    # Prop D (pointwise), two code paths
    PD1 = L.propDE_via_Q(p, x0, E, n, Np, K)
    PD2 = L.block_bound(p, gl, n, Np, K, None)
    if Fraction(int(PD2.numerator), int(PD2.denominator)) == PD1:
        cnt["path_agree"] += 1
    else:
        cnt["path_disagree"] += 1
        print("PATH DISAGREE (D)", p, x0, n, Np, float(PD1), float(PD2))
    if maxColl <= PD1 and max_eps <= PD1 - 1:
        cnt["D_ok"] += 1
    else:
        cnt["D_bad"] += 1
        print("PROP D FAIL", p, x0, n, N, Np, K, float(maxColl), float(PD1))
    maxr["D"] = max(maxr["D"], float(maxColl / PD1))
    # chi^2 version on W=[n,N): p^D Coll_D <= Prop D with N'=N, K->D
    PDchi = L.propDE_via_Q(p, x0, E, n, N, D)
    if maxCollD <= PDchi:
        cnt["chi_ok"] += 1
    else:
        cnt["chi_bad"] += 1
        print("PROP D (chi) FAIL", p, x0, n, N, D, float(maxCollD), float(PDchi))
    maxr["chi"] = max(maxr["chi"], float(maxCollD / PDchi))
    # Prop E, Lemma F (need M_W <= K - theta)
    if MW <= K - theta and theta >= 1:
        PE1 = L.propDE_via_Q(p, x0, E, n, Np, K, theta=theta, MW=MW, mode="MW")
        PE2 = L.block_bound(p, gl, n, Np, K, min(theta, K - MW))
        if Fraction(int(PE2.numerator), int(PE2.denominator)) == PE1:
            cnt["path_agree"] += 1
        else:
            cnt["path_disagree"] += 1
            print("PATH DISAGREE (E)", p, x0, n, Np, float(PE1), float(PE2))
        if EB <= PE1:
            cnt["E_ok"] += 1
        else:
            cnt["E_bad"] += 1
            print("PROP E FAIL", p, x0, n, N, Np, b, K, D, theta, float(EB), float(PE1))
        maxr["E"] = max(maxr["E"], float(EB / PE1) if PE1 else 0)
        # Lemma F with the sup over a subset of B (stronger test)
        LHS = sum_hs / npts
        sub = random.sample(pts, min(len(pts), 4))
        RHS = Fraction(0)
        a = 0
        for c in range(H):
            if c >= 1 and (x0 + n + c) % p == 0:
                a += L.vmod(x0 + n + c, p, E)
            if a >= K:
                RHS += Fraction(p ** K, 2 ** (c + 1))
                continue
            k = K - a; f = theta - a
            best = Fraction(0)
            for x in sub:
                u = x + n + c
                Pv, Dv = L.pi_and_deriv(u, H - c, p ** K)
                dpu = L.SignedDP(p, k, max(f, 0), first_fixed=True)
                for cc in range(H - c):
                    dpu.step(Pv[cc], Dv[cc])
                z, tot = dpu.count_zero_fast(k, max(f, 0))
                Gv = Fraction(p ** k * z, tot)
                best = max(best, Gv)
            RHS += Fraction(p ** a, 2 ** (c + 1)) * best
        if LHS <= RHS:
            cnt["F_ok"] += 1
        else:
            cnt["F_bad"] += 1
            print("LEMMA F FAIL", p, x0, n, N, Np, b, K, D, theta, float(LHS), float(RHS))
        maxr["F"] = max(maxr["F"], float(LHS / RHS) if RHS else 0)
        # Prop E' >= Prop E (kappa>0 at p=3,5,7)
        lEp = L.eprime_log(p, K, H, MW, min(theta, K - MW), C)
        import mpmath as mp
        if mp.log(mp.mpf(int(PE2.numerator))) - mp.log(mp.mpf(int(PE2.denominator))) <= lEp:
            cnt["Ep_ok"] += 1
        else:
            cnt["Ep_bad"] += 1
            print("E' < E", p, x0, n, Np, K, float(lEp))
    else:
        cnt["F_skip"] += 1
print(f"p={p} KIND={KIND}: {cnt}")
print(f"max ratios: Coll_K/PropD={maxr['D']:.4f}  chi-version={maxr['chi']:.4f}  E_B eps/PropE={maxr['E']:.4f}  LemmaF LHS/RHS={maxr['F']:.4f}")
