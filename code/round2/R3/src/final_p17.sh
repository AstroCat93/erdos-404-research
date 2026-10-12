#!/bin/sh
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/P17_t8_H47_A_pos_b.log && [ $(cat logs/P17_t8_H47_B_j*.log 2>/dev/null | grep -c SUMMARY) -ge 8 ]; do sleep 60; done
python3 src/chain.py specs/p17_D9.txt > logs/CHAIN_p17_D9.txt 2>&1
