# Referee: generic (p n + d)/2 system, own derivation.  Principal class: a with p | 2a-d. E=ord_p(2).
# row: c(m) <= 2^(-E g) c(2^E m) + [p !| b] (p/2^(j+1))^g cbar(2^j b),  b=(2m-d)/p, j min with 2^j b principal.
import sys,subprocess,numpy as np
from scipy.optimize import linprog
def system(p,d,k):
    N=p**k; Nl=p**(k-1); inv2=pow(2,-1,p); res=(d*inv2)%p
    E=1
    while pow(2,E,p)!=1: E+=1
    ms=[m for m in range(N) if m%p==res]; rows=[]
    for m in ms:
        b=((2*m-d)//p)%Nl; assert (2*m-d)%p==0
        if b%p==0: rows.append((m,(pow(2,E,N)*m)%N,None,None)); continue
        j=0
        while (2**j*b)%p!=res: j+=1
        rows.append((m,(pow(2,E,N)*m)%N,(2**j*b)%Nl,j))
    return N,Nl,E,ms,rows
def solve(p,d,k,g):
    N,Nl,E,ms,rows=system(p,d,k); idx={m:i for i,m in enumerate(ms)}
    rs=sorted({r for _,_,r,_ in rows if r is not None}); ridx={r:len(ms)+i for i,r in enumerate(rs)}
    nv=len(ms)+len(rs)+1; A=[];b=[]
    for m,m2,r,j in rows:
        row=np.zeros(nv); row[idx[m]]+=1; row[idx[m2]]-=2.0**(-E*g)
        if r is not None: row[ridx[r]]-=(p/2.0**(j+1))**g
        A.append(row);b.append(0); row=np.zeros(nv); row[idx[m]]=1; row[-1]=-1; A.append(row);b.append(0)
    for r in rs:
        for t in range(p):
            row=np.zeros(nv); row[ridx[r]]=1; row[idx[r+t*Nl]]-=1; A.append(row);b.append(0)
    c=np.zeros(nv);c[-1]=1
    res=linprog(c,A_ub=np.array(A),b_ub=b,bounds=[(1,None)]*len(ms)+[(0,None)]*(nv-len(ms)),method='highs')
    return None if res.status!=0 else {m:res.x[idx[m]] for m in ms}
def opt(p,d,k):
    lo,hi=0.01,1.5
    for _ in range(36):
        mid=(lo+hi)/2
        if solve(p,d,k,mid) is not None: lo=mid
        else: hi=mid
    return lo
def T(n,p,d): return n//2 if n%2==0 else (p*n+d)//2
def oncycle(a,p,d,lim=3000):
    n=a
    for _ in range(lim):
        n=T(n,p,d)
        if n==a: return True
    return False
if __name__=="__main__":
    p,d,X,amax=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
    ks=[int(s) for s in sys.argv[5].split(",")]
    N,Nl,E,ms,rows=system(p,d,2); res=ms[0]%p
    W=[]
    for k in ks:
        go=opt(p,d,k)
        for g in (go-1e-5,0.6*go): W.append((k,g,solve(p,d,k,g)))
        print("k",k,"gamma_opt",round(go,7))
    gs=[g for _,g,_ in W]
    for XF in ("1",str(2**E),"256"):
        import os
        out=subprocess.run(["taskset","-c","0-1","./ref_pistar",str(p),str(d),str(X),"1",str(amax),str(p),str(res)]+[repr(g) for g in gs],capture_output=True,text=True,env=dict(os.environ,XF=XF)).stdout.split("\n")
        for gi,(k,g,c) in enumerate(W):
            M=max(c.values()); Nk=p**k; best=(1e300,);cyc=(1e300,)
            for l in out:
                f=l.split()
                if not f: continue
                a=int(f[0]); v=float(f[2+4*gi])*2**(E*g)*M/c[a%Nk]; x=int(f[3+4*gi])
                if oncycle(a,p,d):
                    if v<cyc[0]: cyc=(v,a,x)
                elif v<best[0]: best=(v,a,x)
            print(f"p={p} d={d} x>={XF}a k={k} g={g:.6f} M={M:.4g}: min ratio non-cycle {best}  cycle {cyc}")
