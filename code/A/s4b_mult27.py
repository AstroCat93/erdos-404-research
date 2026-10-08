# horizons for p=3 at N = 27k (k<=40) with modulus up to 3^K <= 2^maxbits
import sys
sys.path.insert(0, '.')
from s4_horizon import horizon, vfact
maxbits = int(sys.argv[1])
for k in range(1, 41):
    N = 27 * k
    h, lim = horizon(N, 3, maxbits)
    print(f"N={N} (=27*{k}, N/27 mod 3={k%3}):", f"fails at M={h} v={vfact(h,3)-vfact(N,3)}" if h else f"covers all M<{lim}")
    sys.stdout.flush()
