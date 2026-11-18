"""Exact checks for the barrier / rigidity statements of REPORT.md (w2-gamma).
T(n)=n/2 (n even), (3n+1)/2 (n odd).  Class C: S(2x)=x, S(x)=T(x)+g(x) on odd x, g 1-Lipschitz 2-adically.
"""
import sys, random
from math import gcd
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def v2(n):
    assert n!=0
    return (n & -n).bit_length()-1

# ---------- controls S_a ----------
def S_a(a):
    M = 1<<(a+1)
    def S(n):
        if n%2==0: return n//2
        return (3*n+1)//2 - ((1<<a) if n%M==M-1 else 0)
    return S

def prefix_property(S, k):
    """n mod 2^k <-> first k parities is a bijection on [1,2^k]+shifts"""
    seen = {}
    for n in range(1, (1<<k)+1):
        x=n; w=[]
        for _ in range(k):
            w.append(x&1); x=S(x)
        w=tuple(w)
        if w in seen: return False
        seen[w]=n
    # and invariance under adding multiples of 2^k
    for _ in range(300):
        n = random.randrange(1,1<<k); t=random.randrange(1,1<<20)
        x=n; y=n+(t<<k)
        for _ in range(k):
            if (x&1)!=(y&1): return False
            x=S(x); y=S(y)
    return True

print("== Theorem R(b): controls S_a ==")
for a in range(0, 13):
    S = S_a(a); n0=(1<<(a+1))-1
    assert S(n0)==n0
    ok = prefix_property(S, min(a+6, 14))
    viol=[n for n in range(1, 1<<(a+5)) if not ((n%2==0 and (n==0 or 1<=S(n)<n)) or (n%2==1 and n<S(n)<=2*n))]
    cong = all((S(n)-T(n)) % (1<<a)==0 for n in range(1,1<<(a+4)))
    same = all(S(n)==T(n) for n in range(1,n0))
    # cycles reached from n<=N
    N=200000 if a<=8 else 50000
    cyc=set(); maxlen=0; bad=0
    for n in range(1,N+1):
        x=n; steps=0; seen_local={}
        while True:
            if x<n and x in ():
                break
            if x in seen_local: break
            seen_local[x]=steps; x=S(x); steps+=1
            if steps>20000: bad+=1; break
            if x<n: break  # descended below start: earlier start handles it
        if steps<=20000 and x in seen_local and x>=n:
            # found a cycle containing x
            c=[x]; y=S(x)
            while y!=x: c.append(y); y=S(y)
            cyc.add(min(c))
    print(f"a={a:2d} fixed pt {n0}: prefix-bijection={ok}, S==T below n0: {same}, S≡T mod 2^a: {cong}, "
          f"(II)/(III) violated exactly at {viol}, cycle minima from n<={N}: {sorted(cyc)}, non-terminating(20000 steps): {bad}")

# ---------- Theorem R(a): exhaustive rigidity on odd x < 2^K ----------
print("== Theorem R(a): exhaustive search for nonzero 1-Lipschitz g with |g(x)|<=(x-1)/2 on odd x<2^7 ==")
odds=list(range(1,128,2))
sols=0
def rec(i,g):
    global sols
    if i==len(odds):
        if any(g): sols+=1
        return
    x=odds[i]; B=(x-1)//2
    for val in range(-B,B+1):
        if all((val-g[j])%(1<<v2(x-odds[j]))==0 for j in range(i)):
            g.append(val); rec(i+1,g); g.pop()
rec(0,[])
print("nonzero solutions:", sols, "(theorem predicts 0)")
# sharpness of the constant: allow |g(x)| <= (x+1)/2
sols2=0
def rec2(i,g,limit):
    global sols2
    if sols2>=limit: return
    if i==len(odds):
        if any(g): sols2+=1
        return
    x=odds[i]; B=(x+1)//2
    for val in range(-B,B+1):
        if all((val-g[j])%(1<<v2(x-odds[j]))==0 for j in range(i)):
            g.append(val); rec2(i+1,g,limit); g.pop()
rec2(0,[],1000)
print("with |g(x)|<=(x+1)/2: nonzero solutions found (capped at 1000):", sols2)

# ---------- Theorem B: implant, S≡T mod m, S=T on [1,X], S>=T ----------
print("== Theorem B: cycle implants ==")
def implant(m, X):
    # choose a with gcd(2^a-3, m)=1 and a>=3
    a=3
    while gcd((1<<a)-3, m)!=1: a+=1
    D=(1<<a)-3
    k=v2(m) if m%2==0 else 0
    Modd = m>>k
    kp=max(k,1)
    while True:
        mp_=(1<<kp)*Modd
        r=pow(D,-1,1<<kp)
        if r>X and r%2==1 and kp>=2: break
        kp+=1
    # c in [1,D] with 1+2*mp_*c ≡ 0 mod D
    c=(-pow(2*mp_,-1,D))%D
    if c==0: c=D
    G=mp_*c
    x0=(1+2*G)//D
    assert (1+2*G)%D==0 and x0%(1<<kp)==r
    def S(n):
        if n%2==0: return n//2
        return (3*n+1)//2 + (G if n%(1<<kp)==r else 0)
    return S,a,kp,r,G,x0
for (m,X) in [(1,10),(2**10,1000),(3**5*5*7*11,10**6),(2**20*3**10*5**5*7**3,10**9),(13*17*2**7,10**4)]:
    S,a,kp,r,G,x0=implant(m,X)
    x=x0; orb=[x]
    for _ in range(a):
        x=S(x); orb.append(x)
    assert orb[-1]==x0 and len(set(orb[:-1]))==a
    assert G%m==0 and r>X and G%(1<<kp)==0
    assert all(S(n)==T(n) for n in range(1,min(X,5000)+1))
    print(f"m={m}, X={X}: class {r} mod 2^{kp}, G={G}, cycle of length {a} through x0={x0} (x0>X: {x0>X}); prefix-bijection(k=12): {prefix_property(S,12)}")

# ---------- 3n+d: primitive cycles for every d coprime to 6 ----------
print("== 3n+d (d coprime to 6): primitive positive cycles, i.e. positive rational T-cycles n/d not in Z ==")
def prim_cycle(d, start_limit):
    def Td(n): return n//2 if n%2==0 else (3*n+d)//2
    for n in range(1, start_limit, 2):
        if gcd(n,d)!=1: continue
        # Floyd
        s=n; f=n
        while True:
            s=Td(s); f=Td(Td(f))
            if s==f: break
        # s on a cycle
        c=[s]; y=Td(s)
        while y!=s: c.append(y); y=Td(y)
        if gcd(min(c),d)==1:
            return min(c), len(c)
    return None
D=int(sys.argv[1]) if len(sys.argv)>1 else 3000
missing=[]; cnt=0
for d in range(5, D):
    if gcd(d,6)!=1: continue
    cnt+=1
    r=prim_cycle(d, 400)
    if r is None: missing.append(d)
print(f"d coprime to 6, 5<=d<{D}: {cnt} values; those with NO primitive cycle found from odd starts <400: {missing}")
