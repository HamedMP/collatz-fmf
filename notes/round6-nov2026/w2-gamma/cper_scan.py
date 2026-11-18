"""Scan of the class C_per: S = T + g on odd n, g periodic mod 16, 2-adically 1-Lipschitz, |g|<=8, S(N) in N.
For each such g: iterate all starts n<=3000; report number of maps, how many have nontrivial extra cycles,
and whether any orbit exceeds 2^400 (divergence suspect)."""
import itertools
def v2(n): return (n&-n).bit_length()-1
odds=[1,3,5,7,9,11,13,15]
maps=[]
def rec(i,g):
    if i==8: maps.append(tuple(g)); return
    x=odds[i]
    for val in range(-8,9):
        if all((val-g[j])%(1<<v2(x-odds[j]))==0 for j in range(i)):
            # positivity of S on the class: smallest element x: (3x+1)/2+val>=1
            if (3*x+1)//2+val>=1:
                g.append(val); rec(i+1,g); g.pop()
rec(0,[])
print("number of maps g (mod 16, |g|<=8, 1-Lipschitz, positive):", len(maps))
suspects=[]; ncyc_hist={}
for g in maps:
    G={o:g[i] for i,o in enumerate(odds)}
    def S(n): return n>>1 if n&1==0 else ((3*n+1)>>1)+G[n&15]
    cyc=set(); done={}
    for n in range(1,3001):
        x=n; path=[]
        while x not in done and x.bit_length()<400:
            done[x]=-1; path.append(x); x=S(x)
        if x.bit_length()>=400: suspects.append((g,n)); lab=None
        elif done[x]==-1:
            # new cycle (x is on the current path)
            c=[x]; y=S(x)
            while y!=x: c.append(y); y=S(y)
            lab=min(c); cyc.add(lab)
        else: lab=done[x]
        for p in path: done[p]=lab if lab is not None else -2
    ncyc_hist[len(cyc)]=ncyc_hist.get(len(cyc),0)+1
print("histogram {number of distinct cycles reached from n<=3000: number of maps}:", dict(sorted(ncyc_hist.items())))
print("maps with an orbit exceeding 2^400:", len(set(s[0] for s in suspects)), suspects[:5])
