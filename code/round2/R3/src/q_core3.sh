#!/bin/sh
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/P7_t8_H47_B_pos.log 2>/dev/null; do sleep 20; done
./bin/fibcov 17 8 47 2 pos 1 2 3 4 5 6 7 8 > logs/P17_t8_H47_A_pos_a.log 2>&1
./bin/fibcov2b 17 8 47 2 0 1 2 3 4 5 > logs/P17_t8_H47_B_pos_a.log 2>&1
