#!/bin/bash
# Fourth logged batch: the two p=3 jobs of batch3 again, now with resource guards in t_cyl.py (the n=26 run stopped
# on the int64 guard p^R < 2^56 of alive_all for a cylinder with a deep gate; the n=30 run ran out of memory
# in the per-xi FFT of W3 for an enumeration of 3^10 points).  Guards skip such cylinders / levels and count them.
cd "$(dirname "$0")"
LOGD=../../../data/round4/verify_D_W6_falsify
R=./run.sh
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 26 6 5 102 15 rand,gate_hist,gate_win,tight - 1 20
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 30 6 6 103 6 rand,gate_hist,tight 40 1 12
