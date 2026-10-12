#!/bin/sh
# scan Fourier L1/L2 of gate windows; args: p t "H list" "K list"
p=$1; t=$2; Hs=$3; Ks=$4
for H in $Hs; do for K in $Ks; do ./bin/fwin $p $t $H $K; done; done
