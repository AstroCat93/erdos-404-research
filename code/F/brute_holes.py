import sys, math
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def holes(p,A,B):
    e=lambda x: sum(vp(k,p) for k in range(1,x+1))
    eA,eB=e(A),e(B); M=p**(eB-eA)
    S=1  # bitmask of reachable residues (relative)
    full=(1<<M)-1
    for n in range(A,B):
        w=(math.factorial(n)//p**eA)%M
        S=S|(((S<<w)|(S>>(M-w)))&full)
    return M-bin(S).count('1')
p,A,B=map(int,sys.argv[1:4]); print(holes(p,A,B))
