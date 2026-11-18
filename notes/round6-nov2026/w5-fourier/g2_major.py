# Block-pairing majorant for |T_K(xi)|, xi = num * 3^(-P0) mod 2^K  (num integer, may be huge, e.g. 3^n).
#   usage: g2_major.py K num [r=2] [eps=0.1] [mult=3]
# Running frequency at node (P,k): xi_P = num*3^(-P) mod 2^k.  r-block identity (exact, k >= 4r):
#   T_k(xi_P) = sum_{A=0..r} S_A(P,k) * T_{k-Q_A}(xi_{P+P_A}),  S_A = sum_{u, #a=A} e(-num*D_u*3^(-(P+P_A))/2^k)
# Majorant  U(P,k) = sum_A |S_A| U(P+P_A, k-Q_A),  U = N_k for k < 4r.   Then |T_K(num)| <= U(0,K).
# r=2:  |S_1| = 2|cos(pi*{11*num*3^(-(P+5))/2^k})|.   Node eps-good  <=>  |S_1| <= 2cos(pi*eps).
# g(P,k) = [good] + min over children: the min number of good nodes on any block path.
# Prints delta_U = -log(U/N)/log N, gmin, and the fraction of good nodes among all reachable nodes.
import sys, math, itertools
K = int(sys.argv[1]); num = eval(sys.argv[2]); r = int(sys.argv[3]) if len(sys.argv) > 3 else 2
eps = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
mult = int(sys.argv[5]) if len(sys.argv) > 5 else 3
la = {3: (2, 3), 5: (2, 5)}[mult]; lb = {3: (3, 4), 5: (3, 7)}[mult]   # (P,Q) increments of a, b  (5n+1: a=(25w+..)/32? see note)
if mult != 3: sys.exit("only mult=3 implemented")
N = [1, 2, 2, 2]
for k in range(4, K+1): N.append(N[k-3] + N[k-4])
# blocks of r letters grouped by number of a's; D_{ua}=9D+2^Q, D_{ub}=27D (u applied outermost-first)
blocks = {}
for w in itertools.product('ab', repeat=r):
    P = Q = D = 0
    for ch in w:
        if ch == 'a': D = 9*D + (1 << Q); P += 2; Q += 3
        else: D = 27*D; P += 3; Q += 4
    blocks.setdefault((P, Q), []).append(D)
blocks = sorted(blocks.items())
Pmax = (3*K)//4 + 3*r + 8
MK = 1 << K
inv = [1]; i3 = pow(3, -1, MK)
for p in range(Pmax + 1): inv.append((inv[-1]*i3) % MK)
kmin = 4*r
R = [None]*(K+1); G = [None]*(K+1)
tw = 2*math.pi; good_cnt = tot_cnt = 0
thr = 2*math.cos(math.pi*eps)
for k in range(K+1):
    npk = (3*(K-k))//4 + 2
    if k < kmin:
        R[k] = [1.0]*npk; G[k] = [0]*npk; continue
    Rk = [0.0]*npk; Gk = [0]*npk; mask = (1 << k) - 1; sh = max(k - 60, 0); sc = 1.0/(1 << min(k, 60))
    for P in range(npk):
        tot = 0.0; gm = 10**9; isgood = 0
        for (dP, dQ), Ds in blocks:
            base = num*inv[P + dP]
            if len(Ds) == 1: mod = 1.0
            else:
                sr = si = 0.0
                for D in Ds:
                    t = ((-base*D) & mask) >> sh
                    sr += math.cos(tw*t*sc); si += math.sin(tw*t*sc)
                mod = math.hypot(sr, si)
                if r == 2 and mod <= thr: isgood = 1
            kk = k - dQ; PP = P + dP
            if PP < len(R[kk]):
                tot += mod*(N[kk]/N[k])*R[kk][PP]
                if G[kk][PP] < gm: gm = G[kk][PP]
            else:    # outside stored cone (unreachable from (0,K)); trivial bound
                tot += mod*(N[kk]/N[k]); gm = 0
        Rk[P] = tot; Gk[P] = gm + isgood
        good_cnt += isgood; tot_cnt += 1
    R[k] = Rk; G[k] = Gk
lN = math.log(N[K])
c0 = min(2*N[k-7]/N[k] for k in range(8, K+1)) if K >= 8 else 0
beta = 1 - (1 - math.cos(math.pi*eps))*c0
print("K=%d num=%s r=%d eps=%g : U/N=2^%.2f  delta_U=%.4f  | gmin=%d (gmin/K=%.4f) good-node frac=%.3f  beta=%.4f  bound-from-gmin delta=%.4f"
      % (K, sys.argv[2], r, eps, math.log2(R[K][0]), -math.log(R[K][0])/lN, G[K][0], G[K][0]/K,
         good_cnt/max(tot_cnt, 1), beta, -G[K][0]*math.log(beta)/lN))
