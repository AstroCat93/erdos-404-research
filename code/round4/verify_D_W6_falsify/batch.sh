#!/bin/bash
# Logged batch for the numerical-falsification check of M4D's W1-W6.  One job at a time, nice -n 10,
# 30-minute timeout and 3 GB address-space limit per job (see run.sh).
cd "$(dirname "$0")"
LOGD=../../../data/round4/verify_D_W6_falsify
mkdir -p "$LOGD"
R=./run.sh
ALL=rand,gate_hist,gate_win,near2,tight
# ---------------- cylinder tests: W1, W2, W3, W4, W5 ----------------------------------------------------
# args: p n H H' seed ncyl kinds [psub] [kextra] [maxcombos]
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 20 5 4 101 40 $ALL - 1
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 26 6 5 102 15 $ALL - 1 20
$R $LOGD/cyl_p3.log python3 t_cyl.py 3 30 6 6 103 6 rand,gate_hist,tight - 2 12
$R $LOGD/cyl_p3_edge.log python3 t_cyl.py 3 21 2 4 104 15 D0,any - 1
$R $LOGD/cyl_p3_edge.log python3 t_cyl.py 3 22 5 2 105 15 D20,any - 1
$R $LOGD/cyl_p5.log python3 t_cyl.py 5 20 5 5 201 30 $ALL - 1
$R $LOGD/cyl_p5.log python3 t_cyl.py 5 25 5 5 202 10 rand,gate_hist,gate_win,tight 60 1 20
$R $LOGD/cyl_p5_edge.log python3 t_cyl.py 5 20 3 5 203 12 D0,any - 1
$R $LOGD/cyl_p5_edge.log python3 t_cyl.py 5 20 5 3 204 12 D20,any - 1
$R $LOGD/cyl_p7.log python3 t_cyl.py 7 21 7 7 301 16 rand,gate_hist,tight 25 0 20
$R $LOGD/cyl_p7.log python3 t_cyl.py 7 28 7 7 302 8 rand,gate_hist,gate_win,tight 20 1 16
$R $LOGD/cyl_p7_edge.log python3 t_cyl.py 7 21 3 7 303 10 D0,any 25 0 16
$R $LOGD/cyl_p7_edge.log python3 t_cyl.py 7 21 7 3 304 10 D20,any 25 0 16
# ---------------- chain tests: Theorem W6 at finite horizon ---------------------------------------------
# args: p n0 H L seed natoms schedules ebar_modes [psub] [kinds]
$R $LOGD/chain_p3.log python3 t_chain.py 3 24 5 3 401 5 U,R,RP,S,P,M inf,med,q1 - rand,gate_hist
$R $LOGD/chain_p3.log python3 t_chain.py 3 20 5 3 402 5 U,R,P,M med,tiny - rand,gate_hist
$R $LOGD/chain_p3.log python3 t_chain.py 3 24 5 3 403 5 P,S,U med 1 rand,gate_hist
$R $LOGD/chain_p5.log python3 t_chain.py 5 25 5 3 501 3 U,R,RP,S,P,M inf,med - rand,gate_hist
$R $LOGD/chain_p5.log python3 t_chain.py 5 25 5 3 502 4 P,S,M med,q1 1 rand,gate_hist
$R $LOGD/chain_p7.log python3 t_chain.py 7 35 7 3 601 4 U,RP,S,P,M med,inf 6 rand,gate_hist
$R $LOGD/chain_p7.log python3 t_chain.py 7 35 7 3 602 4 S,P med 1 rand,gate_hist
