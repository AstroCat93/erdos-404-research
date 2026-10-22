#!/bin/sh
# batch2.sh: exact tests of Lemma W1, Lemma W2, Prop W3, Cor W4 (weighted window identities) at p = 3, 5, 7.
L=../../../data/round4/M4D/weighted_twowin.log
R=./run.sh
for mode in unif rand fib; do
$R $L 1700 python3 weighted_twowin_check.py 3 21 10 20 5 4 $mode 6
$R $L 1700 python3 weighted_twowin_check.py 3 22 6 26 6 5 $mode 7
$R $L 1700 python3 weighted_twowin_check.py 5 23 6 20 5 5 $mode 5
$R $L 1700 python3 weighted_twowin_check.py 7 24 4 21 7 7 $mode 4
done
