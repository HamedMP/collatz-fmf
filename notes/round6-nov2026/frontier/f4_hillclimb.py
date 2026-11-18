"""Hill-climb primitive morphisms on K letters to maximise the weighted early-repetition constant iota(phi).
If iota(phi) > T0 = 4/(3 log2(3) - 4) = 5.2997 can be reached, the factor-recurrence barrier cannot exclude
that fixed point (obstruction witness).  Floats: exploration only."""
import random, sys, numpy as np
from f3_lemma_and_search import iota
K=int(sys.argv[1]); seed=int(sys.argv[2]); iters=int(sys.argv[3]); maxlen=int(sys.argv[4])
random.seed(seed)
def rand_phi():
    phi=[]
    for x in range(K):
        L=random.randrange(1,maxlen+1); img=[random.randrange(K) for _ in range(L)]
        if x==0:
            img[0]=0
            if L==1: img.append(random.randrange(1,K))
        phi.append(img)
    return phi
def mutate(phi):
    phi=[list(p) for p in phi]; x=random.randrange(K); p=phi[x]; t=random.random()
    if t<0.4 and len(p)>(2 if x==0 else 1): del p[random.randrange(1 if x==0 else 0,len(p))]
    elif t<0.7 and len(p)<maxlen: p.insert(random.randrange(1 if x==0 else 0,len(p)+1),random.randrange(K))
    else:
        i=random.randrange(1 if x==0 else 0,len(p)) if len(p)>(1 if x==0 else 0) else None
        if i is not None: p[i]=random.randrange(K)
    return phi
def score(phi):
    r=iota(phi,K,N=500,Ls=range(1,50))
    return -1 if r is None else r[0]
best=None; bs=-1
for restart in range(max(1,iters//1500)):
    cur=rand_phi(); cs=score(cur)
    for it in range(1500):
        nxt=mutate(cur); ns=score(nxt)
        if ns>=cs: cur,cs=nxt,ns
        if cs>bs: bs,best=cs,cur
r=iota(best,K,N=6000,Ls=list(range(1,80))+list(range(80,900,5)))
print("K=%d best screen %.4f refined(N=6000) %.4f at %s phi=%s l=%s"%(K,bs,r[0],r[1],[''.join(map(str,p)) for p in best],np.round(r[2],3)),flush=True)
