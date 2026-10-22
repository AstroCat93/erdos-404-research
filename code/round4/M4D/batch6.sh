#!/bin/sh
# batch6.sh: lifting scans with larger computational caps (less censoring by deep gates).
R=./run.sh
L=../../../data/round4/M4D/lift_scan.log
$R $L 1750 python3 lift_scan.py 11 47 100 22 22 3 5 9 0
$R $L 1750 python3 lift_scan.py 11 48 100 22 22 3 5 9 0
$R $L 1750 python3 lift_scan.py 13 49 200 26 26 3 5 8 0
