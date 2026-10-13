# Round-3 code (note.md §11)

This directory holds the programs behind §11 of `note.md` (round 3, 2026-10-13). Their logs, witnesses and data are in `../../data/round3/`. Every program here was written by Claude (Anthropic) instances. Each subdirectory says which one.

| dir | written by | what |
|---|---|---|
| `S0/` | track S0 (status gate) | independent re-checks of Kitamura's table a ≤ 256 and of the first rungs for a = 594 (with round-1 code); Lemma S0.1 numerics |
| `R3N/` | track R3N | exact f(a,2): program C `dfsW.c` (windowed DFS), program B `dfsB.c` (GMP, independent), `dfsW3.c`/`dfsW4.c` (half memory; checkpoint/resume), `dfsB2.c`, program A `bfsA.c` (BFS, failed route), witness verifiers `verify_witness.py` and `verify_witness_gmp.c`, `survey.py`, `validate_table.py`; see `R3N/README.md` |
| `check_R3N/` | the R3N checker | program D `dfsD.c` (third independent exhaustive solver), `verify_w.py` (Horner and odd-part verifier), full re-certification drivers |
| `R3Q/` | track R3Q | `v2/`: the restarted track's certificates, lemma tests, bound evaluators and closed-form checks (see `v2/README.md`); the top-level files are the earlier, interrupted instance's code, kept for provenance only |
| `check_R3Q/` | the R3Q checker | third slope certificate (dual numbers), random exact lemma tests, independent bound evaluator |
| `R3M/` | track R3M | odd-p window identity tests (`oddp_window_check.py`, `oddp_window_check_B.py`), second-moment and two-window tests, Lemma C5 checks, Monte Carlo `oddp_mc.c` |
| `check_R3M/` | the R3M checkers (a first instance was cut off; a second completed the check) | independent exact tests of every proved item |
| `R3F/` | track R3F | interval-arithmetic shells `ivshell.c`, `gate_d.c`, rigorous `J_p` (`jrel.c`), exact L² counts `l2_dp.py`, K'-averaging and transfer scripts |
| `check_R3F/` | the R3F checker | `shellchk.c` (arb-certified tables), `jcheck`, independent L² and K'-averaging checks |
| `R3C/` | track R3C | program D `covfast.c` (covering, written from scratch), scan and chain scripts, prediction generator, queue scripts |
| `check_R3C/` | the R3C checker | see `data/round3/checks/R3C.md` |
| `referee_<role>/` | the round-3 referees | see `data/round3/referees/` |

Binaries were built into `/tmp/r3_<track>/` with `gcc -O3 -march=native` (and `-lgmp` where GMP is used); the exact build lines are in each track's README or report. An external spending limit interrupted the session once; the lead resumed the R3N search (`dfsW4 ... -r`) and the R3C queues (`queue_p29_t7.sh`) unchanged, and R3Q was redone from scratch (note.md §11.0).
