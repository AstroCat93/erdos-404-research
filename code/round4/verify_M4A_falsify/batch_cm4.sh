#!/bin/sh
# atom low-scale Prop D (cm4), E' >= E (cm5), Theorem 1 / Lemma F / Props D, E on balls (cm6), Lemma H (cm7)
cd /home/user/erdos-404-research/code/round4/verify_M4A_falsify
D=/home/user/erdos-404-research/data/round4/verify_M4A_falsify
A=/home/user/erdos-404-research/data/round4/M4A
for p in 11 13 17 19 23; do
  ./run.sh $D/cm4_atomlow_p$p.log 900 python3 cm4_atomlow.py $A/atom_p$p.txt 6 3 4 $p
done
for p in 3 5 7 11 13 17 19 23; do
  ./run.sh $D/cm5_eprime_p$p.log 900 python3 cm5_eprime.py $p 5$p 120 300 3000 10 10
done
./run.sh $D/cm6_thm1_p7.log 900 python3 cm6_thm1.py 7 71 40 4
./run.sh $D/cm6_thm1_p11.log 900 python3 cm6_thm1.py 11 111 30 3
./run.sh $D/cm6_thm1_p13.log 900 python3 cm6_thm1.py 13 131 20 3
for p in 7 11 13; do
  ./run.sh $D/cm7_lemmaH_p$p.log 900 python3 cm7_lemmaH.py $p 7$p 600 4
done
for p in 17 19 23; do
  ./run.sh $D/cm7_lemmaH_p$p.log 900 python3 cm7_lemmaH.py $p 7$p 600 3
done
./run.sh $D/cm8_propD_window_p7.log 900 python3 cm8_propD_window.py 7 87 60 6 4
./run.sh $D/cm8_propD_window_p11.log 900 python3 cm8_propD_window.py 11 811 50 5 4
./run.sh $D/cm8_propD_window_p13.log 900 python3 cm8_propD_window.py 13 813 40 4 4
./run.sh $D/cm8_propD_window_p17.log 900 python3 cm8_propD_window.py 17 817 40 4 4
./run.sh $D/cm8_propD_window_p19.log 900 python3 cm8_propD_window.py 19 819 30 4 4
./run.sh $D/cm8_propD_window_p23.log 900 python3 cm8_propD_window.py 23 823 30 4 4
