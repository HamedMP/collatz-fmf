# referee-g2: exact re-derivation tests of (I1)-(I3) for all vectors, L<=Lmax, and of the pairing identity (Step 2).
import sys, math, cmath, itertools
from collections import defaultdict
Lmax=int(sys.argv[1]) if len(sys.argv)>1 else 16
def run(L):
    nv=0; comps={}
    for y in range(1<<L,1<<(L+1)):
        x=y; d=[]
        for j in range(L):
            if x&1: d.append(j); x=(3*x+1)>>1
            else: x>>=1
        a=len(d); z=x
        if a==0: continue
        tau=z-3**a; M=3**a
        assert 0<=tau<M, ("tau range",L,y)
        al=[L-d[a-1]]+[d[a-j+1]-d[a-j] for j in range(2,a+1)]+[d[0]+1]
        assert min(al)>=1 and sum(al)==L+1 and len(al)==a+1
        key=(a,tuple(al)); assert key not in comps; comps[key]=1      # I1 injective
        s=0; acc=0
        for j in range(1,a+1):
            acc+=al[j-1]; s+=3**(j-1)*pow(2,-acc,M)
        assert (s-tau)%M==0, ("I2",L,y)
        for m in (0,1,2,5,L//2,L,L+3):
            sig=(tau*pow(2,-m,M))%M; c=(sig<<m)//M
            assert (sig<<m)==tau+c*M and 0<=c<(1<<m) and (z-(1-c)*M)%(1<<m)==0, ("I3",L,y,m)
        nv+=1
    # I1 surjective: count compositions
    cnt=defaultdict(int)
    for (a,al) in comps: cnt[a]+=1
    for a,cn in cnt.items(): assert cn==math.comb(L,a)==math.comb(L,a)  # compositions of L+1 into a+1 parts = C(L,a)
    return nv
tot=0
for L in range(1,Lmax+1): tot+=run(L)
print("I1-I3 and 0<=tau<3^a OK on",tot,"vectors, L<=",Lmax)

# pairing identity: uniform on V(L,a); sigma = tau*2^-m mod 3^a; h=3^i h'; n=a-i.
def e(x): return cmath.exp(2j*math.pi*x)
def sfrac(x): 
    x=x-math.floor(x); return x-1 if x>0.5 else x
def pairing(L,a,m,h):
    i=0; hp=h
    while hp%3==0: hp//=3; i+=1
    n=a-i; M=3**a; Mn=3**n; half=n//2
    groups=defaultdict(list)
    for ones in itertools.combinations(range(L),a):
        d=ones
        al=[L-d[a-1]]+[d[a-j+1]-d[a-j] for j in range(2,a+1)]+[d[0]+1]
        s=0; acc=0
        for j in range(1,a+1):
            acc+=al[j-1]; s+=3**(j-1)*pow(2,-acc,M)
        tau=s%M; sig=(tau*pow(2,-m,M))%M
        b=tuple(al[2*j]+al[2*j+1] for j in range(half))
        G=(b,tuple(al[2*half:]))
        groups[G].append((e(h*sig/M),tuple(al[2*j+1] for j in range(half))))
    worst=0; worst_cos=0; nb3=0
    for (b,rest),lst in groups.items():
        # uniformity of alpha_2j given G
        assert len(lst)==math.prod(x-1 for x in b)
        assert len(set(x[1] for x in lst))==len(lst)
        cond=abs(sum(x[0] for x in lst))/len(lst)
        prod=1.0; bs=0
        for j in range(1,half+1):
            bs+=b[j-1]; l=m+bs
            base=hp*3**(2*j-2)*pow(2,-l,Mn)
            f=sum(e(((base*(2**k+3))%Mn)/Mn) for k in range(1,b[j-1]))/(b[j-1]-1)
            prod*=abs(f)
            if b[j-1]==3:
                theta=sfrac(((hp*3**(2*j-2)*pow(2,-l+1,Mn))%Mn)/Mn)
                worst_cos=max(worst_cos,abs(abs(f)-abs(math.cos(math.pi*theta)))); nb3+=1
        worst=max(worst,abs(cond-prod))
    return len(groups),worst,worst_cos,nb3
for (L,a,m,h) in [(12,7,0,1),(12,7,3,5),(14,9,2,7),(14,9,4,6),(15,9,5,9),(16,10,3,11),(16,10,7,18),(16,11,1,2)]:
    g,w,wc,nb=pairing(L,a,m,h)
    print("L=%d a=%d m=%d h=%d: groups=%d  max| |E[chi|G]| - prod|f_j| | = %.2e   max||f_j|-|cos(pi theta)|| over %d pairs with b=3 = %.2e"%(L,a,m,h,g,w,nb,wc))
