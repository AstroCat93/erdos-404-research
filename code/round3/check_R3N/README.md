# check_R3N (round 3): adversarial check of track R3N (f(594,2) = 90394 and related claims)

Report: `data/round3/checks/R3N.md`. Logs: `data/round3/check_R3N/`. Binaries and scratch: `/tmp/r3_check_R3N/`.

| file | role |
|---|---|
| `rerun_594.sh` | re-runs the track's programs C (`dfsW.c`) and B (`dfsB.c`), rebuilt from source, on a = 594: C at K = 90395 and 90394 (witness), B at K = 90395 |
| `verify_w.py` | own exact witness verifier (gmpy2). Two methods that must agree, both different from the track's verifiers (which sum a running product n!): (H) backward Horner nesting S = a_1!(1 + P(a_1+1,a_2)(1 + ...)), exact integers; (M) S mod 2^(K+64) from odd parts of n! and Legendre's v_2(n!) = n - s_2(n). Requires v_2(S) = K exactly, min A = a, strictly increasing |
| `verify_all.sh` | runs `verify_w.py` on the track's shipped witnesses (594 at 90394 from C and from B, 594 at 66126, 17662 at 148725 and 212995) and on two later 17662 witnesses that exist only in `/tmp/r3_R3N` |
| `dfsD.c` | own exhaustive solver ("program D"), written from scratch: single steps n -> n+1, unshifted S_n mod 2^K, 128-bit windows (`unsigned __int128`), GMP `mpn` full precision, survivors updated only at the positions where the choice vector changed, running factorial cross-checked against `mpz_fac_ui` every 8th window. Prints steps (= steps_B - 1 by the counting of the track's Lemma 5) and alive_even (= nodes_C / 4). Option `-p L START END TLIMIT` (added after the 594 and survey runs) expands only the subtrees at window L with index in [START, END) and stops at a subtree boundary after TLIMIT seconds, printing NEXT |
| `chain_17662.sh` | independent upper-bound check of the track's dfsW4 result EXACT f(17662,2) = 221465: `dfsD 17662 221466` split into sequential jobs (`-p 120 START inf 1000`, hard cap 1790 s each) over the subtrees rooted at window 120 |
| `validate_D.py` | validates `dfsD` (and `verify_w.py`) against Kitamura's table a <= 256 (both directions, witnesses checked), against a seeded random sample or explicit rows of the track's survey, and (`full`) re-certifies every exact survey row |
| `test_verifier.py` | validation of `verify_w.py`: brute force on random small sets, and negative tests |
| `check_csv.py` | parsing-only consistency checks of the track's survey CSVs against the claims of its report (§4.1, §6), against Kitamura's rows, and of the profile sum |

Build: `gcc -O3 -march=native -o /tmp/r3_check_R3N/dfsD dfsD.c -lgmp` (gcc 13.3.0).
Track binaries: `gcc -O3 -march=native -o /tmp/r3_check_R3N/dfsW code/round3/R3N/dfsW.c` and
`gcc -O3 -march=native -o /tmp/r3_check_R3N/dfsB code/round3/R3N/dfsB.c -lgmp`.
