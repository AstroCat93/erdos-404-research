# Extra post-processing (round-3 retry): per-maxv-bucket contributions to EZ and EZ^2, EZ growth, ratio vs p^G/4,
# and the 2*delta_G*G comparison with Kitamura's "11.5/G".  Reads data/annealed_p*_G*.txt and data/mc_cap*.txt.
import glob, re, os, math
from fractions import Fraction as Fr
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=open(W+"/data/annealed_buckets.tsv","w"); out.write("p\tG\tM_G\tmaxv\tclasses\tsurviving\tEZ_contrib\tEZ2_contrib\n")
summ=open(W+"/data/annealed_overview.tsv","w"); summ.write("p\tG\tM_G\tdelta_G\tEZ\tEZ2\tratio\tEZ2/(p^G/4)\tE[Z|Z>0]\tmaxZ\n")
for fn in sorted(glob.glob(W+"/data/annealed_p*_G*.txt")):
    t=open(fn).read(); m=re.search(r"# p=(\d+) G=(\d+) M_G=(\d+) p\^G=(\d+)",t)
    if not m or "total" not in t: continue
    p,G,MG,pG=map(int,m.groups())
    S1=S2=0; surv=0; mx=0
    for l in t.splitlines():
        if l.startswith("row "):
            v,cnt,sv,s1,s2,mxx=map(int,l.split()[1:])
            c1=Fr(s1,2**MG); c2=Fr(s2*pG,4**MG)   # contributions to EZ = sumN/2^M and EZ2 = p^G sumN2/4^M
            out.write(f"{p}\t{G}\t{MG}\t{v}\t{cnt}\t{sv}\t{float(c1):.5f}\t{float(c2):.6g}\n")
            S1+=s1; S2+=s2; surv+=sv; mx=max(mx,mxx)
    EZ=Fr(S1,2**MG); EZ2=Fr(S2*pG,4**MG); d=Fr(surv,pG)
    summ.write(f"{p}\t{G}\t{MG}\t{float(d):.6f}\t{float(EZ):.5f}\t{float(EZ2):.6g}\t{float(EZ2/EZ/EZ):.6g}\t{float(EZ2/Fr(pG,4)):.4f}\t{float(EZ/d):.4f}\t{float(Fr(mx*pG,2**MG)):.6g}\n")
out.close(); summ.close()
print(open(W+"/data/annealed_overview.tsv").read())
# Kitamura comparison: 2*delta_G*G from the Monte Carlo (fraction among even x)
print("G  delta_G(MC,best)  2*delta_G*G   (Kitamura's 11.5/G would mean 2*delta_G*G = 11.5 if measured among even a)")
import csv
rows=list(csv.DictReader(open(W+"/data/delta_G2_montecarlo.tsv"),delimiter="\t"))
best={}
for r in rows:
    G=int(r["G"]); se=float(r["stderr"])
    if G not in best or se<best[G][1]: best[G]=(float(r["delta"]),se,int(r["samples"]))
with open(W+"/data/kitamura_11p5_comparison.tsv","w") as f:
    f.write("G\tdelta_G\tstderr\t2*delta_G*G\tstderr_of_that\n")
    for G in sorted(best):
        d,se,ns=best[G]; print(f"{G:5d} {d:.5f}+-{se:.5f}  {2*d*G:.2f}+-{2*se*G:.2f}"); f.write(f"{G}\t{d:.6f}\t{se:.6f}\t{2*d*G:.3f}\t{2*se*G:.3f}\n")
