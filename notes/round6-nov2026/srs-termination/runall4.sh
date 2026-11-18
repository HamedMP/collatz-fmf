#!/bin/bash
cd "$(dirname "$0")"
PY="taskset -c 7 nice -n 5 /home/matrix/home/projects/collatz/venv/bin/python -u"
while [ ! -f logs/alldone3.flag ]; do sleep 15; done
$PY prove.py --sched mini --tag sub RET~4 RET~5 RET~6 RET~7 RET~8 RET~9 RET~10 RET~11 RET~12 > logs/sub2.log 2>&1
echo ALLDONE > logs/alldone4.flag
