#!/bin/sh
export OMP_NUM_THREADS=2
for q in 24 32 40 48 56 64 80 88 96 104; do taskset -c 6-7 ./f1_count $q 3 1 > out_3p1_Q$q.txt; done
taskset -c 6-7 ./f1_count 96 5 1 > out_5p1_Q96.txt
taskset -c 6-7 ./f1_count 96 3 -1 > out_3m1_Q96.txt
taskset -c 6-7 ./f1_count 112 3 1 > out_3p1_Q112.txt
taskset -c 6-7 ./f1_count 120 3 1 > out_3p1_Q120.txt
echo done
