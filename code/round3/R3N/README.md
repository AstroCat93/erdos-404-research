# Track R3N (round 3): exact f(a,2), in particular f(594,2) = 90394

All programs decide "is there a finite set A with min A = a and 2^K | sum_{n in A} n! ?" for even a,
and print the exact value f(a,2) when the answer is no (see data/round3/reports/R3N.md, Lemmas 1-2).

| file | role |
|---|---|
| `dfsW.c` | **program C**: windowed depth-first search (hand-written 64-bit limb arithmetic, unshifted sums S_N mod 2^K, pair steps, 256-bit windows, prefix-sharing materialisation). Writes a witness on success. |
| `dfsWp.c` | program C plus a population profile (number of alive paths at every window boundary) |
| `dfsB.c` | **program B**: independent windowed DFS (GMP `mpz`, shifted normal form T_N = S_N/2^{v(N!)}, single steps, 128-bit windows, each survivor rebuilt from scratch). Shares no code with C. |
| `dfsW3.c` | program C with half the table memory (stores N! only; options applied as N!·m, m = 1, N+1, N+2). Output identical to `dfsW` on 262 validation runs and on a = 594 |
| `dfsW4.c` | `dfsW3` plus checkpoint/resume (`-c FILE -i SECONDS -r`, `-x` for testing) and witnesses for intermediate best valuations (`-b PREFIX`, written each time the best death valuation crosses a multiple of 4096). Resume tested on a = 34 (10 interruptions) and a = 594 (11 interruptions): identical node and survivor counts |
| `dfsB2.c` | program B with half the table memory (G stored at even offsets; odd offsets via `mpz_addmul_ui`). Output identical to `dfsB` on 262 validation runs |
| `bfsA.c` | program A: breadth-first search with hash deduplication (only used for validation and for a=594 up to N=10596; too memory-hungry for a=594 at full depth) |
| `verify_witness.py` | exact witness verifier, plain Python integers (running product, no reduction) |
| `verify_witness_gmp.c` | second exact witness verifier, GMP (`mpz_fac_ui` + running product, `mpz_scan1`) |
| `validate_table.py` | runs B and C against K. Kitamura's exact table f(a,2), a <= 256 (both directions) |
| `survey.py` | exact f(a,2) for a range of even a: C with doubling targets, then B at K=f and f+1, then C's witness at K=f checked by the GMP verifier |
| `profile_summary.py` | summary of a `dfsWp` profile |

Build (binaries in /tmp/r3_R3N):

```sh
gcc -O3 -march=native -o dfsW dfsW.c
gcc -O3 -march=native -o dfsWp dfsWp.c
gcc -O3 -march=native -o dfsB dfsB.c -lgmp
gcc -O3 -march=native -o bfsA bfsA.c
gcc -O2 -o verify_witness_gmp verify_witness_gmp.c -lgmp
```

Main commands (logs in data/round3/R3N/):

```sh
dfsW 594 90395                          # C: reachable=0, EXACT f=90394 (181 s)
dfsB 594 90395                          # B: reachable=0, EXACT f=90394 (1001 s)
dfsW 594 90394 w594_90394.txt           # C: witness, 44801 terms (140 s)
python3 -I verify_witness.py w594_90394.txt 594 90394      # v2(sum) = 90394
verify_witness_gmp w594_90394.txt 594 90394                # v2(sum) = 90394
```

Further runs (all logged in data/round3/R3N/):

```sh
dfsB 594 90394 wB594_90394.txt          # B: its own witness (44804 terms), 320 s
clang -O3 -march=native -DWL=8 -o dfsW8c dfsW.c && dfsW8c 594 90395   # 512-bit windows: same node count
dfsWp 594 90395 - profile_594.txt       # population profile
python3 -I validate_table.py p2_exact_table_1_256.csv /tmp/r3_R3N    # Kitamura's table, ALL_OK
python3 -I survey.py 2 4096 65536 /tmp/r3_R3N survey_2_4096.csv      # and 4098..16384, 16386..32768 (cap 131072)
python3 -I profile_summary.py profile_594.txt 594
```
