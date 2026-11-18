from mpmath import mp, mpf, log, floor
import math
mp.dps=120
th=log(3)/log(2)
# ---- Eliahou numbers, independent method: enumerate upper (semi)convergents of theta by denominator
def cf(x,n):
    out=[]
    for _ in range(n):
        a=int(floor(x)); out.append(a); x=1/(x-a)
    return out
A=cf(th,60)
def least(X0):
    delta=log(1+mpf(1)/(3*X0))/log(2)
    # convergents
    p0,q0,p1,q1=1,0,A[0],1   # p_{-1}/q_{-1}, p_0/q_0
    best=None
    for i in range(1,60):
        a=A[i]
        # semiconvergents (p0+t p1)/(q0+t q1), t=1..a ; they lie on the side of p0/q0... i odd => above theta
        for t in range(1,a+1):
            p=p0+t*p1; q=q0+t*q1
            e=mpf(p)/q-th
            if e>0 and e<=delta:
                if best is None or q<best[1]: best=(p,q)
            if best and q>best[1]: break
        p0,q0,p1,q1=p1,q1,p0+a*p1,q0+a*q1
        if best and q1>best[1]: break
    return best
for j in (68,71,72,75,76,78):
    L,K=least(mpf(2)**j); print('X0=2^%d'%j,'K',K,'L',L,'L+K',L+K)
L,K=least(mpf(2)**71); eps=L-K*th
X=1/(3*(mpf(2)**(eps/K)-1)); print('threshold log2',mp.nstr(log(X)/log(2),10),'minus log2(2ln2)=',mp.nstr(log(X)/log(2)-log(2*log(2))/log(2),10), '1/(2ln2)=',mp.nstr(1/(2*log(2)),8))
# brute sanity that no smaller K works for X0=2^71 among K up to 3e6 is pointless; instead check all convergent denominators list
print('cf',A[:26])
# ---- Lemma C2 equidistribution error: direct evaluation of (1/K) sum 2^-{l0+i theta} for several K, l0
import numpy as np
thf=float(th)
mp.dps=40
def meanf(K,l0,chunk=5*10**6):
    s=0.0;i=0
    while i<K:
        m=min(chunk,K-i)
        idx=np.arange(i,i+m,dtype=np.float64)
        # high precision frac: use two-part theta
        fr=(l0+idx*thf)%1.0
        s+=np.exp2(-fr).sum(); i+=m
    return s/K
c=1/(2*math.log(2))
for K in (10**6,10**7,10**8):
    worst=max(abs(meanf(K,l0)-c) for l0 in (0.0,0.3,0.77))
    print('K',K,'max |mean-1/(2ln2)|',worst,'K*err',K*worst)
# Ostrowski-type rigorous bound K*D*_K <= 3+sum_{i<=m+1} a_i  with q_m<=K<q_{m+1} (standard, e.g. Kuipers-Niederreiter)
q=[1,0];
for a in A: q=[a*q[0]+q[1],q[0]]+q[1:] if False else [a*q[0]+q[1],q[0]]; 
qs=[];q0,q1=0,1
for a in A: q0,q1=q1,a*q1+q0; qs.append(q1)
qs=[1]+qs  # q_0=1,q_1,...
for K in (10**9,72057431991,10**12,10**15,10**20):
    m=max(i for i,v in enumerate(qs) if v<=K)
    tot=3+sum(A[1:m+2])
    print('K',K,'m',m,'3+sum a_i',tot,'=> D*_K <=',tot/K,'Koksma err <= 0.5*D =',0.5*tot/K)
