import sys, subprocess, math
def Ep(p,L):
    M=p**L
    return M,[(-1)**u*pow(math.factorial(u),-1,M)%M for u in range(p)]
def cover(M,xs):
    out=subprocess.run(["./rcover"],input=f"{M} {len(xs)} "+" ".join(map(str,xs)),capture_output=True,text=True).stdout
    return int(out.split()[1])
p=int(sys.argv[1]); Ls=[int(x) for x in sys.argv[2:]]
for L in Ls:
    M,xs=Ep(p,L)
    print("p=%d L=%d missing=%d"%(p,L,cover(M,xs)),flush=True)
