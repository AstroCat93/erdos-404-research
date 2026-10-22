#!/bin/sh
# exact global finite-horizon tests of Theorem B1/B1' (one log per configuration)
D=/home/user/erdos-404-research/data/round4/verify_M4B_falsify
cd /home/user/erdos-404-research/code/round4/verify_M4B_falsify
./run.sh $D/t5_p7_14_21_lin.log    python3 t5_global.py 7 14 21 lin 8 3 1/5
./run.sh $D/t5_p7_14_21_ladder.log python3 t5_global.py 7 14 21 ladder 14 3 1/5
./run.sh $D/t5_p7_14_21_hash.log   python3 t5_global.py 7 14 21 hash 9 3 1
./run.sh $D/t5_p7_14_17_lin.log    python3 t5_global.py 7 14 17 lin 8 3 1/20
./run.sh $D/t5_p7_15_22_lin.log    python3 t5_global.py 7 15 22 lin 9 3 1/10
./run.sh $D/t5_p5_10_15_lin.log    python3 t5_global.py 5 10 15 lin 7 3 1/5
./run.sh $D/t5_p5_10_15_hash.log   python3 t5_global.py 5 10 15 hash 7 3 1
./run.sh $D/t5_p5_12_17_ladder.log python3 t5_global.py 5 12 17 ladder 10 3 1/2
./run.sh $D/t5_p3_6_9_lin.log      python3 t5_global.py 3 6 9 lin 5 3 1/2
./run.sh $D/t5_p3_8_11_hash.log    python3 t5_global.py 3 8 11 hash 4 3 1
./run.sh $D/t5_p7_14_21_ladder_L4.log python3 t5_global.py 7 14 21 ladder 14 4 1/5
./run.sh $D/t5_p5_10_15_lin_L5.log    python3 t5_global.py 5 10 15 lin 7 5 1/5
./run.sh $D/t5_p7_14_21_lin_L4.log    python3 t5_global.py 7 14 21 lin 8 4 1/5
