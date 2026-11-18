# Exhaustive test of Lemma G as stated, by exact enumeration of the backward tree of T.
# For 3∤m, m<=200, d<=8, 4d<=k<=4d+6: exists n, T^k(n)=m, exactly d odd steps, 2^k m/3^d - 2^(k-d) < n <= 2^k m/3^d.
# Also: is the hypothesis k>=4d needed? report smallest k (per d) for which conclusion holds for all m.
import sys
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def levels(m,dmax,kmax):
    # S[k][d] = set of n with T^k(n)=m and exactly d odd steps
    S=[[set() for _ in range(dmax+1)] for _ in range(kmax+1)]
    S[0][0].add(m)
    for k in range(kmax):
        for d in range(dmax+1):
            for n in S[k][d]:
                S[k+1][d].add(2*n)
                if d<dmax and (2*n-1)%3==0:
                    p=(2*n-1)//3
                    if p%2==1 and p>0: S[k+1][d+1].add(p)
    return S
DM=8;KM=4*DM+6
fail=0;tests=0
need=[0]*(DM+1)   # largest k<4d at which conclusion fails for some m
failbelow={}
for m in range(1,201):
    if m%3==0: continue
    S=levels(m,DM,KM)
    for d in range(DM+1):
        for k in range(d,min(KM,4*d+6)+1):
            lo_num=(1<<k)*m-(1<<(k-d))*3**d   # n*3^d > lo_num
            hi_num=(1<<k)*m
            ok=any(lo_num< n*3**d <=hi_num for n in S[k][d])
            if k>=4*d:
                tests+=1
                if not ok: fail+=1; print("FAIL",m,d,k)
            elif not ok:
                need[d]=max(need[d],k); failbelow[(d,k)]=failbelow.get((d,k),0)+1
# sanity of the tree: forward check on a sample
S=levels(7,DM,20)
for k in (5,12,20):
    for d in range(DM+1):
        for n in S[k][d]:
            x=n;o=0
            for _ in range(k): o+=x&1; x=T(x)
            assert x==7 and o==d
print("Lemma G: tests",tests,"failures",fail)
print("largest k<4d where conclusion FAILS for some m<=200, per d:",need)
# 3|m: conclusion fails for d>=1?
S=levels(3,3,14); print("m=3 d=1 sets nonempty?",any(S[k][1] for k in range(15)))
