from core import *
import math
def sums_mod(xs,M):
    s={0}
    for x in xs: s|={(y+x)%M for y in s}
    return s
def pis(x,n,M):
    out=[1%M];pr=1
    for j in range(1,n): pr=pr*(x+j)%M; out.append(pr)
    return out
# Thm 3.8
print("Thm3.8: residues r mod 16 with full A_r mod 16:",[r for r in range(16) if len(sums_mod(pis(r,16,16),16))==16])
# also check pi_j(r) == 0 mod 16 for j>=16 trivially (16 consecutive), and check with j up to 40 nothing changes
print("  with j<40:",[r for r in range(16) if len(sums_mod(pis(r,40,16),16))==16])
# Thm 3.11
S=sums_mod([math.factorial(t) for t in range(9)],81)
print("Thm3.11: Z/81 minus sums of t!, t<=8:",sorted(set(range(81))-S))
# actual A_N mod 81 for N = 81*c, several c, all terms j< 60
for N in (81,162,243,81*5,81*7,81*100):
    s=sums_mod(pis(N,60,81),81)
    print("  N=%d missing"%N,sorted(set(range(81))-s))
# which N mod 81 have A_N full mod 81 (j up to 60 suffices: v(pi_j)>=v(j!)>=4 for j>=9)
full=[N for N in range(81) if len(sums_mod(pis(N,12,81),81))==81]
print("N mod 81 with A_N full mod 81:",full)
# deeper: which N mod 3^k have A_N full mod 3^k
for k in (5,6):
    M=3**k
    full=[N for N in range(M) if len(sums_mod(pis(N,2*k+4,M),M))==M]
    # need terms until v(j!)>=k : j with v_3(j!)>=k
    print("k=%d: #N mod 3^k full:"%k,len(full),"residues mod 81:",sorted(set(N%81 for N in full)))
# gate congruence Thm 3.9(b): P_m(r) == (p-1)! (-1)^u/u! mod p^{j+1} for p^j | m+1
bad=0;cnt=0
for p in (3,5,7,11,13):
    for j in range(0,4):
        M=p**(j+1)
        for t in range(1,30):
            m=p**j*t-1
            if m<0: continue
            for r in range(p):
                u=p-1-r
                lhs=1
                for i in range(1,r+1): lhs=lhs*(p*m+i)%M
                rhs=math.factorial(p-1)*(-1)**u*pow(math.factorial(u),-1,M)%M
                cnt+=1
                if lhs!=rhs: bad+=1
print("gate congruence: %d cases, %d failures"%(cnt,bad))
