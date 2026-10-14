#!/bin/sh
D=/home/user/erdos-404-research/data/round4/verify_M4B_falsify
cd /home/user/erdos-404-research/code/round4/verify_M4B_falsify
./run.sh $D/t6_p7_lin_j1.log    python3 t6_atom_j.py 21 7 14 21 lin 8 1 4 1/5 40
./run.sh $D/t6_p7_ladder_j2.log python3 t6_atom_j.py 22 7 14 21 ladder 14 2 5 1/5 30
./run.sh $D/t6_p7_hash_j1.log   python3 t6_atom_j.py 23 7 16 23 hash 9 1 4 1 30
./run.sh $D/t6_p5_lin_j1.log    python3 t6_atom_j.py 24 5 10 15 lin 7 1 4 1/5 40
./run.sh $D/t6_p3_lin_j1.log    python3 t6_atom_j.py 25 3 6 9 lin 5 1 4 1/2 30
