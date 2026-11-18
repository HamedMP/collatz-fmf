"""Checks for section S (divergence series).  usage: python check_series.py -> 'ALL SERIES CHECKS PASSED'"""
import random
from fractions import Fraction as Fr
random.seed(3)
def cyc(word,mul=3,add=1):
    """rational fixed point x of the affine map of a parity word under x->(mul x+add)/2 | x/2"""
    A=Fr(1);B=Fr(0)
    for b in word:
        if b: A,B=A*mul/2,(B*mul+add)/2
        else: A,B=A/2,B/2
    return B/(1-A)
# S3: for periodic words with 3^a>2^p the real sum R equals -x_T(word) and equals the 3n-1 cycle point
for _ in range(300):
    p=random.randint(2,14); w=[random.randint(0,1) for _ in range(p)]
    a=sum(w)
    if 3**a<=2**p or a==0: continue
    # real sum over one period then geometric
    s=Fr(0);A=0
    for j,b in enumerate(w):
        if b: s+=Fr(2**j,3**(A+1)); A+=1
    R=s/(1-Fr(2**p,3**a))
    assert R==-cyc(w) and R==cyc(w,3,-1)
    # S1 on the shifted word, S2: R>=1
    w2=w[1:]+w[:1]; s2=Fr(0);A=0
    for j,b in enumerate(w2):
        if b: s2+=Fr(2**j,3**(A+1)); A+=1
    R2=s2/(1-Fr(2**p,3**a))
    assert R2==(R/2 if w[0]==0 else (3*R-1)/2)
    assert R>=1
assert cyc([1,1,0],3,-1)==5
# S2 on random dense aperiodic words (truncated real series, tail bounded): y_k>=1
for _ in range(50):
    n=4000; w=[1 if random.random()<0.72 else 0 for _ in range(n)]
    for k in (0,7,100):
        y=0.0;A=0
        for j in range(k,k+600):
            if w[j]: y+=2.0**(j-k)/3.0**(A+1); A+=1
        assert y>=1-1e-9, (k,y)
print("ALL SERIES CHECKS PASSED")
