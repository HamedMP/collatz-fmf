# exact-integer re-evaluation of the "concrete" bound N(Q,m) <= sum_v J_kappa(lambda_v), and litmus
import sys, numpy as np
from math import comb
from fractions import Fraction
N=[1,2,2,2]
for k in range(4,100200): N.append(N[k-3]+N[k-4])
def Erec(j,memo={}):
    if j in memo: return memo[j]
    if j<4: r=sorted({0,(1<<j)-1})
    else:
        mod=1<<j; i9=pow(9,-1,mod); i27=pow(27,-1,mod)
        r=sorted([((8*z-1)*i9)%mod for z in Erec(j-3)]+[(16*z*i27)%mod for z in Erec(j-4)])
    memo[j]=r; return r
Jc={}
def J(kap,m):
    if (kap,m) in Jc: return Jc[(kap,m)]
    mod=1<<kap; L=1<<(kap-m); E=np.array(Erec(kap)); out=[]; lam=1
    for j in range(1<<(kap-2)):
        cnt=np.bincount((E*lam)%mod,minlength=mod); cc=np.concatenate([[0],np.concatenate([cnt,cnt]).cumsum()])
        out.append(int((cc[L:L+mod]-cc[:mod]).max())); lam=lam*3%mod
    Jc[(kap,m)]=out; return out
def bound(Q,m,k):
    K=Q+m; n=K-k; tot=0; chk=0
    for (dq,dp) in ((3,2),(4,3)):
        for qp in range(n-dq,n):
            kap=K-qp-dq; D=1<<(kap-2); Jt=J(kap,m)
            B=qp//4
            while (qp-4*B)%3: B-=1
            A=(qp-4*B)//3; c=comb(A+B,A)
            while True:
                tot+=c*Jt[(-(2*A+3*B+dp))%D]; chk+=c*N[kap]
                if B<3: break
                # C(A+B+1,A+4) from C(A+B,A)
                c=c*(A+B+1); 
                for t in range(3): c=c*(B-t)
                for t in range(1,5): c=c//1 if False else c
                c=c//((A+1)*(A+2)*(A+3)*(A+4)); A+=4; B-=3
                assert True
    assert chk==N[K],"weights"
    return tot
for (Q,m,k) in ((96,1,8),(96,2,10),(96,4,12),(10**4,1,8),(10**5,1,10)):
    b=bound(Q,m,k); print("Q=%d m=%d k=%d: exact bound/N_Q = %.4f"%(Q,m,k,float(Fraction(b,N[Q]))))
