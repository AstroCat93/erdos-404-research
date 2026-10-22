#!/bin/sh
# Reproduce every log of the obstruction/scope check of track M4C (about 4 core-minutes in total, nice -n 10).
# Run from the repository root.  Logs go to data/round4/verify_C_obstruction/ (each with ### command/start/wall lines).
set -e
D=code/round4/verify_C_obstruction
L=data/round4/verify_C_obstruction
run() {  # run <log> <command...>
  log=$1; shift
  { echo "### command: $*"; echo "### start: $(date -u +%FT%TZ)"; s=$(date +%s); "$@"; echo "### wall: $(( $(date +%s)-s )) s"; } > "$log" 2>&1
}
run $L/qfourier.log nice -n 10 python3 $D/qfourier.py 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
run $L/propW_check.log nice -n 10 python3 $D/propW_check.py 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
run $L/context_checks.log nice -n 10 python3 $D/context_checks.py $L/qfourier.log
grep "^p=" $L/qfourier.log | sed -E 's/p= *([0-9]+) wilson=[01] q1-1=([^ ]+) q2-1=([^ ]+) q3-1=([^ ]+).*/\1 \2 \3 \4/' | awk '$1>=11' > /tmp/r4_verify_C_obstruction_qvals.txt
{ echo "### command: reassemble.py p q1-1 q2-1 q3-1 1 for the 21 primes 11..97 (q-values from qfourier.log)"; echo "### start: $(date -u +%FT%TZ)"; s=$(date +%s)
  while read p a b c; do nice -n 10 python3 $D/reassemble.py $p $a $b $c 1; done < /tmp/r4_verify_C_obstruction_qvals.txt
  echo "### wall: $(( $(date +%s)-s )) s"; } > $L/reassemble.log 2>&1
{ for args in "11 1.436234e-03 1.115961e-01 3000000 3 4 5 7 9 11 15 21" "13 2.202392e-05 8.124352e-03 6000000 3 4 5 7 9 12 15 21" "7 1.428223e-02 1.125488e-01 6000000 3 4 5 7 9 12 15 21"; do
    echo "### command: nice -n 10 python3 $D/phase1_pointwise.py $args"; echo "### start: $(date -u +%FT%TZ)"; s=$(date +%s)
    nice -n 10 python3 $D/phase1_pointwise.py $args; echo "### wall: $(( $(date +%s)-s )) s"; done; } > $L/phase1_pointwise.log 2>&1
# scope_p7.log: reassemble.py at p=7 stops with "T2 fails at l=11" (N_W = 4), see the log.
run $L/compare_logs.log python3 $D/compare_logs.py data/round4/M4C/assemble.log $L/reassemble.log
