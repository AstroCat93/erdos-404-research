#!/usr/bin/env python3
"""Tamper tests: apply one mutation at a time to a raw certificate stream, run
both independent checkers on the mutated stream, record the verdicts.

Usage: tamper.py RAW_CERT K L S2 WORKDIR PCHECK CCHECK [--only NAME,...]
A mutation "passes" (the checker behaves correctly) when both checkers REJECT it.
If a mutation is accepted the script says so loudly; the caller must then
explain why the mutated stream is still a genuinely valid certificate.
"""
import sys, os, random, subprocess, time, json

raw, K, L, S2s, work, pcheck, ccheck = sys.argv[1:8]
K = int(K); L = int(L)
only = None
if '--only' in sys.argv:
    only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
S2 = [int(x) for x in S2s.split(',')]
rng = random.Random(20261015)

data = open(raw, 'rb').read()
assert data.endswith(b'end\n')
lines = data.split(b'\n')[:-1]          # without the final empty piece
del data
hdr, tree, tail = lines[:5], lines[5:-1], lines[-1]
assert tail == b'end' and hdr[4] == b'begin'
NT = len(tree)
print(f"loaded {NT} node lines", flush=True)


def children_count(depth):
    return len(S2) if depth == 0 else K


# depth of each node and subtree ends are computed lazily for chosen indices
def subtree_end(i):
    """index one past the subtree starting at tree[i] (i must not be the root)"""
    pend = 1
    j = i
    while pend:
        pend -= 1
        if tree[j] == b'B':
            pend += K
        j += 1
    return j


def children_of(i):
    """list of (start, end) for the children of the B at tree index i (non-root)"""
    assert tree[i] == b'B'
    out = []
    j = i + 1
    for _ in range(K):
        e = subtree_end(j)
        out.append((j, e))
        j = e
    return out


def root_children():
    out = []
    j = 1
    for _ in range(len(S2)):
        e = subtree_end(j)
        out.append((j, e))
        j = e
    assert j == NT
    return out


def pick(pred, lo, hi, tries=100000):
    for _ in range(tries):
        i = rng.randrange(lo, hi)
        if pred(i):
            return i
    raise RuntimeError('pick failed')


def is_leaf(i):
    return tree[i].startswith(b'L ')


def leafn(i):
    return int(tree[i][2:])


muts = []   # (name, description, function returning list of lines (full stream))


def M(name, desc):
    def deco(fn):
        muts.append((name, desc, fn))
        return fn
    return deco


def full(t, h=None, e=b'end'):
    return (h or hdr) + t + [e]


@M('leaf_first_plus1', 'first leaf with n>1: n -> n+1')
def _():
    i = next(i for i in range(NT) if is_leaf(i) and leafn(i) > 1)
    t = tree[:]; t[i] = b'L %d' % (leafn(i) + 1)
    return full(t), f"tree line {i}: {tree[i]!r} -> {t[i]!r}"


@M('leaf_mid_other', 'random mid-stream leaf: n -> a different n taken from a random other leaf')
def _():
    i = pick(is_leaf, NT // 3, 2 * NT // 3)
    while True:
        j = pick(is_leaf, 0, NT)
        if leafn(j) != leafn(i):
            break
    t = tree[:]; t[i] = tree[j]
    return full(t), f"tree line {i}: {tree[i]!r} -> {t[i]!r}"


@M('leaf_last_minus1', 'last leaf: n -> n-1')
def _():
    i = max(i for i in range(NT - 50, NT) if is_leaf(i))
    t = tree[:]; t[i] = b'L %d' % (leafn(i) - 1)
    return full(t), f"tree line {i}: {tree[i]!r} -> {t[i]!r}"


@M('leaf_exceeds_L', 'a leaf with n = L -> n = L+1 (violates n <= L)')
def _():
    i = pick(lambda i: tree[i] == b'L %d' % L, 0, NT)
    t = tree[:]; t[i] = b'L %d' % (L + 1)
    return full(t), f"tree line {i}: {tree[i]!r} -> {t[i]!r}"


@M('leaf_unassigned_prime', 'first leaf "L 1" (R(2)=0) -> "L 3": 3 not assigned at depth 1')
def _():
    assert tree[1] == b'L 1'
    t = tree[:]; t[1] = b'L 3'
    return full(t), "tree line 1: 'L 1' -> 'L 3'"


@M('leaf_zero', 'a leaf n -> 0')
def _():
    i = pick(is_leaf, 0, NT)
    t = tree[:]; t[i] = b'L 0'
    return full(t), f"tree line {i}: {tree[i]!r} -> 'L 0'"


@M('drop_leaf_mid', 'delete one leaf line mid-stream (a B loses a child)')
def _():
    i = pick(is_leaf, NT // 3, 2 * NT // 3)
    t = tree[:i] + tree[i + 1:]
    return full(t), f"deleted tree line {i}: {tree[i]!r}"


@M('drop_leaf_last', 'delete the last leaf line')
def _():
    i = NT - 1
    assert is_leaf(i)
    return full(tree[:-1]), f"deleted tree line {i}: {tree[i]!r}"


@M('drop_subtree', 'delete a whole child subtree (a B at depth >= 2 with its descendants)')
def _():
    i = pick(lambda i: tree[i] == b'B' and i > 10, NT // 4, 3 * NT // 4)
    e = subtree_end(i)
    return full(tree[:i] + tree[e:]), f"deleted tree lines {i}..{e - 1} ({e - i} lines, subtree rooted at a B)"


@M('dup_leaf', 'duplicate a leaf line (a B gains a child)')
def _():
    i = pick(is_leaf, NT // 3, 2 * NT // 3)
    return full(tree[:i + 1] + [tree[i]] + tree[i + 1:]), f"duplicated tree line {i}: {tree[i]!r}"


@M('swap_root_children_0_1', 'swap the subtrees of R(2)=0 and R(2)=2')
def _():
    rc = root_children()
    (a0, a1), (b0, b1) = rc[0], rc[1]
    t = [tree[0]] + tree[b0:b1] + tree[a0:a1] + tree[b1:]
    return full(t), f"root children 0 [{a0},{a1}) and 1 [{b0},{b1}) swapped"


@M('swap_root_children_2_3', 'swap the subtrees of R(2)=4 and R(2)=6')
def _():
    rc = root_children()
    (a0, a1), (b0, b1) = rc[2], rc[3]
    t = tree[:a0] + tree[b0:b1] + tree[a0:a1] + tree[b1:]
    return full(t), f"root children 2 [{a0},{a1}) and 3 [{b0},{b1}) swapped"


@M('swap_sibling_leaves', 'at a random B whose children are all leaves with >=2 distinct n, swap two children with different n')
def _():
    def ok(i):
        if tree[i] != b'B':
            return False
        ch = tree[i + 1:i + 1 + K]
        return all(c.startswith(b'L ') for c in ch) and len(set(ch)) >= 2
    i = pick(ok, NT // 3, 2 * NT // 3)
    ch = list(range(i + 1, i + 1 + K))
    a = ch[0]
    b = next(c for c in ch if tree[c] != tree[a])
    t = tree[:]; t[a], t[b] = t[b], t[a]
    return full(t), f"B at tree line {i}: swapped children {a - i - 1} and {b - i - 1} ({tree[a]!r} <-> {tree[b]!r})"


@M('swap_sibling_subtrees', 'at a random non-root B, swap two adjacent child subtrees whose contents differ')
def _():
    while True:
        i = pick(lambda i: tree[i] == b'B' and i > 0, NT // 4, 3 * NT // 4)
        ch = children_of(i)
        cand = [c for c in range(K - 1) if tree[ch[c][0]:ch[c][1]] != tree[ch[c + 1][0]:ch[c + 1][1]]
                and (ch[c][1] - ch[c][0] > 1 or ch[c + 1][1] - ch[c + 1][0] > 1)]
        if cand:
            break
    c = rng.choice(cand)
    (a0, a1), (b0, b1) = ch[c], ch[c + 1]
    t = tree[:a0] + tree[b0:b1] + tree[a0:a1] + tree[b1:]
    return full(t), f"B at tree line {i}: swapped child subtrees {c} [{a0},{a1}) and {c + 1} [{b0},{b1})"


@M('reverse_children', 'at a random non-root B, list its children in value order k-1..0')
def _():
    while True:
        i = pick(lambda i: tree[i] == b'B' and i > 0, NT // 4, 3 * NT // 4)
        ch = children_of(i)
        parts = [tree[a:b] for a, b in ch]
        if parts != parts[::-1]:
            break
    t = tree[:ch[0][0]] + [x for p in reversed(parts) for x in p] + tree[ch[-1][1]:]
    return full(t), f"B at tree line {i}: children reversed"


@M('hdr_R2_order', 'header R2 values out of order (R2 2 0 4 6), tree unchanged')
def _():
    h = hdr[:]; h[3] = b'R2 2 0 4 6'
    return full(tree, h), "R2 line -> 'R2 2 0 4 6'"


@M('hdr_R2_order_consistent', 'header R2 2 0 4 6 AND root subtrees 0,1 swapped to match (semantically equal, syntactically illegal)')
def _():
    rc = root_children()
    (a0, a1), (b0, b1) = rc[0], rc[1]
    t = [tree[0]] + tree[b0:b1] + tree[a0:a1] + tree[b1:]
    h = hdr[:]; h[3] = b'R2 2 0 4 6'
    return full(t, h), "R2 -> 'R2 2 0 4 6' and root children 0,1 swapped"


@M('hdr_R2_drop6', 'weaker statement: R2 0 2 4 and the R(2)=6 subtree removed (valid certificate of C(8,L,{0,2,4}) only)')
def _():
    rc = root_children()
    a0, a1 = rc[3]
    h = hdr[:]; h[3] = b'R2 0 2 4'
    return full(tree[:a0] + tree[a1:], h), f"R2 -> 'R2 0 2 4', deleted [{a0},{a1})"


@M('hdr_L_minus1', 'header L -> L-1, tree unchanged')
def _():
    h = hdr[:]; h[2] = b'L %d' % (L - 1)
    return full(tree, h), f"L line -> 'L {L - 1}'"


@M('hdr_k4', 'header k 8 -> k 4, tree unchanged')
def _():
    h = hdr[:]; h[1] = b'k 4'
    return full(tree, h), "k line -> 'k 4'"


@M('leaf_to_U', 'a random leaf -> U (open case)')
def _():
    i = pick(is_leaf, NT // 3, 2 * NT // 3)
    t = tree[:]; t[i] = b'U'
    return full(t), f"tree line {i}: {tree[i]!r} -> 'U'"


@M('B_to_leaf', 'a random B -> its first leaf child line (structure shifts)')
def _():
    i = pick(lambda i: tree[i] == b'B' and is_leaf(i + 1) and i > 0, NT // 3, 2 * NT // 3)
    t = tree[:]; t[i] = tree[i + 1]
    return full(t), f"tree line {i}: 'B' -> {tree[i + 1]!r}"


@M('truncate_no_end', 'stream ends without the end line')
def _():
    return hdr + tree, "'end' removed"


@M('truncate_mid', 'stream cut after 60% of the node lines (no end)')
def _():
    c = int(NT * 0.6)
    return hdr + tree[:c], f"kept {c} node lines"


@M('trailing_line', 'extra node line after end')
def _():
    return full(tree) + [b'L 1'], "appended 'L 1' after 'end'"


BYTE_MUTS = {
    'no_final_LF': ('final LF removed', lambda b: b[:-1]),
    'trailing_space': ('trailing space on the first leaf line', lambda b: b.replace(b'\nL 1\n', b'\nL 1 \n', 1)),
    'crlf_one_line': ('CR before LF on one mid-stream leaf line', None),
    'leading_zero': ('leading zero on the first leaf line with n>1', None),
    'blank_line': ('an empty line inserted after begin', lambda b: b.replace(b'begin\n', b'begin\n\n', 1)),
    'non_ascii': ('a 0xC2 byte in the magic line', lambda b: b.replace(b'pairtree-cert 1', b'pairtree\xc2cert 1', 1)),
}


def run_checkers(path):
    out = {}
    t = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, '-I', pcheck, path,
                        '--k', str(K), '--L', str(L), '--S2', S2s],
                       capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
        out['py'] = (d['verdict'], '; '.join(d['reject_reasons']), round(time.time() - t, 1))
    except Exception:
        out['py'] = ('CRASH', p.stdout[-300:] + p.stderr[-300:], round(time.time() - t, 1))
    t = time.time()
    with open(path, 'rb') as f:
        p = subprocess.run(['nice', '-n', '10', ccheck, str(K), str(L), S2s], stdin=f,
                           capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]
    out['c'] = ('PROOF' if p.returncode == 0 else 'REJECT', last, round(time.time() - t, 1))
    return out


results = []
fn_path = os.path.join(work, 'tampered.raw')
todo = [(n, d, f, None) for n, d, f in muts] + [(n, d, None, g) for n, (d, g) in BYTE_MUTS.items()]
for name, desc, f, g in todo:
    if only and name not in only:
        continue
    if f is not None:
        ls, detail = f()
        blob = b'\n'.join(ls) + b'\n'
    else:
        blob = b'\n'.join(full(tree)) + b'\n'
        if name == 'crlf_one_line':
            i = pick(is_leaf, NT // 3, 2 * NT // 3)
            # rebuild with a CR on that line
            t = tree[:]; t[i] = tree[i] + b'\r'
            blob = b'\n'.join(full(t)) + b'\n'
            detail = f"tree line {i}: {tree[i]!r} -> {t[i]!r}"
        elif name == 'leading_zero':
            i = next(i for i in range(NT) if is_leaf(i) and leafn(i) > 1)
            t = tree[:]; t[i] = b'L 0' + tree[i][2:]
            blob = b'\n'.join(full(t)) + b'\n'
            detail = f"tree line {i}: {tree[i]!r} -> {t[i]!r}"
        else:
            blob = g(blob)
            detail = desc
    with open(fn_path, 'wb') as fo:
        fo.write(blob)
    del blob
    r = run_checkers(fn_path)
    os.remove(fn_path)
    both_reject = r['py'][0] == 'REJECT' and r['c'][0] == 'REJECT'
    rec = {'mutation': name, 'description': desc, 'detail': detail,
           'python': r['py'], 'c': r['c'], 'both_reject': both_reject}
    results.append(rec)
    print(json.dumps(rec), flush=True)
    if not both_reject:
        print(f"!!! MUTATION {name} ACCEPTED by at least one checker", flush=True)

print(f"SUMMARY: {sum(r['both_reject'] for r in results)}/{len(results)} mutations rejected by both checkers", flush=True)
