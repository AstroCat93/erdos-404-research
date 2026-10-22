# Re-fit of T4's Monte Carlo table (their data file read as data): for each G take the run with the most samples
# among runs with cap >= G; weighted log-log LS; report chi2. Also show which run each point came from.
import numpy as np, csv
rows=list(csv.DictReader(open("../T4-computations/data/delta_G2_montecarlo.tsv"),delimiter="\t"))
best={}
for r in rows:
    G=int(r['G']); n=int(r['samples']); 
    if G not in best or n>int(best[G]['samples']): best[G]=r
def fit(Gs):
    x=np.log([g for g in Gs]); y=np.log([float(best[g]['delta']) for g in Gs])
    s=np.array([float(best[g]['stderr'])/float(best[g]['delta']) for g in Gs]); w=1/s**2
    A=np.vstack([np.ones_like(x),x]).T; W=np.diag(w)
    cov=np.linalg.inv(A.T@W@A); b=cov@A.T@W@y
    chi2=float(((y-A@b)**2*w).sum())
    return np.exp(b[0]),-b[1],np.sqrt(cov[1,1]),chi2,len(Gs)-2
for lo in [64,128,256,512]:
    Gs=[g for g in sorted(best) if lo<=g<=2046]
    C,c,ce,chi2,dof=fit(Gs)
    print(f"[{lo},2046] n={len(Gs)} C={C:.3f} exponent={c:.3f}+-{ce:.3f} chi2/dof={chi2:.1f}/{dof}  runs(cap)={[best[g]['cap_run'] for g in Gs]}")
