"""f3_dp.py -- polynomial-time evaluation of the Fourier sums of the level sets,
   T_K(xi) = sum_{c in E_K} e(xi c / 2^K),   via   G(P,k) := T_k(h * mult^{-P} mod 2^k),
   G(P,k) = e(-d h mult^{-(P+2)} / 2^k) G(P+2,k-3) + G(P+3,k-4)   (k>=4).
usage: python f3_dp.py K h1,h2,... [mult=3] [d=1]
prints |T_K(h)|/N_K, the square-root benchmark N_K^{-1/2}, and max over P of |G(P,k)|/N_k at the
intermediate levels k = K/2 (frequencies h*mult^{-P}: the 'geometric progression' family).
High-precision (gmpy2) arithmetic: precision 0.2K+96 bits; phases from exact integers."""
import sys, math, gmpy2
from gmpy2 import mpfr, mpc
K=int(sys.argv[1]); hs=[int(t) for t in sys.argv[2].split(',')]
mult=int(sys.argv[3]) if len(sys.argv)>3 else 3
d=int(sys.argv[4]) if len(sys.argv)>4 else 1
prec=int(0.2*K)+96
gmpy2.get_context().precision=prec
TWOPI=2*gmpy2.const_pi()
def phase(num,k):   # e(num/2^k), num integer
    num%= (1<<k)
    th=gmpy2.div_2exp(mpfr(num),k) if k<=prec else gmpy2.div_2exp(mpfr(num>>(k-prec)),prec)
    a=TWOPI*th
    return mpc(gmpy2.cos(a),gmpy2.sin(a))
N=[1,2,2,2]
for k in range(4,K+1): N.append(N[k-3]+N[k-4])
def run(h):
    Amax=K//3
    # rows indexed by A (descending); row[B] = G at (A,B)
    nxt={}  # row A+1
    mid={}
    for A in range(Amax,-1,-1):
        cur={}
        Bmax=(K-3*A)//4
        for B in range(Bmax,-1,-1):
            P=2*A+3*B; k=K-3*A-4*B
            if k<4:
                if k==0: g=mpc(1)
                else:
                    inv=pow(mult,-P,1<<k)
                    g=1+phase(-d*h*inv,k)
            else:
                inv=pow(mult,-(P+2),1<<k)
                g=phase(-d*h*inv,k)*nxt[B]+cur[B+1]
            cur[B]=g
            if k in (K//2,K//2+1,K//2+2,K//2+3):
                r=abs(g)/N[k]
                if k not in mid or r>mid[k][0]: mid[k]=(r,P)
        nxt=cur
    return cur[0], mid
print("# K=%d mult=%d d=%d   log2 N_K=%.2f   sqrt benchmark N_K^-1/2 = 2^%.2f"%(K,mult,d,math.log2(N[K]), -0.5*math.log2(N[K])))
for h in hs:
    T,mid=run(h)
    r=abs(T)/N[K]
    l2=float(gmpy2.log2(r)) if r>0 else float('-inf')
    worst=max(mid.values())
    kk=[k for k in mid if mid[k]==worst][0]
    print("h=%6d  log2(|T_K(h)|/N_K) = %9.2f   ratio to sqrt benchmark: 2^%+.2f   | max_P |T_k(h*%d^-P)|/N_k at k~K/2: 2^%.2f (k=%d, sqrt bench 2^%.2f)"%(
        h,l2,l2+0.5*math.log2(N[K]),mult,float(gmpy2.log2(worst[0])),kk,-0.5*math.log2(N[kk])))
