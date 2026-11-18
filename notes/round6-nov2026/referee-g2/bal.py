# referee-g2: exact DP test of (BAL). Walk S_j = a_j*log2(3) - j, bits iid Bernoulli(theta0).
# ratio(u,h,L) = P(min_{1<=j<=L} S_j > -u, S_L+u in [h,h+1)) * L^1.5 / ((u+1)(h+1))
import numpy as np, math, sys
th=math.log(2)/math.log(3); l3=math.log2(3)
Lmax=int(sys.argv[1]) if len(sys.argv)>1 else 4000
marks=[50,100,200,400,800,1600,2400,3200,4000]
marks=[x for x in marks if x<=Lmax]
glob=0
for u in (0.0,0.3,1.0,2.0,3.0,5.0,10.0,20.0,40.0,80.0,160.0):
    p=np.zeros(Lmax+2); p[0]=1.0
    a=np.arange(Lmax+2)
    row=[]
    for j in range(1,Lmax+1):
        q=np.empty_like(p); q[0]=p[0]*(1-th); q[1:]=p[1:]*(1-th)+p[:-1]*th
        q[a*l3-j<=-u]=0.0
        p=q
        if j in marks:
            S=a*l3-j+u
            hb=np.floor(S).astype(int); ok=p>0
            agg=np.bincount(hb[ok],weights=p[ok])
            hh=np.arange(len(agg))
            r=agg*j**1.5/((u+1)*(hh+1))
            k=int(np.argmax(r)); row.append("%.3f@h=%d"%(r[k],k)); glob=max(glob,r[k])
    print("u=%6.1f "%u+" ".join(row),flush=True)
print("L marks",marks); print("sup ratio",glob)
