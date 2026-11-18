#!/usr/bin/env python3
"""w4-E e1: exact checks of the shadow identity (Theorem Sh) and of the cycle product identity on all control maps.
Map family: T(x) = x/2 (x even), (q x + c(x))/2 (x odd), c(x) odd, possibly x-dependent (S_a).
Finite shadow identity (exact rationals), for 0 <= k <= K:
   x_k = M(k,K) x_K - sum_{k<=i<K, x_i odd} (c_i/q) M(k,i),   M(k,i) = 2^(i-k) / q^(a_i-a_k).
Run: taskset -c 4 python e1_shadow.py
"""
from fractions import Fraction as F
import random
random.seed(20261118)

def step(x, q, cfun):
    if x % 2 == 0: return x // 2, None
    c = cfun(x); return (q * x + c) // 2, c

def traj(n, q, cfun, K):
    xs = [n]; cs = []
    for _ in range(K):
        y, c = step(xs[-1], q, cfun); xs.append(y); cs.append(c)
    return xs, cs

def check_shadow(n, q, cfun, K):
    xs, cs = traj(n, q, cfun, K)
    # backward recursion delta_k^(K): delta_K = 0; even: delta_k = 2 delta_{k+1}; odd: delta_k = (2 delta_{k+1} + c)/q
    delta = F(0); Mk = F(1)   # Mk = M(k,K)
    cnt = 0
    for k in range(K - 1, -1, -1):
        if cs[k] is None: delta = 2 * delta; Mk = 2 * Mk
        else: delta = (2 * delta + cs[k]) / q; Mk = Mk * F(2, q)
        assert xs[k] == Mk * xs[K] - delta, (n, q, k)
        cnt += 1
    return cnt

def Sa(a):
    return lambda x: 1 - (2 ** (a + 1) if (x + 1) % 2 ** (a + 1) == 0 else 0)   # S_a = T - 2^a on x = -1 mod 2^(a+1)

tot = 0
for q, cf, name in [(3, lambda x: 1, "3n+1"), (3, lambda x: -1, "3n-1"), (5, lambda x: 1, "5n+1"),
                    (3, lambda x: 5, "3n+5"), (3, lambda x: 7, "3n+7"), (3, lambda x: 11, "3n+11"),
                    (3, Sa(0), "S_0"), (3, Sa(3), "S_3"), (3, Sa(6), "S_6")]:
    c = 0
    starts = [2 ** j - 1 for j in range(2, 40)] + [random.getrandbits(100) | 1 for _ in range(60)] + list(range(1, 60))
    for n in starts:
        c += check_shadow(n, q, cf, 120)
    tot += c
    print("%-6s shadow identity: %d exact instances OK" % (name, c))
print("TOTAL exact instances:", tot)

# cycle product identity 2^p = q^a prod(1 + c_i/(q x_i)) and the value of p versus ceil/floor(a log2 q)
from math import log2, ceil, floor
def cyc(n, q, cfun):
    xs = [n]; a = 0; P = F(1)
    while True:
        x = xs[-1]; y, c = step(x, q, cfun)
        if c is not None: a += 1; P *= 1 + F(c, q * x)
        if y == n: break
        xs.append(y)
    p = len(xs)
    assert F(2 ** p, q ** a) == P
    return p, a, float(P), min(xs)
print("\ncycle identity 2^p/q^a = prod(1+c/(q x)) (exact):")
for n, q, cf, name in [(1, 3, lambda x: 1, "3n+1 {1,2}"), (1, 3, lambda x: -1, "3n-1 {1}"), (5, 3, lambda x: -1, "3n-1 thru 5"),
                       (17, 3, lambda x: -1, "3n-1 thru 17"), (13, 5, lambda x: 1, "5n+1 thru 13"), (17, 5, lambda x: 1, "5n+1 thru 17"),
                       (1, 5, lambda x: 1, "5n+1 thru 1"), (1, 3, lambda x: 5, "3n+5 thru 1"), (19, 3, lambda x: 5, "3n+5 thru 19"),
                       (23, 3, lambda x: 5, "3n+5 thru 23"), (187, 3, lambda x: 5, "3n+5 thru 187"), (347, 3, lambda x: 5, "3n+5 thru 347"),
                       (5, 3, lambda x: 7, "3n+7 thru 5"), (1, 3, lambda x: 11, "3n+11 thru 1"), (13, 3, lambda x: 11, "3n+11 thru 13"),
                       (1, 3, Sa(0), "S_0 fixed 1"), (15, 3, Sa(3), "S_3 fixed 15"), (127, 3, Sa(6), "S_6 fixed 127")]:
    p, a, P, m = cyc(n, q, cf)
    print("  %-14s p=%3d a=%3d min=%4d  2^p/q^a=%.6f  ceil(a log2 q)=%3d floor=%3d  p==ceil:%s" %
          (name, p, a, m, P, ceil(a * log2(q)), floor(a * log2(q)), p == ceil(a * log2(q))))
