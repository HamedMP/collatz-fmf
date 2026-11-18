"""n1_disc.py -- star discrepancy of the short orbit {xi*3^i mod 2^k / 2^k : i<R}, vs random points.
usage: python n1_disc.py k   (floats from the top 64 bits: exploration only)
starts: xi=1 (integer powers: degenerate for R<0.63k), xi=3^(5k) (deep in the orbit), xi random odd.
Prints D*_R*sqrt(R) (random points: about 0.6-1.2) and max_{a<=32}|sum e(a x_i)|/sqrt(R)."""
import sys, math, random, numpy as np, gmpy2
from gmpy2 import mpz
k=int(sys.argv[1]); random.seed(k)
MOD=(mpz(1)<<k); MASK=MOD-1; SH=k-62
def orbit(xi,R):
    out=np.empty(R); x=mpz(xi)&MASK
    for i in range(R):
        out[i]=int(x>>SH); x=(x*3)&MASK
    return out/2.0**62
def dstar(x):
    x=np.sort(x); R=len(x); i=np.arange(1,R+1)
    return max(np.max(i/R-x), np.max(x-(i-1)/R))
def four(x):
    if len(x)>2_000_000: x=x[:2_000_000]
    return max(abs(np.exp(2j*np.pi*a*x).sum()) for a in range(1,33))/math.sqrt(len(x))
Rs=sorted(set([math.ceil(math.sqrt(k)), int(k**0.75), k//2, k, 2*k, int(k**1.25), int(k**1.5), k*k]))
starts={'xi=1':1, 'xi=3^(5k)':pow(3,5*k,int(MOD)), 'xi=random':random.getrandbits(k)|1}
print("# k=%d ; columns: R, then for each start D*sqrt(R) [maxFourier/sqrt(R)], last: random points"%k)
Rmax=max(Rs)
orbs={nm:orbit(xi,Rmax) for nm,xi in starts.items()}
rnd=np.random.default_rng(k).random(Rmax)
for R in Rs:
    s="R=%9d (R/k=%8.3f)"%(R,R/k)
    for nm in starts:
        x=orbs[nm][:R]; s+=" | %s: %7.3f [%6.2f]"%(nm,dstar(x)*math.sqrt(R),four(x))
    s+=" | random: %6.3f [%5.2f]"%(dstar(rnd[:R])*math.sqrt(R),four(rnd[:R]))
    print(s,flush=True)
