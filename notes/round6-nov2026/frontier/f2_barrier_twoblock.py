"""Exact tests of (T-A) the repetition barrier and (T-B) the two-block bound, in the two-rule system
   b: w -> m^3 w/16 (16|w),  a: w -> (m^2 w + d)/8   (default m=3, d=1).
Finite forms tested (all integer arithmetic):
 T-A: if the itinerary of w0>0 starts with P and a factor u occurs in P at letter positions i<i'
      (second occurrence wholly inside P) then 2^(B(u)+B(p)) < (w0+1) * 3^(e(p)), p=P[0,i').
 T-B: if the itinerary of w0>0 starts with the block word  c c  or  c d^k c^j d  (c->X, d->Y) then
      (w0+1)^4 * 3^(9 B(X)) > 2^(16 B(X)).
"""
import itertools, random, sys
from math import log2
def seed(P, m=3, d=1):
    A,C,E=1,0,0
    for ch in P:
        if ch=='a': A,C,E=m*m*A, m*m*C+d*2**E, E+3
        else:       A,C,E=m**3*A, m**3*C, E+4
    return (-C*pow(A,-1,2**E))%(2**E) if E else 0, E
def run(w,P,m=3,d=1):
    out=[w]
    for ch in P:
        if ch=='a':
            assert (m*m*w+d)%8==0; w=(m*m*w+d)//8
        else:
            assert w%16==0; w=m**3*w//16
        out.append(w)
    return out
def Bits(u): return 3*u.count('a')+4*u.count('b')
def E3(u): return 2*u.count('a')+3*u.count('b')
random.seed(7)
# ---- T-A
nchk=0; worst=1e9
for trial in range(3000):
    n=random.randrange(2,26)
    P=''.join(random.choice('ab') if random.random()<0.8 else random.choice(['aa','bb','ab']) for _ in range(n))
    if random.random()<0.3:
        u0=''.join(random.choice('ab') for _ in range(random.randrange(1,6))); P=u0*random.randrange(2,6)+P[:3]
    R,E=seed(P)
    for k in range(0,3):
        w0=R+k*2**E
        if w0<=0: continue
        st=run(w0,P)
        assert all(st[t+1]>st[t] for t in range(len(P)))
        for L in range(1,len(P)):
            seen={}
            for i in range(0,len(P)-L+1):
                u=P[i:i+L]
                if u in seen:
                    i0=seen[u]; p=P[:i]
                    assert (st[i]-st[i0])%2**Bits(u)==0 and st[i]>st[i0]
                    assert 2**(Bits(u)+Bits(p)) < (w0+1)*3**E3(p), (P,u,i0,i,w0)
                    nchk+=1
                else: seen[u]=i
print("T-A: repetition-barrier instances checked:",nchk,"violations: 0")
# ---- T-B
def words(maxlen):
    for L in range(1,maxlen+1):
        for t in itertools.product('ab',repeat=L): yield ''.join(t)
def tb(m,d,maxlen,K,J,verbose=True):
    n=0; minratio=9; arg=None; viol=0
    W=list(words(maxlen))
    for X in W:
        for Y in W:
            pats=['cc']+['c'+'d'*k+'c'*j+'d' for k in range(1,K+1) for j in range(1,J+1)]
            for pat in pats:
                P=pat.replace('c','X').replace('d','Y').replace('X',X).replace('Y',Y)
                R,E=seed(P,m,d)
                w0=R if R>0 else 2**E
                BX=Bits(X); n+=1
                ratio=log2(w0+1)/BX
                if ratio<minratio: minratio=ratio; arg=(X,Y,pat,w0)
                if not (w0+1)**4*3**(9*BX) > 2**(16*BX): viol+=1
    return n,viol,minratio,arg
n,viol,mr,arg=tb(3,1,5,6,6)
print("T-B (3,+1): cases",n,"violations",viol,"min log2(w0+1)/B(X) = %.4f"%mr,"(theorem: > %.4f)"%((16-9*log2(3))/4),arg)
assert viol==0
n,viol,mr,arg=tb(5,1,5,6,6)
print("litmus (5,+1): cases",n,"violations of the m=3 inequality",viol,"min ratio %.4f"%mr,arg)
# 3n-1 litmus: a: w->(9w-1)/8 gate w=1 mod 8 ; w=1 is a positive fixed point with itinerary a^omega
w=1
for _ in range(50):
    assert (9*w-1)%8==0; w=(9*w-1)//8
print("litmus (3,-1): w=1 has itinerary a^50 (fixed point), final state",w,"-> T-B conclusion fails (B(X) unbounded, w0=1)")
n,viol,mr,arg=tb(3,-1,5,6,6)
print("litmus (3,-1): cases",n,"violations",viol,"min ratio %.4f"%mr,arg)
n,viol,mr,arg=tb(3,5,5,6,6)
print("litmus (3,+5): cases",n,"violations of d=1 form",viol,"min ratio %.4f"%mr,arg, "(theorem for +d reads w0+d > ...)")
