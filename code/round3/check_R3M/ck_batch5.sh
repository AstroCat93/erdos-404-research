#!/bin/sh
# ck_batch5.sh -- second check_R3M instance: boundary runs of C2 outside (5.2), Observation G
# (deep gates and the classes x = -1, -2 mod p kill the slope-0 population), and the heuristic probes
# of section 7.1 (independent Monte Carlo of M^0_n; importance sampling of gate contributions).
R=code/round3/check_R3M
D=data/round3/check_R3M
T=600
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 9003 4 14 4 4 out 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 9005 4 12 4 4 s-2 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 9005 4 12 4 4 s-4 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1501 4 16 4 4 edge 4 8
$R/ck_run2.sh $D/gatekill.log $T python3 $R/ck_gate_kill.py 3 1601 300 24
$R/ck_run2.sh $D/gatekill.log $T python3 $R/ck_gate_kill.py 5 1602 200 24
$R/ck_run2.sh $D/gatekill.log $T python3 $R/ck_gate_kill.py 7 1603 100 24
$R/ck_run2.sh $D/mc_M.log $T python3 $R/ck_mc_M.py 3 701 4000 8,16,24,32
for i in 9 12 18 24; do
  $R/ck_run2.sh $D/deepgate_M2.log 300 python3 $R/ck_deepgate_M2.py 3 80$i 30 24 $i 12
done
