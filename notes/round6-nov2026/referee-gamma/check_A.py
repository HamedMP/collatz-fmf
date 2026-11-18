# Independent test of Lemma 2 / Theorem A with A = Z (dense, countable, T-invariant in Z_2), exact integers.
# enumeration: 0..X, then -1, X+1, -2, X+2, ...
X=63
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def idx(a): return a if 0<=a<=X else (X+2*(a-X) if a>0 else X+2*(-a)-1)
def own(c,j):   # least-index integer == c mod 2^j
    c%=1<<j
    return min((c,c-(1<<j)),key=idx)
H={0:0}
J=13
for j in range(J):
    for n1 in range(1<<j): H[n1+(1<<j)]=own(H[n1]+(1<<j),j+1)
N=1<<J
v2=lambda d:(d&-d).bit_length()-1
import random; random.seed(0)
assert len(set(H.values()))==N
assert all(v2(H[a]-H[b])==v2(a-b) for a,b in ((random.randrange(N),random.randrange(N)) for _ in range(400000)) if a!=b)
assert all(H[n]==n for n in range(X+1))
img=set(H.values()); print('image contains all |a|<=',next(a for a in range(N) if a not in img or -a not in img)-1)
Hinv={v:k for k,v in H.items()}
S={n:Hinv[T(H[n])] for n in range(N) if T(H[n]) in Hinv}
print('S defined on',len(S),'of',N)
print('S=T up to',next(n for n in sorted(S) if S[n]!=T(n))-1,'(claimed >=',(2*X-1)//3,')')
print('S==T mod 32 everywhere:',all((S[n]-T(n))%32==0 for n in S), ' mod 64:',all((S[n]-T(n))%64==0 for n in S))
ks=sorted(S); bad=0
for _ in range(300000):
    a,b=random.choice(ks),random.choice(ks)
    if a!=b and (a-b)%2==0 and v2(S[a]-S[b])!=v2(a-b)-1: bad+=1
print('Lemma-1 valuation violations for S_A:',bad)
print('S(0)=',S[0],'; n>0 with S(n)=0:',[n for n in S if n and S[n]==0])
# cycles from negative cycles
for a in (-1,-5,-17):
    n=Hinv[a]; orb=[n]
    while S[orb[-1]]!=n: orb.append(S[orb[-1]])
    print('cycle through h^-1(%d):'%a,orb)
