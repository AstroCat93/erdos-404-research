#!/bin/sh
cd "$(dirname "$0")"
D=../data
( time ./tree 2 29 3 $D/p2 8 ) > $D/tree_p2.txt 2>&1
( time ./tree 3 16 3 $D/p3 5 ) > $D/tree_p3.txt 2>&1
( time ./tree 5 10 3 $D/p5 3 ) > $D/tree_p5.txt 2>&1
( time ./tree 7 8 3 $D/p7 2 ) > $D/tree_p7.txt 2>&1
( time ./tree 11 6 3 $D/p11 2 ) > $D/tree_p11.txt 2>&1
( time ./tree 13 6 3 $D/p13 2 ) > $D/tree_p13.txt 2>&1
echo ALLDONE > $D/trees_done.txt
