# Step 1: brute force #(E mod 2^k), independent of the report.
import sys
from fractions import Fraction
inv9 = lambda k: pow(9,-1,1<<k)
inv27 = lambda k: pow(27,-1,1<<k)
# (A) forward brute force: residue r mod 2^k is in E mod 2^k iff forward itinerary never dies
# before precision runs out. With j bits left: j==0 ok; need r mod 2^min(j,3) in {7 mod} or r mod 2^min(j,4)==0
def alive(r,j):
    while True:
        if j==0: return True
        if j<=3:
            m=(1<<j)-1
            return (r&m)==(7&m) or (r&m)==0
        if r&7==7:
            r=((9*r+1)>>3)&((1<<(j-3))-1); j-=3
        elif r&15==0:
            r=((27*r)>>4)&((1<<(j-4))-1); j-=4
        else: return False
# careful: for j<=3 residue 7 mod 2^j: a branch; then leftover 0 bits. 0 mod 2^j: b-branch possible (j<4). ok
NA={}
for k in range(0,23):
    NA[k]=sum(alive(r,k) for r in range(1<<k))
# (B) backward: images of inverse branches
S={0:{0}}
def Sk(k):
    if k<=0: return {0}
    if k in S: return S[k]
    M=1<<k
    out=set()
    for z in Sk(k-3): out.add(((8*z-1)*inv9(k))%M)
    for z in Sk(k-4): out.add((16*z*inv27(k))%M)
    S[k]=out; return out
N=[len(Sk(k)) for k in range(41)]
print("fwd",[NA[k] for k in range(23)])
print("bwd",N)
print("agree", all(NA[k]==N[k] for k in range(23)))
print("rec fails at", [k for k in range(4,41) if N[k]!=N[k-3]+N[k-4]])
# cross-check (B) at k<=22 sets equal forward sets
for k in (10,17,22):
    assert Sk(k)=={r for r in range(1<<k) if alive(r,k)}
import math
f=lambda s:2**(-3*s)+2**(-4*s)-1
lo,hi=0,1
for _ in range(100):
    mid=(lo+hi)/2
    if f(mid)>0: lo=mid
    else: hi=mid
print("s",lo, "log2 N40/40", math.log2(N[40])/40, "ratio N40/N39", N[40]/N[39], 2**lo)
print("a(-1)",Fraction(9*-1+1,8),"b(0)",0)
