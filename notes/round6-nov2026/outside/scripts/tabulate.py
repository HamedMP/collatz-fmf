#!/usr/bin/env python3
"""Binary-search the largest p/q (fixed q) for which the energy-game solver finds a
(j,p,q)-certificate.  usage: tabulate.py BIN jmin jmax q [capmult]
An OK is a rigorous statement only after the dumped certificate passes verify_cert.py;
a FAIL is rigorous only when cap >= (number of states)*q (printed as 'exact-cap')."""
import subprocess, sys

def feasible(binp, j, p, q, cap):
    r = subprocess.run([binp, str(j), str(p), str(q), str(cap)], capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip()

def main():
    binp = sys.argv[1]; jmin = int(sys.argv[2]); jmax = int(sys.argv[3]); q = int(sys.argv[4])
    capmult = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    for j in range(jmin, jmax + 1):
        nstates = 2 * 3 ** (j - 1)
        exact = nstates * q
        cap = exact if (capmult == 0 or exact <= capmult * q) else capmult * q
        lo, hi = 0, (631 * q) // 1000 + 1     # p/q >= ln2/ln3 is impossible
        okline = ''
        while hi - lo > 1:
            mid = (lo + hi) // 2
            ok, line = feasible(binp, j, mid, q, cap)
            if ok: lo, okline = mid, line
            else: hi = mid
        print(f"j={j} states={nstates} best p/q={lo}/{q}={lo/q:.4f} (fail at {hi}/{q}; cap={'exact' if cap==exact else cap}) :: {okline}", flush=True)

main()
