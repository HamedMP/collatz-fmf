# Independent numeric check of every identity formalized in lean/CollatzFMF/*.lean.
# FMF / hop are computed SEMANTICALLY (iterate Collatz until first multiple of 4),
# not from the closed formulas.
import random
def C(n): return n//2 if n%2==0 else 3*n+1
def v2(n):
    k=0
    while n%2==0: n//=2; k+=1
    return k
def fmf_sem(x):
    k=0; y=x
    while y%4: y=C(y); k+=1
    return k,y
def hop(x):
    _,f=fmf_sem(x); return f>>v2(f)
def letter(x): return (v2(x+1), v2(fmf_sem(x)[1]))
G01={(2,2),(3,2)}
# Theorem A (unified + three cases)
for x in list(range(1,200001,2))+[random.randrange(1,2**200)|1 for _ in range(5000)]+[2**k-1 for k in range(1,300)]:
    s=v2(x+1); m=(x+1)>>s
    k,f=fmf_sem(x)
    assert k==2*s-1 and f==2*(3**s*m-1), x
    if x%4==1: assert k==1 and f==4*(3*(x//4)+1)
    else:
        kk=x//4
        if kk%2==0: assert k==3 and f==4*(9*(kk//2)+4)
        else:
            t=v2(kk+1); mm=(kk+1)>>t; assert k==3+2*t and f==2*(3**(t+2)*mm-1)
# letters <-> residues, hop formulas
for x in range(1,400001,2):
    l=letter(x)
    assert (l==(2,2))==(x%16==11) and (l==(3,2))==(x%32==7)
    if l==(2,2): assert 8*hop(x)==9*x+5
    if l==(3,2): assert 16*hop(x)==27*x+19
    if l in G01: assert hop(x)%3==1
# return partial map T, as in paper section 6, vs. real FMF dynamics
def T(n):
    y=33*n+32; r4=v2(y)
    out=[]
    for r in range(0, r4//4+1):
        w=y//16**r
        if y==16**r*w and w%8==(7 if r%2==0 else 5):
            num=3*27**r*w-85
            assert num%88==0 and num>0, (n,r)   # exactness claim
            out.append((r,w,num//88))
    assert len(out)<=1
    return out[0] if out else None
cnt=0; bad=0
for n in range(0,3000000):
    t=T(n)
    x=96*n+91
    assert letter(x)==(2,2)
    # real dynamics: follow hops while letters stay in G01, find next depth-0 state of normal form
    y=hop(x); r=0; ok=True
    while True:
        l=letter(y)
        if l==(2,2): break
        if l==(3,2): y=hop(y); r+=1; continue
        ok=False; break
    if ok and y%96!=91: ok=False   # next depth-0 state must itself continue (m = 7 mod 8)
    if t is None:
        # no gate: then real dynamics must not return to a normal-form depth-0 state via 1^r
        if ok: bad+=1
    else:
        rr,w,n2=t; cnt+=1
        assert ok and r==rr and y==96*n2+91, (n,t,r,y)
        assert 88*16**rr*n2+85*16**rr==3*27**rr*(33*n+32)
        assert 8*16**rr*(33*n2+32)==9*27**rr*(33*n+32)+16**rr
print("gate hits",cnt,"non-gate returns",bad)
assert T(0) is None
# x0=1 sanity
assert hop(1)==1 and letter(1)==(1,2)
# Lemma P identity
for m in range(1,100000):
    if (27*m+1)%16==0:
        m2=(27*m+1)//16; assert 16*(11*m2+1)==27*(11*m+1)
# examples for Lean
for x in [1,3,7,27,91,103,187,859,763]:
    print(x, fmf_sem(x), hop(x), letter(x))
for n in [7,15,16,163,0,1]:
    print("T",n,T(n))
print("ALL OK")
