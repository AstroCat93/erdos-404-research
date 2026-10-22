# Exponent vectors

Each file lists lines `q v`: a prime *q* and the value R(q) of an exponent vector, read modulo *k*.
Lines starting with `#` are comments. For a prime p ≡ 1 (mod k) with primitive root g, the vector
of p is R(q) = ind_g(q) mod k. A number n < p is then a k-th power residue iff
f(n) = Σ v_q(n) R(q) ≡ 0 (mod k) (paper, Lemma 2.1). The *least zero pair* of R is the least n ≥ 1
with f(n) ≡ f(n+1) ≡ 0. SHA-256 sums are in `SHA256SUMS`.

| File | k | Contents | Least zero pair |
|---|---|---|---|
| `vec8_compact.txt` | 8 | **R\***: R(q) = 1 for every prime not listed; 74 listed primes, with R(2) = 2 | 1508324 |
| `vec8_L1508323.txt` | 8 | the SAT assignment: all 114765 primes ≤ 1508325, R(2) = 2 | 1508324 |
| `k8_L1508323_witness.txt` | 8 | the tree-search assignment: all 114765 primes ≤ 1508325, R(2) = 2, found by `code/generator/pairtree.c --stop-at-first-U` | 1508324 |
| `vec9_compact18_146290624.txt` | 9 | R(q) = 1 for every prime not listed; 18 listed primes | 146290624 |
| `bll_k8_tableV.txt` | 8 | the vector of Brillhart, Lehmer and Lehmer (1964), Table V, transcribed from the paper (R = 1 for primes not listed) | 1200744 |

For the full assignments, the least zero pair 1508324 does not depend on the values at primes above
1508325, because 1508324 and 1508325 have no such prime factor and the next prime after 1508323 is
1508383.

R\* is the greedy simplification of `vec8_L1508323.txt` (`code/lower/simplify.c`). Each listed
prime other than 2 is needed: resetting it to 1 creates an earlier zero pair. `verify.sh` checks
this with `code/lower/lbcheck.c`, and `code/extended/run_extended.sh` (E6) reproduces the
simplification. The comment lines of `vec8_compact.txt` name `src/simplify.c`; that program is
`code/lower/simplify.c` here. They call the simplification "greedy reset-to-1"; where a reset to 1
failed, the simplifier also tried the values 2 and 0, so some listed values differ from the SAT
assignment. The comment lines of `vec9_compact18_146290624.txt` name
`src/casetest2.c` and an intermediate 7-exception vector. That program is
`code/provenance/casetest2.c`; the intermediate vector is not included. These comments are left
unchanged so that the hashes quoted in the paper stay valid.
