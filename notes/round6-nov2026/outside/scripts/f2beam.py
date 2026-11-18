"""Beam search over term-by-term extensions F -> x^N + F (every F with F(0)=1 arises this way).
Keeps the B best polynomials (by t) per degree.  Exploration; every reported t is an exact value
for the printed polynomial (exponent list), hence a valid lower bound on tau(n).
usage: f2beam.py Nmax B"""
import sys, math
from f2lib import t
Nmax, B = int(sys.argv[1]), int(sys.argv[2])
beam = {0: [(0, 1)]}
for n in range(0, Nmax):
    if n not in beam: continue
    cands = sorted(set(beam[n]), reverse=True)[:B]
    beam[n] = cands
    for tv, F in cands:
        for N in range(n + 1, Nmax + 1):
            G = F | (1 << N)
            beam.setdefault(N, []).append((t(G), G))
    if n and (n & (n - 1) == 0 or n % 16 == 0 or n < 40):
        tv, F = cands[0]
        ex = [i for i in range(n, -1, -1) if F >> i & 1]
        print(f"n={n} t={tv} t/n={tv/n:.3f} t/(n log2 n)={tv/(n*math.log2(n)) if n>1 else 0:.3f} w={len(ex)} exps={ex if len(ex) < 30 else str(ex[:30])+'...'}", flush=True)
