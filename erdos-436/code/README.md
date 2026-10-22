# Programs

Paths are relative to the repository root. "§" refers to [`paper/note.md`](../paper/note.md). All
programs were written with an AI system (see the paper's §9). "Separately written" means written in
a different AI session, from [`certificate/FORMAT.md`](../certificate/FORMAT.md) or from the
definitions, without reusing the generator's code. No person has read these programs line by line.

C programs compile with `gcc -O2` (gcc 13.3 was used). Python programs need Python 3 and only the
standard library, except those marked *numpy*. Every program prints its usage at the top of its
source file.

## Upper bound (§3)

| Program | Origin | What it does | Run by |
|---|---|---|---|
| `generator/pairtree.c` | the generator | builds the canonical case tree for (k, L, S2) and writes the certificate stream; also the depth-capped trees and the full-depth witness search of the negative controls | `verify.sh` [4], `run_extended.sh` E4 |
| `upper/check_cert.py` | written together with the generator, against `FORMAT.md` | checks a certificate; factors every leaf with its own sieve; prints the header it verified | `verify.sh` [2] |
| `upper/pcheck.py` | separately written from `FORMAT.md` alone | checks a certificate against an expected header and hash (sieve factorisation, stack walk) | `verify.sh` [2] |
| `upper/ccheck.c` | separately written from `FORMAT.md` alone | checks a certificate (trial division by the assigned primes only, counter walk); also walks the tree for given assignments | `verify.sh` [2], E2, E3 |
| `upper/rcheck.c` | separately written from `FORMAT.md` | third checker, with strict syntax checks | `verify.sh` [2] |
| `upper/regen.c` | separately written from the canonical-form rule of `FORMAT.md` | regenerates the canonical stream; its SHA-256 must equal the bundled one | `verify.sh` [4] |
| `upper/tree8.c` | separately written | the same branching rule with node counts only (2000473 internal nodes, 14003308 closed leaves for k = 8) | E1 |
| `upper/smallp.c` | with the generator | (H3): r(8,2,p) for all primes 3 ≤ p ≤ 1508325 by Euler's criterion | `verify.sh` [2] |
| `upper/smallp_ref.c` | separately written | (H3) by three methods (Euler's criterion, the index model with discrete logarithms, and brute force for p < 20000), which must agree | `verify.sh` [2] |
| `extended/smallp_euler.c` | separately written | (H3) a third time | E5 |

## Lower bound (§4, §7)

| Program | Origin | Algorithm | Run by |
|---|---|---|---|
| `lower/pairs.c` | separately written from the definitions | linear least-prime-factor sieve, f(n) = f(n/lp(n)) + R(lp(n)) | `verify.sh` [3], E6 |
| `lower/pairs_np.py` (*numpy*) | separately written, same session as `pairs.c` but a different algorithm | additive prime-power sieve | `verify.sh` [3] |
| `lower/fp_seg.c` | separately written | segmented divide-out sieve | `verify.sh` [3] |
| `lower/lbcheck.c` | separately written from the paper's definitions | smallest-prime-factor recursion; with `reset`, resets each listed prime to 1 and reports whether the least zero pair moves earlier | `verify.sh` [3] |
| `lower/check_vector.py` | with the generator | smallest-prime-factor recursion, standard library only | `verify.sh` [3], E4 |
| `lower/simplify.c` | same session as `pairs.c` | greedy simplification that produced R\* from the SAT assignment: for each prime in decreasing order, move its value to 1, or failing that to 2 or 0, whenever the first zero pair stays at 1508324 | E6 |
| `lower/vecfacts.py` | separately written | the facts of §4 about the vectors: the table in the paper equals the file, agreement with [BLL64, Table V] at 24 of 39 primes, the 23776 differences between the two full assignments, the trivial unit stabiliser of R\* | `verify.sh` [3], E6 |

## Extended tests (`extended/`)

`extended/run_extended.sh` (or `./verify.sh --extended`) runs E1 to E7:

| Step | Programs | Statement of the paper |
|---|---|---|
| E1 | `upper/tree8.c` | §3: a separately written implementation of the branching rule gives identical node counts |
| E2 | `extended/tamper.py`, `extended/tamper2.py`, `extended/diff_small.py` | §3: both checkers written from `FORMAT.md` alone reject all 35 invalid mutations of the k = 8 stream (31 structural, 3 semantic, 1 header) and accept a valid alternative leaf; three checkers agree on all 7955 single-line mutants of the k = 2, 3, 4, 5 certificates |
| E3 | `extended/rscan.c`, `extended/e2e.py` | §3: 2126 primes p ≡ 1 (mod 8) (2000 random primes between 1508326 and 10⁴⁰, and all 126 primes p < 5·10⁸ with r(8,2,p) ≥ 650); R_{p,g} is computed from p, the tree is walked, and the leaf pair is confirmed by modular exponentiation |
| E4 | `generator/pairtree.c`, `lower/check_vector.py` | §3: at L = Λ(k,2) − 1 the generator finds a full assignment with no zero pair, for k = 2, …, 8; the k = 8 trees capped at depths 61, 62 and 80 leave 432, 432 and 5301696 leaves unresolved; the k = 8 witness equals `vectors/k8_L1508323_witness.txt` |
| E5 | `extended/smallp_euler.c` | (H3), third program |
| E6 | `lower/simplify.c`, `lower/vecfacts.py`, `lower/pairs.c` | §4: R\* is the greedy simplification of the SAT assignment; facts about the vectors; the model reproduces the bound 1200744 of [BLL64, Table V] |
| E7 | `extended/chebo.c`, `extended/chebo_analyse.py` (*numpy*) | Remark 6.1: among the 12711219 primes p ≡ 1 (mod 8) below 10⁹, R_{p,g}(2) is never odd, and every assignment on the primes 2, …, 17 with R(2) even occurs |

`extended/arevalo_check.sh` (optional; needs git and network access) downloads Fabian Arevalo's
repository <https://github.com/farev/matematica> at commit
`4404f5bd46cd9248807980ea73a8a6467afdb342`, compiles and runs Arevalo's `tree2.c` and
`check_tree2.py`, and then checks the cross-check of §3 and the statement of §4 that R\*, restricted
to the 62 primes below 300, is the eleventh of Arevalo's 108 unsettled vectors
(`extended/cmp108.py`, `extended/rstar_in_gaps.py`, `extended/audit_external_pairs.py`). On
2026-10-15 the inputs had these SHA-256 hashes:

* `tree2.c`: `8ef9fa5ce810bc93e971008be69038512f87a2810e6c107c5b80b97c63cfcce5`;
* `check_tree2.py`: `91bbe9820395b29af3b23723bb342b29063d1456c291f2d7dfb49f5214168a14`;
* `data/pairs_P300_L10000000.txt`: `caf449a676cad94bde064d590c96ab3a24bae6bc213c286ad165ed80b27540e3`.

No code from that repository is included here.

## Provenance (`provenance/`)

These programs found the vectors. They are not needed to verify anything, because the vectors are
checked directly.

* `provenance/sat8.py` encodes "no zero pair n ≤ L" for k = 8 as a SAT problem, with the values on
  the first 16 primes fixed (`provenance/sat8_prefix16.txt`). It solves the problem with CaDiCaL 1.5.3
  through PySAT (`pip install python-sat`; solver name `cadical153`). With L = 1508323 it found
  `vectors/vec8_L1508323.txt` in under a second, after about 40 s of encoding. The same prefix
  with L = 1508324 is unsatisfiable.
* `lower/simplify.c` then simplified the values one prime at a time (to 1 where possible, otherwise
  to 2 or 0), keeping the first zero pair at 1508324. This gave R\* (run E6 reproduces it).
* `provenance/casetest2.c` is the local search (a lookahead variant of the case test of
  [BLL64, §4]) that produced the k = 9 vector of §7.

## Expected output and timings

Times are from the runs recorded in [`expected/`](../expected/), on one core of a 4-core Linux
machine with 15 GB of memory, gcc 13.3, Python 3.13 and numpy 2.5. `verify.sh` takes about
2 minutes in total. Its slowest steps are `check_cert.py` on k = 8 (about 37 s), `pcheck.py` on k = 8
(about 17 s), and `regen.c` and `pairtree.c` on k = 8 (about 9 s and 5 s). The extended tests take
about 15 minutes. Their slowest steps are the structural tamper tests of E2 (about 6 minutes), the
empirical test of E7 (about 3 minutes), the depth-80 capped tree of E4 (about 1.5 minutes) and the
scan for hard primes in E3 (about 1 minute). `code/extended/arevalo_check.sh` takes about
1.5 minutes after the download.
