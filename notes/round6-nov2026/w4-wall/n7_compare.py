"""n7_compare.py -- evaluate the proved bounds on |T_K(h)|/N_K (h odd): Theorem A of w3-fp0
(Parseval on the full group, needs 2^k << sqrt K) against Theorem A' here (pair counting + completion)."""
import math
c1=6.5; s=0.2877607871468
N=[1,2,2,2]
for j in range(4,900): N.append(N[j-3]+N[j-4])
def old(L,k):  # L=log2 K
    return (1+3*c1*2**(k-2-L/2))*2/math.sqrt(N[k-3])
def new(L,k):
    worst=0
    for kap in range(k-3,k+1):
        v=2*N[3]/N[kap]+2*c1*2**(-L/2)*sum(N[j]*j*2**((j+1)/2) for j in range(4,kap+1))/N[kap]
        worst=max(worst,v)
    return math.sqrt(worst)
print("log2K | Theorem A: best k, log2 bound, exponent | Theorem A': best k, log2 bound, exponent   (asymptotic exponents 0.0719 / 0.0913)")
for L in (20,40,60,80,120,160,240,320,480,640):
    ko=min(range(7,int(L)),key=lambda k:old(L,k)); kn=min(range(7,min(890,int(L))),key=lambda k:new(L,k))
    bo=math.log2(old(L,ko)); bn=math.log2(new(L,kn))
    print("%5d | k=%3d %8.2f %7.4f | k=%3d %8.2f %7.4f"%(L,ko,bo,-bo/L,kn,bn,-bn/L))
