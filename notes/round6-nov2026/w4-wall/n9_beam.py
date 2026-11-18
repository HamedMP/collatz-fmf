"""n9_beam.py -- unbiased adversarial search: beam search for odd xi mod 2^k maximising |T_k(xi)|.
Uses T_k(xi) = e(-xi/9 /2^k) T_{k-3}(xi/9) + T_{k-4}(xi/27): candidates at level k are the 8 lifts
9x + t 2^(k-3) of the best x at level k-3 and the 16 lifts 27y + t 2^(k-4) of the best y at level k-4.
usage: python n9_beam.py kmax beam.  Prints, per level, the best exponent log|T|/log N found and whether
the maximiser is +-3^n*u/t (t in 1,11; u<=9), and the best member of that family for comparison."""
import sys, cmath, math
kmax=int(sys.argv[1]); beam=int(sys.argv[2])
N=[1,2,2,2]
for j in range(4,kmax+1): N.append(N[j-3]+N[j-4])
TW=2j*math.pi
def T(k,xi):
    m=1<<k; inv3=pow(3,-1,m)
    pw=[xi%m]
    for _ in range(k+5): pw.append(pw[-1]*inv3%m)
    nxt={}
    for A in range(k//3,-1,-1):
        cur={}
        for B in range((k-3*A)//4,-1,-1):
            P=2*A+3*B; kk=k-3*A-4*B
            if kk==0: g=1
            elif kk<4: g=1+cmath.exp(-TW*((pw[P]&((1<<kk)-1))/(1<<kk)))
            else: g=cmath.exp(-TW*((pw[P+2]&((1<<kk)-1))/(1<<kk)))*nxt[B]+cur[B+1]
            cur[B]=g
        nxt=cur
    return abs(cur[0])
def family(k):
    m=1<<k; out={}
    for n in range(0,k):
        for t in (1,11):
            for u in (1,3,5,7,9):
                for sg in (1,-1): out.setdefault(sg*pow(3,n,m)*u*pow(t,-1,m)%m,(sg,n,u,t))
    return out
best={}
k0=12
for k in range(k0,k0+4):
    sc=sorted(((T(k,xi),xi) for xi in range(1,1<<k,2)),reverse=True)[:beam]; best[k]=sc
for k in range(k0+4,kmax+1):
    cand=set()
    for _,x in best[k-3]:
        for t in range(8): cand.add((9*x+(t<<(k-3)))%(1<<k))
    for _,y in best[k-4]:
        for t in range(16): cand.add((27*y+(t<<(k-4)))%(1<<k))
    best[k]=sorted(((T(k,xi),xi) for xi in cand if xi&1),reverse=True)[:beam]
    if k%12==0 or k==kmax:
        fam=family(k); v,xi=best[k][0]; d=fam.get(xi)
        fb=max((T(k,x),x) for x in fam if fam[x][1]>=int(0.5*k) and fam[x][1]<=int(0.66*k))
        lg=math.log(N[k])
        print("k=%3d N=%.3g beam best: delta=%.4f %s | family best: delta=%.4f (%+d*3^%d*%d/%d)"%(k,N[k],1-math.log(v)/lg,("in family %+d*3^%d*%d/%d"%d) if d else "NOT in family xi=%d"%xi,1-math.log(fb[0])/lg,*fam[fb[1]]),flush=True)
