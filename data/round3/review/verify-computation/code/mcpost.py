import sys, math
h={}; h16={}; N=0
for l in open(sys.argv[1]):
    if l.startswith("#"): N=int(l.split("N=")[1].split()[0]); continue
    a=l.split(); g=int(a[0][2:]); c=int(a[1][6:]); h[g]=c
    if "by_x_mod16:" in l: h16[g]=list(map(int,l.split("by_x_mod16:")[1].split()))
cap=max(h)
def delta(G): return sum(c for g,c in h.items() if g>=G)/N
for G in [8,16,24,29,32,48,64,96,126]:
    d=delta(G); se=math.sqrt(d*(1-d)/N)
    s14=sum(h16[g][14] for g in h if g>=G); sev=sum(sum(h16[g][r] for r in range(0,16,2)) for g in h if g>=G)
    print(f"G={G} delta={d:.6f}({se:.6f})  share of x=14 mod 16 among even survivors={s14/sev:.3f}")
