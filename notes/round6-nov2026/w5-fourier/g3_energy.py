# additive energy of E_k in Z/2^k:  En = #{(a,b,c,d): a+b = c+d mod 2^k} ; tau = log En / log N
# (sum_xi |T_k(xi)|^4 = 2^k * En).  Random-set benchmark: 2N^2 - N + N^4/2^k.
import sys, math, numpy as np
def Ek(k):
    if k == 0: return [0]
    if k <= 3: return [0, 2**k - 1]
    M = 1 << k
    i9 = pow(9, -1, M); i27 = pow(27, -1, M)
    return [((8*z-1)*i9) % M for z in Ek(k-3)] + [(16*z*i27) % M for z in Ek(k-4)]
for k in range(16, int(sys.argv[1])+1, 4):
    E = np.array(sorted(Ek(k)), dtype=np.uint64); N = len(E); M = np.uint64((1 << k) - 1)
    S = ((E[:, None] + E[None, :]) & M).ravel()
    _, cnt = np.unique(S, return_counts=True)
    En = int((cnt.astype(np.int64)**2).sum())
    Si = (E[:, None] + E[None, :]).ravel(); _, c2 = np.unique(Si, return_counts=True); EnZ = int((c2.astype(np.int64)**2).sum())
    print("k=%d N=%d E_cyc=%d tau=%.4f  E_Z=%d tauZ=%.4f  E/(2N^2-N)=%.3f  N^4/2^k=%.2f  max rep=%d"
          % (k, N, En, math.log(En)/math.log(N), EnZ, math.log(EnZ)/math.log(N), En/(2*N*N-N), N**4/2**k, cnt.max()))
