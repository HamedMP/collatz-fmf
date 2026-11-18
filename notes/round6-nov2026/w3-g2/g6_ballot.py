# g6_ballot.py -- exact barrier counts for Theorem S+ (w3-g2)
# B_L(s) = #{ v in {0,1}^L : 2*3^(a_j) > 2^(j-s) for all 1<=j<=L }   (exact integers)
# checks  B_L(s) <= K * (s+2) * lam^(theta0*(s+1)) * 2^(eta*L) / L^1.5  and prints the sup of the ratio.
import math
th=math.log(2)/math.log(3); lam=th/(1-th); eta=-(th*math.log2(th)+(1-th)*math.log2(1-th))
def B(Lmax,s,marks):
    cur={0:1}; out={}
    for j in range(1,Lmax+1):
        nxt={}
        amin=None
        for a,c in cur.items():
            for a2 in (a,a+1):
                # alive iff 2*3^a2 > 2^(j-s)
                if j-s<=1 or 2*3**a2 > 1<<(j-s):
                    nxt[a2]=nxt.get(a2,0)+c
        cur=nxt
        if j in marks: out[j]=sum(cur.values())
    return out
def lg(n): return math.log2(n) if n.bit_length()<1000 else (n.bit_length()-1000)+math.log2(n>>(n.bit_length()-1000))
marks=[25,50,100,200,400,800,1600,2400]
print("eta=%.6f lam=%.6f  omega=1.5-theta0*log2(lam)/eta=%.5f"%(eta,lam,1.5-th*math.log2(lam)/eta))
worst=0
for s in (0,3,8,12,16,20):
    out=B(max(marks),s,set(marks))
    row=[]
    for L in marks:
        r=lg(out[L]) - (math.log2(s+2)+th*(s+1)*math.log2(lam)+eta*L-1.5*math.log2(L))
        row.append("%.3f"%2**r); worst=max(worst,2**r)
    print("s=%2d  ratio at L=%s : %s"%(s,marks," ".join(row)))
print("sup ratio",worst)
# with s = s(L) = ceil(log2(10 L)/eta): B_L / (2^(eta L) L^-omega log2 L)
om=1.5-th*math.log2(lam)/eta
for L in (50,100,200,400,800,1600):
    s=math.ceil(math.log2(10*L)/eta); o=B(L,s,{L})[L]
    print("L=%d s(L)=%d  B_L/(2^(eta L) L^-omega log2 L) = %.3f   B_L/(2^(eta L) L^-0.5) = %.4f"%(L,s,2**(lg(o)-eta*L+om*math.log2(L))/math.log2(L), 2**(lg(o)-eta*L+0.5*math.log2(L))))
