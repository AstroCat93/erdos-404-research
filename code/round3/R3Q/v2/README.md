# R3Q (restarted), round 3: programs behind data/round3/reports/R3Q.md

All programs are pure Python 3, need sympy and gmpy2 for the second certificate and the verifier, and run on one core.

| file | role |
|---|---|
| `cert_classes.py`, `cert_classes_sympy.py` | Lemma 3 slope and dead-class certificates (two implementations, no shared code; `../slope_cert.py` from the earlier instance is a third) |
| `common.py` | exact helpers for the lemma tests (BFS of alive paths, Taylor coefficients, weights rho) |
| `test_elementary.py` | random exact tests of Lemmas 1, 4, 6, 8 |
| `test_step.py` | exact test of Lemma 5 (one-step identity), with a rho := 1 control |
| `test_uwin.py` | exact test of Lemma 9 (general thresholds, `gen`) and Corollary 9' (beta thresholds), with a coarser-atom control |
| `bounds.py` | Theorems A, B and Corollary D: float parameter search, exact rational evaluation |
| `verify_bounds.py` | independent exact re-derivation of every bound printed by `bounds.py` or `rule.py` |
| `rule.py`, `rule_K0.py` | Theorem C: fixed parameter rule, exact evaluation, closed-form majorant check on [2400, 4e6] |
| `rule_A.py` | Theorem A': closed-form check on [1024, 4e6] and exact spot values |
| `explore_rhomax.py` | exploration only (heuristic): typical size of max rho |
| `run_logs.sh` | regenerates the logs in `data/round3/R3Q/` (except the two scans `scan_D.log`, `scan_D2.log`, whose commands are recorded inside them) |

The earlier, interrupted R3Q instance's scripts are one directory up. They were used only as a map (see report §9).
