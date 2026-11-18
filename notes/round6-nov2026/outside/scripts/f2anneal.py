"""Simulated annealing for polynomials F of degree n (F(0)=1) with large t(F,S_3).  Exploration only.
usage: f2anneal.py n iters seed"""
import sys, random, math
from f2lib import t
n, iters, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
random.seed(seed)
top = (1 << n) | 1
F = top | (random.getrandbits(n - 1) << 1)
cur = t(F); best, bestF = cur, F
for it in range(iters):
    T = 2.0 * (1 - it / iters) + 0.05
    G = F ^ (1 << random.randint(1, n - 1))
    if random.random() < 0.3: G ^= (1 << random.randint(1, n - 1))
    v = t(G)
    if v >= cur or random.random() < math.exp((v - cur) / T):
        F, cur = G, v
        if cur > best: best, bestF = cur, F
print(f"n={n} best t={best} t/n={best/n:.3f} t/(n log2 n)={best/(n*math.log2(n)):.3f} t/n^1.5={best/n**1.5:.3f} F={bin(bestF)[2:]}", flush=True)
