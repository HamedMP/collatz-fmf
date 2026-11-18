"""Period Lemma test for F_c = sum_{l=0}^{c} x^{(M+1) l}, M = 2^j, a = M+1,
   on the trajectory set  C = {2^e : 0<=e<=j}  u  {2^e - 2^i : 0<=i<e<=j}  (1 <= c <= M):
   with P = 2^{bitlength(a c)} (row period of the columns <= a c),
     S_3^P(F_c) = F_{c - lowbit(c)}   if c is not a power of two,
     S_3^P(F_c) = F_{c - 2}           if c = 2^e >= 2,
     S_3^P(F_1) = 1,
   and S_3^r(F_c) != 1 for r < P.   (For c outside C the statement is FALSE, e.g. j=4, c=5.)
   Summing the periods along 2^i -> 2^i-2 -> 2^i-4 -> ... gives t(F_{2^i}) = 2^{j+2}((i-1)2^{i-1}+1).
usage: f2period.py jmax          expected: 'violations=0' for every j"""
import sys
from f2lib import s3
for j in range(1, int(sys.argv[1]) + 1):
    M = 2**j; a = M + 1; bad = 0
    Fc = lambda c: sum(1 << (a * l) for l in range(c + 1))
    C = sorted({2**e for e in range(j + 1)} | {2**e - 2**i for e in range(1, j + 1) for i in range(e)})
    for c in C:
        F = Fc(c); P = 1 << (a * c).bit_length(); early = False
        for _ in range(P):
            if F == 1: early = True
            F = s3(F)
        if c == 1: ok = (F == 1) and not early
        elif c & (c - 1) == 0: ok = (F == Fc(c - 2)) and not early
        else: ok = (F == Fc(c - (c & -c))) and not early
        bad += (not ok)
    print(f"j={j} M={M}: |C|={len(C)} violations={bad}", flush=True)
