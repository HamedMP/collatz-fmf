"""Referee's independent numerical checks of Lemma P7, Lemma J*, Lemma M (PROOFS.md) at toy scale.

Joint law of (S_n, X_n), X_n = F_n(a_1..a_n) mod 3^n, S_n = a_1+..+a_n, a_i iid Geom(2), by the
forward recursion  F_j = (3 F_{j-1} + 1) 2^{-a_j}  carried in Z/3^n (float64 probabilities; S truncated
at SMAX, lost mass printed).  No code shared with sA/sB/sE.
Run: python ref_Jstar.py [nmax]
"""
import sys, cmath, math
import numpy as np

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9


def joint_law(n, smax):
    q = 3 ** n
    inv2 = (q + 1) // 2
    Y = np.arange(q)
    idx3 = (3 * Y + 1) % q            # X -> 3X+1
    idxh = (Y * inv2) % q             # X -> X/2
    P = np.zeros((smax + 1, q))
    P[0, 0] = 1.0
    for _ in range(n):
        T = np.zeros_like(P)
        for s in range(smax + 1):
            if P[s].any():
                T[s] = np.bincount(idx3, weights=P[s], minlength=q)
        G = np.zeros_like(P)
        for s in range(1, smax + 1):
            v = 0.5 * (T[s - 1] + G[s - 1])       # G[s] = sum_{a>=1} 2^-a H^a T[s-a]
            G[s] = np.bincount(idxh, weights=v, minlength=q)
        P = G
    return P


def coset_avg(P, n, m):
    q, r = 3 ** n, 3 ** m
    A = P.reshape(P.shape[0], q // r, r).sum(axis=1) / (q // r)   # index Y = k*r + (Y mod r)
    return np.tile(A, (1, q // r))


def tao_table():
    P = joint_law(2, 80).sum(axis=0) * 63
    return np.round(P, 6)


def majorant(n, xi, bmax=60):
    """E prod_{j<=n/2} |f(3^{2j-2} 2^{-b_[1,j]}, b_j)|, f(x,b) = mean_{a2=1..b-1} chi(x(2^{a2}+3))."""
    q = 3 ** n
    inv2 = (q + 1) // 2
    J = n // 2
    lmax = bmax * J
    W = {0: 1.0}
    for j in range(1, J + 1):
        W2 = {}
        for l0, w in W.items():
            for b in range(2, bmax + 1):
                l = l0 + b
                x = (pow(3, 2 * j - 2, q) * pow(inv2, l, q)) % q
                acc = 0j
                for a2 in range(1, b):
                    acc += cmath.exp(-2j * math.pi * ((xi * x * (pow(2, a2, q) + 3)) % q) / q)
                f = abs(acc) / (b - 1)
                W2[l] = W2.get(l, 0.0) + w * (b - 1) * 2.0 ** (-b) * f
        W = W2
    return sum(W.values())


if __name__ == "__main__":
    print("Tao's Z/9 table x63 (expect 0 8 16 0 11 4 0 2 22):", tao_table())
    print("\n[M] max-mass of Syrac(Z/3^m) vs (2/3)^m and 2^-m")
    for m in range(1, NMAX + 1):
        P = joint_law(m, 2 * m + 60)
        mx = P.sum(axis=0).max()
        print(f"  m={m}  lost mass={1 - P.sum():.1e}  max={mx:.8f}  max/(2/3)^m={mx / (2 / 3) ** m:.4f}  max*2^m={mx * 2 ** m:.4f}")

    print("\n[J*] Osc^J_{m,n} (joint in (S,X)) vs Tao's plain Osc_{m,n} (X only)")
    print("   n  m   Osc_plain    Osc_joint    ratio")
    for n in range(3, NMAX + 1):
        P = joint_law(n, 2 * n + 60)
        Pm = P.sum(axis=0, keepdims=True)
        for m in range(1, n):
            oj = np.abs(P - coset_avg(P, n, m)).sum()
            op = np.abs(Pm - coset_avg(Pm, n, m)).sum()
            print(f"  {n:2d} {m:2d}   {op:.6f}    {oj:.6f}    {oj / op if op > 0 else float('nan'):.3f}")

    print("\n[P7] sum_s |E 1_{S=s} chi(X_n)|  vs  |E chi(X_n)|  vs  E prod|f|  (need LHS <= RHS)")
    ok = True
    for n in range(4, min(NMAX, 9) + 1):
        P = joint_law(n, 2 * n + 60)
        q = 3 ** n
        Y = np.arange(q)
        for xi in (1, 2, 4, 5, 7, 3 ** (n - 1) + 1, q - 1):
            if xi % 3 == 0:
                continue
            ph = np.exp(-2j * np.pi * ((xi * Y) % q) / q)
            per_s = P @ ph
            lhs = np.abs(per_s).sum()
            plain = abs(per_s.sum())
            rhs = majorant(n, xi)
            good = lhs <= rhs + 1e-9
            ok &= good
            print(f"  n={n} xi={xi:<6d} sum_s={lhs:.6f}  plain={plain:.6f}  majorant={rhs:.6f}  {'ok' if good else 'VIOLATION'}")
    print("P7 inequality:", "holds in all rows" if ok else "VIOLATED")
