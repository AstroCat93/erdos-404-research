# EXACT weight-conservation check by adaptive refinement (handles case (ii) steps exactly).
# Starting from a 1-stable (path p, point y) at time N0 with stability ball U = y + 2^sigma Z_2, compute
#   W_n = sum over balls V subset U on which env through n is constant and V fine enough that validity of every
#   continuation of p through n is constant on V:   sum_{q valid on V} mu(V) 2^{P_n - n}
# and compare with W_{N0} = mu(U) 2^{P_{N0} - N0}.  Refinement rule: split while some v(y0+l) >= rho (l<=n)
# or rho < P_n (validity of q through n depends only on y mod 2^{P_n} once the environment is constant).
import random, sys
BIG = 900; MOD = 1 << BIG
def v2(n):
    n %= MOD
    return BIG if n == 0 else (n & -n).bit_length() - 1
def valid(y, path):
    g = 0; prec = BIG
    for k, e in enumerate(path):
        n = k + 1; d = v2(y + n); t = (g + e) % (1 << prec)
        if d and (t & ((1 << d) - 1)): return False
        prec -= d; u = ((y + n) >> d) % (1 << prec)
        g = ((t >> d) * pow(u, -1, 1 << prec)) % (1 << prec)
    return True
def conts(y, p, n):
    out = []; st = [tuple(p)]
    while st:
        q = st.pop()
        if not valid(y, q): continue
        if len(q) == n: out.append(q); continue
        st.append(q + (0,)); st.append(q + (1,))
    return out
def kappa(y, path):
    K2 = 1 << 300; B = 0; pi = 1; g = 0; prec = BIG
    for k, e in enumerate(path):
        n = k + 1; d = v2(y + n); t = (g + e) % (1 << prec); prec -= d
        u = ((y + n) >> d) % (1 << prec); g = ((t >> d) * pow(u, -1, 1 << prec)) % (1 << prec)
        B = (B + g * pi) % K2; pi = (pi * (y + n)) % K2
    return v2(B) if B else 300
RHOMAX = [10**9]
def W(y0, rho, p, n, budget):
    env = [v2(y0 + l) for l in range(1, n + 1)]
    if max(env) >= rho and rho >= RHOMAX[0]:
        return 0.0   # ball around a negative integer -l at depth >= RHOMAX: contributes 0 once deeper than all shadow valuations
    if max(env) >= rho or rho < sum(env):
        if budget[0] <= 0: raise RuntimeError("budget")
        budget[0] -= 1
        return W(y0, rho + 1, p, n, budget) + W((y0 + (1 << rho)) % MOD, rho + 1, p, n, budget)
    P = sum(env)
    return len(conts(y0, p, n)) * 2.0 ** (P - n - rho)
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2]); force_ii = len(sys.argv) > 3
done = 0; worst = 0.0; nii = 0
while done < trials:
    N0 = rnd.randrange(8, 18); T = rnd.randrange(1, 5)
    y = rnd.getrandbits(BIG) & ~1
    if force_ii:  # put a negative integer -(N0+s) inside the ball: y close to -(N0+s)
        s = rnd.randrange(1, T + 1); y = (-(N0 + s) + (rnd.getrandbits(BIG - 40) << rnd.randrange(10, 18))) % MOD
        if y % 2: continue
    ps = conts(y, (1,), N0)
    if not ps: continue
    p = rnd.choice(ps)
    env0 = [v2(y + l) for l in range(1, N0 + 1)]; P0 = sum(env0); M = max(env0)
    kap = kappa(y, p); sig = P0 - kap
    if not (sig >= kap + M + 1): continue
    n = N0 + T
    caseii = any(v2(y + l) >= sig for l in range(N0 + 1, n + 1))
    RHOMAX[0] = sig + 40
    try:
        w = W(y % (1 << sig), sig, p, n, [400000])
    except RuntimeError:
        continue
    rel = w / 2.0 ** (P0 - N0 - sig)
    done += 1; nii += caseii; worst = max(worst, abs(rel - 1))
    print(f"N0={N0} T={T} kappa={kap} sigma={sig} M={M} case_ii_ahead={caseii} ratio={rel:.9f}")
print("trials", done, "with case (ii) ahead:", nii, "max |ratio-1| =", worst)
