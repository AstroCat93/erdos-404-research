#!/bin/bash
# Second logged batch: adversarial hill-climbing (t_adv.py).  One job at a time (see run.sh).
cd "$(dirname "$0")"
LOGD=../../../data/round4/verify_D_W6_falsify
R=./run.sh
# args: p n H H2 seed ncyl iters [psub]
$R $LOGD/adv.log python3 t_adv.py 3 20 5 4 701 6 250
$R $LOGD/adv.log python3 t_adv.py 3 24 5 5 702 3 150
$R $LOGD/adv.log python3 t_adv.py 5 20 5 5 703 4 150
$R $LOGD/adv.log python3 t_adv.py 7 21 7 7 704 3 100 12
