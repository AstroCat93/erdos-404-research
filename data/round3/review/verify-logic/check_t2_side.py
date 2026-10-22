# Spot check of the side terms (B_L(n0)+n0 2^-K) G^0.227 of Cor 11.30 and of the hypotheses of Thm 11.29.
import math
al = 0.227
def hL(n, L): return 0.5 * (n - math.log2(n) - 3 * L - 4)
def BL(n0, L, l0):
    s = 0.0; i = 1
    while True:
        t = 2.0 ** (-math.floor(hL(max(n0, i - l0), L)) - 1)
        s += t
        if i > n0 + l0 and t < 1e-30: break
        i += 1
    return s
for name, k, L, l0 in [("C0", 3, 1, 4), ("C2", 3, 3, 8), ("C6", 4, 6, 14)]:
    best = 0; arg = None
    cands = set()
    for j in range(10, 61):
        for d in range(-600, 600): cands.add(2 ** j + d)
    for q in range(4 * 10, 4 * 61):   # n0 changes when 4 log2 G crosses an integer
        g = 2 ** (q / 4)
        for d in range(-3, 4): cands.add(int(g) + d)
    for G in sorted(cands):
        if G < 2 ** 10: continue
        n0 = math.ceil(4 * math.log2(G)) + 3 * L + 40
        T = G // 2; K = int(math.floor(math.log2(T - l0 + 1)))
        assert T >= n0 + l0 and 2 ** K >= l0 and K > k and n0 >= 19
        val = (BL(n0, L, l0) + n0 * 2.0 ** (-K)) * G ** al
        if val > best: best, arg = val, G
    print(name, "max side term over sampled G in [2^10,2^60]: %.4f at G=%d" % (best, arg))
