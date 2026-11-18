#!/bin/bash
cd "$(dirname "$0")"
while [ ! -f logs/alldone.flag ]; do sleep 15; done
bash runq.sh calib2 > logs/calib2.log 2>&1
bash runq.sh deep W > logs/deepW.log 2>&1
bash runq.sh deep G > logs/deepG.log 2>&1
bash runq.sh deep RET > logs/deepRET.log 2>&1
echo ALLDONE > logs/alldone2.flag
