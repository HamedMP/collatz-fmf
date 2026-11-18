#!/bin/bash
# sequential experiment queue (one core).  usage: nohup bash runq.sh PHASE > logs/PHASE.log 2>&1 &
cd "$(dirname "$0")"
PY="taskset -c 7 nice -n 5 /home/matrix/home/projects/collatz/venv/bin/python -u"
case "$1" in
calib)  $PY prove.py --sched quick --tag calib P RET-11 RET-r0 W-r0 W-16 G-0 G-1 RET-r1 RET-no01 RET-no10 ;;
neg)    $PY prove.py --sched quick --tag neg C3m C5 FMF3m FMF5 S3m G5 ;;
main)   $PY prove.py --sched quick --tag main W G RET ;;
yahT)   $PY prove.py --sched tiny --tag yahT T-0 T-1 T-2 T-3 T-4 T-5 T-6 T-7 T-8 T-9 T-10 ;;
sub)    $PY prove.py --sched mini --tag sub W~0 W~1 W~2 W~3 W~4 W~5 W~6 W~7 W~8 W~9 W~10 \
            G~0 G~1 G~2 G~3 G~4 G~5 G~6 G~7 G~8 G~9 G~10 \
            RET~0 RET~1 RET~2 RET~3 RET~4 RET~5 RET~6 RET~7 RET~8 RET~9 RET~10 RET~11 RET~12 ;;
front)  # dynamic rules only, original (full) systems: the clean frontier
        G="n:tr:1:2:20,n:fo:1:2:20,n:fr:1:2:20,n:tr:1:4:20,n:fo:1:4:20,n:fr:1:4:20,a:tr:1:4:20,a:fo:1:4:20"
        G="$G,n:tr:2:2:60,n:fo:2:2:60,n:fr:2:2:60,a:tr:2:3:60,a:fo:2:3:60,n:tr:2:3:120,n:fo:2:3:120,n:fr:2:3:120"
        G="$G,a:tr:2:4:120,a:fo:2:4:120,n:tr:3:2:300,a:tr:3:3:300"
        $PY prove.py --sched tiny --tag front --grid "$G" W G RET ;;
farkas) $PY prove.py --sched tiny --tag farkas --grid "a:tr:5:8:1200" Farkas ;;
deep)   G="n:tr:3:3:1200,a:tr:3:4:1200"
        $PY prove.py --sched tiny --tag deep --grid "$G" $2 ;;
calib2) $PY prove.py --sched quick --tag calib2 G0y ;;
esac
