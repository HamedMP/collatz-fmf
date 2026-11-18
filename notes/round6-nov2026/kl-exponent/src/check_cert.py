#!/usr/bin/env python3
"""Independent exact-integer checker for Krasikov-Lagarias L_k^NT certificates.

Shares no code with the solver (klrho.c / run_k.py).  All arithmetic that the verdict
depends on is integer arithmetic (Python ints; numpy uint64 with an a-priori overflow
bound for large k).  Rows are generated from RESIDUES m mod 3^k by the definitions
(4m, (4m-2)/3, (2m-1)/3 and the three lifts r + j*3^(k-1)); no closed-form index
shortcut is used in the Python-int path, and the numpy path is cross-checked against
the Python-int path on a sample of rows.

Certificate directory:
  cert.json   {"k", "gamma_num", "gamma_log2den", "mode": "lower"|"upper",
               "weights": file, "dtype": "<u4"|"<u8"}
  weights     N = 3^(k-1) unsigned ints; entry i is the weight of residue m = 3i+2 mod 3^k.

gamma = gamma_num / 2^gamma_log2den, lambda = 2^gamma.  Exact row coefficients of
L_k^NT(lambda):  lambda^-2 = 4^-gamma, lambda^(alpha-2) = (3/4)^gamma,
lambda^(alpha-1) = (3/2)^gamma  (alpha = log2 3).

Coefficient bounds (integers / 2^PREC, PREC = 160) by directed rounding:
  s_0 = 3 (resp. 2);  s_{j+1} = sqrt(s_j):  lower = isqrt(lower << PREC),
  upper = isqrt(upper << PREC) + 1;  3^gamma = prod over binary digits of gamma of
  3^(2^-j), products rounded down (lower) / up (upper).  Every operand is positive,
  so floor of a product of lower bounds is a lower bound, and similarly for upper.

mode "lower": checks  S*w[m] <= a*w[4m] + L(m)*min_j w[lift_j(aux(m))]  with a, L
   LOWER bounds of the true coefficients times S  => w is a feasible point of
   L_k^NT(2^gamma) (after scaling so min w = 1).
mode "upper": checks  a*w[4m] + L(m)*min_j(...) < S*w[m]  with UPPER bounds
   => F(w) < w, hence no positive feasible vector exists at this gamma
   (if d <= F(d), d > 0, s = max d/w attained at m*: d[m*] <= F(d)[m*] <= s F(w)[m*]
    < s w[m*] = d[m*], contradiction; F monotone and 1-homogeneous).

usage: check_cert.py CERTDIR [--pyint]
"""
import json
import os
import random
import sys
from math import isqrt

import numpy as np

PREC = 160
ONE = 1 << PREC


def root_chains(base, t):
    """lower/upper fixed-point bounds for base^(2^-j), j = 0..t."""
    lo = [base * ONE]
    hi = [base * ONE]
    for _ in range(t):
        lo.append(isqrt(lo[-1] << PREC))
        hi.append(isqrt(hi[-1] << PREC) + 1)
    return lo, hi


def pow_bounds(base, num, t):
    """(lower, upper) fixed-point bounds of base^(num / 2^t), 0 <= num."""
    lo_chain, hi_chain = root_chains(base, t)
    ip, frac = divmod(num, 1 << t)
    lo = hi = (base ** ip) * ONE
    for j in range(1, t + 1):            # digit of weight 2^-j
        if (frac >> (t - j)) & 1:
            lo = (lo * lo_chain[j]) >> PREC
            hi = ((hi * hi_chain[j]) >> PREC) + 1
    return lo, hi


def coefficients(num, t, S, mode):
    lo3, hi3 = pow_bounds(3, num, t)
    lo2, hi2 = pow_bounds(2, num, t)
    assert 0 < lo3 <= hi3 and 0 < lo2 <= hi2
    if mode == "lower":
        a = (S * ONE * ONE) // (hi2 * hi2)                # <= S * 4^-gamma
        b = (S * lo3 * ONE) // (hi2 * hi2)                # <= S * (3/4)^gamma
        c = (S * lo3) // hi2                              # <= S * (3/2)^gamma
    else:
        a = -((-S * ONE * ONE) // (lo2 * lo2))            # >= S * 4^-gamma (ceil)
        b = -((-S * hi3 * ONE) // (lo2 * lo2))
        c = -((-S * hi3) // lo2)
    return a, b, c


def row_terms(m, k):
    """for residue m = 2 mod 3 (0 <= m < 3^k): (4m mod 3^k, kind, [three lifts])."""
    M = 3 ** k
    M1 = 3 ** (k - 1)
    assert m % 3 == 2
    r9 = m % 9
    if r9 == 2:
        assert (4 * m - 2) % 3 == 0
        r = ((4 * m - 2) // 3) % M1
        kind = 1
    elif r9 == 8:
        assert (2 * m - 1) % 3 == 0
        r = ((2 * m - 1) // 3) % M1
        kind = 2
    else:
        return (4 * m) % M, 0, []
    assert r % 3 == 2
    return (4 * m) % M, kind, [r, r + M1, r + 2 * M1]


def check_pyint(w, k, a, b, c, S, mode, rows=None):
    M = 3 ** k
    worst = None
    it = rows if rows is not None else range(2, M, 3)
    for m in it:
        m4, kind, lifts = row_terms(m, k)
        rhs = a * w[(m4 - 2) // 3]
        if kind:
            rhs += (b if kind == 1 else c) * min(w[(x - 2) // 3] for x in lifts)
        lhs = S * w[(m - 2) // 3]
        ok = (lhs <= rhs) if mode == "lower" else (rhs < lhs)
        if not ok:
            return False, m, None
        sl = (rhs - lhs) / lhs if mode == "lower" else (lhs - rhs) / lhs
        worst = sl if worst is None else min(worst, sl)
    return True, None, worst


def check_numpy(w, k, a, b, c, S, mode):
    N = 3 ** (k - 1)
    N3 = N // 3
    wmax = int(w.max())
    assert wmax * S < 2 ** 64 and wmax * a + wmax * max(b, c) < 2 ** 64, "overflow"
    a64, b64, c64, z64, S64 = (np.uint64(v) for v in (a, b, c, 0, S))
    worst = None
    CH = 1 << 22
    for s in range(0, N, CH):
        e = min(N, s + CH)
        i = np.arange(s, e, dtype=np.int64)
        u, t = i // 3, i % 3
        r = np.where(t == 0, (4 * u) % N3, (2 * u + 1) % N3)
        wb = np.minimum(np.minimum(w[r], w[r + N3]), w[r + 2 * N3]).astype(np.uint64)
        L = np.where(t == 0, b64, np.where(t == 2, c64, z64))
        rhs = a64 * w[(4 * i + 2) % N].astype(np.uint64) + L * wb
        lhs = w[s:e].astype(np.uint64) * S64
        bad = (lhs > rhs) if mode == "lower" else (rhs >= lhs)
        if bad.any():
            return False, 3 * (s + int(np.argmax(bad))) + 2, None
        d = (rhs.astype(np.float64) - lhs.astype(np.float64)) / lhs.astype(np.float64)
        mm = float(d.min() if mode == "lower" else (-d).min())
        worst = mm if worst is None else min(worst, mm)
    return True, None, worst


def main():
    certdir = sys.argv[1]
    with open(os.path.join(certdir, "cert.json")) as f:
        cert = json.load(f)
    k, num, t, mode = cert["k"], cert["gamma_num"], cert["gamma_log2den"], cert["mode"]
    assert isinstance(k, int) and k >= 2 and isinstance(num, int) and isinstance(t, int)
    assert 0 < num < (1 << t) and 1 <= t <= 64 and mode in ("lower", "upper")
    assert cert["dtype"] in ("<u4", "<u8")
    N = 3 ** (k - 1)
    w = np.fromfile(os.path.join(certdir, cert["weights"]), dtype=cert["dtype"])
    assert w.shape == (N,), w.shape
    assert int(w.min()) >= 1
    force_py = "--pyint" in sys.argv
    if cert["dtype"] == "<u8" or force_py:
        S = 1 << 64
        a, b, c = coefficients(num, t, S, mode)
        wl = [int(x) for x in w]
        ok, bad, worst = check_pyint(wl, k, a, b, c, S, mode)
        path = "python-int, all rows from residues"
    else:
        S = 1 << 30
        a, b, c = coefficients(num, t, S, mode)
        ok, bad, worst = check_numpy(w, k, a, b, c, S, mode)
        path = "numpy uint64 (overflow excluded)"
        if ok:   # cross-check the vectorised index formulas against the residue definitions
            rnd = random.Random(12345)
            M = 3 ** k
            rows = [3 * rnd.randrange(N) + 2 for _ in range(20000)] + [2, 5, 8, M - 1, M - 4, M - 7]

            class W:
                def __getitem__(self, i):
                    return int(w[i])
            ok2, bad2, _ = check_pyint(W(), k, a, b, c, S, mode, rows)
            assert ok2, f"numpy path passed but python-int sample failed at m={bad2}"
            path += " + 20006-row python-int sample"
    g = num / (1 << t)
    if not ok:
        print(f"FAILED k={k} mode={mode} gamma={num}/2^{t} at residue m={bad}")
        sys.exit(1)
    wmin, wmax = int(w.min()), int(w.max())
    what = ("feasible: all rows hold" if mode == "lower" else "infeasible: F(w) < w in all rows")
    print(f"VERIFIED k={k} N={N} mode={mode} gamma={num}/2^{t}={g:.10f} lambda={2 ** g:.8f} "
          f"{what}; spread={wmax / wmin:.6f} min_rel_slack~{worst:.3e} [{path}]")


if __name__ == "__main__":
    main()
