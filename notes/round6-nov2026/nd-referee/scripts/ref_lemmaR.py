"""Independent check of Lemma R of PROOFS.md (referee's own code, no reuse of sC).

K(beta, gamma, t, m0) := sum_ell 2^{1-frac(g(ell))} P(S_{ell-m0} = ceil(g(ell)) - t),
  g(ell) = ell*beta + gamma,  P(S_k = s) = C(s-1,k-1) 2^{-s}  (sum of k iid Geom(2)).
Claim (beta = log2 3): K -> 1/ln(4/3) uniformly in gamma, t.
General prediction for any slope beta < 2:  K -> (1/(2-beta)) * mean of 2^{1-u} along the orbit
  = 1/((2-beta) ln 2) if beta irrational; gamma-DEPENDENT if beta rational.
Arithmetic: lgamma in float64 (relative error ~1e-12 on each term), frac via mpmath 60 digits.
Run:  python ref_lemmaR.py
"""
import math, random
from mpmath import mp, mpf, floor as mfloor, log as mlog

mp.dps = 60
B3 = mlog(3) / mlog(2)
LN2 = math.log(2.0)


def logP(k, s):
    if k == 0:
        return 0.0 if s == 0 else -math.inf
    if s < k:
        return -math.inf
    return math.lgamma(s) - math.lgamma(k) - math.lgamma(s - k + 1) - s * LN2


def K(beta, gamma, t, m0, kcen):
    """beta, gamma mpf.  Sum over ell with k=ell-m0 within 12 sigma of the centre kcen."""
    d = 2 - float(beta)
    half = int(12 * math.sqrt(2 * kcen) / abs(d)) + 50
    ell_c = kcen + m0
    tot = 0.0
    for ell in range(max(m0 + 1, ell_c - half), ell_c + half + 1):
        g = ell * beta + gamma
        fl = mfloor(g)
        u = float(g - fl)
        s = int(fl) + (1 if u > 0 else 0)       # ceil
        lp = logP(ell - m0, s - t)
        if lp > -700:
            tot += 2.0 ** (1.0 - u) * math.exp(lp)
    return tot


def gamma_for(beta, t, m0, kcen, phase):
    # centre condition: g(ell) - t - 2(ell-m0) = 0 at ell = kcen+m0, plus a free phase in [0,1)
    ell = kcen + m0
    return mpf(t) + 2 * kcen - ell * beta + mpf(phase)


def sweep(beta, label, target, scales, m0s=(3, 20), nph=24, seed=1):
    rnd = random.Random(seed)
    print(f"--- slope {label}; predicted limit {target:.10f}")
    for kcen in scales:
        worst = 0.0; lo = 9e9; hi = -9e9
        for m0 in m0s:
            for _ in range(nph):
                t = 2 * m0 + rnd.randint(-int(3 * math.sqrt(m0)) - 1, int(3 * math.sqrt(m0)) + 1)
                ph = rnd.random() * 3 - 1.5
                v = K(beta, gamma_for(beta, t, m0, kcen, ph), t, m0, kcen)
                lo = min(lo, v); hi = max(hi, v); worst = max(worst, abs(v - target))
        print(f"  k*={kcen:>7}  min K={lo:.8f}  max K={hi:.8f}  max|K-target|={worst:.3e}")


if __name__ == "__main__":
    T3 = 1.0 / math.log(4.0 / 3.0)
    print("1/ln(4/3) =", T3)
    scales = [30, 100, 300, 1000, 3000, 10000, 30000, 100000]
    sweep(B3, "log2(3)  [3n+1 and 3n-1]", T3, scales)
    # rational slopes: no equidistribution, K must depend on the phase gamma
    for (p, q) in [(3, 2), (8, 5), (19, 12)]:
        b = mpf(p) / q
        sweep(b, f"{p}/{q} (rational control)", 1.0 / ((2 - p / q) * LN2), scales[2:6])
    # good rational approximations of log2 3 with large denominator behave like log2 3 at small scales
    b = mpf(1054) / 665
    sweep(b, "1054/665 (convergent of log2 3)", 1.0 / ((2 - 1054 / 665) * LN2), [1000, 100000])
    # a Liouville-like slope: beta = 8/5 + 1e-9 : equidistributes only at scale >> 1e9
    b = mpf(8) / 5 + mpf(10) ** -9
    sweep(b, "8/5+1e-9 (near-rational: shows why an irrationality MEASURE is needed)",
          1.0 / ((2 - 1.6) * LN2), [1000, 100000])
    # 5n+1 analogue: slope log2 5 > 2 (positive drift).  The renewal sum still converges
    # (to 1/((log2 5 - 2) ln 2) = 1/ln(5/4)); Lemma R alone does not see the sign of the drift.
    B5 = mlog(5) / mlog(2)
    sweep(B5, "log2(5)  [5n+1: drift sign enters elsewhere]", 1.0 / math.log(5.0 / 4.0), [300, 3000, 30000])
