#!/usr/bin/env python3
"""Exhaustive single-edit differential test on the small certificates.

For every single-line edit of the k=2, 3, 4 certificates (and a random sample for
k=5), three checkers judge the mutated stream:
  py    - pcheck.check (sieve factorisation, stack walk)
  c     - ccheck (trial division by assigned primes, counter walk)
  naive - a deliberately simple recursive-descent checker defined below
          (factorises n, n+1 by trial division over all integers).
All three must agree.  For k = 2 every accepted mutant is additionally checked
semantically: all 2^4 assignments are walked through the mutant tree and the
leaf reached must close a pair (n, n+1) with n <= 9 under that assignment.
Usage: diff_small.py CERTDIR PCHECK_DIR CCHECK WORKDIR
"""
import sys, os, lzma, random, subprocess, itertools, json, time

certdir, pdir, ccheck, work = sys.argv[1:5]
sys.path.insert(0, pdir)
import pcheck  # noqa: E402


def naive_check(text, k, L, S2):
    """returns 'PROOF' or 'REJECT'.  Independent, simple, recursive."""
    try:
        if not text.endswith('\n') or '\r' in text:
            return 'REJECT'
        ls = text[:-1].split('\n')
        if ls[:1] != ['pairtree-cert 1'] or ls[1] != f'k {k}' or ls[2] != f'L {L}' \
                or ls[3] != 'R2 ' + ' '.join(map(str, S2)) or ls[4] != 'begin' or ls[-1] != 'end':
            return 'REJECT'
        body = ls[5:-1]
        primes = [q for q in range(2, L + 2) if all(q % r for r in range(2, int(q ** 0.5) + 1))]
        pos = [0]
        state = {'U': 0}

        def fac(m):
            out = {}
            q = 2
            while m > 1:
                while m % q == 0:
                    out[q] = out.get(q, 0) + 1; m //= q
                q += 1
            return out

        def node(depth, R):
            if pos[0] >= len(body):
                raise ValueError('eof')
            ln = body[pos[0]]; pos[0] += 1
            if ln == 'B':
                if depth >= len(primes):
                    raise ValueError('deep')
                vals = S2 if depth == 0 else range(k)
                for v in vals:
                    node(depth + 1, R + [v])
            elif ln == 'U':
                state['U'] += 1
            elif ln.startswith('L ') and ln[2:].isdigit() and ln[2:] == str(int(ln[2:])):
                n = int(ln[2:])
                if not 1 <= n <= L:
                    raise ValueError('range')
                assigned = {primes[i]: R[i] for i in range(depth)}
                for m in (n, n + 1):
                    f = fac(m)
                    if any(q not in assigned for q in f):
                        raise ValueError('unassigned')
                    if sum(e * assigned[q] for q, e in f.items()) % k:
                        raise ValueError('sum')
            else:
                raise ValueError('syntax')
        node(0, [])
        if pos[0] != len(body) or state['U']:
            return 'REJECT'
        return 'PROOF'
    except (ValueError, IndexError, RecursionError):
        return 'REJECT'


def semantic_k2(text):
    """k=2, L=9: walk all 16 assignments of primes 2,3,5,7 through the tree."""
    body = text[:-1].split('\n')[5:-1]
    # build tree
    pos = [0]

    def build():
        ln = body[pos[0]]; pos[0] += 1
        if ln == 'B':
            return [build() for _ in range(2)]
        return ln
    tree = build()
    primes = [2, 3, 5, 7]
    for R in itertools.product(range(2), repeat=4):
        t = tree; d = 0
        while isinstance(t, list):
            t = t[R[d]]; d += 1
        n = int(t[2:])
        def f(m):
            s = 0
            for i, q in enumerate(primes):
                while m % q == 0:
                    m //= q; s += R[i]
            return s % 2 if m == 1 else None
        if not (n <= 9 and f(n) == 0 and f(n + 1) == 0):
            return False
    return True


def mutants(ls, k, L, rng=None, sample=None):
    """single-line edits of the node lines (ls = full list of lines).
    Descriptors are enumerated first and only the (sampled) ones are materialised."""
    desc = []
    lo, hi = 5, len(ls) - 1
    for i in range(lo, hi):
        desc.append(('del', i, None))
        desc.append(('dup', i, None))
        if i + 1 < hi and ls[i] != ls[i + 1]:
            desc.append(('swap', i, None))
        for rep in ('B', 'U', 'L 1'):
            if ls[i] != rep:
                desc.append(('to_' + rep.replace(' ', ''), i, rep))
        if ls[i].startswith('L '):
            n = int(ls[i][2:])
            for nn, tag in ((n + 1, 'n+1'), (n - 1, 'n-1'), (0, 'n=0'), (L + 1, 'n=L+1'), (L, 'n=L')):
                if nn != n:
                    desc.append((tag, i, f'L {nn}'))
    if sample and len(desc) > sample:
        desc = rng.sample(desc, sample)
    for tag, i, rep in desc:
        if tag == 'del':
            yield tag, i, ls[:i] + ls[i + 1:]
        elif tag == 'dup':
            yield tag, i, ls[:i + 1] + [ls[i]] + ls[i + 1:]
        elif tag == 'swap':
            t = ls[:]; t[i], t[i + 1] = t[i + 1], t[i]; yield tag, i, t
        else:
            t = ls[:]; t[i] = rep; yield tag, i, t


rng = random.Random(5)
report = {}
for k, L, S2, sample in ((2, 9, [0, 1], None), (3, 77, [0, 1, 2], None), (4, 1224, [0, 1, 2, 3], None),
                         (5, 7888, [0, 1, 2, 3, 4], 1000)):
    t0 = time.time()
    text = lzma.open(os.path.join(certdir, f'k{k}_L{L}.cert.xz'), 'rt').read()
    ls = text[:-1].split('\n')
    S2s = ','.join(map(str, S2))
    muts = list(mutants(ls, k, L, rng, sample)) if k <= 4 else mutants(ls, k, L, rng, sample)
    nm = 0
    agree = disagree = accepted = sem_ok = 0
    examples_acc = []
    path = os.path.join(work, f'small_mut_k{k}.cert')
    import itertools as _it
    for tag, i, t in _it.chain([('orig', -1, ls)], muts):
        nm += tag != 'orig'
        s = '\n'.join(t) + '\n'
        with open(path, 'w') as f:
            f.write(s)
        vp = pcheck.check(path, k, L, S2, quiet=True)['verdict']
        with open(path, 'rb') as f:
            vc = 'PROOF' if subprocess.run([ccheck, str(k), str(L), S2s], stdin=f,
                                           capture_output=True).returncode == 0 else 'REJECT'
        vn = naive_check(s, k, L, S2) if k <= 4 else None
        vs = [vp, vc] + ([vn] if vn else [])
        if len(set(vs)) == 1:
            agree += 1
        else:
            disagree += 1
            print('DISAGREE', k, tag, i, vs, flush=True)
        if tag != 'orig' and vp == 'PROOF':
            accepted += 1
            if len(examples_acc) < 5:
                examples_acc.append((tag, i, ls[i] if i < len(ls) else None))
            if k == 2:
                sem_ok += semantic_k2(s)
    os.remove(path)
    report[k] = {'mutants': nm, 'agree': agree, 'disagree': disagree,
                 'mutants_accepted': accepted, 'accepted_examples': examples_acc,
                 'k2_semantic_ok_of_accepted': sem_ok if k == 2 else None,
                 'seconds': round(time.time() - t0, 1)}
    print(k, json.dumps(report[k]), flush=True)
print(json.dumps(report))
