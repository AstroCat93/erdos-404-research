#!/bin/sh
# batch4.sh: heuristic Monte Carlo scans of the lifting hypothesis (Theorem F) along window chains.
R=./run.sh
C=../../../data/round4/M4D/cw5.log
$R $C 900 python3 cw5_check.py 3 51 20 12 10 6 6
$R $C 900 python3 cw5_check.py 5 52 20 15 10 8 6
$R $C 900 python3 cw5_check.py 7 53 20 14 11 7 6
$R $C 900 python3 cw5_check.py 11 54 12 22 11 11 6
L=../../../data/round4/M4D/lift_scan.log
$R $L 1750 python3 lift_scan.py 13 41 800 26 26 3 5 7 5
$R $L 1750 python3 lift_scan.py 11 42 300 22 22 3 5 7 5
$R $L 1750 python3 lift_scan.py 7 43 150 21 24 2 4 10 7
$R $L 1750 python3 lift_scan.py 5 44 150 20 20 2 4 13 9
$R $L 1750 python3 lift_scan.py 3 45 150 12 16 2 4 18 12
$R $L 1750 python3 lift_scan.py 7 46 40 21 33 0 3 11 0
