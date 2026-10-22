#!/usr/bin/env python3
"""End-to-end test of the reduction "certificate => r(k,2,p) <= L" on real primes.

For each test prime p (p = 1 mod k, p > L+1):
  * pick a primitive k-th root of unity z = c^((p-1)/k) from a non-residue c of
    suitable order, and set R(q) = log_z(q^((p-1)/k)) for the first T primes q.
    (This is ind_g(q) mod k for SOME primitive root g; any g serves Lemma 1.)
  * walk the certificate tree with R (done by ccheck's walk mode) and read off the leaf n;
  * check independently, by modular exponentiation only, that n <= L and that
    n and n+1 are k-th power residues mod p;
  * compute r(k,2,p) by brute force and check r <= n.
Usage: e2e.py K L S2 RAW_CERT CCHECK WORKDIR [extra_primes_file]
"""
import sys, random, subprocess, os, json, time

K, L, S2s, raw, ccheck, work = sys.argv[1:7]
K = int(K); L = int(L)
extra = sys.argv[7] if len(sys.argv) > 7 else None
T = 400
rng = random.Random(4361508324 + K)


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


small_primes = []
c = 2
while len(small_primes) < T:
    if is_prime(c):
        small_primes.append(c)
    c += 1


def rand_prime(lo, hi):
    while True:
        p = rng.randrange(lo, hi)
        p -= (p - 1) % K
        if p > L + 1 and is_prime(p):
            return p


def root_of_unity(p):
    """a primitive K-th root of unity mod p"""
    e = (p - 1) // K
    for c in range(2, 10000):
        z = pow(c, e, p)
        # order of z is exactly K iff z^(K/q) != 1 for every prime q | K
        if all(pow(z, K // q, p) != 1 for q in {q for q in (2, 3, 5, 7) if K % q == 0}):
            return z
    raise RuntimeError


def assignment(p):
    z = root_of_unity(p)
    table = {}
    w = 1
    for j in range(K):
        table[w] = j
        w = w * z % p
    assert len(table) == K
    e = (p - 1) // K
    return [table[pow(q, e, p)] for q in small_primes]


def is_res(n, p):
    return pow(n, (p - 1) // K, p) == 1


def r_brute(p, cap=None):
    prev = True  # 1 is a residue
    n = 1
    while True:
        nx = is_res(n + 1, p)
        if prev and nx:
            return n
        prev = nx
        n += 1
        if cap and n > cap:
            return None


primes = []
ranges = [(L + 2, 10 ** 7, 500), (10 ** 7, 10 ** 9, 500), (10 ** 9, 10 ** 12, 500),
          (10 ** 12, 10 ** 18, 300), (10 ** 30, 10 ** 40, 200)]
for lo, hi, cnt in ranges:
    for _ in range(cnt):
        primes.append(('random', rand_prime(lo, hi)))
if extra:
    for ln in open(extra):
        if ln.strip():
            p = int(ln.split()[0])
            if p % K == 1 and p > L + 1:
                primes.append(('scan', p))
# deduplicate
seen = set(); P = []
for tag, p in primes:
    if p not in seen:
        seen.add(p); P.append((tag, p))

t0 = time.time()
vecs = []
s2 = set(int(x) for x in S2s.split(','))
bad_r2 = 0
for i, (tag, p) in enumerate(P):
    v = assignment(p)
    if v[0] not in s2:
        bad_r2 += 1
    vecs.append(v)
wf = os.path.join(work, f'walk_k{K}.txt')
of = os.path.join(work, f'walk_k{K}.out')
with open(wf, 'w') as f:
    for i, v in enumerate(vecs):
        f.write(f"{i} " + ' '.join(map(str, v)) + '\n')
with open(raw, 'rb') as fin:
    pr = subprocess.run(['nice', '-n', '10', ccheck, str(K), str(L), S2s, wf, of], stdin=fin,
                        capture_output=True, text=True)
print(pr.stdout.strip())
got = {}
for ln in open(of):
    i, d, n = map(int, ln.split())
    got.setdefault(i, []).append((d, n))
fails = []
stats = {'tests': len(P), 'R2_not_in_S2': bad_r2, 'leaf_eq_r': 0, 'leaf_gt_r': 0,
         'max_depth': 0, 'max_leaf_n': 0, 'max_r': 0}
depth_hist = {}
for i, (tag, p) in enumerate(P):
    g = got.get(i)
    if not g or len(g) != 1:
        fails.append((p, 'walk produced', g)); continue
    d, n = g[0]
    if n < 1:
        fails.append((p, 'walk ended at U or short vector', g)); continue
    if not (n <= L and is_res(n, p) and is_res(n + 1, p)):
        fails.append((p, 'leaf pair is not a residue pair', n)); continue
    r = r_brute(p, cap=n)
    if r is None or r > n:
        fails.append((p, 'r > leaf n ?!', n)); continue
    stats['leaf_eq_r' if r == n else 'leaf_gt_r'] += 1
    stats['max_depth'] = max(stats['max_depth'], d)
    stats['max_leaf_n'] = max(stats['max_leaf_n'], n)
    if r > stats['max_r']:
        stats['max_r'] = r; stats['max_r_p'] = p
    depth_hist[d] = depth_hist.get(d, 0) + 1
stats['depth_hist'] = dict(sorted(depth_hist.items()))
stats['fails'] = fails[:20]
stats['n_fails'] = len(fails)
stats['seconds'] = round(time.time() - t0, 1)
print(json.dumps(stats))
os.remove(wf); os.remove(of)
