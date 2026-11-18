# g8_critical.py -- dead end 1: at the critical slope one triangle can cover the whole diagonal (w3-g2)
# xi = 2^l0 mod 3^n, l0 = round(n log2 3 + K sqrt(n)).  White fraction of renewal points (b_j=3) on
# (i) pinned critical paths (mean valuation log2 3) and (ii) i.i.d. Geom(1/2) paths (Tao's case, mean 2).
import random, math
random.seed(7); l3=math.log2(3); eps=0.05
def theta(h,j,l,P):
    x=h*pow(9,j-1,P)*pow(2,-(l-1),P)%P
    if 2*x>P: x-=P
    return x/P
def comp(total,parts):
    cuts=[0]+sorted(random.sample(range(1,total),parts-1))+[total]
    return [cuts[i+1]-cuts[i] for i in range(parts)]
def geo(): 
    k=1
    while random.random()<0.5: k+=1
    return k
print("n  K  white-fraction(pinned critical)  white-fraction(iid Geom(1/2))   [generic xi=1 gives ~0.90]")
for n in (200,800):
    P=3**n; L=round(n*l3)
    for K in (-2,0,2,4):
        l0=round(n*l3+K*math.sqrt(n)); h=pow(2,l0,P)
        out=[]
        for mode in (0,1):
            w=tot=0
            for it in range(40):
                al=comp(L+1,n+1) if mode==0 else [geo() for _ in range(n)]
                s=0
                for j in range(1,n//2+1):
                    b=al[2*j-2]+al[2*j-1]; s+=b
                    if b==3: tot+=1; w+=abs(theta(h,j,s,P))>eps
            out.append(w/tot)
        print(n,K," %.3f   %.3f"%tuple(out))
