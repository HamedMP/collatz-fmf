# g5_white.py -- sanity check of the white-point majorant under the pinned (uniform composition) measure (w3-g2)
# For frequency h' (coprime to 3), shift m, n=a: theta(j,l) = { h' 9^(j-1) (2^(-l+1) mod 3^n) / 3^n },
# white iff |theta| > eps.  Reports: mean number / fraction of white renewal points (b_j = 3) on pinned paths,
# the largest black-triangle depth  s = log(eps/|theta|)  met in the band |l - j log2 9| <= 3 sqrt(n).
import random, math
from fractions import Fraction
random.seed(1)
l3=math.log2(3)
def theta(h,j,l,n,P):
    x=h*pow(9,j-1,P)*pow(2,-(l-1),P)%P
    if 2*x>P: x-=P
    return x/P
def comp(total,parts):   # uniform composition of total into `parts` positive parts
    cuts=sorted(random.sample(range(1,total),parts-1)); cuts=[0]+cuts+[total]
    return [cuts[i+1]-cuts[i] for i in range(parts)]
eps=0.05
print("a L h m  mean#white(b=3)  frac_white  E exp(-eps^2 W)   max band depth s   (n/2)")
for a in (60,200,600,2000):
    L=round(a*l3); P=3**a
    for h in (1,5,7):
        for m in (0,4):
            ws=[];fr=[];
            for it in range(60 if a<=600 else 12):
                al=comp(L+1,a+1); s=m; w=0; tot=0
                for j in range(1,a//2+1):
                    b=al[2*j-2]+al[2*j-1]; s+=b
                    if b==3:
                        tot+=1; w+= abs(theta(h,j,s,a,P))>eps
                ws.append(w); fr.append(w/max(tot,1))
            # band scan
            smax=0
            for j in range(1,a//2+1, max(1,a//400)):
                c=round(j*2*l3)+m; wid=int(3*math.sqrt(a))
                for l in range(max(1,c-wid),c+wid+1, max(1,wid//40)):
                    t=abs(theta(h,j,l,a,P))
                    if 0<t<=eps: smax=max(smax,math.log(eps/t))
            print(a,L,h,m," %.1f  %.3f  %.3e   %.2f   (%d)"%(sum(ws)/len(ws),sum(fr)/len(fr),sum(math.exp(-eps*eps*w) for w in ws)/len(ws),smax,a//2))
