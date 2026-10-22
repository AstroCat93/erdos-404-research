#!/usr/bin/env python3
"""R3Q (restarted) Lemma 3 certificates, implementation 1 (direct integer products).
(a) x=0 mod 8 : every e_1..e_5 with 16 | S_e(x) (length 6) has v(S_e'(x)) = 1         [x mod 16]
(b) x=2 mod 16: every e_1..e_7 with 2^7 | S_e(x) (length 8) has v(S_e'(x)) = 3        [x mod 128]
(c) x=6 mod 16: every e_1..e_9 with 2^11 | S_e(x) (length 10) has v(S_e'(x)) = 3      [x mod 2^11]
(d) x=10 mod 16: no e_1..e_5 with 2^7 | S_e(x) (length 6)                              [x mod 128]
(e) x=4 mod 8 : no e_1..e_3 with 2^4 | S_e(x) (length 4)                               [x mod 16]
Exhaustive; S_e(x) = sum_{j<n} e_j pi_j(x), e_0 = 1."""
from itertools import product
def v2(a): return (a & -a).bit_length()-1 if a else 99
def pis(x, n):
    p=[1]; d=[0]
    for j in range(1,n):
        d.append(d[-1]*(x+j)+p[-1]); p.append(p[-1]*(x+j))
    return p, d
def run(res, mod, n, lift, need_slope):
    bad=0; alive=0
    for x in range(res, 1<<lift, mod):
        p,d=pis(x,n)
        for e in product((0,1), repeat=n-1):
            E=(1,)+e
            S=sum(p[j] for j in range(n) if E[j]); Sp=sum(d[j] for j in range(n) if E[j])
            if S % (1<<lift)==0:
                alive+=1
                if need_slope is None or v2(Sp)!=need_slope: bad+=1
    return alive,bad
for name,args in [("a",(0,8,6,4,1)),("b",(2,16,8,7,3)),("c",(6,16,10,11,3)),("d",(10,16,6,7,None)),("e",(4,8,4,4,None))]:
    a,b=run(*args)
    ok = (b==0) if args[4] is not None else (a==0)
    print(f"({name}) residues {args[0]} mod {args[1]}, length {args[2]}, modulus 2^{args[3]}: qualifying words={a} violations={b if args[4] is not None else a}  {'OK' if ok else 'FAIL'}")
