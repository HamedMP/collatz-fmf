#!/usr/bin/env python3
"""Independent check of a dumped (j,p,q)-certificate for the map n -> n/2 | (a n + c)/2, plus
(i) brute-force check of the game moves against true predecessors of random integers,
(ii) a simulation of Lemma 1: play the strategy on actual integers starting from n0 (off every cycle),
    checking  #O >= (p k - g(n0))/q,  n_k <= n0 2^k / a^m (for c=+1),  T^k(n_k) = n0  and distinctness.
usage: verify_cert.py a c j p q certfile [n0] [steps]"""
import sys, random
import numpy as np
a, c, j, p, q = map(int, sys.argv[1:6]); f = sys.argv[6]
n0 = int(sys.argv[7]) if len(sys.argv) > 7 else 4
steps = int(sys.argv[8]) if len(sys.argv) > 8 else 3000
N = a**j; N1 = N // a
g = np.fromfile(f, dtype=np.int32).astype(np.int64)
assert len(g) == N and g.min() >= 0
r = np.arange(N, dtype=np.int64); live = r % a != 0
# E condition: g(2r) <= g(r) - p
condE = g[(2 * r) % N] <= g - p
u = (2 * r - c) % (a * a)
allowed = (u % a == 0) & (u != 0)
b = ((2 * r - c) // a) % N1                       # floor division; exact where allowed
worst = np.max(np.stack([g[b + t * N1] for t in range(a)]), axis=0)
condO = allowed & (worst <= g + q - p)
bad = live & ~(condE | condO)
print(f"certificate check a={a} c={c} j={j} p/q={p}/{q}: states={int(live.sum())} violations={int(bad.sum())} max g={int(g[live].max())}")
assert bad.sum() == 0
# (i) moves vs real integers
random.seed(1)
for _ in range(20000):
    n = random.randrange(1, 10**30)
    if n % a == 0: continue
    rr = n % N
    assert (2 * n) % N == (2 * rr) % N
    real = (2 * n - c) % a == 0 and ((2 * n - c) // a) % a != 0
    assert real == bool(allowed[rr])
    if real:
        m = (2 * n - c) // a
        assert (a * m + c) % 2 == 0 and (a * m + c) // 2 == n and m % 2 in (0, 1)
        assert m % N1 == b[rr] and m % a != 0
print("moves agree with true predecessors on 20000 random integers (O-move legality, residue of child mod a^(j-1))")
# (ii) Lemma 1 simulation
def T(n): return n // 2 if n % 2 == 0 else (a * n + c) // 2
n = n0; assert n % a != 0
seen = {n}; k = m_ = 0; g0 = int(g[n % N])
for _ in range(steps):
    rr = n % N
    if condE[rr] and not condO[rr]: n = 2 * n
    elif condO[rr]: n = (2 * n - c) // a; m_ += 1
    else: raise SystemExit("stuck")
    k += 1
    assert n > 0 and n % a != 0 and n not in seen; seen.add(n)
    assert q * m_ >= p * k - g0
    if c == 1: assert n * a**m_ <= n0 * 2**k
x = n
for _ in range(k): x = T(x)
assert x == n0
import math
print(f"Lemma-1 play from n0={n0}: k={k} steps, #O={m_}, ratio={m_/k:.4f} >= p/q - g0/(qk) = {p/q - g0/(q*k):.4f}; T^k(n_k)=n0 OK; all n_k distinct; k/ln(n_k) = {k/ (n.bit_length()*math.log(2)):.4f}  (limit 1/(ln2-(p/q)ln{a}) = {1/(math.log(2)-p/q*math.log(a)):.4f})")
