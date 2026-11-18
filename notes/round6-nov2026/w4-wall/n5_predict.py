"""n5_predict.py -- first-passage prediction for the adversarial exponent:
 |T_k(3^n)| ~ max over (A,B), 2A+3B=n, of C(A+B,A)*sqrt(N_{k-3A-4B})  (coherent head, square-root tail).
 delta_pred(nu) = 1 - max/(s k), n = nu k.   usage: python n5_predict.py [mult]"""
import math,sys
mult=float(sys.argv[1]) if len(sys.argv)>1 else 3
s=0.2877607871468
H=lambda p: 0 if p in (0,1) else -(p*math.log2(p)+(1-p)*math.log2(1-p))
def pred(nu):
    best=-1e9
    for t in range(0,100001):
        f=t/100000          # fraction of a-letters
        L=nu/(2*f+3*(1-f))   # letters per k
        Q=L*(3*f+4*(1-f))
        if Q>1: continue
        best=max(best,L*H(f)+0.5*s*(1-Q))
    return 1-best/s
numax=1/math.log2(mult)
for nu in (0.1,0.2,0.3,0.4,0.5,0.55,0.6,numax):
    print("mult=%g n/k=%.4f predicted delta=%.4f"%(mult,nu,pred(nu)))
