# Exact-arithmetic tests of every lemma in REPORT.md, plus the computed recursion.
import math, random, sys
from fractions import Fraction as Fr
from math import comb
random.seed(1)
theta = math.log(2)/math.log(3); lam = theta/(1-theta)
eta = -(theta*math.log2(theta)+(1-theta)*math.log2(1-theta))
print("theta",theta,"lambda",lam,"eta",eta, "2^eta",2**eta,"3^eta",3**eta)
def T(x,s=1): return x//2 if x%2==0 else (3*x+s)//2
def win(x,j,s=1):
    a=0
    for _ in range(j):
        a+=x&1; x=T(x,s)
    return a,x
# L1 (Terras count): any 2^j consecutive integers contain exactly C(j,a) with a odd steps in first j
for s in (1,-1):
    for j in range(0,15):
        for start in (2**j, 1, 12345, 2**j+7):
            if s==-1 and start<1: continue
            cnt=[0]*(j+1); vecs=set()
            for x in range(start,start+2**j):
                y=x;v=0
                for i in range(j): v|=(y&1)<<i; y=T(y,s)
                vecs.add(v); cnt[bin(v).count('1')]+=1
            assert len(vecs)==2**j and cnt==[comb(j,a) for a in range(j+1)],(s,j,start)
print("L1 Terras bijection/counts OK (j<=14, both maps)")
# L2: T^j(x) <= 3^a x/2^j + (3/2)^a - 1 (3x+1);  T^j(x) <= 3^a x/2^j (3x-1); and x<2^(j+1) => T^j(x) < 3^(a+1)
for trial in range(40000):
    j=random.randint(0,120); x=random.randint(1,2**random.randint(1,140))
    a,y=win(x,j,1)
    assert Fr(3**a*x,2**j) <= y <= Fr(3**a*x,2**j)+Fr(3**a,2**a)-1
    if x<2**(j+1): assert y<3**(a+1)
    a,y=win(x,j,-1)
    assert y<=Fr(3**a*x,2**j)
    if x<2**(j+1): assert y<3**(a+1)
for j in range(0,13):          # exhaustive on blocks
    for x in range(2**j,2**(j+1)):
        a,y=win(x,j,1); assert y<3**(a+1) and y<=Fr(3**a*x,2**j)+Fr(3**a,2**a)-1
print("L2 affine bound OK")
# L3 Chernoff: sum_{a>=t} C(j,a) <= 2^(eta j) lam^(theta j - t), all integer t, j<=700
worst=-1e9
for j in range(0,701):
    tail=0
    for t in range(j,-1,-1):
        tail+=comb(j,t)
        d=math.log2(tail)-(eta*j+(theta*j-t)*math.log2(lam))
        worst=max(worst,d); assert d<1e-9,(j,t,d)
print("L3 Chernoff OK, max log2(LHS/RHS) =",worst)
# identity (1+lam) lam^-theta = 2^eta and 3^theta=2
assert abs((1+lam)*lam**(-theta)-2**eta)<1e-12 and abs(3**theta-2)<1e-12
# Computed recursion: F[L] >= N(2^L) for every distinct stretch.
LMAX=int(sys.argv[1]) if len(sys.argv)>1 else 1500
F=[0]; G=[]
pow3=[3**a for a in range(LMAX+2)]
for L in range(1,LMAX+1):
    j=L-1; g=0
    for a in range(j+1):
        c=comb(j,a)
        M=2*pow3[a]+(-((-pow3[a])>>a))      # x_{k+j} < M  (ceil of (3/2)^a)
        i=(M-1).bit_length()                 # x_{k+j} <= M-1 < 2^i
        g+= min(c,F[i]) if i<=j else c
    G.append(min(g,2**j))
    F.append(min(2**L-1,(L-1)+sum(G)))
sup=max(math.log2(F[L])-eta*L for L in range(1,LMAX+1))
argsup=max(range(1,LMAX+1),key=lambda L: math.log2(F[L])-eta*L)
print("recursion: sup_L F_L/2^(eta L) =",2**sup,"at L=",argsup,"; at L=LMAX:",2**(math.log2(F[LMAX])-eta*LMAX))
S=sum(Fr(F[i],2**i) for i in range(1,LMAX+1))
print("sum_{i<=LMAX} F_i/2^i =",float(S))
# analytic constants
for (A,u) in ((9.3,3.2),(9.5,3.2),(10,3.2)):
    Sx=lam**u + A*6**eta*3**eta/(3**eta-1)*3**(-eta*u)
    lhs=Sx/(2**eta-1)+2/2**(3*eta)
    print("A",A,"u",u,"step needs",lhs,"<= A:",lhs<=A)
A=9.5
tail=A*2**(-(1-eta)*(LMAX+1))/(1-2**(-(1-eta)))
print("tail of sum beyond LMAX <=",tail," => C <=",float(S)+tail)
# purely analytic C: sum_i min(1, A 2^{-(1-eta) i})
print("analytic C <=",sum(min(1.0,A*2**(-(1-eta)*i)) for i in range(1,20000)))
# L4: class-injection inequality and final bounds on real stretches
def stretch(n,s=1):
    seen=set(); xs=[]; x=n
    while x not in seen: seen.add(x); xs.append(x); x=T(x,s)
    return xs
def test_stretch(xs,s):
    K=len(xs)
    for cut in (K, max(1,K//2), max(1,K-3)):
        ys=xs[:cut]; Kc=len(ys); srt=sorted(ys)
        import bisect
        cls={}
        for k,x in enumerate(ys):
            j=x.bit_length()-1
            if k+j<Kc:
                a=sum(v&1 for v in ys[k:k+j]); cls[(j,a)]=cls.get((j,a),0)+1
                assert ys[k+j]<3**(a+1)
        for (j,a),c in cls.items():
            assert c<=comb(j,a) and c<=bisect.bisect_left(srt,3**(a+1))
        for L in range(0,min(LMAX,srt[-1].bit_length())+1):
            assert bisect.bisect_left(srt,2**L)<=F[L]
        assert sum(Fr(1,x) for x in ys) <= 28
for n in list(range(1,20001))+[random.randint(1,2**60) for _ in range(3000)]+[2**200-1,27,2**64+1]:
    test_stretch(stretch(n,1),1)
for n in list(range(1,5001))+[random.randint(1,2**40) for _ in range(500)]:
    test_stretch(stretch(n,-1),-1)
print("L4 injection inequality + N(2^L)<=F_L on real stretches (incl. truncated) OK")
