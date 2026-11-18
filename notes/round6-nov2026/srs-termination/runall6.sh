#!/bin/bash
cd "$(dirname "$0")"
PY="taskset -c 7 nice -n 5 /home/matrix/home/projects/collatz/venv/bin/python -u"
while [ ! -f logs/alldone5.flag ]; do sleep 15; done
$PY validate.py 1000000 W01 > logs/validate_W01.log 2>&1
$PY prove.py --sched quick --tag main2 W01 > logs/main2.log 2>&1
echo ALLDONE > logs/alldone6.flag
