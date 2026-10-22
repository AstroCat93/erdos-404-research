#!/bin/sh
# ck_batch1.sh -- the exact-test batch of the check of track R3M (run from the repository root).
R=code/round3/check_R3M
D=data/round3/check_R3M
$R/ck_run.sh $D/propA.log python3 $R/ck_propA.py 3 101 25 20 26 2
$R/ck_run.sh $D/propA.log python3 $R/ck_propA.py 3 102 4 24 33 3
$R/ck_run.sh $D/propA.log python3 $R/ck_propA.py 5 103 4 30 40 2 0 40
$R/ck_run.sh $D/propA.log python3 $R/ck_propA.py 7 104 3 28 42 1 0 30
$R/ck_run.sh $D/propA.log python3 $R/ck_propA.py 3 105 10 20 26 3 1
$R/ck_run.sh $D/propB.log python3 $R/ck_propB.py 3 201 40 20 26
$R/ck_run.sh $D/propB.log python3 $R/ck_propB.py 3 202 10 30 38
$R/ck_run.sh $D/propB.log python3 $R/ck_propB.py 5 203 10 20 28
$R/ck_run.sh $D/propB.log python3 $R/ck_propB.py 7 204 6 14 22 200
$R/ck_run.sh $D/propB.log python3 $R/ck_propB.py 11 205 4 22 33 100
$R/ck_run.sh $D/C1C2.log python3 $R/ck_C1C2.py 3 301 20 20 4 4
$R/ck_run.sh $D/C1C2.log python3 $R/ck_C1C2.py 3 302 5 26 5 5
$R/ck_run.sh $D/C1C2.log python3 $R/ck_C1C2.py 5 303 5 20 5 5
$R/ck_run.sh $D/C1C2.log python3 $R/ck_C1C2.py 7 304 2 21 7 7 0 2000
$R/ck_run.sh $D/C1C2.log python3 $R/ck_C1C2.py 3 305 10 16 6 6 1
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 3 401 30 10 5 5
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 3 402 20 16 6 6
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 3 403 10 24 8 8
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 5 404 20 12 6 6
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 5 405 10 20 10 10
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 7 406 20 14 8 8
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C5 11 407 10 22 11 11
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py N3 3 501 8 8
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py N3 5 502 8 8
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py N3 7 503 6 9
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py N3 11 504 5 12
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C4 3 601 400 60 1.25
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C4 5 602 400 60 1.25
$R/ck_run.sh $D/C5_N3_C4.log python3 $R/ck_C5_N3_C4.py C4 7 603 400 80 1.3
