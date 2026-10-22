#!/bin/bash
# batch_extraC.sh -- program C (third program) on two more depth-7 positions, K'' = 28 and 1, one after
# the other (one core, ~4.2 GB), run after batch_depth7.sh.
ROOT=/home/user/erdos-404-research
BIN=${BIN:?set BIN}
OUT=${OUT:-$ROOT/data/round3/check_R3C}
R=$ROOT/code/round3/check_R3C/run_logged.sh
cd $ROOT
for K in 28 1; do $R $OUT/X_C_p29_t7_H45_K$K.log 4700000 $BIN/covchk 29 7 45 1 pos $K; done
echo "batch_extraC done $(date -u)"
