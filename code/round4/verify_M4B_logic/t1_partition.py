#!/usr/bin/env python3
"""t1_partition.py -- Lemma B1a and the G_{l-1}-measurability of B_l for random window times.

usage: t1_partition.py p seed nx n0 n1 L rule [kcap] [onestep]
  rule in {ladder, hash}; onestep=1 is the NEGATIVE CONTROL (n_{l+1} read from x mod p^{m_l}).
For random x (half of them with a forced gate v(x+i) = s, s <= 12, i <= n_L) and random z != 0:
  (a) partition / refinement:  M_{n_l} < m_l and m_l >= m_{l-1};
  (b) Lemma B1a: at x' = x + p^{m_l(x)} z, recomputed from scratch, n_0..n_{l+1}(x') = n_0..n_{l+1}(x)
      and m_0..m_l(x') = m_0..m_l(x);
  (c) two-step predictability: at x' = x + p^{m_{l-1}(x)} z, n_{l+1}(x') = n_{l+1}(x);
  (d) B_l measurability (l >= 1): at x' = x + p^{m_{l-1}} z the first event
      {D_{l-1}+D_l <= m_{l-1}-M_{n_{l+1}}, M_{n_{l+1}} < m_{l-1}} has the same truth value, and when it
      holds and K = D_{l-1}+D_l <= kcap, eps_l(x') == eps_l(x) exactly (Fractions).
With onestep=1, (c) and (d) are expected to FAIL in some cases (shows the test is sensitive).
"""
import random
import sys

from vlib import PAdic, eps_composite, rule_hash, rule_ladder, window_times


def first_event(P, x, ns, ms, l):
    n_prev, n_next = ns[l - 1], ns[l + 1]
    m_prev = ms[l - 1]
    M = max(P.v(x + i) for i in range(1, n_next + 1))
    if not M < m_prev:
        return False, None, None
    D = ms[l] - ms[l - 1]
    D2 = ms[l + 1] - ms[l]
    return (D + D2 <= m_prev - M), D, D + D2


def main():
    a = sys.argv[1:]
    p, seed, nx, n0, n1, L = (int(t) for t in a[:6])
    rname = a[6]
    kcap = int(a[7]) if len(a) > 7 else 6
    onestep = int(a[8]) if len(a) > 8 else 0
    rule = rule_ladder() if rname == "ladder" else rule_hash()
    P = PAdic(p, 220)
    rnd = random.Random(seed)
    cnt = dict(a=0, b=0, c=0, d1=0, d2=0)
    bad = dict(a=0, b=0, c=0, d1=0, d2=0)
    nmax_seen = 0
    for it in range(nx):
        x = rnd.randrange(P.mod)
        if it % 2:
            ns_tmp, _ = window_times(p, x, n0, n1, rule, L, P, onestep)
            i = rnd.randrange(1, ns_tmp[-1] + 1)
            s = rnd.randrange(1, 13)
            x = (-i + p ** s * (1 + p * rnd.randrange(p ** 150))) % P.mod  # v(x+i) = s exactly
        ns, ms = window_times(p, x, n0, n1, rule, L, P, onestep)
        nmax_seen = max(nmax_seen, ns[-1])
        for l in range(L + 1):
            cnt['a'] += 1
            M = max(P.v(x + i) for i in range(1, ns[l] + 1))
            if not (M < ms[l] and (l == 0 or ms[l] >= ms[l - 1])):
                bad['a'] += 1
        for l in range(L):
            z = rnd.randrange(1, p ** 40)
            xp = x + p ** ms[l] * z
            ns2, ms2 = window_times(p, xp, n0, n1, rule, L, P, onestep)
            cnt['b'] += 1
            if ns2[:l + 2] != ns[:l + 2] or ms2[:l + 1] != ms[:l + 1]:
                bad['b'] += 1
        for l in range(1, L):
            z = rnd.randrange(1, p ** 40)
            xp = x + p ** ms[l - 1] * z
            ns2, ms2 = window_times(p, xp, n0, n1, rule, L, P, onestep)
            cnt['c'] += 1
            if ns2[:l + 2] != ns[:l + 2]:
                bad['c'] += 1
                continue  # times differ: B_l cannot even be compared (negative control)
            fe, D, K = first_event(P, x, ns, ms, l)
            fe2, D_, K_ = first_event(P, xp, ns2, ms2, l)
            cnt['d1'] += 1
            if fe != fe2:
                bad['d1'] += 1
                continue
            if fe and K <= kcap:
                cnt['d2'] += 1
                e1 = eps_composite(x, ns[l - 1], ns[l], ns[l + 1], p, D, K)
                e2 = eps_composite(xp, ns2[l - 1], ns2[l], ns2[l + 1], p, D_, K_)
                if e1 != e2 or (D, K) != (D_, K_):
                    bad['d2'] += 1
    tag = "NEGATIVE CONTROL (one-step rule)" if onestep else "two-step rule"
    print(f"RESULT t1 p={p} n0={n0} n1={n1} L={L} rule={rule.name} [{tag}] nx={nx} max n_L={nmax_seen}")
    for k, lab in (('a', 'partition/refinement M<m, m nondecreasing'),
                   ('b', 'Lemma B1a: times and m constant on A_l'),
                   ('c', 'n_(l+1) constant on A_(l-1)'),
                   ('d1', 'first event of B_l constant on A_(l-1)'),
                   ('d2', 'eps_l constant on A_(l-1) (exact)')):
        print(f"  ({k}) {lab}: failures {bad[k]}/{cnt[k]}")


if __name__ == "__main__":
    main()
