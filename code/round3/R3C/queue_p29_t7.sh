#!/bin/bash
# queue_p29_t7.sh -- depth-7 position certificates at p = 29 (round 3, track R3C).
# For K'' = K0..K1 (in increasing order): program D (covfast) then program A (fibcov) on the block of
# length H = 45 ending at N* = 29^7 K''.  If either program reports NOT_COVERED, both are re-run at
# H = 46 for that position.  One log per (program, H, K''); sequential (each job needs ~4.3 GB).
# Stop gracefully by creating /tmp/r3_R3C/STOP.
ROOT=/home/user/erdos-404-research
BIN=/tmp/r3_R3C/bin
OUT=$ROOT/data/round3/R3C/p29_t7
K0=${1:-2}; K1=${2:-28}
mkdir -p $OUT
cd $ROOT
for K in $(seq $K0 $K1); do
  for H in 45 46; do
    [ -e /tmp/r3_R3C/STOP ] && { echo "STOP file found before K=$K H=$H"; exit 0; }
    code/round3/R3C/run.sh $OUT/P29_t7_H${H}_D_K$K.log env COVFAST_ZMAX=16777216 $BIN/covfast 29 7 $H 1 pos $K
    [ -e /tmp/r3_R3C/STOP ] && { echo "STOP file found before A K=$K H=$H"; exit 0; }
    code/round3/R3C/run.sh $OUT/P29_t7_H${H}_A_K$K.log $BIN/fibcov 29 7 $H 1 pos $K
    if grep -q "^D .* COVERED" $OUT/P29_t7_H${H}_D_K$K.log && grep -q "^A .* missing=0 COVERED" $OUT/P29_t7_H${H}_A_K$K.log \
       && ! grep -q "NOT_COVERED" $OUT/P29_t7_H${H}_D_K$K.log $OUT/P29_t7_H${H}_A_K$K.log; then
      break
    fi
  done
done
echo "queue done K=$K0..$K1"
