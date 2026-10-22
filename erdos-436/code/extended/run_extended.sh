#!/usr/bin/env bash
# run_extended.sh -- the longer checks quoted in paper/note.md sections 3, 4 and 6 that verify.sh does
# not run.  None of them is needed for the proof; they test the checkers and the model.
#
#   E1  a separately written branching program (code/upper/tree8.c) gives the certificate's node counts;
#   E2  tamper tests: 35 invalid mutations of the k = 8 stream must be rejected by both checkers that
#       were written from FORMAT.md alone, one valid alternative must be accepted, and on 7955 single-line
#       mutants of the k = 2..5 certificates three checkers must agree;
#   E3  end-to-end test on real primes: 2126 primes p = 1 mod 8 (2000 random up to 1e40, and every
#       p < 5e8 with r(8,2,p) >= 650): walk the tree with R_p and confirm the leaf by modular arithmetic;
#   E4  negative controls at L = Lambda(k,2) - 1 for k = 2..8: a full assignment of all primes <= L+1
#       with no zero pair (so no tree closes at L - 1), and the depth-capped k = 8 trees;
#   E5  (H3) with a third, separately written program;
#   E6  R* is reproduced from the SAT assignment by the greedy simplifier; facts about the vectors;
#       the model reproduces the bound 1200744 of [BLL64, Table V];
#   E7  (needs numpy) the empirical test of Remark 6.1 on the 1.27e7 primes p = 1 mod 8 below 1e9.
#
# Usage: bash code/extended/run_extended.sh      (from anywhere; uses build/ at the repository root)
# One core, about 15 minutes, up to 2 GB of memory and 400 MB of temporary disk in build/work.
set -uo pipefail
cd "$(dirname "$0")/../.."
B=build; LOG=$B/logs/extended; BIN=$B/bin; WK=$B/work
mkdir -p "$LOG" "$BIN" "$WK"
NICE=${NICE:-nice -n 10}
NPASS=0; NFAIL=0; FAILED=()
T_START=$EPOCHREALTIME
elapsed() { awk -v a="$1" -v b="$EPOCHREALTIME" 'BEGIN { printf "%.1f", b - a }'; }
check() {      # same as in verify.sh
  local name=$1 pats=$2; shift 2
  local t0=$EPOCHREALTIME rc ok=1 pat rest=$pats miss=""
  "$@" > "$LOG/$name.log" 2>&1; rc=$?
  [ $rc -eq 0 ] || ok=0
  while :; do
    pat=${rest%%|||*}
    grep -Eq -- "$pat" "$LOG/$name.log" || { ok=0; miss+="        expected output not found: $pat"$'\n'; }
    [[ $rest == *'|||'* ]] || break
    rest=${rest#*|||}
  done
  if [ $ok = 1 ]; then NPASS=$((NPASS+1)); printf "  PASS  %-34s %7ss\n" "$name" "$(elapsed "$t0")"
  else NFAIL=$((NFAIL+1)); FAILED+=("$name"); printf "  FAIL  %-34s %7ss  (exit %s; see %s)\n%s" "$name" "$(elapsed "$t0")" "$rc" "$LOG/$name.log" "$miss"; fi
}
have_numpy() { python3 -c 'import numpy' > /dev/null 2>&1; }

echo "run_extended.sh   ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
gcc -O2 -o $BIN/pairtree code/generator/pairtree.c && gcc -O2 -std=gnu99 -o $BIN/ccheck code/upper/ccheck.c &&
gcc -O2 -o $BIN/tree8 code/upper/tree8.c && gcc -O2 -o $BIN/rscan code/extended/rscan.c &&
gcc -O2 -o $BIN/smallp_euler code/extended/smallp_euler.c && gcc -O2 -o $BIN/simplify code/lower/simplify.c &&
gcc -O2 -o $BIN/pairs code/lower/pairs.c && gcc -O2 -o $BIN/chebo code/extended/chebo.c || { echo "compilation failed"; exit 1; }

C8=certificate/k8_L1508324.cert.xz
echo "[E1] separately written branching program"
check E1_tree8_node_counts 'k=8 L=1508324 T=80 p_T=409 nodes=2000473 closed=14003308 unresolved=0' \
  $NICE $BIN/tree8 8 1508324 80

echo "[E2] tamper tests"
xz -dc $C8 > $WK/k8.raw
check E2_tamper_structural 'SUMMARY: 31/31 mutations rejected by both checkers' \
  $NICE python3 -I code/extended/tamper.py $WK/k8.raw 8 1508324 0,2,4,6 $WK code/upper/pcheck.py $BIN/ccheck
check E2_tamper_semantic 'SUMMARY: 4/4 semantic mutations behaved as expected' \
  $NICE python3 -I code/extended/tamper2.py $WK/k8.raw 8 1508324 0,2,4,6 $WK code/upper/pcheck.py $BIN/ccheck
sed -e '2s/^k 8$/k 4/' -e '4s/^R2 0 2 4 6$/R2 0 2/' $WK/k8.raw > $WK/hk4.raw
check E2_tamper_header_k4 '"verdict": "REJECT"|||VERDICT REJECT' \
  bash -c "! $NICE python3 -I code/upper/pcheck.py $WK/hk4.raw --k 8 --L 1508324 --S2 0,2,4,6 && ! $NICE $BIN/ccheck 4 1508324 0,2 < $WK/hk4.raw"
rm -f $WK/hk4.raw
check E2_differential_small_certs '"mutants": 6327, "agree": 6328, "disagree": 0|||^2 \{"mutants": 56, "agree": 57, "disagree": 0|||^3 \{"mutants": 572, "agree": 573, "disagree": 0|||^5 \{"mutants": 1000, "agree": 1001, "disagree": 0' \
  $NICE python3 -I code/extended/diff_small.py certificate code/upper $BIN/ccheck $WK

echo "[E3] end-to-end test on real primes"
check E3_rscan_hard_primes 'scanned 6558874 primes p=1 mod 8 in \[1508325,500000000\); max r = 1024 at p = 217647713' \
  bash -c "$NICE $BIN/rscan 1508325 500000000 650 > $WK/hard_primes.txt"
check E3_e2e_k8 '"tests": 2126, .*"n_fails": 0' \
  $NICE python3 -I code/extended/e2e.py 8 1508324 0,2,4,6 $WK/k8.raw $BIN/ccheck $WK $WK/hard_primes.txt
rm -f $WK/k8.raw
for spec in "2 9 0,1" "4 1224 0,1,2,3"; do
  set -- $spec; xz -dc certificate/k$1_L$2.cert.xz > $WK/k$1.raw
  check E3_e2e_k$1 '"n_fails": 0' $NICE python3 -I code/extended/e2e.py $1 $2 $3 $WK/k$1.raw $BIN/ccheck $WK
  rm -f $WK/k$1.raw
done

echo "[E4] negative controls at L = Lambda(k,2) - 1"
declare -A LAM=([2]=9 [3]=77 [4]=1224 [5]=7888 [6]=202124 [7]=1649375 [8]=1508324)
declare -A PI=([2]=4 [3]=21 [4]=200 [5]=997 [6]=18159 [7]=124585 [8]=114765)   # number of primes <= Lambda(k,2)
for T in 61 62 80; do
  case $T in 80) U=5301696 ;; *) U=432 ;; esac
  check E4_k8_L1508323_capped_T$T "unresolved\(U\)=$U " $NICE $BIN/pairtree 8 1508323 --r2 even --maxdepth $T
done
for k in 2 3 4 5 6 7 8; do
  L=$((LAM[$k]-1)); ord=$(seq -s, 1 $((k-1))),0; r2=all; [ $k = 8 ] && r2=even
  check E4_k${k}_witness_search "first unresolved node at depth ${PI[$k]} " \
    $NICE $BIN/pairtree $k $L --r2 $r2 --order $ord --stop-at-first-U --witness-out $WK/k${k}_witness.txt
  check E4_k${k}_witness_least_pair "least zero pair n = ${LAM[$k]} " \
    $NICE python3 -I code/lower/check_vector.py $k $((L+1000)) $WK/k${k}_witness.txt 1
done
check E4_k8_witness_equals_bundled_file 'identical' \
  bash -c "cmp $WK/k8_witness.txt vectors/k8_L1508323_witness.txt && echo identical"

echo "[E5] (H3) with a third program"
check E5_H3_smallp_euler '^exceptional: 3 5 13 17 41 113$|||max r over non-exceptional: 552 at p=1476217' \
  $NICE $BIN/smallp_euler 1508325

echo "[E6] the vectors"
check E6_simplify_SAT_to_Rstar 'non-default entries equal vectors/vec8_compact.txt: True' \
  bash -c "$NICE $BIN/simplify -k 8 -v vectors/vec8_L1508323.txt -L 1508323 -t 1 -fix 2 -order desc -alt 2,0 -o $WK/simp8.txt &&
           python3 -I -c '
import sys
a = {int(q): int(v) for q, v in (l.split() for l in open(sys.argv[1])) if int(v) != 1}
b = {int(q): int(v) for q, v in (l.split() for l in open(sys.argv[2]) if not l.startswith(\"#\"))}
print(\"non-default entries equal vectors/vec8_compact.txt:\", a == b)
sys.exit(0 if a == b else 1)' $WK/simp8.txt vectors/vec8_compact.txt"
check E6_vector_facts 'R\* agrees at 24 of them|||#primes where 1\*SAT != witness: 23776|||stabiliser of R\* in \(Z/8\)\^\*: \[1\]' \
  python3 -I code/lower/vecfacts.py .
check E6_BLL64_TableV_vector_gives_1200744 '^FIRST_PAIR n=1200744 n\+1=1200745$' \
  $NICE $BIN/pairs -k 8 -v vectors/bll_k8_tableV.txt -N 1300000 -d 1

echo "[E7] empirical Chebotarev test (Remark 6.1)"
if have_numpy; then
  check E7_chebo_k8_m8_1e9 'primes_used=12711219 discrete_log_failures=0 non_primitive_g_u=0' \
    $NICE $BIN/chebo 8 8 1000000000 $WK/k8m8
  check E7_chebo_analyse 'R\(2\) odd \(least g\): 0|||^\[m=7\] .*allowed vectors never realised=0 ' \
    $NICE python3 -I code/extended/chebo_analyse.py 8 8 $WK/k8m8 1
  rm -f $WK/k8m8.least $WK/k8m8.real
else
  echo "  SKIP  E7 (numpy not installed)"
fi

echo "extended summary: $NPASS passed, $NFAIL failed, total $(elapsed "$T_START") s"
if [ $NFAIL -gt 0 ]; then printf '  failed: %s\n' "${FAILED[@]}"; exit 1; fi
echo "ALL EXTENDED CHECKS PASSED"
