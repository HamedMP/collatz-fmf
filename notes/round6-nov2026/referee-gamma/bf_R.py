# Brute-force finite Theorem R by backtracking. Written BEFORE reading the proofs.
import sys
def v2(m):
    m=abs(m); c=0
    while m%2==0: m//=2; c+=1
    return c
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def rng(n,mode):
    if n%2==0: return range(1,n)            # (II)
    if mode=='III': return range(n+1,2*n+1)
    if mode=='2n+1': return range(n+1,2*n+2)
    if mode=='n<=S': return range(n,2*n+1)
    if mode=='n<=S<=2n+1': return range(n,2*n+2)
    if mode=='noupper': return range(n+1,4*n+1)
def count(N,mode,limit=10**6,show=3):
    S=[0]*(N+1); sols=[0]; ex=[]
    def ok(n,s):
        for m in range(n-2,0,-2):
            d=s-S[m]
            if d==0 or v2(d)!=v2(n-m)-1: return False
        return True
    def rec(n):
        if sols[0]>=limit: return
        if n>N:
            sols[0]+=1
            if any(S[i]!=T(i) for i in range(1,N+1)) and len(ex)<show: ex.append(S[1:])
            return
        for s in rng(n,mode):
            if ok(n,s):
                S[n]=s; rec(n+1)
    rec(1); return sols[0],ex
for mode in ['III','2n+1','n<=S','n<=S<=2n+1','noupper']:
    for N in [4,8,12,16,20,24,32,40,48,64]:
        c,ex=count(N,mode)
        print(mode,N,c, 'nonT example:' if ex else '', [ [ (i+1,e[i],T(i+1)) for i in range(len(e)) if e[i]!=T(i+1)] for e in ex[:2]],flush=True)
        if c>=10**6: break
