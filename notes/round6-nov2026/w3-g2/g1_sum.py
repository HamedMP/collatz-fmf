import sys,collections
# usage: g1_sum.py L file...   -> E_lambda for lambda grid
L=int(sys.argv[1]); h=collections.Counter(); leaves=0
for f in sys.argv[2:]:
    for line in open(f):
        w=line.split()
        if w[0]=='D': h[int(w[1])]+=int(w[2])
        if w[0]=='L': leaves+=int(w[-1])
tot=sum(h.values())
out=[]
for lam in (1,1.25,1.5,2,3,4,8):
    J=int(lam*L)          # survive all j<=J  <=> D > J
    out.append(sum(c for d,c in h.items() if d>J))
print(L,leaves,tot,*out)
