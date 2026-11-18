# g2_model.py -- "independent generations" random-walk model for E_lambda(2^L)  (w3-g2)
# Model: y uniform in [2^L, 2^(L+1)), parities i.i.d. fair for ALL steps, T^j(y) ~ y*3^a/2^j.
# survive to J  <=>  a_j*log2(3) - j >= -1 - log2(y/2^L)  for all j <= J.
# For J <= L this is exact up to the +1 terms (Terras); for J > L it is the tilted-independence heuristic.
import numpy as np, math, sys
l3=math.log2(3)
def model(L, lams, NY=2048):
    Js=[int(l*L) for l in lams]; JM=max(Js)
    us=np.log2(1+(np.arange(NY)+0.5)/NY)          # y/2^L = 1+(i+.5)/NY
    # P[i,a] mass
    P=np.zeros((NY,JM+2)); P[:,0]=1.0
    res={}
    a=np.arange(JM+2)
    for j in range(1,JM+1):
        Q=0.5*P; Q[:,1:]+=0.5*P[:,:-1]
        alive=(a[None,:]*l3 - j >= -1-us[:,None])
        P=Q*alive
        if j in Js: res[j]=P.sum()/NY*2.0**L
    return [res[J] for J in Js]
if __name__=="__main__":
    lams=(1,1.25,1.5,2,3,4,8)
    for L in map(int,sys.argv[1:]):
        print(L,*["%.6g"%x for x in model(L,lams)])
