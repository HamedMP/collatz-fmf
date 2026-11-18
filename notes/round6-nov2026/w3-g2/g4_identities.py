# g4_identities.py -- exact checks of the identities used in Theorem W (w3-g2)
import itertools, random
from math import comb
def T(x): return x//2 if x%2==0 else (3*x+1)//2
def yv(v):  # integer in [2^L,2^(L+1)) with parity vector v
    L=len(v); r=0; t=0; p=1
    for j,b in enumerate(v):
        if (t&1)!=b: r|=1<<j; t+=p
        if t&1: t=(3*t+1)//2; p*=3
        else: t//=2
    return r+(1<<L), t, p     # y, tau_v = T^L(y-2^L), 3^a
cnt=0
for L in range(2,15):
    for v in itertools.product((0,1),repeat=L):
        y,tau,p=yv(v); a=sum(v)
        x=y
        for b in v:
            assert (x&1)==b; x=T(x)
        z=x; assert z==p+tau and 0<=tau<p
        if a==0: continue
        # (ii) tau_v = sum_j 3^(j-1) 2^(-alpha_[1,j]) mod 3^a, alpha_1 = L-d_{a-1}, alpha_j = d_{a-j+1}-d_{a-j}
        d=[i for i,b in enumerate(v) if b]
        al=[L-d[-1]]+[d[a-j+1]-d[a-j] for j in range(2,a+1)]
        inv2=pow(2,-1,p); s=0; F=0
        for j in range(1,a+1):
            s+=al[j-1]; F=(F+3**(j-1)*pow(inv2,s,p))%p
        assert F==tau
        # (i) low m bits of z from top m bits of sigma/3^a, sigma = tau*2^-m mod 3^a
        for m in (1,2,3,5,8):
            sig=tau*pow(inv2,m,p)%p; c=(sig<<m)//p
            assert (sig<<m)-c*p==tau
            assert (z-(1-c)*p)%(1<<m)==0
        cnt+=1
print("identities OK on",cnt,"vectors")
# pair-conditioning: |E[chi | pair sums]| = prod |f|, exhaustive small case with pinned sum
import cmath, math
def check_pair(L,a,rho,m):
    p=3**a; inv2=pow(2,-1,p)
    from collections import defaultdict
    grp=defaultdict(list); tot=0
    for v in itertools.product((0,1),repeat=L):
        if sum(v)!=a: continue
        d=[i for i,b in enumerate(v) if b]
        al=[L-d[-1]]+[d[a-j+1]-d[a-j] for j in range(2,a+1)]
        s=m; F=0
        for j in range(1,a+1):
            s+=al[j-1]; F=(F+3**(j-1)*pow(inv2,s,p))%p
        ph=cmath.exp(-2j*math.pi*rho*F/p)
        key=tuple(al[2*j]+al[2*j+1] for j in range(a//2))+tuple(al[2*(a//2):])+(d[0],)
        grp[key].append((al,ph)); tot+=1
    S=0; Maj=0
    for key,lst in grp.items():
        ce=sum(ph for al,ph in lst)/len(lst)
        # predicted product of |f|
        pr=1.0; s=m
        for j in range(a//2):
            b=key[j]; s+=b
            # f = average over alpha_{2j} in 1..b-1 of chi(3^(2j) 2^(-s) (2^alpha+3))
            x=3**(2*j)*pow(inv2,s,p)
            f=sum(cmath.exp(-2j*math.pi*rho*(x*(2**al2+3)%p)/p) for al2 in range(1,b))/(b-1)
            pr*=abs(f)
        assert abs(abs(ce)-pr)<1e-9, (abs(ce),pr)
        S+=ce*len(lst); Maj+=pr*len(lst)
    return abs(S)/tot, Maj/tot, tot
for (L,a,rho,m) in [(12,7,1,0),(13,8,5,3),(14,9,7,2),(16,10,1,4),(16,10,11,1)]:
    print("L,a,rho,m",L,a,rho,m,"|char|=%.4f majorant=%.4f N=%d"%check_pair(L,a,rho,m))
