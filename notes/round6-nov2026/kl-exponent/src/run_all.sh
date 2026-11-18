#!/bin/sh
# usage: run_all.sh KFROM KTO GUESS  -- search + exact check, sequential, one core
cd "$(dirname "$0")/.." || exit 1
PY=/home/matrix/home/projects/collatz/venv/bin/python
ulimit -v 4200000
g=$3
for k in $(seq $1 $2); do
  fl=""; [ $k -ge 19 ] && fl="--float"
  taskset -c 6 $PY src/run_k.py $k $g $fl || exit 1
  taskset -c 6 $PY src/check_cert.py cert/k${k}_lower || echo "CHECK-FAILED k=$k lower"
  taskset -c 6 $PY src/check_cert.py cert/k${k}_upper || echo "CHECK-FAILED k=$k upper"
  g=$($PY -c "import json;print(json.load(open('cert/k${k}_search.json'))['gamma_star_float']+0.008)")
done
