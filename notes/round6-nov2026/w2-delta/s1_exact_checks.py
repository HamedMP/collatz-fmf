#!/usr/bin/env python3
"""w2-delta s1: exact integer checks of the lemmas behind Theorems H and S.
Run: taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python s1_exact_checks.py
"""
from fractions import Fraction
from math import comb
import random, sys

def T(x, q=3, d=1):
    return x // 2 if x % 2 == 0 else (q * x + d) // 2

def vec(x, L, q=3, d=1):
    a = 0; bits = []
    for _ in range(L):
        bits.append(x & 1); a += x & 1; x = T(x, q, d)
    return tuple(bits), a, x

# (1) Terras bijection: x in [2^L,2^(L+1)) <-> parity vectors of length L
for (q, d) in [(3, 1), (3, -1), (3, 5), (5, 1)]:
    for L in range(1, 13):
        seen = set()
        for x in range(2**L, 2**(L + 1)):
            seen.add(vec(x, L, q, d)[0])
        assert len(seen) == 2**L, (q, d, L)
print("L1 Terras bijection on [2^L,2^(L+1)): OK for L<=12, maps (3,1),(3,-1),(3,5),(5,1)")

# (2) descent lemma: 3^a <= 2^(L-s-1)  =>  T^L(x) <= x/2^s   (x in [2^L, 2^(L+1)))
cnt = 0
for s in (1, 2, 3, 4):
    for L in range(1, 19):
        for x in range(2**L, 2**(L + 1)):
            _, a, y = vec(x, L)
            if 3**a * 2**(s + 1) <= 2**L:
                cnt += 1
                assert y * 2**s <= x, (s, L, x)
rnd = random.Random(1)
for _ in range(200000):
    L = rnd.randrange(19, 400); s = rnd.choice((2, 3, 4))
    x = rnd.randrange(2**L, 2**(L + 1))
    if rnd.random() < .5:   # adversarial: 2^m - 1 type and 0-heavy types
        x = (x >> (L // 2)) << (L // 2) | rnd.randrange(2**(L // 4))
        if x < 2**L: x += 2**L
    _, a, y = vec(x, L)
    if 3**a * 2**(s + 1) <= 2**L:
        cnt += 1
        assert y * 2**s <= x
print("L2 descent lemma: %d exact instances, 0 violations" % cnt)

# (3) remainder bound r_v/2^L <= (3/2)^a - 1 :  T^L(x) = (3^a x + r)/2^L
c3 = 0
for L in range(1, 17):
    for x in range(2**L, 2**(L + 1)):
        _, a, y = vec(x, L)
        r = y * 2**L - 3**a * x
        assert r >= 0 and r * 2**a <= (3**a - 2**a) * 2**L
        c3 += 1
print("L3 remainder bound: %d exact instances, 0 violations" % c3)

# (4) ancestor lemma on real trajectories: for every t, the sum of 1/x_k over good
#     ancestors k = t - L(x_k) is <= 2/(2^s x_t); and the full inequality of Thm H.
def check_traj(n, s=3):
    xs = [n]
    while xs[-1] != 1:
        xs.append(T(xs[-1]))
    K = len(xs)                       # distinct elements x_0..x_{K-1} (ends with 1)
    anc = {}
    bad = Fraction(0); ovh = Fraction(0)
    for k, x in enumerate(xs):
        L = x.bit_length() - 1
        a = sum(y & 1 for y in xs[k:k + L]) if k + L <= K else None
        if a is None:                 # window runs past the end: recompute a exactly
            _, a, _ = vec(x, L)
        if 3**a * 2**(s + 1) > 2**L:
            bad += Fraction(1, x)
        elif k + L >= K:
            ovh += Fraction(1, x)
        else:
            assert xs[k + L] * 2**s <= x
            anc.setdefault(k + L, []).append(x)
    for t, lst in anc.items():
        assert sum(Fraction(1, x) for x in lst) * 2**s * xs[t] <= 2, (n, t)
    assert ovh <= 1
    W = sum(Fraction(1, x) for x in xs)
    assert W <= bad + ovh + Fraction(2, 2**s) * W
    return float(W), float(bad), float(ovh)

mx = (0, 0)
tests = list(range(2, 3000)) + [2**k - 1 for k in range(2, 70)] + [27, 703, 871, 6171, 77031, 837799, 8400511, 63728127, 993] \
        + [random.Random(7).randrange(2, 10**12) for _ in range(300)]
for n in tests:
    W, bad, ovh = check_traj(n)
    if W > mx[0]: mx = (W, n)
print("L4 ancestor lemma + inequality W <= bad + ovh + (2/8)W: %d trajectories OK; max harmonic sum %.6f at n=%d" % (len(tests), mx[0], mx[1]))
