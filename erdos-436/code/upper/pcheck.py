#!/usr/bin/env python3
"""Independent checker for 'pairtree-cert 1' certificates.

Written from certificate/FORMAT.md only (the generator's and the bundled
checker's source were not read).  Standard library only.

Usage:
  pcheck.py CERT [--k K] [--L L] [--S2 v,v,...] [--sha256 HEX]
CERT may be raw, .xz or .gz, or '-' for a raw stream on stdin.

The optional --k/--L/--S2 give the TARGET statement C(k, L, S2).  The verdict
is PROOF only if the stream is a valid tree with no U leaves AND its header
parameters equal the target (S2 of the certificate must contain the target S2;
equality is required here to be strict).  --sha256 compares the SHA-256 of the
decompressed stream.

Leaf conditions (FORMAT.md section 4) are checked by factoring n and n+1 with a
smallest-prime-factor sieve up to L+1; nothing from the certificate other than
the node lines is trusted.
Exit status: 0 = PROOF of target (and hash matches if given), 1 otherwise.
"""
import sys, lzma, gzip, hashlib, time, argparse, json, resource
from array import array


class Invalid(Exception):
    pass


def canon_int(tok, what):
    # decimal, no sign, no leading zeros; zero is "0"
    if not tok or not tok.isdigit():
        raise Invalid(f"{what}: not a canonical decimal: {tok[:40]!r}")
    if len(tok) > 1 and tok[0] == 0x30:
        raise Invalid(f"{what}: leading zero: {tok[:40]!r}")
    return int(tok)


def open_stream(path):
    if path == '-':
        return sys.stdin.buffer
    with open(path, 'rb') as f:
        magic = f.read(6)
    if magic.startswith(b'\xfd7zXZ\x00'):
        return lzma.open(path, 'rb')
    if magic.startswith(b'\x1f\x8b'):
        return gzip.open(path, 'rb')
    return open(path, 'rb')


def line_iter(f, h, stats):
    """Yield the lines (without LF) of the decompressed stream.  Updates the
    SHA-256 h with every byte, enforces 7-bit ASCII and a final LF."""
    rem = b''
    while True:
        chunk = f.read(1 << 24)
        if not chunk:
            break
        h.update(chunk)
        stats['bytes'] += len(chunk)
        if not chunk.isascii():
            raise Invalid("non-ASCII byte in stream")
        parts = (rem + chunk).split(b'\n')
        rem = parts.pop()
        yield from parts
    if rem:
        raise Invalid("stream does not end with LF (or trailing bytes after last LF)")


def sieve_spf(N):
    """smallest prime factor for 0..N (spf[0]=spf[1]=0) and the primes <= N."""
    spf = array('i', [0]) * (N + 1)
    r = int(N ** 0.5)
    while r * r > N:
        r -= 1
    while (r + 1) * (r + 1) <= N:
        r += 1
    # mark composites: assign from largest p down so the smallest prime wins
    small = bytearray([1]) * (r + 1)
    small[0:2] = b'\x00\x00'
    for i in range(2, int(r ** 0.5) + 1):
        if small[i]:
            small[i * i::i] = bytearray(len(range(i * i, r + 1, i)))
    sp = [i for i in range(2, r + 1) if small[i]]
    for p in reversed(sp):
        cnt = len(range(p * p, N + 1, p))
        spf[p * p::p] = array('i', [p]) * cnt
    primes = []
    for m in range(2, N + 1):
        if spf[m] == 0:
            spf[m] = m
            primes.append(m)
    return spf, primes


def check(path, tk=None, tL=None, tS2=None, tsha=None, quiet=False):
    t0 = time.time()
    stats = {'bytes': 0}
    h = hashlib.sha256()
    f = open_stream(path)
    it = line_iter(f, h, stats)
    res = {'file': path}
    try:
        def nxt(what):
            try:
                return next(it)
            except StopIteration:
                raise Invalid(f"unexpected end of stream while reading {what}")

        if nxt('magic') != b'pairtree-cert 1':
            raise Invalid("bad magic line")
        l2 = nxt('k line')
        if l2[:2] != b'k ':
            raise Invalid("bad k line")
        k = canon_int(l2[2:], 'k')
        if k < 2:
            raise Invalid("k < 2")
        l3 = nxt('L line')
        if l3[:2] != b'L ':
            raise Invalid("bad L line")
        L = canon_int(l3[2:], 'L')
        if L < 1:
            raise Invalid("L < 1")
        toks = nxt('R2 line').split(b' ')
        if toks[0] != b'R2' or len(toks) < 2:
            raise Invalid("bad R2 line")
        S2 = [canon_int(t, 'R2 value') for t in toks[1:]]
        for a, b in zip(S2, S2[1:]):
            if not a < b:
                raise Invalid("R2 values not strictly increasing")
        if S2[0] < 0 or S2[-1] > k - 1:
            raise Invalid("R2 value out of range")
        if nxt('begin') != b'begin':
            raise Invalid("missing begin")
        res.update(k=k, L=L, S2=S2)

        spf, primes = sieve_spf(L + 1)
        M = len(primes)
        pidx = array('i', [-1]) * (L + 2)
        for i, p in enumerate(primes):
            pidx[p] = i
        res['M'] = M
        t_sieve = time.time() - t0

        def factor(m):
            out = []
            while m > 1:
                p = spf[m]
                e = 0
                while m % p == 0:
                    m //= p
                    e += 1
                out.append((pidx[p], e))
            return tuple(out)

        cache = {}
        ALL = list(range(k))
        R = [None] * (M + 1)
        st_d = []   # depth of each open B node
        st_j = []   # index of the child currently being read
        depth = 0
        nB = nL = nU = 0
        maxdepth = 0
        maxn = 0
        maxn_cnt = 0
        leaf_depth_hist = {}
        root_done = False
        lineno = 5
        for line in it:
            lineno += 1
            if line == b'B':
                if depth >= M:
                    raise Invalid(f"line {lineno}: B at depth {depth} >= M = {M}")
                nB += 1
                v0 = S2[0] if depth == 0 else 0
                R[depth] = v0
                st_d.append(depth)
                st_j.append(0)
                depth += 1
                if depth > maxdepth:
                    maxdepth = depth
                continue
            if line == b'U':
                nU += 1
            elif line[:2] == b'L ':
                n = canon_int(line[2:], f"line {lineno}: leaf")
                if n < 1 or n > L:
                    raise Invalid(f"line {lineno}: leaf n = {n} outside [1, L]")
                info = cache.get(n)
                if info is None:
                    fa = factor(n)
                    fb = factor(n + 1)
                    mx = max(i for i, _ in fa + fb)
                    info = (mx, fa, fb)
                    cache[n] = info
                mx, fa, fb = info
                if mx >= depth:
                    raise Invalid(f"line {lineno}: leaf n = {n} at depth {depth}: "
                                  f"prime {primes[mx]} of n(n+1) is not assigned")
                s = 0
                for i, e in fa:
                    s += e * R[i]
                if s % k:
                    raise Invalid(f"line {lineno}: leaf n = {n} at depth {depth}: f(n) = {s % k} != 0")
                s = 0
                for i, e in fb:
                    s += e * R[i]
                if s % k:
                    raise Invalid(f"line {lineno}: leaf n = {n} at depth {depth}: f(n+1) = {s % k} != 0")
                nL += 1
                leaf_depth_hist[depth] = leaf_depth_hist.get(depth, 0) + 1
                if n > maxn:
                    maxn, maxn_cnt = n, 1
                elif n == maxn:
                    maxn_cnt += 1
            else:
                raise Invalid(f"line {lineno}: unrecognised node line {line[:40]!r}")
            # leaf done: move to next sibling of the deepest unfinished B
            while st_d:
                d = st_d[-1]
                j = st_j[-1] + 1
                vals = S2 if d == 0 else ALL
                if j < len(vals):
                    st_j[-1] = j
                    R[d] = vals[j]
                    depth = d + 1
                    break
                st_d.pop()
                st_j.pop()
            if not st_d:
                root_done = True
                break
        if not root_done:
            raise Invalid(f"stream ended with {len(st_d)} unfinished B nodes")
        lineno += 1
        if nxt('end') != b'end':
            raise Invalid(f"line {lineno}: expected 'end' after the root's listing")
        for extra in it:
            raise Invalid(f"line {lineno + 1}: data after 'end'")
        res.update(valid=True, B=nB, L_leaves=nL, U=nU, nodes=nB + nL + nU,
                   max_depth=maxdepth, max_leaf_n=maxn, max_leaf_n_count=maxn_cnt,
                   distinct_leaf_n=len(cache),
                   leaf_depth_hist={str(a): b for a, b in sorted(leaf_depth_hist.items())},
                   sieve_s=round(t_sieve, 2))
    except Invalid as e:
        # drain to finish the hash only if cheap; record reason
        res.update(valid=False, reason=str(e))
    res['bytes_read'] = stats['bytes']
    res['sha256_decompressed'] = h.hexdigest() if res.get('valid') else None
    res['seconds'] = round(time.time() - t0, 2)
    res['cpu_seconds'] = round(time.process_time(), 2)
    res['max_rss_MB'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
    # verdict
    reasons = []
    if not res.get('valid'):
        reasons.append('INVALID: ' + res['reason'])
    else:
        if res['U']:
            reasons.append(f"partial tree: {res['U']} U leaves (not a proof)")
        if tk is not None and res['k'] != tk:
            reasons.append(f"k = {res['k']} != target {tk}")
        if tL is not None and res['L'] != tL:
            reasons.append(f"L = {res['L']} != target {tL}")
        if tS2 is not None and res['S2'] != tS2:
            reasons.append(f"S2 = {res['S2']} != target {tS2}")
        if tsha is not None and res['sha256_decompressed'] != tsha:
            reasons.append(f"sha256 {res['sha256_decompressed']} != expected {tsha}")
    res['verdict'] = 'PROOF' if not reasons else 'REJECT'
    res['reject_reasons'] = reasons
    if not quiet:
        print(json.dumps(res, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cert')
    ap.add_argument('--k', type=int)
    ap.add_argument('--L', type=int)
    ap.add_argument('--S2')
    ap.add_argument('--sha256')
    a = ap.parse_args()
    s2 = [int(x) for x in a.S2.split(',')] if a.S2 else None
    r = check(a.cert, a.k, a.L, s2, a.sha256)
    sys.exit(0 if r['verdict'] == 'PROOF' else 1)


if __name__ == '__main__':
    main()
