import math,csv,re,sys
D='data/'
# census
cen={}
for l in open('../../publish-erdos404/review/computation/census_p2_32.out'):
    m=re.match(r'p=2 G=(\d+) count=(\d+) delta',l)
    if m: cen[int(m[1])]=int(m[2])/2**int(m[1])
# MC
runs={}
for cap in (126,256,512,1024,2046):
    f=open(D+f'mc_cap{cap}.txt');h=f.readline()
    ns=int(re.search(r'ns=(\d+)',h)[1]); ov=int(re.search(r'overflow_samples=(\d+)',h)[1])
    s={int(m[1]):int(m[2]) for l in f for m in [re.match(r'k=(\d+) surv=(\d+)',l)] if m}
    assert ov==0 and len(s)==cap+1 and all(s[k]>=s[k+1] for k in range(cap)) and s[0]==ns
    runs[cap]=(ns,s)
print('max |z| vs census G<=32 per cap:')
for cap,(ns,s) in runs.items():
    zs=[(s[G]/ns-cen[G])/math.sqrt(cen[G]*(1-cen[G])/ns) for G in range(1,33)]
    print(cap, round(max(abs(z) for z in zs),2))
best={}
for G in (64,96,126,128,192,256,384,512,768,1024,1536,2046):
    cap=min(c for c in runs if c>=G and c!=126) if G!=126 else 126
    # most samples among caps>=G
    cap=max((c for c in runs if c>=G), key=lambda c:runs[c][0])
    ns,s=runs[cap]; d=s[G]/ns; se=math.sqrt(d*(1-d)/ns); best[G]=(d,se)
    print(f'G={G} cap={cap} delta={d:.5f} se={se:.5f} dG={d*G:.3f}')
# fits (weighted log-log, w=(d/se)^2) and local exponents
def fit(lo):
    pts=[(G,d,se) for G,(d,se) in best.items() if G>=lo and G!=126]
    w=[(d/se)**2 for _,d,se in pts]; x=[math.log(G) for G,_,_ in pts]; y=[math.log(d) for _,d,_ in pts]
    W=sum(w); xm=sum(wi*xi for wi,xi in zip(w,x))/W; ym=sum(wi*yi for wi,yi in zip(w,y))/W
    b=sum(wi*(xi-xm)*(yi-ym) for wi,xi,yi in zip(w,x,y))/sum(wi*(xi-xm)**2 for wi,xi in zip(w,x))
    a=ym-b*xm; chi=sum(wi*(yi-a-b*xi)**2 for wi,xi,yi in zip(w,x,y))
    xm2=sum(x)/len(x);ym2=sum(y)/len(y);b2=sum((xi-xm2)*(yi-ym2) for xi,yi in zip(x,y))/sum((xi-xm2)**2 for xi in x)
    print(f'fit G>={lo}: n={len(pts)} C={math.exp(a):.3f} c={-b:.3f} chi2={chi:.1f}  unweighted c={-b2:.3f}')
for lo in (64,128,256,512): fit(lo)
Gs=[64,96,128,192,256,384,512,768,1024,1536,2046]
for g1,g2 in zip(Gs,Gs[1:]):
    (d1,s1),(d2,s2)=best[g1],best[g2]; c=-math.log(d2/d1)/math.log(g2/g1); e=math.sqrt((s1/d1)**2+(s2/d2)**2)/math.log(g2/g1)
    print(f'local {g1}->{g2}: {c:.3f}({e:.3f})')
# survivors
surv={}
for cap in (1022,2046,4094):
    surv[cap]={int(a):int(g) for l in open(D+f'surv_cap{cap}.txt') if not l.startswith('#') for a,g in [l.split()]}
    assert len(surv[cap])==4096 and -1 not in surv[cap].values()
for a in surv[1022]: assert surv[1022][a]==min(surv[2046][a],1022) and surv[2046][a]==min(surv[4094][a],2046)
g=surv[4094]
for A in (256,1024,4096):
    print('N(%d,G):'%A, [sum(1 for a in range(1,A+1) if g[a]>=G) for G in (8,16,32,64,128,256,512,1024,2048,3072,4094)])
print('survivors cap 4094:', [a for a in g if g[a]>=4094])
for G in (8,16,32): print('locality G=%d'%G, sum(1 for a in range(1,4097) if g[a]>=G)/4096, cen[G])
kit={int(r['a']):(r['status'],int(r['value'])) for r in csv.DictReader(open('kitamura/p2_exact_table_1_256.csv'))}
mm=[a for a in range(1,257) if min(kit[a][1],4094)!=g[a]]
print('kitamura rows',len(kit),'statuses',set(s for s,_ in kit.values()),'mismatches',mm)
# gate
for p in (11,13):
    txt=open(D+f'gatesum_p{p}.txt').read(); I=float(re.search(r'I_p=([\d.e-]+)',txt)[1])
    r=[float(m[2])/(int(m[1])*(1-1/p)*I) for m in re.finditer(r'p^%d i=\d+ p\^i=(\d+) Lunit=([\d.e+-]+)'%p,txt)]
    r=[float(m[2])/(int(m[1])*(1-1/p)*I) for m in re.finditer(r'i=\d+ p\^i=(\d+) Lunit=([\d.e+-]+)',txt)]
    print(f'p={p} I_p={I} I/(2/pi)^p={I/(2/math.pi)**p:.5f} ratios', [round(x,7) for x in r])
    print(open(D+f'gatesum_p{p}_ngl{32 if p==11 else 8}.txt').read().strip()[-120:])
