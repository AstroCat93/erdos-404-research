#!/bin/bash
R=/home/user/erdos-404-research/code/round4/verify_D_P_recompute/run.sh
$R cov_p13_t7.log /tmp/r4_verify_D_P_recompute/covfib 13 7 39 2 all
/home/user/erdos-404-research/code/round4/verify_D_P_recompute/thmP_batch.sh
echo BATCH2_DONE >> /home/user/erdos-404-research/data/round4/verify_D_P_recompute/cov_p13_t7.log
