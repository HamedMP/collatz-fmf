# Theorem B at parameters satisfying its hypotheses (Q=96): uses referee counter output
import sys, math, numpy as np
from math import comb
sys.setrecursionlimit(10000)
Q=96
N=[1,2,2,2]
for k in range(4,400): N.append(N[k-3]+N[k-4])
W=[1,0,0,1]
for q in range(4,400): W.append(W[q-3]+W[q-4])
inf=0; hist={}
for ln in open(sys.argv[1]):
    a,b=ln.split()
    if a=='inf': inf=int(b)
    else: hist[int(a)]=int(b)
def NQm(m): return inf+sum(v for mm,v in hist.items() if mm>=m)
assert NQm(0)==N[Q]
# compare with author's file
auth={int(l.split()[1]):int(l.split()[2]) for l in open('../w3-fp0/out_3p1_Q96.txt') if not l.startswith('#')}
assert all(NQm(m)==v for m,v in auth.items()); print("referee counter == author's out_3p1_Q96.txt for all",len(auth),"m; N(96,96)=",NQm(96), "first m with N=1:",min(m for m in range(200) if NQm(m)==1))
def Erec(j,memo={}):
    if j in memo: return memo[j]
    if j<4: r=sorted({0,(1<<j)-1})
    else:
        mod=1<<j; i9=pow(9,-1,mod); i27=pow(27,-1,mod)
        r=sorted([((8*z-1)*i9)%mod for z in Erec(j-3)]+[(16*z*i27)%mod for z in Erec(j-4)])
    memo[j]=r; return r
Fc={}
def Ftab(kap,m):
    if (kap,m) in Fc: return Fc[(kap,m)]
    mod=1<<kap; ind=np.zeros(mod); ind[Erec(kap)]=1; TT=np.abs(np.fft.fft(ind))
    iv=np.zeros(mod); iv[:1<<(kap-m)]=1; a=np.abs(np.fft.fft(iv))/mod; a[0]=0
    D=1<<(kap-2); F=np.empty(D); lam=1; h=np.arange(mod)
    for j in range(D): F[j]=(a*TT[(h*lam)%mod]).sum(); lam=lam*3%mod
    Fc[(kap,m)]=F; return F
c1=6.5
for m in range(1,5):
    K=Q+m; lhs=abs(NQm(m)-N[K]/2**m)
    for k in range(max(7,m+3),min(K-84,15)+1):
        n=K-k; assert n>=84
        sumF=0.0; grp=0.0; chk=0
        for (dq,dp) in ((3,2),(4,3)):
            for qp in range(n-dq,n):
                kap=K-qp-dq; D=1<<(kap-2); F=Ftab(kap,m)
                B=qp//4
                while (qp-4*B)%3: B-=1
                A=(qp-4*B)//3; tot=0; mx=0
                while B>=0:
                    M=comb(A+B,A); P=2*A+3*B+dp; sumF+=M*F[(-P)%D]; tot+=M; mx=max(mx,M); A+=4; B-=3
                assert tot==W[qp]; chk+=tot*N[kap]
                grp+=(W[qp]+3*D*mx)*F.mean()
                assert F.mean()<=(4.47+2.37*kap)*math.sqrt(N[kap])
        assert chk==N[K]
        rhs=(1+3*c1*2**(k-2)/math.sqrt(Q+m-k-4))*(4.47+2.37*k)*N[K]/math.sqrt(N[k-3])
        ok = lhs<=sumF<=grp<=rhs
        print("m=%d k=%2d: |N-2^-m N_K|=%.1f <= sumF=%.4g <= group=%.4g <= ThmB RHS=%.4g ; RHS/N_K=%.1f ; sumF/N_K=%.3f  %s"%(m,k,lhs,sumF,grp,rhs,rhs/N[K],sumF/N[K],"OK" if ok else "FAIL"))
# vacuity scan: min over admissible (Q,m,k) of RHS/N_K for Q up to 10^40
s=0.28776078708402889
best={}
for e in (2,3,6,12,20,30,40,60,100):
    Qf=10.0**e; b=1e99
    for k in range(7,400):
        lnN=math.log(1.2)+s*(k-3)*math.log(2)
        r=(1+3*c1*2.0**(k-2)/math.sqrt(Qf-k-3))*(4.47+2.37*k)/math.exp(lnN/2)
        b=min(b,r)
    print("Q=1e%d: min_k RHS/N_K >= %.3g  (bound non-trivial for some m only if < 1)"%(e,b))
