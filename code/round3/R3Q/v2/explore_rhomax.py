#!/usr/bin/env python3
"""Exploration only [heuristic, not used in any proof]: size of max_s rho_n^{(lam)}(s) for random even x
and n in [50,500]; prints median and max over 30 samples. (The third column, labelled regular, uses
x+n = 2^40-1, which is NOT a regular environment; ignore it.)  usage: explore_rhomax.py"""
import random, sys
def v2(a): return (a & -a).bit_length()-1 if a else 10**9
def dist(x, n, lam):
    mod=1<<lam; d={0:1}; c=1; i=0
    while v2(c) < lam:
        cm=c%mod; nd={}
        for t,k in d.items():
            nd[t]=nd.get(t,0)+k; u=(t+cm)%mod; nd[u]=nd.get(u,0)+k
        d=nd; i+=1; c*= (x+n+i)
    tot=sum(d.values())
    return max(d.values())*mod/tot, len(d)/mod, i
rnd=random.Random(1)
for lam in (4,8,12,16,20):
    rs=[]
    for t in range(30):
        x=2*rnd.getrandbits(200); n=rnd.randrange(50,500)
        rs.append(dist(x,n,lam)[0])
    rs.sort()
    print(lam, "median rho_max", rs[15], "max", rs[-1], " regular:", dist(0, 2**40-1, lam))
