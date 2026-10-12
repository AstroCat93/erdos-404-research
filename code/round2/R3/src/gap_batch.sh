#!/bin/sh
# runs on the core freed after the p=7 depth-8 B run; then resumes the paused queue 3
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/P7_t8_H47_B_pos.log 2>/dev/null; do sleep 15; done
# (a) failure structure near threshold (all classes)
for spec in "13 7 38 2" "13 6 34 2" "13 4 23 0" "17 6 33 1" "19 6 34 1" "11 6 32 1" "11 5 29 1" "17 5 29 1" "7 6 33 2" "7 5 27 2"; do
  python3 src/failstruct.py $spec 60 >> logs/failstruct.txt 2>&1
done
# (b) p=13 scans saved to a log (calibration data)
for t in 1 2 3 4 5 6 7; do python3 src/scanH.py 13 $t 2 39; done > logs/scan_p13_t1-7.log 2>&1
# (c) out-of-sample tests: (17,7,42) predicted FAIL (uniform), (19,7,44) predicted FAIL at some of 18 positions
FIBCOV_STOP=1 FIBCOV_FIBRESTOP=1 ./bin/fibcov 17 7 42 2 all > logs/OOS_p17_t7_H42_A.log 2>&1
./bin/fibcov 19 7 44 2 pos 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 > logs/OOS_p19_t7_H44_A.log 2>&1
# (d) p=23: scans t<=6, depth-7 positions
for t in 1 2 3 4 5 6; do python3 src/scanH.py 23 $t 2 40; done > logs/scan_p23_t1-6.log 2>&1
./bin/fibcov 23 7 43 1 pos 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 > logs/P23_t7_H43_A_pos.log 2>&1
./bin/fibcov2b 23 7 43 1 8 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 > logs/P23_t7_H43_B_pos.log 2>&1
echo GAPDONE > logs/gap_done.txt
kill -CONT $(pgrep -f q_core3.sh)
