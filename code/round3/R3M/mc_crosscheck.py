#!/usr/bin/env python3
"""mc_crosscheck.py -- independent recount of Z_n(x) (alive paths) and Z0_n(x) (slope-0 alive paths)
for the SAMPLE lines printed by bin/oddp_mc (which uses the carry recursion); here aliveness is decided by
evaluating S_e(x) and S_e'(x) as integers (no shared code).  usage: oddp_mc ... NVERB | mc_crosscheck.py p
"""
import sys
p = int(sys.argv[1])
ok = tot = 0
for line in sys.stdin:
    if not line.startswith('SAMPLE'):
        continue
    _, xs, ns, Zs, Z0s = line.split()
    x, n = int(xs), int(ns)
    MOD = p ** 80
    def vp(a):
        a %= MOD
        if a == 0:
            return 80
        k = 0
        while a % p == 0:
            a //= p; k += 1
        return k
    P = [1]; dP = [0]
    for j in range(1, n + 1):
        dP.append(dP[-1] * (x + j) + P[-1]); P.append(P[-1] * (x + j))
    V = [0]
    for j in range(1, n + 1):
        V.append(V[-1] + vp(x + j))
    Z = Z0 = 0
    st = [(1, 1, 0)]
    while st:
        j, S, Sd = st.pop()
        if vp(S) < V[j]:
            continue
        if j == n:
            Z += 1; Z0 += (Sd % p != 0); continue
        st.append((j + 1, S, Sd)); st.append((j + 1, S + P[j], Sd + dP[j]))
    tot += 1
    good = (Z == int(Zs) and Z0 == int(Z0s))
    ok += good
    print(f"x={x} n={n}: C program Z={Zs} Z0={Z0s}; recount Z={Z} Z0={Z0} {'OK' if good else 'MISMATCH'}")
print(f"RESULT crosscheck p={p}: {ok}/{tot} samples agree")
