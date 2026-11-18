"""Exact checks of the F-map lemmas (REPORT section B).  F(x) = T^L(x), L = floor(log2 x).
usage: python check_F.py   -> prints 'ALL F CHECKS PASSED' """
import random
from fractions import Fraction
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def Fdata(x):
    L=x.bit_length()-1; y=x; a=0; c=0  # 2^k y = 3^a x + c
    v=[]
    for k in range(L):
        if y&1: c=3*c+(1<<k); a+=1; v.append(1); y=(3*y+1)//2
        else: v.append(0); y//=2
    assert (y<<L)==3**a*x+c
    return L,a,c,y,v
def check(x):
    L,a,c,y,v=Fdata(x)
    r=x-(1<<L)
    z=r
    for _ in range(L): z=T(z)            # T(0)=0
    assert y==3**a+z                                   # F1: F(x)=3^a+T^L(x-2^L)
    assert 3**a<=y and Fraction(y)<2*3**a+Fraction(3,2)**a-1+ (1 if a==0 else 0)   # F2
    assert Fraction(c,1<<L)<=Fraction(3,2)**a-1        # c_v/2^L <= (3/2)^a-1
    if a>0:
        g=(c*pow(pow(2,L,3**a),-1,3**a))%3**a          # gamma_v = c_v 2^-L mod 3^a
        assert y%3**a==g and y in (3**a+g,2*3**a+g)    # F3
        if y==2*3**a+g: assert Fraction(g)<Fraction(3,2)**a
    # level law
    Lp=y.bit_length()-1; fl=(3**a).bit_length()-1
    assert Lp-fl in (0,1,2)
    # bad  <=>  a >= amin(L) (least a with 3^a >= 2^L), up to the explicit exceptional window
    bad = y>=x; amin=0
    while 3**amin<(1<<L): amin+=1
    if a>=amin: assert bad
    else:
        if bad: return 1     # exceptional: 3^a<2^L but F(x)>=x
    return 0
exc=0
for x in range(2,1<<17): exc+=check(x)
print("exhaustive x<2^17 ok; exceptional bad with 3^a<2^L:",exc)
random.seed(1)
for _ in range(3000):
    b=random.randint(18,400); x=random.getrandbits(b)|(1<<b); check(x)
for n in range(2,300):
    check(2**n-1); check(2**n+1); check((2**n-1)//3 if n%2==0 else 2**n-3)
# fixed points / cycles of F for T and control maps on x<2^16
def Fgen(x,step):
    L=x.bit_length()-1
    for _ in range(L): x=step(x)
    return x
def Sa(a):
    return lambda n: T(n)-(1<<a) if (n+1)%(1<<(a+1))==0 else T(n)
fp=[x for x in range(1,1<<16) if Fgen(x,T)==x]; print("F fixed points for T below 2^16:",fp); assert fp==[1]
m31=lambda n: n//2 if n%2==0 else (3*n-1)//2
print("F fixed points for 3n-1 below 2^16:",[x for x in range(1,1<<16) if Fgen(x,m31)==x])
for a in range(0,8):
    s=Sa(a); print(" S_%d F-fixed points below 2^12:"%a,[x for x in range(1,1<<12) if Fgen(x,s)==x])
print("ALL F CHECKS PASSED")
