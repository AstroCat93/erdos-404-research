#!/bin/sh
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/P11_t8_H44_B_pos.log 2>/dev/null; do sleep 20; done
./bin/fibcov2b 11 7 41 3 4 37 > logs/P11_t7_H41_K37_B.log 2>&1
./bin/fibcov2b 17 7 43 2 6 $(cat data/K_p17_t7_B_half1.txt) $(cat data/K_p17_t7_B_half2.txt) > logs/U_p17_t7_H43_B.log 2>&1
./bin/fibcov2b 17 8 47 2 0 12 13 14 15 16 > logs/P17_t8_H47_B_pos_c.log 2>&1
