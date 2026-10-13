#!/bin/bash
# batch_light.sh -- the single-core checks of the R3C check (chain checkers, prediction files,
# independent brute force).  Started while the D re-runs (one core) are going.
ROOT=/home/user/erdos-404-research
OUT=$ROOT/code/round3/check_R3C/logs
R=$ROOT/code/round3/check_R3C/run_logged.sh
cd $ROOT
L=data/round3/R3C:data/round3/R3C/p29_t7
# 1. both chain checkers, every spec of the report, from the archived logs
{
  echo "# chain checkers re-run by the R3C check, $(date -u '+%Y-%m-%d %H:%M:%S UTC'), R3C_LOGS=$L"
  for s in p29_AD p29_AC_AD p29_ACD_D7 p31_AC_D7 neg_p29_H44 neg_p29_K27 neg_p29_C_pos neg_p29_t6_H39 neg_p31_D8; do
    echo "### chain_r3.py spec $s"; R3C_LOGS=$L nice -n 10 python3 -I code/round3/R3C/chain_r3.py code/round3/R3C/specs/$s.txt | grep -E 'CHAIN|NOT certified|first non|=False'
  done
  for P in A C D; do
    echo "### chain_c_r3.py $P 29 8"; R3C_LOGS=$L nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py $P 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"
    echo "### chain_c_r3.py $P 29 7"; R3C_LOGS=$L nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py $P 29 7 "1:7,2:13,3:19,4:24,5:29,6:40" ""
    echo "### chain_c_r3.py $P 31 7"; R3C_LOGS=$L nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py $P 31 7 "1:7,2:14,3:19,4:25,5:30,6:41" ""
  done
  echo "### extra control: chain_c_r3.py A 29 8 with depth-7 H=44 (the H44 directory added)"
  R3C_LOGS=$L:data/round3/R3C/p29_t7_H44 nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py A 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:44"
  echo "### extra control: chain_r3.py on a copy of the logs with ONE depth-7 D log (K''=17) removed"
  T=$(mktemp -d); cp data/round3/R3C/p29_t7/*.log $T/; rm $T/P29_t7_H45_D_K17.log
  R3C_LOGS=data/round3/R3C:$T nice -n 10 python3 -I code/round3/R3C/chain_r3.py code/round3/R3C/specs/p29_AD.txt | grep -E 'CHAIN|NOT certified|first non'
  R3C_LOGS=data/round3/R3C:$T nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py D 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"
  echo "### extra control: the same with K''=17's D line edited to missing=1 NOT_COVERED"
  cp data/round3/R3C/p29_t7/P29_t7_H45_D_K17.log $T/; sed -i 's/missing=0 COVERED/missing=1 NOT_COVERED/' $T/P29_t7_H45_D_K17.log
  R3C_LOGS=data/round3/R3C:$T nice -n 10 python3 -I code/round3/R3C/chain_r3.py code/round3/R3C/specs/p29_AD.txt | grep -E 'CHAIN|NOT certified|first non'
  R3C_LOGS=data/round3/R3C:$T nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py D 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"
  rm -rf $T
  echo "### chain_c_r3.py on the round-2 program-C logs (must reproduce data/round2/review/computation/chain_c.out)"
  for pl in "7 9 1:4,2:7,3:19,4:26,5:28,6:34 7:40,8:47" "11 9 1:5,2:10,3:18,4:22,5:30,6:33 7:40:37=41,8:44" \
            "13 9 1:6,2:10,3:19,4:24,5:32,6:35,7:39 8:47" "17 9 1:5,2:11,3:16,4:25,5:30,6:34,7:43 8:47" \
            "19 8 1:5,2:12,3:17,4:27,5:31,6:35 7:45" "23 8 1:7,2:12,3:18,4:23,5:33,6:37 7:43"; do
    set -- $pl; R3C_LOGS=data/round2/review/computation/logs nice -n 10 python3 -I code/round3/R3C/chain_c_r3.py C $1 $2 "$3" "$4"
  done
  echo "### data/round2/review/computation/chain_c.out (for comparison)"; cat data/round2/review/computation/chain_c.out 2>/dev/null || echo "(not found)"
} > $OUT/chains_rerun.log 2>&1
# 2. the registered predictions: regenerate and compare; independent recount
{
  echo "# predict.py regenerated $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  T=$(mktemp -d)
  nice -n 10 python3 code/round3/R3C/predict.py 29 1 7 pos:28 > $T/p29.txt 2>&1
  nice -n 10 python3 code/round3/R3C/predict.py 31 1 7 pos:30 > $T/p31.txt 2>&1
  grep -v '^#' data/round3/R3C/PREDICTIONS_registered.txt > $T/reg_body.txt
  cat $T/p29.txt $T/p31.txt | grep -v '^#' > $T/gen_body.txt
  if diff $T/reg_body.txt $T/gen_body.txt > $T/d.txt; then echo "registered body == regenerated body (non-comment lines): IDENTICAL"; else echo "DIFFERENCES:"; cat $T/d.txt; fi
  rm -rf $T
  nice -n 10 python3 code/round3/check_R3C/pred_recount.py
  echo "# pred_eval.py re-run, compared with the archived PREDICTIONS_evaluation.txt (body)"
  nice -n 10 python3 code/round3/R3C/pred_eval.py > /tmp/claude-0/-home-user-erdos-404-research/64513d2d-9023-5297-8d1a-eefeb2df66c3/scratchpad/pe.txt 2>&1
  if diff <(grep -v '^# \(command\|run\)' data/round3/R3C/PREDICTIONS_evaluation.txt) /tmp/claude-0/-home-user-erdos-404-research/64513d2d-9023-5297-8d1a-eefeb2df66c3/scratchpad/pe.txt; then echo "pred_eval.py output == archived evaluation"; fi
} > $OUT/predictions_check.log 2>&1
# 3. independent brute force
for T in rho0 selftest scans negatives lemma lemma29; do
  $R $OUT/indep_$T.log 0 python3 code/round3/check_R3C/indep.py $T
done
echo "batch_light done $(date -u)"
