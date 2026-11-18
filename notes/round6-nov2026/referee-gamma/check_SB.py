import numpy as np, math, random
def T(n): return n//2 if n%2==0 else (3*n+1)//2
# ---- Theorem S
M=1<<14
n=np.arange(1,M,dtype=np.int64)
Tn=np.where(n%2==0,n//2,(3*n+1)//2)
def lowbit(d): return d & -d
for a in range(0,11):
    S=Tn - (1<<a)*((n%2==1)&((n+1)%(1<<(a+1))==0))
    assert S.min()>=1
    okI=True
    for par in (0,1):
        idx=n[n%2==par]; Sv=S[idx-1]
        for i in range(len(idx)-1):
            d=idx[i+1:]-idx[i]; e=Sv[i+1:]-Sv[i]
            if (e==0).any() or not (2*lowbit(np.abs(e))==lowbit(d)).all(): okI=False;break
    ev=n%2==0; od=~ev
    II=(S[ev]<n[ev]).all()
    viol=n[od][~((S[od]>n[od])&(S[od]<=2*n[od]))]
    na=(1<<(a+1))-1
    modok=((S-Tn)%(1<<a)==0).all(); eq=(S[:na-1]==Tn[:na-1]).all()
    print(a,'I',okI,'II',II,'IIIviol',viol.tolist(),'fixed',S[na-1]==na,'modT',modok,'eqbelow',eq, 'S0=3n-1' if a==0 and (S[od]==(3*n[od]-1)//2).all() else '')
# dual family T+2^a on class: (III) upper-bound sharpness
for a in range(0,6):
    S=Tn + (1<<a)*((n%2==1)&((n+1)%(1<<(a+1))==0)); od=n%2==1
    print('dual',a,'IIIviol',n[od][~((S[od]>n[od])&(S[od]<=2*n[od]))].tolist())
# ---- Remark: parity prefixes for class 15 mod 16 under S_a
def Sa(a,x): return x//2 if x%2==0 else (3*x+1)//2-((1<<a) if (x+1)%(1<<(a+1))==0 else 0)
for a in range(0,12):
    pref=set()
    for x in range(15,1<<16,16):
        y=x;w=''
        for _ in range(4): w+=str(y&1); y=Sa(a,y)
        pref.add(w)
    print('a',a,'prefixes of 15 mod 16 under S_a',pref)
# ---- Theorem B
def implant(m,X):
    ps=[p for p in range(5,m+1) if m%p==0 and all(p%q for q in range(2,int(p**.5)+1))]
    a=1
    for p in ps: a=a*(p-1)//math.gcd(a,p-1)
    while a<3: a*= 2 if a>1 else 3
    D=2**a-3; assert math.gcd(D,6*m)==1
    k=0;Mo=m
    while Mo%2==0: Mo//=2;k+=1
    kp=max(k,2)
    while 2**kp<=D*X: kp+=1
    mp_=2**kp*Mo; r=pow(D,-1,2**kp); assert r>X
    c=(-pow(2*mp_,-1,D))%D or D
    G=mp_*c; assert (1+2*G)%D==0
    x0=(1+2*G)//D
    S=lambda n: n//2 if n%2==0 else (3*n+1)//2+(G if n%2**kp==r else 0)
    assert x0%2**kp==r and G%m==0 and G%2**kp==0 and G>0
    cyc=[x0];y=S(x0)
    while y!=x0 and len(cyc)<10*a: cyc.append(y);y=S(y)
    assert y==x0 and len(cyc)==a and min(cyc)>X
    assert all(S(n)==T(n) for n in range(1,min(X,10**6)+1))
    random.seed(1)
    pts=[random.randrange(1,2**(kp+8))|1 for _ in range(3000)]+[r+2**kp*j for j in range(200)]+[r+2**j for j in range(1,kp+5)]
    for u in pts:
        for v in pts:
            if u!=v:
                d=u-v; e=S(u)-S(v); assert e!=0 and (e&-e)*2==(d&-d)
    print('implant m',m,'X',X,'a',a,'D',D,"k'",kp,'r',r,'c',c,'G',G,'x0',x0,'cycle len',len(cyc),'OK')
for m,X in [(1,100),(35,10**6),(2,1),(12,5),(1,1),(1000,10**4),(7*11*13,50)]: implant(m,X)
