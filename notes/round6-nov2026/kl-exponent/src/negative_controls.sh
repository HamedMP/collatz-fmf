#!/bin/bash
# negative controls for check_cert.py: every mutated certificate must be rejected.
# usage: negative_controls.sh SCRATCHDIR
cd "$(dirname "$0")/.." || exit 1
PY=/home/matrix/home/projects/collatz/venv/bin/python
S=$1; mkdir -p "$S"
mut() { # name srcdir python-snippet
  rm -rf "$S/$1"; cp -r "$2" "$S/$1"
  $PY -I - "$S/$1" <<PYEOF
import json, sys, numpy as np
d = sys.argv[1]; c = json.load(open(d + "/cert.json")); w = np.fromfile(d + "/weights.bin", dtype=c["dtype"])
$3
json.dump(c, open(d + "/cert.json", "w")); w.tofile(d + "/weights.bin")
PYEOF
  if taskset -c 6 $PY src/check_cert.py "$S/$1" > "$S/$1.out" 2>&1; then echo "NOT REJECTED: $1"; else echo "rejected as expected: $1 ($(head -c 90 "$S/$1.out" | tr '\n' ' '))"; fi
  rm -rf "$S/$1"
}
mut k12_gamma_up   cert/k12_lower 'c["gamma_num"] += int(1e-7 * 2**40)'
mut k12_mode_swap  cert/k12_lower 'c["mode"] = "upper"'
mut k12_weight_up  cert/k12_lower 'w[12345] = w[12345] + w[12345] // 1000'
mut k12_weight_dn  cert/k12_lower 'w[777] = w[777] - w[777] // 1000'
mut k12u_gamma_dn  cert/k12_upper 'c["gamma_num"] -= int(1e-7 * 2**40)'
mut k17_gamma_up   cert/k17_lower 'c["gamma_num"] += int(1.2e-5 * 2**40)'
mut k17_weight_up  cert/k17_lower 'w[31337] = w[31337] + w[31337] // 1000'
mut k17u_gamma_dn  cert/k17_upper 'c["gamma_num"] -= int(1.2e-5 * 2**40)'
