"""Random-model prediction for stopping-time records, and structured seeds.
A_k = #parity vectors of length k all of whose prefixes (length i>=1, j ones) satisfy 3^j > 2^i
    = #residue classes mod 2^k with coefficient stopping time > k.
Model: #{n<2^N : sigma(n) > k} ~ 2^(N-k) A_k ; predicted record k*(N) = max{k : 2^(N-k) A_k >= 1}.
"""
import sys
from math import log
def T(n): return n>>1 if n&1==0 else (3*n+1)>>1
def sigma(n, cap=10**7):
    x=n; k=0
    while k<cap:
        x=T(x); k+=1
        if x<n: return k
    return None
def glide_std(n):
    x=n; k=0
    while True:
        x = x>>1 if x&1==0 else 3*x+1
        k+=1
        if x<n: return k
KMAX=2600
# thresholds: need j > i*log3(2): minimal j for prefix length i
import math
L=math.log(2)/math.log(3)
def minj(i):
    j=int(i*L)
    while 3**j <= 2**i: j+=1
    while j>0 and 3**(j-1) > 2**i: j-=1
    return j
cur={0:1}  # j -> count
A=[1]
for i in range(1,KMAX+1):
    mj=minj(i); nxt={}
    for j,c in cur.items():
        for jj in (j,j+1):
            if jj>=mj: nxt[jj]=nxt.get(jj,0)+c
    cur=nxt; A.append(sum(cur.values()))
print("growth rate of A_k: (A_2600/A_1300)^(1/1300) =", math.exp((math.log(A[2600])-math.log(A[1300]))/1300), " (theory 2*0.96593=1.93185)")
def kstar(N):
    k=N
    best=N
    for k in range(1,KMAX+1):
        if (A[k]<<N) >= (1<<k): best=k
    return best
rec={10:81,14:105,16:135,19:173,20:183,21:224,23:246,24:287,25:298,26:376,28:395,31:433,32:447}
print("N : exhaustive record max sigma(n<2^N) [glide.c]  vs model k*(N)")
for N in sorted(rec): print(f"  {N:3d}: {rec[N]:5d}   model {kstar(N):5d}   record/N={rec[N]/N:.2f}")
for N in (40,50,60,64,71,100):
    print(f"  model k*({N}) = {kstar(N)}  ({kstar(N)/N:.2f} per bit)")
print("asymptotic model slope: ln2/(-ln 0.965926) per bit =", log(2)/(-log(0.9659258)))
# literature glide record-holders (values recalled from Roosendaal's tables; glides recomputed here exactly)
for n in (1008932249296231, 118303688851791519, 180352746940718527, 2602714556700227743):
    print(f"  n={n} (2^{log(n,2):.2f}): sigma(T-steps)={sigma(n)}, glide(standard steps)={glide_std(n)}, sigma/bit={sigma(n)/log(n,2):.2f}; model k*({int(log(n,2))+1})={kstar(int(log(n,2))+1)}")
# structured seeds
print("structured seeds: sigma / N")
import random
random.seed(1)
def qinv(word, N):
    """residue mod 2^N with periodic parity sequence word^inf (lifting bit by bit)."""
    n=0
    for k in range(N):
        # parity at step k of n must be word[k%len]
        x=n
        for i in range(k): x=T(x)
        if (x&1)!=word[k%len(word)]: n|=(1<<k)
    return n
for N in (60,120,240,480):
    row=[]
    n=(1<<N)-1; row.append(("2^N-1 (seed -1)",sigma(n)))
    for name,w in (("-5: (110)",[1,1,0]),("-17: (11110111000)",[1,1,1,1,0,1,1,1,0,0,0]),("(1110)",[1,1,1,0]),("(11101)",[1,1,1,0,1]),("(1101)",[1,1,0,1])):
        n=qinv(w,N)
        if n<3: continue
        row.append((name+f" [{n.bit_length()} bits]",sigma(n)))
    rs=[sigma(random.getrandbits(N)|(1<<(N-1))|3) for _ in range(20000)]
    row.append(("best of 20000 random N-bit",max(rs)))
    print(f" N={N}: "+"; ".join(f"{a}: {b} ({b/N:.2f}/bit)" for a,b in row))
