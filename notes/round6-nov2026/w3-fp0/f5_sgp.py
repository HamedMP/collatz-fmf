"""f5_sgp.py -- numerical support for the named estimate (SGP): decay of the Fourier sums of E_k
along SHORT geometric progressions  xi_i = h * mult^{-i} mod 2^k,  i = 0..R-1,  R ~ sqrt(k).
usage: python f5_sgp.py k h R [mult d]
prints log2 of  (1/R) sum_i |T_k(xi_i)| / N_k  and of max_i, against the square-root benchmark."""
import sys, math, gmpy2
from gmpy2 import mpfr, mpc
K=int(sys.argv[1]); h=int(sys.argv[2]); R=int(sys.argv[3])
mult=int(sys.argv[4]) if len(sys.argv)>4 else 3
d=int(sys.argv[5]) if len(sys.argv)>5 else 1
prec=int(0.2*K)+96
gmpy2.get_context().precision=prec
TWOPI=2*gmpy2.const_pi()
def phase(num,k):
    num%=(1<<k)
    th=gmpy2.div_2exp(mpfr(num),k) if k<=prec else gmpy2.div_2exp(mpfr(num>>(k-prec)),prec)
    a=TWOPI*th
    return mpc(gmpy2.cos(a),gmpy2.sin(a))
N=[1,2,2,2]
for k in range(4,K+1): N.append(N[k-3]+N[k-4])
def run(P0):
    nxt={}
    for A in range(K//3,-1,-1):
        cur={}
        for B in range((K-3*A)//4,-1,-1):
            P=P0+2*A+3*B; k=K-3*A-4*B
            if k<4: g=mpc(1) if k==0 else 1+phase(-d*h*pow(mult,-P,1<<k),k)
            else:   g=phase(-d*h*pow(mult,-(P+2),1<<k),k)*nxt[B]+cur[B+1]
            cur[B]=g
        nxt=cur
    return abs(cur[0])/N[K]
vals=[run(P0) for P0 in range(R)]
avg=sum(vals)/R
print("k=%d h=%d R=%d (system %dn%+d): log2 avg = %.2f, log2 max = %.2f, log2 min = %.2f ; sqrt benchmark %.2f ; trivial 0"%(
    K,h,R,mult,d,float(gmpy2.log2(avg)),float(gmpy2.log2(max(vals))),float(gmpy2.log2(min(vals))),-0.5*math.log2(N[K])))
