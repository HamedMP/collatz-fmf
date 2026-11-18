"""Obstruction test.  For an itinerary x in {a,b}^N the factor-recurrence barrier gives, for every repetition
(u at letter positions i<i'),   log2(w0+1) > V := B(u) - G(x[0,i')),   B = 3#a+4#b,  G = (2#a+3#b)log2(3) - B.
For each i' the best u is the longest previous factor LPF[i'] (overlaps allowed).  We compute
   Vmax(N) = max_{i'<N} V(i')   exactly-in-structure (float only in log2(3)) via suffix array + LCP.
The barrier excludes x  <=>  Vmax(N) -> infinity.
Usage: f6_obstruction_lpf.py  NLETTERS
"""
import sys, numpy as np
from math import log2
def suffix_array(s):
    n=len(s); rank=s.astype(np.int64).copy(); k=1
    sa=np.argsort(rank,kind='stable')
    while True:
        r2=np.full(n,-1,dtype=np.int64); r2[:n-k]=rank[k:]
        key=rank*(n+2)+(r2+1)
        sa=np.argsort(key,kind='stable'); ks=key[sa]
        newr=np.empty(n,dtype=np.int64); newr[sa]=np.concatenate([[0],np.cumsum(ks[1:]!=ks[:-1])])
        rank=newr
        if rank.max()==n-1: break
        k*=2
    return sa,rank
def lpf_simple(s):
    """Crochemore-Ilie style with explicit range-min, O(n) amortised."""
    n=len(s); sa,rank=suffix_array(s); sl=s.tolist(); sal=sa.tolist(); rl=rank.tolist()
    lcp=[0]*(n+1); h=0
    for i in range(n):
        if rl[i]>0:
            j=sal[rl[i]-1]
            while i+h<n and j+h<n and sl[i+h]==sl[j+h]: h+=1
            lcp[rl[i]]=h
            if h>0: h-=1
        else: h=0
    lpf=[0]*n
    # previous-smaller-index to the left in SA order, tracking min lcp along the way
    st=[]  # entries: [index, lcp_between_this_entry_and_the_entry_below_in_stack]
    for r in range(n):
        i=sal[r]; m=lcp[r]   # lcp(sa[r-1],sa[r])
        while st and st[-1][0]>i:
            m=min(m,st[-1][1]); st.pop()
        if st: lpf[i]=max(lpf[i],m)
        st.append([i,m])
    st=[]
    for r in range(n-1,-1,-1):
        i=sal[r]; m=lcp[r+1] if r+1<n else 0   # lcp(sa[r],sa[r+1])
        while st and st[-1][0]>i:
            m=min(m,st[-1][1]); st.pop()
        if st: lpf[i]=max(lpf[i],m)
        st.append([i,m])
    return lpf
def brute_lpf(sl):
    n=len(sl); out=[0]*n
    for i in range(n):
        best=0
        for j in range(i):
            h=0
            while i+h<n and sl[i+h]==sl[j+h]: h+=1
            best=max(best,h)
        out[i]=best
    return out
def fixed(phi,N):
    w=[0]
    while len(w)<N:
        nw=[]
        for x in w:
            nw.extend(phi[x])
            if len(nw)>=N: break
        w=nw
    return w[:N]
def vmax(x):
    """x: numpy array of 0 (=a) / 1 (=b). returns list of (N, Vmax(N), argmax i', LPF) at checkpoints"""
    lpf=lpf_simple(x); n=len(x); L3=log2(3)
    Bp=np.concatenate([[0],np.cumsum(3+x)]); Ep=np.concatenate([[0],np.cumsum(2+x)])
    out=[]; best=-1e18; arg=None; cp=1000
    for ip in range(1,n):
        L=lpf[ip]
        if ip+L>=n: break    # truncated by end of prefix: stop (later values unreliable)
        V=(Bp[ip+L]-Bp[ip])-(Ep[ip]*L3-Bp[ip])
        if V>best: best=V; arg=(ip,L)
        if ip+1==cp or ip==n-2:
            out.append((ip+1,round(float(best),2),arg)); cp*=4
    out.append((ip,round(float(best),2),arg))
    return out
if __name__=="__main__":
    import random
    rnd=random.Random(1)
    for _ in range(200):
        t=np.array([rnd.randrange(2) for _ in range(rnd.randrange(2,60))])
        assert lpf_simple(t)==brute_lpf(t.tolist())
    print("LPF routine matches brute force on 200 random words")
    N=int(sys.argv[1]) if len(sys.argv)>1 else 40000
    def itin(phi,blocks,N):
        y=fixed(phi,N); return np.array([c for k in y for c in blocks[k]],dtype=np.int64)
    A=[0];Bk=[1]
    cases={
     "control: Fibonacci 0->01,1->0 ; blocks a, ba": ([[0,1],[0]],[[0],[1,0]]),
     "control: binary non-uniform 0->0110, 1->11 (superlinear complexity); blocks a, ba": ([[0,1,1,0],[1,1]],[[0],[1,0]]),
     "control: Thue-Morse ; blocks a, ba": ([[0,1],[1,0]],[[0],[1,0]]),
     "WITNESS K=4: 0->0312113,1->201,2->000303302,3->301110 ; blocks b^(4+k) a": ([[0,3,1,2,1,1,3],[2,0,1],[0,0,0,3,0,3,3,0,2],[3,0,1,1,1,0]],[[1]*(4+k)+[0] for k in range(4)]),
     "WITNESS K=4 same morphism ; blocks b^(20+k) a": ([[0,3,1,2,1,1,3],[2,0,1],[0,0,0,3,0,3,3,0,2],[3,0,1,1,1,0]],[[1]*(20+k)+[0] for k in range(4)]),
    }
    for name,(phi,blocks) in cases.items():
        nl=N if 'b^(20' not in name else N//3
        x=itin(phi,blocks,nl)
        print(name,"| letters",nl,"| ab-length",len(x)); print("   (N, Vmax, (i',LPF)):",vmax(x),flush=True)
