# referee step 1/2/9: independent E_k, N(Q,m), T_k, Lemma 1 decomposition, Prop E
import sys, math, cmath, itertools
import numpy as np
def life(w, cap=10**6):
    if w==0: return cap
    bits=0
    while True:
        if w%8==7: w=(9*w+1)//8; bits+=3
        elif w%16==0: w=27*w//16; bits+=4
        else:
            for r in (3,2,1,0):
                if w%(1<<r) in (0,(1<<r)-1): return bits+r
def inE(w,K): return life(w)>=K
# (A) recursion
def Erec(j,memo={}):
    if j in memo: return memo[j]
    if j<4: r=sorted({0,(1<<j)-1})
    else:
        mod=1<<j; i9=pow(9,-1,mod); i27=pow(27,-1,mod)
        r=sorted([((8*z-1)*i9)%mod for z in Erec(j-3)]+[(16*z*i27)%mod for z in Erec(j-4)])
    memo[j]=r; return r
# (B) definition brute force: all residues, forward integer test
for k in range(0,23):
    bf=[r for r in range(1<<k) if inE(r,k)]
    assert bf==Erec(k),k
print("E_k recursion == forward brute force for k<=22; N_k:",[len(Erec(k)) for k in range(23)])
# (C) words: f_v(0) for all words with Q_v>=k (2-adic points truncated)
def words_pts(k):
    out=set(); mod=1<<k
    def rec(Qv,Pv,Dv):   # f_v(z)=(2^Q z - D)/3^P ; appending letter l: f_{vl}(z)=f_v(f_l(z))
        if Qv>=k: out.add((-Dv*pow(3,-Pv,mod))%mod); return
        # f_v(f_a(z)) = (2^Q (8z-1)/9 - D)/3^P = (2^(Q+3) z - 2^Q - 9D)/3^(P+2)
        rec(Qv+3,Pv+2,9*Dv+(1<<Qv)); rec(Qv+4,Pv+3,27*Dv)
    rec(0,0,0); return sorted(out)
for k in range(1,23): assert words_pts(k)==Erec(k),k
print("E_k == {f_v(0) mod 2^k} OK k<=22")
N=[1,2,2,2]
for k in range(4,400): N.append(N[k-3]+N[k-4])
assert all(len(Erec(k))==N[k] for k in range(41))
assert all(N[k+1]>=N[k] for k in range(399))
# projection consistency E_{k+1} mod 2^k = E_k
for k in range(0,40): assert sorted({c%(1<<k) for c in Erec(k+1)})==Erec(k)
print("projection E_{k+1}->E_k onto OK; N monotone")
# N(Q,m) brute force: direct over all w<2^Q for Q<=18, vs E enumeration
def NQm_E(Q,m): return sum(1 for c in Erec(Q+m) if c< (1<<Q))
for Q in range(1,19):
    lv=[life(w) for w in range(1<<Q)]
    for m in range(0,Q+1):
        assert sum(1 for L in lv if L>=Q+m)==NQm_E(Q,m),(Q,m)
print("N(Q,m) direct == via E_{Q+m}, Q<=18, m<=Q")
tab={}
for Q in range(1,41):
    row=[]
    for m in range(0,Q+1):
        if Q+m>62: break
        row.append(NQm_E(Q,m))
    tab[Q]=row
    assert all(row[i]>=row[i+1] for i in range(len(row)-1))
print("N(Q,m) monotone in m (Q<=40, Q+m<=62)")
for Q in (24,32,40): print(" Q=%d:"%Q,tab[Q])
print(" N(Q,Q) for Q=1..31:",[tab[Q][Q] for Q in range(1,32)])
# T_k direct
def T(k,xi):
    mod=1<<k
    return sum(cmath.exp(2j*math.pi*((xi*c)%mod)/mod) for c in Erec(k))
s=0.28776078708402889
print("k, |T_k(h)|/N_k for h=1,2,3,5 ; N^-1/2 ; 6.2*k^(-s/4)")
for k in (10,14,18,22,26,30,36,40):
    print(k,["%.4f"%(abs(T(k,h))/N[k]) for h in (1,2,3,5)],"%.4f"%N[k]**-.5,"%.3f"%(6.2*k**(-s/4)))
# Parseval & Lemma 3
for kap in range(3,15):
    mod=1<<kap; ind=np.zeros(mod); ind[Erec(kap)]=1; TT=np.abs(np.fft.fft(ind))
    assert abs((TT**2).sum()-mod*N[kap])<1e-6*mod*N[kap]
    # order of 3
    x=3;o=1
    while x!=1: x=x*3%mod;o+=1
    assert o==1<<(kap-2)
    G=np.array([pow(3,i,mod) for i in range(o)],dtype=np.int64)
    worst=0
    for h in range(1,mod+1):   # includes h=0 mod 2^kap
        e=(h&-h).bit_length()-1
        idx=(h*G)%mod
        fib=np.bincount(idx).max(); assert fib<=2**e,(kap,h,fib)
        lhs=TT[idx].mean(); rhs=2**(1+e/2)*math.sqrt(N[kap])
        assert lhs<=rhs+1e-9,(kap,h); worst=max(worst,lhs/rhs)
    if kap in(8,12,14): print("Lemma3 kap=%d worst lhs/rhs=%.3f"%(kap,worst))
print("Lemma 3 + Parseval + order(3) OK kap<=14, all h incl h=0 mod 2^kap")
# Lemma 4
for kap in range(3,13):
    mod=1<<kap; ind=np.zeros(mod); ind[Erec(kap)]=1; TT=np.abs(np.fft.fft(ind)); E=np.array(Erec(kap))
    G=[pow(3,i,mod) for i in range(1<<(kap-2))]
    for m in range(1,kap+1):
        L=1<<(kap-m); iv=np.zeros(mod); iv[:L]=1; a=np.abs(np.fft.fft(iv))/mod
        hh=np.arange(1,mod); hs=np.minimum(hh,mod-hh)
        assert np.all(a[1:]<=1/(2*hs)+1e-12)
        Fs=[]
        for l in G:
            F=(a[1:]*TT[(hh*l)%mod]).sum(); Fs.append(F)
            v=(E*l)%mod
            # sup over tau of discrepancy
            cnt=np.zeros(mod); np.add.at(cnt,v,1); cc=np.concatenate([cnt,cnt]).cumsum()
            win=cc[L-1:L-1+mod]-np.concatenate([[0],cc[:mod-1]])
            assert np.abs(win-N[kap]/2**m).max()<=F+1e-7,(kap,m,l)
        assert np.mean(Fs)<=(4.47+2.37*kap)*math.sqrt(N[kap])
print("Lemma 4 OK kap<=12 all m, all lam in G, all tau")
# Lemma 1 decomposition, exact, K<=40
def stopped(n):
    out=[]
    def rec(Qv,Pv,Dv):
        for (dq,dp,D2) in ((3,2,9*Dv+(1<<Qv)),(4,3,27*Dv)):
            if Qv+dq>=n: out.append((Qv+dq,Pv+dp,D2,Qv,dq))
            else: rec(Qv+dq,Pv+dp,D2)
    rec(0,0,0); return out
for K in range(8,41):
    EK=Erec(K); EKs=set(EK); TK={h:T(K,h) for h in (1,6,40)} if K<=30 else {}
    for k in range(7,K):
        if K>30 and k not in (7,8,11,K-1,K-5): continue
        n=K-k; cover=[]; cnt={m:0 for m in range(1,k-2)}; Ts={h:0 for h in TK}
        for (Qv,Pv,Dv,qp,dq) in stopped(n):
            kap=K-Qv; assert k-3<=kap<=k and qp<n<=Qv
            f0=(-Dv*pow(3,-Pv,1<<K))%(1<<K); rv=f0%(1<<Qv); tau=f0>>Qv; lam=pow(3,-Pv,1<<kap)
            ys=[(lam*z+tau)%(1<<kap) for z in Erec(kap)]
            cover+= [rv+(y<<Qv) for y in ys]
            for m in cnt: cnt[m]+=sum(1 for y in ys if y<(1<<(kap-m)))
            for h in Ts: Ts[h]+=cmath.exp(2j*math.pi*((h*f0)%(1<<K))/(1<<K))*T(kap,(h*lam)%(1<<kap))
        assert len(cover)==len(EK) and set(cover)==EKs,(K,k)
        for m in cnt: assert cnt[m]==sum(1 for c in EK if c<(1<<(K-m))),(K,k,m)
        for h in Ts: assert abs(Ts[h]-TK[h])<1e-6*N[K]
print("Lemma 1 decomposition + window identity (all m<=k-3) + T identity OK, K<=40")
# Prop E
from functools import lru_cache
def propE(K,h):
    @lru_cache(None)
    def Gf(P,k):
        mod=1<<k
        if k<4: return T(k,(h*pow(3,-P,mod))%mod) if k>0 else 1
        return cmath.exp(-2j*math.pi*((h*pow(3,-(P+2),mod))%mod)/mod)*Gf(P+2,k-3)+Gf(P+3,k-4)
    return Gf(0,K)
mx=0
for K in range(4,31):
    for h in (1,2,3,5,7,12,1001, 1<<(K-3), 3<<(K-5) if K>5 else 1):
        mx=max(mx,abs(propE(K,h)-T(K,h))/N[K])
print("Prop E max rel error K<=30:",mx)
# necessity remark
for K in (20,30,40):
    print("K=%d |T_K(2^(K-j))|/N_K, j=3..8:"%K,["%.3f"%(abs(T(K,1<<(K-j)))/N[K]) for j in range(3,9)])
