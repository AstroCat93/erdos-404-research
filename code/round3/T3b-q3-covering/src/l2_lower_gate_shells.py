#!/usr/bin/env python3
"""(1) c_1(p,rho) = sum_{xi'=1}^{p-1} prod_{u<=rho} cos^2(pi xi' y_u / p), y_u = unit elements of a window with (H-1) mod p = rho
    (Lemma 10.11(d): y_i = (-1)^rho rho! (-1)^u/u!, u = rho - i, mod p).  Theorem S5(c): L^2(window) >= c_1 p^M.
(2) Gate shell sums G_p(d) = sum_{eta' in (Z/p^d)^x} E_p-hat(eta'/p^d), E_p-hat(theta) = prod_{u<p} |cos(pi theta (p-1)! (-1)^u/u!)|,
    and the max over the shell; these weight the carry Fourier coefficients in Theorem S4."""
import math
from fractions import Fraction
def inv(a,m): return pow(a,-1,m)
for p in [7,11,13,17,19]:
    row=[]
    for rho in range(p):
        ys=[((-1)**rho*math.factorial(rho)*(-1)**u*inv(math.factorial(u)%p,p))%p for u in range(rho+1)]
        c1=sum(math.prod(math.cos(math.pi*xi*y/p)**2 for y in ys) for xi in range(1,p))
        row.append(c1)
    print(f"p={p}: c_1(p,rho) for rho=0..{p-1}: "+' '.join(f"{x:.3g}" for x in row))
print()
for p in [7,11,13]:
    E=[(math.factorial(p-1)*(-1)**u)//math.factorial(u) for u in range(p)]   # integers (p-1)!(-1)^u/u!
    for d in range(1,7):
        md=p**d
        if md>3*10**6: break
        tot=0.0; mx=0.0
        for eta in range(1,md):
            if eta%p==0: continue
            v=math.prod(abs(math.cos(math.pi*eta*e/md)) for e in E)
            tot+=v; mx=max(mx,v)
        print(f"p={p} d={d}: gate shell sum G_p(d)={tot:.4g}  max over shell={mx:.4g}  (#terms={md-md//p}, random-model {(md-md//p)*(2/math.pi)**p:.4g})")
