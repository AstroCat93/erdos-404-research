#!/bin/sh
# ck_batch4.sh -- second check_R3M instance: new exact tests (equality and boundary cases, Lemma 1-2,
# structure of Theorem C3, Lemma C4) and the p=7 two-window run.  Run from the repository root.
R=code/round3/check_R3M
D=data/round3/check_R3M
T=600
$R/ck_run2.sh $D/lemma12.log $T python3 $R/ck_lemma12.py 3 1101 60 40
$R/ck_run2.sh $D/lemma12.log $T python3 $R/ck_lemma12.py 5 1102 60 40
$R/ck_run2.sh $D/lemma12.log $T python3 $R/ck_lemma12.py 7 1103 60 40
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1201 10 20 4 4 in 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1202 6 26 5 5 in 3 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1203 6 18 4 4 edge 4 7
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1204 6 12 4 4 out 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 3 1205 6 12 4 4 s-3 4 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 5 1206 5 20 5 5 in 3 5
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py C2eq 7 1207 3 21 7 7 in 2 3
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 3 1301 5 20 26 1 w2edge 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 3 1302 5 20 26 1 w3edge 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 3 1303 5 24 33 2 w2edge 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 3 1304 5 20 26 1 w2out 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 3 1305 5 20 26 1 w3out 6
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 5 1306 3 30 40 1 w2edge 4
$R/ck_run2.sh $D/edge.log $T python3 $R/ck_edge.py Aedge 7 1307 2 28 42 1 w2edge 3
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py part 3 1401 200 80
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py part 5 1402 200 80
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py part 7 1403 200 100
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py F1 3 1411 40 300 18
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py F1 5 1412 40 300 22
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py F1 7 1413 40 300 28
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py meas 3 1421 60 8 1.25 8
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py meas 5 1422 60 10 1.25 5
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py meas 7 1423 60 14 1.25 4
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py C4 3 1431 300 30 1.25 8 100
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py C4 3 1432 200 80 1.25 10 400
$R/ck_run2.sh $D/C3struct.log $T python3 $R/ck_C3_struct.py C4 3 1433 200 80 1.25 10 400 7
$R/ck_run2.sh $D/C1C2.log $T python3 $R/ck_C1C2.py 7 324 3 21 7 7 0 300 2
