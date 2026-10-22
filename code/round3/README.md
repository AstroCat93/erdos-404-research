# Round-3 code (note.md §11)

This directory holds the programs behind §11 of `note.md` (round 3: 2026-10-12, then 2026-10-20/21 after a budget interruption). The logs and data they produced are in `../../data/round3/`. Every program here was written by Claude (Anthropic) instances. According to the workflow configuration, the round-3 track instances ran on Claude Fable 5.1; the lead-author instance reports its model as Claude Opus 5.5 (note.md §11.0). Each subdirectory below says which instance wrote it. No human has checked any of this code.

| dir | written by | what |
|---|---|---|
| `T1a-oddp-quenched/` | track T1a | odd-$p$ quenched martingale (§11.1): window statistics and atom Monte Carlo `winvar.c`, `l2mc.c`; exact window checks `window_exact.py`, `window_exact2.py`; `cp_const.py`, `summarize.py`; batch scripts `run_batch_r3*.sh`, `run_l2mc_batch.sh` |
| `T1b-Kp-structure/` | track T1b | Hausdorff-dimension constants $D_p(w,K)$ of Corollary 11.19 (`wdim.c`, `run_batch.sh`); independent brute force `wdim_check.py`; `hensel_check.py`; the $p=2$, $K=2$ enumeration `p2k2.py` |
| `T2-p2-rate/` | track T2 | $p=2$ rate (§11.3): certificates `certs.py`, `check_cert.py`; slopes and depths `slopes.py`, `slope_depth.py`; `gcap.py`; constants of Corollary 11.30 `constants*.py`; heuristics `agresti*.py`, `lambda_test.py`, `ftilde.py`, `gamma.py` |
| `T3a-q3-fourier/` | track T3a | exact $L^2$ masses (`l2dp.c`, `l2dp_twoarray.c`, `l2post.py`) and their checks `verify_l2_r3.py`, `verify_wide_r3.py`; gate law and $\theta_p$ (`gamma_enum.c`, `gamma_exact.py`, `gamma_table.py`, `theta.py`, `cpJ.c`, `cpJ.py`, `carry_check.py`, `defect_table.py`); sequential Monte Carlo `smc2.c`, `smc_*.py`, `run_smc*.sh` |
| `T3b-q3-covering/` | track T3b | covering programs A′ (`src/fibcov_ip.c`) and C′ (`src/covchk_ip.c`), `src/validate_ip.py`, job and worker scripts, chain checker `src/chain_r3.py`, `src/selfsim_check.py`, `src/s3_check.py`, `src/l2_*.py`; the $p=19$ class lists, job queues and chain specifications (`*.txt`) behind Theorem 11.50 |
| `T3b-finish/` | T3b finishing instance | `src/collect_t3b.py` (log collection and result table) |
| `T4-computations/` | track T4 (and T4b-finish in `code/`) | exact annealed moments `src/annealed.c` and the independent `code/xcheck_annealed.c`; Monte Carlo and range sampler `src/gsampleN.c`; gate sums `src/gatesum.c`; deep $g_2$ values `code/p2add.c`; post-processing scripts; `run_annealed.sh`, `run_queue.sh` |
| `lead/` | lead-author instance | `lead_checks_r3.py`, `lead_t2_certs.py`, `lead_t2_constants.py`, `lead_deep_gcap.py`, `lead_r3fix_checks.py` (rows L1–L10 of note.md §11.8) |

The round-3 referees' programs are archived together with their reports and logs in `../../data/round3/review/` (`verify-logic/`, `verify-computation/`, `verify-novelty/`, the sixteen `refute-*` directories and `recheck/`).

## Build and run

Track commands are listed in note.md §11.8; run each inside its track directory. For example:

```sh
cd T1b-Kp-structure && clang -O2 -o wdim wdim.c -lm && ./wdim 2 9 22     # about 13 min, 32 MB
python3 wdim_check.py 2,3,7 3,2,5 5,1,4 2,5,6 7,1,3

cd ../T3a-q3-fourier && python3 verify_l2_r3.py && python3 theta.py

cd ../T3b-q3-covering
clang -O2 -o bin/fibcov_ip src/fibcov_ip.c      # program A'
clang -O2 -o bin/covchk_ip src/covchk_ip.c      # program C'
python3 src/validate_ip.py
L=../../../data/round2
python3 src/chain_r3.py 19 9 "$L/outputs/R3:$L/logs_original/R3:$L/review/computation/logs:../../../data/round3/T3b-q3-covering/logs" specs_p19_D9_r3.txt 2   # CHAIN OK, f(1,19) >= 17927094312

cd .. && python3 -I lead/lead_r3fix_checks.py && python3 -I lead/lead_t2_constants.py 400
```

Notes:
- Compiled binaries are not included. Create `bin/` first where a command writes into it.
- In ten copied scripts (T3b workers and job wrappers, `validate_ip.py`, T4's `run_annealed.sh` and `run_queue.sh`) the absolute path of the working session was replaced by `<WORKSPACE>`. Set it to a directory of your own before running them.
- The scripts were written for the working layout `code_r3/<track>/` and `data_r3/<track>/`, with this repository checked out as `publish-erdos404/` beside them. Some of them therefore expect relative paths that differ from this repository's layout. Pass the paths explicitly, as in the chain example above. The chain example above uses this repository's paths and was re-run in this layout on 2026-10-21 (`CHAIN OK` with one and with two programs per certificate).
- Kitamura's `p2_exact_table_1_256.csv` is not redistributed; fetch it from `KitaKen1/erdos-404-p2-landscape` for the comparisons in T4 and `lead_checks_r3.py`.
- Run times are listed in note.md §11.8 and in each track's `writeup.md`. The coverage runs behind Theorem 11.50 took about 25 core-hours in total (three workers, at most 45 min and about 3.2 GB per job).
