#!/bin/sh
# re-run of every uniform certificate used by the R3 chains (programs A and B), output dir $1
cd "$(dirname "$0")/.."
O=$1
for spec in "7 1 4 0 0" "7 2 7 0 1" "7 3 19 1 2" "7 4 26 2 1" "7 5 28 2 1" "7 6 34 2 1" \
            "11 1 5 0 0" "11 2 10 0 1" "11 3 18 1 0" "11 4 22 1 0" "11 5 30 1 2" "11 6 33 2 1" \
            "13 1 6 0 0" "13 2 10 0 1" "13 3 19 1 1" "13 4 24 1 1" "13 5 32 1 1" "13 6 35 2 1" "13 7 39 2 1" \
            "17 1 5 0 0" "17 2 11 0 1" "17 3 16 0 1" "17 4 25 1 1" "17 5 30 1 1" "17 6 34 1 1" \
            "19 1 5 0 0" "19 2 12 0 1" "19 3 17 0 1" "19 4 27 1 1" "19 5 31 1 1" "19 6 35 1 1" \
            "23 1 7 0 0" "23 2 12 0 1" "23 3 18 0 1" "23 4 23 0 1" "23 5 33 1 0" "23 6 37 1 0"; do
  set -- $spec
  ./bin/fibcov $1 $2 $3 $4 all > $O/U_p$1_t$2_H$3_A.log 2>&1
  sp=6; [ "$1 $2" = "13 7" ] && sp=8
  ./bin/fibcov2 $1 $2 $3 $5 $sp all 1 > $O/U_p$1_t$2_H$3_B.log 2>&1
  echo "$spec: $(grep SUMMARY $O/U_p$1_t$2_H$3_A.log | grep -o 'ALL_COVERED\|SOME_NOT_COVERED') $(grep SUMMARY $O/U_p$1_t$2_H$3_B.log | grep -o 'ALL_OK\|SOME_FAIL')"
done
