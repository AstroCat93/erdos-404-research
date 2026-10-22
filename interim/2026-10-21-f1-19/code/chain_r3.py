#!/usr/bin/env python3
"""chain_r3.py -- chain check (note.md Proposition 10.10) for f(1,p) >= v_p((p^D-1)!), requiring for every
depth t < D either a uniform certificate Cov(p,t,H) (all unit classes mod p^c, H+1 < p^t) or position
certificates for every K'' < p^(D-t) (p !| K'', p^t K'' - H > 1), each certified by at least TWO programs.
Programs recognised: A/A' (lines 'A p=... missing=0 COVERED'), B ('B p=... notcovered=0 OK'), C/C' ('C p=... miss=0 COVERED').
usage: chain_r3.py p D LOGDIR[:LOGDIR...] SPECFILE [MINPROGS]   (spec lines: uniform t H / pos t H k0 k1; MINPROGS = programs required per certificate, default 2)
2026-10-20: added MINPROGS and a per-program report so that a chain resting on ONE program is reported as such."""
import glob, os, re, sys
def vf(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def collect(dirs):
    cert={}  # (p,t,H) -> {prog: set(K)}
    for d in dirs:
        for fn in glob.glob(os.path.join(d,'*.log')):
            for line in open(fn, errors='replace'):
                m=re.match(r"A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) (COVERED|NOT_COVERED)",line)
                if m:
                    p,t,H,K,miss=map(int,m.groups()[:5])
                    if miss==0 and m.group(6)=='COVERED': cert.setdefault((p,t,H),{}).setdefault('A',set()).add(K)
                    continue
                m=re.match(r"B p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) notcovered=(\d+) (OK|FAIL)",line)
                if m:
                    p,t,H,K,nc=map(int,m.groups()[:5])
                    if nc==0 and m.group(6)=='OK': cert.setdefault((p,t,H),{}).setdefault('B',set()).add(K)
                    continue
                m=re.match(r"C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=(\d+) miss=(\d+)(\S*) (COVERED|UNCOVERED)",line)
                if m:
                    p,t,H,K,Kpc,miss=map(int,m.groups()[:6])
                    if miss==0 and m.group(8)=='COVERED' and not m.group(7): cert.setdefault((p,t,H),{}).setdefault('C',set()).add(K)
    return cert
def uniform_ok(S,p,t,H):
    c=vf(H-1,p)
    if c==0: return len(S)>0
    pc=p**c; need={K for K in range(1,pc) if K%p}; have={K%pc for K in S}
    return need<=have
def main():
    p,D=int(sys.argv[1]),int(sys.argv[2]); dirs=sys.argv[3].split(':'); minp=int(sys.argv[5]) if len(sys.argv)>5 else 2
    spec=[ln.split() for ln in open(sys.argv[4]) if ln.strip() and not ln.startswith('#')]
    cert=collect(dirs)
    uni={}; pos={}; ok=True
    for row in spec:
        if row[0]=='uniform':
            t,H=int(row[1]),int(row[2]); progs=cert.get((p,t,H),{})
            good=[q for q,S in progs.items() if uniform_ok(S,p,t,H)]
            cond=H+1<p**t
            print(f"uniform Cov({p},{t},{H}): programs certifying all classes = {sorted(good)}; H+1<p^t={cond}")
            if len(good)>=minp and cond: uni[t]=H
            else: ok=False
        elif row[0]=='pos':
            t,H,k0,k1=map(int,row[1:5]); Ks=[K for K in range(k0,k1+1) if K%p]; progs=cert.get((p,t,H),{})
            good=[q for q,S in progs.items() if all(K in S for K in Ks)]
            cond=all(p**t*K-H>1 for K in Ks)
            miss={q:[K for K in Ks if K not in S][:8] for q,S in progs.items() if q not in good}
            print(f"positions depth {t} H={H} K''={k0}..{k1} ({len(Ks)}): programs certifying all = {sorted(good)}; N*-H>1={cond}" + (f"; incomplete: {miss}" if miss else ''))
            if len(good)>=minp and cond: pos.setdefault(t,set()).update(Ks)
            else: ok=False
    for t in range(1,D):
        if t in uni: continue
        need={K for K in range(1,p**(D-t)) if K%p}
        if not need<=pos.get(t,set()):
            print(f"depth {t}: NOT all positions below p^{D} certified by {minp} program(s) ({len(need-pos.get(t,set()))} missing)"); ok=False
    if ok: print(f"CHAIN OK ({minp} program(s) per certificate): no first failure below {p}^{D}; f(1,{p}) >= v_{p}(({p}^{D}-1)!) = {vf(p**D-1,p)}")
    else: print("CHAIN INCOMPLETE")
main()
