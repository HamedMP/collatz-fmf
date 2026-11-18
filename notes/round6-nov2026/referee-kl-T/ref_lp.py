# Referee LP: rows L1-L3 as stated, c>=1, aux d(r)<=c(r+t*3^(k-1)).  Generalised to map (p n + dd)/2 optional.
import sys, json, numpy as np
from scipy.optimize import linprog
def build(k, g, lift=None):
    # lift: modulus step for the min (default 3^(k-1)); returns A_ub, b_ub, index
    N=3**k; Nl=3**(k-1)
    ms=[m for m in range(N) if m%3==2]; idx={m:i for i,m in enumerate(ms)}
    rs=[r for r in range(Nl) if r%3==2]; ridx={r:len(ms)+i for i,r in enumerate(rs)}
    nv=len(ms)+len(rs)+1  # last = M
    A=[];b=[]
    for m in ms:
        row=np.zeros(nv); row[idx[m]]+=1; row[idx[4*m%N]]-=4.0**(-g)
        if m%9==2:
            r=((4*m-2)//3)%Nl; assert (4*m-2)%3==0 and r%3==2; row[ridx[r]]-=0.75**g
        elif m%9==8:
            r=((2*m-1)//3)%Nl; assert (2*m-1)%3==0 and r%3==2; row[ridx[r]]-=1.5**g
        A.append(row); b.append(0)
        row=np.zeros(nv); row[idx[m]]=1; row[-1]=-1; A.append(row); b.append(0)
    for r in rs:
        for t in range(3):
            row=np.zeros(nv); row[ridx[r]]=1; row[idx[r+t*Nl]]-=1; A.append(row); b.append(0)
    return np.array(A),np.array(b),ms,idx,nv
def solve(k,g,obj=None):
    A,b,ms,idx,nv=build(k,g)
    c=np.zeros(nv); 
    if obj is None: c[-1]=1
    else: c[:len(ms)]=obj; 
    bounds=[(1,None)]*len(ms)+[(0,None)]*(nv-len(ms)-1)+[(1,1e6 if obj is not None else None)]
    res=linprog(c,A_ub=A,b_ub=b,bounds=bounds,method='highs')
    if res.status!=0: return None
    return {m:res.x[idx[m]] for m in ms}
def opt(k,lo=0.3,hi=1.5):
    for _ in range(40):
        mid=(lo+hi)/2
        if solve(k,mid) is not None: lo=mid
        else: hi=mid
    return lo
def check(k,g,c,tol=0):
    N=3**k;Nl=3**(k-1); worst=1e9
    cb=lambda r: min(c[(r+t*Nl)%N] for t in range(3))
    for m in c:
        rhs=4.0**(-g)*c[4*m%N]
        if m%9==2: rhs+=0.75**g*cb(((4*m-2)//3)%Nl)
        if m%9==8: rhs+=1.5**g*cb(((2*m-1)//3)%Nl)
        worst=min(worst,rhs-c[m])
    return worst
if __name__=="__main__":
    out={}
    for k in (2,3,4):
        go=opt(k); print("k",k,"gamma_opt",go, "feasible at 1.0001?",solve(k,1.0001) is not None,"at 1.0?",solve(k,1.0) is not None, "at 1.05?", solve(k,1.05) is not None)
        vecs=[]
        rng=np.random.default_rng(k)
        for g in (go-1e-4, go-0.02, 0.7*go, 0.3*go):
            c=solve(k,g); vecs.append((g,c)); print("  g",g,"M",max(c.values()),"min",min(c.values()),"slack",check(k,g,c))
            for j in range(3):
                n=len(c); c2=solve(k,g,obj=-rng.random(n)*(rng.random(n)<0.5))
                if c2: vecs.append((g,c2)); print("   rand vertex M",max(c2.values()),"slack",check(k,g,c2))
        out[k]=[(g,{str(m):v for m,v in c.items()}) for g,c in vecs]
    json.dump(out,open("weights.json","w"))
