#!/bin/sh
# Tasks (2), (3), (4): run after the annealed batch finishes.  4 threads each, sequential.  Timings logged.
W="<WORKSPACE>/e404r3/T4-computations"
cd "$W"
while ! grep -q ALLDONE logs/annealed.log; do sleep 10; done
L=logs/queue.log
run() { name=$1; shift; echo "=== $name: $* start $(date +%T)" >> $L; s=$(date +%s); "$@" > data/$name.txt 2>> $L; echo "=== $name done in $(( $(date +%s) - s )) s" >> $L; }
# (2) survivors 1 <= a <= 4096 at increasing caps
run surv_cap32   ./src/gsample_nl2  -1 0 32   4096 4
run surv_cap254  ./src/gsample_nl4  -1 0 254  4096 4
run surv_cap1022 ./src/gsample_nl17 -1 0 1022 4096 4
run surv_cap2046 ./src/gsample_nl33 -1 0 2046 4096 4
# (4) gate-block sums and integrals (p=13 integral with 12 GL nodes; p<=11 with 16)
run gatesum_p5   ./src/gatesum 5  8 4 16
run gatesum_p7   ./src/gatesum 7  8 4 16
run gatesum_p11  ./src/gatesum 11 8 4 16
run gatesum_p13  ./src/gatesum 13 8 4 12
# (3) Monte Carlo delta_G(2)
run mc_cap126    ./src/gsample_nl2  40000000 20261012 126  4
run mc_cap256    ./src/gsample_nl5  20000000 20261013 256  4
run mc_cap512    ./src/gsample_nl9   2000000 20261014 512  4
run mc_cap1024   ./src/gsample_nl17  1000000 20261015 1024 4
run mc_cap2046   ./src/gsample_nl33   200000 20261016 2046 4
# (2) deep survivors
run surv_cap4094 ./src/gsample_nl65 -1 0 4094 4096 4
echo QUEUEDONE >> $L
