"""Hostile-referee brute force for sunit B3/B4 (independent re-implementation)."""
import random, math, itertools, sys
from math import gcd, log2
random.seed(20261117)
TH = log2(3)
def v2(n): return (n & -n).bit_length() - 1

def hop(x, a=3):
    """odd x (x != -1); returns (s, v, x') via the report's formula (a=3: y=x+1)."""
    y = x + 1
    s = v2(y); m = y >> s
    q = a**s * m - 1
    e = v2(q)            # v-1
    return s, e + 1, q >> e

def literal(x):
    """first value divisible by 4 in the Collatz orbit after odd x, reduced to odd."""
    z = 3 * x + 1
    while z % 4:
        z = z // 2 if z % 2 == 0 else 3 * z + 1
    return z >> v2(z), v2(z)

# ---------- A. hop formula, Lemma 1, Lemma 3 on > 10^6 hops ----------
nh = 0; worst = -9.0
def check_hop(x, lit=False):
    global nh, worst
    s, v, xp = hop(x)
    h = s + v - 1
    y, yp = x + 1, xp + 1
    assert v >= 2 and s >= 1 and xp >= 1 and xp % 2 == 1
    assert (1 << h) * yp == 3**s * y + (1 << h) - (1 << s)          # Lemma 1
    assert yp << s <= 3**s * y                                       # Lemma 3(b) exact: y' <= (3/2)^s y
    if lit:
        assert literal(x) == (xp, v), x
    if x < 1 << 60:
        worst = max(worst, log2(yp) - log2(y) - (TH - 1) * s)
    nh += 1
    return s, h, xp
for x in range(1, 1_400_001, 2):
    check_hop(x, lit=True)
for _ in range(3000):
    x = random.getrandbits(random.randint(20, 300)) | 1
    for _ in range(100):
        s, h, x = check_hop(x)
for n in range(1, 400):
    x = (1 << n) - 1
    for _ in range(50):
        s, h, x = check_hop(x)
print("A: hops checked", nh, " max of L'-L-(th-1)s (should be <=0):", worst)

# ---------- B. window bookkeeping (D) and Lemma 3 Z-bound ----------
def orbit(x, K):
    out = []
    for _ in range(K):
        s, v, xn = hop(x); out.append((x, s, s + v - 1)); x = xn
    return out, x
maxexc = {1: (-99, 0), 2: (-99, 0), 3: (-99, 0)}
longest_inc = (0, 0)
cnt = 0
for x0 in list(range(1, 400_001, 2)) + [(1 << n) - 1 for n in range(2, 200)]:
    orb, xe = orbit(x0, 40 if x0 < 400_001 else 12)
    ss = [o[1] for o in orb]; hs = [o[2] for o in orb]; xs = [o[0] for o in orb]
    S = 0; H = 0
    for j in range(len(orb)):
        Lj = log2(xs[j] + 1)
        assert Lj <= log2(x0 + 1) + (TH - 1) * S + 1e-9              # L_j <= L_0 + (th-1) S_j
        assert (1 << H) * (xs[j] + 1) <= (1 << j) * 3**S * (x0 + 1)  # Z_j <= 2^j 3^S y_0
        assert ss[j] <= Lj + 1e-12
        S += ss[j]; H += hs[j]
    for k in (1, 2, 3):
        win = sum(hs[:k]) + ss[k]
        assert sum(ss[:k + 1]) + k <= win
        e = win - log2(x0 + 1)
        if x0 > 3 and e > maxexc[k][0]: maxexc[k] = (e, x0)
    # longest strictly increasing run of s
    run = 1
    for j in range(1, len(ss)):
        run = run + 1 if ss[j] > ss[j - 1] else 1
        if run > longest_inc[0]: longest_inc = (run, x0)
    cnt += 1
print("B: orbits", cnt, " max T_k-L_0 (k=1,2,3):", maxexc, " longest strictly increasing s-run:", longest_inc)

# x0 = 1: C(k,delta) >= 2k - delta ; ratio 1 forever
orb, _ = orbit(1, 20); assert all(o[1:] == (1, 2) for o in orb)
print("B: x=1 letters s=1,h=2 forever (ratio 1; not excluded by Cor C)")

# 2^n - 1 : second depth after the spike
mx = 0
for n in range(2, 3000):
    s0, v0, x1 = hop((1 << n) - 1); assert s0 == n
    s1 = v2(x1 + 1); mx = max(mx, s1 / n)
    # k=1 window vs L0=n
print("B: max s_1/s_0 over x0=2^n-1, n<3000:", mx)

# ---------- C. Theorem E recursion: worst-case iteration of the proved inequalities ----------
# a_{n+1} <= q a_n + b with q = theta + delta*(theta-1)
for (k, d, L0, C) in [(1, .1, 10, 50), (5, .01, 100, 1e4), (20, .5, 3, 1e6)]:
    q = 1 + (1 + d) * (TH - 1); b = (1 + d) * L0 + C
    a = 0.0
    for n in range(1, 60):
        a = q * a + b
        assert a <= (b / (q - 1)) * q**n * (1 + 1e-12)
print("C: recursion bound a_n <= b/(q-1) q^n ok; q = theta + delta(theta-1)")

# ---------- D. litmus: 5n+1 through 13, 3n-1 cycles (negative x under 3n+1) ----------
def ghop(y, a, d):
    s = v2(y); m = y >> s
    q = a**s * m - d
    e = v2(q)
    return s, s + e, (q >> e) + d            # (s, h, y')
y = 3 * 13 + 1; lets = []
for _ in range(30):
    s, h, y = ghop(y, 5, 1); lets.append((s, h))
print("D: 5n+1 @13 letters:", set(lets), " y stays", y)
for xs0 in (-5, -17, -7, -3, -9, -11, -91):
    x = xs0; lets = []; seq = []
    for _ in range(40):
        if x == -1: lets.append("HIT -1 (y=0, void)"); break
        s, v, xn = hop(x); lets.append((s, s + v - 1)); seq.append(x)
        assert abs(xn + 1) << s <= 3**s * abs(x + 1)
        x = xn
    print("D: 3n-1 as x=%d:" % xs0, lets[:8], "...", "orbit", seq[:6])

# ---------- E. return map, Theorem F tuple, n <= 10^6 (and negatives), s <= 3 ----------
def rstep(n):
    y = 33 * n + 32
    if y == 0: return None
    t = v2(y)
    if t % 4: return None
    r = t // 4; w = y >> t
    if w % 8 != (7 if r % 2 == 0 else 5): return None
    P = 9 * 27**r; Q = 1 << (4 * r + 3)
    D = 1 if r == 0 else (2592 * 27**(r - 1) - 85 * 16**r) // 11
    assert (2592 * 27**(r - 1) - 85 * 16**r) % 11 == 0 if r else True
    assert (P * n + D) % Q == 0
    n2 = (P * n + D) // Q
    # block form in v coordinates
    v = 8 * y; assert v == (1 << (4 * r + 3)) * w
    assert 8 * (33 * n2 + 32) == 3**(3 * r + 2) * w + 1
    return n2, r
def sfree(z):
    z = abs(z)
    while z % 2 == 0: z //= 2
    while z % 3 == 0: z //= 3
    return z
stats = {}; nt = 0; lenhist = {}
def retcheck(n0, smax=3, positive=True):
    global nt
    ns = [n0]; word = []
    while len(word) < smax + 1:
        st = rstep(ns[-1])
        if st is None: break
        ns.append(st[0]); word.append(st[1])
    L = len(word); lenhist[L] = lenhist.get(L, 0) + 1
    vs = [8 * (33 * n + 32) for n in ns]
    for s in range(1, L):          # letters r_0..r_s
        a = [4 * r + 3 for r in word[:s + 1]]; b = [3 * r + 2 for r in word[:s + 1]]
        w = [vs[l] >> a[l] for l in range(s + 1)]
        assert all(vs[l] == w[l] << a[l] and w[l] % 2 for l in range(s + 1))
        A = sum(a[1:]); B = sum(b[:s])
        units = [3**sum(b[l:s]) * 2**sum(a[1:l]) for l in range(1, s + 1)]
        tup = [(1 << A) * w[s], -3**B * w[0]] + [-u for u in units]
        assert len(tup) == s + 2
        assert sum(tup) == 0
        vals = [v2(t) for t in tup]
        assert vals[0] == A and vals[1] == 0 and vals[2:] == [sum(a[1:l]) for l in range(1, s + 1)]
        sv = sorted(vals); assert sv[0] == sv[1] == 0 and all(sv[i] < sv[i + 1] for i in range(1, len(sv) - 1))
        for size in range(1, len(tup)):
            for I in itertools.combinations(range(len(tup)), size):
                assert sum(tup[i] for i in I) != 0
        g = 0
        for t in tup: g = gcd(g, t)
        assert g == 1
        assert sum(units) <= 3**B
        assert 4 * B <= 3 * (a[0] + A)
        nt += 1
        if positive:
            assert w[0] > 0 and w[s] > 0
            prod = 1
            for t in tup: prod *= sfree(t)
            assert prod <= w[0] * w[s]
            assert max(abs(t) for t in tup) >= (1 << A) * w[s]
            assert (1 << A) * w[s] <= 2 * 3**B * w[0]
            exc = a[0] + A - log2(vs[0])
            if exc > stats.get(s, (-99,))[0]: stats[s] = (exc, n0, tuple(word[:s + 1]))
    return L
for n0 in range(0, 1_000_001):
    retcheck(n0)
print("E: positive n<=1e6: tuples checked", nt, " word-length histogram (cap 4):", dict(sorted(lenhist.items())))
print("E: max excess sum(a_l) - log2 v_0 by s:", stats)
nt0 = nt
for n0 in range(-200_000, 0):
    retcheck(n0, positive=False)
print("E: negative n: extra tuples (identity/valuation/subsum/gcd only):", nt - nt0)
# forced long words: least residues for all words of length <=4 over letters 0..3
cntw = 0; minratio = {}
for L in range(2, 5):
    for word in itertools.product(range(4), repeat=L):
        P, Q, D = 1, 1, 0
        for r in word:
            p = 9 * 27**r; q = 1 << (4 * r + 3)
            dd = 1 if r == 0 else (2592 * 27**(r - 1) - 85 * 16**r) // 11
            P, Q, D = p * P, q * Q, p * D + dd * Q
        R = (-D * pow(P, -1, Q)) % Q
        assert R >= 1
        for mult in (0, 1, 7):
            assert retcheck(R + Q * mult, smax=L - 1) >= L
        ns = R; ok = True
        for r in word:
            st = rstep(ns); assert st is not None and st[1] == r; ns = st[0]
        cntw += 1
        rat = log2(R) / log2(Q)
        if rat < minratio.get(L, (9,))[0]: minratio[L] = (rat, word, R, Q)
print("E: all", cntw, "words over {0..3}, len 2..4 realised by least residue R_W>=1; min log R_W/log Q_W:", minratio)
print("E: n=-1:", rstep(-1), " n=0:", rstep(0))
print("ALL REFEREE CHECKS PASSED")
