#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "runq.sh [c]alib" >/dev/null; do sleep 15; done
for ph in neg main front yahT sub farkas; do
  bash runq.sh $ph > logs/$ph.log 2>&1
done
echo ALLDONE > logs/alldone.flag
