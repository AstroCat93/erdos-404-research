#!/usr/bin/env bash
# verify.sh -- re-run the computational checks behind Lambda(8,2) = 1508324 from a clean clone.
#
# Usage:  ./verify.sh [--no-regen] [--extended]
#
#   1. hashes      SHA-256 of every certificate (compressed and decompressed) and every vector,
#                  and the hashes quoted in paper/note.md section 8;
#   2. (H1)        the k = 8 certificate (and the k = 2, 4 certificates used for p != 1 mod 8)
#                  with four checkers: two written from certificate/FORMAT.md alone
#                  (code/upper/pcheck.py, code/upper/ccheck.c), a third written from FORMAT.md
#                  (code/upper/rcheck.c) and the checker written with the generator
#                  (code/upper/check_cert.py); k = 3, 5, 6, 7 with the two C checkers;
#      (H3)        r(8,2,p) for all primes 3 <= p <= 1508325 with two programs;
#   3. (H2)        the least zero pair of R* (vectors/vec8_compact.txt) with five programs, the
#                  two full 114765-prime assignments, the "every exception is needed" test, and
#                  the k = 9 vector of note section 7 with three programs;
#   4. regeneration (skip with --no-regen): the generator code/generator/pairtree.c and the
#                  separately written canonical regenerator code/upper/regen.c rebuild every
#                  certificate stream, whose SHA-256 must equal certificate/SHA256SUMS.decompressed.
#   --extended     afterwards runs code/extended/run_extended.sh (tamper tests, end-to-end test on
#                  real primes, negative controls; about 15 more minutes).
#
# Needs: bash, gcc, python3 (standard library), xz, sha256sum.  numpy is optional (one extra
# lower-bound checker).  One core, about 1 GB of memory, about 3 minutes in total.
# Compiled programs and logs go to build/ (git-ignored).  Exit status 0 iff every check passed.
set -uo pipefail
cd "$(dirname "$0")"
ROOT=$PWD
B=build; LOG=$B/logs; BIN=$B/bin
mkdir -p "$LOG" "$BIN"
NICE=${NICE:-nice -n 10}
REGEN=1; EXTENDED=0
for a in "$@"; do
  case "$a" in
    --no-regen) REGEN=0 ;;
    --extended) EXTENDED=1 ;;
    -h|--help) sed -n '2,26p' "$0"; exit 0 ;;
    *) echo "unknown option $a"; exit 2 ;;
  esac
done

NPASS=0; NFAIL=0; FAILED=()
T_START=$EPOCHREALTIME
elapsed() { awk -v a="$1" -v b="$EPOCHREALTIME" 'BEGIN { printf "%.1f", b - a }'; }
# check NAME 'REGEX1|||REGEX2...' CMD...   run CMD (stdout+stderr to build/logs/NAME.log);
# PASS iff it exits 0 and every REGEX matches some line of the log.
check() {
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

echo "verify.sh: Lambda(8,2) = 1508324   ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
echo "tools: $(gcc --version | head -1); $(python3 --version 2>&1); $(xz --version | head -1)$(have_numpy && echo "; numpy $(python3 -c 'import numpy; print(numpy.__version__)')")"

# ---------------------------------------------------------------------------------------------
echo "[0] compile"
CC="gcc -O2"
t0=$EPOCHREALTIME
$CC -o $BIN/pairtree  code/generator/pairtree.c                 2> $LOG/compile.log &&
$CC -std=gnu99 -o $BIN/ccheck code/upper/ccheck.c                2>> $LOG/compile.log &&
$CC -o $BIN/rcheck    code/upper/rcheck.c                        2>> $LOG/compile.log &&
$CC -o $BIN/regen     code/upper/regen.c                         2>> $LOG/compile.log &&
$CC -o $BIN/smallp    code/upper/smallp.c                        2>> $LOG/compile.log &&
$CC -o $BIN/smallp_ref code/upper/smallp_ref.c                   2>> $LOG/compile.log &&
$CC -o $BIN/pairs     code/lower/pairs.c                         2>> $LOG/compile.log &&
$CC -o $BIN/fp_seg    code/lower/fp_seg.c                        2>> $LOG/compile.log &&
$CC -o $BIN/lbcheck   code/lower/lbcheck.c                       2>> $LOG/compile.log
if [ $? -ne 0 ]; then echo "  FAIL  compilation (see $LOG/compile.log)"; exit 1; fi
printf "  PASS  %-34s %7ss\n" "compile 9 C programs" "$(elapsed "$t0")"

# ---------------------------------------------------------------------------------------------
echo "[1] hashes"
check hash_certificates_xz 'k8_L1508324.cert.xz: OK' \
  bash -c 'cd certificate && sha256sum -c SHA256SUMS'
check hash_certificates_decompressed '^k8_L1508324.cert: OK$|||^k2_L9.cert: OK$|||^k4_L1224.cert: OK$' \
  bash -c 'cd certificate && rc=0; while read -r h f; do g=$(xz -dc "$f.xz" | sha256sum | cut -d" " -f1);
           if [ "$g" = "$h" ]; then echo "$f: OK"; else echo "$f: FAILED ($g)"; rc=1; fi; done < SHA256SUMS.decompressed; exit $rc'
check hash_vectors 'vec8_compact.txt: OK|||vec9_compact18_146290624.txt: OK' \
  bash -c 'cd vectors && sha256sum -c SHA256SUMS'
check hash_table_of_note 'all [0-9]+ hashes quoted in paper/note.md section 8 are in the SHA256SUMS files' \
  python3 -I -c '
import re, sys
note = open("paper/note.md").read()
sec = note[note.index("## 8."):note.index("## 9.")]
quoted = re.findall(r"`([0-9a-f]{64})`", sec)
known = set()
for f in ("certificate/SHA256SUMS", "certificate/SHA256SUMS.decompressed", "vectors/SHA256SUMS"):
    known |= {l.split()[0] for l in open(f) if l.strip()}
bad = [h for h in quoted if h not in known]
print("quoted:", len(quoted), "not found:", bad)
if bad or not quoted: sys.exit(1)
print(f"all {len(quoted)} hashes quoted in paper/note.md section 8 are in the SHA256SUMS files")'

# ---------------------------------------------------------------------------------------------
echo "[2] upper bound: certificates (H1) and small primes (H3)"
declare -A LAM=([2]=9 [3]=77 [4]=1224 [5]=7888 [6]=202124 [7]=1649375 [8]=1508324)
s2_of() { if [ "$1" = 8 ]; then echo 0,2,4,6; else seq -s, 0 $(($1-1)); fi; }
for k in 8 2 4; do
  L=${LAM[$k]}; S2=$(s2_of $k); f=certificate/k${k}_L${L}.cert.xz
  h=$(grep " k${k}_L${L}.cert\$" certificate/SHA256SUMS.decompressed | cut -d' ' -f1)
  pyS2=$(echo "$S2" | sed 's/,/, /g')
  check k${k}_check_cert.py "^parsed: k=$k L=$L R2=\[$pyS2\] .* U-leaves=0|||^SHA-256 of the decompressed stream: $h\$|||^VERIFIED: " \
    $NICE python3 -I code/upper/check_cert.py $f
  check k${k}_pcheck.py '"verdict": "PROOF"' \
    $NICE python3 -I code/upper/pcheck.py $f --k $k --L $L --S2 $S2 --sha256 $h
  check k${k}_ccheck "^VERDICT PROOF of C\($k, $L, S2\)" \
    bash -c "xz -dc $f | $NICE $BIN/ccheck $k $L $S2"
  check k${k}_rcheck "VERDICT: VALID PROOF of C\(k=$k, L=$L, S2\)" \
    bash -c "xz -dc $f | $NICE $BIN/rcheck $k $L $S2"
done
for k in 3 5 6 7; do      # the classical values Lambda(k,2), k = 3, 5, 6, 7 (calibration only)
  L=${LAM[$k]}; S2=$(s2_of $k); f=certificate/k${k}_L${L}.cert.xz
  check k${k}_ccheck "^VERDICT PROOF of C\($k, $L, S2\)" bash -c "xz -dc $f | $NICE $BIN/ccheck $k $L $S2"
  check k${k}_rcheck "VERDICT: VALID PROOF of C\(k=$k, L=$L, S2\)" bash -c "xz -dc $f | $NICE $BIN/rcheck $k $L $S2"
done
check H3_smallp 'no pair .* 3\(d=2\) 5\(d=4\) 13\(d=4\) 17\(d=8\) 41\(d=8\) 113\(d=8\)$|||with no pair: 6; with r > 1508324: 0; largest finite r = 552 at p = 1476217' \
  $NICE $BIN/smallp 8 1508325 1508324
check H3_smallp_ref '^exceptional primes \(no pair\): 3 5 13 17 41 113$|||552 at p=1476217|||method disagreements \(Euler vs index model vs brute force\): 0$' \
  $NICE $BIN/smallp_ref 1508325

# ---------------------------------------------------------------------------------------------
echo "[3] lower bound (H2): R* and the k = 9 vector"
V8=vectors/vec8_compact.txt
check Rstar_74_exceptions_R2_even '^74 listed primes, R\(2\) = 2$' \
  bash -c "awk '!/^#/ && NF==2 { n++; if (\$1==2) r=\$2 } END { print n \" listed primes, R(2) = \" r; exit !(n==74 && r%2==0) }' $V8"
check Rstar_table_of_note_equals_file 'note table entries: 74  file entries: 74  identical: True' \
  python3 -I code/lower/vecfacts.py .
check Rstar_pairs.c '^FIRST_PAIR n=1508324 n\+1=1508325$|||R\(2\)=2' \
  $NICE $BIN/pairs -k 8 -v $V8 -N 1508326 -d 1
check Rstar_fp_seg.c '^LEAST_ZERO_PAIR 1508324 1508325 ' \
  $NICE $BIN/fp_seg 8 1508325 $V8 1
check Rstar_check_vector.py 'least zero pair n = 1508324 ' \
  $NICE python3 -I code/lower/check_vector.py 8 1508324 $V8 1
check Rstar_lbcheck.c_reset_test '^LEAST_ZERO_PAIR 1508324 1508325 |||every listed prime other than 2 individually necessary: YES' \
  $NICE $BIN/lbcheck 8 1508400 $V8 1 reset
if have_numpy; then
  check Rstar_pairs_np.py '^\[np\] FIRST_PAIR n=1508324 n\+1=1508325$' \
    $NICE python3 -I code/lower/pairs_np.py 8 $V8 1508326 --default 1
else
  echo "  SKIP  Rstar_pairs_np.py                  (numpy not installed)"
fi
for v in vec8_L1508323.txt k8_L1508323_witness.txt; do   # the two full assignments of all 114765 primes
  check full_${v%.txt}_pairs.c '^FIRST_PAIR n=1508324 n\+1=1508325$|||missing=0' \
    $NICE $BIN/pairs -k 8 -v vectors/$v -N 1508326 -d none
  check full_${v%.txt}_fp_seg.c '^LEAST_ZERO_PAIR 1508324 1508325 |||primes <= n\+1: 114765, of which listed: 114765' \
    $NICE $BIN/fp_seg 8 1508325 vectors/$v -1
done
V9=vectors/vec9_compact18_146290624.txt
check k9_pairs.c '^FIRST_PAIR n=146290624 n\+1=146290625$' \
  $NICE $BIN/pairs -k 9 -v $V9 -N 146290626 -d 1
check k9_fp_seg.c '^LEAST_ZERO_PAIR 146290624 146290625 ' \
  $NICE $BIN/fp_seg 9 146290625 $V9 1
check k9_lbcheck.c '^LEAST_ZERO_PAIR 146290624 146290625 ' \
  $NICE $BIN/lbcheck 9 146290625 $V9 1

# ---------------------------------------------------------------------------------------------
if [ $REGEN = 1 ]; then
  echo "[4] regeneration of the canonical certificate streams"
  for k in 8 2 3 4 5 6 7; do
    L=${LAM[$k]}; S2=$(s2_of $k); r2=all; [ $k = 8 ] && r2=even
    h=$(grep " k${k}_L${L}.cert\$" certificate/SHA256SUMS.decompressed | cut -d' ' -f1)
    check k${k}_regenerate_pairtree "^$h  -\$" \
      bash -c "$NICE $BIN/pairtree $k $L --r2 $r2 --out - 2> $LOG/k${k}_pairtree_stats.log | sha256sum"
    check k${k}_regenerate_regen.c "^$h  -\$" \
      bash -c "$NICE $BIN/regen $k $L $S2 2> /dev/null | sha256sum"
  done
fi

echo "summary: $NPASS passed, $NFAIL failed, total $(elapsed "$T_START") s"
if [ $NFAIL -gt 0 ]; then printf '  failed: %s\n' "${FAILED[@]}"; exit 1; fi
echo "ALL CHECKS PASSED"
if [ $EXTENDED = 1 ]; then exec bash code/extended/run_extended.sh; fi
exit 0
