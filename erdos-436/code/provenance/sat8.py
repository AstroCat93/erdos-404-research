# Independent SAT test for Lambda(8,2) inside a fixed prefix region.
# Question: is there an assignment R: primes -> Z/8 extending the prefix, with no n<=L such that f(n)=f(n+1)=0?
# f completely additive, f(q)=R(q). Only "at least one value per prime" is needed: if several values of a
# prime are true in a model, any one of them gives an assignment with no zero pair n <= L.
# Usage: python3 sat8.py L PREFIX_FILE NFIX [SOLVER]   (writes vec8_L<L>_n<NFIX>.txt in the current directory)
# vectors/vec8_L1508323.txt is the output vec8_L1508323_n16.txt of a run with L=1508323, NFIX=16 (the prefix in
# sat8_prefix16.txt) and the PySAT solver name cadical153 (CaDiCaL 1.5.3). Since that run, only the output
# directory and these comments have changed.
import sys, time, itertools, numpy as np
from pysat.solvers import Solver
L=int(sys.argv[1]); prefix_file=sys.argv[2]; nfix=int(sys.argv[3]); K=8
solver_name=sys.argv[4] if len(sys.argv)>4 else 'cadical153'
pref=[tuple(map(int,l.split())) for l in open(prefix_file) if l.strip()][:nfix]
fixed={q:v%K for q,v in pref}
N=L+1
t0=time.time()
spf=np.zeros(N+1,dtype=np.int64)
for i in range(2,N+1):
    if spf[i]==0:
        spf[i::i][spf[i::i]==0]=i
spf=spf.tolist()
primes=[i for i in range(2,N+1) if spf[i]==i]
assert all(q in fixed for q in primes if q<=max(fixed)), "prefix must cover all primes up to its max"
var={}; nv=0
def newvar():
    global nv; nv+=1; return nv
for q in primes:
    if q not in fixed:
        var[q]=nv+1; nv+=8   # x_{q,v} = var[q]+v
clauses=[]
for q in var: clauses.append([var[q]+v for v in range(K)])
# z status per n: None => constant false, True => constant true, int => variable
zinfo=[None]*(N+2)
def fac(n):
    d={}
    while n>1:
        p=spf[n]; d[p]=d.get(p,0)+1; n//=p
    return d
facs=[None]*(N+2)
for n in range(1,N+1):
    d=fac(n); c=0; vp=[]
    for p,e in d.items():
        if p in fixed: c=(c+e*fixed[p])%K
        else: vp.append((p,e))
    facs[n]=(c,vp)
print("factored",time.time()-t0,file=sys.stderr)
def zvar(n):
    c,vp=facs[n]
    if not vp: return (c==0)
    z=newvar()
    ps=[p for p,_ in vp]; es=[e for _,e in vp]
    for vals in itertools.product(range(K),repeat=len(vp)):
        if (c+sum(e*v for e,v in zip(es,vals)))%K==0:
            clauses.append([-(var[p]+v) for p,v in zip(ps,vals)]+[z])
    return z
zcache={}
def getz(n):
    if n not in zcache: zcache[n]=zvar(n)
    return zcache[n]
closed_by=None
for n in range(1,L+1):
    a=facs[n]; b=facs[n+1]
    # quick skip: constant-false member
    if not a[1] and a[0]!=0: continue
    if not b[1] and b[0]!=0: continue
    za=getz(n); zb=getz(n+1)
    if za is True and zb is True:
        closed_by=n; break
    if za is True: clauses.append([-zb]); continue
    if zb is True: clauses.append([-za]); continue
    clauses.append([-za,-zb])
print(f"L={L} vars={nv} clauses={len(clauses)} build={time.time()-t0:.1f}s",file=sys.stderr)
if closed_by:
    print(f"RESULT L={L}: UNSAT trivially, prefix already has smooth zero pair at {closed_by}"); sys.exit()
with Solver(name=solver_name,bootstrap_with=clauses) as s:
    t1=time.time(); r=s.solve(); dt=time.time()-t1
    print(f"RESULT L={L} nfix={nfix} solver={solver_name}: {'SAT' if r else 'UNSAT'} in {dt:.1f}s")
    if r:
        m=set(x for x in s.get_model() if x>0)
        R=dict(fixed)
        for q,b in var.items():
            for v in range(K):
                if b+v in m: R[q]=v; break
        with open(f"vec8_L{L}_n{nfix}.txt","w") as F:
            for q in sorted(R): F.write(f"{q} {R[q]}\n")
        print("wrote vector")
