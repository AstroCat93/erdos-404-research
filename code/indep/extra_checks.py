#!/usr/bin/env python3
"""Extra spot checks for values quoted in the note (uses the oracle of indep_checks.py)."""
import importlib.util, sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'indep_checks.py')).read().split('ok_all = True')[0]   # oracle definitions only
ns = {}; exec(src, ns)
g_ge, g_val, vfact = ns['g_ge'], ns['g_val'], ns['vfact']
def chk(name, ok): print(('[OK ] ' if ok else '[BAD] ') + name, flush=True)
# f(949,3) = 488
g = 488 - vfact(949, 3); chk(f"f(949,3)=488 (g={g})", g_ge(949, 3, g) and not g_ge(949, 3, g + 1))
# gamma_5(17)=7: f(a,5) = v_5(a!)+7 for a = 5^8 - 17 and a = 2*5^8 - 17
for a in (5**8 - 17, 2 * 5**8 - 17):
    chk(f"g_5({a}) = 7", g_val(a, 5, 9) == 7)
# gamma_2(14)=15: a = 2^16 - 14
chk("g_2(2^16-14) = 15", g_val(2**16 - 14, 2, 17) == 15)
# Proposition 3.4(c): gamma_p(p^k+2) >= 3k and finite
for p, k in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (5, 1), (7, 1)]:
    m = p**k + 2
    gm = g_val(-m, p, 80)
    chk(f"3k <= gamma_{p}({m}) < 80 : gamma={gm}, 3k={3*k}", 3 * k <= gm < 80)
# g_7 never 2: classes mod 7^3 with g>=2 equal classes with g>=3 (as sets mod 343)
S2 = {r for r in range(343) if g_ge(r, 7, 2)}; S3 = {r for r in range(343) if g_ge(r, 7, 3)}
chk(f"g_7 != 2 everywhere: |S2|={len(S2)} |S3|={len(S3)} equal={S2==S3}", S2 == S3)
# g_2(0) = 254
chk("g_2(0) = 254", g_ge(0, 2, 254) and not g_ge(0, 2, 255))
