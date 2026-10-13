#!/bin/sh
# ck_batch2.sh -- heuristic probes of the check of track R3M (run from the repository root).
R=code/round3/check_R3M
D=data/round3/check_R3M
$R/ck_run.sh $D/mc_M.log python3 $R/ck_mc_M.py 3 701 20000 16,24,32,40
$R/ck_run.sh $D/mc_M.log python3 $R/ck_mc_M.py 5 702 2000 16,24,30
for i in 12 18 24 27 30 32; do
  $R/ck_run.sh $D/deepgate_M2.log python3 $R/ck_deepgate_M2.py 3 80$i 300 32 $i 12
done
for i in 15 20 25 28; do
  $R/ck_run.sh $D/deepgate_M2.log python3 $R/ck_deepgate_M2.py 5 81$i 200 28 $i 8
done
