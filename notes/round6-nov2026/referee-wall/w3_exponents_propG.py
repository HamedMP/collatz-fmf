# Referee: exponents of Theorem A'/B'/C', constants, Remark 2/3 arithmetic, Proposition G recursion.
import math, sys, cmath
import numpy as np
import mpmath as mp

s = 0.2877607871
x = 2 ** (-s); assert abs(x ** 3 + x ** 4 - 1) < 1e-9
print("== exponents ==")
print("s/(2+4s) = %.5f ; s/4 = %.5f" % (s / (2 + 4 * s), s / 4))
print("(1-s)s/(2+4s) = %.5f ; (1-s)s/4 = %.5f" % ((1 - s) * s / (2 + 4 * s), (1 - s) * s / 4))
print("log exponent A': s/(1+2s) = %.4f" % (s / (1 + 2 * s)))
print("log exponent B1': term1 1+s/(1+2s) = %.4f ; term2 1.5-1/(2+4s) = %.4f" % (1 + s / (1 + 2 * s), 1.5 - 1 / (2 + 4 * s)))
print("log exponent C': (1-s)*1.1826 = %.4f ; (1-s)*1.19 = %.4f" % ((1 - s) * (1 + s / (1 + 2 * s)), (1 - s) * 1.19))
print("k coefficient 1/(1+2s) = %.4f" % (1 / (1 + 2 * s)))
print("Remark 3: (1-s)/8 = %.4f ; rho0 = 1/(s+1/2) = %.4f ; 1/(2s) = %.4f" % ((1 - s) / 8, 1 / (s + .5), 1 / (2 * s)))
rho0 = 1 / (s + .5)
print("Remark 2: current saving exponent s*rho0 = %.4f ; Korobov c/rho^2 must exceed it at some rho>rho0:" % (s * rho0))
print("   threshold if valid only for rho>=2: c > 4*s*rho0 = %.3f (report: 8s = %.3f)" % (4 * s * rho0, 8 * s))
print("   threshold if valid down to rho0   : c > s*rho0^3 = %.3f (report: 0.29)" % (s * rho0 ** 3))

# boundedness of A' with the stated k (work in log2 K =: L, K huge)
print("== Theorem A' bound * K^{s/(2+4s)} / (log2 K)^{s/(1+2s)} (e=0), should stay bounded ==")
for L in [40, 80, 160, 320, 640, 1e3, 1e4, 1e5, 1e6, 1e8]:
    k = math.floor((L - 2 * math.log2(L)) / (1 + 2 * s))
    t1 = math.log2(6) - s * (k - 3)
    t2 = math.log2(72 * k) + k / 2 - L / 2          # K-k-4 ~ K
    lb = 0.5 * (max(t1, t2) + math.log2(1 + 2 ** (-abs(t1 - t2))))
    norm = lb + L * s / (2 + 4 * s) - (s / (1 + 2 * s)) * math.log2(L)
    # B' closed form
    b1 = math.log2(2.45 * (1.5 + .78 * k)) - s * (k - 3) / 2
    b2 = math.log2(8.5 * (1 + .7 * k) * math.sqrt(k)) + k / 4 - L / 4
    bb = max(b1, b2) + math.log2(1 + 2 ** (-abs(b1 - b2)))
    normb = bb + L * s / (2 + 4 * s) - 1.19 * math.log2(L)
    print("log2K=%9.0f k=%8d  log2(A' bound)=%12.2f  normalised 2^%.3f | log2(B' bound)=%12.2f normalised(1.19) 2^%.3f"
          % (L, k, lb, norm, bb, normb))

# sums used in B'
for kap in [8, 16, 24]:
    H = 1 << (kap - 1)
    h = np.arange(1, H + 1)
    v = np.log2((h & -h)).astype(float)
    S1 = (2 ** (s * v / 2) / h).sum(); S2 = (1 / h).sum()
    assert S1 <= 1.46 + .78 * kap and S2 <= 1 + .7 * kap
    print("kappa=%d: sum 2^(s v2/2)/h = %.3f <= %.3f ; sum 1/h = %.3f <= %.3f" % (kap, S1, 1.46 + .78 * kap, S2, 1 + .7 * kap))

# Remark 3 identity: sum over odd a of |sum_i M(i) e(a 3^i/2^j)|^2 = 2^(j-1) sum M^2 when support < tau/2
for j in [8, 12]:
    mod = 1 << j; tau = mod // 4
    L = tau // 2 - 1
    rng = np.random.default_rng(1); M = rng.random(L)
    pw = np.array([pow(3, i, mod) for i in range(L)])
    tot = 0
    for a in range(1, mod, 2):
        tot += abs((M * np.exp(2j * np.pi * ((a * pw) % mod) / mod)).sum()) ** 2
    print("Remark 3 j=%d: sum_a |.|^2 / (2^(j-1) sum M^2) = %.6f" % (j, tot / (2 ** (j - 1) * (M ** 2).sum())))

# ---------- Proposition G ----------
print("== Proposition G ==")
Ebase = {0: [0], 1: [0, 1], 2: [0, 3], 3: [0, 7]}
def Eset(kmax):
    E = dict(Ebase)
    for k in range(4, kmax + 1):
        m = 1 << k
        E[k] = [((8 * z - 1) * pow(9, -1, m)) % m for z in E[k - 3]] + [(16 * z * pow(27, -1, m)) % m for z in E[k - 4]]
    return E
E = Eset(26)

def e_frac(num, k):
    """e(num / 2^k) at current mp precision, num integer (reduced mod 2^k)."""
    num %= (1 << k)
    return mp.expjpi(mp.mpf(2 * num) / (1 << k)) if k > 0 else mp.mpc(1)

def T_rec(k, xi, sign=1):
    """T_k(xi) by the recursion T_k(xi) = e(-xi*9^-1/2^k) T_{k-3}(xi/9) + T_{k-4}(xi/27); xi integer (taken mod 2^k).
    State = (A,B): k' = k-3A-4B, frequency xi*3^(-(2A+3B)) mod 2^k'."""
    memo = {}
    # iterative, in order of decreasing k'
    import functools
    sys.setrecursionlimit(100000)
    def G(kk, P):
        key = (kk, P)
        if key in memo: return memo[key]
        if kk < 4:
            m = 1 << kk
            f = (xi * pow(3, -P, m)) % m if kk > 0 else 0
            r = sum(e_frac(f * c, kk) for c in Ebase[kk])
        else:
            m = 1 << kk
            f9 = (xi * pow(3, -(P + 2), m)) % m          # xi * 3^-P * 9^-1 mod 2^kk
            r = e_frac(-f9, kk) * G(kk - 3, P + 2) + G(kk - 4, P + 3)
        memo[key] = r
        return r
    return G(k, 0)

# verify recursion against direct sums, k<=26
mp.mp.prec = 80
rng = np.random.default_rng(7)
maxerr = 0
for k in range(4, 27):
    m = 1 << k
    for xi in [1, 3, 5, 2, 12, 3 ** 9, 3 ** 15, -7] + [int(v) for v in rng.integers(1, 1 << 40, 6)]:
        d = sum(cmath.exp(2j * math.pi * ((xi * c) % m) / m) for c in E[k])
        r = complex(T_rec(k, xi))
        maxerr = max(maxerr, abs(d - r))
print("recursion vs direct sums, k<=26, 14 frequencies each: max abs err = %.2e" % maxerr)
assert maxerr < 1e-9

NN = [1, 2, 2, 2]
for j in range(4, 3300): NN.append(NN[j - 3] + NN[j - 4])
def delta(k, n):
    mp.mp.prec = int(0.35 * k) + 160
    t = T_rec(k, 3 ** n)
    la = mp.log(abs(t)) if t != 0 else mp.mpf('-inf')
    lN = mp.log(NN[k])
    return float(-(la - lN) / lN)

ks = [200, 400, 800] + ([int(a) for a in sys.argv[1:]])
fr = [0.1, 0.3, 0.5, 0.6, 0.63, 0.66, 0.7]
print("delta(k, n) for xi = 3^n, n = round(frac*k):")
print(" k    " + "".join("%8.2f" % f for f in fr))
for k in ks:
    print("%5d " % k + "".join("%8.3f" % delta(k, round(f * k)) for f in fr), flush=True)
# fine scan around 0.63 and window average (R = ceil sqrt k) worst
for k in [200, 400]:
    R = math.ceil(math.sqrt(k))
    ds = {n: delta(k, n) for n in range(int(0.45 * k), int(0.72 * k) + 1)}
    nmin = min(ds, key=ds.get)
    print("k=%d: min single-frequency delta = %.3f at n=%d (n/k=%.3f)" % (k, ds[nmin], nmin, nmin / k))
    # worst window average of |T|/N over R consecutive n: delta0 = -log(avg |T|/N)/log N
    lN = math.log(NN[k]); ns = sorted(ds)
    best = 9
    for a in range(len(ns) - R + 1):
        avg = sum(math.exp(-ds[n] * lN) for n in ns[a:a + R]) / R
        best = min(best, -math.log(avg) / lN)
    print("      worst window (R=%d) delta0 over n/k in [0.45,0.72] = %.3f (report: %s)" % (R, best, {200: 0.126, 400: 0.099}[k]))
# stability under precision
mp.mp.prec = 600; t1 = T_rec(400, 3 ** 252); mp.mp.prec = 1200; t2 = T_rec(400, 3 ** 252)
print("precision check k=400,n=252: rel diff %.1e" % float(abs(t1 - t2) / abs(t2)))
