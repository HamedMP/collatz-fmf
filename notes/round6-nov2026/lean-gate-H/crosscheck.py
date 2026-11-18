"""Cross-check of the Lean statements (integer forms) in exact arithmetic."""
from fractions import Fraction as F
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def it(L,x):
    a=0
    for _ in range(L): a+=x%2; x=T(x)
    return a,x
def log2(n): return n.bit_length()-1 if n>0 else 0
def good(s,x):
    L=log2(x); a,_=it(L,x); return 3**a*(2**a+1)*2**s <= 2**(L+a)
# guards used in Lean
assert it(4,27)==(3,47) and 2**4*47==27*27+23
a,y=it(6,97); assert (a,2**6*y-3**a*97)==(4,143)
assert good(3,16) and not good(3,27)
n1=n2=0
for L in range(0,13):
    for x in range(0,3*2**L):
        a,y=it(L,x); r=2**L*y-3**a*x
        assert r>=0 and r*2**a+2**L*2**a<=3**a*2**L; n1+=1
        for s in range(0,5):
            if x>=2**L and 3**a*(2**a+1)*2**s<=2**(L+a):
                assert 2**s*y<=x; n2+=1
print("lemma1 instances",n1,"lemma2 instances",n2)
# Terras generating function and bad mass
for L in range(0,15):
    cnt={}
    for n in range(2**L,2**(L+1)):
        a,_=it(L,n); cnt[a]=cnt.get(a,0)+1
    from math import comb
    assert all(cnt.get(a,0)==comb(L,a) for a in range(L+1))
for s in (2,3,4):
    tot=F(0); w=F(0)
    for n in range(1,2**16):
        if not good(s,n):
            L=log2(n); a,_=it(L,n)
            wt=F(2**(s+1))*F(7,4)**a/F(14,5)**L
            assert F(1,n)<=wt; tot+=F(1,n)
    assert tot<=56*2**(s+1); print("s",s,"bad mass below 2^16:",float(tot),"bound",56*2**(s+1))
# lemma3 + theorem H on stretches
mx=F(0)
for n in range(1,3000):
    xs=[n]
    while True:
        y=T(xs[-1])
        if y in xs: break
        xs.append(y)
    K=len(xs); s=3
    for t in range(K):
        A=[k for k in range(K) if good(s,xs[k]) and k+log2(xs[k])==t]
        assert sum(F(1,xs[k]) for k in A) <= F(2,2**s*xs[t])
    W=sum(F(1,v) for v in xs); mx=max(mx,W); assert W<=1196
print("max harmonic sum",float(mx))
