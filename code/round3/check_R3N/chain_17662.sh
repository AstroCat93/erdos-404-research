#!/bin/bash
# check_R3N: independent upper-bound check of dfsW4's EXACT f(17662,2) = 221465 with program D at
# K = 221466, split into sequential jobs (each <= 1790 s wall) over the subtrees at window L = 120.
B=/tmp/r3_check_R3N/dfsD
L=/home/user/erdos-404-research/data/round3/check_R3N/D_17662_K221466_chain.log
echo "# cmd: bash code/round3/check_R3N/chain_17662.sh : jobs 'timeout 1790 nice -n 10 $B 17662 221466 -p 120 START inf 1000' with START = previous NEXT ($(date -u +%FT%TZ))" > $L
start=0; job=0
while :; do
  job=$((job+1))
  echo "## job $job: START=$start ($(date -u +%FT%TZ))" >> $L
  s=$(date +%s)
  out=$(timeout 1790 nice -n 10 $B 17662 221466 -p 120 $start inf 1000 2>&1); rc=$?
  echo "$out" | grep -v '^\[' >> $L
  echo "## job $job exit=$rc wall=$(( $(date +%s) - s )) s" >> $L
  if [ $rc -ne 0 ]; then echo "## CHAIN ABORTED (exit $rc)" >> $L; break; fi
  nxt=$(echo "$out" | sed -n 's/^STOPPED by time limit: NEXT=\([0-9]*\).*/\1/p')
  if [ -z "$nxt" ]; then echo "## CHAIN COMPLETE" >> $L; break; fi
  start=$nxt
done
