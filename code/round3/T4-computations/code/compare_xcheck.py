# compare code/xcheck_annealed chunk outputs (logs/xcheck_annealed.log) with src/annealed totals (data/annealed_p*_G*.txt)
import re,os,json
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res=[]
for line in open(W+"/logs/xcheck_annealed.log"):
    m=re.match(r"xcheck p=(\d+) G=(\d+) : (.*) elapsed (\d+) s",line)
    if not m: continue
    p,G=int(m.group(1)),int(m.group(2)); surv=sN=sN2=0; mx=0; ncl=0
    for part in m.group(3).split(";"):
        f=part.split()
        if len(f)<8: continue
        ncl+=int(f[3]); surv+=int(f[4]); sN+=int(f[5]); sN2+=int(f[6]); mx=max(mx,int(f[7]))
    t=open(W+f"/data/annealed_p{p}_G{G}.txt").read()
    mm=re.search(r"total classes=(\d+) surviving=(\d+) sumN=(\d+) sumN2=(\d+) maxN=(\d+)",t)
    ref=tuple(map(int,mm.groups()))
    ok=(ref==(ncl,surv,sN,sN2,mx))
    print(f"p={p} G={G}: xcheck classes={ncl} surv={surv} sumN={sN} sumN2={sN2} maxN={mx}  src/annealed={ref}  {'AGREE' if ok else 'MISMATCH'}  ({m.group(4)} s)")
    res.append({"p":p,"G":G,"classes":ncl,"surviving":surv,"sumN":str(sN),"sumN2":str(sN2),"maxN":mx,"agrees_with_src_annealed":ok,"seconds":int(m.group(4))})
json.dump(res,open(W+"/data/xcheck_annealed.json","w"),indent=1)
