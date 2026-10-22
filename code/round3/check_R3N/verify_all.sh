#!/bin/bash
# check_R3N: run the own verifier verify_w.py on the track's shipped witnesses (and on the two
# later 17662 witnesses that exist only in /tmp/r3_R3N).  Sequential, nice -n 10.
R=/home/user/erdos-404-research
V=$R/code/round3/check_R3N/verify_w.py
D=$R/data/round3/R3N
L=$R/data/round3/check_R3N/verify_own.log
echo "# cmd: bash code/round3/check_R3N/verify_all.sh  ($(date -u +%FT%TZ)); verifier: python3 -I $V FILE a K" > $L
for spec in "$D/witness_594_K90394.txt.gz 594 90394" "$D/witnessB_594_K90394.txt.gz 594 90394" \
            "$D/witness_594_K66126.txt.gz 594 66126" "$D/witness_17662_K148725.txt.gz 17662 148725" \
            "$D/witness_17662_v212995.txt.gz 17662 212995" \
            "/tmp/r3_R3N/best17662_217088.txt 17662 217088" "/tmp/r3_R3N/best17662_221186.txt 17662 221186"; do
  set -- $spec
  echo "## $1 a=$2 K=$3" >> $L
  s=$(date +%s.%N); nice -n 10 python3 -I $V $1 $2 $3 >> $L 2>&1; rc=$?; e=$(date +%s.%N)
  echo "exit=$rc wall=$(echo "$e - $s" | bc)s" >> $L
done
