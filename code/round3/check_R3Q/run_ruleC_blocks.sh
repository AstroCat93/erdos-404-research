#!/bin/sh
# exact Theorem C rule values at the report's table K and at the last K of each M-block (worst case within a block)
cd "$(dirname "$0")"
for K in 3584 4096 8192 16384; do nice -n 10 python3 -I bounds_check.py ruleC $K $K 1 | grep RULE; done
M=48; while [ $M -le 400 ]; do K=$((64*M+63)); nice -n 10 python3 -I bounds_check.py ruleC $K $K 1 | grep RULE; M=$((M+1)); done
