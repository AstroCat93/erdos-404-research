# Post-process data/annealed_p*_G*.txt (exact integer rows) into conditioned moments.
# Z = p^G N / 2^{M_G}.  For threshold K: moments restricted to classes with maxv <= K, where
# maxv = max_{1<=i<=M_G} v_p(x+i).  Output: data/annealed_summary.tsv (machine-readable) + stdout table.
import glob, re, math, os, sys
from fractions import Fraction as Fr
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[]
for fn in sorted(glob.glob(W+"/data/annealed_p*_G*.txt")):
    txt=open(fn).read()
    m=re.search(r"# p=(\d+) G=(\d+) M_G=(\d+) p\^G=(\d+)",txt)
    if not m or "total" not in txt: continue
    p,G,MG,pG=map(int,m.groups())
    buckets=[]
    for line in txt.splitlines():
        if line.startswith("row "):
            v,cnt,surv,S1,S2,mx=line.split()[1:]
            buckets.append((int(v),int(cnt),int(surv),int(S1),int(S2),int(mx)))
    rows.append((p,G,MG,pG,buckets))
rows.sort()
out=open(W+"/data/annealed_summary.tsv","w")
out.write("p\tG\tM_G\tcond\tK\tmeasure\tdelta_cond\tEZ\tEZ2\tratio\tEZ_given_surv\tmaxZ\n")
def stats(p,G,MG,pG,bk,K,label):
    cnt=sum(b[1] for b in bk if b[0]<=K); surv=sum(b[2] for b in bk if b[0]<=K)
    S1=sum(b[3] for b in bk if b[0]<=K); S2=sum(b[4] for b in bk if b[0]<=K); mx=max([b[5] for b in bk if b[0]<=K] or [0])
    if cnt==0: return None
    # E[Z ; maxv<=K] normalised by the conditional measure: E[Z | maxv<=K]
    EZ=Fr(S1*pG, 2**MG*cnt); EZ2=Fr(S2*pG*pG, 4**MG*cnt)
    ratio=EZ2/EZ/EZ if EZ else float('nan')
    meas=Fr(cnt,pG); dl=Fr(surv,cnt)
    EZs=EZ/dl if surv else float('nan')
    out.write(f"{p}\t{G}\t{MG}\t{label}\t{K}\t{float(meas):.8g}\t{float(dl):.8g}\t{float(EZ):.8g}\t{float(EZ2):.8g}\t{float(ratio):.8g}\t{float(EZs):.8g}\t{float(Fr(mx*pG,2**MG)):.6g}\n")
    return (float(meas),float(dl),float(EZ),float(EZ2),float(ratio),float(EZs))
print("p G M_G | all: delta EZ EZ2 ratio | K=ceil(2log_p M_G): K meas delta_K EZ_K EZ2_K ratio_K | K=ceil(log_p M_G)+1: K meas delta EZ EZ2 ratio")
for p,G,MG,pG,bk in rows:
    a=stats(p,G,MG,pG,bk,99,"all")
    K2=math.ceil(2*math.log(MG)/math.log(p)); b=stats(p,G,MG,pG,bk,K2,"maxv<=2log_p(M_G)")
    K1=math.ceil(math.log(MG)/math.log(p))+1; c=stats(p,G,MG,pG,bk,K1,"maxv<=log_p(M_G)+1")
    for K in range(1,40): 
        if any(x[0]<=K for x in bk): stats(p,G,MG,pG,bk,K,"maxv<=K")
    print(f"{p} {G} {MG} | {a[1]:.5f} {a[2]:.4g} {a[3]:.4g} {a[4]:.4g} | {K2} {b[0]:.4f} {b[1]:.5f} {b[2]:.4g} {b[3]:.4g} {b[4]:.4g} | {K1} {c[0]:.4f} {c[1]:.5f} {c[2]:.4g} {c[3]:.4g} {c[4]:.4g}")
out.close()
