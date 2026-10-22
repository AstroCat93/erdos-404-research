# gamma_2(m) = max_B v_2(S_B(-m)), B subset [1,m-1]; exact via set of reachable sums mod 2^cap
import sys
def v2(z):
    if z==0: return 10**9
    return (z & -z).bit_length()-1
for m in range(3,27):
    pis=[]; p=1
    for b in range(1,m):
        p*= (b-m); pis.append(p)
    sums={1}
    for q in pis:
        sums = sums | {s+q for s in sums}
    print(m, max(v2(s) for s in sums), len(sums))
