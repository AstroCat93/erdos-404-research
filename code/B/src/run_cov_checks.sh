#!/bin/sh
# independent re-check of every positive coverage certificate used in Theorem A
cd "$(dirname "$0")/.."
for spec in "3 1 2" "5 1 3" "5 2 10" "5 3 20" "5 4 25" "7 1 4" "7 2 7" "7 3 19" "7 4 26" "7 5 28" \
            "11 1 5" "11 2 10" "11 3 18" "11 4 22" "11 5 30" "11 6 33" \
            "13 1 6" "13 2 10" "13 3 19" "13 4 24" "13 5 32" "13 6 35"; do
  python3 src/cov_check.py $spec
done
python3 src/cov_check.py 7 6 35 300
