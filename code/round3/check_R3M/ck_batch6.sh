#!/bin/sh
# ck_batch6.sh -- second check_R3M instance: larger importance-sampling probe of gate contributions to
# E[(M^0_n)^2] (heuristic; section 7.1 of the R3M report).
R=code/round3/check_R3M
D=data/round3/check_R3M
for i in 9 12 15 18 21 27 33 39; do
  $R/ck_run2.sh $D/deepgate_M2.log 300 python3 $R/ck_deepgate_M2.py 3 82$i 100 40 $i 14
done
for i in 10 15 20 25 30; do
  $R/ck_run2.sh $D/deepgate_M2.log 300 python3 $R/ck_deepgate_M2.py 5 83$i 100 30 $i 8
done
$R/ck_run2.sh $D/mc_M.log 600 python3 $R/ck_mc_M.py 5 702 2000 16,24,30
