import random, math, itertools
from fractions import Fraction as Fr
random.seed(1)
s=0.2877607870840288
def alive(r,j):
    while True:
        if j==0: return True
        if j<=3:
            m=(1<<j)-1
            return (r&m)==(7&m) or (r&m)==0
        if r&7==7: r=((9*r+1)>>3)&((1<<(j-3))-1); j-=3
        elif r&15==0: r=((27*r)>>4)&((1<<(j-4))-1); j-=4
        else: return False
def Eset(k,memo={}):
    if k<=0: return {0}
    if k not in memo:
        M=1<<k; i9=pow(9,-1,M); i27=pow(27,-1,M)
        memo[k]={((8*z-1)*i9)%M for z in Eset(k-3)}|{(16*z*i27)%M for z in Eset(k-4)}
    return memo[k]
# --- counts
N=[len(Eset(k)) for k in range(65)]
print("N64",N[64],"max N_k/2^{sk} k<=64",max(N[k]/2**(s*k) for k in range(65)))
L={}
def Lf(Q):
    if Q<=0: return 1
    if Q not in L: L[Q]=Lf(Q-3)+Lf(Q-4)
    return L[Q]
print("leaves level60",Lf(60))
# --- A. theta identity
def apply(z,ch):
    if ch=='a':
        z2=(9*z+1)/8
        assert (z.numerator*pow(z.denominator,-1,8))%8==7
    else:
        assert (z.numerator*pow(z.denominator,-1,16))%16==0
        z2=27*z/16
    return z2
def fixpt(word):  # rational with itinerary word^omega : solve u(z)=z, u affine
    al,be=Fr(1),Fr(0)
    for ch in word:
        if ch=='a': al,be=al*Fr(9,8),(9*be+1)/8
        else: al,be=al*Fr(27,16),be*Fr(27,16)
    return be/(1-al)
def gammas(word):
    P=Q=0; g=Fr(0); out=[(0,0,Fr(0))]
    for ch in word:
        if ch=='a': g+=Fr(2**Q,3**(P+2)); P+=2;Q+=3
        else: P+=3;Q+=4
        out.append((P,Q,g))
    return out
cnt=0; maxg=Fr(0); badint=[]
for n in range(1,15):
    for word in itertools.product('ab',repeat=n):
        z=fixpt(word); z0=z
        G=gammas(word*3)
        for j,ch in enumerate(word*3):
            z=apply(z,ch); P,Q,g=G[j+1]
            assert z*2**Q==3**P*(z0+g); cnt+=1
        assert z==z0
        P,Q,g=G[n]; gR=g/(1-Fr(2**Q,3**P))   # gamma_R of periodic word
        assert z0+gR==0 and -1<=z0<=0 and 0<=gR<=1
        maxg=max(maxg,gR)
        if z0.denominator==1: badint.append((''.join(word),z0))
print("theta identity ok on",cnt,"periodic steps; max gamma_R",maxg,"; integer periodic pts:",set(v for _,v in badint))
# integer starts: least residues of cylinders of random long words
def least_res(word):
    r=0;q=0;M=1;wp=0   # wp=u(r), class r mod 2^q
    for ch in word:
        if ch=='a':
            t=next(t for t in range(8) if (9*(wp+M*t)+1)%8==0)
            r+=t<<q; q+=3; wp=(9*(wp+M*t)+1)//8; M*=9
        else:
            t=next(t for t in range(16) if (wp+M*t)%16==0)
            r+=t<<q; q+=4; wp=27*(wp+M*t)//16; M*=27
    return r,q,M,wp
for _ in range(3000):
    n=random.randint(1,60); word=[random.choice('ab') for _ in range(n)]
    r,q,M,wp=least_res(word); z=Fr(r); G=gammas(word)
    for j,ch in enumerate(word):
        z=apply(z,ch); P,Q,g=G[j+1]; assert z*2**Q==3**P*(r+g)
    assert z==wp and 0<=wp<M and (wp<<q)//M==r and G[-1][2]<1
print("integer-start identity + mirror ok on 3000 random words")
# --- B. rational scan: long-lived p/q
def lifeQ(p,q,cap=400):
    L=0
    while L<cap:
        if p%2:
            if (9*p+q)%8: return L
            p=(9*p+q)//8; L+=3
        else:
            if p%16: return L
            p=27*p//16; L+=4
        if p==0: return cap
    return L
H=400; out=[]; 
for q in range(1,H,2):
    for p in range(-H,H+1):
        if math.gcd(p,q)==1 and lifeQ(p,q)>=400: out.append(Fr(p,q))
print("rationals height<=%d with life>=400 bits:"%H,len(out),"outside [-1,0]:",[x for x in out if not -1<=x<=0],"integers:",[x for x in out if x.denominator==1])
print("  sample",sorted(out)[:12])
# --- C. (iv)
def Ed(d,k,gate):
    res=set()
    for r in range(1<<k):
        x=r;j=k;ok=True
        while j>0:
            if j<=3:
                m=(1<<j)-1; ok=(x&m)==(gate&m) or (x&m)==0; break
            if x%8==gate: x=((9*x+d)>>3)%(1<<(j-3)); j-=3
            elif x%16==0: x=((27*x)>>4)%(1<<(j-4)); j-=4
            else: ok=False;break
        if ok: res.add(r)
    return res
k=16; E=Eset(k); M=1<<k
for d in (-1,3,5,7,-115,115,11):
    right=Ed(d,k,(-d)%8)=={(d*z)%M for z in E}
    lit=Ed(d,k,7)=={(d*z)%M for z in E}
    print("d=%d: E_d==d*E with gate w=-d mod 8: %s ; with literal gate w=7 mod 8: %s"%(d,right,lit))
z=Fr(-27,115); z1=apply(z,'a'); z2=apply(z1,'b'); print("-27/115 ->",z1,"->",z2)
w=27; assert (9*w-115)%8==0; w1=(9*w-115)//8; print("d=-115: 27 ->",w1,"->",27*w1//16, "; gate 27 mod 8 =",27%8,"-d mod 8 =",115%8, "; mod 11:",27%11,16%11,115%11,"; mod 3 of w=33n+32d:",(32*-115)%3,27%3,16%3)
print("1 in -E:", (9*1-1)//8)
# --- D. hull
for m in (4,8,12):
    got=set()
    for kk in range(0,1<<(m-1)):
        K=4*kk+m; e=(-pow(16,kk)*pow(27,-kk,1<<K))%(1<<K)
        assert alive(e,min(K,60)) if K<=60 else True
        assert e%(16**kk)==0; got.add(e>>(4*kk))
    print("m=%d: e_k tops == {v=5,7 mod 8}:"%m, got=={v for v in range(1<<m) if v%8 in(5,7)})
# direct: all top-j-bit patterns among E mod 2^k, k<=48
for j in (6,8,10):
    pats=set()
    for k in range(j,49):
        pats|={c>>(k-j) for c in Eset(k)}
    print("top-%d-bit patterns seen among E mod 2^k (k<=48): %d of %d"%(j,len(pats),1<<j))
# F side
for m in (3,5):
    got={(-pow(16,-kk,3**m))%3**m for kk in range(2*3**m)}
    print("3-adic m=%d: == {v=2 mod 3}:"%m, got=={v for v in range(3**m) if v%3==2})
# --- E. bucket reflection
Qp=24;m=6;E=Eset(Qp);M=1<<Qp
from collections import Counter
bE=Counter(c>>(Qp-m) for c in E); bN=Counter(((-c)%M)>>(Qp-m) for c in E)
mis=[sg for sg in range(1<<m) if bN[sg]!=bE[(1<<m)-1-sg]]
print("bucket sigma of -E == bucket -sigma-1 of E fails at sigma:",mis,[(bN[x],bE[(1<<m)-1-x]) for x in mis])
