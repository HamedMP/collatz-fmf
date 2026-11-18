# Strongest finite form, small x0 (where it has content): for ANY i<i', L with pi[i,i+L)=pi[i',i'+L),
# and |x_j|>=|x0| for j<=i':  x_i==x_i'  or  2^L <= |x_i-x_i'| < max|x_t| <= |x0| a^k_t/2^t (1+1/(a x0))^k_t  (exact).
import sys
from math import log2
def step(x,a): return (x//2,0) if x%2==0 else ((a*x+1)//2,1)
def test(a,xrange_,CAP=64,label=""):
    st=dict(x0=0,pairs=0,content=0,periodic=0,cong_fail=0,size_fail=0,G_fail=0); tight=None
    for x0 in xrange_:
        if x0 in (0,-1): continue
        xs=[x0]; ps=[]
        x=x0
        for _ in range(2*CAP):
            x,p=step(x,a); xs.append(x); ps.append(p)
        nd=0
        while nd<CAP and abs(xs[nd+1])>=abs(x0): nd+=1   # |x_j|>=|x0| for j<=nd
        if nd<2: continue
        st['x0']+=1
        ks=[0]
        for p in ps: ks.append(ks[-1]+p)
        for i in range(nd):
            for i2 in range(i+1,nd+1):
                L=0
                while L<CAP and ps[i+L]==ps[i2+L]: L+=1
                if L==0: continue
                st['pairs']+=1
                if (xs[i]-xs[i2])%(1<<L): st['cong_fail']+=1; print("CONG FAIL",a,x0,i,i2,L)
                if L<CAP and (xs[i]-xs[i2])%(1<<(L+1))==0 and xs[i]!=xs[i2]: st['cong_fail']+=1; print("CONVERSE FAIL",a,x0,i,i2,L)
                if xs[i]==xs[i2]: st['periodic']+=1; continue
                if (1<<L)>abs(x0): st['content']+=1
                for t in (i,i2):
                    k=ks[t]
                    if x0>0:
                        if xs[t]*(1<<t)*(a*x0)**k > x0*a**k*(a*x0+1)**k: st['G_fail']+=1; print("G FAIL",a,x0,t)
                    else:
                        if abs(xs[t])*(1<<t) > abs(x0)*a**k: st['G_fail']+=1; print("G FAIL neg",a,x0,t)
                mx=max(abs(xs[i]),abs(xs[i2]))
                if not (1<<L)<mx: st['size_fail']+=1; print("SIZE FAIL",a,x0,i,i2,L,xs[i],xs[i2])
                s=log2(mx)-L
                if tight is None or s<tight[0]: tight=(s,x0,i,i2,L)
    print(label,"a=%d"%a,st,"tightest log2(max)-L:",tight)
test(3,range(2,200001),label="pos")
test(5,range(2,60001),label="pos")
test(3,range(-20000,-1),label="neg")
test(7,range(2,20001),label="pos")
# litmus cycles
def litmus(a,x0,per):
    xs=[x0]; ps=[]; x=x0
    for _ in range(6*per): x,p=step(x,a); xs.append(x); ps.append(p)
    print("litmus a=%d x0=%d parity period %s min|x| on cycle=%d"%(a,x0,''.join(map(str,ps[:per])),min(map(abs,xs))))
    # Lemma L on c^omega with X=period: u=c at block positions 0,1 -> bits i=0,i'=per
    print("   X=period, u=X at i=0,i'=%d: x_i=%d x_i'=%d ->"%(per,xs[0],xs[per]),"PERIODIC branch" if xs[0]==xs[per] else "INEQUALITY branch")
    bad=0;tot=0;perb=0
    for i in range(2*per):
        for i2 in range(i+1,3*per):
            L=0
            while L<2*per and ps[i+L]==ps[i2+L]: L+=1
            if L==0: continue
            tot+=1
            if xs[i]==xs[i2]: perb+=1; continue
            if not (1<<L)<max(abs(xs[i]),abs(xs[i2])): bad+=1
    print("   all repeated factors: pairs",tot,"periodic-branch",perb,"violations",bad)
litmus(5,13,7); litmus(5,1,2) ; litmus(5,17,7); litmus(3,-5,3); litmus(3,-17,11); litmus(3,-1,1); litmus(3,1,2)
