#!/usr/bin/env python3
"""Exact test of f(a,p) >= K by forward residue-set DP with exact pruning.

Definition: f(a,p) >= K  iff  exists finite T subset [a, oo), min T = a, p^K | sum_{n in T} n!.
Exactness of pruning: let N_K = min{N : v_p(N!) >= K}. Terms n >= N_K vanish mod p^K, so only
n < N_K matter. After deciding membership of n, every later term is divisible by
p^{min(K, v_p((n+1)!))}, hence a partial sum that is not 0 mod that power can never be completed;
dropping it loses nothing. States are residues mod p^K (a set), so the DP is exact.
Returns (reachable: bool, max_states).
"""
import sys

def vfact(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s

def test_ge(a, p, K, cap=5_000_000):
    if K <= 0:
        return True, 1
    M = p ** K
    NK = 0
    while vfact(NK, p) < K:
        NK += 1
    if a >= NK:            # a! itself is 0 mod p^K
        return True, 1
    fact = 1
    for i in range(2, a + 1):
        fact = fact * i % M
    states = {fact % M}
    mx = 1
    def prune(st, n):
        e = min(K, vfact(n + 1, p))
        q = p ** e
        return {s for s in st if s % q == 0}
    states = prune(states, a)
    for n in range(a + 1, NK):
        fact = fact * n % M
        if not states:
            break
        new = set(states)
        for s in states:
            new.add((s + fact) % M)
        states = prune(new, n)
        mx = max(mx, len(states))
        if len(states) > cap:
            raise RuntimeError(f"state cap exceeded at n={n}: {len(states)}")
    return (0 in states) if states else False, mx

def exact_f(a, p, kmax=100000, cap=5_000_000):
    """Return exact f(a,p) by increasing K until unreachable (f is the last reachable K)."""
    K = vfact(a, p)            # always reachable via T={a}
    stats = []
    while K <= kmax:
        ok, mx = test_ge(a, p, K + 1, cap)
        stats.append((K + 1, ok, mx))
        if not ok:
            return K, stats
        K += 1
    return None, stats

if __name__ == "__main__":
    a, p = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3:
        K = int(sys.argv[3])
        print(a, p, K, test_ge(a, p, K))
    else:
        f, st = exact_f(a, p)
        print(f"f({a},{p}) = {f}   (max states in final test: {st[-1][2]})")
