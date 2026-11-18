"""Checks for Theorem B (perturbed-rotation / Benford law along every trajectory).
usage: python check_benford.py  -> ends with 'ALL BENFORD CHECKS PASSED' """
import random, math
from fractions import Fraction
import mpmath as mp
mp.mp.dps=400
lam=mp.log(3)/mp.log(2)
# continued fraction of log2(3)
def cf(x,n):
    out=[]; 
    for _ in range(n):
        a=int(mp.floor(x)); out.append(a); x=1/(x-a)
    return out
A=cf(lam,120)
print("cf log2 3:",A[:30])
p=[A[0],A[0]*A[1]+1]; q=[1,A[1]]
for i in range(2,120): p.append(A[i]*p[-1]+p[-2]); q.append(A[i]*q[-1]+q[-2])
print("q:",q[:20])
for i in range(1,100): assert abs(lam-mp.mpf(p[i])/q[i])<mp.mpf(1)/(q[i]*q[i+1])
def S(N):
    m=max(i for i in range(len(q)) if q[i]<=N); return sum(A[1:m+2])
for N in (10**3,10**4,10**5,10**6,10**9,10**12,10**20,10**30): print("S(%g)=%d"%(N,S(N)))
lamf=float(lam)
# --- Lemma R brute force: counts of {alpha+j*lam}, j<q_i in arcs deviate by <=2; E(M)<=2*sum of Ostrowski digits
def arcdisc_count(ts):
    ts=sorted(ts); N=len(ts)
    gp=max((j+1)-N*t for j,t in enumerate(ts)); gm=min(j-N*t for j,t in enumerate(ts))
    return gp-gm            # sup over arcs of |count - N*len|
random.seed(7)
for i in range(1,12):
    for _ in range(20):
        al=random.random(); d=arcdisc_count([(al+j*lamf)%1 for j in range(q[i])])
        assert d<=2+1e-9,(q[i],d)
for _ in range(300):
    M=random.randint(1,20000); al=random.random()
    r=M; dig=0
    for i in range(len(q)-1,-1,-1):
        if q[i]<=r and (i>0 or True):
            if i==0 and q[1]==1: continue
            dig+=r//q[i]; r%=q[i]
    assert r==0
    d=arcdisc_count([(al+j*lamf)%1 for j in range(M)])
    assert d<=2*dig+1e-9 and dig<=S(M),(M,d,dig)
print("Lemma R and Ostrowski bound: ok")
# --- trajectories
def frac_log2(o):
    L=o.bit_length()-1
    if L>200: m=o>>(L-200); return float(mp.log(mp.mpf(m)/mp.mpf(2)**200,2))
    return float(mp.log(mp.mpf(o)/mp.mpf(2)**L,2))
def run(n,mul=3,add=1,maxodd=10**7,label=""):
    """odd terms of the trajectory until a repeat of a small term / reaching the cycle; checks exact identity."""
    x=n; odds=[]; seen=set()
    while len(odds)<maxodd:
        if x<10**6:
            if x in seen: break
            seen.add(x)
        if x&1: odds.append(x); x=(mul*x+add)//2
        else: x//=2
    N=len(odds)
    if N<2: return None
    # exact identity: log2 o_i = log2 o_0 + i*log2(mul) - D_i + eta_i
    eta=[0.0]; 
    for o in odds[:-1]:
        eta.append(eta[-1]+float(mp.log(1+mp.mpf(add)/(mul*o),2)))
    lm=float(mp.log(mul,2))
    t0=frac_log2(odds[0])
    if mul==3 and add==1:
        for i in random.sample(range(N),min(N,40)):
            ti=frac_log2(odds[i]); pred=(t0+((i*lam)%1)+eta[i])%1
            dd=abs(ti-float(pred)); dd=min(dd,1-dd); assert dd<1e-9,(i,dd)
    ts=[frac_log2(o) for o in odds]
    D=arcdisc_count(ts)/N
    V=abs(eta[-1])
    out=dict(label=label,N=N,D=D,V=V)
    if mul==3 and add==1:
        s=S(N)
        best=min(dl+(math.floor(V/dl)+1)*2*s/N for dl in [10**(-k/20) for k in range(0,120)])
        velem=(1+0.5*math.log(2*N-1))/(3*math.log(2))
        assert V<=velem+1e-12 and V<=math.log2(7.62)
        assert D<=best+1e-12
        out.update(bound=best,S=s,Velem=velem)
    return out
random.seed(11)
rows=[]
for bits in (200,1000,5000,20000,60000):
    n=random.getrandbits(bits)|(1<<bits)|1; rows.append(run(n,label="random %d-bit"%bits))
for e in (500,5000,30000): rows.append(run(2**e-1,label="2^%d-1"%e))
rows.append(run(27,label="27")); rows.append(run(837799,label="837799"))
rows.append(run(2**60000+2**30001-1,label="2^60000+2^30001-1"))
for r in rows:
    if r: print({k:(round(v,5) if isinstance(v,float) else v) for k,v in r.items()})
# controls (no assertion on bounds: shows the law is map-blind)
for (mul,add,n,lab) in [(3,-1,random.getrandbits(20000)|(1<<20000)|1,"3n-1 random 20000-bit"),(5,1,7,"5n+1 from 7, 30000 odd steps")]:
    r=run(n,mul,add,maxodd=30000,label=lab); print({k:(round(v,5) if isinstance(v,float) else v) for k,v in r.items()})
print("ALL BENFORD CHECKS PASSED")
