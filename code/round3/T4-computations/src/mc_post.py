# Task (3): delta_G(2) Monte Carlo estimates and power-law fits.
import os, glob, math, re
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
runs={}
for fn in sorted(glob.glob(W+"/data/mc_cap*.txt")):
    txt=open(fn).read(); m=re.search(r"ns=(\d+) seed=(\d+) CAP=(\d+).*maxpop=(\d+) overflow_samples=(\d+)",txt)
    if not m: continue
    ns,seed,cap,mp,ovf=map(int,m.groups()); d={}
    for line in txt.splitlines():
        if line.startswith("k="):
            k,s,f=line.split(); d[int(k[2:])]=int(s[5:])
    runs[cap]=(ns,seed,mp,ovf,d)
out=open(W+"/data/delta_G2_montecarlo.tsv","w"); out.write("G\tcap_run\tsamples\tsurvivors\tdelta\tstderr\tdelta*sqrtG\tdelta*G\tdelta*G^0.75\n")
exact={4:.375,8:.2421875,12:.1958007812,16:.1517028809,20:.1416854858,24:.1291697025,28:.1164024770,29:.1134132706,32:.1016}
pts=[]
for cap in sorted(runs):
    ns,seed,mp,ovf,d=runs[cap]
    print(f"cap={cap} ns={ns} seed={seed} maxpop={mp} overflow={ovf}")
    for G in [8,16,24,29,32,48,64,96,128,192,256,384,512,768,1024,1536,2046]:
        if G in d:
            p=d[G]/ns; se=math.sqrt(p*(1-p)/ns)
            out.write(f"{G}\t{cap}\t{ns}\t{d[G]}\t{p:.6f}\t{se:.6f}\t{p*math.sqrt(G):.4f}\t{p*G:.3f}\t{p*G**0.75:.4f}\n")
            ex=exact.get(G); print(f"  G={G:5d} delta={p:.5f} +- {se:.5f}  delta*sqrtG={p*math.sqrt(G):.4f} delta*G={p*G:.3f}" + (f"  exact={ex}" if ex else ""))
            if G>=64: pts.append((G,p,se,cap))
out.close()
# best estimate per G: the run with the most samples at that G (largest ns among caps >= G)
best={}
for G,p,se,cap in pts:
    if G not in best or se<best[G][1]: best[G]=(p,se,cap)
print("best estimates:",{G:(round(v[0],5),round(v[1],5)) for G,v in sorted(best.items())})
# local exponents and global fit delta ~ C G^-c (weighted least squares in log-log)
Gs=sorted(best); 
for i in range(len(Gs)-1):
    G1,G2=Gs[i],Gs[i+1]; p1,p2=best[G1][0],best[G2][0]
    print(f"local exponent between G={G1} and {G2}: c={-math.log(p2/p1)/math.log(G2/G1):.3f}")
xs=[math.log(G) for G in Gs]; ys=[math.log(best[G][0]) for G in Gs]; ws=[(best[G][0]/best[G][1])**2 for G in Gs]
sw=sum(ws); mx=sum(w*x for w,x in zip(ws,xs))/sw; my=sum(w*y for w,y in zip(ws,ys))/sw
c=-sum(w*(x-mx)*(y-my) for w,x,y in zip(ws,xs,ys))/sum(w*(x-mx)**2 for w,x in zip(ws,xs)); C=math.exp(my+c*mx)
print(f"weighted log-log fit over G in {Gs}: delta_G ~ {C:.3f} * G^-{c:.3f}")
for lo in [128,256]:
    sel=[G for G in Gs if G>=lo]
    if len(sel)>=2:
        xs=[math.log(G) for G in sel]; ys=[math.log(best[G][0]) for G in sel]; ws=[(best[G][0]/best[G][1])**2 for G in sel]
        sw=sum(ws); mx=sum(w*x for w,x in zip(ws,xs))/sw; my=sum(w*y for w,y in zip(ws,ys))/sw
        c=-sum(w*(x-mx)*(y-my) for w,x,y in zip(ws,xs,ys))/sum(w*(x-mx)**2 for w,x in zip(ws,xs)); C=math.exp(my+c*mx)
        print(f"fit over G >= {lo}: delta_G ~ {C:.3f} * G^-{c:.3f}")
