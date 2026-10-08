#!/bin/sh
# Re-run (job 2): every coverage certificate used in Theorem A, with cov.c (exhaustive over K' classes),
# then the independent checker cov_check2.c on the two largest instances.
cd "$(dirname "$0")"
OUT=../outputs/B_cov.log; : > $OUT
for spec in "5 1 3" "5 2 10" "5 3 20" "5 4 25" "7 1 4" "7 2 7" "7 3 19" "7 4 26" "7 5 28" "7 6 35" \
            "11 1 5" "11 2 10" "11 3 18" "11 4 22" "11 5 30" "11 6 33" \
            "13 1 6" "13 2 10" "13 3 19" "13 4 24" "13 5 32" "13 6 35" "13 7 39"; do
  set -- $spec; ./bin/cov $1 $2 $3 $3 34 >> $OUT 2>&1
done
# negative cases quoted in the note
for spec in "3 2 9" "3 3 27" "2 2 4"; do set -- $spec; ./bin/cov $1 $2 $3 $3 34 0 >> $OUT 2>&1; done
# nsample = 0 means exhaustive over all unit classes K' mod p^c (one random lift per class)
( time ./bin/cov_check2 7 6 35 0 1 | tail -1 ) >> $OUT 2>&1
( time ./bin/cov_check2 13 7 39 0 1 | tail -1 ) >> $OUT 2>&1
echo DONE >> $OUT
