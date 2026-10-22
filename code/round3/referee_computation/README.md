# Round-3 computational referee: programs and logs

Written by the round-3 computational referee (an AI instance; see `data/round3/referees/computation.md`).
None of these files shares code with the round-3 tracks (`R3N`, `R3Q`, `R3M`, `R3F`) or with their
checkers (`check_*`). The only inputs read from the tracks are the shipped data files (witnesses,
survey CSVs) and the parameters printed in their logs and reports.

| file | what | log(s) in `logs/` |
|---|---|---|
| `verify_witness_bsplit.py` | witness verifier for f(a,2) >= K: sum of n! by binary splitting over the witness (CPython integers, not GMP), then v_2; self-test against direct sums | `witness_selftest.log`, `witness_594_K90394.log`, `witness_17662_K221465.log` |
| `rsolve.c` | exact exhaustive solver: decides "some P with min P = a has 2^K \| sum P n!"; reports the maximum valuation over all P when unreachable; writes a witness when reachable | `rsolve_594.log`, `rsolve_shadow.log`, `rsolve_17662.log` |
| `check_survey.py` | random sample (seed 404, 320 rows) of the R3N survey CSVs plus a = 34, 1102, 17534, each in both directions with `rsolve`; witnesses re-verified by `verify_witness_bsplit.py`; rows with g <= 300 also by a pure-Python breadth-first oracle | `survey_sample.log` |
| `csv_claims.py` | table-level claims of note §11.1 re-derived from the CSVs | `csv_claims.log` |
| `lemma3_cert.py` | R3Q Lemma 3 (note Lemma 11.5): exhaustive certificate by integer evaluation and divided differences; plus an exhaustive alive-path test on random 2-adic x | `lemma3_cert.log` |
| `cord_row.py` | rows K = 37, 40, 448 of R3Q Corollary D (note Corollary 11.8), from the statements of Theorems A, B in exact rationals | `cord_rows.log` |
| `rule_check.py` | the closed-form majorants behind note Theorems 11.7 and 11.9 | `rule_check.log` |
| `gate_shells.py` | R3F Lemma A1, Theorem A2, Theorem A5 entries (note 11.16, 11.17, 11.19) | `gate_shells.log` |
| `propB_check.py` | R3M Proposition B (note Proposition 11.11) at p = 5 on five windows, brute force vs. the identity | `propB_check.log`, `propB_population_crosscheck.log` |

Build and run (one core, `nice -n 10`; total CPU about 47 minutes, of which 29 minutes went to the optional `rsolve 17662 221466` run, which hit its 30-minute timeout without a result):

```sh
gcc -O3 -march=native -o /tmp/r3_ref_computation/rsolve code/round3/referee_computation/rsolve.c
python3 -I code/round3/referee_computation/verify_witness_bsplit.py data/round3/R3N/witness_594_K90394.txt.gz 594 90394
python3 -I code/round3/referee_computation/verify_witness_bsplit.py data/round3/R3N/witness_17662_K221465.txt.gz 17662 221465
python3 -I code/round3/referee_computation/check_survey.py /tmp/r3_ref_computation/rsolve /tmp/r3_ref_computation/w 404 320 300 34,1102,17534 data/round3/R3N/survey_*.csv
/tmp/r3_ref_computation/rsolve 594 90395            # 6 min, 0.5 GB
/tmp/r3_ref_computation/rsolve 594 90394 w594.txt   # 2 min
python3 -I code/round3/referee_computation/lemma3_cert.py
python3 -I code/round3/referee_computation/cord_row.py
python3 -I code/round3/referee_computation/rule_check.py
python3 -I code/round3/referee_computation/gate_shells.py
python3 -I code/round3/referee_computation/propB_check.py
```

Each log starts with its command line.
