"""n4_short.py -- how large are SHORT incomplete sums  S = sum_{i in I} e(a 3^i/2^j), |I|=R=2^(j/rho)?
Prints max over all windows of one period and a in {1,5}, in units of sqrt(R) and of 2^(j/2).
(Is the completion bound 2^(j/2) sharp for 1<rho<2, or is sqrt(R) the truth?)"""
import numpy as np, math
for j in (16,20,24):
    tau=1<<(j-2); m=1<<j
    x=np.empty(tau,dtype=np.int64); v=1
    for i in range(tau): x[i]=v; v=v*3%m
    for rho in (1.1,1.27,1.5,1.74,2.0,2.5,3.0,4.0):
        R=int(round(2**(j/rho))); 
        if R>=tau or R<4: continue
        best=0
        for a in (1,5):
            z=np.exp(2j*np.pi*((a*x)%m)/m); p=np.concatenate([[0],np.cumsum(z),np.cumsum(z)[:R]+0])
            w=np.abs(p[R:R+tau]-p[:tau]); best=max(best,w.max())
        print("j=%d rho=%.2f R=%7d : max window sum = %9.1f = %5.2f sqrt(R) = %5.3f 2^(j/2) ; sqrt(R ln tau)=%.1f"%(j,rho,R,best,best/math.sqrt(R),best/2**(j/2),math.sqrt(R*math.log(tau))))
