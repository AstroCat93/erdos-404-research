#!/usr/bin/env python3
"""Summarise winvar logs (logs/r3/*.log) into markdown tables for writeup.md Sec. 6."""
import re,sys,glob,math
def parse_traj(fn):
    rows=[]; cmd=None; sample=None
    for line in open(fn):
        if line.startswith('CMD:'): cmd=line.split('./winvar')[1].split(); 
        elif line.startswith('X sample='): sample=int(line.split()[1].split('=')[1])
        elif line.startswith('W l=') and 'END' not in line and 'SKIPPED' not in line and 'ABORT' not in line:
            d=dict(kv.split('=',1) for kv in line[2:].split(' ') if '=' in kv and not kv.startswith('byorder'))
            d['p']=cmd[1]; d['L']=cmd[2]; d['sample']=sample; rows.append(d)
    return rows
out=[]
for p in (3,5,7):
    rows=parse_traj(f'logs/r3/traj_p{p}.log')
    out.append(f'\n**p = {p}** (trajectory mode; columns: L, sample, window [n,N), D, hypotheses W1W2W3ENV and W2\' (with lambda_max), |P^L| (parents with slope <= L), M_l, relative variance R, R*|P^L|, kappa, rho-weighted Weyl sums of phase points at orders p,p^2,p^3 and W_1*sqrt(|P^L|)):\n')
    out.append('| L | x# | [n,N) | D | hyp | W2\' | lam_max | \\|P^L\\| | M_l | R | R·\\|P^L\\| | κ | Weyl p/p²/p³ | W₁√\\|P^L\\| | exact |')
    out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for d in rows:
        pl=int(d['popL']); 
        if pl==0: continue
        R=float(d['relvar']); w=d['weyl'].split('/'); w1=float(w[0])
        out.append(f"| {d['L']} | {d['sample']} | [{d['n']},{d['N']}) | {d['D']} | {d['hyp']} | {d['W2b']} | {d['lammax']} | {pl} | {float(d['M']):.4g} | {R:.3g} | {R*pl:.2g} | {float(d['corr']):.2g} | {d['weyl']} | {w1*math.sqrt(pl):.2f} | {d['exact']}/{d['K']} |")
print('\n'.join(out))

# ---- atom Monte Carlo tables ----
def parse_atom(fn):
    blocks=[]; cur=None
    for line in open(fn):
        if line.startswith('CMD:'): cur={'cmd':line.split('./winvar')[1].split(),'rows':[],'atom':'','samples':''}; blocks.append(cur)
        elif line.startswith('# atom'): cur['atom']=line.strip()[2:]
        elif line.startswith('# samples'): cur['samples']=line.strip()[2:]
        elif re.match(r'^\s*\d+\s+\d+\s',line): cur['rows'].append(line.split())
    return blocks
out=['\n\n### Atom Monte Carlo (mode 2): E[M_l], E[M_l^2] over the digits above the atom\n']
for fn in ['logs/r3/atom2_p3.log','logs/r3/atom2_p5.log','logs/r3/atom2_p7.log','logs/r3/atom_p3.log','logs/r3/atom_p5.log']:
    for b in parse_atom(fn):
        c=b['cmd']; p,L,n0=c[1],c[2],c[4]
        if not b['rows'] or 'inf' in b['rows'][0][2]: 
            out.append(f"\n`{fn}` seed {c[0]}: p={p} L={L} n0={n0}: **no completed samples** (population cap exceeded on this atom at the last window)."); continue
        out.append(f"\n`{fn}` seed {c[0]}: p={p}, L={L}, n0={n0}, {b['atom']}, {b['samples']}\n")
        out.append('| l | n | E\\|P\\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |')
        out.append('|---|---|---|---|---|---|---|---|---|---|')
        for r in b['rows']:
            r=r+['']*(10-len(r)); out.append('| '+' | '.join(r[:10])+' |')
print('\n'.join(out))
