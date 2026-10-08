import sys
def gge(p,G,c):
    M=p**G; mask=(1<<M)-1; s=1<<(1%M); r=1
    for b in range(1,p*G):
        r=r*(c+b)%M
        if r: s|=((s<<r)|(s>>(M-r)))&mask
        if s&1: return True
    return bool(s&1)
for p,Gm,show in [(2,16,[4,8,12,16]),(3,8,[1,4,8]),(5,5,[1,4]),(7,3,[1,2,3])]:
    surv=[0] ; G=0; out={}
    surv=[c for c in range(p) if gge(p,1,c)]; G=1; out[1]=len(surv)/p
    while G<Gm:
        G+=1
        surv=[c+j*p**(G-1) for c in surv for j in range(p) if gge(p,G,c+j*p**(G-1))]
        out[G]=len(surv)/p**G
    print(p,{g:round(out[g],5) for g in show},flush=True)
