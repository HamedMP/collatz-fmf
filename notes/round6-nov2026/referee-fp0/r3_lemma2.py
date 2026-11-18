import math, numpy as np
from math import comb
s=0.28776078708402889; x=2**-s
assert abs(x**3+x**4-1)<1e-15
W=[1,0,0,1]
for q in range(4,3001): W.append(W[q-3]+W[q-4])
U=[W[q]*x**q for q in range(0,400)]
print("min U_60..63 = %.5f, inf U_q q in[60,400) = %.5f, limit %.5f"%(min(U[60:64]),min(U[60:]),1/(3*x**3+4*x**4)))
worstmode=0; worst3=0; worst2=0; worstc=0; viol2=0
Ds=list(range(1,65))+[2**j for j in range(7,12)]+[97,193,300,777]
for q in range(80,3001):
    Ms=[]  # ordered by i: (A0+4i, B0-3i)
    B=q//4
    while (q-4*B)%3: B-=1
    A=(q-4*B)//3
    while B>=0: Ms.append(comb(A+B,A)); A+=4; B-=3
    assert sum(Ms)==W[q]
    # log concave
    assert all(Ms[i]*Ms[i]>=Ms[i-1]*Ms[i+1] for i in range(1,len(Ms)-1))
    mx=max(Ms); worstmode=max(worstmode,mx*math.sqrt(q)/W[q])
    # modal claim M x^q <= 1.8/sqrt q
    assert mx*x**q<=1.8/math.sqrt(q) if q<1000 else True
    f=np.array([m/W[q] for m in Ms]); fm=mx/W[q]
    for D in Ds:
        if D> len(f)+2 and D not in (2048,777): continue
        pad=np.zeros(((len(f)+D-1)//D)*D); pad[:len(f)]=f
        sums=pad.reshape(-1,D).sum(axis=0).max()
        worst3=max(worst3,(sums-1/D)/fm); 
        worstc=max(worstc,(sums-1/D)*math.sqrt(q))
        assert sums<=1/D+3*6.5/math.sqrt(q)
print("max M sqrt(q)/W over 80<=q<=3000: %.4f"%worstmode)
print("max over q,D,residue of (sum - W/D)/maxM = %.4f (claim <=3, proof gives <=2)"%worst3)
print("max (sum-W/D)*sqrt(q)/W = %.4f (claim <= 3*6.5=19.5)"%worstc)
