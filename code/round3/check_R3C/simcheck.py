#!/usr/bin/env python3
"""simcheck.py -- check of track R3C (round 3, 2026-10-13): how much code does program D
(code/round3/R3C/covfast.c) share with programs A (fibcov.c), B (fibcov2.c) and C (covchk.c)?

Three measures, each reported for every pair of sources (the round-2 pairs A-B, A-C, B-C serve as
baselines: A and B have one author; C was accepted in round 2 as independent of A and B):
  (1) exact lines: whitespace-normalised, comments removed, lines of >= 20 characters that occur
      verbatim in both files (this is the measure used in the R3C report, section 4.2);
  (2) renamed lines: the same, after every identifier that is not a C keyword or a standard library
      name is replaced by 'ID' and every integer literal by 'NUM' (catches copies with renamed
      variables); only lines with >= 8 tokens are counted;
  (3) token 10-grams: fraction of the 10-grams of the identifier-normalised token stream of file X
      that also occur in file Y (containment), and the number of maximal shared runs of >= 25 tokens.
usage: python3 simcheck.py   (paths are relative to the repository root)
"""
import itertools
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FILES = {
    'A': 'code/round2/R3/src/fibcov.c',
    'B': 'code/round2/R3/src/fibcov2.c',
    'C': 'code/round2/review/computation/covchk.c',
    'D': 'code/round3/R3C/covfast.c',
}
KEEP = set('''auto break case char const continue default do double else enum extern float for goto if
inline int long register restrict return short signed sizeof static struct switch typedef union unsigned
void volatile while uint64_t u64 u128 size_t __int128 int64_t uint32_t
malloc calloc realloc free memset memcpy printf fprintf stderr stdout fflush exit strtoull atoi atol
strcmp getenv fopen fclose fscanf clock_gettime timespec CLOCK_MONOTONIC aligned_alloc
__builtin_popcountll __builtin_ctzll tv_sec tv_nsec main argc argv
mpz_t mpz_init mpz_inits mpz_clear mpz_clears mpz_set mpz_set_ui mpz_mul mpz_mul_ui mpz_add_ui
mpz_sub_ui mpz_mod mpz_remove mpz_get_ui mpz_ui_pow_ui mpz_fdiv_q_ui mpz_sgn mpz_init_set
mpz_init_set_ui UINT64_MAX NULL'''.split())
TOK = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|0[xX][0-9a-fA-F]+[uUlL]*|\d+[uUlL]*|'
                 r'<<=|>>=|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^!~<>=]=?|[()\[\]{};,.?:#]')


def strip_comments(s):
    s = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), s, flags=re.S)
    return re.sub(r'//[^\n]*', '', s)


def lines_of(src):
    out = []
    for ln in strip_comments(src).split('\n'):
        ln = ' '.join(ln.split())
        if ln and not ln.startswith('#'):
            out.append(ln)
    return out


def norm_tokens(text):
    out = []
    for t in TOK.findall(text):
        if re.match(r'[A-Za-z_]', t):
            out.append(t if t in KEEP else 'ID')
        elif re.match(r'\d|0[xX]', t):
            out.append('NUM')
        else:
            out.append(t)
    return out


def main():
    src = {k: open(os.path.join(ROOT, v)).read() for k, v in FILES.items()}
    L = {k: lines_of(v) for k, v in src.items()}
    print("# simcheck.py: code overlap between programs A, B, C, D (comments and preprocessor lines removed)")
    for k, v in FILES.items():
        print(f"#   {k} = {v}: {len(L[k])} non-empty code lines")
    print()
    print("pair | exact lines >=20 chars | renamed lines >=8 tokens | 10-gram containment X in Y, Y in X | shared runs >=25 tokens")
    details = {}
    for x, y in itertools.combinations('ABCD', 2):
        ex = sorted({l for l in L[x] if len(l) >= 20} & {l for l in L[y] if len(l) >= 20})
        nx = {}
        for l in L[x]:
            t = norm_tokens(l)
            if len(t) >= 8:
                nx.setdefault(' '.join(t), l)
        ny = {}
        for l in L[y]:
            t = norm_tokens(l)
            if len(t) >= 8:
                ny.setdefault(' '.join(t), l)
        rn = sorted(set(nx) & set(ny))
        tx = norm_tokens('\n'.join(L[x]))
        ty = norm_tokens('\n'.join(L[y]))
        g = 10
        gx = {tuple(tx[i:i + g]) for i in range(len(tx) - g + 1)}
        gy = {tuple(ty[i:i + g]) for i in range(len(ty) - g + 1)}
        cxy = len(gx & gy) / max(1, len(gx))
        cyx = len(gx & gy) / max(1, len(gy))
        # maximal shared runs of >= 25 tokens (greedy over x)
        R = 25
        gyR = {}
        for i in range(len(ty) - R + 1):
            gyR.setdefault(tuple(ty[i:i + R]), i)
        runs = []
        i = 0
        while i <= len(tx) - R:
            key = tuple(tx[i:i + R])
            if key in gyR:
                j = gyR[key]
                n = R
                while i + n < len(tx) and j + n < len(ty) and tx[i + n] == ty[j + n]:
                    n += 1
                runs.append((i, j, n))
                i += n
            else:
                i += 1
        print(f"{x}-{y} | {len(ex)} | {len(rn)} | {cxy:.3f}, {cyx:.3f} | {len(runs)} (longest {max([r[2] for r in runs], default=0)} tokens)")
        details[(x, y)] = (ex, [(nx[k], ny[k]) for k in rn], runs, tx, ty)
    for pair in [('A', 'D'), ('C', 'D'), ('B', 'D'), ('A', 'C')]:
        ex, rn, runs, tx, ty = details[pair]
        x, y = pair
        print(f"\n## {x}-{y}: renamed-line matches ({len(rn)})")
        for a, b in rn:
            print(f"  {x}: {a}\n  {y}: {b}")
        print(f"## {x}-{y}: shared token runs of >= 25 tokens ({len(runs)}), as normalised text of {x}")
        for i, j, n in runs:
            print(f"  [{n} tokens] " + ' '.join(tx[i:i + n]))


if __name__ == '__main__':
    sys.exit(main())
