#!/bin/sh
D=/home/user/erdos-404-research/data/round3/check_R3F
C=/home/user/erdos-404-research/code/round3/check_R3F
R=$C/run_logged.sh
rm -f $D/b3_l2_*.log
$R $D/b3_l2_p3_N3.log python3 -I $C/b3check.py 3 3 15
$R $D/b3_l2_p3_N0.log python3 -I $C/b3check.py 3 0 14
$R $D/b3_l2_p5_N5.log python3 -I $C/b3check.py 5 5 9
$R $D/b3_l2_p5_N0.log python3 -I $C/b3check.py 5 0 9
$R $D/b3_l2_p7_N7.log python3 -I $C/b3check.py 7 7 8
$R $D/b3_l2_p11_N11.log python3 -I $C/b3check.py 11 11 5
$R $D/b3_l2_p13_N13.log python3 -I $C/b3check.py 13 13 4
