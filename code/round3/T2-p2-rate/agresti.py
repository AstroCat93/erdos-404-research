# Heuristic BPVE (Agresti) predictor: P(g_2(x)>=G | x) ~ min(1, kappa / A_G(x)),
# A_G(x) = sum_{k: x+k+1 odd, k < n_G} 2^{-W_{k+1}(x)}, n_G = first n with V_n(x) >= G, W_n = n - V_n.
import random, sys, math
def v2(z):
    return (z & -z).bit_length()-1
def agresti(x, G):
    V=0; n=0; A=0.0
    while V < G:
        n+=1; d=v2(x+n); V+=d
        W=n-V
        if d==0: A+=2.0**(-W)
    return A
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='haar':
        random.seed(7); S=int(sys.argv[2])
        Gs=[16,32,64,128,256,512,1024,2048,4096,8192,16384]
        acc={G:[] for G in Gs}
        for s in range(S):
            x=random.getrandbits(200)&~1
            for G in Gs: acc[G].append(agresti(x,G))
        for G in Gs:
            a=acc[G]
            m1=sum(1/v for v in a)/len(a)/2  # factor 1/2: only even x (odd x have g=0)
            print(G, 'E[1/A]/2=%.5g'%m1, 'G*E=%.4g'%(G*m1))
