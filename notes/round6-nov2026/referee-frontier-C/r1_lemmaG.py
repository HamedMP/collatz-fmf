# Referee test of Lemma G: exact integers. x_n*2^n*(3x0)^k <= x0*3^k*(3x0+1)^k
import sys
LIM=100000; CAP=400
inst=viol=0; maxn=0
viol_nohyp=0; inst_nohyp=0
for x0 in range(1,LIM):
    x=x0; k=0; ok=True
    for n in range(0,CAP+1):
        # here x = x_n, k = k_n ; hypothesis x_j>=x0 for j<=n
        if x<x0: ok=False
        lhs=x*(1<<n)*x0**k; rhs=x0*(3*x0+1)**k
        if ok:
            inst+=1; maxn=max(maxn,n)
            if lhs>rhs: viol+=1; print("VIOL",x0,n)
        elif n<=40:
            inst_nohyp+=1
            if lhs>rhs: viol_nohyp+=1
        if not ok and n>40: break
        if x&1: x=(3*x+1)//2; k+=1
        else: x//=2
print("LemmaG: instances",inst,"violations",viol,"max n",maxn)
print("without hypothesis (n<=40): instances",inst_nohyp,"violations",viol_nohyp)
