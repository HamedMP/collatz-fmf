"""Python cross-check of the Lean sanity examples and of the formal statements as written
(exact integers).  Run: taskset -c 6 /home/matrix/home/projects/collatz/venv/bin/python crosscheck.py"""
import itertools
def step(l,w):
    if l=='a': return (9*w+1)//8 if w%8==7 else None
    return 27*w//16 if w%16==0 else None
def run(v,w):
    for l in v:
        w=step(l,w)
        if w is None: return None
    return w
B=lambda v: 3*v.count('a')+4*v.count('b'); e=lambda v: 2*v.count('a')+3*v.count('b')
# Lean examples
assert step('a',7)==8 and step('b',16)==27 and run('aa',55) is None
assert run('bbb',4096)==19683 and run('ba',80)==152 and run('aba',71)==152
assert 2**(B('a')+B('ab'))==1024 and 72*3**e('ab')==17496 and B('bba')==11 and e('bba')==8
assert run('bb',256)==729 and 2**64 < 257**4*3**36 == 654783403832048509485517521
assert run('a',33*7+32)==33*8+32 and run('ba',33*48+32)==33*92+32
# (A-i): cylinder of u = one residue class mod 2^B(u); Theorem A integer form, exhaustive small
nA=0
for L in range(1,6):
    for u in map(''.join,itertools.product('ab',repeat=L)):
        ws=[w for w in range(1,1<<(B(u)+2)) if run(u,w) is not None] if B(u)<=14 else []
        if ws:
            assert len({w%(1<<B(u)) for w in ws})==1 and len(ws)==4-(ws[0]%(1<<B(u))==0)
for w0 in range(1,200000):
    w=w0; P=''; st=[w0]
    while True:
        nx=[(l,step(l,w)) for l in 'ab' if step(l,w) is not None]
        if not nx: break
        P+=nx[0][0]; w=nx[0][1]; st.append(w)
    for i in range(len(P)):
        for i2 in range(i+1,len(P)):
            for n in range(1,len(P)-i2+1):
                if P[i:i+n]==P[i2:i2+n]:
                    u=P[i:i+n]; p=P[:i2]; nA+=1
                    assert 2**B(u)<=st[i2]-st[i] and 2**(B(u)+B(p))<(w0+1)*3**e(p)
print("Theorem A instances:",nA)
# Theorem B_XX form on itineraries
# KL core
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def S(a,x):
    out=set()
    for n in range(1,x+1):
        m=n
        seen=set()
        while m<=x and m not in seen:
            if m==a: out.add(n); break
            seen.add(m); m=T(m)
    return out
def oncycle(a):
    m=T(a)
    for _ in range(10000):
        if m==a: return True
        m=T(m)
    return False
assert (T(5),T(8),T(11),T(7))==(8,4,17,11)
r2=lambda a: (2*a-1)//3 if a%9==8 else (4*a-2)//3
assert [r2(a) for a in (8,11,17,20)]==[5,14,11,26]
nC=0
for a in range(2,120,3):
    if oncycle(a): continue
    for x in (4*a,4*a+1,5*a,8*a,300):
        if x<4*a: continue
        Sa,S4=S(a,x),S(4*a,x)
        assert S4<=Sa-{a}
        if a%9 in (8,2):
            Sr=S(r2(a),x)
            assert Sr<=Sa-{a} and not(S4&Sr) and len(Sa)>=1+len(S4)+len(Sr)
        nC+=1
print("KL core instances:",nC)
# the core is false on the cycle at a=2 (r2(2)=2): S_r2 = S_a not inside S_a\{a}
assert r2(2)==2 and oncycle(2)
print("OK")
