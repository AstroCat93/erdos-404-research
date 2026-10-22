#!/bin/sh
# batch3.sh: Theorem P checks: independent re-verification of small covering certificates (bin/liftprof),
# exact first-failure simulations at p=7, and the plateau-bound arithmetic.
R=./run.sh
L=../../../data/round4/M4D/cov_verify.log
$R $L 1700 python3 cov_verify.py 7 1 4 all
$R $L 1700 python3 cov_verify.py 7 2 7 all
$R $L 1700 python3 cov_verify.py 7 3 19 all
$R $L 1700 python3 cov_verify.py 7 4 26 all
$R $L 1700 python3 cov_verify.py 7 5 28 all
$R $L 1700 python3 cov_verify.py 7 6 34 sample:120:7 5
$R $L 1700 python3 cov_verify.py 7 6 33 sample:40:8 5
$R $L 1700 python3 cov_verify.py 7 3 18 all
$R $L 1700 python3 cov_verify.py 13 1 6 all
$R $L 1700 python3 cov_verify.py 13 2 10 all
$R $L 1700 python3 cov_verify.py 13 3 19 all
$R $L 1700 python3 cov_verify.py 13 4 24 all
$R $L 1700 python3 cov_verify.py 11 4 22 all
$R $L 1700 python3 cov_verify.py 11 5 30 sample:60:9
L=../../../data/round4/M4D/plateau_check.log
$R $L 1700 python3 plateau_check.py 7 31 400 thm 50 6
$R $L 1700 python3 plateau_check.py 7 32 200 ctrl 0 0
L=../../../data/round4/M4D/plateau_bounds.log
$R $L 600 python3 plateau_bounds.py
