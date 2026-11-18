#!/bin/sh
# controls: 3n+d (d=5,7,11,13) to 1e8 and 5n+1 to 2e7. Usage: taskset -c 1 sh run_controls.sh
for d in 5 7 11 13; do echo "== 3n+$d"; ./basins 3 $d 100000000 0 | grep -E "cycles|X=1000000 |X=100000000|profile c[0-9] mod 9:|profile c[0-9] mod 8:" ; done > out_3npd.txt 2>&1
./basins 5 1 20000000 0 | grep -E "cycles|X=|gaphist" > out_5np1.txt 2>&1
echo done > controls.done
