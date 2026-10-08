# Referee's independent witness verifier: S = sum_{n in A} n!  ; reports whether p^K | S and p^(K+1) | S.
# Descending Horner: F(n) = [n in A] + (n+1) F(n+1), S = F(1)  (requires min A = 1 for the f(1,p) claims)
import sys, re, time
def load(path):
    xs=[]
    with open(path) as f:
        for line in f:
            if line.startswith('#'): continue
            xs.extend(int(t) for t in re.findall(r'\d+', line))
    return xs
def verify(A, p, K, chunk=2000):
    A=sorted(A); assert len(set(A))==len(A)
    inA=set(A); top=max(A)
    M=p**(K+1)
    Mbits=M.bit_length()
    F=0
    n=top
    while n>=1:
        L=max(1,n-chunk+1)
        # chunk [L..n]: F(L) = Q + P*F(n+1), with P=prod_{k=L}^{n}(k+1)
        Q=0; P=1
        for k in range(n, L-1, -1):
            Q = (1 if k in inA else 0) + (k+1)*Q
            P *= (k+1)
        F = Q + P*F
        if F.bit_length() > Mbits + 400000:
            F %= M
        n=L-1
    F%=M
    okK = F % p**K == 0
    okK1 = F == 0
    return okK, okK1, A[0], len(A), top
if __name__=="__main__":
    path,p,K=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    t=time.time()
    A=load(path)
    r=verify(A,p,K)
    print("%s p=%d K=%d: min=%d terms=%d max=%d  p^K|S: %s  p^(K+1)|S: %s  (%.0fs)"%(path.split('/')[-1],p,K,r[2],r[3],r[4],r[0],r[1],time.time()-t),flush=True)
