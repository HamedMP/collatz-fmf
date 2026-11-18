"""f6_concrete.py -- what the proved chain gives at a concrete Q (floating-point evaluation of the
proved inequality  N(Q,m) <= sum_v J_kappa_v(3^{-P_v}),  J_kappa(lam) = sup_tau #{z in E_kappa: lam z+tau in [0,2^(kappa-m))}).
J is computed exactly for every lam in <3>; the multiplicities C(A+B,A) of P_v are evaluated with lgamma (floats).
Prints rho = bound / N_Q  (rho < 1 is a genuine saving over the trivial bound; heuristic value 2^{-(1-s)m}).
usage: python f6_concrete.py log10Q m k"""
import sys, math
import numpy as np
from math import lgamma
L10=float(sys.argv[1]); m=int(sys.argv[2]); k=int(sys.argv[3])
Q=int(round(10**L10)); K=Q+m; n=K-k
s=0.28776078708402889; lx=-s*math.log(2)   # root of 2^-3s+2^-4s=1 to 17 digits
def Eset(j,memo={}):
    if j in memo: return memo[j]
    if j<4: r=sorted({0,(1<<j)-1})
    else:
        mod=1<<j; r=sorted([((8*z-1)*pow(9,-1,mod))%mod for z in Eset(j-3)]+[(16*z*pow(27,-1,mod))%mod for z in Eset(j-4)])
    memo[j]=r; return r
def Jtab(kap):
    mod=1<<kap; D=1<<(kap-2); E=np.array(Eset(kap),dtype=np.int64); nE=len(E); L=1<<(kap-m)
    out=np.empty(D,dtype=np.int64); lam=1; CH=1<<13
    for st in range(0,D,CH):
        c=min(CH,D-st); lams=np.empty(c,dtype=np.int64)
        for i in range(c): lams[i]=lam; lam=(lam*3)%mod
        V=np.sort((lams[:,None]*E[None,:])%mod,axis=1); Vx=np.concatenate([V,V+mod],axis=1)
        best=np.zeros(c,dtype=np.int64)
        for i in range(nE):
            best=np.maximum(best,(Vx[:,i:i+nE]<(V[:,i]+L)[:,None]).sum(axis=1))
        out[st:st+c]=best
    return out   # out[j] = J(3^j)
NQ_norm=1.3130   # N_Q x^Q for large Q
total=0.0; wsum=0.0
for (lq,lp) in ((3,2),(4,3)):
    for qp in range(n-lq, n):
        if qp<0: continue
        kap=K-qp-lq; D=1<<(kap-2); J=Jtab(kap)
        B=np.arange(0,qp//4+1); B=B[(qp-4*B)%3==0]; A=(qp-4*B)//3
        lg=np.array([lgamma(a+b+1)-lgamma(a+1)-lgamma(b+1) for a,b in zip(A,B)])+qp*lx
        w=np.exp(lg)                      # = M(q',i) x^{q'}
        P=2*A+3*B+lp
        idx=(-P)%D                        # 3^{-P} = 3^{(-P) mod D}
        total+= (w*J[idx]).sum()*math.exp(-lx*(qp-Q))   # x^{Q-q'}
        wsum+=w.sum()
rho=total/NQ_norm
assert abs(wsum/7-0.2898)<2e-3, wsum
print("Q=10^%.1f m=%d k=%d : proved-chain bound N(Q,m)/N_Q <= %.4f   (trivial 1, heuristic %.4f)"%(L10,m,k,rho,2**(-(1-s)*m)))
