#!/bin/bash
# queue of game tabulations (single core)
V=/home/matrix/home/projects/collatz/venv/bin/python
cd "$(dirname "$0")"
taskset -c 7 nice -n 5 $V tabulate2.py 5 1 2 6 200 300 > ../data/tab_5n1_q200.log 2>&1
taskset -c 7 nice -n 5 $V tabulate2.py 3 1 11 13 100 150 ../data/certs > ../data/tab_3n1_q100.log 2>&1
