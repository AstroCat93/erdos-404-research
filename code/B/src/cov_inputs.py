# Print the Cov(p,t,H) block y_i(K) = prod_{s=1}^{i} (p^t K - (H-s)) mod p^(t+c), c = v_p((H-1)!), i = 0..H-1,
# in the input format of review/computation/rcover.c:  "M n y_0 ... y_{n-1}".
# usage: python3 cov_inputs.py p t H K | ../../../review/computation/rcover
import sys
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
p,t,H,K=map(int,sys.argv[1:5])
c=vfact(H-1,p); M=p**(t+c); X=p**t*K
out=[1%M]; pr=1
for i in range(1,H):
    pr=pr*(X-(H-i))%M; out.append(pr)
print(M,len(out)," ".join(map(str,out)))
