#!/bin/sh
PY=/home/matrix/home/projects/collatz/venv/bin/python
K=800
for f in 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.63 0.66 0.7; do n=$($PY -c "print(int($f*$K))"); taskset -c 6 $PY g2_major.py $K "3**$n" 2 0.1; done
for r in 3 4 5; do taskset -c 6 $PY g2_major.py 800 1 $r; done
taskset -c 6 $PY g2_major.py 400 1 8
