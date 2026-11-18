#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
ulimit -v 1500000
W31=$(ls data/w/p3d1_k*.txt); W3m=$(ls data/w/p3dm1_k*.txt); W51=$(ls data/w/p5d1_k*.txt)
echo "== 3n+1: all a<=120, x<=1e8"; taskset -c 6 src/pistar32 3 1 2 120 1 1e12 100000000 $W31
echo "== 3n-1: all a<=120, x<=1e8"; taskset -c 6 src/pistar32 3 -1 1 120 1 1e12 100000000 $W3m
echo "== 5n+1: all a<=3000, x<=1e9"; taskset -c 6 src/pistar32 5 1 1 3000 1 1e12 1000000000 $W51
