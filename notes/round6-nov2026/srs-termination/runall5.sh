#!/bin/bash
cd "$(dirname "$0")"
PY="taskset -c 7 nice -n 5 /home/matrix/home/projects/collatz/venv/bin/python -u"
while [ ! -f logs/alldone4.flag ]; do sleep 15; done
$PY prove.py --sched quick --tag calib3 W-r1 > logs/calib3.log 2>&1
$PY prove.py --sched tiny --tag deep --grid "n:tr:3:3:1200,a:tr:3:4:1200" P > logs/deepP.log 2>&1
echo ALLDONE > logs/alldone5.flag
