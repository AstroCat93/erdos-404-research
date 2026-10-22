# Round-3 logs, data and referee material (note.md §11)

| dir | what |
|---|---|
| `T1a-oddp-quenched/`, `T1b-Kp-structure/`, `T2-p2-rate/`, `T3a-q3-fourier/`, `T3b-q3-covering/`, `T4-computations/` | Each track's report (`writeup.md`), logs and data files. `T1b-Kp-structure/PREDICTIONS_registered_T1b.txt` and `T3b-q3-covering/PREDICTIONS_registered_r3*.txt` are the registered predictions (note.md Corollary 11.19 and Computation 11.51). `T3b-q3-covering/logs/` holds the covering certificates of programs A′ and C′ behind $f(1,19)\ge17\,927\,094\,312$ (Theorem 11.50). |
| `T3b-finish/`, `T4b-finish/` | Reports and logs of the two finishing instances (log collection for T3b; the T4 addendum and re-verification). |
| `gate-status/`, `gate-literature/` | The read-only status check of 2026-10-12 and the verified reference list (note.md §11.0). |
| `lead/` | The lead-author AI instance's re-runs and checks (rows L1–L10 of note.md §11.8), with `commands_log.txt`. |
| `review/verify-logic/`, `review/verify-computation/`, `review/verify-novelty/` | The three round-3 AI referees (2026-10-21): reports, their own code and logs. |
| `review/refute-<result>-gap/`, `review/refute-<result>-counterexample/` | The sixteen targeted AI refutation attempts on Theorems 11.14, 11.17, 11.29, 11.38 and Corollaries 11.19, 11.20, 11.30, 11.39 (2026-10-21). |
| `review/recheck/` | The AI re-check of the corrected note (2026-10-21), `recheck_r3.md` and its script `check_1145.py`. Its six minor findings (R1–R6) are applied in note.md. |

Notes:
- All of this was produced by Claude (Anthropic) instances. No human has checked it.
- File modification times are not preserved by git. Times quoted in note.md §11.0 and §11.9 come from the working directory and from the files' own headers.
- Path-only edits: in T3b's covering logs the machine's hostname was replaced by `<host>`; in `review/verify-computation/code/run_dim.sh` and `run_l2.sh` the referee's scratch directory was replaced by `<scratchpad>/`; in `review/verify-logic/logs/check_p2_firstmoment.log` two absolute paths in warning messages were replaced by a repository-relative path and `<python-site-packages>/`. Nothing else was edited. Four compiled referee binaries were not copied.
- No file here is larger than 1 MB, so nothing is gzipped.
- Kitamura's files fetched by T4 are not redistributed. Only our derived count `T4-computations/kitamura_derived/kitamura_N256.txt` is included; see note.md §2 and the References for links.
