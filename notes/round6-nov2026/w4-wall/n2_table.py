"""n2_table.py -- full table of Fourier sums of the level sets along the WHOLE two-sided 3-orbit.
   G(P,k) := T_k(h * mult^{-P} mod 2^k),  P in [Pmin, Pmax]  (P<0: frequency h*mult^{|P|}, the
   'small integer' adversarial zone; P>0: the generic zone used in w3-fp0).
   Recursion (w3-fp0 Prop. E): G(P,k) = e(-d h mult^{-(P+2)}/2^k) G(P+2,k-3) + G(P+3,k-4), k>=4.
usage: python n2_table.py K h [mult d] [levels comma list]
For each recorded level k: delta(P) = -log2(|G(P,k)|/N_k)/log2(N_k); worst single P, and the worst
window average of length R=ceil(sqrt(k)) (the (SGP) quantity), separately for P<0 and P>=0."""
import sys, math, gmpy2
from gmpy2 import mpfr, mpc, mpz
K=int(sys.argv[1]); h=int(sys.argv[2])
mult=int(sys.argv[3]) if len(sys.argv)>3 else 3
d=int(sys.argv[4]) if len(sys.argv)>4 else 1
levels=[int(t) for t in sys.argv[5].split(',')] if len(sys.argv)>5 else [K//4,K//2,K]
prec=int(0.2*K)+96
gmpy2.get_context().precision=prec
TWOPI=2*gmpy2.const_pi()
Pmin=-int(0.75*K)-8; Pmax0=int(0.35*K)
def top(k): return Pmax0+int(0.75*(K-k))+6
MOD=mpz(1)<<K
inv=gmpy2.invert(mult,MOD)
# pw[j] = mult^j mod 2^K for j in [-JJ, JJ]
JJ=max(-Pmin, top(0))+8
pos=[mpz(1)]; neg=[mpz(1)]
for j in range(JJ):
    pos.append(pos[-1]*mult%MOD); neg.append(neg[-1]*inv%MOD)
def pw(j): return pos[j] if j>=0 else neg[-j]
def phase(num,k):
    num&=(1<<k)-1
    th=gmpy2.div_2exp(mpfr(num),k) if k<=prec else gmpy2.div_2exp(mpfr(num>>(k-prec)),prec)
    s,c=gmpy2.sin_cos(TWOPI*th)
    return mpc(c,s)
N=[1,2,2,2]
for k in range(4,K+1): N.append(N[k-3]+N[k-4])
rows={}
out={}
for k in range(0,K+1):
    hi=top(k); row=[None]*(hi-Pmin+1)
    if k>=4:
        r3=rows[k-3]; r4=rows[k-4]
    for P in range(Pmin,hi+1):
        if k==0: g=mpc(1)
        elif k<4: g=1+phase(-d*h*pw(-P),k)
        else: g=phase(-d*h*pw(-(P+2)),k)*r3[P+2-Pmin]+r4[P+3-Pmin]
        row[P-Pmin]=g
    rows[k]=row
    if k-5 in rows: del rows[k-5]
    if k in levels:
        lg=math.log2(N[k])
        out[k]=[ (float(gmpy2.log2(abs(g)/N[k])) if g!=0 else -1e9) for g in row]
for k in levels:
    L=out[k]; lg=math.log2(N[k]); R=math.ceil(math.sqrt(k))
    def P_of(ix): return ix+Pmin
    lo=max(Pmin,-int(0.72*k)); ix0=lo-Pmin; ixz=-Pmin; ix1=Pmax0-Pmin
    def worst(a,b):
        m=max(range(a,b),key=lambda i:L[i]); return P_of(m), -L[m]/lg
    def worstwin(a,b):
        best=None
        for st in range(a,b-R):
            mx=max(L[st:st+R]); av=mx+math.log2(sum(2**(x-mx) for x in L[st:st+R])/R)
            if best is None or av>best[1]: best=(P_of(st),av)
        return best[0], -best[1]/lg
    import statistics
    med=statistics.median(-x/lg for x in L[ixz:ix1])
    print("k=%d h=%d (%dn%+d) log2N=%.1f R=%d | generic P>=0: median delta=%.3f worst single (P=%d) delta=%.3f worst window (P0=%d) delta0=%.3f"%(
        (k,h,mult,d,lg,R,med)+worst(ixz,ix1)+worstwin(ixz,ix1)))
    wP,wd=worst(ix0,ixz); wwP,wwd=worstwin(ix0,ixz)
    print("      adversarial P<0 (xi=h*%d^n, n=-P): worst single n=%d (n/k=%.4f) delta=%.4f ; worst window start n=%d..%d (n/k=%.4f) delta0=%.4f"%(
        mult,-wP,-wP/k,wd,-wwP-R+1,-wwP,-wwP/k,wwd))
    # profile of delta vs n/k
    prof=[]
    for fr in (0.1,0.2,0.3,0.4,0.5,0.55,0.6,0.62,0.63,0.64,0.66,0.7):
        n=int(fr*k); prof.append("%.2f:%.3f"%(fr,-L[-n-Pmin]/lg))
    print("      profile n/k:delta  "+"  ".join(prof))
