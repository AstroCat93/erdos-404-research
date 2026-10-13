# Track R3M (round 3): odd primes, Haar measure of K_p

Report: `data/round3/reports/R3M.md`. Logs: `data/round3/R3M/`.

Build the Monte Carlo program before re-running `mc_population.log` / `mc_crosscheck.log` rows:

    mkdir -p code/round3/R3M/bin && gcc -O2 -o code/round3/R3M/bin/oddp_mc code/round3/R3M/oddp_mc.c -lm

| file | role |
|---|---|
| `oddp_window_check.py` | exact test of Prop A (odd-p window identity), direct evaluation |
| `oddp_window_check_B.py` | independent exact test of Prop A (carry recursion, flint slopes, DP weights) |
| `spectral_check.py` | exact test of Prop B (pointwise child counts, second-moment identity) |
| `twowin_check.py` | exact test of Cor A' over two windows, Lemma C1(b), Prop C2 |
| `lemma_c5_check.py` | exact test of Lemma C5 (signed-process decomposition of eps) |
| `oddp_mc.c`, `mc_crosscheck.py` | Monte Carlo of populations and its independent cross-check (heuristic) |
| `spectral_mc.py`, `epsilon_scan.py`, `signed_slopes.py`, `eps_gate_depth.py` | heuristic scans (sections 7.2, 7.3, Remark C6, Prop N3) |
| `runlog.sh` | logging wrapper (command line, start time, filtered output, wall time) |
