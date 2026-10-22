#!/usr/bin/env python3
"""check_cert.py -- stand-alone checker for "pairtree-cert 1" certificates (FORMAT.md).

Usage:  python3 -I check_cert.py CERT[.xz|.gz]

Python standard library only.  Written against FORMAT.md, sharing no code with the
generator.  On success it prints the combinatorial statement proved and exits 0;
on any defect it prints the reason and exits 1.  A certificate containing "U"
(unresolved) leaves is parsed completely and reported, but is NOT a proof (exit 2).
"""
import sys, lzma, gzip, hashlib
from math import isqrt


def fail(msg, lineno=None):
    print("REJECTED" + (f" (line {lineno})" if lineno else "") + ": " + msg)
    sys.exit(1)


def open_text(path):
    if path.endswith('.xz'):
        return lzma.open(path, 'rb')
    if path.endswith('.gz'):
        return gzip.open(path, 'rb')
    return open(path, 'rb')


def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    f = open_text(sys.argv[1])
    sha = hashlib.sha256()
    lineno = 0

    def nextline():
        nonlocal lineno
        b = f.readline()
        lineno += 1
        sha.update(b)
        if not b:
            return None
        if not b.endswith(b'\n'):
            fail("line not terminated by LF", lineno)
        try:
            return b[:-1].decode('ascii')
        except UnicodeDecodeError:
            fail("non-ASCII byte", lineno)

    # ---- header -------------------------------------------------------------
    if nextline() != "pairtree-cert 1":
        fail("bad magic line", lineno)
    t = (nextline() or "").split(' ')
    if len(t) != 2 or t[0] != 'k' or not t[1].isdigit() or str(int(t[1])) != t[1]:
        fail("bad k line", lineno)
    k = int(t[1])
    if not 2 <= k <= 64:
        fail("k out of range", lineno)
    t = (nextline() or "").split(' ')
    if len(t) != 2 or t[0] != 'L' or not t[1].isdigit() or str(int(t[1])) != t[1]:
        fail("bad L line", lineno)
    L = int(t[1])
    if L < 1:
        fail("L < 1", lineno)
    t = (nextline() or "").split(' ')
    if t[0] != 'R2' or len(t) < 2:
        fail("bad R2 line", lineno)
    S2 = []
    for s in t[1:]:
        if not s.isdigit() or str(int(s)) != s:
            fail("bad R2 value", lineno)
        v = int(s)
        if not 0 <= v < k or (S2 and v <= S2[-1]):
            fail("R2 values must be strictly increasing and in [0, k)", lineno)
        S2.append(v)
    if nextline() != "begin":
        fail("expected 'begin'", lineno)

    # ---- primes up to L+1 and smallest-prime-factor table ---------------------
    N = L + 1
    spf = list(range(N + 1))
    for i in range(2, isqrt(N) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    primes = [p for p in range(2, N + 1) if spf[p] == p]
    index = {p: i for i, p in enumerate(primes)}
    ALL = list(range(k))

    def values(d):              # children values of a B node at depth d, in order
        return S2 if d == 0 else ALL

    def residue_sum(m, depth, R, ln):
        s = 0
        while m > 1:
            q = spf[m]; e = 0
            while m % q == 0:
                m //= q; e += 1
            i = index[q]
            if i >= depth:
                fail(f"leaf uses prime {q}, which is not assigned at depth {depth}", ln)
            s += e * R[i]
        return s % k

    # ---- the tree, in preorder ------------------------------------------------
    R = [0] * len(primes)       # R[i] = value currently assigned to primes[i]
    stack = []                  # open B nodes: [depth, position of the current child]
    depth = 0                   # depth of the node described by the next line
    nB = nL = nU = 0
    maxn = 0
    leaf_by_depth = {}
    while True:
        line = nextline()
        if line is None:
            fail("unexpected end of file inside the tree", lineno)
        if line == 'B':
            if depth >= len(primes):
                fail(f"B at depth {depth}: there is no prime p_{depth} <= L+1", lineno)
            nB += 1
            stack.append([depth, 0])
            R[depth] = values(depth)[0]
            depth += 1
            continue
        if line == 'U':
            nU += 1
        elif line.startswith('L '):
            s = line[2:]
            if not s.isdigit() or s[0] == '0':
                fail("bad leaf line", lineno)
            n = int(s)
            if n > L:
                fail(f"leaf pair n={n} exceeds L={L}", lineno)
            if residue_sum(n, depth, R, lineno) != 0 or residue_sum(n + 1, depth, R, lineno) != 0:
                fail(f"leaf pair ({n},{n + 1}) is not a pair of residues under the path assignment", lineno)
            nL += 1
            if n > maxn:
                maxn = n
            leaf_by_depth[depth] = leaf_by_depth.get(depth, 0) + 1
        else:
            fail(f"unrecognised node line {line!r}", lineno)
        # a leaf has been read: move to the next sibling of the deepest unfinished B node
        while stack:
            top = stack[-1]
            vals = values(top[0])
            if top[1] + 1 < len(vals):
                top[1] += 1
                R[top[0]] = vals[top[1]]
                depth = top[0] + 1
                break
            stack.pop()
        if not stack:
            break
    if nextline() != 'end':
        fail("expected 'end' after the last node", lineno)
    if f.read(1):
        fail("data after 'end'", lineno)

    print(f"parsed: k={k} L={L} R2={S2}  B={nB} L-leaves={nL} U-leaves={nU} total={nB + nL + nU}")
    print(f"SHA-256 of the decompressed stream: {sha.hexdigest()}")
    print("leaves per depth: " + " ".join(f"{d}:{c}" for d, c in sorted(leaf_by_depth.items())))
    if nU:
        print(f"NOT A PROOF: {nU} unresolved leaves")
        sys.exit(2)
    print(f"VERIFIED: every map R from the primes <= {L + 1} to Z/{k} with R(2) in {set(S2)} admits "
          f"1 <= n <= {L} with f_R(n) = f_R(n+1) = 0 mod {k}; largest leaf n = {maxn}")


if __name__ == '__main__':
    main()
