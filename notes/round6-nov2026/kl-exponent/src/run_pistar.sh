#!/bin/bash
# brute-force campaign for Theorem T and the litmus maps; one core.
cd "$(dirname "$0")/.." || exit 1
ulimit -v 4200000
W31=$(ls data/w/p3d1_k*.txt); W3m=$(ls data/w/p3dm1_k*.txt); W51=$(ls data/w/p5d1_k*.txt)
R="taskset -c 6 src/pistar"
echo "== 3n+1: all a<=3000, x<=1e7"; $R 3 1 2 3000 1 1e12 10000000 $W31
echo "== 3n+1: a in [3000,1e6] every 997th principal a, x<=min(65536a,1e8)"; $R 3 1 3000 1000000 997 65536 100000000 $W31
echo "== 3n+1: a in [1e6,1e7] every 99991st, x<=4096a"; $R 3 1 1000000 10000000 99991 4096 40000000000 $W31
echo "== 3n+1: x just above a: all a<=200000, x<=16a"; $R 3 1 2 200000 1 16 1000000000 $W31
echo "== 5n+1: all a<=3000, x<=1e7"; $R 5 1 1 3000 1 1e12 10000000 $W51
echo "== 5n+1: all a<=100000, x<=256a"; $R 5 1 1 100000 1 256 1000000000 $W51
echo "== 3n-1: all a<=3000, x<=1e7"; $R 3 -1 1 3000 1 1e12 10000000 $W3m
echo "== 3n-1: all a<=200000, x<=16a"; $R 3 -1 1 200000 1 16 1000000000 $W3m
echo "== 3n-1: a in [3000,1e6] every 997th, x<=min(65536a,1e8)"; $R 3 -1 3000 1000000 997 65536 100000000 $W3m
