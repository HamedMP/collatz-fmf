# g7_fit.py -- table of E_lambda, model ratio and exponents (w3-g2)
import math, subprocess, sys, glob, collections
from g2_model import model
eta=0.9499555274
lams=(1,1.25,1.5,2,3,4,8)
def load(L):
    fs=sorted(glob.glob("g1_L%d.log"%L)+glob.glob("g1_L%d_p*.log"%L))
    h=collections.Counter()
    for f in fs:
        for line in open(f):
            w=line.split()
            if w and w[0]=='D': h[int(w[1])]+=int(w[2])
    return [sum(c for d,c in h.items() if d>int(l*L)) for l in lams]
Ls=[int(x) for x in sys.argv[1:]]
E={L:load(L) for L in Ls}; Mo={L:model(L,lams) for L in Ls}
print("lambda            "+"  ".join("%10s"%l for l in lams))
for L in Ls:
    print("L=%d E          "%L+"  ".join("%10d"%x for x in E[L]))
    print("L=%d E/model    "%L+"  ".join("%10.4f"%(x/m) for x,m in zip(E[L],Mo[L])))
    print("L=%d z-score    "%L+"  ".join("%10.2f"%((x-m)/math.sqrt(m)) for x,m in zip(E[L],Mo[L])))
for i in range(len(Ls)-1):
    L1,L2=Ls[i],Ls[i+1]
    print("local exp %d->%d  "%(L1,L2)+"  ".join("%10.4f"%(math.log2(E[L2][k]/E[L1][k])/(L2-L1)) if E[L1][k]>0 else "         -" for k in range(len(lams))))
    print(" +1.5*log2 corr    "+"  ".join("%10.4f"%((math.log2(E[L2][k]/E[L1][k])+1.5*math.log2(L2/L1))/(L2-L1)) if E[L1][k]>0 else "         -" for k in range(len(lams))))
print("predicted 1-lam(1-eta)"+"  ".join("%8.4f"%(1-l*(1-eta)) for l in lams))
# model exponents at large L (pure model, shows convergence of the corrected local exponent)
for (L1,L2) in ((60,64),(120,128),(240,256)):
    m1=model(L1,lams,256); m2=model(L2,lams,256)
    print("model corrected exp %d->%d "%(L1,L2)+"  ".join("%8.4f"%((math.log2(b/a)+1.5*math.log2(L2/L1))/(L2-L1)) for a,b in zip(m1,m2)))
