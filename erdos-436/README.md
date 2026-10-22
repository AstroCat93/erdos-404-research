# Λ(8,2) = 1508324: consecutive eighth-power residues (Erdős problem #436)

**Status: preprint, not peer reviewed.** No person has verified the proofs or the code (see
[AI assistance](#ai-assistance) below).

## The result in plain English

Pick a prime *p* and count 1, 2, 3, … until you reach the first two neighbouring numbers *n*,
*n*+1 that are both nonzero 8th powers modulo *p*. Λ(8,2) is the worst case: the furthest you
can be forced to count for infinitely many primes. D. H. and Emma Lehmer, W. H. Mills, M. Dunton
and J. Brillhart found the analogous numbers for squares up to 7th powers in 1962–64. For 8th
powers only bounds were known. Don Reble reported 1499876 ≤ Λ(8,2) ≤ 1508324 in 2019, and Fabian
Arevalo published a checkable proof of the upper bound in September 2026. This repository adds an explicit
pattern of power characters that attains 1508324. A classical theorem of Mills (1963) shows that
infinitely many primes follow this pattern, so **Λ(8,2) = 1508324**. This is the term a(8) of
OEIS [A000445](https://oeis.org/A000445), which continues 9, 77, 1224, 7888, 202124, 1649375. The
proof is computer-assisted.

## Exact statement

For a prime *p* let r(k,2,p) be the least *n* ≥ 1 such that *p* ∤ *n*(*n*+1) and *n*, *n*+1 are
both *k*-th power residues modulo *p* (∞ if there is none), and let
Λ(k,2) = limsup_{p→∞} r(k,2,p) (Lehmer–Lehmer, 1962).

**Theorem.** Λ(8,2) = 1508324. More precisely:

* **(a)** every prime *p* ∉ {2, 3, 5, 13, 17, 41, 113} has r(8,2,p) ≤ 1508324, and those seven
  primes have no pair at all;
* **(b)** the primes *p* ≡ 1 (mod 8) with r(8,2,p) = 1508324 include a set of positive
  Dirichlet density.

So the maximum over non-exceptional primes, which is the convention of Brillhart–Lehmer–Lehmer
and of OEIS A000445, is also 1508324. The proof is in [`paper/note.pdf`](paper/note.pdf)
(source [`paper/note.md`](paper/note.md), LaTeX export [`paper/note.tex`](paper/note.tex)).

The pattern behind (b) is the exponent vector R\* with R\*(q) = 1 for every prime *q* except 74:

* R\* = 0 at 3, 97, 149, 163;
* R\* = 3 at 233, 271, 443, 641, 1297;
* R\* = 2 at the 65 primes listed in [`vectors/vec8_compact.txt`](vectors/vec8_compact.txt),
  including *q* = 2.

The least *n* with f(n) = f(n+1) = 0 (mod 8), where f(n) = Σ v_q(n) R\*(q), is
1508324 = 2²·47·71·113, with 1508325 = 3·5²·7·13²·17.

## What is new and what is not

| Part | Due to |
|---|---|
| The definition of Λ(k,l) and Λ(2,2) = 9 | D. H. Lehmer and E. Lehmer (1962) |
| Λ(3,2) = 77 | M. Dunton (published 1965) |
| Λ(4,2) = 1224 | W. H. Mills; published by R. G. Bierstedt and W. H. Mills (1963) |
| Λ(5,2) = 7888 and Λ(6,2) = 202124 | D. H. Lehmer, E. Lehmer and W. H. Mills (1963) |
| Λ(7,2) = 1649375, and Λ(8,2) ≥ 1200744 | J. Brillhart, D. H. Lehmer and E. Lehmer (1964) |
| The case-vector method used here | Lehmer, Lehmer, Mills and Selfridge (1962); Brillhart, Lehmer and Lehmer (1964) |
| Realizability: every pattern with even R(2) is realised by infinitely many primes | W. H. Mills (1963), Theorem 3; the paper includes a proof only to be self-contained |
| The bounds 1499876 ≤ Λ(8,2) ≤ 1508324 (no public description of the method or data found) | Don Reble (reported 2019; recorded in OEIS A000445 by Christopher E. Thompson) |
| The first public, reproducible certificate of that bound | Fabian Arevalo (2 September 2026) |
| The 108 case vectors that Arevalo's tree leaves unsettled, and the proposal to search for full extensions of them | Fabian Arevalo. R\* is a full extension of the eleventh of these vectors |
| **The explicit vector R\* attaining 1508324, and with it the exact value** | **New here** |
| A re-certification of the upper bound in a new, fully specified format, with separately written checkers | New here, but it proves a known bound |
| Λ(9,2) ≥ 146290624 (see below) | Found in this work; no priority claim, because Reble's 2019 post could not be read; far from exact |

The new part is small: one explicit vector, found by computer once Arevalo had published the
unsettled cases and proposed this search. It settles one OEIS term. It does not settle Erdős
problem #436.

## How to verify

Needs bash, gcc, python3 (standard library), xz and sha256sum; numpy is optional. One core,
about 1 GB of memory.

```bash
git clone https://github.com/AstroCat93/erdos-404-research
cd erdos-404-research/erdos-436
./verify.sh                    # about 2 minutes; ends with "ALL CHECKS PASSED"
./verify.sh --extended         # then about 15 more minutes of further tests
bash code/extended/arevalo_check.sh   # optional: downloads and runs Arevalo's code (cross-check)
```

`verify.sh` prints one PASS/FAIL line per check, with its time, and exits 0 only if every check
passed. It checks:

1. **hashes**: every certificate (compressed and decompressed) and vector, and every hash quoted in
   the paper's §8;
2. **(H1) the upper-bound certificates**: the k = 8 certificate and the k = 2, 4 certificates (needed
   for primes p ≢ 1 mod 8) with four checkers, two of them written from
   [`certificate/FORMAT.md`](certificate/FORMAT.md) alone; the k = 3, 5, 6, 7 certificates, which
   reproduce the classical values, with two checkers;
3. **(H3) the small primes** p ≤ 1508325, with two programs;
4. **(H2) the lower-bound vector**: the least zero pair of R\* with five programs (one needs numpy),
   the test that every listed exception except q = 2 is needed, the two full assignments of all
   114765 primes, and the k = 9 vector with three programs;
5. **regeneration**: two programs rebuild all seven certificate streams, whose SHA-256 must match
   (skip with `--no-regen`).

The reference transcripts are [`expected/verify.log`](expected/verify.log),
[`expected/extended.log`](expected/extended.log) and
[`expected/arevalo_check.log`](expected/arevalo_check.log). The longest single steps are the Python checkers on
the k = 8 certificate, about 37 s and 17 s. [`code/README.md`](code/README.md) lists every program,
its origin, and the statement of the paper that it checks.

## A remark on k = 9

Every exponent vector is realisable for k = 9. The vector that equals 1 except at 18 primes
([`vectors/vec9_compact18_146290624.txt`](vectors/vec9_compact18_146290624.txt)) has least zero
pair 146290624 = 2⁶·41·197·283, 146290625 = 5⁵·13²·277. Hence **Λ(9,2) ≥ 146290624**. Brillhart,
Lehmer and Lehmer (1964) gave Λ(9,2) > 10⁷. The vector came from a local search that stalled, so the
bound is surely not sharp. Reble's 2019 post could not be retrieved, so we make no priority claim
for k = 9.

## Repository layout

| Path | Contents |
|---|---|
| [`paper/`](paper/) | the note (`note.md`, `note.pdf`, `note.tex`), its stylesheet and `render.sh` |
| [`certificate/`](certificate/) | the certificates for k = 2, …, 8 (`.xz`), `FORMAT.md`, and SHA-256 sums of the compressed files and the decompressed streams |
| [`vectors/`](vectors/) | R\*, the two full k = 8 assignments, the k = 9 vector, and the vector of Brillhart–Lehmer–Lehmer's Table V, with SHA-256 sums |
| [`code/`](code/) | the generator, the certificate checkers, the lower-bound checkers, the extended tests and the search programs (provenance) |
| [`verify.sh`](verify.sh) | the verification script |
| [`expected/`](expected/) | transcripts of `verify.sh`, of the extended tests and of the cross-check with Arevalo's code |

## AI assistance

The computations, the programs, the literature search and the text of the paper and of this
repository were produced with an AI system, Claude (Anthropic), used via Claude Code, under the
author's direction. Each computational claim was re-checked in separate sessions of the same AI
system, which wrote their own programs from the format specification or from the definitions.
These sessions all ran on the same underlying system, so their agreement is not independent in the
way that checks by different people would be. All checks were made by AI sessions of the same
system. The author directed the work but has not personally verified the proofs or the code. No
person has checked the paper's proofs, and no person has read the programs line by line.
Independent checking by people is welcome; please report problems through the issue tracker.

## Licence and citation

* Code (`code/` except `code/README.md`, `verify.sh`, `paper/render.sh`, `paper/note.css`): MIT licence, see [`LICENSE`](LICENSE).
* Paper, certificates, vectors and documentation: CC BY 4.0, see [`LICENSE-docs.md`](LICENSE-docs.md).
* How to cite: [`CITATION.cff`](CITATION.cff).

No code from Arevalo's repository is included. `code/extended/arevalo_check.sh` downloads it to
run it.
