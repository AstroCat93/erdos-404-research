#!/usr/bin/env python3
"""b3_ball_check.py -- exact test of Lemma B3 (conservation of the UNWEIGHTED signed mass on Hensel balls).

Signed strings delta in {-1,0,1}^t (weights 2,1,1 out of 4), S_delta(Z) = sum_{c<t} delta_c pi_c(Z),
alive at t at z iff v(S_delta(z)) >= V_t(z); slope lambda = v(S_delta'(z)).
Lemma B3: let delta be alive at t at z' with slope lambda, m = V_t(z'), M = M_t(z'), M' = M_t'(z'),
D = V_t'(z') - m, and assume
   (H) m >= 2 lambda + M + 1,  (W1) t'-t >= p lambda,  (W2) D + lambda <= m - M,  (W3) lambda < m - M'.
Then on the ball B = z' + p^(m-lambda) Z_p:
   E_{z in B} [ p^{V_t'(z)} sum_f P(f) 1((delta,f) alive at t' at z) ] = p^m        (exactly),
i.e. sum over the p^(lambda+D) classes k of z = z' + p^(m-lambda) k mod p^(m+D) of the weighted child
count equals p^lambda.  On a single FINE cylinder z'+p^m Z_p the same average is p^m * p^lambda a(s)
(the frozen weight rho of R3M Prop A), which is NOT 1 in general (control column 'fine').
Aliveness of every (delta,f) is decided by direct evaluation of S at z mod p^PREC.
usage: b3_ball_check.py p SEED NZ t t' [MAXPAR] [LMIN] [nohyp|nohypH]
(parents: signed strings with delta_0 != 0, found by a randomised pruned DFS; LMIN = least slope tested)
"""
import random
import sys
from fractions import Fraction

from m4b_lib import Ctx, valuations

W = {0: 2, 1: 1, -1: 1}


def pis(C, z, T):
    pi = [1] * (T + 1)
    dpi = [0] * (T + 1)
    for j in range(1, T + 1):
        pi[j] = pi[j - 1] * (z + j) % C.mod
        dpi[j] = (dpi[j - 1] * (z + j) + pi[j - 1]) % C.mod
    return pi, dpi


def alive_signed(C, pi, V, t, rnd, budget=200000):
    """(delta) with delta in {-1,0,1}^t, delta_0 != 0, alive at t: randomised DFS with prefix pruning
    (a prefix of an alive string is alive), at most `budget` nodes visited."""
    out = []
    stack = [((e,), e * pi[0] % C.mod, 1) for e in (1, -1) if C.v(e) >= V[1]]
    nodes = 0
    while stack and nodes < budget:
        d, S, k = stack.pop()
        nodes += 1
        if k == t:
            out.append(d)
            continue
        es = [0, 1, -1]
        rnd.shuffle(es)
        for e in es:
            S2 = (S + e * pi[k]) % C.mod
            if C.v(S2) >= V[k + 1]:
                stack.append((d + (e,), S2, k + 1))
    return out


def S_of(C, pi, d):
    return sum(e * pi[c] for c, e in enumerate(d)) % C.mod


def child_mass(C, z, d, t, t2):
    """sum over f in {-1,0,1}^(t2-t) of 4^(t2-t) P(f) 1((d,f) alive at t2 at z) (integer)."""
    vals, V = valuations(C, z, t2)
    pi, _ = pis(C, z, t2)
    S0 = S_of(C, pi, d)
    tot = 0
    stack = [(S0, t, 1)]
    while stack:
        S, k, w = stack.pop()
        if k == t2:
            tot += w
            continue
        for e in (0, 1, -1):
            S2 = (S + e * pi[k]) % C.mod
            if C.v(S2) >= V[k + 1]:
                stack.append((S2, k + 1, w * W[e]))
    return tot


def main():
    p, seed, NZ, t, t2 = (int(a) for a in sys.argv[1:6])
    MAXPAR = int(sys.argv[6]) if len(sys.argv) > 6 else 40
    LMIN = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    nohyp = len(sys.argv) > 8 and sys.argv[8] in ('nohyp', 'nohypH')
    nohypH = len(sys.argv) > 8 and sys.argv[8] == 'nohypH'
    C = Ctx(p, 120)
    rnd = random.Random(seed)
    npar = nok = nfine_ne1 = nz = 0
    for it in range(NZ):
        z0 = rnd.randrange(C.mod)
        vals, V = valuations(C, z0, t2)
        m, M, M2 = V[t], max(vals[1:t + 1]), max(vals[1:t2 + 1])
        D = V[t2] - m
        pi, dpi = pis(C, z0, t2)
        par = alive_signed(C, pi, V, t, rnd)
        rnd.shuffle(par)
        nz += 1
        cnt = 0
        for d in par:
            if not any(d):
                continue  # the zero string has slope infinity
            dS = sum(e * dpi[c] for c, e in enumerate(d)) % C.mod
            lam = C.v(dS)
            hyp = (m >= 2 * lam + M + 1 and t2 - t >= p * lam and D + lam <= m - M and lam < m - M2)
            if nohypH and not hyp:
                hyp = (m >= 2 * lam + M + 1)  # 'nohypH': only parents violating (H) itself count as violating
            if hyp == nohyp or lam < LMIN:
                continue
            if lam + D > 7:
                continue
            cnt += 1
            if cnt > MAXPAR:
                break
            tot = 0
            fine = []
            for k in range(p ** (lam + D)):
                z = (z0 + p ** (m - lam) * k) % C.mod
                cm = child_mass(C, z, d, t, t2)
                tot += cm
                fine.append(cm)
            target = p ** lam * 4 ** (t2 - t)
            ok = (tot == target)
            # fine-cylinder control: average over the p^D classes inside z0 + p^m Z_p (k = p^lam * j)
            fine_avg = Fraction(sum(fine[p ** lam * j] for j in range(p ** D)), p ** D * 4 ** (t2 - t))
            rho_fine = fine_avg * p ** D   # = rho(delta) of R3M Prop A on the fine cylinder of z0
            nfine_ne1 += (rho_fine != 1)
            npar += 1
            nok += ok
            if not ok or npar <= 6:
                tag = "MISMATCH" if (not ok and not nohyp) else " "
                print(f"{tag} z#{it} lam={lam} m={m} M={M} M'={M2} D={D}: ball sum/target = "
                      f"{Fraction(tot, target)}  fine-cylinder rho = {rho_fine}", flush=True)
    kind = "violating (H)/(W)" if nohyp else "satisfying (H),(W1)-(W3)"
    print(f"RESULT p={p} t={t} t'={t2} {kind}: {nz} base points, {npar} parents with finite slope; "
          f"ball identity exact in {nok}/{npar}; fine-cylinder rho != 1 in {nfine_ne1}/{npar}")


if __name__ == "__main__":
    main()
