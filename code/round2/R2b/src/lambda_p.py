# Lambda_p = sum_{d>=1} (p^d - p^{d-1}) (2/pi)^{U_d},  U_d = min{i : v_p(i!) >= d}
import math
def vf(n,p):
    s=0
    while n: n//=p; s+=n
    return s
for p in [5,7,11,13,17,19,23,29,31]:
    lq=math.log(2/math.pi); tot=0.0; i=0
    for d in range(1,2000):
        while vf(i,p)<d: i+=1
        lt=d*math.log(p)+math.log(1-1/p) + i*lq
        if lt>-700: tot+=math.exp(lt)
    print(f"p={p:3d}  Lambda_p={tot:.6f}  C_max=1/Lambda_p={1/tot:.3f}")
