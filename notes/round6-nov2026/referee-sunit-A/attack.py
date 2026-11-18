# attempts to build violating families + adversarial inputs
from math import log2
from brute import check, hop, v2
# adversarial
adv=[1,3,5,7,9,27,31]+[2**n-1 for n in range(1,400,7)]+[2**n*3-1 for n in range(1,300,11)]+[2**n*9-1 for n in range(1,300,13)]+[2**n*3**20-1 for n in range(1,200,17)]
# numbers with x'=1: 3^s m -1 = 2^a  -> m=(2^a+1)/3^s
for s in range(1,6):
    for a in range(1,400):
        if (2**a+1)%3**s==0:
            m=(2**a+1)//3**s
            if m%2: 
                for t in (s,):
                    adv.append(2**s*m-1)
for x in adv:
    assert x%2==1
    check(x, K=(1,2,3,4,5), syrcheck=True)
print('adversarial ok', len(adv))
# A: direct search, deep s, small m
best=[]
for k in (1,2,3):
    b=(-9,None); r=(0,None)
    for s in range(1,1500):
        for m in range(1,400,2):
            x0=(m<<s)-1
            x=x0; H=0
            for i in range(k):
                x,si,a,_=hop(x); H+=si+a
            T=H+v2(x+1); L=log2(x0+1)
            if T-L>b[0]: b=(T-L,(s,m))
            if L>60 and T/L>r[0]: r=(T/L,(s,m))
    print('k',k,'deep-s search: max T-L0',b,' max T/L0 with L0>60',r, flush=True)
# B: lattice attack k=1: smallest m with v2(3^s m -1)=a and v2(3^s m -1+2^a)>=N
worst=(0,None)
for s in range(1,400):
    inv=pow(3**s,-1,1<<600)
    for a in range(1,60):
        base=(inv*(1-(1<<a)))
        for N in range(a+2,600,1):
            m=base%(1<<N)
            if m%2==0: continue
            w=3**s*m-1
            if v2(w)!=a: continue
            T=s+v2(w+(1<<a)); L=s+log2(m)
            if L>80 and T/L>worst[0]: worst=(T/L,(s,a,N,m.bit_length(),T))
print('lattice attack k=1: max T/L0 (L0>80)',worst)
