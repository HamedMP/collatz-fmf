# verify_gap.py -- exact-integer checks of Lemma G (covering) and Theorem G (cluster localisation)
# for qn+1 maps (q=3: c<=4 per odd step; q=5: c<=8).  Usage: python verify_gap.py
import random
from fractions import Fraction
def T(n,q): return n//2 if n%2==0 else (q*n+1)//2
def chain(m,d,q):
    """greedy backward chain: d odd predecessors, each n_i=(2^c n_{i-1}-1)/q with smallest c
    such that n_i is an integer not divisible by q. returns (n, k=sum c, cmax)."""
    n=m;k=0;cmax=0
    for _ in range(d):
        c=1
        while True:
            v=(1<<c)*n-1
            if v%q==0 and (v//q)%q!=0: break
            c+=1
        n=v//q;k+=c;cmax=max(cmax,c)
    return n,k,cmax
random.seed(1)
for q,cb in ((3,4),(5,8)):
    worst=0;tests=0
    for _ in range(4000):
        m=random.choice([random.randrange(1,10**3),random.randrange(1,10**12),2**random.randrange(1,80),2**random.randrange(2,60)-1])
        if m%q==0: continue
        d=random.randrange(0,25)
        n,k0,cmax=chain(m,d,q)
        assert cmax<=cb and k0<=cb*d
        k=k0+random.randrange(0,5); n2=n<<(k-k0)
        # forward check: T^k(n2)=m with exactly d odd steps
        x=n2;odd=0
        for _ in range(k):
            odd+=x&1; x=T(x,q)
        assert x==m and odd==d
        # localisation: 2^k m/q^d - 2^(k-d)... general q: n in (2^k m/q^d - S/q^d, 2^k m/q^d], S/q^d < 2^k * sum_i q^(-1-i) 2^(b_i-k)
        hi=Fraction((1<<k)*m,q**d)
        assert n2<=hi
        if q==3:
            assert n2>hi-(1<<max(k-d,0)) if d>0 else n2==hi
        tests+=1; worst=max(worst,cmax)
    print(f"q={q}: {tests} random (m,d,k) OK; largest single c used = {worst} (bound {cb})")
# Corollary G2 illustration (q=3): relative gap bound from seeds 2^j.
import math
al=math.log2(3)
for D in (5,12,41,53,306,665):
    pts=sorted(((-d*al)%1.0) for d in range(D+1)); g=max([b-a for a,b in zip(pts,pts[1:])]+[pts[0]+1-pts[-1]])
    eps=g; K0=math.ceil(4*D+0.585*D+math.log2(1/eps))+1
    print(f"D={D}: max gap of {{-d log2 3}} = {g:.5f}; for x >= 2^{K0} every [x(1-{eps:.4f}), x*2^{g:.4f}] meets G  (relative length ~ {(2**g-1)+eps:.4f})")
