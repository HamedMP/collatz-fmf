"""Kill test for Lemma C: distinct F and F^2 images of doubly-bad x versus the number N_2 of doubly-bad x.
usage: python lemmaC_test.py 14 24"""
import sys, numpy as np
from math import log2
def F(x):
    L=x.bit_length()-1
    for _ in range(L): x = x>>1 if not x&1 else (3*x+1)>>1
    return x
for L in range(int(sys.argv[1]),int(sys.argv[2])+1):
    x=np.arange(1<<L,1<<(L+1),dtype=np.uint64); y=x.copy()
    for _ in range(L):
        odd=(y&np.uint64(1)).astype(bool)
        y=np.where(odd,(np.uint64(3)*y+np.uint64(1))>>np.uint64(1),y>>np.uint64(1))
    ys=[int(v) for v in y[y>=x]]
    cache={}
    n2=0; im1=set(); im2=set()
    for v in ys:
        if v not in cache: cache[v]=F(v)
        w=cache[v]
        if w>=v: n2+=1; im1.add(v); im2.add(w)
    print("L=%d N2=%d distinct F(x)=%d (%.3f) distinct F^2(x)=%d (%.3f)  log2/L: %.4f %.4f %.4f"%(L,n2,len(im1),len(im1)/n2,len(im2),len(im2)/n2,log2(n2)/L,log2(len(im1))/L,log2(len(im2))/L),flush=True)
