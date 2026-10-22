#!/bin/bash
# Re-check, with covchk.c, every uniform certificate Cov(p,t,H_t) cited by Theorem P
# except (13,7,39) and (17,7,43) (moduli 13^9, 17^9 too large for a plain bitset here).
R=/home/user/erdos-404-research/code/round4/verify_D_P_recompute/run.sh
X=/tmp/r4_verify_D_P_recompute/covchk
$R cov_controls.log $X 7 6 33 dump 5
$R cov_controls.log $X 7 3 18
for spec in "7 1 4" "7 2 7" "7 3 19" "7 4 26" "7 5 28" "7 6 34" \
            "11 1 5" "11 2 10" "11 3 18" "11 4 22" "11 5 30" "11 6 33" \
            "13 1 6" "13 2 10" "13 3 19" "13 4 24" "13 5 32" "13 6 35" \
            "17 1 5" "17 2 11" "17 3 16" "17 4 25" "17 5 30" "17 6 34" \
            "19 1 5" "19 2 12" "19 3 17" "19 4 27" "19 5 31" "19 6 35" \
            "23 1 7" "23 2 12" "23 3 18" "23 4 23" "23 5 33" "23 6 37"; do
  set -- $spec
  $R cov_p$1.log $X $1 $2 $3 all
done
# class invariance at the deepest level actually used: lifted representatives K'+j p^c
$R cov_lift.log $X 7 6 34 lift 3
$R cov_lift.log $X 11 6 33 lift 5
$R cov_lift.log $X 13 6 35 lift 2
echo BATCH_DONE >> /home/user/erdos-404-research/data/round4/verify_D_P_recompute/cov_controls.log
