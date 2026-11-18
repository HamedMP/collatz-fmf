# referee: independent recomputation of all constants (exact binomials, mpmath interval-free but 40-digit)
from math import comb
from fractions import Fraction
import mpmath as mp
mp.mp.dps=40
LMAX=1500
th0=mp.log(2)/mp.log(3); H2=lambda t: -(t*mp.log(t,2)+(1-t)*mp.log(1-t,2)); eta=H2(th0)
print("eta",eta, "2^-eta",2**-eta)
def amin_of(L,s,q=3):
    a=0
    # good iff q^a(1+2^-a) <= 2^(L-s)  <=> q^a (2^a+1) 2^s <= 2^(L+a)
    while a<=L and q**a*(2**a+1)*2**s <= 2**(L+a): a+=1
    return a   # bad iff a>=amin
def levels(s,q=3):
    out=[]
    for L in range(LMAX):
        am=amin_of(L,s,q)
        b=sum(comb(L,a) for a in range(am,L+1))
        bo=sum(comb(L-1,a-1) for a in range(max(am,1),L+1)) if L>=1 else (1 if am==0 else 0)
        # L=0: integer 1, vector empty; it is odd.  count it as odd-bad to be safe
        pa=mp.mpf(b)/mp.mpf(2)**L; po=mp.mpf(bo)/mp.mpf(2)**L
        ma=min(pa, mp.mpf(2)**-L+mp.log(1+pa)); mo=min(po, mp.mpf(2)**-L+mp.log(1+2*po)/2)
        out.append((ma,mo,b,bo))
    return out
def tail(s):
    th=(LMAX-s-1)*th0/LMAX; rate=1-H2(th); return mp.mpf(2)**(-rate*LMAX)/(1-mp.mpf(2)**(-rate))
D={}
for s in (2,3,4,5,6):
    lv=levels(s); tl=tail(s)
    sa=[mp.mpf(0)]*(LMAX+1); so=[mp.mpf(0)]*(LMAX+1)
    for L in range(LMAX-1,-1,-1): sa[L]=sa[L+1]+lv[L][0]; so[L]=so[L+1]+lv[L][1]
    D[s]=(sa,so,tl)
    c=mp.mpf(2)**(1-s)
    print("s=%d beta_all(0)=%s tail=%s  H const=%s"%(s,mp.nstr(sa[0]+tl,10),mp.nstr(tl,3),mp.nstr((sa[0]+tl+1)/(1-c),10)))
def bounds(L0,eps):
    U=min((D[s][0][L0]+D[s][2]+eps)/(1-mp.mpf(2)**(1-s)) for s in D)
    W=min(D[s][1][L0]+D[s][2]+eps+mp.mpf(2)**(1-s)*U for s in D)
    return U,W
MB=mp.mpf('0.225654112732')+mp.mpf('1e-9'); PB=495
eps=33*mp.mpf(2)**-32+(PB+2)*mp.mpf(2)**-31
U,W=bounds(32,eps)
print("L0=32: beta_all(32),beta_odd(32) per s:",[(s,mp.nstr(D[s][0][32],7),mp.nstr(D[s][1][32],7)) for s in D])
print("eps",mp.nstr(eps,4),"U",mp.nstr(U,8),"W_odd",mp.nstr(W,8),"Res<=",mp.nstr(mp.exp(MB+W/3),8),"segment<=",mp.nstr(mp.exp(MB+W/3)*4/3,8))
for L0 in (32,68,71):
    U,W=bounds(L0,(L0+1)*mp.mpf(2)**-L0)
    print("levels>=%d: sum<=%s odd<=%s prod<=%s"%(L0,mp.nstr(U,8),mp.nstr(W,8),mp.nstr(mp.exp(W/3),8)))
# Theorem S
sup=0;arg=0
for L in range(0,1200):
    b=sum(comb(L,a) for a in range(0,L+1) if 16*3**a>2**L)
    r=mp.mpf(b+L)/mp.mpf(2)**(eta*L)
    if r>sup: sup=r;arg=L
print("Thm S: sup_{L<1200}(b_L+L)/2^(eta L)=",mp.nstr(sup,8),"at L=",arg)
ch=mp.mpf(2)**(4*th0*mp.log(th0/(1-th0),2)); den=1-2**-eta-2**(-3*eta)
print("Chernoff const",mp.nstr(ch,8),"denominator",mp.nstr(den,8),"K0 needed >=",mp.nstr((ch+mp.mpf(1200)/mp.mpf(2)**(eta*1200))/den,8), " small-L K0:",mp.nstr(sup/den,8))
# direct check of the true ratio b_L/2^(eta L) for large L against 3.868
for L in (1200,1300,1499):
    b=sum(comb(L,a) for a in range(0,L+1) if 16*3**a>2**L); print(" L",L,"b_L/2^(eta L)=",mp.nstr(mp.mpf(b)/mp.mpf(2)**(eta*L),6))
# exact recursion bound: iterate N_L <= N_{L-1}+N_{L-3}+b_L+L and compare with 11.3*2^(eta L)
N=[0,0,0]; worst=0
for L in range(0,1200):
    b=sum(comb(L,a) for a in range(0,L+1) if 16*3**a>2**L)
    N.append(N[-1]+N[-3]+b+L); r=mp.mpf(N[-1])/mp.mpf(2)**(eta*L); worst=max(worst,r)
print("recursion iterate: sup N_L/2^(eta L) =",mp.nstr(worst,8))
# 5n+1 litmus
for L in (40,160,640):
    am=amin_of(L,3,5); print("q=5 L",L,"bad fraction",mp.nstr(mp.mpf(sum(comb(L,a) for a in range(am,L+1)))/mp.mpf(2)**L,6))
