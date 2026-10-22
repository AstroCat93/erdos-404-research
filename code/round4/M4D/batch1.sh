#!/bin/sh
# batch1.sh: exact tests of Lemma L (lifting lemma) at p = 3, 5, 7, 11, plus negative controls.
L=../../../data/round4/M4D/lift_lemma.log
R=./run.sh
$R $L 1500 python3 lift_lemma_check.py 3 11 12 12 12 6 150
$R $L 1500 python3 lift_lemma_check.py 3 12 8 18 12 8 150
$R $L 1500 python3 lift_lemma_check.py 5 13 12 15 12 8 150
$R $L 1500 python3 lift_lemma_check.py 5 14 8 20 13 10 150
$R $L 1500 python3 lift_lemma_check.py 7 15 12 14 12 8 150
$R $L 1500 python3 lift_lemma_check.py 7 16 8 21 14 10 100
$R $L 1500 python3 lift_lemma_check.py 11 17 10 22 14 12 100
$R $L 1500 python3 lift_lemma_check.py 11 18 6 33 14 13 60
$R $L 1500 python3 lift_lemma_check.py 5 13 6 15 12 8 150 1
$R $L 1500 python3 lift_lemma_check.py 7 15 6 14 12 8 150 1
