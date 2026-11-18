"""Finite demonstration of Theorem A (REPORT.md): an N_0 -> N_0 map S = h^{-1} T h, h a parity-preserving
2-adic isometry with h(N_0) = A := N_0 ∪ {T^t(z)}, z an irrational 2-adic integer (aperiodic parity word).
S has the parity-prefix (shift-conjugacy) property, S = T on small n, S ≡ T mod 2^k, and an infinite
non-periodic (hence unbounded) orbit.  All arithmetic exact; z_t is known modulo 2^P.
Enumeration of A: 0,1,...,XP, z_0, XP+1, z_1, XP+2, ...   (rank = position).
"""
XP=63; TZ=6000; P=400; DEPTH=200
def T(n): return n>>1 if n&1==0 else (3*n+1)>>1
# aperiodic parity word: binary Champernowne word 1 10 11 100 101 ... (not eventually periodic: it contains
# arbitrarily long runs of 0 and infinitely many 1s), so z is an irrational 2-adic integer.
w=[]; i=1
while len(w)<TZ+P+10:
    w.extend(int(c) for c in bin(i)[2:]); i+=1
# z_0 mod 2^(P+TZ) with parity word w
n=0; y=0; p3=1
for k in range(P+TZ):
    if (y&1)!=w[k]: n+= (1<<k); y+=p3
    if y&1: y=(3*y+1)>>1; p3*=3
    else: y>>=1
z=[n]
for t in range(TZ): z.append(T(z[-1]) % (1<<(P+TZ-t-1)))
mask=lambda j:(1<<j)-1
first=[{} for _ in range(DEPTH+1)]      # depth j: residue -> least t with z_t in class
for t in range(TZ+1):
    for j in range(DEPTH+1):
        r=z[t]&mask(j)
        if r not in first[j]: first[j][r]=t
def rank_n(c): return c if c<=XP else XP+2*(c-XP)
def rank_z(t): return XP+1+2*t
def owner(c,j):
    """first enumerated element of A in class c mod 2^j (0<=c<2^j)."""
    assert j<=DEPTH
    t=first[j].get(c)
    if t is not None and rank_z(t)<rank_n(c): return ('z',t)
    assert t is not None or c-XP < TZ, "outside validated range"
    return ('n',c)
def bit(a,j):
    return ((a[1] if a[0]=='n' else z[a[1]])>>j)&1
def h(n):
    c=0;j=0
    while (n>>j)!=0:
        pb=bit(owner(c,j),j); nb=pb if ((n>>j)&1)==0 else 1-pb
        c|=nb<<j; j+=1
    return owner(c,j)
def hinv(a):
    val=a[1] if a[0]=='n' else z[a[1]]
    n=0;j=0
    while True:
        o=owner(val&mask(j),j)
        if o==a: return n
        if bit(o,j)!=((val>>j)&1): n|=1<<j
        j+=1
def S(n):
    a=h(n)
    b=('n',T(a[1])) if a[0]=='n' else ('z',a[1]+1)
    return hinv(b)
NMAX=1500
vals={n:S(n) for n in range(NMAX)}
assert all(hinv(h(n))==n for n in range(NMAX))
print("S defined on 0..%d, values natural; first values:"%(NMAX-1), [vals[n] for n in range(70,90)])
print("S(n)==T(n) for all n<=40:", all(vals[n]==T(n) for n in range(41)), "; first n with S(n)!=T(n):", next(n for n in range(NMAX) if vals[n]!=T(n)))
print("S(n) ≡ T(n) mod 2^5 for all n<%d:"%NMAX, all((vals[n]-T(n))%32==0 for n in range(NMAX)))
# parity-prefix property: n mod 2^k <-> first k parities, on 0<=n<2^k, k=7 (orbits stay in validated range or we skip)
k=7; seen={}; ok=True
for n in range(1<<k):
    x=n; word=[]
    for _ in range(k): word.append(x&1); x=S(x)
    word=tuple(word)
    if word in seen: ok=False
    seen[word]=n
print("parity-prefix bijection on residues mod 2^%d:"%k, ok and len(seen)==1<<k)
# lifts: n and n+2^k*t have same first k parities
import random; random.seed(3); ok2=True; checked=0
for _ in range(600):
    n=random.randrange(1<<k); m=n+(random.randrange(1,8)<<k)
    x,y=n,m
    try:
        for _ in range(k):
            if (x&1)!=(y&1): ok2=False
            x=S(x); y=S(y)
        checked+=1
    except AssertionError: pass   # orbit left the range where z_t was precomputed
print("prefix invariance under +2^k t:", ok2, "(%d pairs fully inside validated range)"%checked)
# the divergent orbit
orb=[hinv(('z',t)) for t in range(0,400)]
x=orb[0]; good=True
nsteps=0
for t in range(1,400):
    try: x=S(x)
    except AssertionError: break
    nsteps+=1
    if x!=orb[t]: good=False
print("orbit of n_z=%d under S follows h^{-1}(z_t) for %d steps: %s"%(orb[0],nsteps,good), "; all 400 values distinct:", len(set(orb))==400)
print("parities along it equal the aperiodic word:", [o&1 for o in orb[:60]]==w[:60])
print("first orbit values:", orb[:16], " max of first 400:", max(orb))
