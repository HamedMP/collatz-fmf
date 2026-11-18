"""(1) Two-block weighted lemma: for block word y = c d^k c^j d..., weights lc=1, ld=rho, the four candidate
    repetitions A,B,C,D always contain one with ratio <= 3 (exact rational grid + random), sup of the min.
(2) Weighted early-repetition constant iota(phi) for primitive morphisms on 2 and 3 letters:
    iota = inf over repetitions (u at i<i') of l(w[0,i')) / l(u),  l = left Perron eigenvector (floats: exploration).
"""
import random, itertools, sys
from fractions import Fraction as F
import numpy as np
def minratio(k,j,rho):
    c=[1+k*rho]
    if k>=2: c.append((1/rho+1)/(k-1))
    c.append((1+j)/rho+k)
    if j>=2: c.append((2+k*rho)/(j-1))
    return min(c)
worst=F(0); arg=None
for k in range(1,40):
    for j in range(1,60):
        for num in range(1,400):
            for den in (1,2,3,5,7,16,40):
                rho=F(num,den)
                m=minratio(k,j,rho)
                if m>worst: worst=m; arg=(k,j,rho)
print("lemma grid: max over (k,j,rho) of min candidate ratio = %.5f at"%float(worst),arg,"(claim <= 1+sqrt3=2.73205 <= 3)")
assert worst<=3
def fixed(phi,N,start=0):
    w=[start]
    while len(w)<N:
        nw=[]
        for x in w:
            nw.extend(phi[x])
            if len(nw)>=N: break
        if len(nw)<=len(w) and len(nw)<N: return None
        w=nw
    return w[:N]
def iota(phi,K,N=600,Ls=None):
    M=np.zeros((K,K))
    for x in range(K):
        for y in phi[x]: M[y,x]+=1
    if not (np.linalg.matrix_power(M,K*K)>0).all(): return None
    ev,V=np.linalg.eig(M.T); i=np.argmax(ev.real); l=np.abs(V[:,i].real); l=l/l.min()
    w=fixed(phi,N)
    if w is None: return None
    pref=np.concatenate([[0],np.cumsum(l[w])])
    best=1e18; arg=None
    s=bytes(w)
    for L in (Ls or range(1,min(120,N//6))):
        seen=set()
        for i in range(0,N-L+1):
            u=s[i:i+L]
            if u in seen:
                r=pref[i]/(pref[i+L]-pref[i])
                if r<best: best=r; arg=(L,i)
                if pref[i]>best*(pref[i+L]-pref[i])*3: break
            else: seen.add(u)
    return best,arg,l
if __name__=="__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
    K=int(sys.argv[2]) if len(sys.argv)>2 else 3
    ntr=int(sys.argv[3]) if len(sys.argv)>3 else 4000
    maxlen=int(sys.argv[4]) if len(sys.argv)>4 else 6
    top=[]
    for t in range(ntr):
        phi=[]
        for x in range(K):
            L=random.randrange(1,maxlen+1)
            img=[random.randrange(K) for _ in range(L)]
            if x==0:
                img[0]=0
                if L==1: img.append(random.randrange(K))
            phi.append(img)
        r=iota(phi,K,N=400,Ls=range(1,40))
        if r is None: continue
        top.append((r[0],phi))
    top.sort(key=lambda t:-t[0])
    print("K=%d: %d primitive morphisms sampled; top iota (N=400 screening):"%(K,len(top)))
    for v,phi in top[:8]:
        r=iota(phi,K,N=3000,Ls=list(range(1,60))+list(range(60,400,7)))
        print("  screen %.3f  refined(N=3000) %.4f at (L,i')=%s  phi=%s  l=%s"%(v,r[0],r[1],[''.join(map(str,p)) for p in phi],np.round(r[2],3)))
