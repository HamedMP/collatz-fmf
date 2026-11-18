#!/bin/bash
cd "$(dirname "$0")"
PY="taskset -c 7 nice -n 5 /home/matrix/home/projects/collatz/venv/bin/python -u"
while [ ! -f logs/alldone2.flag ]; do sleep 15; done
$PY prove.py --sched d4 --tag yahT4 T-2 T-10 > logs/yahT4.log 2>&1
$PY prove.py --sched tiny --tag farkasneg --neg 1 --grid "a:tr:5:8:1200" Farkas > logs/farkasneg.log 2>&1
echo ALLDONE > logs/alldone3.flag
