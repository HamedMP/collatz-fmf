#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "runq.sh [d]eep W" >/dev/null; do sleep 15; done
bash runq.sh deep G > logs/deepG.log 2>&1
echo ALLDONE > logs/alldone2.flag
