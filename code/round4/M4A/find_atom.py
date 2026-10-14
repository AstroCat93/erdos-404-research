#!/usr/bin/env python3
"""find_atom.py -- search for an admissible atom A = xA + p^m Z_p at time nj (track M4A, round 4).

A is admissible (data/round3/reports/R3M.md, Theorem C3) if the slope-0 population P^0_{nj} is nonempty on A
(a path e of length nj, e_0 = 1, with v(S_e(xA)) >= V_nj(xA) =: m and v(S_e'(xA)) = 0; both properties are
constant on A by R3M Lemma 2(a)) and the window conditions D_j <= m - M_{n_{j+1}}, M_{n_{j+1}} < m hold.
The path is found by a randomized depth-first search with prefix pruning (a prefix of an alive path is alive,
R3M (F2)); it is then re-verified by direct evaluation of S_e(xA), S_e'(xA) with exact integers.
Also reports i_1 = min{i >= 1: xA + i == 0 mod p^m} (no random gate before i_1) and the scale data
i_s = (-xA mod p^s), s <= m (v(xA+i) >= s iff i == i_s mod p^s).
usage: find_atom.py p SEED nj n_{j+1} [NODELIMIT [OUTFILE]]   prints the atom and the path as a bit string;
with OUTFILE, writes p, n0, m, xA and path = e_0 e_1 ... e_{nj-1} (one character per bit) for fe_verify.py.
"""
import random
import sys

from m4a_lib import vp


def main():
    p, seed, nj, nj1 = (int(a) for a in sys.argv[1:5])
    limit = int(sys.argv[5]) if len(sys.argv) > 5 else 2 * 10 ** 6
    outfile = sys.argv[6] if len(sys.argv) > 6 else None
    rnd = random.Random(seed)
    for attempt in range(1000):
        x = rnd.randrange(p ** 200)
        depth = [0] + [vp(x + i, p, 10 ** 6) for i in range(1, nj1 + 1)]
        V = [0] * (nj1 + 1)
        for i in range(1, nj1 + 1):
            V[i] = V[i - 1] + depth[i]
        m = V[nj]
        Mj1 = max(depth[1:nj1 + 1])
        Dj = V[nj1] - V[nj]
        if not (Dj <= m - Mj1 and Mj1 < m):
            continue
        xA = x % p ** m
        mod = p ** (m + 3)
        pi = [1] * (nj + 1)
        dpi = [0] * (nj + 1)
        for c in range(1, nj + 1):
            pi[c] = pi[c - 1] * (xA + c) % mod
            dpi[c] = (dpi[c - 1] * (xA + c) + pi[c - 1]) % mod
        # DFS: state (c, S, dS, bits); alive at c means v(S) >= V[c]
        stack = [(1, 1 % mod, 0, 1)]
        nodes = 0
        found = None
        while stack and nodes < limit:
            c, S, dS, bits = stack.pop()
            nodes += 1
            if c == nj:
                if dS % p != 0:
                    found = bits
                    break
                continue
            ch = [0, 1]
            rnd.shuffle(ch)
            for b in ch:
                S2 = (S + b * pi[c]) % mod
                dS2 = (dS + b * dpi[c]) % mod
                if vp(S2, p, 10 ** 6) >= V[c + 1] if S2 else True:
                    # slope-0 pruning: once v(pi'_c) >= 1 for all later c, S' mod p is frozen
                    if c + 1 > 2 * p and V[c + 1] - max(depth[1:c + 2]) >= 1 and dS2 % p == 0:
                        continue
                    stack.append((c + 1, S2, dS2, bits | (b << c)))
        print(f"attempt {attempt}: m={m} D_j={Dj} M_(n_j+1)={Mj1} nodes={nodes} found={found is not None}", flush=True)
        if found is None:
            continue
        # independent re-verification by direct evaluation (exact integers, no reduction)
        S = 0
        dS = 0
        P, dP = 1, 0
        for c in range(nj):
            if (found >> c) & 1:
                S += P
                dS += dP
            dP = dP * (xA + c + 1) + P
            P = P * (xA + c + 1)
        vS = vp(S, p, 10 ** 6)
        ok = vS >= m and dS % p != 0 and (found & 1) == 1
        i1 = (-xA) % p ** m or p ** m
        iss = [(-xA) % p ** s or p ** s for s in range(1, m + 1)]
        print(f"RESULT p={p} nj={nj} m={m} xA={xA}")
        print(f"RESULT path_bits={found:b}"[::1])
        print(f"RESULT direct check: v(S_e(xA))={vS} >= m={m}: {vS >= m}; S_e'(xA) mod p = {dS % p} (nonzero: {dS % p != 0}); e_0=1: {found & 1}; ADMISSIBLE={ok}")
        print(f"RESULT i_1 = {i1}  (log_p i_1 = {len(str(i1))} decimal digits)")
        print(f"RESULT scales: s, i_s for s<=12: {[(s + 1, iss[s]) for s in range(min(12, m))]}")
        print(f"RESULT min over s of log_p(i_s) - s: {min(__import__('math').log(iss[s], p) - (s + 1) for s in range(m)):.3f}")
        if outfile and ok:
            bitstr = ''.join('1' if (found >> c) & 1 else '0' for c in range(nj))
            with open(outfile, 'w') as fh:
                fh.write(f"p={p}\nn0={nj}\nm={m}\nxA={xA}\npath={bitstr}\n")
            print(f"RESULT wrote {outfile}")
        return


if __name__ == "__main__":
    main()
