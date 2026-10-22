# Random test of Prop 11.25: alive paths at n with V_n>=Vcert have slope <= L. Also W_n bookkeeping.
import random,sys
P=200; MOD=1<<P
def v2(a):
    a%=MOD
    if a==0: return P
    return (a & -a).bit_length()-1
cls={'C0':(0,8,1,4),'C2':(2,8,3,7),'C6':(6,16,6,11)}
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
for name,(r0,mod,L,Vc) in cls.items():
    worst=0; npts=int(sys.argv[2]) if len(sys.argv)>2 else 300
    for _ in range(npts):
        x=(r0+mod*random.getrandbits(P))%MOD
        # paths: list of (S,S') at current n ; start n=1: e0=1, S=pi_0=1
        pij=1; dpij=0; V=0
        paths=[(1,0)]; n=1
        # at step n, pi_n = pi_{n-1}*(x+n)
        while True:
            newpi=(pij*(x+n))%MOD; newdpi=(dpij*(x+n)+pij)%MOD
            # extend: paths of length n -> length n+1 with e_n in {0,1} using pi_n? careful indices
            # path length n uses pi_0..pi_{n-1}; we hold pij=pi_{n-1}
            # alive at n: v(S)>=V_n where V_n=v(pi_n)
            Vn=v2(newpi)
            if Vn>P-30: break
            paths=[(S,dS) for (S,dS) in paths if v2(S)>=Vn]
            if Vn>=Vc:
                for S,dS in paths:
                    lam=v2(dS); worst=max(worst,lam)
                    assert lam<=L,(name,n,lam)
            # children: add e_n*pi_n
            paths=[(S,dS) for (S,dS) in paths]+[((S+newpi)%MOD,(dS+newdpi)%MOD) for (S,dS) in paths]
            pij,dpij=newpi,newdpi; n+=1
            if len(paths)>200000: print("blowup",name); break
    print(name,"max slope seen",worst,"L",L)
