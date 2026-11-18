"""Exact tests for the general-Collatz statements (T(x)=x/2 or (3x+1)/2; litmus: (m x + d)/2).
 (G1) growth lemma: if x_j >= x_0 for all j<=n then  x_n * 2^n * (3 x0)^k <= 3^k * x0 * (3 x0+1)^k,  k=#odd steps.
 (G2) finite two-block theorem: parity prefix = block word 'cc' or c d^k c^j d (c->X,d->Y), orbit weakly
      non-descending through the prefix, states at the two occurrences distinct, dens(X),dens(Y)<=th, g=th*log2(3)-1<1/3
      ==> |X| * (1 - 3g - 3*th*log2(1+1/(3x0))) < log2(x0).
 (G3) Justin's formula: iterated palindromic closure u_{n+1} = t u_n with t a prefix of u_n when the new letter occurred before.
"""
import itertools, random
from math import log2
from fractions import Fraction as F
def step(x,m=3,d=1): return (x//2,0) if x%2==0 else ((m*x+d)//2,1)
# G1
cnt=0
for x0 in list(range(1,60000))+[2**k-1 for k in range(17,70)]+[random.Random(3).getrandbits(64)|1 for _ in range(2000)]:
    x=x0;k=0
    for n in range(1,400):
        x,b=step(x);k+=b
        if x<x0: break
        assert x*2**n*(3*x0)**k <= 3**k*x0*(3*x0+1)**k, (x0,n)
        cnt+=1
print("G1 growth-lemma instances:",cnt,"violations 0")
# G2
def seedof(P,m=3,d=1):
    A,C,E=1,0,0     # x_E = (A x0 + C)/2^E
    R=0
    # build residue bit by bit
    x0=0
    for n,bit in enumerate(P):
        # choose bit n of x0 so that parity at step n equals bit
        val=(A*x0+C)//2**n if (A*x0+C)%2**n==0 else None
        assert val is not None
        if val%2!=int(bit): x0+=2**n
        if bit=='1': A,C=m*A,m*C+d*2**n
    return x0
def orbit(x0,n,m=3,d=1):
    o=[x0];w=''
    for _ in range(n):
        x,b=step(o[-1],m,d);o.append(x);w+=str(b)
    return o,w
def g2(m,maxlen,K,J,lo,hi):
    lg=log2(m);tested=0;viol=0;worst=None
    W=[''.join(t) for L in range(2,maxlen+1) for t in itertools.product('01',repeat=L)]
    W=[v for v in W if lo<=v.count('1')/len(v)<=hi]
    for X in W:
        for Y in W:
            th=max(X.count('1')/len(X),Y.count('1')/len(Y)); g=th*lg-1
            if not (0<=g<1/3): continue
            for pat in ['cc']+['c'+'d'*k+'c'*j+'d' for k in range(1,K+1) for j in range(1,J+1)]:
                P=''.join(X if ch=='c' else Y for ch in pat)
                x0=seedof(P,m)
                if x0<3: x0+=2**len(P)
                o,w=orbit(x0,len(P),m); assert w==P
                if min(o)<x0: continue
                # candidate choice as in the proof
                lc,ld=len(X),len(Y)
                if pat=='cc': u,i,ip=lc,0,lc
                else:
                    k=pat.index('c',1)-1; j=len(pat)-k-2; rho=ld/lc
                    if k*rho<=2: u,i,ip=lc,0,lc+k*ld
                    elif k>=2: u,i,ip=(k-1)*ld,lc,lc+ld
                    elif j>=2 and rho<=3*j-5: u,i,ip=(j-1)*lc,lc+ld,2*lc+ld
                    else: u,i,ip=ld,lc,(1+j)*lc+ld
                assert P[i:i+u]==P[ip:ip+u] and ip<=3*u and u>=lc
                assert (o[i]-o[ip])%2**u==0
                if o[i]==o[ip]: continue
                tested+=1
                lhs=lc*(1-3*g-3*th*log2(1+1/(m*x0)))
                if not lhs<log2(x0): viol+=1; worst=(X,Y,pat,x0)
    return tested,viol,worst
print("G2 (3x+1):",g2(3,7,4,4,0.60,0.85))
print("G2 litmus (5x+1), density window (0.43,0.574):",g2(5,7,4,4,0.40,0.58))
# G3
def pal_closure(w):
    for i in range(len(w)):
        if w[i:]==w[i:][::-1]: return w+w[:i][::-1]
rnd=random.Random(5); chk=0
for trial in range(300):
    K=rnd.choice([2,3,4]); u=''; seen=set()
    for n in range(14):
        x=str(rnd.randrange(K)); v=pal_closure(u+x)
        if x in seen:
            t=v[:len(v)-len(u)]
            assert v==t+u and len(t)<=len(u) and u.startswith(t) and v.startswith(u); chk+=1
        seen.add(x); u=v
        if len(u)>4000: break
print("G3 episturmian square-prefix instances:",chk,"violations 0")
