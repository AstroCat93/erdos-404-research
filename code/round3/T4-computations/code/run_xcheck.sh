#!/bin/sh
# independent re-computation of the annealed sums with code/xcheck_annealed.c (2 processes)
cd "$(dirname "$0")"
for pg in "2 18" "3 11" "5 7" "7 6" "3 10" "5 6" "7 5"; do
  set -- $pg
  s=$(date +%s)
  r=$( (./xcheck_annealed $1 $2 0 2 & ./xcheck_annealed $1 $2 1 2 & wait) | tr '\n' ';')
  echo "xcheck p=$1 G=$2 : $r elapsed $(( $(date +%s) - s )) s"
done
