"""Frostman / digit-reversal projection test.
E_{Q'} = E mod 2^{Q'} (as integers in [0,2^{Q'})). For m <= Q', bucket by top m bits sigma = c >> (Q'-m).
Report: #occupied buckets, max bucket, mean = |E_Q'|/2^m, bucket sigma=0, and L2 (correlation) exponent.
Hull fullness (Thm 2) predicts all 2^m buckets occupied once Q' is large enough for fixed m."""
import sys, math
from collections import Counter
from a1_core import leaves
name = sys.argv[1]; Qp = int(sys.argv[2])
s = -math.log2(0.8191725133961643)
E = sorted(set(r % (1 << Qp) for r, q, M, wp, na, nb in leaves(Qp, name)))
n = len(E)
print(f"{name} Q'={Qp} |E mod 2^Q'|={n} = 2^{math.log2(n):.3f}  (s Q' = {s*Qp:.3f})")
print(" m  occupied/2^m      mean      max   bucket0  bucketTop  log2(max)/log2(max(mean,1)+)   D2=-log2(sum p^2)/m")
for m in range(2, Qp + 1, 2):
    c = Counter(x >> (Qp - m) for x in E)
    mx = max(c.values()); mean = n / 2**m
    d2 = -math.log2(sum(v * v for v in c.values()) / n**2) / m
    occ = len(c)
    print(f"{m:3d} {occ:9d}/{2**m if m<40 else 0:<12d} {mean:10.3f} {mx:7d} {c.get(0,0):7d} {c.get((1<<m)-1,0):7d}   ratio max/mean={mx/mean:10.3f}   D2={d2:.4f}")
