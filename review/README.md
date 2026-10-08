# Referee code and outputs

After the first version of `note.md` was written, three separate Claude instances refereed it
(logic, computation, novelty; summary in note.md §9). The logic and computation referees wrote
their own programs from scratch, sharing no code with `code/`. They are kept here, as written,
so that the independent confirmations cited in the note can be reproduced. They are working
scripts, not polished tools. Paths inside them are relative to their own directory.

## `logic/` (logic referee)

| file | checks |
|---|---|
| `check1.py` | gamma_p(m) by meet-in-the-middle, Phi_p, the {68,77} obstruction mod 81, p = 2 never full mod 16, p = 2 class counts |
| `check2.py`, `check3.py` | which N mod 3^k have A_N full mod 3^k (p = 3 full tails only at N = 27, 54 mod 81) |
| `check4.py` | gap theorem (Thm 3.9(d)) on small a; g_3(3), g_3(12); rational roots of S_B for B in [1,8] (needs sympy) |
| `check_Lp.py`, `ecov.c` | L_p for p <= 31 (Python) and L_p >= 6 for 37 <= p <= 53 (C bitmap; `cc -O3 -o ecov ecov.c; ./ecov 37 6`) |
| `check_cov.py` | Cov certificates (Python big-int bitsets); logs `cov_11_6_33.log`, `cov_13_6_35.log` |
| `check_win2.py` | two-block windows; dependence on t mod p only |
| `check_delta.py` | delta_G(p) for small G |
| `lean_rerun.log` | the referee's re-run of the seven Lean files |

## `computation/` (computational referee)

Compile the C programs first: `cc -O3 -o rcover rcover.c && cc -O3 -o census census.c`.

| file | checks |
|---|---|
| `core.py` | exact carry DP for g_p(a), brute force, gamma_p(m) two ways |
| `rcover.c` | cyclic-bitset subset-sum coverage checker (stdin: `M n x_1 ... x_n`) |
| `cov.py` | Cov certificates and negative scans via `rcover` |
| `census.c` | class census by DFS with an exact DP per child (no halving lemma); `census_p2_32.out` is the p = 2 census to G = 32, `census_odd*.out`, `census_p3_*.out` the odd primes |
| `lp.py`, `lp_large.out` | L_p >= 6 for 37 <= p <= 53, L_p >= 5 for 59 <= p <= 97 |
| `win2.py`, `win2_big.out` | two-block windows |
| `wverify.py`, `wverify_big.out` | witness verifier (descending Horner); found that the f(1,3) witness is divisible by 3^2000001 |
| `t1.py` ... `t13.py` | numbered checks of exact values, gamma/Phi tables, Thm 3.8, 3.11, 3.12(a), halving, gap theorem, Prop 3.14, landscapes |
| `t14.py`, `t14.out` | sampled probe of Cov(5,5,H), H = 31..39 (8 classes per H; superseded by note.md R20, which found failing classes at H = 35 and 38) |
| `t15.py` | depth-7 positions at p = 7 (its output was not saved; re-run in note.md R19) |
| `t16.py`, `t16.out` | depth-7 positions at p = 11: H = 40 covers mod 11^10 at N* = 11^7 K'', K'' = 1..10, giving f(1,11) >= 21 435 880 |

The novelty referee wrote no code beyond a PDF text extractor; its findings are summarised in note.md §9.
