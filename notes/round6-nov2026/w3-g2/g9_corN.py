# g9_corN.py -- exact N(L,m,s) = #{y in [2^L,2^(L+1)) : T^(L+m)(y) > y/2^s} against the independence prediction (w3-g2)
import numpy as np, math
from math import comb
th=math.log(2)/math.log(3)
def exact(L,ms,s):
    y=np.arange(1<<L,1<<(L+1),dtype=np.uint64); x=y.copy(); a=np.zeros(len(y),dtype=np.int16); res={}; aL=None
    for j in range(1,L+max(ms)+1):
        odd=(x&1).astype(bool); a+=odd
        x=np.where(odd,(3*x+1)>>1,x>>1)
        if j==L: aL=a.copy()
        if j-L in ms: res[j-L]=(int(np.count_nonzero(x>(y>>s))), x.copy())
    return res,aL,y
def indep(L,m,s,aL,y):
    # prediction: keep the true first generation (a, y), draw the m second-generation parities i.i.d. fair,
    # criterion 3^(a+w) y / 2^(L+m) > y/2^s  <=>  (a+w) log2 3 > L+m-s
    cnt=np.bincount(aL,minlength=L+1); tot=0.0
    for a in range(L+1):
        if cnt[a]==0: continue
        need=math.floor((L+m-s)*th-a)+1
        p=sum(comb(m,w) for w in range(max(need,0),m+1))/2**m if need<=m else 0.0
        tot+=cnt[a]*p
    return tot
for L in (20,24):
    for s in (0,3):
        ms=(0,2,4,8,12,16)
        res,aL,y=exact(L,ms,s)
        print("L=%d s=%d :"%(L,s)," ".join("m=%d %d/%.0f(%.3f)"%(m,res[m][0],indep(L,m,s,aL,y),res[m][0]/indep(L,m,s,aL,y)) for m in ms))
