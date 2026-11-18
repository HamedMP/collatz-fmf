"""n3_lemmas.py -- checks of Lemma 5 (incomplete sums of 3^i mod 2^j), Lemma 6 (fibres of E_k),
Proposition F (second moment along a unimodal progression) and the chain of Theorem A'.
usage: python n3_lemmas.py      (last line: ALL CHECKS OK)"""
import math, cmath, numpy as np
from math import comb
S=0.2877607871468
def E_levels(kmax):
    E=[[0],[0,1],[0,3],[0,7]]
    for j in range(4,kmax+1):
        m=1<<j; i9=pow(9,-1,m); i27=pow(27,-1,m)
        E.append(sorted([((8*z-1)*i9)%m for z in E[j-3]]+[(16*z*i27)%m for z in E[j-4]]))
    return E
KMAX=40
E=E_levels(KMAX); N=[len(e) for e in E]
NN=[1,2,2,2]
for j in range(4,6001): NN.append(NN[j-3]+NN[j-4])
assert NN[:KMAX+1]==N and all(len(set(e))==len(e) for e in E)
# definition check of E_k for k<=18: residues r mod 2^k admitting an a/b itinerary consuming >=k bits
def has_itin(r,k):
    # r mod 2^k known; a needs r=7 mod 8 (consumes 3 bits), b needs r=0 mod 16 (4 bits)
    if k<=0: return True
    if k>=3 and r%8==7: 
        if has_itin(((9*r+1)//8)%(1<<(k-3)),k-3): return True
    if k<3 and any(((r+t*(1<<k))%8)==7 for t in range(8)): return True
    if k>=4 and r%16==0:
        if has_itin((27*r//16)%(1<<(k-4)),k-4): return True
    if k<4 and any(((r+t*(1<<k))%16)==0 for t in range(16)): return True
    return False
for k in range(1,17):
    assert sorted(r for r in range(1<<k) if has_itin(r,k))==E[k], k
print("E_k recursion agrees with the itinerary definition for k<=16; N_k recursion ok")
# growth constants
lo=min(NN[j]/2**(S*j) for j in range(0,6001) if j<3000); hi=max(NN[j]/2**(S*j) for j in range(0,3000))
print("N_j/2^(sj) in [%.4f, %.4f] for j<3000 (claimed [1, 1.64])"%(lo,hi)); assert lo>=1-1e-9 and hi<=1.64
assert all(NN[j+3]<=2*NN[j] for j in range(0,3000)) and all(NN[j+1]>=NN[j] for j in range(1,3000))
# ---- Lemma 5
worst=0
for j in range(4,17):
    tau=1<<(j-2); m=1<<j
    for a in (1,5,-1,-5):
        x=np.empty(tau); v=1
        for i in range(tau): x[i]=v; v=v*3%m
        z=np.exp(2j*np.pi*((a*x)%m)/m)
        assert abs(z.sum())<1e-6*tau                       # complete sum vanishes
        Sab=np.abs(np.fft.fft(z)); assert Sab.max()<=2**((j+1)/2)*(1+1e-9)   # twisted complete sums
        p=np.concatenate([[0],np.cumsum(z)])               # prefix sums over one period
        mx=0.0
        for c0 in range(0,len(p),2048):
            mx=max(mx,np.abs(p[c0:c0+2048,None]-p[None,:]).max())
        assert mx<=j*2**((j+1)/2); worst=max(worst,mx/(j*2**((j+1)/2)))
        if a==1: print("Lemma 5: j=%2d max_I|S_I|=%9.2f  2^(j/2)=%8.2f  bound j*2^((j+1)/2)=%9.2f  max|S(a,b)|/2^((j+1)/2)=%.3f"%(j,mx,2**(j/2),j*2**((j+1)/2),Sab.max()/2**((j+1)/2)))
print("Lemma 5 holds for j<=16, a in {1,5,-1,-5} (all odd a reduce to these by shifting i); worst ratio %.3f"%worst)
# ---- Lemma 6
for k in range(4,KMAX+1):
    for n in range(0,k+1):
        from collections import Counter
        c=Counter(z%(1<<n) for z in E[k])
        fib=max(c.values()); pairs=sum(v*v for v in c.values())
        assert fib<=2*N[k-n], (k,n,fib); assert pairs<=2*N[k-n]*N[k]
print("Lemma 6 (fibre of E_k -> Z/2^n at most 2 N_{k-n}) exact for all n<=k<=%d"%KMAX)
# ---- Proposition F and the chain of Theorem A'
def T(kap,xi):
    m=1<<kap
    return sum(cmath.exp(2j*math.pi*((xi*c)%m)/m) for c in E[kap])
def propF_rhs(kap,e,W,Mstar):
    return 2*N[kap]*(W*N[min(e+3,kap)] + Mstar*sum(N[j+e]*j*2**((j+1)/2) for j in range(4,kap-e+1)))
def Mrow(q):   # {P: count} over words with Q=q
    d={}
    for B in range(0,q//4+1):
        if (q-4*B)%3==0:
            A=(q-4*B)//3; d[2*A+3*B]=comb(A+B,A)
    return d
def dpT(K,h):   # |T_K(h)| by Prop. E in floats (K small)
    from functools import lru_cache
    @lru_cache(None)
    def G(P,k):
        if k==0: return 1
        m=1<<k
        if k<4: return 1+cmath.exp(-2j*math.pi*((h*pow(3,-P,m))%m)/m)
        return cmath.exp(-2j*math.pi*((h*pow(3,-(P+2),m))%m)/m)*G(P+2,k-3)+G(P+3,k-4)
    return abs(G(0,K))
cnt=0
for (K,k) in ((120,14),(160,16),(200,18),(240,20)):
    n=K-k
    for h in (1,2,3,4,6,8,12,32,5*64):
        e=(h&-h).bit_length()-1
        tot1=0; tot2=0; tot3=0; wsum=0
        for (ql,pl) in ((3,2),(4,3)):
            for qp in range(n-ql,n):
                kap=K-qp-ql; M=Mrow(qp)
                if not M: continue
                W=sum(M.values()); Ms=max(M.values())
                vals={P:abs(T(kap,h*pow(3,-(P+pl),1<<kap))) for P in M}
                s1=sum(M[P]*vals[P] for P in M); s2=sum(M[P]*vals[P]**2 for P in M)
                rhs=propF_rhs(kap,e,W,Ms)
                assert s2<=rhs*(1+1e-9), (K,k,h,qp,ql,s2,rhs)
                assert s1<=math.sqrt(W*s2)*(1+1e-9)
                tot1+=s1; tot2+=math.sqrt(W*s2); tot3+=math.sqrt(W*rhs); wsum+=W*N[kap]; cnt+=1
        assert wsum==NN[K]
        tk=dpT(K,h)
        assert tk<=tot1*(1+1e-6)
        if h in (1,8): print("chain K=%d k=%d h=%d: |T_K(h)|/N_K=%.3e <= sum_v|T_kap|/N_K=%.3e <= C-S %.3e <= PropF %.3e"%(K,k,h,tk/NN[K],tot1/NN[K],tot2/NN[K],tot3/NN[K]))
print("Proposition F and the Theorem A' chain hold in %d (group,h) cases"%cnt)
print("ALL CHECKS OK")
