"""Hostile tests for Theorem B: random windows of trajectories (incl. the tail near 1, where the
perturbation eta moves most), exhaustive small n, and the base-3 all-terms version.
usage: python check_benford2.py -> 'ALL WINDOW CHECKS PASSED' """
import random, math
import mpmath as mp
mp.mp.dps=120
def cfq(x,n):
    A=[]; 
    for _ in range(n):
        a=int(mp.floor(x)); A.append(a); x=1/(x-a)
    q=[1,A[1]]
    for i in range(2,n): q.append(A[i]*q[-1]+q[-2])
    return A,q
A2,q2=cfq(mp.log(3)/mp.log(2),60); A3,q3=cfq(mp.log(2)/mp.log(3),60)
def S(N,A,q):
    m=max(i for i in range(len(q)) if q[i]<=N); return sum(A[1:m+2])
def arc(ts):
    ts=sorted(ts); N=len(ts)
    return (max((j+1)-N*t for j,t in enumerate(ts))-min(j-N*t for j,t in enumerate(ts)))/N
def bound(N,V,s):
    return min(dl+(math.floor(V/dl)+1)*2*s/N for dl in [10**(-k/40) for k in range(0,240)])
def fl(o,base):
    L=o.bit_length()
    if L>300: return float(mp.frac(mp.log(mp.mpf(o>>(L-300)),base)+(L-300)*mp.log(2,base)))
    return float(mp.frac(mp.log(mp.mpf(o),base)))
def traj(n):
    xs=[n]
    while xs[-1]!=1: x=xs[-1]; xs.append(x//2 if x%2==0 else (3*x+1)//2)
    return xs            # distinct terms n ... 1
def test(xs):
    odds=[x for x in xs if x&1]; N=len(odds)
    if N>=2:
        V=sum(math.log2(1+1/(3*o)) for o in odds[:-1])
        assert V<=math.log2(7.62) and V<=(1+0.5*math.log(2*N-1))/(3*math.log(2))+1e-12
        D=arc([fl(o,2) for o in odds]); assert D<=bound(N,V,S(N,A2,q2))+1e-9,("b2",xs[0],N,D)
    K=len(xs)
    if K>=2:
        V3=sum(math.log(1+1/(3*x),3) for x in xs[:-1] if x&1)
        D=arc([fl(x,3) for x in xs]); assert D<=bound(K,V3,S(K,A3,q3))+1e-9,("b3",xs[0],K,D)
        return D
random.seed(5)
for n in range(2,3000): test(traj(n))
print("exhaustive n<3000 (full trajectories to 1): ok")
worst=0
for bits in (64,256,1024,4096):
    for _ in range(6 if bits<4096 else 2):
        xs=traj(random.getrandbits(bits)|(1<<bits)|1)
        test(xs)
        for _ in range(40):
            i=random.randrange(len(xs)); j=random.randrange(i,len(xs)+1)
            if j-i>=2: test(xs[i:j])
        for w in (5,20,100,400): test(xs[-w:])       # tail near 1
print("random windows ok")
xs=traj(random.getrandbits(20000)|(1<<20000)|1); K=len(xs)
D3=test(xs); print("base 3, all %d terms of a 20000-bit start: D=%.5f, bound=%.5f"%(K,D3,bound(K,0.3,S(K,A3,q3))))
print("ALL WINDOW CHECKS PASSED")
