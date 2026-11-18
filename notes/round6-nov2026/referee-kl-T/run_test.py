import json,subprocess,sys
import os
P,D=int(os.environ.get("P",3)),int(os.environ.get("D",1))
X,amax=int(sys.argv[1]),int(sys.argv[2]); ares=int(sys.argv[3]) if len(sys.argv)>3 else 2
W=json.load(open("weights.json"))
gs=sorted({g for k in W for g,_ in W[k]})
cmd=["taskset","-c","0-1","./ref_pistar",str(P),str(D),str(X),"1",str(amax),"3",str(ares)]+[repr(g) for g in gs]
out=subprocess.run(cmd,capture_output=True,text=True).stdout.split("\n")
rows={}
for l in out:
    f=l.split()
    if not f: continue
    a=int(f[0]); rows[a]=(int(f[1]),[ (float(f[2+4*i]),int(f[3+4*i]),float(f[4+4*i]),int(f[5+4*i])) for i in range(len(gs))])
# cycle detection for a
def oncycle(a):
    n=a
    for _ in range(10000):
        n=n//2 if n%2==0 else (P*n+D)//2
        if n==a: return True
        if n in (1,2) and a not in (1,2): return False
    return False
tot=sum(r[0] for r in rows.values()); print("a count",len(rows),"total tree nodes",tot)
for k in W:
    N=3**int(k)
    for g,c in W[k]:
        gi=gs.index(g); M=max(c.values())
        best=(1e300,);bestj=(1e300,); cyc=[]
        for a,(n,r) in rows.items():
            inf,x,atj,xj=r[gi]; fac=4**g*M/c[str(a%N)]
            if oncycle(a): cyc.append((a,inf*fac,x,atj*fac,xj)); continue
            if inf*fac<best[0]: best=(inf*fac,a,x)
            if atj*fac<bestj[0]: bestj=(atj*fac,a,xj)
        print(f"k={k} g={g:.6f} M={M:.4g}: min ratio(left-limit) {best[0]:.6f} at a={best[1]} x->{best[2]}^- ; min at-jump {bestj[0]:.6f} at a={bestj[1]} x={bestj[2]} ; cycle a: {[(a,round(v,4),x) for a,v,x,_,_ in cyc]}")
