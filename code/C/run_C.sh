#!/bin/sh
# Re-run (job 3): track C (gate structure, Theorem F, L_p table, two-block windows for p=17).
cd "$(dirname "$0")"
OUT=../outputs
( for p in 3 5 7 11 13 17 19 23 29 31; do ./bin/ecover_fast $p 6 4000000000; done ) > $OUT/C_ecover.out 2>&1
( time python3 check_structure.py ) > $OUT/C_check_structure.out 2>&1
( time python3 check_window_e.py ) > $OUT/C_check_window_e.out 2>&1
( time python3 check_hk_expansion.py ) > $OUT/C_check_hk_expansion.out 2>&1
( time python3 check_finiteness_general.py ) > $OUT/C_check_finiteness_general.out 2>&1
( for j in 3 4 5; do for t in $(seq 1 16); do ./bin/win2_fast 17 $j $t; done; done ) > $OUT/C_win2_p17.out 2>&1
( time python3 verify_witness.py 11 177152 witnesses/w4_p11_J4.txt ) > $OUT/C_verify_w4_p11.out 2>&1
echo DONE >> $OUT/C_win2_p17.out
