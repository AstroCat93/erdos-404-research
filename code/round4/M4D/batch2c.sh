#!/bin/sh
# batch2c.sh: p=7 exact tests of Lemma W1, W2, Prop W3, Cor W4 at n=21 (the n=14 runs never meet (5.2)),
# with positive weight on a random subset of 25 slope-0 parents (other parents weight 0).
L=../../../data/round4/M4D/weighted_twowin.log
R=./run.sh
for mode in unif rand fib; do
$R $L 1700 python3 weighted_twowin_check.py 7 25 4 21 7 7 $mode 4 25
done
$R $L 1700 python3 weighted_twowin_check.py 3 26 10 20 5 4 vary 6
$R $L 1700 python3 weighted_twowin_check.py 5 27 6 20 5 5 vary 5
$R $L 1700 python3 weighted_twowin_check.py 7 28 3 21 7 7 vary 4 25
E=../../../data/round4/M4D/thmF_e2e.log
$R $E 1700 python3 thmF_e2e.py 13 61 400 13 26 3 2 6
$R $E 1700 python3 thmF_e2e.py 11 62 300 11 22 3 2 7
$R $E 1700 python3 thmF_e2e.py 7 63 300 14 14 2 2 8
$R $E 1700 python3 thmF_e2e.py 5 64 200 10 14 2 2 9
$R $E 1700 python3 thmF_e2e.py 7 65 100 14 18 2 3 9
