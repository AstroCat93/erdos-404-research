#!/bin/sh
# Re-run (job 1): regenerate the f(1,5) >= 10^6 witness and verify it; verify the archived f(1,3)>=2e6 and f(1,7)>=1e6 witnesses.
# usage: sh run_B_witness.sh <dir-with-archived-witnesses or "none">
cd "$(dirname "$0")"
OUT=../outputs; ARCH="$1"
( time ./bin/search5 1 1000000 $OUT/f1_5_K1000000.txt ) > $OUT/B_search5_1e6.log 2>&1
( time ./bin/verify_bin 5 1 1000000 $OUT/f1_5_K1000000.txt ) > $OUT/B_verify5_1e6.log 2>&1
( time ./bin/verify_bin 5 1 1000001 $OUT/f1_5_K1000000.txt ) > $OUT/B_verify5_1e6_plus1.log 2>&1
if [ "$ARCH" != "none" ]; then
( time ./bin/verify_bin 3 1 2000000 "$ARCH/f1_3_K2000000.txt" ) > $OUT/B_verify3_2e6.log 2>&1
( time ./bin/verify_bin 7 1 1000000 "$ARCH/f1_7_K1000000.txt" ) > $OUT/B_verify7_1e6.log 2>&1
fi
echo DONE > $OUT/B_witness_done.txt
