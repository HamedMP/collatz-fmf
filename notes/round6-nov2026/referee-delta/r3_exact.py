# referee: exact tests of Lemma 1, 2, 3, Prop I and the Theorem H / S bookkeeping
from fractions import Fraction as Fr
import random, sys
random.seed(20261117)
def T(x,d=1): return x//2 if x%2==0 else (3*x+d)//2
# ---- Lemma 1, 2, Prop I: exhaustive for L<=15
cnt=0; worst_r=Fr(0); tight2=Fr(0)
for L in range(0,16):
    seen=set()
    for x in range(2**L,2**(L+1)):
        y=x; v=[]; 
        for j in range(L): v.append(y&1); y=T(y)
        seen.add(tuple(v)); a=sum(v)
        ds=[j for j in range(L) if v[j]]
        r=sum(3**(a-1-i)*2**ds[i] for i in range(a))
        assert y*2**L==3**a*x+r                      # formula
        assert Fr(r,2**L) <= Fr(3,2)**a-1            # remainder bound
        if a: worst_r=max(worst_r,Fr(r,2**L)/(Fr(3,2)**a-1))
        for s in range(0,7):
            if 3**a*(2**a+1)*2**s <= 2**(L+a):       # good
                assert y*2**s <= x, (L,x,s)
                tight2=max(tight2,Fr(y*2**s,x))
        # Prop I
        tau=(r*pow(2**L,-1,3**a))%(3**a) if a>0 else 0
        assert y==3**a+tau,(L,x)
        # vector depends only on x mod 2^L
        cnt+=1
    assert len(seen)==2**L
print("Lemma1/2/PropI: %d integers, all levels 0..15 OK; max r/(bound)=%.6f; max 2^s T^L(x)/x over good=%.6f"%(cnt,float(worst_r),float(tight2)))
# Prop I random large
for _ in range(3000):
    L=random.randint(16,200); x=random.randrange(2**L,2**(L+1)); y=x; v=[]
    for j in range(L): v.append(y&1); y=T(y)
    a=sum(v); ds=[j for j in range(L) if v[j]]; r=sum(3**(a-1-i)*2**ds[i] for i in range(a))
    tau=(r*pow(2**L,-1,3**a))%(3**a) if a>0 else 0
    assert y==3**a+tau and y*2**L==3**a*x+r and Fr(r,2**L)<=Fr(3,2)**a-1
print("Prop I / Lemma 1 random large: 3000 OK")
# ---- Lemma 3 + Theorem H bookkeeping on stretches
def stretch(n,d=1,maxlen=10**6):
    xs=[];seen=set();x=n
    while x not in seen and len(xs)<maxlen:
        seen.add(x);xs.append(x);x=T(x,d)
    return xs
def check(xs,s,d=1):
    K=len(xs); lev=[x.bit_length()-1 for x in xs]
    # parity count among next L terms: need terms beyond the stretch possibly -> recompute from x directly
    bad=Fr(0);over=Fr(0);tot=Fr(0);A={}
    maxratio=Fr(0)
    for k,x in enumerate(xs):
        L=lev[k]; y=x;a=0
        for j in range(L): a+=y&1; y=T(y,d)
        tot+=Fr(1,x)
        if not (3**a*(2**a+1)*2**s <= 2**(L+a)): bad+=Fr(1,x); continue
        assert y*2**s<=x
        if k+L>=K: over+=Fr(1,x); continue
        assert xs[k+L]==y
        A.setdefault(k+L,[]).append(k)
    ch=Fr(0)
    for t,ks in A.items():
        S=sum(Fr(1,xs[k]) for k in ks); ch+=S
        assert S*xs[t] <= Fr(2,2**s),(t,ks)
        maxratio=max(maxratio,S*xs[t]*2**s)
        assert len(set(lev[k] for k in ks))==len(ks)
    assert over<=1
    assert tot==bad+over+ch and ch<=Fr(2,2**s)*tot
    return float(tot),float(bad),float(over),float(maxratio)
tests=list(range(1,4001))+[2**k-1 for k in range(2,120)]+[2**k+1 for k in range(2,120)]+[(4**k-1)//3 for k in range(2,60)]+[random.getrandbits(100)|1 for _ in range(150)]+[27*2**j for j in range(40)]+[993*2**j for j in range(1,30)]
for d in (1,-1):
  mx=(0,0);mb=0;mo=0;mr=0;nst=0
  for n in tests:
    xs=stretch(n,d)
    cands=[xs]
    if len(xs)>6:
        for _ in range(3):
            i=random.randrange(0,len(xs)-2); j=random.randrange(i+1,len(xs)+1); cands.append(xs[i:j])
    for seg in cands:
      for s in (2,3,4):
        tot,bad,over,ratio=check(seg,s,d); nst+=1
        if tot>mx[0]: mx=(tot,seg[0])
        if s==3: mb=max(mb,bad)
        mo=max(mo,over); mr=max(mr,ratio)
  print("d=%+d: %d (stretch,s) checks OK; max sum=%.6f (start %d); max bad mass(s=3)=%.4f (bound 19.372); max overhang=%.4f (<=1); max ancestor ratio=%.4f (<=2)"%(d,nst,mx[0],mx[1],mb,mo,mr))
# ---- bad mass by enumeration vs binomial count, s=3, levels<=18
from math import comb, log
for L in range(0,19):
    c=0; m=Fr(0)
    for x in range(2**L,2**(L+1)):
        y=x;a=0
        for j in range(L): a+=y&1;y=T(y)
        if not (3**a*(2**a+1)*8 <= 2**(L+a)): c+=1; m+=Fr(1,x)
    am=0
    while am<=L and 3**am*(2**am+1)*8<=2**(L+am): am+=1
    b=sum(comb(L,a) for a in range(am,L+1)); assert b==c
    bound=min(b/2**L, 2.0**-L+log(1+b/2**L)); assert float(m)<=bound+1e-15
print("bad counts by enumeration == binomial counts, and true bad mass <= per-level bound, L<=18 OK")
# ---- reciprocal-sum bound sanity (worst case = consecutive integers / consecutive odds)
for M in (1,2,4,64,1024):
    for b in range(1,M+1):
        tr=sum(Fr(1,M+i) for i in range(b)); assert float(tr)<=1/M+log(1+b/M)+1e-15
        if 2*b<=M+1:
            tro=sum(Fr(1,M+1+2*i) for i in range(b)); assert float(tro)<=1/M+0.5*log(1+2*b/M)+1e-15
print("reciprocal-sum bounds OK")
# ---- Theorem S bookkeeping (crude criterion) on full stretches
eta=0.9499555271883306; worst=0
for n in tests[:4000]+tests[4000:4300]:
    xs=stretch(n); K=len(xs)
    lv=sorted(x.bit_length()-1 for x in xs)
    import bisect
    for L in range(0,lv[-1]+1):
        NL=bisect.bisect_right(lv,L); worst=max(worst,NL/2**(eta*L))
print("Thm S: max N_L/2^(eta L) over tests = %.4f (bound 11.3)"%worst)
