#!/bin/sh
# batch5.sh: heuristic deep-gate stress test of the lifting criterion (forced gate of depth s in W_1).
R=./run.sh
L=../../../data/round4/M4D/gate_stress.log
for s in 2 3 4 5; do for m in start mid; do
$R $L 1700 python3 lift_gate_stress.py 13 7$s 25 26 26 $s $m 8
done; done
for s in 2 3 4 5 6; do for m in start mid; do
$R $L 1700 python3 lift_gate_stress.py 11 8$s 25 22 22 $s $m 9
done; done
for s in 2 3 4; do for m in start mid; do
$R $L 1700 python3 lift_gate_stress.py 7 9$s 25 21 24 $s $m 11
done; done
