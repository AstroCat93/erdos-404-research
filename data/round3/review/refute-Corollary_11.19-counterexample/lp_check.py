"""(1) L_p = max{L : subset sums of E_p={(-1)^u/u!} cover Z/p^L}, own computation (bitset as python int).
(2) Corollary 11.19(a): pointwise N_{1,K}(tau) >= p^{min(J,L_p)}, J=min(K,v(tau+p)), for all tau, K=L_p+1..L_p+2;
    and D_p(1,L_p+1) >= 1-p^{-L_p} computed exactly (mpmath)."""
import math, mpmath as mp
mp.mp.dps=30
def Lp(p, Lmax):
    L=0
    for Lt in range(1, Lmax+1):
        M=p**Lt; bits=1; mask=(1<<M)-1
        for u in range(p):
            e=((-1)**u*pow(math.factorial(u),-1,M))%M
            bits|=((bits<<e)|(bits>>(M-e)))&mask
        if bits==mask: L=Lt
        else: break
    return L
def v(x,p,K):
    if x==0: return K
    c=0
    while x%p==0: x//=p; c+=1
    return min(c,K)
def N1(p,K,tau):
    pK=p**K; G=min(K,sum(v((tau+t)%pK,p,K) for t in range(1,p+1))); M=p**G
    q=[];cur=1
    for s in range(p):
        if s>0: cur=cur*(tau+s)%M
        q.append(cur%M)
    bits=1; mask=(1<<M)-1
    for a in q:
        if a: bits|=((bits<<a)|(bits>>(M-a)))&mask
    return bin(bits).count('1'), G
for p,Lmax in [(2,6),(3,6),(5,5),(7,4),(11,4),(13,4),(17,4),(19,4),(23,5)]:
    L = 1 if p==2 else Lp(p,Lmax)
    if p==2: print("p=2: E_2 subset sums mod 4:", sorted({0,1,(-1)%4,0}), "(L_2 set to 1 by the note)")
    for K in (L+1, L+2):
        if p**(K-1) > 3*10**5: continue
        bad=0; S=mp.mpf(0)
        for y in range(p**(K-1)):
            tau=p*y; n,G=N1(p,K,tau)
            J=min(K, v((tau+p)%p**K,p,K))
            assert G==J, (p,K,tau,G,J)
            if n < p**min(J,L): bad+=1
            S+=mp.log(n)/mp.log(p)
        D=mp.mpf(p-1)/p*S/p**(K-1)
        print(f"p={p} L_p={L} K={K} pointwise failures={bad} D={mp.nstr(D,12)} 1-p^-L={mp.nstr(1-mp.mpf(p)**(-L),12)} ok={D>=1-mp.mpf(p)**(-L)}")
