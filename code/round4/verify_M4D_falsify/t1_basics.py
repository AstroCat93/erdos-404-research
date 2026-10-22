"""t1: standing facts used by Lemma L / Theorem F (M4D report sec. 1).

Tests (all exact integer arithmetic, x natural):
  F1a  V_n(x) >= v_p(n!)                                  [(F1)]
  DEL  v(S_B) >= V_n  =>  v(S_{B cap [1,n)}) >= V_n       [P(x,n) <=> g_p >= V_n]
  DFS  pruned DFS of alive paths == brute force over all 2^(n-1) paths
  DP   target-set DP (carry recursion) == targets of DFS paths
  F2   for every parent e (alive or NOT) and every f in {0,1}^H:
         (e,f) alive at N  =>  e alive at n                 [converse]
         e alive: (e,f) alive at N <=> Q_f = tau mod p^D   [(F2)]
         and tau_N(e,f) = u^{-1}(tau - Q_f)/p^D  mod p^k    [(F2) formula]
  LOC  all chain data (V's, T_l mod p^{D_l}, Sigma_l mod p^{D_l+D_{l+1}})
       agree at a and a + t p^k whenever k >= V_N(a), k > M_N(a)
Usage: python3 t1_basics.py p seed nsamples
"""
import random
import sys
import time

from fz_core import (Mval, Vlist, Window, alive_paths_bruteforce,
                     alive_paths_dfs, pis, sample_x, target, target_sets_dp,
                     vp, vp_fact)

KINDS = ["rand", "near-1", "near-2", "negint"]


def main():
    p = int(sys.argv[1])
    seed = int(sys.argv[2])
    ns = int(sys.argv[3])
    rng = random.Random(seed)
    t0 = time.time()
    fails = {k: 0 for k in ["F1a", "DEL", "DFS", "DP", "F2conv", "F2iff",
                            "F2tau", "LOC"]}
    cnt = {k: 0 for k in fails}

    # F1a
    for _ in range(ns * 20):
        x, _lab = sample_x(p, rng, rng.choice(KINDS), 40)
        n = rng.randint(1, 60)
        V = Vlist(x, n, p)
        cnt["F1a"] += 1
        if V[n] < vp_fact(n, p):
            fails["F1a"] += 1
            print("F1a FAIL", x, n)

    for it in range(ns):
        kind = KINDS[it % len(KINDS)]
        nsmall = rng.randint(3, 12)
        x, lab = sample_x(p, rng, kind, nsmall)
        # DEL: all B subset [1, nsmall+h)
        h = rng.randint(1, 4)
        P = pis(x, nsmall + h)
        Vn = vp(P[nsmall], p)
        q = p ** Vn
        for mask in range(1 << (nsmall + h - 1)):
            B = [b for b in range(1, nsmall + h) if (mask >> (b - 1)) & 1]
            S = 1 + sum(P[b] for b in B)
            if S % q == 0:
                cnt["DEL"] += 1
                S2 = 1 + sum(P[b] for b in B if b < nsmall)
                if S2 % q:
                    fails["DEL"] += 1
                    print("DEL FAIL", x, nsmall, B)
        # DFS vs brute force
        bf = alive_paths_bruteforce(x, nsmall, p)
        df = alive_paths_dfs(x, nsmall, p)
        cnt["DFS"] += 1
        if sorted(bf) != sorted(df):
            fails["DFS"] += 1
            print("DFS FAIL", lab, x, nsmall, len(bf), len(df))

        # DP vs DFS at several times
        n2 = rng.randint(4, 16 if p > 3 else 13)
        times = sorted(set(rng.sample(range(1, n2 + 1), min(4, n2))))
        V = Vlist(x, n2, p)
        Vtop = V[n2] + rng.randint(0, 3)
        dp = target_sets_dp(x, times, p, Vtop)
        P2 = pis(x, n2)
        for t in times:
            paths = alive_paths_dfs(x, t, p, P=P2, V=V)
            k = Vtop - V[t]
            ref = {target(S, P2[t], p, k) for _e, S in paths}
            cnt["DP"] += 1
            if ref != dp[t]:
                fails["DP"] += 1
                print("DP FAIL", lab, x, t, len(ref), len(dp[t]))

        # F2 on a window [n, N)
        n = rng.randint(1, 10)
        H = rng.randint(1, 9)
        N = n + H
        P3 = pis(x, N + 1)
        V3 = Vlist(x, N, p)
        W = Window(x, n, N, p)
        assert W.D == V3[N] - V3[n]
        Qex = W.sums_list_exact()
        qN = p ** V3[N]
        qn = p ** V3[n]
        k = rng.randint(0, 3)
        PS = [0]
        for i in range(H):
            PS = PS + [z + P3[n + i] for z in PS]
        # all parents (alive or not) -- brute force over 2^(n-1)
        for mask in range(1 << (n - 1)):
            e = (1,) + tuple((mask >> (j - 1)) & 1 for j in range(1, n))
            Se = sum(P3[j] for j in range(n) if e[j])
            e_alive = (Se % qn == 0)
            if e_alive:
                tau_hi = target(Se, P3[n], p, W.D + k)
            for fm in range(1 << H):
                Sc = Se + PS[fm]
                c_alive = (Sc % qN == 0)
                if c_alive:
                    cnt["F2conv"] += 1
                    if not e_alive:
                        fails["F2conv"] += 1
                        print("F2conv FAIL", lab, x, n, N, e, fm)
                if e_alive:
                    cnt["F2iff"] += 1
                    Qf = Qex[fm]
                    pred = ((tau_hi - Qf) % (p ** W.D) == 0)
                    if pred != c_alive:
                        fails["F2iff"] += 1
                        print("F2iff FAIL", lab, x, n, N, e, fm)
                    if c_alive:
                        cnt["F2tau"] += 1
                        mk = p ** k
                        z = (tau_hi - Qf)
                        assert z % (p ** W.D) == 0
                        pr = ((z // p ** W.D) * pow(W.unit, -1, mk)) % mk if mk > 1 else 0
                        tr = target(Sc, P3[N], p, k)
                        if pr != tr:
                            fails["F2tau"] += 1
                            print("F2tau FAIL", lab, x, n, N, e, fm, pr, tr)
        # LOC: chain data at a and a + t p^k
        times = sorted(rng.sample(range(1, 3 * N // 2 + 3), 4))
        NN = times[-1]
        VV = Vlist(x, NN, p)
        kk = max(VV[NN], Mval(x, NN, p) + 1)
        a = x % (p ** kk)
        if a == 0:
            a = p ** kk
        b = a + rng.randint(1, 50) * p ** kk
        ok = True
        for (xa, xb) in [(a, b), (a, x)]:
            Va, Vb = Vlist(xa, NN, p), Vlist(xb, NN, p)
            if Va != Vb:
                ok = False
                continue
            Ds = [Va[times[i + 1]] - Va[times[i]] for i in range(3)]
            for i in range(3):
                Ta = alive_paths_dfs(xa, times[i], p, cap=200000)
                Tb = alive_paths_dfs(xb, times[i], p, cap=200000)
                if Ta is None or Tb is None:
                    continue
                Pa, Pb = pis(xa, times[i]), pis(xb, times[i])
                sa = {target(S, Pa[-1], p, Ds[i]) for _e, S in Ta}
                sb = {target(S, Pb[-1], p, Ds[i]) for _e, S in Tb}
                if sa != sb:
                    ok = False
            for i in range(2):
                Wa = Window(xa, times[i], times[i + 1], p)
                Wb = Window(xb, times[i], times[i + 1], p)
                K = Ds[i] + Ds[i + 1]
                if (Wa.sums_mask(K) != Wb.sums_mask(K)).any():
                    ok = False
        cnt["LOC"] += 1
        if not ok:
            fails["LOC"] += 1
            print("LOC FAIL", lab, x, times)

    print("p=%d seed=%d samples=%d  time=%.1fs" % (p, seed, ns, time.time() - t0))
    for k in fails:
        print("  %-7s checks=%9d  failures=%d" % (k, cnt[k], fails[k]))
    print("TOTAL FAILURES", sum(fails.values()))


if __name__ == "__main__":
    main()
