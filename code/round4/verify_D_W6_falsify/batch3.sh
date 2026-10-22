#!/bin/bash
# Third logged batch: re-run of the p=3, n=26 cylinder job without the near2 sampler (the first attempt was
# stopped by hand because near2 never yields a nonempty slope-0 population at p=3 and only burnt attempts).
cd "$(dirname "$0")"
LOGD=../../../data/round4/verify_D_W6_falsify
R=./run.sh
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 26 6 5 102 15 rand,gate_hist,gate_win,tight - 1 20
# re-run of the p=3, n=30 job with 40 sampled parent lines and kextra=1 (the first attempt with all parents and
# kextra=2 exceeded the 3 GB address-space limit while storing the enumeration)
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 30 6 6 103 6 rand,gate_hist,tight 40 1 12
# W1(a) at N for ALL parents at p=7 (children of every alive parent evaluated at every point), lines sampled
$R $LOGD/cyl_p7.log python3 t_cyl.py 7 21 7 7 305 4 rand,gate_hist 25 0 6 full
