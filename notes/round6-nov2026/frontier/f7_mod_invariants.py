"""Modular invariants of the two-rule system  alpha(w)=(9w+1)/8,  beta(w)=27w/16  on Z/m, gcd(m,6)=1.
Both are bijections of Z/m; a union of residue classes is forward-invariant under both partial maps (ignoring
the 2-adic gates, which are independent of w mod m by CRT) iff it is a union of orbits of the group <alpha,beta>.
Claim: for prime p>3 the group is transitive unless p=11, where the orbits are {-1} and its complement.
Exact integer arithmetic."""
from math import gcd
def orbits(m):
    i8=pow(8,-1,m); i16=pow(16,-1,m)
    al=lambda w:(9*w+1)*i8%m; be=lambda w:27*w*i16%m
    seen=[-1]*m; n=0
    for s in range(m):
        if seen[s]>=0: continue
        st=[s]; seen[s]=n
        while st:
            w=st.pop()
            for f in (al,be):
                v=f(w)
                if seen[v]<0: seen[v]=n; st.append(v)
        n+=1
    return n,seen
bad=[]
for m in range(5,2000):
    if gcd(m,6)!=1: continue
    n,seen=orbits(m)
    if n>1: bad.append((m,n))
print("moduli m<2000 coprime to 6 with more than one orbit:",bad[:40],"... count",len(bad))
assert all(m%11==0 for m,_ in bad)
n,seen=orbits(11); print("m=11: orbits",n,"class of -1 alone:",seen.count(seen[10])==1)
for m in (121,1331,55,77):
    n,seen=orbits(m); sizes=sorted(seen.count(c) for c in range(n)); print("m=%d orbit sizes"%m,sizes)
