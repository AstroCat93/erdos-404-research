# Round-2 code (note.md §10)

This directory holds the programs behind §10 of `note.md` (round 2, 2026-10-11/12). The logs and data they produced are in `../../data/round2/`. Every program here was written by Claude (Anthropic) instances. Each subdirectory below says which one.

| dir | written by | what |
|---|---|---|
| `R1a/` | track R1a | second route to mu(K_2) = 0 and Claim 10.9 (`code/class_check.py`, `I8.py`, conservation and T_m tests, `pop.c`); `explore/` scripts |
| `R1b/` | track R1b | `muK2_proof.tex`, the track's write-up of Theorem 10.1; exact checks of the window identity (`mart_check2.py`, `brute_window.py`, `negctrl.py`, `lemmaB_check.py`, `rho_table.py`, `lam_stats.py`, `sim_mart.py`) |
| `R2a/` | track R2a + lead | Fourier shell sums (`fl1.c`; the lead's independent `fl1_lead.c` and interval-arithmetic `iv_shells.py`), Knuth estimators, `renorm_check.py` |
| `R2b/` | track R2b | `src/` (Fourier window diagnostics `fwin2.c`, `twofree.c`, `lambda_p.py`, `rmf_budget.py`, ...), `lean/Renorm.lean` (Theorem 10.12 core, Proposition 10.14 recursion) |
| `R3/` | track R3 | covering programs A (`src/fibcov.c`) and B (`src/fibcov2.c`), brute-force reference `src/brute.py`, `src/validate.py`, chain checker `src/chain.py`, scan and law scripts; `specs/` (chain specifications); `data/` (position and job lists) |
| `.` | lead | `lead_checks.py`, `lead_window_check.py`, `lead_hmean.py`, `run_lead_batch.sh` |
| `review/logic/` | round-2 logic referee | `covmiss.c` (fibre/bitset covering checker), `p2_window.py`, `lam_probe.py`, `quick_checks.py`, `shells.py` |
| `review/computation/` | round-2 computational referee | program C `covchk.c`, `brute_val.py`, `chain_c.py`, `scan.py`, `shells.c`, `equidist_dp.py`, `p2_window.py`, `thm1012_brute.py`, `misc_checks.py`, worker scripts `w*.sh` |
| `review/novelty/` | round-2 novelty referee | `covchk.c`, `brute.py` |

## Build and run

From this directory:

```sh
clang -O3 -march=native -o R3/bin/fibcov  R3/src/fibcov.c
clang -O3 -march=native -o R3/bin/fibcov2 R3/src/fibcov2.c
clang -O3 -o R2a/bin/fl1      R2a/fl1.c -lm -lpthread
clang -O3 -o R2a/bin/fl1_lead R2a/fl1_lead.c -lm
sh run_lead_batch.sh /path/to/a/Mathlib/project   # rows S1-S13 of note.md §10.7; writes to ./outputs/
python3 lead_hmean.py                              # row S14
```

The certificate re-runs (rows C1–C6) work as follows:
1. Copy `../../data/round2/outputs/R3/rerun_jobs_list.txt` to `R3/data/rerun_jobs.txt`.
2. Run `mkdir -p outputs/R3`.
3. From `R3/`, start up to three workers with `sh src/rerun_worker.sh w1` (then `w2`, `w3`).
4. Check the chains with `R3_LOGS=../outputs/R3 python3 src/chain.py specs/p13.txt` (and similarly for the other specs).

To check the archived logs instead, set `R3_LOGS=../../../data/round2/outputs/R3`. The p = 17, depth-9 chain also needs program B's original logs: `R3_LOGS=../../../data/round2/outputs/R3:../../../data/round2/outputs/R3_p17_programB_original`.

The scripts were written for the working layout `code_r2/`, where outputs sat next to the code. That is why fresh outputs go to `./outputs/` here, while the archived outputs are in `../../data/round2/outputs/`. Run times are listed in note.md §10.7. No single job of the 2026-10-12 re-runs took more than 50 minutes, and at most 3 cores were used.
