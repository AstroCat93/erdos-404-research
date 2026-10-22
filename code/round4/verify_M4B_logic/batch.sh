#!/bin/sh
# batch.sh: production runs of the logic check of M4B Theorem B1/B1' (one job at a time, nice -n 10).
D=/home/user/erdos-404-research/data/round4/verify_M4B_logic
cd /home/user/erdos-404-research/code/round4/verify_M4B_logic
R=./runlog.sh
# t3: exact finite-horizon chain (global and per atom)
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 3 12 15 hash 1/4 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 3 12 15 ladder 1/4 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 3 12 15 hash 1/10 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 3 12 15 hash 1/4 3 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 3 12 15 ladder 1/10 3 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 5 15 20 hash 1/4 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 5 15 20 ladder 1/4 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 5 15 20 hash 1/100 2 0
$R $D/t3_global_finite.log 1500 python3 t3_global_finite.py 7 21 28 ladder 1/4 2 4
# t4: the Q_j bound
$R $D/t4_Qbound.log 600 python3 t4_Qbound.py 3 5 300 12,18,24,30
$R $D/t4_Qbound.log 600 python3 t4_Qbound.py 5 6 200 15,20,25
$R $D/t4_Qbound.log 600 python3 t4_Qbound.py 7 7 100 21,28
# t2: exact martingale / C2 on atoms with random times; one-step controls
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 3 21 80 6 9 5 hash 6
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 3 22 80 6 9 5 ladder 6
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 3 23 150 6 9 5 ladder 7 4000 8
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 5 24 12 15 20 4 hash 4 300
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 5 25 10 15 20 4 ladder 4 300
$R $D/t2_atom_c2.log 1500 python3 t2_atom_c2.py 7 26 4 21 28 3 ladder 3 0 4
