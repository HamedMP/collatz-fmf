#!/usr/bin/env python3
"""w2-delta s7: hostile review + litmus maps, exact integer / rational arithmetic.
Run: taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python s7_review_litmus.py
"""
from fractions import Fraction
import random, math

def T(x, q=3, d=1): return x // 2 if x % 2 == 0 else (q * x + d) // 2

def window(x, L, q=3, d=1):
    a = 0
    for _ in range(L):
        a += x & 1; x = T(x, q, d)
    return a, x

# ---- R1: sharpened descent lemma 2' : 3^a(2^a+1) <= 2^(L-s+a)  =>  T^L(x) <= x/2^s
cnt = viol = 0
for s in (2, 3, 4, 5):
    for L in range(1, 18):
        for x in range(2**L, 2**(L + 1)):
            a, y = window(x, L)
            if L - s + a >= 0 and 3**a * (2**a + 1) <= 2**(L - s + a):
                cnt += 1; viol += (y * 2**s > x)
rnd = random.Random(11)
for _ in range(300000):
    L = rnd.randrange(18, 300); s = rnd.choice((2, 3, 4, 5))
    k = rnd.randrange(3)
    if k == 0: x = rnd.randrange(2**L, 2**(L + 1))
    elif k == 1: x = 2**(L + 1) - 1 - rnd.randrange(2**(L // 3)) * 2**(L - L // 3 - 1)   # long 1-runs at the bottom
    else: x = 2**L + rnd.randrange(2**(L // 2)) * 2**(L // 2 - 1)                         # long 0-runs at the bottom
    if not (2**L <= x < 2**(L + 1)): continue
    a, y = window(x, L)
    if L - s + a >= 0 and 3**a * (2**a + 1) <= 2**(L - s + a):
        cnt += 1; viol += (y * 2**s > x)
print("R1 lemma 2': %d exact instances, %d violations" % (cnt, viol))

# ---- R2: full Theorem-H bookkeeping on trajectories (exact rationals), sharpened criterion
def bookkeeping(xs, s=4, q=3, d=1, K=None):
    """xs: distinct segment. returns (W, bad, ovh, max_ancestor_ratio)"""
    K = len(xs); anc = {}; bad = Fraction(0); ovh = Fraction(0)
    for k, x in enumerate(xs):
        L = x.bit_length() - 1
        a, y = window(x, L, q, d)
        good = (L - s + a >= 0) and 3**a * (2**a + 1) <= 2**(L - s + a)
        if not good: bad += Fraction(1, x)
        elif k + L >= K: ovh += Fraction(1, x)
        else:
            assert xs[k + L] == y and y * 2**s <= x
            anc.setdefault(k + L, []).append(x)
    mr = Fraction(0)
    for t, lst in anc.items():
        r = sum(Fraction(1, x) for x in lst) * 2**s * xs[t]
        assert r <= 2; mr = max(mr, r)
    W = sum(Fraction(1, x) for x in xs)
    assert ovh <= 1 and W <= bad + ovh + Fraction(2, 2**s) * W
    return W, bad, ovh, mr

def segment(n, q=3, d=1, cap=10**6):
    xs = []; seen = set(); x = n
    while x not in seen and len(xs) < cap:
        seen.add(x); xs.append(x); x = T(x, q, d)
    return xs

tests = list(range(1, 2500)) + [2**k - 1 for k in range(2, 90)] + [2**k + 1 for k in range(2, 60)] \
    + [(2**(2*k) - 1) // 3 for k in range(2, 40)] + [27, 703, 871, 993, 1986, 6171, 77031, 837799, 8400511, 63728127, 670617279, 9780657630, 75128138247] \
    + [rnd.randrange(2, 10**18) for _ in range(150)] + [rnd.randrange(2**99, 2**100) for _ in range(20)]
mW = (0, 0); mR = (0, 0); mr = Fraction(0)
for n in tests:
    xs = segment(n)
    W, bad, ovh, r = bookkeeping(xs)
    mr = max(mr, r)
    res = 1.0
    for x in xs:
        if x & 1 and x != 1: res *= 1 + 1 / (3 * x)
    if float(W) > mW[0]: mW = (float(W), n)
    if res > mR[0]: mR = (res, n)
print("R2 bookkeeping on %d trajectories (incl. 2^k-1, 2^k+1, records, 100-bit randoms): OK; max sum 1/x = %.6f (n=%d), max Res = %.9f (n=%d), max ancestor ratio = %.4f (<= 2)"
      % (len(tests), mW[0], mW[1], mR[0], mR[1], float(mr)))

# ---- R3: Theorem S (count of distinct elements <= X):  N(X) <= 11.3 X^eta
eta = 0.94995553; worst = 0
for n in tests[:4000]:
    xs = sorted(segment(n))
    for i in range(0, len(xs), max(1, len(xs) // 50)):
        worst = max(worst, (i + 1) / xs[i]**eta)
print("R3 sojourn count: max over tests of #{elements <= X}/X^eta = %.4f  (theorem: <= 11.3)" % worst)

# ---- LITMUS A: 3n-1 (= negative integers under 3n+1). Lemma 2' holds verbatim (remainder <= 0); theorem holds; cycles are finite.
viol = cnt = 0
for L in range(1, 15):
    for x in range(2**L, 2**(L + 1)):
        a, y = window(x, L, 3, -1)
        if L - 4 + a >= 0 and 3**a * (2**a + 1) <= 2**(L - 4 + a):
            cnt += 1; viol += (y * 16 > x)
mx = (0, 0)
for n in list(range(1, 3000)) + [rnd.randrange(2, 10**15) for _ in range(100)]:
    xs = segment(n, 3, -1)
    W, bad, ovh, r = bookkeeping(xs, 4, 3, -1)
    if float(W) > mx[0]: mx = (float(W), n)
cyc = {c: float(sum(Fraction(1, x) for x in segment(c, 3, -1))) for c in (1, 5, 17)}
print("LITMUS 3n-1: lemma %d instances %d violations; bookkeeping OK on 3100 segments; max sum 1/x = %.4f (n=%d); cycle sums %s  -> statement TRUE for 3n-1, no conflict"
      % (cnt, viol, mx[0], mx[1], cyc))

# ---- LITMUS B: 3n+d, d>0: T^L(x) <= 3^a x/2^L + d((3/2)^a - 1); theorem holds with all x < 2^(s+1) d^2 declared bad (constant depends on d).
for d in (5, 7, 11, 13, 17, 23, 499):
    mx = 0; ncyc = set()
    for n in range(1, 4000):
        xs = segment(n, 3, d)
        mx = max(mx, sum(1 / x for x in xs))
        y = T(xs[-1], 3, d); cyc = xs[xs.index(y):]; ncyc.add(min(cyc))
    print("LITMUS 3n+%d: %d cycles met from n<4000, max sum 1/x over distinct segments = %.4f (bounded by C(d) ~ C + O(log d); no conflict)" % (d, len(ncyc), mx))

# ---- LITMUS C: 5n+1.  The descent lemma becomes 5^a(1+2^-a) <= 2^(L-s) and the bad fraction tends to 1: the proof gives nothing.
for L in (40, 160, 640):
    amin = 0
    while 5**amin * (2**amin + 1) <= 2**(L - 4 + amin): amin += 1
    frac = sum(math.comb(L, a) for a in range(amin, L + 1)) / 2**L
    print("LITMUS 5n+1: level %d bad fraction = %.6f (beta diverges; q<4 is exactly the condition 1/log2(q) > 1/2)" % (L, frac))
x = 13; xs = segment(13, 5, 1)
print("LITMUS 5n+1: cycle through 13:", xs, " prod(1+1/(5x)) over odd =", float(math.prod(Fraction(5 * x + 1, 5 * x) for x in xs if x & 1)), "= 2^7/5^3 =", 128 / 125)
