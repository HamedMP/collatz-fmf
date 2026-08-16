"""sC_lemmaR.py — check of Lemma R (renewal-Gaussian-equidistribution assembly).

Claim: with g(ell) = ell*log2(3) + G0 (G0 = log2(y/M), arbitrary real offset),
s*(ell) = ceil(g(ell)), and P(S_ell = s) = C(s-1, ell-1)/2^s the EXACT law of a
sum of ell iid Geom(2) letters,

    K := sum_ell 2^{1 - {g(ell)}} * P(S_ell = s*(ell) - t)   --->  1/ln(4/3)
         = 3.476059496782207...

uniformly in the offset G0 (mod 1 phase), the integer shift t = O(sqrt),
and the window phase — this is the constant that turns the uniform-window
count into Tao's log-uniform limit Q.  Mechanism: the Gaussian profile of
P(S_ell = .) sweeps the moving target at drift 2 - log2(3) per step
(contributing 1/(2-log2 3)) while {g(ell)} equidistributes ({ell log2 3},
Rhin/Erdos-Turan) making E[2^{1-u}] -> 1/ln 2; product = 1/ln(4/3).

Exact ingredients: binomials exact (Python ints), 2^{-s} exact shifts; {g(ell)}
via mpmath 80 digits.  Reported: K over a grid of offsets G0 and shifts t at
center scales L = 300, 1000, 3000, 10000; max |K - 1/ln(4/3)| and its decay.
"""
import sys
from math import comb, floor
from mpmath import mp, mpf, log, ceil as mpceil

mp.dps = 80
LOG23 = log(3) / log(2)
TARGET = 1 / (2 * log(2) - log(3))  # 1/ln(4/3)

def report(name, ok, detail=""):
    print(f"[{name}] {'PASS' if ok else 'FAIL'} {detail}", flush=True)
    if not ok:
        sys.exit(f"FAILED: {name}")

def pS(ell, s):
    """exact P(S_ell = s) as float via integer arithmetic (safe scaling)."""
    if s < ell:
        return 0.0
    c = comb(s - 1, ell - 1)
    # c / 2^s with controlled exponent
    bl = c.bit_length()
    sh = bl - 53
    if sh > 0:
        m = c >> sh
    else:
        m = c << (-sh)
        sh = 0
    # value = m * 2^{sh - s}
    import math as _m
    return _m.ldexp(float(m), sh - s)

def K_sum(G0, t, Lc):
    """sum over ell in a window around center scale Lc capturing the Gaussian.
    Window = 14 sigmas (sigma = sqrt(2 ell)); truncation error < exp(-14^2/4) ~ 5e-22."""
    # center: s* - 2ell ~ 0 when g(ell) = 2ell => ell0 = G0/(2 - log23)
    ell0 = int(G0 / float(2 - LOG23))
    W = int(14 * ((2 * ell0) ** 0.5) / (2 - float(LOG23))) + 40
    tot = 0.0
    import math as _m
    for ell in range(max(1, ell0 - W), ell0 + W):
        g = ell * LOG23 + G0
        gf = int(floor(g))
        su = gf + 1 - t          # ceil for non-integer g
        frac = float(g - gf)
        w = 2.0 ** (1 - frac)
        p = pS(ell, su)
        if p:
            tot += w * p
    return tot

def main():
    print(f"  target 1/ln(4/3) = {float(TARGET):.12f}\n")
    print("   Lc      offset-phase   shift-t     K              K-target")
    worst_by_L = {}
    import random
    rng = random.Random(11)
    for Lc in (300, 1000, 3000, 6000):
        G0base = mpf(Lc) * (2 - LOG23)
        worst = 0.0
        for trial in range(6):
            phase = mpf(rng.random())
            t = rng.choice([0, 1, -3, 7, -15, 25])
            K = K_sum(G0base + phase, t, Lc)
            err = float(abs(K - TARGET))
            worst = max(worst, err)
            if trial < 3:
                print(f"  {Lc:6d}   {float(phase):.6f}      {t:4d}     {float(K):.9f}   {err:+.2e}")
        worst_by_L[Lc] = worst
        print(f"  {Lc:6d}   worst over 6 (phase,t) draws: {worst:.3e}")
    ok = all(worst_by_L[L2] < worst_by_L[L1] * 1.2 for L1, L2 in [(300, 3000), (1000, 6000)]) \
         and worst_by_L[6000] < 5e-3
    report("C1", ok, f"K -> 1/ln(4/3); worst errors by scale: { {k: f'{v:.1e}' for k, v in worst_by_L.items()} }")
    # sanity: the two factors separately
    #   sum_ell P(S_ell = s*(ell)) -> 1/(2 - log2 3);   E[2^{1-u}] -> 1/ln 2
    Lc = 3000
    G0 = mpf(Lc) * (2 - LOG23) + mpf('0.377')
    ell0 = Lc
    W = int(14 * ((2 * ell0) ** 0.5) / (2 - float(LOG23))) + 40
    s_only = sum(pS(ell, int(mpceil(ell * LOG23 + G0))) for ell in range(ell0 - W, ell0 + W))
    print(f"\n  factor check: sum_ell P(S_ell = s*) = {s_only:.6f} vs 1/(2-log2 3) = {float(1/(2-LOG23)):.6f}")
    ok2 = abs(s_only - float(1 / (2 - LOG23))) < 2e-2
    report("C2", ok2, "Gaussian-sweep factor matches 1/(2 - log2 3) = 2.40942...")
    print("\nALL sC CHECKS COMPLETE", flush=True)

main()
