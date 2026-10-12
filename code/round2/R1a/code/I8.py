# Exact computation of I_8(C_0) = int_{x in 8Z_2} N_8(x) 2^{P_8(x)-8} dx, split by j = v(x+8)-3.
# For fixed j, x = -8 + 2^{3+j} eta (eta odd); N_8(x) depends on eta mod 2^R for R large enough
# (we verify stability of the average by increasing R and by random higher digits).
import random, sys
from hier_lib import valid_paths
rnd = random.Random(7)
BIG = 1 << 200
def N8(x): return len(valid_paths(x, 8, cap=10**6))
for R in (6, 9):
    total = 0.0; per_j = []
    for j in range(0, 14):
        s = 0; cnt = 0
        for eta in range(1, 1 << R, 2):
            x = (-8 + ((eta + (rnd.getrandbits(60) << R)) << (3 + j))) % BIG
            s += N8(x); cnt += 1
        avg = s / cnt; per_j.append(avg)
        total += 2.0 ** (-5) * avg
    print("R", R, "avg N_8 by j:", per_j, " I_8 =", total)
