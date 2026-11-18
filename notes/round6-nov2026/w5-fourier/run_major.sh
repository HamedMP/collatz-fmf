#!/bin/sh
PY=/home/matrix/home/projects/collatz/venv/bin/python
for K in 800 1600 3200; do for h in 1 3 5 11 2 1001 "2**64+13" "3**40"; do taskset -c 4-5 $PY g2_major.py $K "$h" 2 0.1; done; done
for K in 800 1600; do for e in 0.02 0.05 0.2 0.3; do taskset -c 4-5 $PY g2_major.py $K 1 2 $e; done; done
