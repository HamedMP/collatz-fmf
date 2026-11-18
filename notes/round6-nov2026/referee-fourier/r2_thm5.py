# Step 5: Theorem 5.  Step 7: Corollary 6 numerics.
import math, random
import numpy as np
from functools import lru_cache
random.seed(11)
N = [1,2,2,2]
for k in range(4, 5001): N.append(N[k-3]+N[k-4])
bad = [k for k in range(8, 5001) if not (5*2*N[k-7] >= 2*N[k])]   # 2N_{k-7} >= 0.4 N_k  <=> 5 N_{k-7} >= N_k
print("2N_{k-7} >= 0.4 N_k fails at k in [8,5000]:", bad, " ; k<8 would be:", [(k, N[k]) for k in range(4, 8)])
print(" N_k = N_{k-6}+2N_{k-7}+N_{k-8} for 8<=k<=5000:", all(N[k] == N[k-6]+2*N[k-7]+N[k-8] for k in range(8, 5001)))
print(" min ratio 2N_{k-7}/N_k: %.6f at k=%d; limit %.6f" % (min((2*N[k-7]/N[k], k) for k in range(8, 5001)) + (2*1.2207440846057596**-7,)))
print(" N_{k-6}<=2N_{k-7}, N_{k-8}<=N_{k-7} for k>=9:", all(N[k-6] <= 2*N[k-7] and N[k-8] <= N[k-7] for k in range(9, 5001)), "; k=8:", (N[2], 2*N[1], N[0], N[1]))
KMAX = 60
E = {0: [0], 1: [0, 1], 2: [0, 3], 3: [0, 7]}
for k in range(4, KMAX+1):
    M = 1 << k; i9 = pow(9, -1, M); i27 = pow(27, -1, M)
    E[k] = [((8*z-1)*i9) % M for z in E[k-3]] + [(16*z*i27) % M for z in E[k-4]]
    assert len(E[k]) == N[k]
def Tabs(k, xi):
    M = 1 << k; xi %= M
    ph = np.array([((xi*c) % M)/M for c in E[k]], dtype=np.float64) if k > 52 else np.array([((xi*c) % M) for c in E[k]], dtype=np.float64)/M
    return abs(np.exp(2j*math.pi*ph).sum())
def UG(h, K, eps):
    @lru_cache(None)
    def y(P, k):
        M = 1 << k; r = (11*h*pow(3, -(P+5), M)) % M
        return r, M
    @lru_cache(None)
    def U(P, k):
        if k < 8: return float(N[k])
        r, M = y(P, k)
        return U(P+4, k-6) + 2*abs(math.cos(math.pi*r/M))*U(P+5, k-7) + U(P+6, k-8)
    @lru_cache(None)
    def g(P, k):
        if k < 8: return 0
        r, M = y(P, k); d = min(r, M-r)
        good = d >= eps*M
        return int(good) + min(g(P+4, k-6), g(P+5, k-7), g(P+6, k-8))
    return U, g
viol = 0; rows = []; tight = 0
for eps in (0.1, 0.02, 0.3, 0.45, 1e-3):
    beta = 1 - 0.4*(1-math.cos(math.pi*eps))
    for h in (1, 2, 3, 5, 11, 27, 243, -1, 3**10, 2**40+13):
        for K in range(8, KMAX+1):
            U, g = UG(h, K, eps)
            # check at root and at a few internal nodes
            nodes = [(0, K)]
            if K >= 30: nodes += [(4, K-6), (5, K-7), (6, K-8), (15, K-21), (18, K-24)]
            for P, k in nodes:
                if eps == 0.1 or (P, k) == (0, K):
                    t = Tabs(k, h*pow(3, -P, 1 << k))
                else: t = None
                u = U(P, k); b = N[k]*beta**g(P, k)
                if (t is not None and t > u*(1+1e-9) + 1e-7) or u > b*(1+1e-9): viol += 1; print("VIOLATION eps", eps, "h", h, "K", K, (P, k), t, u, b)
                if t is not None and t > 0.98*u: tight += 1
            if eps == 0.1 and K in (40, 60) and h in (1, 2, 3, 5, 11, 27, 243):
                rows.append((K, h, Tabs(K, h), U(0, K), N[K]*beta**g(0, K), g(0, K), N[K]))
print("Theorem 5 violations (|G|<=U<=N beta^g; 5 eps x 10 h x K=8..60, root + internal nodes):", viol, " near-tight cases |T|>0.98U:", tight)
for r in rows: print("   K=%d h=%d |T|=%.3f U=%.3f N*beta^g=%.3f g=%d N_K=%d" % r)
# random xi mod 2^K in place of h
viol2 = 0
for _ in range(300):
    K = random.randint(8, 44); xi = random.randrange(1 << K); eps = random.choice([0.05, 0.1, 0.25, 0.49])
    U, g = UG(xi, K, eps); beta = 1-0.4*(1-math.cos(math.pi*eps))
    t = Tabs(K, xi); u = U(0, K)
    if t > u*(1+1e-9)+1e-7 or u > N[K]*beta**g(0, K)*(1+1e-9): viol2 += 1
print("random xi mod 2^K violations:", viol2)
# sharpness of the constant 0.4: would 0.5 work? (k=9 gives 4/8, k=8 4/7, limit 2*lam^-7)
for cst in (0.4, 0.45, 0.4951, 0.5):
    print("  2N_{k-7} >= %.4f N_k for all 8<=k<=5000: %s" % (cst, all(2*N[k-7] >= cst*N[k] for k in range(8, 5001))))
# Corollary 6: N_K beta^{cK} vs N_K^{1-delta}, delta = c log2(1/beta)/s
s = math.log2(1.2207440846057596)
for eps, c in ((0.1, 0.0475), (1e-3, 0.01)):
    beta = 1-0.4*(1-math.cos(math.pi*eps)); d = c*math.log2(1/beta)/s
    worst = max(N[K]*beta**(c*K)/N[K]**(1-d) for K in range(1, 5001))
    print("  Cor6: eps=%g c=%g beta=%.6f delta=%.3e ; sup_K N_K beta^{cK}/N_K^{1-delta} = %.6f (<= 1.64^delta = %.6f)" % (eps, c, beta, d, worst, 1.6384**d))
eta = 0.05; d = eta/s
print("  Cor6 range: delta=eta/s, eta=%.2f: N_K^delta / 2^(eta K) at K=100,1000,5000: %s  (ratio>1 => integers h in (2^{eta K}, N_K^delta] not covered by (D))" % (eta, [round(math.exp(d*math.log(N[K]) - eta*K*math.log(2)), 4) for K in (100, 1000, 5000)]))
