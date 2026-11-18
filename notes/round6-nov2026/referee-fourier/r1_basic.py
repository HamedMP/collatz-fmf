# Steps 1,2,4: E_k brute vs recursion, T_k recursions, Prop 4, Selberg/Prop 1 chain, Prop 3 mirror.
import math, cmath, random, sys
from fractions import Fraction as Fr
import numpy as np
random.seed(7)
def Erec(k, memo={}):
    if k in memo: return memo[k]
    if k == 0: r = [0]
    elif k <= 3: r = [0, 2**k-1]
    else:
        M = 1 << k; i9 = pow(9,-1,M); i27 = pow(27,-1,M)
        r = [((8*z-1)*i9) % M for z in Erec(k-3)] + [(16*z*i27) % M for z in Erec(k-4)]
    memo[k] = r; return r
def Ebrute(k, z0):
    # all words v with Q_v >= k+? applied to arbitrary seed z0 (2-adic integer mod 2^k); independent of seed
    M = 1 << k; i9 = pow(9,-1,M); i27 = pow(27,-1,M)
    # f_v = f_v1 o ... o f_vn : build by composing on the right => track affine map z -> (A z + B) mod M
    out = set(); st = [(1, 0, 0)]
    while st:
        A, B, Q = st.pop()
        if Q >= k: out.add((A*z0 + B) % M); continue
        # f_v o f_a : z -> A*(8z-1)/9 + B
        st.append((A*8*i9 % M, (B - A*i9) % M, Q+3))
        st.append((A*16*i27 % M, B, Q+4))
    return out
Nrec = [1,2,2,2]
for k in range(4, 6000): Nrec.append(Nrec[k-3]+Nrec[k-4])
ok = True
for k in range(0, 27):
    e = Erec(k)
    b1 = Ebrute(k, 0); b2 = Ebrute(k, 12345677); b3 = Ebrute(k, -1 % (1<<k))
    if not (set(e) == b1 == b2 == b3 and len(e) == len(set(e)) == Nrec[k]): ok = False; print("E_k mismatch", k, len(e), len(b1), len(b2), Nrec[k])
print("step1: E_k brute(3 seeds)==recursion, distinct, #=N_k for k<=26:", ok)
def T(k, xi):
    M = 1 << k
    return sum(cmath.exp(2j*math.pi*((xi*c) % M)/M) for c in Erec(k))
def e(n, M): return cmath.exp(2j*math.pi*(n % M)/M)
bad1 = bad2 = bad3 = 0; mx = 0
for _ in range(400):
    k = random.randint(4, 24); M = 1 << k; xi = random.randrange(M)
    i = lambda p: pow(3, -p, M)
    rhs = e(-xi*i(2), M)*T(k-3, xi*i(2) % (1 << (k-3))) + T(k-4, xi*i(3) % (1 << (k-4)))
    d = abs(T(k, xi)-rhs); mx = max(mx, d); bad1 += d > 1e-7
    if k >= 8:
        co = e(-xi*i(2), M) + e(-16*xi*i(5), M)
        rhs = e(-xi*i(2) - 8*xi*i(4), M)*T(k-6, xi*i(4) % (1 << (k-6))) + co*T(k-7, xi*i(5) % (1 << (k-7))) + T(k-8, xi*i(6) % (1 << (k-8)))
        d = abs(T(k, xi)-rhs); mx = max(mx, d); bad2 += d > 1e-7
        bad3 += abs(abs(co) - 2*abs(math.cos(math.pi*((11*xi*i(5)) % M)/M))) > 1e-9
print("step1: one-step failures %d, 2-block failures %d, modulus failures %d, max dev %.2e" % (bad1, bad2, bad3, mx))
# does the 2-block identity fail for k<8 (sharpness of k>=8)?  skip: T_{k-8} undefined.

# ---- step 2: growth constants, monotonicity, Selberg
s = math.log2(1.2207440846057596)
lam = 1.2207440846057596
print("lambda^4-lambda-1 =", lam**4-lam-1, " s =", s)
rat = [Nrec[k]/lam**k for k in range(1, 6000) if k < 2000]
print("N_k/2^(sk): min %.6f (k>=1) max %.6f ; k=0: %.3f" % (min(rat), max(rat), 1.0))
mono = all(Nrec[j] >= Nrec[j-1] for j in range(2, 5999)); print("N_j nondecreasing for j>=1:", mono)
def Ncount(Q, m): return sum(1 for c in Erec(Q+m) if c < (1 << Q))
okm = True
for Q in range(0, 20):
    v = [Ncount(Q, m) for m in range(0, 27-Q)]
    if any(v[i+1] > v[i] for i in range(len(v)-1)): okm = False
    if Q in (5, 9, 12): print("  N(Q=%d,m): %s" % (Q, v))
print("step2: N(Q,m) non-increasing in m (Q<20, Q+m<=26):", okm)
print("  N(Q,Q) for Q=0..13:", [Ncount(Q, Q) for Q in range(0, 14)])
def selberg(alpha, beta, H, G):
    # returns S+ on grid of G points and S- ; Vaaler construction
    x = np.arange(G)/G
    k = np.arange(1, H+1); u = k/(H+1)
    f = -(1-u)/np.tan(math.pi*u) - 1/math.pi
    def V(y): return (np.sin(2*math.pi*np.outer(y, k)) @ f)/(H+1)
    def Fej(y): return 1 + 2*(np.cos(2*math.pi*np.outer(y, k)) @ (1-u))
    def Bp(y): return V(y) + Fej(y)/(2*(H+1))
    def Bm(y): return V(y) - Fej(y)/(2*(H+1))
    return (lambda y: beta-alpha + Bp(y-beta) + Bp(alpha-y)), (lambda y: beta-alpha + Bm(y-beta) + Bm(alpha-y))
worst = 0; okS = True; okchain = True; rows = []
for K in (12, 16, 20, 24, 26):
    EK = np.array(Erec(K), dtype=np.float64)/2.0**K
    for m in range(1, min(K//2, 9)+1):
        Q = K-m; H = 2**m-1; I = 2.0**-m
        Sp, Sm = selberg(0.0, I, H, 0)
        G = 16*(H+1)*8
        x = np.arange(G)/G; vals = Sp(x); ind = ((x >= 0) & (x <= I)).astype(float)
        if (vals - ind).min() < -1e-9: okS = False; print("NOT a majorant", K, m, (vals-ind).min())
        if (Sm(x) - ((x > 0) & (x < I))).max() > 1e-9: okS = False; print("NOT a minorant", K, m)
        co = np.fft.fft(vals)/G
        if abs(co[0].real - (I + 1/(H+1))) > 1e-9: okS = False; print("s(0) wrong", co[0])
        if np.abs(co[H+1:G-H]).max() > 1e-9: okS = False; print("degree > H")
        for h in range(1, H+1):
            bnd = 1/(H+1) + min(I, 1/(math.pi*h))
            worst = max(worst, abs(co[h])/bnd)
            if abs(co[h]) > bnd + 1e-12: okS = False; print("coef bound fails", K, m, h, abs(co[h]), bnd)
        cnt = Ncount(Q, m)
        direct = Sp(EK).sum()
        Tm = {h: T(K, h) for h in range(1, H+1)}
        four = co[0].real*len(EK) + 2*sum((co[h]*Tm[h]).real for h in range(1, H+1))
        chain = len(EK)*(I + 1/(H+1)) + 2*sum((1/(H+1) + I)*abs(Tm[h]) for h in range(1, H+1))
        if not (cnt <= direct + 1e-6 and abs(direct-four) < 1e-5 and four <= chain + 1e-6): okchain = False; print("CHAIN FAIL", K, m, cnt, direct, four, chain)
        if K in (24, 26): rows.append((K, Q, m, cnt, round(direct, 2), round(chain, 1), len(EK)))
print("step2: Selberg majorant/minorant valid, s(0), degree, coefficient bounds:", okS, " max |s(h)|/bound = %.4f" % worst)
print("step2: N(Q,m) <= sum_c S+(c/2^K) = sum_h s(h)T_K(h) <= report line-3 bound:", okchain)
for r in rows: print("   K=%d Q=%d m=%d  N(Q,m)=%d  sum S+=%s  chain bound=%s  N_K=%d" % r)
for d in (0.1, 0.25, 0.5, 0.9):
    th = s*d/(1-s*d); e1 = s-(1-s)*th; e2 = s*(1-d)*(1+th)
    print("  delta=%.2f theta=%.5f: exponent term1 %.6f term2 %.6f  s-delta' %.6f" % (d, th, e1, e2, s-(1-s)*s*d/(1-s*d)))

# ---- step 4: mirror
def frac3(x):
    n, d = x.numerator, x.denominator; b = 0
    while d % 3 == 0: d //= 3; b += 1
    return Fr((n*pow(d, -1, 3**b)) % 3**b, 3**b) if b else Fr(0)
def frac2(x):
    n, d = x.numerator, x.denominator; b = 0
    while d % 2 == 0: d //= 2; b += 1
    return Fr((n*pow(d, -1, 2**b)) % 2**b, 2**b) if b else Fr(0)
def params(K):
    out = []; st = [(0, 0, 0, '')]
    while st:
        P, Q, D, w = st.pop()
        if K-Q <= 3:
            for z in ([0] if K == Q else [0, -1]): out.append((w, z, Fr(z*(1 << Q) - D, 3**P), P))
            continue
        st.append((P+2, Q+3, 9*D + (1 << Q), w+'a')); st.append((P+3, Q+4, 27*D, w+'b'))
    return out
def fword(w, z):
    r = Fr(z)
    for ch in reversed(w): r = (8*r-1)/9 if ch == 'a' else 16*r/27
    return r
okp = True; okmir = True; coinc = {}
for K in range(0, 27):
    pr = params(K); M = 1 << K
    cs = []
    for w, z, r, P in pr:
        if K <= 18 and fword(w, z) != r: okp = False; print("D-recursion wrong", K, w, z)
        cs.append((r.numerator*pow(r.denominator, -1, M)) % M)
        if not (-1 <= r <= 0): okp = False; print("r out of [-1,0]", r)
    if sorted(cs) != sorted(Erec(K)) or len(set(cs)) != len(cs): okp = False; print("param not bijection", K)
    hs = [1, 2, 3, 5, 11, 27, 243, -7, 1001, 3**9, M//3+1, random.randrange(1, 10**12)]
    for h in hs:
        for (w, z, r, P), c in zip(pr, cs):
            x = Fr(h)*r/M
            if (x - frac2(x) - frac3(x)).denominator != 1 or (Fr(h*c, M) - (x - frac3(x))).denominator != 1: okmir = False
        # complex identity
    from collections import defaultdict
    d = defaultdict(list)
    for w, z, r, P in pr: d[r - math.floor(r)].append((w, z, r))
    coinc[K] = [v for v in d.values() if len(v) > 1]
print("step4: parametrisation is a bijection onto E_K (K<=26), r in [-1,0]:", okp)
print("step4: mirror identity exact (12 h per K, K<=26):", okmir)
for K in (4, 5, 6, 7, 8, 9, 22, 25, 26):
    print("   K=%d coincidences mod 1: %s" % (K, [[(w if len(w) < 12 else w[:3]+'..'+str(len(w)), z, str(r)) for w, z, r in v] for v in coinc[K]]))
print("   number of coincident groups per K (0..26):", [len(coinc[K]) for K in range(27)], " group sizes max:", max([len(v) for K in range(27) for v in coinc[K]] + [0]))
