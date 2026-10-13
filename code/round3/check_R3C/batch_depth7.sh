#!/bin/bash
# batch_depth7.sh -- re-runs of depth-7 position certificates at p = 29, H = 45 (check of R3C).
# Binaries are fresh clang -O3 -march=native builds of the committed sources (BIN below);
# their sha256 is written into each log.  Memory plan (limit 9 GB, 2 cores):
#   phase 1: stream X = A at K''=4 then K''=27;  stream Y = C at K''=15 then K''=21  (A+C ~ 8.7 GB)
#   phase 2: D at K''=4 then K''=27, alone (D needs ~4.8 GB)
ROOT=/home/user/erdos-404-research
BIN=${BIN:?set BIN to the directory with fibcov, covchk, covfast}
OUT=$ROOT/data/round3/check_R3C
R=$ROOT/code/round3/check_R3C/run_logged.sh
cd $ROOT
( for K in 4 27; do $R $OUT/X_A_p29_t7_H45_K$K.log 4700000 $BIN/fibcov 29 7 45 1 pos $K; done ) &
PX=$!
( for K in 15 21; do $R $OUT/X_C_p29_t7_H45_K$K.log 4700000 $BIN/covchk 29 7 45 1 pos $K; done ) &
PY=$!
wait $PX $PY
for K in 4 27; do $R $OUT/X_D_p29_t7_H45_K$K.log 0 env COVFAST_ZMAX=16777216 COVFAST_VERBOSE=1 $BIN/covfast 29 7 45 1 pos $K; done
echo "batch_depth7 done $(date -u)"
