"""Test the 'block lemma' for Phi = 1/(1+x^a), a = M+1, M = 2^j:
   for all 0 <= q < M and 1 <= c <= M-1: the staircase started at row M q, level a c
   (state ((1+x^M)^q Phi)|<=ac) has level >= a(c-1) at row M(q+1).
   Also records the worst observed drop  a c - level  in units of a.
usage: f2crash.py jmax"""
import sys
from f2lib import s3, pmul
for j in range(2, int(sys.argv[1]) + 1):
    M = 2**j; a = M + 1
    Phi = sum(1 << (a * l) for l in range(M + 1))
    bad = 0; worst = 0; tot = 0
    for q in range(M):
        P = 1
        for b in range(j):
            if q >> b & 1: P = pmul(P, 1 | (1 << (M << b)))   # (1+x^M)^q
        row = pmul(Phi, P)
        for c in range(1, M):
            F = row & ((1 << (a * c + 1)) - 1)
            assert F >> (a * c) & 1
            for _ in range(M):
                if F == 1: break
                F = s3(F)
            lvl = F.bit_length() - 1
            tot += 1
            if lvl < a * (c - 1): bad += 1; worst = max(worst, a * (c - 1) - lvl)
    print(f"j={j} M={M}: pairs tested={tot} violations={bad} worst shortfall below a(c-1) = {worst}", flush=True)
