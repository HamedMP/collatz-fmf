#!/usr/bin/env python3
"""Generic Krasikov-Lagarias-type system for T(n) = n/2 (even), (P n + D)/2 (odd),
P odd prime with 2 a primitive root (3 or 5), D = +1 or -1.  Floating-point search
(numpy), built directly from residues; second, independent implementation of the
P=3, D=1 system (klrho.c uses closed-form index arithmetic instead).

Principal class: residues m mod P^k with P | 2m - D  (m = r0 mod P).
E = ord_P(2).  Row for principal m:
   c[m] <= 2^(-E gamma) c[2^E m]  +  [b != 0 mod P] (P / 2^(j+1))^gamma * min_lifts c[2^j b + t P^(k-1)]
with b = (2m - D)/P mod P^(k-1) and j in [0,E) minimal with 2^j b = r0 mod P.
(For D = +1 this is KL's system when P = 3.  For D = -1 the row is the formal
analogue; see REPORT.md for why the soundness proof needs D = +1.)

usage: gen_lp.py P D K [--wfile OUT] [--back S]
   prints gamma_k (bisection on the growth factor rho(gamma) = 1) and optionally
   writes a pistar weight file at gamma = gamma_k - S (default S = 1e-6).
"""
import sys

import numpy as np


def build(P, D, k):
    M, M1 = P ** k, P ** (k - 1)
    r0 = next(r for r in range(P) if (2 * r - D) % P == 0)
    E = next(e for e in range(1, P) if pow(2, e, P) == 1)
    m = np.arange(r0, M, P, dtype=np.int64)            # principal residues; index (m - r0)/P
    idx = lambda x: (x - r0) // P
    ev = idx((m * (2 ** E)) % M)
    b = ((2 * m - D) // P) % M1
    assert np.all((2 * m - D) % P == 0)
    live = (b % P) != 0
    j = np.zeros_like(b)
    for jj in range(E - 1, -1, -1):
        j[((b * 2 ** jj) % P == r0)] = jj
    tgt = (b * 2 ** j) % M1
    assert np.all((tgt[live] % P) == r0)
    lifts = np.stack([idx(tgt + t * M1) for t in range(P)])     # garbage where not live
    lifts[:, ~live] = 0
    return dict(P=P, D=D, k=k, M=M, r0=r0, E=E, m=m, ev=ev, live=live, j=j, lifts=lifts)


def F(S, c, gam):
    P, E = S["P"], S["E"]
    out = 2.0 ** (-E * gam) * c[S["ev"]]
    coef = (P / 2.0 ** (S["j"] + 1)) ** gam
    out = out + np.where(S["live"], coef * c[S["lifts"]].min(axis=0), 0.0)
    return out


def rho(S, gam, c=None, tol=1e-12, maxit=200000):
    if c is None:
        c = np.ones(len(S["m"]))
    for _ in range(maxit):
        f = F(S, c, gam)
        r = f / c
        if r.max() / r.min() - 1 < tol:
            break
        c = f / f.min()
    return r.min(), r.max(), c / c.min()


def gamma_k(S, lo=0.01, hi=1.2):
    c = None
    while hi - lo > 1e-10:
        mid = 0.5 * (lo + hi)
        a, b, c = rho(S, mid, c)
        if a * b >= 1:
            lo = mid
        else:
            hi = mid
    return lo, hi


def main():
    P, D, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    back = float(sys.argv[sys.argv.index("--back") + 1]) if "--back" in sys.argv else 1e-6
    S = build(P, D, k)
    lo, hi = gamma_k(S)
    g = lo - back
    a, b, c = rho(S, g)
    print(f"map ({P}n{D:+d})/2 k={k} classes={len(S['m'])} gamma_k in [{lo:.9f},{hi:.9f}] "
          f"lambda={2 ** lo:.7f}; at gamma={g:.9f}: rho in [{a:.10f},{b:.10f}] spread={c.max():.6f}")
    if "--wfile" in sys.argv:
        assert a >= 1.0, "not feasible in floating point"
        with open(sys.argv[sys.argv.index("--wfile") + 1], "w") as f:
            f.write(f"{k} {g:.12f}\n")
            for mm, cc in zip(S["m"], c):
                f.write(f"{mm} {cc:.15g}\n")


if __name__ == "__main__":
    main()
