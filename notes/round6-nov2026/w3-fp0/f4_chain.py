"""f4_chain.py -- hostile end-to-end check of the proof chain of Theorem B on exact data.
For (K=Q+m, k) it enumerates the stopped words v (first prefix with Q_v >= n=K-k), and checks, with exact integers:
 (i)   E_K = disjoint union of  f_v(E_{kappa_v}),  f_v(z) = r_v + 2^{Q_v} * ((z - w'_v) 3^{-P_v} mod 2^kappa)
 (ii)  N(Q,m) = sum_v #{z in E_kappa : (z-w'_v) 3^{-P_v} mod 2^kappa < 2^{kappa-m}}
 (iii) per group (q', last letter): P_v = const - i with multiplicity C(A+B,A), unimodal in i,
       and  sum_{i = w mod D} M_i <= W_{q'}/D + 3 M_max
 (iv)  | N(Q,m) - 2^-m N_K |  <=  sum_v F_kappa(3^{-P_v})  <=  sum_groups (3 D M_max + W_q') * avg_{lam in <3>} F_kappa(lam)
       with F_kappa(lam) := sum_{h != 0} |a_h| |T_kappa(h lam)|  (exact DFT of the interval [0,2^(kappa-m)))
 (v)   avg F_kappa <= (4.47+2.37 kappa) sqrt(N_kappa).
usage: python f4_chain.py K m k [mult d]"""
import sys, math
import numpy as np
K,m,k=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
mult=int(sys.argv[4]) if len(sys.argv)>4 else 3
d=int(sys.argv[5]) if len(sys.argv)>5 else 1
M2,M3=mult**2,mult**3
Q=K-m; n=K-k
def Eset(j,memo={}):
    if j in memo: return memo[j]
    if j<4: r=sorted({0,(-d)%(1<<j)})
    else:
        mod=1<<j; r=sorted([((8*z-d)*pow(M2,-1,mod))%mod for z in Eset(j-3)]+[(16*z*pow(M3,-1,mod))%mod for z in Eset(j-4)])
    memo[j]=r; return r
EK=set(Eset(K)); NK=len(EK)
NQm=sum(1 for c in EK if c<(1<<Q))
# stopped words: (Qv,Pv,Dv, qprime, last) ; f_v(z) = (2^Qv z - Dv)/mult^Pv, forward v(w) = (mult^Pv w + Dv)/2^Qv
words=[]
def gen(Qv,Pv,Dv,A,B):
    if Qv>=n: return
    # append a: new D = M2*D + d*2^Qv ; append b: D = M3*D
    for (dq,dp,let) in ((3,2,'a'),(4,3,'b')):
        D2 = M2*Dv + d*(1<<Qv) if let=='a' else M3*Dv
        if Qv+dq>=n: words.append((Qv+dq,Pv+dp,D2,Qv,let,A,B))
        else: gen(Qv+dq,Pv+dp,D2,A+(let=='a'),B+(let=='b'))
gen(0,0,0,0,0)
tot=0; cover=set(); cnt=0; errsum=0.0
groups={}
Fcache={}
def Fk(kap):
    if kap in Fcache: return Fcache[kap]
    mod=1<<kap; ind=np.zeros(mod); ind[Eset(kap)]=1
    T=np.abs(np.fft.fft(ind))
    L=1<<(kap-m); iv=np.zeros(mod); iv[:L]=1
    a=np.abs(np.fft.fft(iv))/mod
    Dg=1<<(kap-2); h=np.arange(1,mod)
    F=np.empty(Dg); lam=1
    for j in range(Dg):
        F[j]=(a[1:]*T[(h*lam)%mod]).sum(); lam=(lam*mult)%mod
    Fcache[kap]=F; return F
dlog={}
def dl(kap,lam):  # discrete log base mult mod 2^kap
    if kap not in dlog:
        t={}; x=1
        for j in range(1<<(kap-2)): t[x]=j; x=(x*mult)%(1<<kap)
        dlog[kap]=t
    return dlog[kap][lam]
for (Qv,Pv,Dv,qp,let,A,B) in words:
    kap=K-Qv; mod=1<<kap
    rv=(-Dv*pow(mult,-Pv,1<<Qv))%(1<<Qv)
    wp=(mult**Pv*rv+Dv)>>Qv
    assert (mult**Pv*rv+Dv)%(1<<Qv)==0
    lam=pow(mult,-Pv,mod)
    c_here=0
    for z in Eset(kap):
        y=((z-wp)*lam)%mod
        c=rv+(y<<Qv)
        assert c in EK and c not in cover
        cover.add(c)
        if y<(1<<(kap-m)): c_here+=1
        assert (y<(1<<(kap-m)))==(c<(1<<Q))
    cnt+=c_here
    N_kap=len(Eset(kap))
    F=Fk(kap)[dl(kap,lam)]
    assert abs(c_here-N_kap*2.0**-m)<=F+1e-9
    errsum+=F
    groups.setdefault((qp,let,kap),[]).append((A,B,Pv))
assert cover==EK and cnt==NQm
print("K=%d m=%d k=%d (system %dn%+d): #stopped words=%d, N_K=%d, N(Q,m)=%d, 2^-m N_K=%.2f"%(K,m,k,mult,d,len(words),NK,NQm,NK*2.0**-m))
print(" (i),(ii) decomposition and bucket identity: OK")
W=[1,0,0,1]
for q in range(4,K+1): W.append(W[q-3]+W[q-4])
bound=0.0; bound5=0.0
for (qp,let,kap),lst in groups.items():
    # multiplicities by P
    from collections import Counter
    cP=Counter(P for (_,_,P) in lst)
    Ps=sorted(cP); vals=[cP[P] for P in Ps]
    assert Ps==list(range(Ps[0],Ps[-1]+1)) and sum(vals)==W[qp]
    pk=vals.index(max(vals))
    assert all(vals[i]<=vals[i+1] for i in range(pk)) and all(vals[i]>=vals[i+1] for i in range(pk,len(vals)-1)), "unimodal"
    Dg=1<<(kap-2); Mmax=max(vals)
    for w in range(min(Dg,len(Ps))):
        assert sum(vals[w::Dg])<=W[qp]/Dg+3*Mmax
    avgF=Fk(kap).mean()
    Nk=len(Eset(kap))
    assert avgF<=(4.47+2.37*kap)*math.sqrt(Nk)
    bound+=(3*Dg*Mmax+W[qp])*avgF
    bound5+=(3*Dg*Mmax+W[qp])*(4.47+2.37*kap)*math.sqrt(Nk)
print(" (iii) unimodality + AP-sum lemma: OK on %d groups"%len(groups))
print(" (iv)  |N(Q,m)-2^-m N_K| = %.2f  <=  sum_v F = %.2f  <=  group bound = %.2f  <=(v) explicit bound = %.2f"%(abs(NQm-NK*2.0**-m),errsum,bound,bound5))
assert abs(NQm-NK*2.0**-m)<=errsum+1e-6<=bound+1e-6<=bound5+1e-6
print(" chain OK")
