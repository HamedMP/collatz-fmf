#!/usr/bin/env python3
"""w2-delta s6: final explicit constants for Theorem H / Corollary R (weak residue bound).
Uses the sharpened descent lemma (Lemma 2'): for x in [2^L,2^(L+1)) with a odd steps among the first L,
     3^a (2^a + 1) <= 2^(L-s+a)   ==>   T^L(x) <= x / 2^s .
Bad vectors at level L: 3^a (2^a+1) > 2^(L-s+a).  b_L = #bad, bo_L = #bad with first bit 1.
Mass bounds (distinct integers in [2^L, 2^(L+1))):
     sum_{bad x} 1/x <= min(b_L/2^L, 2^-L + ln(1 + b_L/2^L)),   sum_{bad odd x} 1/x <= min(bo_L/2^L, 2^-L + (1/2) ln(1 + 2 bo_L/2^L)).
Run: taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python s6_final_constants.py [L0 M_B P_B H_B]
"""
import sys
from fractions import Fraction
from math import comb, log2, log, exp, log1p
LMAX = 1400

def H2(t): return -t*log2(t) - (1-t)*log2(1-t)

def masses(s, q=3):
    """per-level upper bounds (floats rounded up by 1e-12 relative) for all / odd bad mass"""
    out = []
    for L in range(LMAX):
        amin = 0
        while q**amin * (2**amin + 1) <= 2**(L - s + amin) if L - s + amin >= 0 else False: amin += 1
        tot = sum(comb(L, a) for a in range(amin, L + 1))
        odd = sum(comb(L - 1, a - 1) for a in range(max(amin, 1), L + 1)) if L >= 1 else 0
        pa = float(Fraction(tot, 2**L)); po = float(Fraction(odd, 2**L))
        # distinct integers >= M=2^L:  sum_{i<b} 1/(M+i) <= 1/M + ln(1+(b-1)/M);  odd ones: <= 1/M + (1/2) ln(1+2b/M)
        ma = min(pa, log1p(pa) + 2.0**(-L)); mo = min(po, 0.5 * log1p(2 * po) + 2.0**(-L))
        out.append((ma * (1 + 1e-12), mo * (1 + 1e-12), pa, po))
    return out

def tail(s):
    # L >= LMAX: bad => a > (L-s-1)/log2(3) (since 3^a(1+2^-a) > 2^(L-s) implies 3^a > 2^(L-s-1));
    # Chernoff P(Bin(L,1/2) >= th L) <= 2^(-L(1-H2(th))), th = (LMAX-s-1)/(LMAX log2 3) (increasing in L)
    th = (LMAX - s - 1) / (LMAX * log2(3)); rate = 1 - H2(th)
    return 2**(-rate * LMAX) / (1 - 2**(-rate))

args = sys.argv[1:]
cases = [(26, 0.225654112732, 339, 1.936739)] if not args else [(int(args[0]), float(args[1]), int(args[2]), float(args[3]))]
SS = (2, 3, 4, 5)
data = {}
for s in SS:
    ms = masses(s); tl = tail(s)
    suf_all = [0.0] * (LMAX + 1); suf_odd = [0.0] * (LMAX + 1)
    for L in range(LMAX - 1, -1, -1):
        suf_all[L] = suf_all[L + 1] + ms[L][0]; suf_odd[L] = suf_odd[L + 1] + ms[L][1]
    data[s] = (suf_all, suf_odd, tl)
    c = 2.0 / 2**s                       # contraction constant c = 2^(1-s)  (ancestor lemma)
    print("s=%d c=%.4f tail<=%.1e  beta_all(0)=%.5f  tier-1: sum 1/x_k <= (beta_all(0)+1)/(1-c) = %.4f"
          % (s, c, tl, suf_all[0] + tl, (suf_all[0] + tl + 1) / (1 - c)))

def bounds(L0, eps):
    U = min((data[s][0][L0] + data[s][2] + eps) / (1 - 2.0 / 2**s) for s in SS)
    W = min(data[s][1][L0] + data[s][2] + eps + (2.0 / 2**s) * U for s in SS)
    return U, W

for (L0, MB, PB, HB) in cases:
    eps = (L0 + 1) * 2.0**(-L0) + (PB + 2) * 2.0**(1 - L0)
    U, W = bounds(L0, eps)
    S = MB + 1e-9 + W / 3
    for s in SS:
        print("   L0=%d s=%d: beta_all=%.5f beta_odd=%.5f" % (L0, s, data[s][0][L0] + data[s][2], data[s][1][L0] + data[s][2]))
    print("FINAL L0=%d: eps=%.2e  U(all, levels>=L0) <= %.5f   W_odd(levels>=L0) <= %.5f" % (L0, eps, U, W))
    print("   => log Res <= M_B + W_odd/3 = %.5f ,  Res(n) <= %.4f  for every n reaching 1" % (S, exp(S)))
    print("   => any distinct segment: prod over odd elements (1+1/(3x)) <= (4/3)*%.4f = %.4f ; sum of 1/x_k <= %.4f (1 and 2 included: +1)"
          % (exp(S), 4 / 3 * exp(S), HB + 1e-6 + 1 + U))
for L0 in (32, 40, 60, 68, 71):
    U, W = bounds(L0, (L0 + 1) * 2.0**(-L0))
    print("orbit segments with all elements >= 2^%d: sum 1/x <= %.5f, odd sum <= %.5f, product <= %.5f" % (L0, U, W, exp(W / 3)))
