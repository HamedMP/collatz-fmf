# Referee test of the finite inequality behind Theorem C (exact integer arithmetic except
# one final log comparison done with Fractions on a rational upper bound of log2 3).
import itertools, sys, random
from fractions import Fraction as F
from math import log2
random.seed(7)

def step(x,a): return (x//2,0) if x%2==0 else ((a*x+1)//2,1)
def lift(P,a):
    # least nonneg residue mod 2^N whose parity prefix is P (Terras bijection), by bit lifting
    r=0
    for n in range(len(P)):
        # check parity at step n for r mod 2^(n+1)
        x=r
        for j in range(n): x,_=step(x,a)
        if (x&1)!=P[n]: r+= 1<<n
    return r
def orbit(x,n,a):
    xs=[x]; ps=[]
    for _ in range(n):
        x,p=step(x,a); xs.append(x); ps.append(p)
    return xs,ps

def run(a,maxblk,maxw,mults,window_only):
    la=log2(a)
    stats=dict(cases=0,nd_cases=0,pairs=0,periodic=0,terras_fail=0,G_fail=0,dens_fail=0,final_fail=0,
               thmC_applicable=0,thmC_fail=0,nohyp_pairs=0,nohyp_fail=0)
    blocks=[tuple(b) for L in range(1,maxblk+1) for b in itertools.product((0,1),repeat=L)]
    for X in blocks:
      for Y in blocks:
        if X==Y: continue
        dens=max(F(sum(X),len(X)),F(sum(Y),len(Y)))
        for wl in range(2,maxw+1):
          ws=list(itertools.product('cd',repeat=wl-1))
          if len(ws)>24: ws=random.sample(ws,24)
          for w in ws:
            w=('c',)+w
            bl=[X if ch=='c' else Y for ch in w]
            P=[b for B in bl for b in B]; N=len(P)
            if N>60: continue
            pos=[0]
            for B in bl: pos.append(pos[-1]+len(B))
            r=lift(P,a)
            for m in mults:
                x0=r+m*(1<<N)
                if x0<2: continue
                xs,ps=orbit(x0,N,a)
                assert ps==P
                stats['cases']+=1
                ks=[0]
                for p in ps: ks.append(ks[-1]+p)
                # repeated block-aligned factors
                for I in range(wl):
                  for I2 in range(I+1,wl):
                    ln=0
                    while I2+ln<wl and w[I+ln]==w[I2+ln]:
                        ln+=1
                        i,i2=pos[I],pos[I2]; ul=pos[I+ln]-pos[I]
                        nd=all(xs[j]>=x0 for j in range(i2+1))
                        # Terras
                        if (xs[i]-xs[i2])%(1<<ul): stats['terras_fail']+=1; print("TERRAS FAIL",a,x0,X,Y,w,i,i2,ul)
                        # float theta' : max(dens, log_a 2) ; g
                        th=max(float(dens),1/la); g=th*la-1
                        from math import log2 as l2
                        bound=l2(x0)+(g+th*l2(1+1/(a*x0)))*i2
                        if not nd:
                            stats['nohyp_pairs']+=1
                            if xs[i]!=xs[i2] and ul>=bound: stats['nohyp_fail']+=1
                            continue
                        stats['pairs']+=1
                        if xs[i]==xs[i2]: stats['periodic']+=1; continue
                        mx=max(xs[i],xs[i2])
                        if not (1<<ul)<mx: stats['terras_fail']+=1; print("DICHOTOMY FAIL",x0,i,i2)
                        # Lemma G exactly at both times
                        for t in (i,i2):
                            if xs[t]*(1<<t)*(a*x0)**ks[t] > x0*a**ks[t]*(a*x0+1)**ks[t]: stats['G_fail']+=1
                            if F(ks[t],t) > dens if t else False: stats['dens_fail']+=1
                        if not ul<bound-1e-9:
                            stats['final_fail']+=1; print("FINAL FAIL",a,x0,X,Y,''.join(w),i,i2,ul,bound)
                        if i2<=3*ul and ul>=len(X) and 0<=g<1/3:
                            stats['thmC_applicable']+=1
                            c=1-3*g-3*th*l2(1+1/(a*x0))
                            if not len(X)*c<l2(x0): stats['thmC_fail']+=1; print("THMC FAIL",a,x0,X,Y,''.join(w),i,i2)
                if all(x>=x0 for x in xs): stats['nd_cases']+=1
    return stats
if __name__=="__main__":
    mults=[0,1,2,3,5,7,11,101,10**6+3]
    print("a=3",run(3,4,7,mults,False))
    print("a=5",run(5,4,7,mults,False))
