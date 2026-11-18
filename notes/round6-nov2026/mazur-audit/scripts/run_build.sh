#!/bin/bash
# usage: run_build.sh BUILD_DIR   (direct lean compile against the repo's local Mathlib v4.36.0 oleans; read-only on that cache)
export PATH=$HOME/.elan/bin:$PATH
export LEAN_NUM_THREADS=1
P=/home/matrix/home/projects/collatz/repo/lean/.lake/packages
LP="$1/out"
for d in $P/*/.lake/build/lib/lean; do LP="$LP:$d"; done
export LEAN_PATH="$LP"
cd "$1" && exec taskset -c 0-1 elan run leanprover/lean4:v4.36.0 make -k -j2 -f Makefile
