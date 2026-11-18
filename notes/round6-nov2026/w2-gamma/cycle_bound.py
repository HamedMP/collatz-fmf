"""Eliahou-type lower bound on the length of a nontrivial positive 3n+1 cycle.
T(n)=n/2 (even), (3n+1)/2 (odd). Cycle with K odd terms, L terms in all, min element m > X0:
   2^L = prod_{odd x}(3+1/x)  =>  0 < L - K*theta <= K*log2(1+1/(3*X0)),  theta=log2(3).
We find, for each X0, the fraction L/K with least K in (theta, theta+delta], delta=log2(1+1/(3 X0)),
by an exact Stern-Brocot ("simplest fraction in an interval") search on rational enclosures of the
endpoints (mpmath, 200 digits; endpoints are perturbed by 1e-150 both ways and the answer must agree).
"""
from mpmath import mp, mpf, log, floor
from fractions import Fraction
mp.dps = 200
theta = log(3)/log(2)

def simplest_between(lo, hi):
    """least-denominator fraction p/q with lo < p/q <= hi (lo<hi positive mpf)."""
    # continued-fraction descent
    a = floor(lo)
    if a + 1 <= hi:
        return int(a) + 1, 1
    # lo and hi share integer part a (hi < a+1)
    if hi == a:  # cannot happen since lo<hi and floor(lo)=a
        raise ValueError
    # x = a + 1/y, lo<x<=hi  <=> 1/(hi-a) <= y < 1/(lo-a) (lo-a may be 0 -> inf)
    flo, fhi = lo - a, hi - a
    ylo = 1/fhi
    if flo == 0:
        p, q = int(mp.ceil(ylo)), 1
    else:
        yhi = 1/flo
        p, q = simplest_between_lc(ylo, yhi)
    return int(a)*p + q, p

def simplest_between_lc(lo, hi):
    """least-denominator fraction with lo <= p/q < hi."""
    a = floor(lo)
    if a == lo:
        return int(a), 1
    if a + 1 < hi:
        return int(a) + 1, 1
    flo, fhi = lo - a, hi - a
    # x=a+1/y, lo<=x<hi <=> 1/fhi < y <= 1/flo
    p, q = simplest_between(1/fhi, 1/flo)
    return int(a)*p + q, p

def bound(X0):
    delta = log(1 + mpf(1)/(3*X0))/log(2)
    res = []
    for e in (mpf(0), mpf(10)**-150, -mpf(10)**-150):
        res.append(simplest_between(theta + e, theta + delta - e))
    assert res[0] == res[1] == res[2], res
    L, K = res[0]
    # sanity
    assert 0 < L - K*theta <= K*delta
    return L, K

if __name__ == "__main__":
    print("X0=2^j : min K (odd terms), min L (T-steps), L+K (3n+1 & n/2 steps counted separately)")
    prev = None
    for j in list(range(60, 101)) + [110, 120, 128, 150, 200]:
        L, K = bound(mpf(2)**j)
        if (L, K) != prev:
            print(f"j={j:4d}  K={K}  L={L}  L+K={L+K}")
        prev = (L, K)
    # exact threshold at which the 2^71 answer stops being admissible
    L, K = bound(mpf(2)**71)
    eps = L - K*theta
    # admissible iff eps <= K log2(1+1/(3X0)) iff X0 <= 1/(3(2^(eps/K)-1))
    X = 1/(3*(mpf(2)**(eps/K) - 1))
    print("2^71 candidate (L,K)=", (L, K), "dies when X0 >", mp.nstr(X, 25), "= 2^", mp.nstr(log(X)/log(2), 12))
    # denominators of convergents of theta for reference
    x = theta; h0,h1,k0,k1 = 1,0,0,1  # h_{-1},h_{-2}...
    conv = []
    for i in range(30):
        a = int(floor(x)); h0,h1 = a*h0+h1,h0; k0,k1 = a*k0+k1,k0
        conv.append((a,h0,k0)); x = 1/(x-a)
    print("convergents (a_i, p_i, q_i):")
    for c in conv: print("  ", c)
    # thresholds: for each successive candidate (L,K), the X0 beyond which plain Eliahou excludes it,
    # and the threshold under the equidistribution refinement (Lemma C2 of REPORT.md): X0 -> X0 * 2 ln 2.
    print("candidate (L,K): excluded by plain Eliahou iff X0 > 2^t ; by refined Lemma C2 iff X0 > 2^(t - 0.4712)")
    X0 = mpf(2)**60
    for _ in range(12):
        L, K = bound(X0)
        eps = L - K*theta
        X = 1/(3*(mpf(2)**(eps/K) - 1))
        t = log(X)/log(2)
        print(f"  L={L} K={K}: t={mp.nstr(t,10)}  refined t'={mp.nstr(t - log(2*log(2))/log(2),10)}")
        X0 = X*(1+mpf(10)**-30)
