# Step 7: Corollary 6 bookkeeping, in logs (base 2).
import math
N = [1,2,2,2]
for k in range(4, 5001): N.append(N[k-3]+N[k-4])
L = [math.log2(n) for n in N]
s = math.log2(1.2207440846057596)
print("best constant c0 with 2N_{k-7} >= c0 N_k, k>=8: 4/9 (k=10):", all(9*2*N[k-7] >= 4*N[k] for k in range(8, 5001)))
for eps, c in ((0.1, 0.0475), (1e-3, 0.01)):
    beta = 1-0.4*(1-math.cos(math.pi*eps)); d = c*math.log2(1/beta)/s
    worst = max(L[K] + c*K*math.log2(beta) - (1-d)*L[K] for K in range(1, 5001))
    print("eps=%g c=%g beta=%.8f delta=%.4e: sup_K log2[N_K beta^(cK)/N_K^(1-delta)] = %.3e <= delta*log2(1.6384) = %.3e" % (eps, c, beta, d, worst, d*math.log2(1.6384)))
for eta in (0.05, 0.2):
    d = eta/s
    print("eta=%.2f delta=eta/s=%.4f: N_K^delta/2^(eta K) at K=100,1000,5000 = %s (>1: integers in (2^(eta K), N_K^delta] are outside (D)'s range)" % (eta, d, [round(2**(d*L[K]-eta*K), 4) for K in (100, 1000, 5000)]))
