"""Distinct F-images: |F(level L)|/2^L and |F(bad_L)|/|bad_L|.  usage: python fimage.py 12 24"""
import sys, numpy as np
for L in range(int(sys.argv[1]),int(sys.argv[2])+1):
    x=np.arange(1<<L,1<<(L+1),dtype=np.uint64); y=x.copy()
    for _ in range(L):
        odd=(y&np.uint64(1)).astype(bool)
        y=np.where(odd,(np.uint64(3)*y+np.uint64(1))>>np.uint64(1),y>>np.uint64(1))
    bad=y>=x
    print("L=%d  distinct F / 2^L = %.4f   bad=%d  distinct F(bad)/bad = %.4f"%(L,len(np.unique(y))/(1<<L),bad.sum(),len(np.unique(y[bad]))/bad.sum()),flush=True)
