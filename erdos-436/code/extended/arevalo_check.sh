#!/usr/bin/env bash
# arevalo_check.sh -- optional third-party cross-check of paper/note.md section 3 ("Cross-check with [Ar]")
# and section 4 (R* restricted to the primes below 300 is one of the 108 unsettled vectors of [Ar]).
#
# WARNING: this downloads F. Arevalo's public repository https://github.com/farev/matematica at the
# commit cited in the note (4404f5bd46cd9248807980ea73a8a6467afdb342) and compiles and runs code
# from it (tree2.c, check_tree2.py).  None of that code is part of this repository.  Needs git and
# network access, or AREVALO_REPO=/path/to/an/existing/clone.  About 2 minutes and 100 MB of disk.
#
# Usage (from anywhere):  bash code/extended/arevalo_check.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT=$PWD
W=$ROOT/build/arevalo; LOG=$ROOT/build/logs/arevalo; mkdir -p "$W" "$LOG" "$ROOT/build/bin"
COMMIT=4404f5bd46cd9248807980ea73a8a6467afdb342
NICE=${NICE:-nice -n 10}
if [ -n "${AREVALO_REPO:-}" ]; then
  REPO=$(cd "$AREVALO_REPO" && pwd)
else
  REPO=$W/matematica
  if [ ! -d "$REPO/.git" ]; then
    git init -q "$REPO"
    git -C "$REPO" remote add origin https://github.com/farev/matematica
    GIT_LFS_SKIP_SMUDGE=1 git -C "$REPO" fetch -q --depth 1 origin $COMMIT
    GIT_LFS_SKIP_SMUDGE=1 git -C "$REPO" checkout -q FETCH_HEAD
  fi
fi
echo "Arevalo repository at commit $(git -C "$REPO" rev-parse HEAD) (expected $COMMIT)"
A=$REPO/conjectures/power-residue-pairs
echo "input hashes (the values seen on 2026-10-15 are listed in code/README.md):"
(cd "$A" && sha256sum tree2.c check_tree2.py data/pairs_P300_L10000000.txt)

gcc -O2 -o "$W/tree2" "$A/tree2.c"
gcc -O2 -o "$ROOT/build/bin/pairtree" "$ROOT/code/generator/pairtree.c"
cd "$W"
ln -sfn "$A/data" data            # the certificate header records this relative path
echo "== Arevalo's tree2 at L = 1508324 (expect: unsettled=0, max_settling_n=1508324)"
$NICE ./tree2 8 data/pairs_P300_L10000000.txt 1508324 cert_k8_P300_L1508324.gz --even 2 > "$LOG/tree2_L1508324.log" 2>&1
grep -E "^k=8 L=1508324:" "$LOG/tree2_L1508324.log"
echo "== Arevalo's check_tree2.py on that certificate (about 1 minute)"
$NICE python3 -I "$A/check_tree2.py" 8 data/pairs_P300_L10000000.txt cert_k8_P300_L1508324.gz > "$LOG/check_tree2.log" 2>&1
head -1 "$LOG/check_tree2.log"
grep -q "tree exhaustive; unsettled=0; all settled leaves verified; U = max settling n = 1508324" "$LOG/check_tree2.log"
echo "== Arevalo's tree2 --dry at L = 1508323 (expect 108 unsettled vectors)"
$NICE ./tree2 8 data/pairs_P300_L10000000.txt 1508323 /dev/null --even 2 --dry > "$LOG/tree2_dry_L1508323.log" 2> "$LOG/tree2_dry_L1508323.unsettled.txt"
grep -E "^k=8 L=1508323:" "$LOG/tree2_dry_L1508323.log"
echo "== our tree capped at depth 62 (the 62 primes below 300) at L = 1508323 (expect 432 unresolved leaves)"
$NICE "$ROOT/build/bin/pairtree" 8 1508323 --r2 even --maxdepth 62 --unres-out "$W/ours_T62_unresolved.txt" 2> "$LOG/pairtree_T62.log"
wc -l < "$W/ours_T62_unresolved.txt"
echo "== the 108 vectors of Arevalo's dry run vs our 432 unresolved leaves, up to units (expect equal: True)"
python3 -I "$ROOT/code/extended/cmp108.py" "$LOG/tree2_dry_L1508323.unsettled.txt" "$W/ours_T62_unresolved.txt" | tee "$LOG/cmp108.log"
grep -q "equal: True" "$LOG/cmp108.log"
echo "== R* restricted to the primes below 300 vs the published file data/gaps_k8_P300_L1500000.txt (expect [(11, 1)])"
python3 -I "$ROOT/code/extended/rstar_in_gaps.py" "$ROOT/vectors/vec8_compact.txt" "$A/data/gaps_k8_P300_L1500000.txt"
echo "== audit of Arevalo's smooth-pairs file, which check_tree2.py trusts"
(cd "$A" && python3 -I "$ROOT/code/extended/audit_external_pairs.py" data/pairs_P300_L10000000.txt 1508324)
rm -f "$W/cert_k8_P300_L1508324.gz"
echo "AREVALO CROSS-CHECK DONE"
