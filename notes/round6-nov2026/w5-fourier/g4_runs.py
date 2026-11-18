# Bad-run structure (Lemma R).  Node (P,k): m(P,k) = symmetric residue of 11*num*3^(-(P+5)) mod 2^k; bad iff |m| < eps*2^k.
#   usage: g4_runs.py K num [eps=0.001]
# (i) exact check of the mirror at nodes: (X mod 2^k)/2^k + (X' mod 3^p)/3^p - 11num/(2^k 3^p) is an integer,
#     X = 11num*3^-p mod 2^k, X' = 11num*2^-k mod 3^p.
# (ii) longest run of consecutive bad nodes along a block path (steps (4,-6),(5,-7),(6,-8)), and exact check
#      that along every bad->bad step  m(P,k) == 3^dP * m(P+dP,k-dQ)   (needs eps*(2^dQ+3^dP) < 1).
import sys, random
from fractions import Fraction as Fr
K = int(sys.argv[1]); num = eval(sys.argv[2]); eps = Fr(sys.argv[3]) if len(sys.argv) > 3 else Fr(1, 1000)
random.seed(2); badm = 0
for _ in range(300):
    k = random.randint(4, 200); p = random.randint(1, 150)
    X = (11*num*pow(3, -p, 1 << k)) % (1 << k); Y = (11*num*pow(2, -k, 3**p)) % 3**p
    if (Fr(X, 1 << k) + Fr(Y, 3**p) - Fr(11*num, (1 << k)*3**p)).denominator != 1: badm += 1
print("mirror at nodes, failures:", badm)
MK = 1 << K; Pmax = (3*K)//4 + 12
inv = [1]; i3 = pow(3, -1, MK)
for p in range(Pmax + 1): inv.append((inv[-1]*i3) % MK)
def m(P, k):
    M = 1 << k; x = (11*num*inv[P+5]) & (M-1)
    return x - M if x > M >> 1 else x
run = {}; nbad = ntot = 0; viol = 0; best = (0, None)
steps = [(4, 6), (5, 7), (6, 8)]
for k in range(8, K+1):
    for P in range((3*(K-k))//4 + 2):
        ntot += 1
        mm = m(P, k)
        if abs(mm) >= eps*(1 << k): continue
        nbad += 1; r = 1
        for dP, dQ in steps:
            c = run.get((P+dP, k-dQ))
            if c:
                if mm != 3**dP * m(P+dP, k-dQ): viol += 1
                r = max(r, 1 + c)
        run[(P, k)] = r
        if r > best[0]: best = (r, (P, k))
print("K=%d num=%s eps=%s: nodes=%d bad=%d (frac %.5f, 2eps=%.5f) longest bad run=%d at (P,k)=%s; exactness violations=%d"
      % (K, sys.argv[2], eps, ntot, nbad, nbad/ntot, 2*float(eps), best[0], best[1], viol))
