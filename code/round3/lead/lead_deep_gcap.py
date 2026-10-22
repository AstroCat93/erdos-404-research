# Lead re-check of deep exact values g_2(a) at p=2 with track T2's independent Python carry recursion
# (gcap.py), which shares no code with track T4's p2add.c.  Usage: python3 -I lead_deep_gcap.py <dir containing gcap.py> [a,cap ...]
import sys, time
sys.path.insert(0, sys.argv[1])
from gcap import gcap
pairs = [tuple(map(int, s.split(','))) for s in sys.argv[2:]] or [(3456, 4900), (2210, 6300), (1102, 11600), (34, 18500)]
for a, cap in pairs:
    t = time.time()
    g = gcap(a, cap)
    v2fact = sum(a >> i for i in range(1, 64))
    print(f"a={a} cap={cap} min(g_2(a),cap)={g} {'(exact: died below cap)' if g < cap else '(survived cap)'} f(a,2)=v2(a!)+g={g + v2fact} time={time.time()-t:.1f}s", flush=True)
