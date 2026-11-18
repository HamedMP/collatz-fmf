from fractions import Fraction as F
import math
def G(P,Q,d,k): return k**(P+Q-1)*k**P/((k**P-1)*k**(d+1))
def bestA(P,Q,nu,k):
    best=None
    for d in range(P-1,6*P):
        g=G(P,Q,d,k); q=k**Q
        if q-1-g<=0: continue
        A=(1+nu**d)/(q-1-g)
        if best is None or A<best[0]: best=(A,d)
    return best
# (a)
P,Q=8,5
for nu,k in [(F(16,15),F(8,7))]:
    assert 3**Q<=2**P and 1+nu**P<=k**Q*nu**Q
    A,d=bestA(P,Q,nu,k); print(P,Q,nu,k,float(k**Q),float(A),d)
# (b)
P,Q=65,41
assert 3**Q<=2**P
cands=[]
for m in range(60,400):
  for mm in range(1,6):
    nu=1+F(mm,m)
    if not (1.0079<float(nu)<1.0087): continue
    need=((1+nu**P)/nu**Q)
    kmin=float(need)**(1/Q)
    # find small rational kappa>=kmin
    for den in range(20,700):
        num=math.ceil(kmin*den-1e-15)
        k=F(num,den)
        if 1+nu**P<=k**Q*nu**Q:
            cands.append((float(k**Q),nu,k))
cands.sort(key=lambda t:(t[0]))
seen=set()
for q,nu,k in cands[:400]:
    if (nu,k) in seen: continue
    seen.add((nu,k))
    if len(seen)>12: break
    A,d=bestA(P,Q,nu,k); print(q,nu,k,float(A),d)
