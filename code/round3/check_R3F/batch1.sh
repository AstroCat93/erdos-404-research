#!/bin/sh
# batch 1: tail shells of note 10.4.1 / R3F (e), all levels; then gate shells (R3F A5) and factorial-measure shells (R3F B4-data)
D=/home/user/erdos-404-research/data/round3/check_R3F
C=/home/user/erdos-404-research/code/round3/check_R3F
R=$C/run_logged.sh
$R $D/e_tail_p13_k1-7.log sh -c "for k in 1 2 3 4 5 6 7; do python3 -I $C/shells.py tail 13 13 \$k; done"
$R $D/e_tail_p11_k1-8.log sh -c "for k in 1 2 3 4 5 6 7 8; do python3 -I $C/shells.py tail 11 11 \$k; done"
$R $D/a_gate_p5_d1-10.log sh -c "for k in 1 2 3 4 5 6 7 8 9 10; do python3 -I $C/shells.py gate 5 \$k; done"
$R $D/a_gate_p7_d1-9.log sh -c "for k in 1 2 3 4 5 6 7 8 9; do python3 -I $C/shells.py gate 7 \$k; done"
$R $D/b4_fact_p7_d1-9.log sh -c "for k in 1 2 3 4 5 6 7 8 9; do python3 -I $C/shells.py fact 7 \$k; done"
$R $D/b4_fact_p11_d1-7.log sh -c "for k in 1 2 3 4 5 6 7; do python3 -I $C/shells.py fact 11 \$k; done"
$R $D/b4_fact_p13_d1-7.log sh -c "for k in 1 2 3 4 5 6 7; do python3 -I $C/shells.py fact 13 \$k; done"
$R $D/a_gate_p11_d1-9.log sh -c "for k in 1 2 3 4 5 6 7 8 9; do python3 -I $C/shells.py gate 11 \$k; done"
$R $D/a_gate_p13_d1-8.log sh -c "for k in 1 2 3 4 5 6 7 8; do python3 -I $C/shells.py gate 13 \$k; done"
$R $D/a_gate_p13_d9.log python3 -I $C/shells.py gate 13 9 --chunks 6
