# referee brute force: hop = Syracuse^s, telescoped identity, tuple hypotheses, all subsums
import sys
from math import gcd, log2
def v2(n): return (n & -n).bit_length()-1
def hop(x):
    y=x+1; s=v2(y); m=y>>s
    w=3**s*m-1; a=v2(w); return w>>a, s, a, m   # a=v-1
def syr(x):
    n=3*x+1; a=v2(n); return n>>a, a
def check(x0, K=(1,2,3), syrcheck=True):
    # orbit
    xs=[x0]; ss=[]; hs=[]; ms=[]
    for i in range(max(K)+1):
        x1,s,a,m=hop(xs[-1]); ss.append(s); hs.append(s+a); ms.append(m)
        if syrcheck and i<max(K):
            z=xs[-1]; tot=0
            for j in range(s):
                z,d=syr(z); tot+=d
                assert (d==1) == (j<s-1) or (j==s-1 and d>=2), (x0,i,j,d)
            assert z==x1 and tot==s+a and a>=1 and x1%2==1, (x0,i)
        xs.append(x1)
    out={}
    for k in K:
        S=[0]; H=[0]
        for i in range(k): S.append(S[-1]+ss[i]); H.append(H[-1]+hs[i])
        Sk=S[k]; Hk=H[k]; T=Hk+ss[k]; s0=ss[0]
        # my own telescoped identity
        lhs=(xs[k]+1)<<Hk
        rhs=3**Sk*(x0+1)+sum(3**(Sk-S[i+1])*((1<<H[i+1])-(1<<(H[i]+ss[i]))) for i in range(k))
        assert lhs==rhs,(x0,k)
        tup=[(1<<(T-s0))*ms[k], -3**Sk*ms[0]]
        for i in range(k):
            assert H[i+1]-s0>=0 and H[i]+ss[i]-s0>=0
            sg=3**(Sk-S[i+1])
            tup.append(-sg<<(H[i+1]-s0)); tup.append(sg<<(H[i]+ss[i]-s0))
        assert sum(tup)==0 and all(tup), (x0,k,'sum')
        g=0
        for e in tup: g=gcd(g,e)
        assert g==1,(x0,k,'gcd',tup)
        sums=[0]
        for e in tup: sums+=[t+e for t in sums]
        assert sums.count(0)==2,(x0,k,'SUBSUM',tup)
        # (12) lhs
        prod=1
        for e in tup:
            e=abs(e)
            e>>=v2(e)
            while e%3==0: e//=3
            prod*=e
        assert prod<=ms[0]*ms[k]
        nrm=max(abs(e) for e in tup); assert nrm>=(1<<(T-s0))*ms[k]
        # Lemma 3, S_k<=T-k-1, trivial bound
        assert lhs<=2**k*3**Sk*(x0+1) and Sk<=T-k-1
        out[k]=(T, log2(x0+1), log2(prod)/log2(nrm) if nrm>1 else 9.0)
    return out
if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    best={k:(-1,0) for k in (1,2,3)}; bestr={k:(0,0) for k in (1,2,3)}; mind={k:(9,0) for k in (1,2,3)}
    n=0
    for x0 in range(lo|1,hi,2):
        o=check(x0); n+=1
        for k,(T,L,d) in o.items():
            if T-L>best[k][0]: best[k]=(T-L,x0)
            if x0>1000 and T/L>bestr[k][0]: bestr[k]=(T/L,x0)
            if d<mind[k][0]: mind[k]=(d,x0)
    print(lo,hi,'n',n,'all asserts passed'); print('max T-L0',best); print('max T/L0 (x0>1000)',bestr); print('min log(prod)/log||x||',mind)
