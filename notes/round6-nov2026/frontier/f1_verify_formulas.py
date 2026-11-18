"""Verify: (i) repo return block n'=(P_r n+D_r)/Q_r  <=>  w=33n+32, w=16^r z -> (9*27^r z+1)/8
(ii) single-coordinate two-rule map: b: w->27w/16 (16|w), a: w->(9w+1)/8 (w=7 mod 8)
(iii) Collatz x=108n+103=(36w-19)/11 has T-parity word (1110)^r 110 across the block and lands on 108n'+103.
Exact integers only."""
from fractions import Fraction
def P(r): return 9*27**r
def Q(r): return 2**(4*r+3)
def D(r): return 1 if r==0 else (2592*27**(r-1)-85*16**r)//11
def Tstep(x): return (x//2,0) if x%2==0 else ((3*x+1)//2,1)
cnt=0
for r in range(0,7):
    assert r==0 or (2592*27**(r-1)-85*16**r)%11==0
    q=Q(r)
    # gate residue
    n0=(-D(r)*pow(P(r),-1,q))%q
    for k in range(0,400):
        n=n0+k*q
        n1=(P(r)*n+D(r))//q; assert (P(r)*n+D(r))%q==0
        w=33*n+32
        assert w%(16**r)==0; z=w//16**r; assert z%2==1 and (3**r*z)%8==7
        w1=(9*27**r*z+1)//8; assert (9*27**r*z+1)%8==0 and w1==33*n1+32
        # two-rule
        u=w
        for _ in range(r):
            assert u%16==0; u=27*u//16
        assert u%8==7; u=(9*u+1)//8; assert u==w1
        # Collatz parity
        x=108*n+103; assert 11*x==36*w-19
        word=''
        for _ in range(4*r+3):
            x,b=Tstep(x); word+=str(b)
        assert word=='1110'*r+'110', (r,n,word)
        assert x==108*n1+103
        cnt+=1
# non-gate n: no return block of ANY r is admissible in w-coordinates
import random
random.seed(1)
bad=0
for _ in range(20000):
    n=random.randrange(1,10**12); w=33*n+32
    v=(w&-w).bit_length()-1
    if v%4==0:
        r=v//4; z=w>>v
        if (3**r*z)%8==7:
            assert (P(r)*n+D(r))%Q(r)==0; bad+=1
        else: assert all((P(rr)*n+D(rr))%Q(rr)!=0 for rr in range(0,12))
    else: assert all((P(rr)*n+D(rr))%Q(rr)!=0 for rr in range(0,12))
print("OK blocks checked:",cnt,"random gate-consistency checks: 20000, admissible:",bad)
