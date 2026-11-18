#!/usr/bin/env python3
"""Binary-search the largest p (fixed q) with a (j,p,q)-certificate for the map (a n + c)/2.
usage: tabulate2.py a c jmin jmax q capmult [dumpdir]
cap = min(nstates*q, capmult*q).  FAIL is rigorous only when cap = nstates*q ('exact').
OK is rigorous once the dumped certificate passes verify_cert.py."""
import subprocess, sys, os, math, time
here = os.path.dirname(os.path.abspath(__file__))
a, c, jmin, jmax, q, capmult = map(int, sys.argv[1:7])
dumpdir = sys.argv[7] if len(sys.argv) > 7 else None
for j in range(jmin, jmax + 1):
    nstates = a**j - a**(j-1)
    exact = nstates * q
    cap = min(exact, capmult * q)
    lo, hi = 0, int(q * math.log(2) / math.log(a)) + 1
    t0 = time.time()
    while hi - lo > 1:
        mid = (lo + hi) // 2
        r = subprocess.run([os.path.join(here, 'game2'), str(a), str(c), str(j), str(mid), str(q), str(cap)], capture_output=True, text=True)
        if r.returncode == 0: lo = mid
        else: hi = mid
    line = ''
    if dumpdir and lo > 0:
        os.makedirs(dumpdir, exist_ok=True)
        f = os.path.join(dumpdir, f'cert_a{a}_c{c}_j{j}_p{lo}_q{q}.bin')
        line = subprocess.run([os.path.join(here, 'game2'), str(a), str(c), str(j), str(lo), str(q), str(cap), f], capture_output=True, text=True).stdout.strip()
    print(f"a={a} c={c} j={j} states={nstates} best p/q={lo}/{q} fail at {hi}/{q} cap={'exact' if cap == exact else cap} t={time.time()-t0:.0f}s :: {line}", flush=True)
