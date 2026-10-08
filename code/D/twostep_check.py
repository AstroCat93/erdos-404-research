#!/usr/bin/env python3
"""Check the p=2 two-step rule: at an even stage N with t = v_2(N+2), a state c in Z_2 has
  t = 1: 2 valid continuations to stage N+2;
  t >= 2: 2 if c == 0, 1 if c == +-1, 0 otherwise (mod 2^t);
and the children are (q + eta*w)/(u*w) with c = 2^t q + r, u = N+1, N+2 = 2^t w,
  r=0: eta in {0,1};  r=1: eta=1;  r=-1: eta=0.
Also the p=3 rule: at stage N == -3 mod 3^t (t>=1), c survives to N+3 iff c mod 3^t in {-3,...,2}."""
import random
R = 60
rnd = random.Random(1)
def v(n, p):
    k = 0
    while n % p == 0:
        n //= p; k += 1
    return k
bad = 0
for _ in range(20000):
    N = 2 * rnd.randrange(1, 10 ** 6)
    c = rnd.randrange(2 ** R)
    if rnd.random() < 0.5:  # bias towards c = 0, +-1 mod 2^t
        t0 = v(N + 2, 2); c = (c << t0) + rnd.choice([0, 1, -1])
    mod = 2 ** R
    t = v(N + 2, 2); u = N + 1; w = (N + 2) >> t
    kids = []
    for e1 in (0, 1):
        x = (c + e1) * pow(u, -1, mod) % mod  # c_{N+1}
        for e2 in (0, 1):
            y = x + e2
            if y % 2 ** t == 0:
                kids.append((y >> t) * pow(w, -1, mod) % 2 ** (R - t))
    r = c % 2 ** t
    if t == 1:
        exp = 2
    else:
        exp = 2 if r == 0 else (1 if r in (1, 2 ** t - 1) else 0)
    if len(kids) != exp:
        bad += 1
        continue
    if t >= 2 and exp > 0:
        rr = 0 if r == 0 else (1 if r == 1 else -1)
        q = (c - rr) >> t
        etas = [0, 1] if rr == 0 else ([1] if rr == 1 else [0])
        pred = sorted(((q + eta * w) * pow(u * w, -1, mod)) % 2 ** (R - t) for eta in etas)
        if pred != sorted(kids):
            bad += 1
print("p=2 two-step rule mismatches:", bad)
bad3 = 0
for _ in range(20000):
    t = rnd.randrange(1, 6)
    N = -3 + 3 ** t * rnd.randrange(1, 10 ** 5)
    if v(N + 3, 3) < t:
        continue
    c = rnd.randrange(3 ** 30); mod = 3 ** 30
    ok = False
    for e1 in (0, 1):
        x = (c + e1) * pow(N + 1, -1, mod) % mod
        for e2 in (0, 1):
            y = (x + e2) * pow(N + 2, -1, mod) % mod
            for e3 in (0, 1):
                if (y + e3) % 3 ** t == 0:
                    ok = True
    pred = (c % 3 ** t) in {x % 3 ** t for x in range(-3, 3)}
    if ok != pred:
        bad3 += 1
print("p=3 three-step rule mismatches:", bad3)
