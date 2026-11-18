#!/usr/bin/env python3
"""Robustness check for construction (C) of nonperiodic.py (rank-1 compression):
 1. alternating optimisation from random starting v (log-uniform in [1, 20]);
 2. for (k, j) = (2,1), (3,1): exhaustive log-grid over v (3 values, v_min = 1) with an
    LP in u for each fixed v  (bilinear problem -> LP once v is fixed).
Floating point search; numerical evidence only.
usage: nonperiodic_c_check.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
import nonperiodic as NP


def rho_sep_from(k, j, gam, maps, v0, sweeps=40):
    K = k + j
    nu, nv = 3 ** (k - 1), 3 ** j
    u, v = np.ones(nu), v0.copy()
    best = 0.0
    for _ in range(sweeps):
        for which in (0, 1):
            for _ in range(400):
                c = np.outer(v, u).ravel()
                R = (NP.Fmap(c, K, gam, maps) / c).reshape(nv, nu)
                g = R.min(axis=0) if which == 0 else R.min(axis=1)
                if g.max() / g.min() - 1 < 1e-10:
                    break
                if which == 0:
                    u = u * g; u /= u.min()
                else:
                    v = v * g; v /= v.min()
        cur = float(R.min())
        if cur - best < 1e-12:
            break
        best = cur
    return float(R.min()), v


def lp_u_feasible(k, j, gam, v, maps):
    """exists u >= 1 with (u (x) v) <= F(u (x) v)?  rows are linear in u for fixed v
    (min over lifts -> one row per lift)."""
    K = k + j
    N, N3, t, ev, r = maps
    nu = 3 ** (k - 1)
    A, B, C = 4.0 ** -gam, 0.75 ** gam, 1.5 ** gam
    rows = []
    for i in range(N):
        coefs = [B, 0.0, C][t[i]]
        lifts = [r[i] + s * N3 for s in range(3)] if coefs else [None]
        for l in lifts:
            row = np.zeros(nu)
            row[i % nu] += v[i // nu]
            row[ev[i] % nu] -= A * v[ev[i] // nu]
            if l is not None:
                row[l % nu] -= coefs * v[l // nu]
            rows.append(row)
    res = linprog(np.zeros(nu), A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                  bounds=[(1.0, 1e6)] * nu, method="highs")
    return res.status == 0


def main():
    rng = np.random.default_rng(1)
    G = {K: NP.gamma_full(K)[0] for K in range(2, 8)}
    print("1. random restarts of the alternating scheme: rho_sep at gamma_k + 1e-4 (rho >= 1 would be a gain)")
    for k, j in ((2, 1), (2, 2), (3, 1), (3, 2), (4, 1), (4, 2), (5, 1)):
        maps = NP.level_maps(k + j)
        best = 0
        for _ in range(30):
            v0 = np.exp(rng.uniform(0, 3, 3 ** j)); v0 /= v0.min()
            best = max(best, rho_sep_from(k, j, G[k] + 1e-4, maps, v0)[0])
        print(f"   k={k} j={j}: best rho over 30 starts at gamma_k+1e-4 = {best:.8f}")
    print("2. exhaustive grid over v (j=1), LP in u: feasible at gamma_k + 1e-4 ?  and at gamma_k - 1e-4 ?")
    grid = np.exp(np.linspace(0, np.log(50), 40))
    for k in (2, 3):
        maps = NP.level_maps(k + 1)
        nfeas_hi = nfeas_lo = n = 0
        for pos in range(3):
            for x, y in itertools.product(grid, grid):
                v = np.ones(3); v[(pos + 1) % 3] = x; v[(pos + 2) % 3] = y
                n += 1
                nfeas_hi += lp_u_feasible(k, 1, G[k] + 1e-4, v, maps)
        for v in (np.ones(3),):
            nfeas_lo += lp_u_feasible(k, 1, G[k] - 1e-4, v, maps)
        print(f"   k={k} j=1: {nfeas_hi} of {n} grid points v feasible at gamma_k+1e-4; v=1 feasible at gamma_k-1e-4: {bool(nfeas_lo)}")


if __name__ == "__main__":
    main()
