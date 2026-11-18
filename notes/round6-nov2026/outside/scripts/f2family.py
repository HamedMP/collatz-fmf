"""Verify the closed formula for the family F_{j,i} = sum_{l=0}^{2^i} x^{(2^j+1) l}  (1 <= i <= j):
     t(F_{j,i}, S_3) = 2^{j+2} * ((i-1) 2^{i-1} + 1),
   hence (i = j)  t = (j-1) 2^{2j+1} + 2^{j+2}  at degree n = 2^j (2^j + 1),
   and t_min(f) = 2 t + n for the (palindromic) polynomial f = F.
usage: f2family.py jmax_all jmax_diag"""
import sys, time
from f2lib import t
ja, jd = int(sys.argv[1]), int(sys.argv[2])
ok = True
for j in range(1, ja + 1):
    for i in range(1, j + 1):
        a = 2**j + 1
        F = sum(1 << (a * l) for l in range(2**i + 1))
        v = t(F); pred = 2**(j + 2) * ((i - 1) * 2**(i - 1) + 1)
        ok &= (v == pred)
        if v != pred: print("MISMATCH", j, i, v, pred)
print(f"all (j,i) with 1<=i<=j<={ja}: {'OK' if ok else 'FAIL'}", flush=True)
for j in range(ja + 1, jd + 1):
    a = 2**j + 1; t0 = time.time()
    F = sum(1 << (a * l) for l in range(2**j + 1))
    v = t(F); pred = (j - 1) * 2**(2 * j + 1) + 2**(j + 2); n = a * 2**j
    print(f"j={j} n={n} t={v} predicted={pred} {'OK' if v == pred else 'MISMATCH'} t/(n log2 n)={v/(n*__import__('math').log2(n)):.4f} [{time.time()-t0:.0f}s]", flush=True)
