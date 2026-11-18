#!/bin/sh
# Build the CollatzFMF Lean project (max 2 cores) and show the tail of the output.
# Usage: sh build.sh [lake build args...]
export PATH="$HOME/.elan/bin:$PATH"
export LEAN_NUM_THREADS=2
cd /home/matrix/home/projects/collatz/repo/lean || exit 1
LOG=/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/lean/build.log
taskset -c 0-1 lake build "$@" > "$LOG" 2>&1
echo "exit: $?" >> "$LOG"
tail -n "${TAILN:-60}" "$LOG"
