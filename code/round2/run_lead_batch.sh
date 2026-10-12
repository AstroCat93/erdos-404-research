#!/bin/sh
# run_lead_batch.sh -- the lead author's single-core re-runs for note_v2.md Section 10.7 (rows S1-S11).
# usage: sh run_lead_batch.sh [FORMAL_DIR]     (outputs go to code_r2/outputs/)
# FORMAL_DIR: Lean 4 + Mathlib project containing Formal/E404R2b/Renorm.lean (optional).
# All paths are quoted: the working tree lives under a path with spaces.
FORMAL="$1"
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")" || exit 1
R="$(pwd)"
O="$R/outputs"
mkdir -p "$O"
# run DIR OUTFILE CMD...   (runs CMD in DIR, stdout+stderr to $O/OUTFILE, logs wall time)
run() {
  d="$1"; f="$2"; shift 2
  s=$(date +%s)
  ( cd "$d" && "$@" ) > "$O/$f" 2>&1
  rc=$?
  el=$(( $(date +%s) - s ))
  echo "[wall ${el}s] exit=$rc ($d) $* > $f" >> "$O/lead_batch_times.log"
}

run "$R" lead_checks.out python3 lead_checks.py
run "$R/R2b/src" S10_lambda_p.out python3 lambda_p.py
run "$R/R2b/src" S10_rmf_budget.out python3 rmf_budget.py

run "$R/R1b" S1_mart_check2_30_36.log python3 mart_check2.py 1011 20 30 36 300 10
run "$R/R1b" S1_mart_check2_50_58.log python3 mart_check2.py 1012 12 50 58 300 10
run "$R/R1b" S1_mart_check2_70_77.log python3 mart_check2.py 1013 8 70 77 400 10
run "$R/R1b" S2_brute_24_30.log python3 brute_window.py 1021 15 24 30 200 8
run "$R/R1b" S2_brute_32_39.log python3 brute_window.py 1022 8 32 39 200 6
run "$R/R1b" S3_negctrl.out python3 negctrl.py 1031 30 36 300 15
run "$R/R1b" S4_lemmaB_check.out python3 lemmaB_check.py 1041 30 36 300 30
run "$R/R1b" S5_rho_table.out python3 rho_table.py

run "$R" S12_lead_window_30_36.log python3 lead_window_check.py 2001 25 30 36
run "$R" S12_lead_window_40_48.log python3 lead_window_check.py 2002 12 40 48
run "$R/R3/src" S13_R3_validate.log python3 validate.py

run "$R/R1a/code" S6_class_check.log python3 class_check.py
run "$R/R1a/code" S7_I8.log python3 I8.py

run "$R/R2a" S8_fl1_p13.out ./bin/fl1 13 13 1 7 0 1
run "$R/R2a" S8_fl1_p11.out ./bin/fl1 11 11 1 8 0 1
run "$R/R2a" S8_iv_p13.out python3 iv_shells.py 13 13 4
run "$R/R2a" S8_iv_p11.out python3 iv_shells.py 11 11 5
run "$R/R2a" S8_fl1_lead_p13.out ./bin/fl1_lead 13 13 7
run "$R/R2a" S8_fl1_lead_p11.out ./bin/fl1_lead 11 11 8
for a in "13 13 1 3" "13 13 1 4" "13 13 2 4" "11 11 1 4" "11 11 2 4" "11 11 2 5"; do
  set -- $a
  run "$R/R2a" "S9_renorm_check_$1_$3_$4.out" python3 renorm_check.py $1 $2 $3 $4
done

if [ -n "$FORMAL" ]; then
  run "$FORMAL" S11_lean_Renorm.log lake env lean Formal/E404R2b/Renorm.lean
fi
echo LEAD_BATCH_DONE >> "$O/lead_batch_times.log"
