import math
import numpy as np
s=0.28776078708402889; c1=6.5
N=[1,2,2,2]
for k in range(4,3000): N.append(N[k-3]+N[k-4])
r=[N[j]*2**(-s*j) for j in range(0,900)]
print("N_j 2^-sj: j=0..7",["%.4f"%v for v in r[:8]]," min j>=4: %.4f max j>=1: %.4f  limit ~%.5f"%(min(r[4:]),max(r[1:]),r[899]))
for e in (2,4,7,12,20,30,40,60,100,200):
    Qf=10.0**e; b=(1e99,0)
    for k in range(7,min(900,int(min(Qf,1e9))-90)):
        r_=(1+3*c1*2.0**(k-2)/math.sqrt(Qf-k-3))*(4.47+2.37*k)/math.sqrt(N[k-3])
        b=min(b,(r_,k))
    L=math.log2(Qf); B1=3.7*L*Qf**(-s/4)
    ms=math.floor(s/4*L-math.log2(L))
    print("Q=1e%d: min_k ThmB RHS/N_K = %.3g at k=%d ; B1 rhs = %.3g ; m*=%d ; CorC factor 13 L^(1-s) Q^(-s(1-s)/4) = %.3g (trivial: N_Q<=1.64*2^sQ)"%(e,b[0],b[1],B1,ms,13*L**(1-s)*Qf**(-s*(1-s)/4)))
worst=-9; worstA=-9
for L10 in range(220,40000):
    L=L10/10
    k=math.floor(L/2)-4
    for m in (1,math.floor(L/2-8)):
        if m<1: continue
        assert k>=max(7,m+3)
        lg_ratio=(k-2)-0.5*L   # 2^(k-2)/sqrt(Q); sqrt(Q+m-k-4) vs sqrt(Q): correction below
        corr=1.0 if L>60 else math.sqrt(2.0**L/(2.0**L+m-k-4))
        fac=(1+3*c1*2.0**lg_ratio*corr)*(4.47+2.37*k)/math.sqrt(N[k-3])
        worst=max(worst,math.log2(fac)-(math.log2(3.7*L)-s/4*L))
        fa=2*(1+3*c1*2.0**lg_ratio*corr)/math.sqrt(N[k-3])
        worstA=max(worstA,math.log2(fa)-(math.log2(6.2)-s/4*L))
print("Cor B1: max log2(ThmB factor/(3.7 log2Q Q^(-s/4))) on Q=2^22..2^4000 = %.4f ; Thm A (const 6.2, K=Q): %.4f  (<=0 confirms)"%(worst,worstA))
print("s(1-s)/4=%.5f 1-s=%.5f; 4.7*1.64=%.3f; *2^(1-s)=%.3f"%(s*(1-s)/4,1-s,4.7*1.64,4.7*1.64*2**(1-s)))
print("moduli roots z^4=z+1:",sorted(abs(np.roots([1,0,0,-1,-1]))), "2^s=%.5f"%2**s)
L=22
while math.floor(s/4*L-math.log2(L))<1: L+=1
print("m*>=1 first at Q=2^%d"%L)
