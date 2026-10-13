#!/bin/bash
cd /home/user/erdos-404-research
R=code/round3/R3C/run.sh
B=/tmp/r3_R3C/bin
# HOLD-band tests above the minimum at p=31 (cheap)
$R data/round3/R3C/scanall_p31_t2.log env R3C_BIN=$B python3 code/round3/R3C/scan_r3.py 31 2 14 16 --all
$R data/round3/R3C/scanall_p31_t3.log env R3C_BIN=$B python3 code/round3/R3C/scan_r3.py 31 3 19 21 --all
$R data/round3/R3C/scanall_p31_t4.log env R3C_BIN=$B python3 code/round3/R3C/scan_r3.py 31 4 25 27 --all
$R data/round3/R3C/scanall_p31_t5.log env R3C_BIN=$B python3 code/round3/R3C/scan_r3.py 31 5 30 39 --all
# third program (D) on the uniform certificates of the p = 29 chain (lift 3: K = K' + 3 p^c)
$R data/round3/R3C/U29_D_t1_H7.log  $B/covfast 29 1 7 0 cls 3
$R data/round3/R3C/U29_D_t2_H13.log $B/covfast 29 2 13 0 cls 3
$R data/round3/R3C/U29_D_t3_H19.log $B/covfast 29 3 19 0 cls 3
$R data/round3/R3C/U29_D_t4_H24.log $B/covfast 29 4 24 0 cls 3
$R data/round3/R3C/U29_D_t5_H29.log $B/covfast 29 5 29 0 cls 3
$R data/round3/R3C/U29_D_t6_H40.log $B/covfast 29 6 40 1 cls 3
echo queue2 done
