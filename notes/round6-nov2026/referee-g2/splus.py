# referee-g2: Theorem S+ numerics. b_L(s)=B_L(s)/2^(eta L) by scaled DP (cross-checked with exact integers for small L),
# then the recursion n_L = 2^-eta n_{L-1} + L 2^(-eta s) n_{L-s} + b_L(s) + L 2^(-eta L), s=s(L)=ceil(log2(10L)/eta) with equality (worst case).
import numpy as np, math, sys
th=math.log(2)/math.log(3); lam=th/(1-th); eta=-(th*math.log2(th)+(1-th)*math.log2(1-th)); l3=math.log2(3)
om=1.5-th*math.log2(lam)/eta
print("theta0=%.6f lambda=%.6f eta=%.7f theta0*log2(lam)=%.6f /eta=%.6f omega=%.6f 2^-eta=%.5f (1+lam)lam^-theta0=%.7f 2^eta=%.7f"%(th,lam,eta,th*math.log2(lam),th*math.log2(lam)/eta,om,2**-eta,(1+lam)*lam**-th,2**eta))
Lmax=int(sys.argv[1]) if len(sys.argv)>1 else 3000
def sL(L): return math.ceil(math.log2(10*L)/eta)
svals=sorted(set(sL(L) for L in range(1,Lmax+1)))
a=np.arange(Lmax+2)
b={}
for s in svals:
    p=np.zeros(Lmax+2); p[0]=1.0; out=np.zeros(Lmax+1); c=2**-eta
    for j in range(1,Lmax+1):
        q=np.empty_like(p); q[0]=p[0]*c; q[1:]=(p[1:]+p[:-1])*c
        q[a*l3-j<=-(s+1)]=0.0      # bad iff S_j > -(s+1) for all j
        p=q; out[j]=p.sum()
    b[s]=out
# exact integer cross-check
def Bexact(L,s):
    cur={0:1}
    for j in range(1,L+1):
        nxt={}
        for aa,cnt in cur.items():
            for a2 in (aa,aa+1):
                if j-s<=1 and True:
                    ok = (2*3**a2)*(1<<max(0,s-j)) > (1<<max(0,j-s))
                else: ok = 2*3**a2 > 1<<(j-s)
                if ok: nxt[a2]=nxt.get(a2,0)+cnt
        cur=nxt
    return sum(cur.values())
for L in (30,60,120):
    s=sL(L); ex=Bexact(L,s); print("exact check L=%d s=%d: B=%d  DP/exact=%.12f"%(L,s,ex,b[s][L]*2**(eta*L)/ex))
# (BAL)-consequence ratio
worst=0
for s in svals:
    for L in range(20,Lmax+1):
        worst=max(worst,b[s][L]*L**1.5/((s+2)*lam**(th*(s+1))))
print("sup_{s in s(L)-range, 20<=L<=%d} B_L(s) L^1.5/((s+2) lam^(theta0(s+1)) 2^(eta L)) = %.3f"%(Lmax,worst))
n=np.zeros(Lmax+1)
for L in range(1,Lmax+1):
    s=sL(L)
    n[L]=c*n[L-1]+(L*2**(-eta*s)*n[L-s] if L-s>=0 else 0)+b[s][L]+L*2**(-eta*L)
g=lambda L: L**-om*math.log(L+2)
print("  L  s(L)  b_L        n_L        n_L/g(L)   n_L*L^0.5  n_L/b_L  [first two terms]/n_L")
for L in (25,50,100,200,400,800,1200,1600,2000,2400,3000):
    if L>Lmax: break
    s=sL(L); first=(c*n[L-1]+L*2**(-eta*s)*n[L-s])/n[L]
    print("%5d %3d %.4e %.4e %9.3f %9.3f %7.3f %.4f"%(L,s,b[s][L],n[L],n[L]/g(L),n[L]*L**0.5,n[L]/b[s][L],first))
loc=[(L,(math.log(n[2*L]/math.log(2*L+2))-math.log(n[L]/math.log(L+2)))/math.log(2)) for L in (100,200,400,800,1500) if 2*L<=Lmax]
print("local exponent of n_L/log(L+2) between L and 2L:",["%d:%.3f"%x for x in loc]," (claimed -omega=%.3f)"%-om)
