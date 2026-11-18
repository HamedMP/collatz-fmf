#!/usr/bin/env python3
"""w2-delta s2: exact bad-mass constants.
 b_L(s)   = #{v in {0,1}^L : 3^a(v) * 2^(s+1) > 2^L}      (the "bad" parity vectors at level L)
 bo_L(s)  = same with v_0 = 1                              (bad odd integers)
 beta_all(L0) = sum_{L>=L0} b_L/2^L ,  beta_odd(L0) = sum_{L>=L0} bo_L/2^L   (exact rationals up to LMAX, rigorous tail)
Run: taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python s2_constants.py
"""
from fractions import Fraction
from math import comb, log2
LMAX = 1200

def H2(t): return -t*log2(t) - (1-t)*log2(1-t)
eta = H2(1/log2(3))
print("eta = H2(log_3 2) = %.8f ; 2^eta = %.6f" % (eta, 2**eta))

def terms(s, q=3, Lmax=LMAX):
    out = []
    for L in range(Lmax):
        amin = 0
        while q**amin * 2**(s + 1) <= 2**L: amin += 1            # bad iff a >= amin
        tot = sum(comb(L, a) for a in range(amin, L + 1))
        odd = sum(comb(L - 1, a - 1) for a in range(max(amin, 1), L + 1)) if L >= 1 else 0
        out.append((tot, odd))
    return out

res = {}
for s in (2, 3, 4):
    tm = terms(s)
    th = (LMAX - s - 1) / (LMAX * log2(3)); rate = 1 - H2(th)     # Chernoff: P(Bin(L,1/2)>=th L) <= 2^{-L(1-H2(th))}, th increasing in L
    tail = 2**(-rate * LMAX) / (1 - 2**(-rate))
    print("s=%d  c=3/2^s=%.4f  rigorous tail(L>=%d) <= %.2e" % (s, 3 / 2**s, LMAX, tail))
    sa = Fraction(0); so = Fraction(0); suf = {}
    for L in range(LMAX - 1, -1, -1):
        sa += Fraction(tm[L][0], 2**L); so += Fraction(tm[L][1], 2**L); suf[L] = (sa, so)
    for L0 in (0, 4, 16, 20, 24, 26, 27, 28, 30, 32, 40, 71):
        ba = float(suf[L0][0]) * (1 + 1e-12) + tail; bo = float(suf[L0][1]) * (1 + 1e-12) + tail
        res[(s, L0)] = (ba, bo)
        print("   L0=%2d  beta_all=%.6f  beta_odd=%.6f" % (L0, ba, bo))
    if s == 3:
        sup = max((2.0**(log2(tm[L][0] + L) - eta * L), L) for L in range(LMAX))
        print("   Theorem S: sup_{L<%d} (b_L+L)/2^(eta L) = %.4f at L=%d ; K = sup/(1-2^-eta-2^-3eta) = %.4f"
              % (LMAX, sup[0], sup[1], sup[0] / (1 - 2**-eta - 2**(-3 * eta))))

print("Tier-1 constant (Theorem H, any distinct segment): sum 1/x_k <= (beta_all(0)+1)/(1-3/2^s):")
for s in (2, 3, 4):
    print("   s=%d: %.4f" % (s, (res[(s, 0)][0] + 1) / (1 - 3 / 2**s)))

for L in (50, 200, 800):
    t5 = terms(3, 5, L + 1)[L][0]; t3 = terms(3, 3, L + 1)[L][0]
    print("litmus q=5: bad fraction at L=%d is %.6f   (q=3: %.3e)" % (L, t5 / 2**L, t3 / 2**L))
