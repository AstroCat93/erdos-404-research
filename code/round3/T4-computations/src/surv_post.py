# Task (2): N(A,G) = #{1<=a<=A : g_2(a) >= G} from data/surv_cap*.txt (exact capped g values; consistency across caps checked).
import os, math, glob
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caps={}
for fn in sorted(glob.glob(W+"/data/surv_cap*.txt")):
    cap=int(fn.split("cap")[1].split(".")[0]); d={}
    for line in open(fn):
        if line.startswith("#") or not line.strip(): continue
        a,g=map(int,line.split()); d[a]=g
    if d: caps[cap]=d
capsl=sorted(caps)
print("caps available:",capsl)
# consistency: for cap1<cap2, g1 = min(g2, cap1)
for i in range(len(capsl)-1):
    c1,c2=capsl[i],capsl[i+1]; bad=[a for a in caps[c1] if caps[c1][a]!=min(caps[c2].get(a,-5),c1) and a in caps[c2]]
    print(f"consistency cap{c1} vs cap{c2}: {len(bad)} mismatches", bad[:5])
top=capsl[-1]; g=caps[top]
ovf=[a for a in g if g[a]<0]; print("population overflows at top cap:",ovf)
out=open(W+"/data/survivors_NAG.tsv","w"); out.write("G\tN256\tN1024\tN4096\tN256*G/256\tN1024*G/1024\tN4096*G/4096\tN256*sqrtG/256\tN1024*sqrtG/1024\tN4096*sqrtG/4096\t11.5/G\n")
Gs=[1,2,3,4,5,6,7,8,10,12,14,16,20,24,28,32,40,48,56,64,80,96,112,128,160,192,224,254,256,320,384,448,512,640,768,896,1022,1024,1280,1536,1792,2046,2048,2560,3072,3584,4094]
for G in Gs:
    if G>top: break
    N=[sum(1 for a in range(1,A+1) if g[a]>=G) for A in (256,1024,4096)]
    out.write(f"{G}\t{N[0]}\t{N[1]}\t{N[2]}\t{N[0]*G/256:.4f}\t{N[1]*G/1024:.4f}\t{N[2]*G/4096:.4f}\t{N[0]*math.sqrt(G)/256:.4f}\t{N[1]*math.sqrt(G)/1024:.4f}\t{N[2]*math.sqrt(G)/4096:.4f}\t{11.5/G:.4f}\n")
out.close(); print(open(W+"/data/survivors_NAG.tsv").read())
# exact g distribution among survivors beyond 32 and the deep survivors list
deep=sorted([a for a in g if g[a]>=top]); print(f"a<=4096 with g_2(a) >= {top}: {len(deep)}:", deep)
exact=sorted([(g[a],a) for a in g if 32<=g[a]<top], reverse=True)[:40]; print("largest exact g values below the cap (g,a):", exact)
# Kitamura cross-check for a<=256
import csv
try:
    rows=list(csv.DictReader(open(W+"/kitamura/p2_exact_table_1_256.csv")))
    def v2f(a):
        s=0
        while a: a//=2; s+=a
        return s
    kg={int(r['a']): int(r['value'])-v2f(int(r['a'])) for r in rows}
    bad=[a for a in kg if min(kg[a],top)!=g[a]]
    print("Kitamura exact table (a<=256) vs ours (capped at %d): %d mismatches %s"%(top,len(bad),bad[:10]))
except Exception as e: print("kitamura check skipped",e)
