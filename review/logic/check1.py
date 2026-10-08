# Independent referee checks (logic lens), written from scratch.
import itertools, math, sys


def vp(n,p):
    if n==0: return 10**9
    k=0
    while n%p==0: n//=p; k+=1
    return k
def pi(b,x):
    r=1
    for l in range(1,b+1): r*=(x+l)
    return r

def gamma(p,m):
    # max_{B subset [1,m-1]} v_p(1+sum pi_b(-m)), meet in middle
    if m==2: return None
    terms=[pi(b,-m) for b in range(1,m)]
    h=len(terms)//2
    def sums(ts):
        s=[0]
        for t in ts: s=s+[x+t for x in s]
        return s
    L=[1+x for x in sums(terms[:h])]; R=sums(terms[h:])
    K=0
    while True:
        M=p**(K+1)
        rs=set(r%M for r in R)
        if any((-l)%M in rs for l in L): K+=1
        else: return K

print("gamma_2:", {m:gamma(2,m) for m in [4,6,8,10,12,14,18,24,26,30,34]})
print("gamma_3:", {m:gamma(3,m) for m in [3,5,6,8,9,11]})
print("gamma_5:", {m:gamma(5,m) for m in [4,5,7,17]})
print("gamma_7(4)",gamma(7,4),"gamma_13(13)",gamma(13,13))
print("gamma_2(2^k+2):",[gamma(2,2**k+2) for k in range(1,6)])
print("gamma_3(5),gamma_3(11):",gamma(3,5),gamma(3,11))

def Phi(p):
    out=[]
    for r in range(p):
        m=p-r
        if m==2: continue
        terms=[pi(b,-m)%p for b in range(1,m)]
        s={1%p}
        for t in terms: s|={(x+t)%p for x in s}
        if 0 not in s: out.append(r)
    return out
for p in [3,5,7,11,13,17,19,23]: print("Phi",p,Phi(p))

# A_N mod 81 for 81|N via t!, t<=8; and actual N
S={0}
for t in range(9): S|={(x+math.factorial(t))%81 for x in S}
print("missing mod 81:",sorted(set(range(81))-S))
for N in [81,162,81*5,243,81*7]:
    terms=[pi(j,N)%81 for j in range(0,40)]
    s={0}
    for t in terms: s|={(x+t)%81 for x in s}
    print(" N=",N,"missing",sorted(set(range(81))-s))
# which N mod 81 give A_N mod 81 full (p=3)
full=[]
for N in range(81):
    terms=[pi(j,N)%81 for j in range(0,14)]
    s={0}
    for t in terms: s|={(x+t)%81 for x in s}
    if len(s)==81: full.append(N)
print("p=3 N mod 81 with A_N full mod 81:",full)

# p=2 mod 16 never full
bad=[r for r in range(16) if len({sum(c) %16 for c in []})<0]
nf=[]
for r in range(16):
    terms=[pi(j,r)%16 for j in range(16)]
    s={0}
    for t in terms: s|={(x+t)%16 for x in s}
    nf.append(len(s))
print("p=2 |A_r mod 16| for r=0..15:",nf)

# g >= G classes
def gge(p,G,c):
    M=p**G
    s={1%M}
    for b in range(1,p*G):
        t=pi(b,c)%M
        s|={(x+t)%M for x in s}
        if 0 in s: return True
    return 0 in s
print("p=2 counts k=1..6:",[sum(gge(2,k,c) for c in range(2**k)) for k in range(1,7)])
print("p=2 classes mod 8 with g>=4:",[c for c in range(8) if gge(2,4,c)])
# p=7 delta_2, delta_3
c2=sum(gge(7,2,c) for c in range(49)); print("p=7 #g>=2 mod 49:",c2)
