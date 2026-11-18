"""Numerical sanity checks for the Mazur positive-density audit (own code; exploratory floats
except where 'EXACT' is printed).  Run: taskset -c 0-1 python scripts/numeric_checks.py"""
import math, sys
from fractions import Fraction as Fr
import numpy as np
from numba import njit

# ---------- 1. density of {n < X : tau(n) <= 10.46 ln n}, ordinary Collatz steps ----------
@njit(cache=True)
def tau_table(N):
    t = np.zeros(N, dtype=np.int32)          # t[1] = 0
    for n in range(2, N):
        m = n; s = 0
        while m >= n:                         # walk until below n (table already filled)
            if m & 1: m = 3*m + 1
            else: m >>= 1
            s += 1
        t[n] = s + t[m]
    return t
@njit(cache=True)
def count_fast(t, C, X):
    c = 0
    for n in range(1, X):
        if t[n] <= C*math.log(n): c += 1
    return c
N = 3*10**7
t = tau_table(N)
print("1. fraction of 1<=n<X with tau(n) <= C ln n (typical clock 3/ln(4/3) = %.4f)" % (3/math.log(4/3)))
for X in (10**3, 10**4, 10**5, 10**6, 10**7, 3*10**7):
    print("   X=%9d  C=10.46: %.4f   C=10.48: %.4f   C=8: %.4f" % (X, count_fast(t, 523/50, X)/X, count_fast(t, 262/25, X)/X, count_fast(t, 8.0, X)/X))
# powers of two alone would give log2(X)/X -> 0; the observed fraction is ~constant, i.e. linear count.

# ---------- 2. Lemma 4.1 (seeds S(M)=1 hit every class mod 3^q) and its 5n+1 / 3n-1 analogues. EXACT ----------
print("2. seed coverage, EXACT integer arithmetic")
for q in range(1, 8):
    s3 = {((4**j - 1)//3) % 3**q for j in range(3**q)}
    sm = {((2*4**j + 1)//3) % 3**q for j in range(3**q)}          # 3n-1: S(M)=1 iff 3M-1=2^a, a odd
    print("   3n+1 q=%d: %d/%d classes   3n-1: %d/%d" % (q, len(s3), 3**q, len(sm), 3**q), end="")
    if q <= 5:
        s5 = {((16**j - 1)//5) % 5**q for j in range(5**q)}       # 5n+1: 5M+1 = 16^j
        print("   5n+1 (mod 5^q): %d/%d" % (len(s5), 5**q))
    else: print()

# ---------- 3. finite Syracuse law mu_q on Z/3^q: EXACT rationals; normalisation, unit support, oscillation ----------
def mu(q):
    law = {0: Fr(1)}
    for lev in range(1, q+1):
        mod = 3**lev; per = 2*3**(lev-1)                      # order of 2 mod 3^lev
        pw = [Fr(2)**(-r) / (1 - Fr(2)**(-per)) for r in range(1, per+1)]   # P(a = r mod per), a>=1
        inv = [pow(2, -r, mod) for r in range(1, per+1)]
        new = {}
        for y, p in law.items():
            for r in range(per):
                z = inv[r]*(3*y + 1) % mod
                new[z] = new.get(z, 0) + p*pw[r]
        law = new
    return law
print("3. EXACT finite Syracuse laws; osc(m,q) = sum_y |mu_q(y) - 3^(m-q) mu_m(y mod 3^m)|")
laws = {q: mu(q) for q in range(1, 6)}
for q in range(1, 6):
    L = laws[q]
    assert sum(L.values()) == 1 and all(y % 3 != 0 for y in L)       # probability law, supported on units
    row = []
    for m in range(1, q+1):
        osc = sum(abs(L.get(y, Fr(0)) - Fr(3**m, 3**q)*laws[m].get(y % 3**m, Fr(0))) for y in range(3**q))
        row.append("m=%d: %.5f" % (m, float(osc)))
    print("   q=%d  max atom*(3/2)^q = %.4f  " % (q, float(max(L.values()))*1.5**q) + "  ".join(row))

# ---------- 4. Lemma 2.1 (mean of weighted transfer) EXACT on random words ----------
import random
random.seed(1)
def F(w, z, t):
    # forward affine map Phi_w = f_{a1} o ... o f_{ad}, f_a(z) = (3z+1)/2^a, on Z/3^(t+d)
    mod = 3**(t+len(w)); y = z
    for a in reversed(w):
        y = (3*y + 1) * pow(2, -a, mod) % mod
    return y
ok = True
for _ in range(200):
    d = random.randint(1, 4); tt = random.randint(1, 3); w = [random.randint(1, 5) for _ in range(d)]
    g = [Fr(random.randint(-5, 5)) for _ in range(3**tt)]
    imgs = [F(w, z, tt) for z in range(3**tt)]
    ok &= len(set(imgs)) == 3**tt                                    # injective
    lhs = Fr(3**d, 2**sum(w)) * sum(abs(x) for x in g) / 3**(tt+d)    # <|T_w g|>_{t+d}
    ok &= lhs == Fr(1, 2**sum(w)) * sum(abs(x) for x in g) / 3**tt
print("4. Lemma 2.1 injectivity + mean identity on 200 random words: EXACT", "OK" if ok else "FAIL")

# ---------- 5. time-constant arithmetic (7.8), (7.9) with mpmath ----------
import mpmath as mp
mp.mp.dps = 50
Lg, g, h = mp.log(2), mp.log(mp.mpf(4)/3), mp.log(mp.mpf(12289)/4096)
kap = mp.mpf(34881)/10000; gam = 2*Lg - h
print("5. (7.9): (523/50) L - (kappa (L+h) + 1) =", mp.nstr((mp.mpf(523)/50)*Lg - (kap*(Lg+h)+1), 8), " (must be >= 0)")
print("   (7.8): (kappa*gamma-1)*2569/9000 - (g/1e5 + 219/250000) =", mp.nstr((kap*gam-1)*mp.mpf(2569)/9000 - (g/100000 + mp.mpf(219)/250000), 8), " (must be >= 0)")
print("   typical ordinary clock 3/ln(4/3) =", mp.nstr(3/g, 8), "; kappa*(L+h)/L + 1/L =", mp.nstr((kap*(Lg+h)+1)/Lg, 8))

# ---------- 6. litmus: drift of the inverse tree, and basin densities for 3n-1 and 5n+1 ----------
print("6. inverse-block growth per Syracuse step under the geometric(1/2) valuation law: E[a] ln2 - ln q")
for qq in (3, 5, 7): print("   q=%d: %+.4f  (%s)" % (qq, 2*math.log(2)-math.log(qq), "typical inverse histories GROW: barrier A~2d is central" if qq == 3 else "typical inverse histories SHRINK: growth needs A/d > log2(q), exponentially rare"))

@njit(cache=True)
def basin(N, q, d, LIM):
    # label[n] = smallest element of the cycle reached by n under n->n/2, qn+d ; 0 if orbit exceeds LIM (treated as escape)
    lab = np.zeros(N, dtype=np.int64)
    for n in range(1, N):
        m = n; steps = 0; res = -1
        while True:
            if m < n: res = lab[m]; break
            if m > LIM: res = 0; break
            if m & 1: m = q*m + d
            else: m >>= 1
            steps += 1
            if m == n:                      # n lies on a cycle and is its minimum
                res = n; break
            if steps > 100000: res = 0; break
        lab[n] = res
    return lab
for (q, d, name) in ((3, -1, "3n-1"), (5, 1, "5n+1")):
    Nb = 2*10**6
    lab = basin(Nb, q, d, 2**61 // q)
    cyc = sorted(set(lab.tolist()) - {0})
    print("   %s cycles (minima) found below %d: %s" % (name, Nb, cyc[:8]))
    for X in (10**3, 10**4, 10**5, 10**6, 2*10**6):
        seg = lab[1:X]
        print("     X=%8d " % X + "  ".join("basin(%d)=%.4f" % (c, float((seg == c).sum())/X) for c in cyc[:4]) + "  escape/unknown=%.4f" % (float((seg == 0).sum())/X))
    if q == 5:
        xs = [10**k for k in range(3, 7)]; cs = [int((lab[1:X] == 1).sum()) for X in xs]
        print("     5n+1: #{n<X reaching 1} =", cs, " local exponents:", ["%.3f" % (math.log(cs[i+1]/cs[i])/math.log(10)) for i in range(3)])
