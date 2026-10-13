#!/bin/sh
# Re-creates the logs of data/round3/R3Q/ (except the two scans).  One core, nice 10.  Run from this directory.
D=../../../../data/round3/R3Q
run() { echo "# cmd: $*  (start $(date -u +%H:%M:%S))"; s=$(date +%s); nice -n 10 "$@"; echo "# wall $(( $(date +%s) - s )) s"; }
{ run python3 -I cert_classes.py; run python3 -I cert_classes_sympy.py
  for a in "0 3 4 1" "2 4 7 3" "6 4 11 3"; do run python3 -I ../slope_cert.py $a; done; } > $D/certificates.log 2>&1
{ run python3 -I test_elementary.py 11 1500 60
  run python3 -I test_step.py 12 600 6 48 10
  run python3 -I test_uwin.py 13 3000 8 34 6 8 gen
  run python3 -I test_uwin.py 14 4000 12 40 6 8; } > $D/lemma_tests.log 2>&1
{ run python3 -I bounds.py D 37 39 1; } > $D/scan_D3.log 2>&1
{ grep -h "^K=.*delta<=" $D/scan_D.log $D/scan_D2.log $D/scan_D3.log | sort -t= -k2 -n > /tmp/r3_R3Q/all_scan_lines.txt
  run python3 -I verify_bounds.py /tmp/r3_R3Q/all_scan_lines.txt; } > $D/verify.log 2>&1
{ run python3 -I rule.py 3072 4096 512
  run python3 -I rule.py 8192 8192 1
  run python3 -I rule.py 16384 16384 1
  run python3 -I -c "import sys; sys.path.insert(0,'.'); import rule; [print(rule.fmt_line(K)) for K in (3072, 4096, 8192)]" 
  run python3 -I rule_K0.py
  run python3 -I rule_A.py; } > $D/rule.log 2>&1
grep -h "^K=.*delta<=" $D/rule.log > /tmp/r3_R3Q/rule_lines.txt
{ run python3 -I verify_bounds.py /tmp/r3_R3Q/rule_lines.txt; } >> $D/rule.log 2>&1
