"""f2_check.py -- exact checks of the ingredients of Theorems A/B (w3-fp0).
usage: python f2_check.py [mult=3|5] [d=1|-1] [kmax=22]
All set computations are exact integers; floats only in the FFT cross-check and printed ratios."""
import sys, math
import numpy as np
mult = int(sys.argv[1]) if len(sys.argv)>1 else 3
d    = int(sys.argv[2]) if len(sys.argv)>2 else 1
kmax = int(sys.argv[3]) if len(sys.argv)>3 else 22
M2, M3 = mult*mult, mult**3
s = 0.28776081  # 2^(-3s)+2^(-4s)=1
x = 2.0**(-s)
assert abs(x**3+x**4-1)<1e-7

def Eset(k, memo={}):
    """E_k = E mod 2^k as a sorted list (system: a: w->(M2 w+d)/8 on w=-d mod 8, b: w->M3 w/16)."""
    if k in memo: return memo[k]
    if k<4:
        r = sorted({0, (-d) % (1<<k)})
    else:
        mod=1<<k
        i2=pow(M2,-1,mod); i3=pow(M3,-1,mod)
        r = sorted([((8*z-d)*i2)%mod for z in Eset(k-3)] + [(16*z*i3)%mod for z in Eset(k-4)])
        assert len(set(r))==len(r)
    memo[k]=r; return r

# ---- (1) brute-force definition check of E_k for small k
def life_ge(w,k):
    rem=k
    while rem>=4:
        if (w+d)%8==0: w=(M2*w+d)//8; rem-=3
        elif w%16==0: w=M3*w//16; rem-=4
        else: return False
    return w%(1<<rem)==0 or (w+d)%(1<<rem)==0
for k in range(0,17):
    assert Eset(k)==[w for w in range(1<<k) if life_ge(w,k)], k
print("E_k recursion == direct definition for k<=16: OK")

# ---- (2) constants: N_k 2^{-sk}, W_q x^q
N=[len(Eset(k)) for k in range(0,4)]
for k in range(4,400): N.append(N[k-3]+N[k-4])
assert all(N[k]==len(Eset(k)) for k in range(0,kmax+1))
W=[1,0,0,1]
for q in range(4,4000): W.append(W[q-3]+W[q-4])
rN=[N[k]*2.0**(-s*k) for k in range(60,64)]
rW=[W[q]*x**q for q in range(60,64)]
print("N_k 2^{-sk} on window k=60..63: min %.4f max %.4f  (convex-combination recursion => these bound all k>=60)"%(min(rN),max(rN)))
print("W_q x^q   on window q=60..63: min %.4f max %.4f"%(min(rW),max(rW)))
print("sup_{k>=0} N_k 2^{-sk} = %.4f, inf_{k>=4} = %.4f"%(max(N[k]*2.0**(-s*k) for k in range(0,64)), min(N[k]*2.0**(-s*k) for k in range(4,64))))
# max term M(q,i) = C(A+B,A) on 3A+4B=q versus W_q/sqrt(q)
worst=0
for q in range(80,3000,7):
    mx=0
    for B in range(0,q//4+1):
        if (q-4*B)%3==0:
            A=(q-4*B)//3; mx=max(mx, math.comb(A+B,A))
    worst=max(worst, mx*math.sqrt(q)/W[q])
print("max_q (M_max(q) sqrt(q)/W_q) over 80<=q<3000 (step 7): %.3f   [proved bound c1 = 1.8/0.28 = 6.5]"%worst)

# ---- (3) Parseval / coset average of |T_k(h lam)|, lam in <mult>
for k in (12,16,20):
    if k>kmax: continue
    mod=1<<k; ind=np.zeros(mod); ind[Eset(k)]=1
    T=np.abs(np.fft.fft(ind))
    assert abs((T**2).sum()-mod*N[k])<1e-6*mod*N[k]
    D=1<<(k-2); lam=[pow(mult,j,mod) for j in range(D)]
    assert len(set(lam))==D
    lam=np.array(lam,dtype=np.int64)
    worst=0; worstL1=0
    for h in list(range(1,65))+[mod//2, mod//4, 3*mod//8]:
        e=(h&-h).bit_length()-1
        avg=T[(h*lam)%mod].mean()
        worst=max(worst, avg/(2**(1+e/2)*math.sqrt(N[k])))
    print("k=%d: max_h  avg_{lam in <%d>} |T_k(h lam)| / (2^{1+e/2} sqrt(N_k)) = %.3f (must be <=1)"%(k,mult,worst))

# ---- (4) exact R(k,m) = avg_{lam in <mult>} sup_tau #{c in E_k : lam c + tau mod 2^k in [0,2^{k-m})}
def Rtable(k, ms):
    mod=1<<k; D=1<<(k-2); E=np.array(Eset(k),dtype=np.int64); n=len(E)
    tot={m:0 for m in ms}; mxJ={m:0 for m in ms}
    CH=1<<14
    lam=1
    for start in range(0,D,CH):
        cnt=min(CH,D-start)
        lams=np.empty(cnt,dtype=np.int64)
        for i in range(cnt):
            lams[i]=lam; lam=(lam*mult)%mod
        V=np.sort((lams[:,None]*E[None,:])%mod,axis=1)
        Vx=np.concatenate([V,V+mod],axis=1)
        for m in ms:
            L=1<<(k-m)
            # for each start index i: number of points in [V_i, V_i+L)
            best=np.zeros(cnt,dtype=np.int64)
            for i in range(n):
                c=(Vx[:,i:i+n] < (V[:,i]+L)[:,None]).sum(axis=1)
                best=np.maximum(best,c)
            tot[m]+=int(best.sum()); mxJ[m]=max(mxJ[m],int(best.max()))
    return {m:(tot[m]/D, mxJ[m]) for m in ms}
print("\nExact R(k,m)/N_k  (average over the cyclic group <%d> mod 2^k of the worst window of length 2^(k-m));"%mult)
print("compare 2^-m (equidistribution) and the Fourier bound 2^-m + (6.83+2.37k)/sqrt(N_k).  [max over lam of J/N_k in brackets]")
ms=[1,2,3,4,5,6]
print("  k   N_k  "+"  ".join("m=%d          "%m for m in ms))
for k in range(8,kmax+1,2):
    R=Rtable(k,[m for m in ms if m<=k-3])
    print("%3d %5d  "%(k,N[k])+"  ".join("%.4f [%.3f]"%(R[m][0]/N[k],R[m][1]/N[k]) if m in R else " "*14 for m in ms))
print("  2^-m:    "+"  ".join("%.4f        "%(2.0**-m) for m in ms))
