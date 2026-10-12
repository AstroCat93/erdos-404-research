#!/bin/sh
# usage: run_uniform.sh "p t H kA kB" ...   -> logs/U_p{p}_t{t}_H{H}_{A,B}.log  (A: K = K'; B: K = K' + p^c)
cd "$(dirname "$0")/.."
for spec in "$@"; do
  set -- $spec
  ./bin/fibcov $1 $2 $3 $4 all > logs/U_p$1_t$2_H$3_A.log 2>&1
  ./bin/fibcov2b $1 $2 $3 $5 6 all 1 > logs/U_p$1_t$2_H$3_B.log 2>&1
  echo "$spec: $(grep SUMMARY logs/U_p$1_t$2_H$3_A.log | grep -o 'ALL_COVERED\|SOME_NOT_COVERED') $(grep SUMMARY logs/U_p$1_t$2_H$3_B.log | grep -o 'ALL_OK\|SOME_FAIL')"
done
