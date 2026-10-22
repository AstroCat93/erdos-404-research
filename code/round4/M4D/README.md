# Track M4D (round 4): decoupling and thinning — code

Report: `data/round4/reports/M4D.md`. Logs: `data/round4/M4D/` (each run preceded by its command line, start time; followed by exit code and wall time; written by `run.sh`). All runs under `nice -n 10`, one at a time, with a wall-time limit.

| file | purpose |
|---|---|
| `m4d_lib.py` | exact p-adic helpers (PAdic, products, alive-path DFS, targets — copied from the validated `code/round3/check_R3M/ck_lib.py`), window elements, numpy subset-sum supports and lift counts |
| `liftprof.c` → `bin/liftprof` | bitset (rotate-or) subset-sum support modulo $p^K$ and per-class lift counts; validated against numpy by `liftprof_validate.py` |
| `lift_lemma_check.py` | exact test of Lemma L (children's targets = affine image of fibre lifts), both directions, brute force over all digit strings; NEG control (wrong unit) |
| `weighted_twowin_check.py` | exact test of Lemmas W1, W2, Prop W4 (both forms), Cor W5(c) (zero variance under complete cosets); modes unif / rand / fib / vary |
| `cw5_check.py` | exact test of Cor W5 (a),(b): optimal-weight harmonic-mean formula |
| `alive_targets_validate.py` | validates the numpy alive-target DP of `lift_scan.py` against the DFS |
| `thmF_e2e.py` | end-to-end exact test of Theorem F (finite horizon): certified chains vs exact survival |
| `lift_scan.py` | heuristic Monte Carlo of the lifting hypothesis (Theorem F) along window chains; also R3M's $\varepsilon$ and the harmonic-mean ratio $m$ |
| `lift_gate_stress.py` | heuristic deep-gate stress test of the lifting criterion (forced gate of depth $s$ in the middle window) |
| `alive_freq_check.py` | frequency of $P(x,n)$ by two independent exact methods (cross-check of the scans) |
| `cov_verify.py` | independent re-check of round-2 covering certificates $\mathrm{Cov}(p,t,H)$ used in Theorem P (and negative controls) |
| `plateau_check.py` | exact simulation test of Theorem P at $p=7$ (target-set recursion), with a control |
| `plateau_bounds.py` | the explicit plateau bounds of Corollary P1 (exact rationals) |
| `batch*.sh`, `chain.sh`, `run.sh` | the logged batches actually run |

Build: `gcc -O2 -o bin/liftprof liftprof.c`.
