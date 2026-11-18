# referee-g2: own exact computation of N(L,m,s) = #{y in [2^L,2^(L+1)) : T^(L+m)(y) > y/2^s}, L=20,
# against (i) the independence prediction (first generation exact, second generation fair coins, criterion as in the proof of Cor. N:
#   bad needs  w > theta0*m - kappa - (s+1)*theta0 [proof's necessary condition]  and the sharper endpoint criterion (a+w)log2 3 > L+m-s),
# (ii) the claimed bound shape lam^(s theta0) m 2^(-(1-eta)m) 2^(eta L)/sqrt(L).  Also per-class equidistribution of z_v mod 2^m (Theorem W, tiny case).
import math, sys
from math import comb
th=math.log(2)/math.log(3); lam=th/(1-th); eta=-(th*math.log2(th)+(1-th)*math.log2(1-th))
L=int(sys.argv[1]) if len(sys.argv)>1 else 20
MS=(2,4,6,8,10,12,14,16); mmax=max(MS)
cntA=[0]*(L+1); N={(m,s):0 for m in MS for s in (0,1,3)}; viol=0
cls={}  # (a, z mod 2^8) -> count  for a near theta0 L
for y in range(1<<L,1<<(L+1)):
    x=y; a=0
    for j in range(L):
        if x&1: x=(3*x+1)>>1; a+=1
        else: x>>=1
    cntA[a]+=1
    if abs(a-th*L)<=1.5: cls[(a,x&255)]=cls.get((a,x&255),0)+1
    w=0
    for j in range(1,mmax+1):
        if x&1: x=(3*x+1)>>1; w+=1
        else: x>>=1
        if j in MS:
            for s in (0,1,3):
                if x<<s > y:            # T^(L+m)(y) > y/2^s
                    N[(j,s)]+=1
                    kap=a-th*L
                    if not (w > th*j-kap-(s+1)*th) and j>=s+2 and L>=s+1+j: viol+=1
print("violations of the proof's necessary condition (must be 0):",viol)
def tail(m,t):  # P(Bin(m,1/2) > t) with real t
    k=math.floor(t)+1
    return sum(comb(m,w) for w in range(max(k,0),m+1))/2**m if k<=m else 0.0
print(" m  s   N_exact   pred_endpoint ratio   pred_proofcond ratio   bound_shape  N/shape")
for s in (0,1,3):
    for m in MS:
        if m<s+2: continue
        p1=sum(cntA[a]*tail(m,(L+m-s)*th-a) for a in range(L+1))
        p2=sum(cntA[a]*tail(m,th*m-(a-th*L)-(s+1)*th) for a in range(L+1))
        sh=lam**(s*th)*m*2**(-(1-eta)*m)*2**(eta*L)/math.sqrt(L)
        print("%2d %2d %9d %12.1f %6.3f %12.1f %6.3f %12.1f %6.3f"%(m,s,N[(m,s)],p1,N[(m,s)]/p1,p2,N[(m,s)]/p2,sh,N[(m,s)]/sh))
for a in sorted(set(k[0] for k in cls)):
    tot=sum(v for k,v in cls.items() if k[0]==a); dev=max(abs(cls.get((a,r),0)/tot-1/256) for r in range(256))
    print("a=%d C(L,a)=%d: max_r |P(z=r mod 256)-1/256| = %.5f  (1/256=%.5f, sqrt-noise ~ %.5f)"%(a,tot,dev,1/256,math.sqrt(1/256/tot)))
