#!/usr/bin/env python3
"""w4-E e2: do the CONCLUSIONS of (H),(R),(S) hold on the observed orbits of 5n+1 (and 3n+1, 3n-1 for comparison)?
For each odd n < NMAX run x -> x/2, (q x + c)/2 until a term repeats or exceeds 2^CAP (escape, 'divergent-looking').
Record per orbit: harm = sum 1/x_k (distinct stretch), xi = prod_{odd}(1 + c/(q x_i)), soj = max_L #{k: x_k < 2^L}/2^(eta L).
Floats here are exploration only.
Run: taskset -c 4 python e2_5n1.py
"""
from math import log2
import sys
ETA = 0.94995553
def run(n, q, c, CAP):
    seen = set(); x = n; harm = 0.0; lxi = 0.0; lv = {}
    k = 0; a = 0; esc = False
    from math import log1p
    while x not in seen:
        if x.bit_length() > CAP: esc = True; break
        seen.add(x); harm += 1.0 / x
        L = x.bit_length(); lv[L] = lv.get(L, 0) + 1
        if x & 1: lxi += log1p(c / (q * x)); a += 1; x = (q * x + c) // 2
        else: x //= 2
        k += 1
    cum = 0; soj = 0.0
    for L in sorted(lv):
        cum += lv[L]; soj = max(soj, cum / 2 ** (ETA * L))
    return harm, lxi, soj, esc, k, a
for q, c, NMAX, CAP in [(5, 1, 30001, 300), (3, 1, 30001, 300), (3, -1, 30001, 300)]:
    best = [(-1, 0)] * 3; nesc = 0; minl = (9, 0)
    for n in range(1, NMAX, 2):
        h, lx, sj, esc, k, a = run(n, q, c, CAP)
        nesc += esc
        for i, v in enumerate((h, lx, sj)):
            if v > best[i][0]: best[i] = (v, n)
        if lx < minl[0]: minl = (lx, n)
    print("q=%d c=%+d odd n<%d cap 2^%d: escapes=%d | sup harm=%.4f (n=%d) | sup log prod=%.4f (n=%d) inf log prod=%.4f (n=%d) | sup N(2^L)/2^(eta L)=%.4f (n=%d)"
          % (q, c, NMAX, CAP, nesc, best[0][0], best[0][1], best[1][0], best[1][1], minl[0], minl[1], best[2][0], best[2][1]))
    sys.stdout.flush()
# the orbit of 7 under 5n+1, long run, exact integers
import mpmath as mp
mp.mp.dps = 60
x = 7; K = 20000; a = 0; harm = mp.mpf(0); lxi = mp.mpf(0); seen_small = 0; mn_after = None
W = []; xs = []
for k in range(K):
    xs.append(x); harm += mp.mpf(1) / x
    if x & 1: lxi += mp.log1p(mp.mpf(1) / (5 * x)); a += 1; x = (5 * x + 1) // 2
    else: x //= 2
print("5n+1, n=7, K=%d steps: bits(x_K)=%d  a_K/K=%.5f (critical 1/log2 5=%.5f)  log2(x_K)/K=%.5f" % (K, x.bit_length(), a / K, 1 / log2(5), x.bit_length() / K))
print("   sum 1/x_k = %s   xi_K = prod(1+1/(5x_i)) = %s" % (mp.nstr(harm, 20), mp.nstr(mp.exp(lxi), 20)))
print("   min of x_k for k>=100: 2^%d, for k>=1000: 2^%d, for k>=10000: 2^%d" % (min(xs[100:]).bit_length() - 1, min(xs[1000:]).bit_length() - 1, min(xs[10000:]).bit_length() - 1))
# real shadow: nu = lim x_k 2^k/5^(a_k); delta_k = nu*5^(a_k)/2^k - x_k, compare with the series sum (1/5) 2^(i-k)/5^(a_i-a_k)
nu = mp.mpf(7) * mp.exp(lxi)
ak = 0
for k in range(0, 41):
    if k in (0, 1, 2, 3, 5, 10, 20, 40):
        y = nu * mp.mpf(5) ** ak / mp.mpf(2) ** k
        # series from the future word
        d = mp.mpf(0); M = mp.mpf(1)
        for i in range(k, k + 3000):
            if xs[i] & 1: d += M / 5; M *= mp.mpf(2) / 5
            else: M *= 2
        print("   k=%2d x_k=%d  nu*5^a/2^k - x_k = %s   series delta_k = %s" % (k, xs[k], mp.nstr(y - xs[k], 15), mp.nstr(d, 15)))
    if xs[k] & 1: ak += 1
