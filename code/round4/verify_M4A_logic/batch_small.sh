#!/bin/bash
# batch of exact small-case tests (verify_M4A_logic); logs in data/round4/verify_M4A_logic/
D=/home/user/erdos-404-research/code/round4/verify_M4A_logic
L=/home/user/erdos-404-research/data/round4/verify_M4A_logic
cd $D
R=$D/runlog.sh
$R $L/lemmaQ.log 900 python3 test_small.py Q 3 11 3000 8 3
$R $L/lemmaQ.log 900 python3 test_small.py Q 5 12 3000 5 2
$R $L/lemmaQ.log 900 python3 test_small.py Q 7 13 3000 4 2
$R $L/lemmaQ.log 900 python3 test_small.py Q 3 21 1500 8 3 1
$R $L/lemmaQ.log 900 python3 test_small.py Q 5 22 1500 5 2 1
$R $L/lemmaQ.log 900 python3 test_small.py Q 7 23 1500 4 2 1
$R $L/thm1_propDE.log 900 python3 test_small.py T1 3 31 25 3 10 20 8
$R $L/thm1_propDE.log 900 python3 test_small.py T1 3 32 15 4 14 26 8
$R $L/thm1_propDE.log 900 python3 test_small.py T1 5 33 20 2 10 24 5
$R $L/thm1_propDE.log 900 python3 test_small.py T1 7 34 12 2 14 44 4
