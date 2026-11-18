#!/usr/bin/env python3
"""Task 5: structured W for Lemma G that are NOT plain functions of a mod 3^k.
Floating point / LP search only (HiGHS); results are numerical, the negative results
for (A) and (B) are backed by Proposition N in REPORT.md.

(A) W(a) = w(a mod 3^k, a mod 2^j)                       -- 2-adic feature
(B) W(a) = w(a mod 3^k, floor(log2 a) mod J)             -- coarse size feature
    (rows required for every transition of the bucket that occurs for large a)
(C) W(a) = u(a mod 3^k) * v(digits k..k+j-1 of a in base 3)   -- rank-1 compression of a
    level-(k+j) vector: 3^(k-1) + 3^j parameters instead of 3^(k+j-1).
    Also the "transposed" split u(top digits) * v(low digits) is covered by exchanging
    the roles (k <-> j) since both orders of (k, j) are run.

For each construction: the largest gamma for which a positive solution of the Lemma G
row system exists, against the plain values gamma_k and gamma_{k+j}.

usage: nonperiodic.py
"""
import math

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def lp_feasible(nvar, rows, cmax=1e7):
    """rows: list of (lhs_var, [(coef, var), ...]) meaning x[lhs] <= sum coef*x[var].
    variables 1 <= x <= cmax (aux variables are included by the caller)."""
    ri, ci, vv = [], [], []
    for r, (lhs, terms) in enumerate(rows):
        ri.append(r); ci.append(lhs); vv.append(1.0)
        for coef, var in terms:
            ri.append(r); ci.append(var); vv.append(-coef)
    A = coo_matrix((vv, (ri, ci)), shape=(len(rows), nvar)).tocsr()
    res = linprog(np.zeros(nvar), A_ub=A, b_ub=np.zeros(len(rows)),
                  bounds=[(1.0, cmax)] * nvar, method="highs")
    return res.status == 0


def bisect(feas, lo=0.3, hi=1.0, tol=2e-7):
    assert feas(lo) and not feas(hi)
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if feas(mid):
            lo = mid
        else:
            hi = mid
    return lo


def system_feature(k, nfeat, f4, fb, f2b):
    """Lemma G rows for W = w(m, phi), m in [3^k], phi in range(nfeat).
    f4(phi), fb(phi), f2b(phi): sets of possible feature values of 4a, b=(2a-1)/3, 2b.
    The lift of b mod 3^k is not determined by (m, phi): min over the three lifts
    (auxiliary variables z <= each lift)."""
    M, M1 = 3 ** k, 3 ** (k - 1)
    res = [m for m in range(2, M, 3)]
    pos = {m: i for i, m in enumerate(res)}
    nc = len(res) * nfeat
    var = lambda m, p: pos[m] * nfeat + p
    aux = {}

    def zvar(r, p):          # min over lifts of w(., p) at class r mod 3^(k-1)
        if (r, p) not in aux:
            aux[(r, p)] = nc + len(aux)
        return aux[(r, p)]

    def rows(gam):
        A, B, C = 4.0 ** -gam, 0.75 ** gam, 1.5 ** gam
        out = []
        for m in res:
            for p in range(nfeat):
                r9 = m % 9
                for p4 in f4(p):
                    if r9 == 5:
                        out.append((var(m, p), [(A, var(4 * m % M, p4))]))
                    elif r9 == 2:
                        r = ((4 * m - 2) // 3) % M1
                        for q in f2b(p):
                            out.append((var(m, p), [(A, var(4 * m % M, p4)), (B, zvar(r, q))]))
                    else:
                        r = ((2 * m - 1) // 3) % M1
                        for q in fb(p):
                            out.append((var(m, p), [(A, var(4 * m % M, p4)), (C, zvar(r, q))]))
        for (r, q), z in list(aux.items()):
            for t in range(3):
                out.append((z, [(1.0, var(r + t * M1, q))]))
        return out

    rows(0.5)                 # populate aux
    return lambda gam: lp_feasible(nc + len(aux), rows(gam))


def gamma_plain(k):
    return bisect(system_feature(k, 1, lambda p: [0], lambda p: [0], lambda p: [0]))


def gamma_2adic(k, j):
    Q = 2 ** j
    inv3 = pow(3, -1, Q)
    return bisect(system_feature(k, Q, lambda s: [(4 * s) % Q],
                                 lambda s: [((2 * s - 1) * inv3) % Q],
                                 lambda s: [(2 * (2 * s - 1) * inv3) % Q]))


def gamma_size(k, J):
    # phi = floor(log2 a) mod J.  4a: +2.  b=(2a-1)/3: log2 b in (log2 a - 0.585.., ) => -1 or 0.
    # 2b: 0 or +1.  Both transitions occur for arbitrarily large a in every residue class.
    return bisect(system_feature(k, J, lambda p: [(p + 2) % J],
                                 lambda p: [(p - 1) % J, p],
                                 lambda p: [p, (p + 1) % J]))


# ---------- (C) rank-1 compression --------------------------------------------------
def level_maps(K):
    N, N3 = 3 ** (K - 1), 3 ** (K - 2)
    i = np.arange(N)
    u, t = i // 3, i % 3
    ev = (4 * i + 2) % N
    r = np.where(t == 0, (4 * u) % N3, (2 * u + 1) % N3)
    return N, N3, t, ev, r


def Fmap(c, K, gam, maps):
    N, N3, t, ev, r = maps
    A, B, C = 4.0 ** -gam, 0.75 ** gam, 1.5 ** gam
    cb = np.minimum(np.minimum(c[r], c[r + N3]), c[r + 2 * N3])
    return A * c[ev] + np.where(t == 0, B, np.where(t == 2, C, 0.0)) * cb


def rho_full(K, gam, maps, c=None):
    c = np.ones(maps[0]) if c is None else c
    for _ in range(20000):
        f = Fmap(c, K, gam, maps)
        r = f / c
        if r.max() / r.min() - 1 < 1e-11:
            break
        c = f / f.min()
    return math.sqrt(r.max() * r.min()), c / c.min()


def rho_sep(k, j, gam, maps, sweeps=60):
    """best growth factor over c = u (x) v, u on index mod 3^(k-1) (residue mod 3^k),
    v on the top j base-3 digits; alternating max-min power iterations (monotone ascent)."""
    K = k + j
    nu, nv = 3 ** (k - 1), 3 ** j
    u, v = np.ones(nu), np.ones(nv)
    best = 0.0
    for _ in range(sweeps):
        for which in (0, 1):
            for _ in range(400):
                c = np.outer(v, u).ravel()                # index = top * nu + low
                R = (Fmap(c, K, gam, maps) / c).reshape(nv, nu)
                g = R.min(axis=0) if which == 0 else R.min(axis=1)   # ratio G(u)/u resp. H(v)/v
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
    return float(R.min()), u, v


def gamma_sep(k, j, glo, ghi):
    maps = level_maps(k + j)
    lo, hi = glo - 1e-4, ghi + 1e-4
    while hi - lo > 1e-6:
        mid = 0.5 * (lo + hi)
        if rho_sep(k, j, mid, maps)[0] >= 1:
            lo = mid
        else:
            hi = mid
    return lo


def gamma_full(K):
    maps = level_maps(K)
    lo, hi = 0.3, 1.0
    c = None
    while hi - lo > 1e-9:
        mid = 0.5 * (lo + hi)
        r, c = rho_full(K, mid, maps, c)
        lo, hi = (mid, hi) if r >= 1 else (lo, mid)
    return lo, c


def main():
    G = {}
    print("plain level-k values (power iteration):")
    for K in range(2, 10):
        G[K], _ = gamma_full(K)
        print(f"  k={K} gamma_k={G[K]:.6f}")
    print("\n(A) 2-adic feature  W = w(a mod 3^k, a mod 2^j)   [LP, HiGHS]")
    for k in (2, 3, 4, 5):
        gp = gamma_plain(k)
        for j in (1, 2, 3):
            g = gamma_2adic(k, j)
            print(f"  k={k} j={j} vars={3 ** (k - 1) * 2 ** j:5d}: gamma={g:.6f}  plain LP gamma_k={gp:.6f}  diff={g - gp:+.1e}")
    print("\n(B) size feature  W = w(a mod 3^k, floor(log2 a) mod J)   [LP, HiGHS]")
    for k in (2, 3, 4):
        gp = gamma_plain(k)
        for J in (2, 3, 5):
            g = gamma_size(k, J)
            print(f"  k={k} J={J} vars={3 ** (k - 1) * J:5d}: gamma={g:.6f}  plain LP gamma_k={gp:.6f}  diff={g - gp:+.1e}")
    print("\n(C) rank-1 compression  c_(k+j) = u(low k digits) (x) v(top j digits)")
    print("    params = 3^(k-1)+3^j ; 'gain' = (gamma_sep-gamma_k)/(gamma_(k+j)-gamma_k);")
    print("    'k_eq' = level whose plain vector has as many parameters (log_3 params + 1)")
    for k, j in ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (6, 1), (6, 2), (7, 1)):
        g = gamma_sep(k, j, G[k], G[k + j])
        par = 3 ** (k - 1) + 3 ** j
        keq = math.log(par, 3) + 1
        # plain gamma at fractional level k_eq by linear interpolation of the table
        k0 = min(int(math.floor(keq)), 8)
        gint = G[k0] + (keq - k0) * (G[k0 + 1] - G[k0])
        print(f"  k={k} j={j}: params={par:5d} (full level {k + j}: {3 ** (k + j - 1):5d})  gamma_sep={g:.6f}  "
              f"gamma_k={G[k]:.6f} gamma_(k+j)={G[k + j]:.6f} gain={(g - G[k]) / (G[k + j] - G[k]):.3f}  "
              f"plain at equal size (k_eq={keq:.2f}, interpolated) {gint:.6f}  => {'WIN' if g > gint + 1e-6 else 'loss'}")
    print("\nsingular values of the level-K Perron vector reshaped (top j digits) x (low digits), log-domain:")
    for K, j in ((8, 2), (8, 3), (9, 3)):
        _, c = gamma_full(K)
        Mx = np.log(c).reshape(3 ** j, 3 ** (K - 1 - j))
        s = np.linalg.svd(Mx - Mx.mean(), compute_uv=False)
        print(f"  K={K} j={j}: sigma/sigma_1 = {np.round(s[:6] / s[0], 4).tolist()}")


if __name__ == "__main__":
    main()
