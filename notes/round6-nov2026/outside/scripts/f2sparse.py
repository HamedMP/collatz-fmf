"""Max t over sparse F = x^n + (<= w-2 middle terms) + 1.  usage: f2sparse.py w n1 n2 ..."""
import sys, itertools, math
from f2lib import t
w = int(sys.argv[1])
for n in map(int, sys.argv[2:]):
    best = (0, None)
    for k in range(0, w - 1):
        for mid in itertools.combinations(range(1, n), k):
            F = (1 << n) | 1
            for i in mid: F |= 1 << i
            v = t(F)
            if v > best[0]: best = (v, mid)
    print(f"n={n} w<={w} max t={best[0]} t/n={best[0]/n:.3f} t/(n log2 n)={best[0]/(n*math.log2(n)):.3f} mid={best[1]}", flush=True)
