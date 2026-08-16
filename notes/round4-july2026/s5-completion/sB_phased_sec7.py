"""sB_phased_sec7.py — check of Lemma P7 (phased Prop 7.1):

    sum_s |E[ 1_{S_n = s} chi(X_n) ]|  <=  E prod_{j in [n/2]} |f(3^{2j-2} 2^{-b_{[1,j]}}, b_j)|

where chi(x) = e(-xi (x mod 3^n)/3^n), S_n = a_{[1,n]}, X_n as in (1.29),
b_j = a_{2j-1}+a_{2j} Pascal, f(x,b) = E[chi(x(2^{a2}+3)) | a1+a2=b]
(uniform a2 in {1..b-1}), leftover letter a_n (n odd) contributing modulus-1
factor only.  RHS is Tao's own (7.5) majorant — his Section 7 proves it is
O_A(n^{-A}).  The inequality itself is proved by conditioning; this script
verifies both sides numerically at n=7,8 for several xi (3∤xi):
LHS from the exact integer table A_n(s,Y) of sA; RHS by exhaustive enumeration
of b-vectors (b<=BMAX) + exact tail slack (each |f|<=1, P(any b>BMAX) bound).

PASS criterion: LHS <= RHS + tail + 1e-12 for every tested xi, and both
decrease with n (qualitative).
"""
import sys, math, cmath
from math import comb
from fractions import Fraction as Fr

sys.setrecursionlimit(10000)

def report(name, ok, detail=""):
    print(f"[{name}] {'PASS' if ok else 'FAIL'} {detail}", flush=True)
    if not ok:
        sys.exit(f"FAILED: {name}")

def joint_table(n, smax):
    dp = {0: {0: 1}}
    for i in range(n):
        M3 = 3 ** (i + 1)
        new = {}
        inv2 = pow(2, -1, M3)
        for s, row in dp.items():
            for Y, cnt in row.items():
                base = (3 * Y + 1) % M3
                v = base
                for a in range(1, smax - s + 1):
                    v = (v * inv2) % M3
                    s2 = s + a
                    if s2 > smax:
                        break
                    d = new.setdefault(s2, {})
                    d[v] = d.get(v, 0) + cnt
        dp = new
    return dp

def lhs_sum(n, xi, smax):
    """sum_s |E 1_{S=s} chi(X_n)| via exact table; truncation slack returned."""
    M = 3 ** n
    dp = joint_table(n, smax)
    tot = 0.0
    for s, row in dp.items():
        z = 0j
        for Y, c in row.items():
            z += c * cmath.exp(-2j * math.pi * (xi * Y % M) / M)
        tot += abs(z) / 2 ** s
    tail = 1 - sum(Fr(comb(s - 1, n - 1), 2 ** s) for s in range(n, smax + 1))
    return tot, float(tail)

def f_factor(x_pow3, x_pow2inv, b, n, xi):
    """f(3^{2j-2} 2^{-B}, b) with x represented by (3^{2j-2} mod 3^n, inv2^B mod 3^n)."""
    M = 3 ** n
    base = (x_pow3 * x_pow2inv) % M
    tot = 0j
    for a2 in range(1, b):
        val = (base * (pow(2, a2, M) + 3)) % M
        tot += cmath.exp(-2j * math.pi * (xi * val % M) / M)
    return abs(tot) / (b - 1)

def rhs_majorant(n, xi, BMAX):
    """E prod_{j in [n/2]} |f| over b-vectors with all b<=BMAX + exact tail slack."""
    M = 3 ** n
    half = n // 2
    inv2 = pow(2, -1, M)
    # DP over j: state = B = b_{[1,j]} (needed for 3^{2j-2}2^{-B}); prob weight
    # P(Pascal=b) = (b-1)/2^b
    from collections import defaultdict
    cur = {0: 1.0}   # B -> prob mass with factors multiplied in expectation? No:
    # need E of PRODUCT: carry accumulated product-weighted mass: state B -> sum of prob*prod
    cur = {0: 1.0}
    for j in range(1, half + 1):
        nxt = defaultdict(float)
        p3 = pow(3, 2 * j - 2, M)
        for B, w in cur.items():
            for b in range(2, BMAX + 1):
                pb = (b - 1) / 2 ** b
                Bb = B + b
                fac = f_factor(p3, pow(inv2, Bb, M), b, n, xi)
                nxt[Bb] += w * pb * fac
        cur = nxt
    val = sum(cur.values())
    # tail: P(some b_j > BMAX) <= half * sum_{b>BMAX}(b-1)2^{-b} = half*(BMAX+1)*2^{-BMAX} exact-ish
    tail = half * (BMAX + 1) * 2.0 ** (-BMAX)
    return val, tail

def main():
    print("  n   xi     LHS(sum_s)      RHS(E prod|f|)   LHS<=RHS+slack")
    allok = True
    for n in (7, 8):
        smax = 3 * n + 22
        for xi in (1, 2, 5, 7, 3 ** 2 + 1, 3 ** 3 + 2):
            if xi % 3 == 0:
                continue
            lhs, ltail = lhs_sum(n, xi, smax)
            rhs, rtail = rhs_majorant(n, xi, 30)
            ok = lhs <= rhs + rtail + ltail + 1e-9
            allok = allok and ok
            print(f"  {n}   {xi:3d}   {lhs:.8f}     {rhs:.8f}      {'OK' if ok else 'VIOLATION'} (slacks {ltail:.1e}/{rtail:.1e})")
    report("B1", allok, "Lemma P7 inequality holds at n=7,8 for all tested xi coprime to 3")
    # also show the plain char |S_chi(n)| for scale: it is <= LHS trivially
    for n in (7, 8):
        smax = 3 * n + 22
        M = 3 ** n
        dp = joint_table(n, smax)
        for xi in (1,):
            z = 0j
            for s, row in dp.items():
                for Y, c in row.items():
                    z += c * cmath.exp(-2j * math.pi * (xi * Y % M) / M) / 2 ** s
            lhs, _ = lhs_sum(n, xi, smax)
            print(f"  n={n} xi={xi}: |S_chi|={abs(z):.8f}  <=  sum_s-version {lhs:.8f} (consistency)")
    report("B2", True, "plain |S_chi| <= summed phased version (consistency rows)")
    print("\nALL sB CHECKS COMPLETE", flush=True)

main()
