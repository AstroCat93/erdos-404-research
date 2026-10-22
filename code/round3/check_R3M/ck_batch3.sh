#!/bin/sh
# ck_batch3.sh -- second checker instance: completes the exact batch of ck_batch1.sh that was cut off
# (C1C2 at p=7 with a smaller precision cap, the NEG control, Lemma C5, Prop N3, Lemma C4).
# Run from the repository root.  One process at a time, under nice (ck_run.sh).
R=code/round3/check_R3M
D=data/round3/check_R3M
$R/ck_run2.sh $D/C1C2.log 900 python3 $R/ck_C1C2.py 7 314 4 21 7 7 0 2000 3
$R/ck_run2.sh $D/C1C2.log 900 python3 $R/ck_C1C2.py 3 305 10 16 6 6 1
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 3 401 30 10 5 5
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 3 402 20 16 6 6
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 3 403 10 24 8 8
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 5 404 20 12 6 6
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 5 405 10 20 10 10
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 7 406 20 14 8 8
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C5 11 407 10 22 11 11
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py N3 3 501 8 8
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py N3 5 502 8 8
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py N3 7 503 6 9
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C4 3 601 400 60 1.25
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C4 5 602 400 60 1.25
$R/ck_run2.sh $D/C5_N3_C4.log 900 python3 $R/ck_C5_N3_C4.py C4 7 603 400 80 1.3
