#!/bin/sh
# Lemma Q battery (exact).  One log per configuration.
D=/home/user/erdos-404-research/data/round4/verify_M4A_falsify
cd /home/user/erdos-404-research/code/round4/verify_M4A_falsify
./run.sh $D/t1_p3_rand.log  1500 python3 t1_lemmaQ.py 3 11 200 rand 7 5 40
./run.sh $D/t1_p3_neg.log   1500 python3 t1_lemmaQ.py 3 12 200 neg 7 5 40
./run.sh $D/t1_p3_int.log   1500 python3 t1_lemmaQ.py 3 13 60 int 7 5 40
./run.sh $D/t1_p3_dbl.log   1500 python3 t1_lemmaQ.py 3 14 40 dbl 7 5 40
./run.sh $D/t1_p3_d1run.log 1500 python3 t1_lemmaQ.py 3 15 80 d1run 7 5 40
./run.sh $D/t1_p3_scan.log  1500 python3 t1_lemmaQ.py 3 16 0 scan 6 4 34 5
./run.sh $D/t1_p5_rand.log  1500 python3 t1_lemmaQ.py 5 21 80 rand 5 3 45
./run.sh $D/t1_p5_neg.log   1500 python3 t1_lemmaQ.py 5 22 80 neg 5 3 45
./run.sh $D/t1_p5_int.log   1500 python3 t1_lemmaQ.py 5 23 40 int 5 3 45
./run.sh $D/t1_p5_dbl.log   1500 python3 t1_lemmaQ.py 5 24 30 dbl 5 3 45
./run.sh $D/t1_p5_d1run.log 1500 python3 t1_lemmaQ.py 5 25 40 d1run 5 3 45
./run.sh $D/t1_p5_scan.log  1500 python3 t1_lemmaQ.py 5 26 0 scan 4 3 40 3
./run.sh $D/t1_p7_rand.log  1500 python3 t1_lemmaQ.py 7 31 80 rand 4 3 50
./run.sh $D/t1_p7_neg.log   1500 python3 t1_lemmaQ.py 7 32 80 neg 4 3 50
./run.sh $D/t1_p7_int.log   1500 python3 t1_lemmaQ.py 7 33 20 int 4 3 50
./run.sh $D/t1_p7_dbl.log   1500 python3 t1_lemmaQ.py 7 34 15 dbl 4 3 50
./run.sh $D/t1_p7_d1run.log 1500 python3 t1_lemmaQ.py 7 35 60 d1run 4 3 50
./run.sh $D/t1_p7_scan.log  1500 python3 t1_lemmaQ.py 7 36 0 scan 3 2 40 2
./run.sh $D/t1_p11_rand.log 1500 python3 t1_lemmaQ.py 11 41 12 rand 3 2 50
