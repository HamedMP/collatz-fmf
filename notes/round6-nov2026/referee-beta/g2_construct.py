# Exact test of the CONSTRUCTION in Corollary G2 (w2-beta T6): for D, eps and x >= 2^(5D+log2(1/eps)+2),
# follow the proof literally (t0, d<=D, K, j, k=K-j, m=2^j, Lemma-G chain), then verify with exact integers:
#   k>=4d, k0<=k, x < n <= x*2^g_D/(1-eps), and T^k(n)=2^j (hence n reaches 1; also iterate to 1 directly).
# Also checks: three-gap claim g_D < 2/q (q = largest convergent denominator <= D), explicit Rhin-type bound.
import random, sys
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.prec=9000
al=mp.log(3)/mp.log(2)
def T(n): return n>>1 if n&1==0 else (3*n+1)>>1
def chain(m,d):
    n=m;k=0
    for _ in range(d):
        r=n%3; assert r
        cs=(2,4) if r==1 else (1,3)
        for c in cs:
            v=(n<<c)-1; assert v%3==0
            if (v//3)%3: break
        else: raise SystemExit("residue claim fails")
        n=v//3; k+=c; assert n&1
    return n,k
def gD(D):
    pts=sorted(mp.frac(-d*al) for d in range(D+1))
    return max([b-a for a,b in zip(pts,pts[1:])]+[pts[0]+1-pts[-1]])
# convergents of log2 3
def convergents(N):
    x=al;h0,h1,k0,k1=0,1,1,0;out=[]
    for _ in range(N):
        a=int(mp.floor(x));h0,h1=h1,a*h1+h0;k0,k1=k1,a*k1+k0;out.append((h1,k1));x=1/(x-a)
    return out
cv=convergents(40); qs=[q for p,q in cv]
print("convergent denominators:",qs[:16])
worst3=0
for D in list(range(1,400))+[665,1000,1500]:
    q=max(q for q in qs if q<=D); g=gD(D); worst3=max(worst3,g*q)
    assert g<mp.mpf(2)/q,(D,q,g)
print("three-gap claim g_D<2/q holds for all tested D; max g_D*q =",mp.nstr(worst3,6))
# explicit all-q bound ||q a|| >= 2^-13.3/ln2 * q^-13.3 on convergents (others are larger)
print("min over convergents (q<1e18) of ||q a||*q^13.3 :",mp.nstr(min(abs(q*al-p)*mp.mpf(q)**13.3 for p,q in cv),6),
      " ; min ||q a||*q :",mp.nstr(min(abs(q*al-p)*q for p,q in cv),6))
random.seed(7); tests=0; minslack=None
for D in (1,2,3,5,12,29,41,53,100,200,306,380):
    g=gD(D)
    for epsden in (2,3,16,1000,10**6):
        eps=Fr(1,epsden)
        L=5*D+mp.log(epsden,2)+2
        e0=int(mp.ceil(L))
        for trial in range(12):
            if trial==0: x=Fr(2)**e0                       # boundary (>= 2^L)
            elif trial==1: x=Fr(int(mp.ceil(mp.mpf(2)**L)))  # smallest integer >= 2^L
            else:
                e=random.choice([e0,e0+1,e0+random.randrange(2,60),2000-random.randrange(0,30)])
                if e<e0: e=e0
                den=random.choice([1,1,7,10**9]); x=Fr((random.getrandbits(e)|(1<<e))*den+random.randrange(den), den)
            t0=mp.log(mp.mpf(x.numerator)/x.denominator/(1-mp.mpf(1)/epsden),2)
            found=False
            for d in range(D+1):
                K=int(mp.ceil(t0+d*al)); u=K-d*al; d=int(d)
                if u<=t0+g:
                    # exact confirmation of 2^K/3^d >= x/(1-eps)
                    if Fr(2**int(K))/Fr(3**int(d))*(1-eps) < x: K+=1
                    if K-d*al>t0+g: continue
                    found=True;break
            assert found,(D,epsden)
            j=int(mp.ceil(d*mp.log(mp.mpf(3)/2,2)+mp.log(epsden,2))); k=K-j; m=1<<j
            assert k>=4*d,(D,d,k)
            nd,k0=chain(m,d); assert k0<=4*d<=k
            n=nd<<(k-k0)
            # exact: Lemma G window and x<n
            assert Fr(2**k*m,3**d)-2**(k-d) < n <= Fr(2**k*m,3**d)
            assert n>x, "n<=x"
            ub=mp.mpf(x.numerator)/x.denominator*mp.mpf(2)**g/(1-mp.mpf(1)/epsden)
            assert mp.mpf(n)<=ub*(1+mp.mpf(2)**-8000)
            y=n;o=0
            for _ in range(k): o+=y&1; y=T(y)
            assert y==m and o==d
            while y!=1: y=T(y)
            tests+=1
    print(f"D={D}: g_D={mp.nstr(g,6)} OK (all eps)")
print("G2 construction: tests",tests,"all inside [x, x*2^g/(1-eps)] and reach 1; x up to ~2^2000")
# 5n+1 analogue of the residue claim: admissible c (2^c n = 1 mod 5), two smallest <= 8, one has 5∤n_i
for n in range(1,2000):
    if n%5==0: continue
    cs=[c for c in range(1,9) if (pow(2,c,5)*n)%5==1]
    assert len(cs)==2 and any((((n<<c)-1)//5)%5 for c in cs)
print("5n+1 residue analogue OK")
