#!/usr/bin/env python3
"""Brute-force test of the direct (tree-induction) form of the Krasikov-Lagarias bound.

Theorem T (REPORT.md section b).  Let k >= 2, lam > 1, gamma = log2(lam) and let
c: {m mod 3^k, m = 2 mod 3} -> (0, inf) satisfy the rows of L_k^NT(lam):
    m = 2 (mod 9):  c[m] <= lam^-2 c[4m] + lam^(alpha-2) cbar[(4m-2)/3]
    m = 5 (mod 9):  c[m] <= lam^-2 c[4m]
    m = 8 (mod 9):  c[m] <= lam^-2 c[4m] + lam^(alpha-1) cbar[(2m-1)/3]
(cbar[r] = min over the three lifts of r mod 3^(k-1)).  Then for every integer
a >= 1, a = 2 (mod 3), a not on a cycle of T, and every real x >= a,
    pistar_a(x) >= c[a mod 3^k] / (4^gamma * max c) * (x/a)^gamma,
where pistar_a(x) = #{n <= x : T^j(n) = a for some j, all T^i(n) <= x, i <= j}.

This script (pure Python, no project imports):
 1. for each k in KS finds a feasible c by power iteration at lam = lam_k - 1e-6
    (lam_k located by bisection) and re-checks the rows in floating point with
    margin;
 2. for every a = 2 (mod 3), 5 <= a <= AMAX, enumerates the predecessor tree of a
    with heights h(v) = max of the values on the path v -> a, for h <= XFACTOR*a;
    pistar_a(x) = #{v : h(v) <= x}; checks the inequality at EVERY real x in
    [a, XFACTOR*a) (it suffices to check just below each jump of the step function);
 3. prints the minimum of pistar_a(x) / bound over everything (must be >= 1).

usage: test_induction_bound.py [AMAX=400] [XFACTOR=4096]
"""
import math
import sys

ALPHA = math.log2(3.0)


def F(c, k, lam):
    N = 3 ** (k - 1)
    N3 = N // 3
    A, B, C = lam ** -2, lam ** (ALPHA - 2), lam ** (ALPHA - 1)
    cb = [min(c[t], c[t + N3], c[t + 2 * N3]) for t in range(N3)]
    out = [0.0] * N
    for i in range(N):
        u, t = divmod(i, 3)
        v = A * c[(4 * i + 2) % N]
        if t == 0:
            v += B * cb[(4 * u) % N3]
        elif t == 2:
            v += C * cb[(2 * u + 1) % N3]
        out[i] = v
    return out


def ratios(c, k, lam):
    f = F(c, k, lam)
    r = [fi / ci for fi, ci in zip(f, c)]
    return min(r), max(r), f


def solve(k, lam, c=None, maxit=20000):
    """power iteration; returns (+1, c) if c <= F(c) reached, (-1, c) if F(c) < c."""
    N = 3 ** (k - 1)
    if c is None:
        c = [1.0] * N
    for _ in range(maxit):
        lo, hi, f = ratios(c, k, lam)
        if lo >= 1.0:
            return 1, c
        if hi < 1.0:
            return -1, c
        mn = min(f)
        c = [x / mn for x in f]
    return 0, c


def lam_k(k, tol=1e-9):
    a, b = 1.2, 2.0
    c = None
    while b - a > tol:
        mid = 0.5 * (a + b)
        r, c = solve(k, mid, c)
        if r > 0:
            a = mid
        elif r < 0:
            b = mid
        else:
            break
    return a, b


def tree_heights(a, xmax):
    """sorted list of h(v) for all v in the predecessor tree of a with h(v) <= xmax."""
    hs = []
    stack = [(a, a)]
    while stack:
        v, h = stack.pop()
        hs.append(h)
        w = 2 * v
        if w <= xmax:
            stack.append((w, max(h, w)))
        if v % 3 == 2:
            b = (2 * v - 1) // 3
            # b < v, so h unchanged; b on a cycle only if a is (excluded by caller)
            stack.append((b, h))
    hs.sort()
    return hs


def main():
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    xfac = int(sys.argv[2]) if len(sys.argv) > 2 else 4096
    published = {2: 1.3534010, 3: 1.5275960, 4: 1.6122870, 5: 1.6627590, 6: 1.6944520}
    worst_all = float("inf")
    for k in (2, 3, 4, 5, 6):
        lo, hi = lam_k(k)
        lam = lo - 1e-6
        r, c = solve(k, lam)
        assert r == 1
        # a few extra monotone steps keep feasibility (c <= F(c) => F(c) <= F(F(c)))
        mlo, mhi, _ = ratios(c, k, lam)
        assert mlo >= 1.0, mlo
        mn = min(c)
        c = [x / mn for x in c]
        cmax = max(c)
        gamma = math.log2(lam)
        D = 1.0 / (4.0 ** gamma * cmax)
        M = 3 ** k
        worst = (float("inf"), None, None)
        for a in range(5, amax + 1, 3):          # a = 2 mod 3, a >= 5 (2 is on the cycle {1,2})
            hs = tree_heights(a, xfac * a)
            ca = c[((a % M) - 2) // 3]
            # count is i on [hs[i-1], hs[i]); bound is increasing: check at right end
            n = len(hs)
            for i in range(1, n + 1):
                xr = hs[i] if i < n else xfac * a
                bound = D * ca * (xr / a) ** gamma
                q = i / bound
                if q < worst[0]:
                    worst = (q, a, xr)
        print(f"k={k}: lam_k in [{lo:.7f},{hi:.7f}] (published {published[k]:.7f}), "
              f"test lam={lam:.7f} gamma={gamma:.6f} spread={cmax:.6f}; "
              f"min pistar/bound = {worst[0]:.4f} at a={worst[1]}, x->{worst[2]}")
        assert worst[0] >= 1.0, "THEOREM T VIOLATED"
        worst_all = min(worst_all, worst[0])
    print(f"OK: theorem T holds on all tested (a, x); global min ratio {worst_all:.4f}")


if __name__ == "__main__":
    main()
