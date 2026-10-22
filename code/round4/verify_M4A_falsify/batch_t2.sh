#!/bin/sh
# Lemma H, window chain (Thm 1 / Lemma F / Props D,E), E' >= E, deep Lemma Q.  One log per configuration.
D=/home/user/erdos-404-research/data/round4/verify_M4A_falsify
cd /home/user/erdos-404-research/code/round4/verify_M4A_falsify
./run.sh $D/t1_p3_d1run.log 1500 python3 t1_lemmaQ.py 3 15 80 d1run 7 5 40
./run.sh $D/t2a_p3.log 600 python3 t2a_lemmaH.py 3 101 3000
./run.sh $D/t2a_p5.log 600 python3 t2a_lemmaH.py 5 102 2000
./run.sh $D/t2a_p7.log 600 python3 t2a_lemmaH.py 7 103 1000
./run.sh $D/t2b_p3_rand.log 900 python3 t2b_chain.py 3 201 60 rand 8 81 177147
./run.sh $D/t2b_p3_deep.log 900 python3 t2b_chain.py 3 202 60 deep 9 81 177147
./run.sh $D/t2b_p3_int.log  900 python3 t2b_chain.py 3 203 40 int 8 81 177147
./run.sh $D/t2b_p5_rand.log 900 python3 t2b_chain.py 5 204 30 rand 6 25 78125
./run.sh $D/t2b_p5_deep.log 900 python3 t2b_chain.py 5 205 30 deep 7 25 78125
./run.sh $D/t2b_p7_rand.log 900 python3 t2b_chain.py 7 206 15 rand 5 49 117649
./run.sh $D/t2b_p7_deep.log 900 python3 t2b_chain.py 7 207 15 deep 6 49 117649
./run.sh $D/t4_p7.log  900 python3 t4_eprime.py 7 301 400 20 3000 12
./run.sh $D/t4_p5.log  900 python3 t4_eprime.py 5 302 200 12 2000 10
./run.sh $D/t4_p3.log  900 python3 t4_eprime.py 3 303 200 8 1500 10
./run.sh $D/t4_p11.log 900 python3 t4_eprime.py 11 304 100 30 3000 8
./run.sh $D/t1_p3_deepQ.log 1200 python3 t1_lemmaQ.py 3 401 6 d1run 9 5 45
./run.sh $D/t1_p5_deepQ.log 1200 python3 t1_lemmaQ.py 5 402 6 d1run 5 4 45
./run.sh $D/t5_atom_lowscale.log 1200 python3 t5_atom_lowscale.py /home/user/erdos-404-research/data/round4/M4A/atom_p7.txt 8 6 3 501
./run.sh $D/t3_atom_fe.log 1200 python3 t3_atom_fe.py /home/user/erdos-404-research/data/round4/M4A/atom_p7.txt 8 16 20 2000
./run.sh $D/t6_p7.log  900 python3 t6_deep_algebra.py 7 601 20 800
./run.sh $D/t6_p5.log  900 python3 t6_deep_algebra.py 5 602 20 600
./run.sh $D/t6_p3.log  900 python3 t6_deep_algebra.py 3 603 20 400
./run.sh $D/t6_p11.log 900 python3 t6_deep_algebra.py 11 604 10 1000
