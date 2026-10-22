# Pointwise test of every deterministic step in the proof of Theorem 11.29, plus Monte Carlo of the
# probabilistic steps, on random x in each class.  Usage: t4_chain.py seed NS
import random, time, sys, math
from fractions import Fraction
from common import *
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 21)
NS=int(sys.argv[2]) if len(sys.argv)>2 else 400
BIAS=len(sys.argv)>3 and sys.argv[3]=='bias'
p3n=0
def hL(n,L): return 0.5*(n-math.log2(n)-3*L-4)
def BL(n0,L,l0,imax=6000):
    tot=0.0
    for i in range(1,imax):
        tot+=2.0**(-math.floor(hL(max(n0,i-l0),L))-1)
    return tot
def binom_cdf(N,t):
    if t<0: return 0.0
    return sum(math.comb(N,j) for j in range(0,min(N,t)+1))/2**N
viol=0; t0=time.time()
for cls in ("C0","C2","C6"):
    global_p3=0
    k,r0,L,l0,sL,EC,Vc=CLASSES[cls]
    for (G,n0) in ((128,19),(128,40),(256,40),(256,80),(512,60),(512,150)):
        T=G//2
        if T<n0+l0: continue
        K=int(math.floor(math.log2(T-l0+1)))
        assert 2**K<=T-l0+1<2**(K+1)
        if not (2**K>=l0 and K>k): continue
        ls=0
        while n0+(ls+2)*l0<=T: ls+=1     # l* = max{l : n_{l+1} <= T}
        ns=[n0+j*l0 for j in range(ls+2)]
        assert ns[ls+1]<=T and (ns[ls+1]+l0>T)
        cs=list(range(-3,8))
        cnt=dict(gG=0,good=0,goodG=0); hitP={c:0 for c in cs}; walk={c:0 for c in cs}; sY0=0.0
        for _ in range(NS):
            x=rand_in_class(cls,rng)
            if BIAS:  # low digits k..K-1 mostly ones (deep walk) or mostly zeros
                pr=rng.choice([0.1,0.9,0.97])
                bits=sum((1<<j) for j in range(k,K) if rng.random()<pr)
                x=(x>>K<<K)|bits|r0
            Vn={n:V(x,n) for n in ns}; 
            gam=[2*Mx(x,ns[l]+l0)+3*L+3<=Vn[ns[l]] for l in range(ls+1)]
            good=all(gam)
            # (P1) bad window => some i with v(x+i) > h_L(max(n0,i-l0))
            if not good:
                ok=any(v(x+i)>hL(max(n0,i-l0),L) for i in range(1,ns[ls]+l0+1))
                if not ok: print("P1 VIOLATION",cls,G,n0,hex(x%2**80)); viol+=1
            gG=g_at_least(x,G)
            cnt['gG']+=gG; cnt['good']+=good; cnt['goodG']+=good and gG
            # Y0
            if gam[0]:
                ps,_=alive_paths(x,n0)
                M0=sum((rho(x,n0,S,dS)[0] for b,S,dS in ps),Fraction(0))*Fraction(2)**(Vn[n0]-n0)
                sY0+=float(M0)
            Wn1=[ns[l+1]-V(x,ns[l+1]) for l in range(ls+1)]
            # P_{n_{l+1}} nonempty for l<=l*
            if good:
                for l in range(ls+1): assert V(x,ns[l+1])<G, "V_N >= G on E_good"
                cntl=alive_count_levels(x,[ns[l+1] for l in range(ls+1)],G)
                allP=all(cntl[ns[l+1]]>0 for l in range(ls+1))
                if gG and not allP: print("P2 VIOLATION",cls,G,n0); viol+=1
            # N_K and walk
            r=x%(1<<K); NK=(1<<K)-r if r else (1<<K)
            sr=s(r)
            assert NK-V(x,NK)<=1-sr, "Lemma 10.2(d) fails"
            for c in cs:
                hit=False
                for l in range(ls+1):
                    if all(gam[:l+1]) and Wn1[l]<=-c: hit=True; break
                if good and hit and allP if good else False: hitP[c]+=1
                if good and not hit:
                    if NK>n0 and not (sr<=c+sL):
                        print("P3 VIOLATION",cls,G,n0,c,hex(x%2**80)); viol+=1
                    if NK>n0: walk[c]+=1; p3n+=1
        mu=2.0**-k
        EY0=mu*sY0/NS
        print(f"{cls} G={G} n0={n0} K={K} l*={ls}: mu(C∩g>=G)≈{mu*cnt['gG']/NS:.4f}, mu(C∩Egood)≈{mu*cnt['good']/NS:.4f}, E[Y0 1_C]≈{EY0:.4f}, B_L={BL(n0,L,l0):.3g}, n0 2^-K={n0*2.0**-K:.3g}")
        for c in cs:
            print(f"   c={c}: mu(C∩Egood∩Hit∩allP)≈{mu*hitP[c]/NS:.4f} <=? 2^-c E[Y0 1_C]≈{2.0**-c*EY0:.4f};  mu(C∩Egood∖Hit∩NK>n0)≈{mu*walk[c]/NS:.4f} <=? {mu*binom_cdf(K-k,c+sL-s(r0)):.4f}")
print("P3 instances exercised",p3n); print("violations",viol,"time %.1fs"%(time.time()-t0))
