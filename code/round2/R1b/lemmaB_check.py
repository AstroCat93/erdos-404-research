"""Check of the deterministic part of Lemma B: if e is alive at n and lambda_e = v(S_e'(x)) >= D
(D = V_N - V_n), then the set of children of e alive at N is the same for every x' = x mod 2^m
(m = V_n), i.e. independent of the digits w at positions m..m+D-1 (and beyond).
Also checks the distinct-level bound  #children <= 2^{N-n-r},  r = floor((N-1-n)/2)."""
import random, sys
import mart_check2 as mc
rnd = random.Random(int(sys.argv[1])); n, N, P, T = (int(a) for a in sys.argv[2:6])
checked = bad = badr = 0; done = 0; tries = 0
while done < T and tries < 200000:
    tries += 1
    x = rnd.getrandbits(P) & ~1
    m = mc.V(x, n); D = mc.V(x, N) - m
    if D < 1 or mc.mu(x, N) >= m: continue
    parents = mc.alive_paths(x, n, P)
    big = [e for e in parents if mc.tau_of(e, x, n, P)[1] >= D]
    if not big: continue
    done += 1
    x0 = x % (1 << m)
    ref = None
    for trial in range(12):
        xw = x0 + (rnd.getrandbits(P - m) << m)
        kids = mc.alive_paths(xw, N, P)
        sets = {e: frozenset(c >> n for c in kids if (c & ((1 << n) - 1)) == e) for e in big}
        if ref is None: ref = sets
        elif sets != ref: bad += 1
        checked += 1
    r = (N - 1 - n) // 2
    for e in big:
        if len(ref[e]) > 2 ** (N - n - r): badr += 1
print(f"instances {done}, w-samples {checked}, children-set changes {bad}, level-bound violations {badr}")
