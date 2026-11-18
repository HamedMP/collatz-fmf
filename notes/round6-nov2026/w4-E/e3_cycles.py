#!/usr/bin/env python3
"""w4-E e3: level-dependent harmonic constants (logic of w2-delta/s6_final_constants.py, re-implemented with
row-by-row exact binomials) and the cycle constraint
   0 < p ln2 - a ln3 <= min(a/(3m), W_odd(L0)/3),  m = min of the cycle >= 2^L0.
Bad vectors at level L (for s): 3^a (2^a+1) > 2^(L-s+a).
Run: taskset -c 4 python e3_cycles.py
"""
from fractions import Fraction
from math import log2, log, exp, log1p
LMAX = 2600
def H2(t): return -t*log2(t) - (1-t)*log2(1-t)
SS = (2, 3, 4, 5, 6, 7, 8)
data = {}
pw3 = [3**a for a in range(LMAX + 2)]
acc = {s: ([0.0] * LMAX, [0.0] * LMAX) for s in SS}
amin = {s: 0 for s in SS}
row = [1]; prev = None
for L in range(LMAX):
    if L > 0:
        prev = row; row = [1] + [prev[i] + prev[i + 1] for i in range(L - 1)] + [1]
    suf = [0] * (L + 2)                       # suf[a] = sum_{j>=a} C(L,j)
    for a in range(L, -1, -1): suf[a] = suf[a + 1] + row[a]
    sufp = [0] * (L + 1)                      # sufp[b] = sum_{j>=b} C(L-1,j)
    if L >= 1:
        for a in range(L - 1, -1, -1): sufp[a] = sufp[a + 1] + prev[a]
    for s in SS:
        if L - s < 0: am = 0
        else:
            while pw3[amin[s]] * (2**amin[s] + 1) <= 2**(L - s + amin[s]): amin[s] += 1
            am = amin[s]
        tot = suf[am] if am <= L else 0
        b = max(am, 1) - 1                    # odd bad: first bit 1, a-1 >= b ones among the other L-1
        odd = sufp[b] if (L >= 1 and b <= L - 1) else 0
        pa = float(Fraction(tot, 2**L)); po = float(Fraction(odd, 2**L))
        ma = min(pa, log1p(pa) + 2.0**(-L)); mo = min(po, 0.5 * log1p(2 * po) + 2.0**(-L))
        acc[s][0][L] = ma * (1 + 1e-12); acc[s][1][L] = mo * (1 + 1e-12)
for s in SS:
    suf_all = [0.0] * (LMAX + 1); suf_odd = [0.0] * (LMAX + 1)
    th = (LMAX - s - 1) / (LMAX * log2(3)); rate = 1 - H2(th)
    tl = 2**(-rate * LMAX) / (1 - 2**(-rate))
    for L in range(LMAX - 1, -1, -1):
        suf_all[L] = suf_all[L + 1] + acc[s][0][L]; suf_odd[L] = suf_odd[L + 1] + acc[s][1][L]
    data[s] = (suf_all, suf_odd, tl)
def bounds(L0):
    eps = (L0 + 1) * 2.0**(-L0)
    U = min((data[s][0][L0] + data[s][2] + eps) / (1 - 2.0 / 2**s) for s in SS)
    W = min(data[s][1][L0] + data[s][2] + eps + (2.0 / 2**s) * U for s in SS)
    return U, W
print("tail bounds at LMAX: " + " ".join("s=%d:%.1e" % (s, data[s][2]) for s in SS))
print("%6s %10s %10s %10s %12s %14s %12s" % ("L0", "U_all", "W_odd", "Lam_max", "frac_min", "W_odd*2^.05L", "a/m cross"))
for L0 in (32, 68, 71, 80, 100, 135, 150, 200, 300, 500, 800, 1000, 1500, 2000):
    U, W = bounds(L0)
    lam = W / 3
    print("%6d %10.5f %10.5f %10.6f %12.6f %14.4f %12.4f" % (L0, U, W, lam, 1 - lam / log(2), W * 2**(0.05004447 * L0), (exp(6 * lam) - 1) / 2))
mx = max((bounds(L0)[1] * 2**(0.05004447 * L0), L0) for L0 in range(71, 2401))
print("max over 71<=L0<=2400 of W_odd(L0)*2^((1-eta)L0) = %.4f at L0=%d  (so W_odd(L0) <= %.2f * 2^(-(1-eta) L0) on that range)" % (mx[0], mx[1], mx[0] + 0.01))
mx = max((bounds(L0)[0] * 2**(0.05004447 * L0), L0) for L0 in range(71, 2401))
print("max over 71<=L0<=2400 of U_all(L0)*2^((1-eta)L0) = %.4f at L0=%d" % mx)
