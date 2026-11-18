import math
from collections import Counter
s=0.2877607870840288
def alive(r,j):
    while True:
        if j<=0: return True
        if j<=3:
            m=(1<<j)-1
            return (r&m)==(7&m) or (r&m)==0
        if r&7==7: r=((9*r+1)>>3)&((1<<(j-3))-1); j-=3
        elif r&15==0: r=((27*r)>>4)&((1<<(j-4))-1); j-=4
        else: return False
# all words (not only leaves) with Q_u <= 33 : mirror identity, own recursion via inverse branches
# r_u computed 2-adically from f_a,f_b composition (independent of forward search), w'=u(r_u) by forward application
tot=bad=0
leaves={Q:[] for Q in range(1,31)}
def rec(word_Q,P,r):   # r = least residue of cylinder mod 2^Q  (cylinder = f_{u1}...f_{un}(Z_2)); extend at the END of word
    global tot,bad
    Q=word_Q
    # forward-apply
    w=r; q=0
    yield_ok=True
    tot+=1
    # w' computed by caller-provided stack below
def run():
    global tot,bad
    # stack: (Q,P,r,wp) ; extending word by letter c at end: new cylinder = {z in cyl(u): u(z) in gate(c)}
    st=[(0,0,0,0,0)]  # Q,P,r,wp,Qprev
    while st:
        Q,P,r,wp,Qprev=st.pop()
        if Q>0:
            tot+=1
            # independent forward check
            x=r
            M3=3**P
            if not (0<=wp<M3 and (wp<<Q)//M3==r): bad+=1
            for QQ in range(Qprev+1,Q+1):
                if QQ<=30: leaves[QQ].append((r,Q,P,wp))
        if Q>=30: continue
        M3=3**P
        for t in range(8):
            v=wp+M3*t
            if v%8==7: st.append((Q+3,P+2,r+(t<<Q),(9*v+1)//8,Q))
        for t in range(16):
            v=wp+M3*t
            if v%16==0: st.append((Q+4,P+3,r+(t<<Q),27*v//16,Q))
run()
print("words with Q_u<=33 checked:",tot,"mirror failures:",bad)
# independent verification that r is truly the cylinder's least residue & wp=u(r): forward replay for a sample level
def replay(r,Q):
    x=r;q=0
    while q<Q:
        if x%8==7: x=(9*x+1)//8;q+=3
        elif x%16==0: x=27*x//16;q+=4
        else: return None
    return x,q
for Q in (7,19,30):
    for r,Qu,P,wp in leaves[Q]:
        assert replay(r,Q)==(wp,Qu)
    print("level",Q,"leaves",len(leaves[Q]))
# N(Q,m) identity: LHS brute force
print("N(Q,m): LHS=#{w<2^Q: w mod 2^(Q+m) in E mod 2^(Q+m)}, RHS=#{leaves u at level Q, r_u<2^Q, w'_u in E mod 2^m}, RHS2 uses m-(Qu-Q) bits")
for Q in (8,12,16,18):
    for m in (0,2,4,8,12):
        lhs=sum(alive(w,Q+m) for w in range(1<<Q))
        rhs=sum(1 for r,Qu,P,wp in leaves[Q] if r<(1<<Q) and alive(wp,m))
        rhs2=sum(1 for r,Qu,P,wp in leaves[Q] if r<(1<<Q) and alive(wp,m-(Qu-Q)))
        print(Q,m,lhs,rhs,rhs2)
# Theorem 6 parameters + FP numerics
def Eset(k,memo={}):
    if k<=0: return {0}
    if k not in memo:
        M=1<<k; i9=pow(9,-1,M); i27=pow(27,-1,M)
        memo[k]={((8*z-1)*i9)%M for z in Eset(k-3)}|{(16*z*i27)%M for z in Eset(k-4)}
    return memo[k]
for Q in range(1,400):
    Qp=math.ceil(Q/(1-s)); m=Qp-Q
    assert 1<=m<=Qp and m>=s*Qp and s*Qp-m<=0
print("Thm6 parameter choice valid for Q=1..399")
for Qp in (40,48,56):
    E=Eset(Qp)
    for m in (int(s*Qp),int(s*Qp)+4,Qp//2):
        b=Counter(c>>(Qp-m) for c in E)
        print("Q'=%d m=%d N=%d max bucket=%d  bucket0=%d  top bucket=%d  2^(sQ'-m)=%.2f"%(Qp,m,len(E),max(b.values()),b[0],b[(1<<m)-1],2**(s*Qp-m)))
    Q=math.floor(Qp*(1-s)); pos=sorted(c for c in E if c<(1<<Q))
    print("   elements of E mod 2^Q' below 2^Q (Q=%d):"%Q,pos[:8],len(pos))
