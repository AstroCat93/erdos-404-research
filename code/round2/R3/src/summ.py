import sys,re
rows={}
for line in open(sys.argv[1]):
    m=re.match(r"p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+).*ratio=([\d.e+-]+).*(HOLDS|FAILS)",line)
    if not m: continue
    p,t,H,c,M=map(int,m.groups()[:5]); r=float(m.group(6)); st=m.group(7)
    rows.setdefault((p,t),[]).append((H,c,r,st))
for (p,t),L in sorted(rows.items()):
    hold=[H for H,c,r,s in L if s=='HOLDS']
    fails_after=[H for H,c,r,s in L if s=='FAILS' and hold and H>min(hold)]
    hmin=min(hold) if hold else None
    rr=[r for H,c,r,s in L if H==hmin]
    print(f"p={p} t={t}: minimal H_t={hmin} (ratio {rr[0] if rr else '-':.3g}) ; failing H above it (within scan): {fails_after}")
