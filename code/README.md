# Code for the Erdős #404 research note (2026-10-08)

See `../note.md`, §7, for the full reproduction table (commands, expected results, timings).
Quick start (macOS/Linux, clang or gcc + python3; Lean optional):

    sh build.sh                                                       # compile every C program (needed first)
    python3 -I indep/indep_checks.py                                  # R2 (independent oracle, ~15 s)
    python3 -I indep/extra_checks.py                                  # R3
    sh C/run_C.sh                                                     # R8-R11
    sh run_DEFA.sh                                                    # R12-R18
    sh B/run_B_cov.sh                                                 # R6 Theorem A certificates (~35 min, ~2.5 GB RAM)
    sh B/run_B_witness.sh none                                        # R4 regenerate + verify f(1,5) >= 10^6 (~11 min)
    sh lean/run_lean.sh /path/to/a/Lean4-v4.34.1-Mathlib-project      # R1

Publication re-checks (R19-R21 in note.md §7.2):

    B/bin/cov_pos 11 7 40 1 2 3 4 5 6 7 8 9 10                        # depth-7 positions, p = 11 (6.5 GB RAM, ~1.5 min)
    B/bin/cov_pos 7 7 40 1 2 3 4 5 6                                  # depth-7 positions, p = 7
    B/bin/cov_pos 5 5 35 1 21001                                      # Cov(5,5,35) fails at K' = 21001
    python3 B/src/cov_inputs.py 7 7 40 1 | ../review/computation/rcover   # same check with the referee's program
                                                                      # (compile it first: cc -O3 -o ../review/computation/rcover ../review/computation/rcover.c)

Subdirectories A..F hold the programs of the six research tracks (A structure, B computation,
C large p, D p=2, E behaviour, F coverage/literature); `indep/` was written independently for the
note; `outputs/` holds the logs of the 2026-10-08 re-runs (files named `pub_*` are the publication
re-checks). All computations are exact (integer / residue arithmetic) except `F/fourier.c`
(floating point, heuristic only) and the Monte Carlo programs `D/gsample*.c` (heuristic only).

Two large regenerable outputs are not committed: `outputs/f1_5_K1000000.txt` (written by R4; a gzipped
copy is in `../archive/witnesses/`) and `outputs/E_trees/` (written by R13).
