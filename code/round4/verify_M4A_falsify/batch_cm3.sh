#!/bin/sh
# Lemma Q exact tests at p = 7, 11, 13, 17, 19, 23 (one job at a time, nice -n 10 via run.sh)
cd /home/user/erdos-404-research/code/round4/verify_M4A_falsify
D=/home/user/erdos-404-research/data/round4/verify_M4A_falsify
K=rand,neg,int,d1first,dbl
./run.sh $D/cm3_lemmaQ_p7.log 1500 python3 cm3_lemmaQ.py 7 707 16 4 3 34 $K
./run.sh $D/cm3_lemmaQ_p11.log 1500 python3 cm3_lemmaQ.py 11 1111 16 3 2 40 $K
./run.sh $D/cm3_lemmaQ_p13.log 1500 python3 cm3_lemmaQ.py 13 1313 10 3 2 44 $K
./run.sh $D/cm3_lemmaQ_p17.log 1500 python3 cm3_lemmaQ.py 17 1717 5 3 2 46 $K
./run.sh $D/cm3_lemmaQ_p19.log 1500 python3 cm3_lemmaQ.py 19 1919 4 3 2 50 $K
./run.sh $D/cm3_lemmaQ_p23.log 1500 python3 cm3_lemmaQ.py 23 2323 3 3 2 56 $K
