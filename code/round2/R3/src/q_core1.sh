#!/bin/sh
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/U_p17_t7_H43_A.log; do sleep 20; done
./bin/fibcov 17 8 47 2 pos 9 10 11 12 13 14 15 16 > logs/P17_t8_H47_A_pos_b.log 2>&1
./bin/fibcov2b 17 8 47 2 0 6 7 8 9 10 11 > logs/P17_t8_H47_B_pos_b.log 2>&1
