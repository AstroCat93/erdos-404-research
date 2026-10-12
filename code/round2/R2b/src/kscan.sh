#!/bin/sh
# usage: kscan.sh p t H c  -> runs fwin over all units K' mod p^c, prints L1 and top-level ratio
p=$1; t=$2; H=$3; c=$4
pc=1; i=0; while [ $i -lt $c ]; do pc=$((pc*p)); i=$((i+1)); done
K=1
while [ $K -lt $pc ]; do
  if [ $((K % p)) -ne 0 ]; then
    ./bin/fwin2 $p $t $H $K | awk -v K=$K 'NR==1{for(i=1;i<=NF;i++){if($i ~ /^L1=/) l1=$i; if($i ~ /^R1=/) r1=$i}} /d=/{last=$0} END{print "K=" K, l1, r1, last}'
  fi
  K=$((K+1))
done
