#!/bin/sh
D=/home/user/erdos-404-research/data/round3/check_R3F
C=/home/user/erdos-404-research/code/round3/check_R3F
R=$C/run_logged.sh
$R $D/a1_a2_a3_exact.log python3 -I $C/a2check.py
$R $D/ident_poisson_b7_b8.log python3 -I $C/identcheck.py
$R $D/b2_budgets.log python3 -I $C/budgetcheck.py
$R $D/b4_cover_direct.log python3 -I $C/covercheck.py 7 9 11 7 13 7
$R $D/c4_kavg.log python3 -I $C/kavgcheck.py 7 2 7  7 2 12  7 2 14  7 2 20  7 2 21  7 3 19  7 3 21  11 3 18  13 2 10  13 2 19  13 2 26  13 2 30  13 2 35  13 2 39  13 3 19  13 3 26  13 3 30  13 3 35  13 3 39  13 4 24
$R $D/b3_l2_p3_N3.log python3 -I $C/b3check.py 3 3 15
$R $D/b3_l2_p3_N0.log python3 -I $C/b3check.py 3 0 14
$R $D/b3_l2_p5_N5.log python3 -I $C/b3check.py 5 5 9
$R $D/b3_l2_p5_N0.log python3 -I $C/b3check.py 5 0 9
$R $D/b3_l2_p7_N7.log python3 -I $C/b3check.py 7 7 8
$R $D/b3_l2_p13_N13.log python3 -I $C/b3check.py 13 13 5
