"""Exact checks (fractions / integers only):
 (1) theta-identity: w_N * 2^{Q_N} = 3^{P_N} (w + gamma_N), gamma_N = sum over a-steps j<=N of 2^{Q_{j-1}}/3^{P_j}, 0<=gamma_N<1,
     and gamma_N = -w mod 2^{Q_N} 2-adically (i.e. 3^{P_N} w + c_N = 0 mod 2^{Q_N}).
 (2) rational points of E: -27/115 has itinerary (ab)^omega (equivalently 3n-115 system has the cycle 27 -> 16 -> 27);
     -1 and 0 fixed; periodic word u gives z = -gamma(u^omega) in [-1,0].
 (3) scan: no rational p/q with q odd, 1<=p,q<=H0 survives; report max life (bits) by height.
 (4) cylinder counts N_k = #(E mod 2^k) and constant in N_k <= C 2^{sk}."""
from fractions import Fraction as Fr
import math, random, sys
def v2(n):
    return (n & -n).bit_length() - 1 if n else 10**9
def stepq(p, q):  # rational p/q, q odd; conditions are 2-adic conditions on p*q^{-1}; a: z=7 mod 8 <=> 9p+q = 0 mod 8 (p odd), b: 16 | p
    if p % 2 == 0:
        if p % 16 == 0 and p != 0: return (27 * (p // 16), q, 4, 'b')
        if p == 0: return (0, q, 4, 'b')
        return None
    if (9 * p + q) % 8 == 0: return ((9 * p + q) // 8, q, 3, 'a')
    return None
def lifeq(p, q, cap=4000):
    L = 0; seen = {}
    while L < cap:
        s = stepq(p, q)
        if s is None: return L
        p, q, d, _ = s; L += d
        g = math.gcd(p, q); p //= g; q //= g
        if (p, q) in seen: return math.inf
        seen[(p, q)] = L
    return math.inf
# (1)
random.seed(1); checked = 0
from a1_core import leaves
for r, q, M, wp, na, nb in leaves(40, '3n+1'):
    w = r; P = Q = 0; gam = Fr(0); z = w
    while True:
        s = stepq(z, 1)
        if s is None or Q >= q: break
        if s[3] == 'a': gam += Fr(2**Q, 3**(P + 2)); P += 2; Q += 3
        else: P += 3; Q += 4
        z = s[0]
        assert Fr(z) * 2**Q == 3**P * (w + gam) and 0 <= gam < 1
        c = gam * 3**P; assert c.denominator == 1 and (3**P * w + int(c)) % 2**Q == 0
        checked += 1
print("(1) theta-identity checked on", checked, "orbit steps: OK")
# (2)
print("(2) life(-27/115) =", lifeq(-27, 115), " life(-1) =", lifeq(-1, 1), " life(0) =", lifeq(0, 1))
z = (-27, 115); s1 = stepq(*z); s2 = stepq(s1[0], s1[1]); print("    -27/115 ->", s1[:2], s1[3], "->", s2[:2], s2[3])
w = 27; w1 = (9 * w - 115); assert w1 % 8 == 0 and (w1 // 8) % 16 == 0 and 27 * (w1 // 8) // 16 == 27
print("    3n-115 system: 27 -> (9*27-115)/8 = 16 -> 27*16/16 = 27  (cycle, itinerary (ab)^omega)")
# (3)
H0 = int(sys.argv[1]) if len(sys.argv) > 1 else 512
best = {}; inf = []
for q in range(1, H0 + 1, 2):
    for p in range(1, H0 + 1):
        if math.gcd(p, q) != 1: continue
        L = lifeq(p, q)
        if L == math.inf: inf.append((p, q)); continue
        h = max(p, q).bit_length()
        if L > best.get(h, (0,))[0]: best[h] = (L, p, q)
print(f"(3) positive rationals p/q, q odd, height <= {H0}: infinite-life ones: {inf}")
for h in sorted(best): print(f"    height < 2^{h}: max life {best[h][0]} bits at {best[h][1]}/{best[h][2]}")
neg_inf = 0; out = 0
for q in range(1, 130, 2):
    for p in range(1, 4 * q + 1):
        if math.gcd(p, q) == 1 and lifeq(-p, q) == math.inf:
            neg_inf += 1
            if p > q: out += 1
print(f"    negative rationals -p/q (q<130 odd, p<=4q) with eventually periodic infinite itinerary: {neg_inf}; of these outside [-1,0]: {out}")
# (4)
s = -math.log2(0.8191725133961643)
N = {}
for k in range(1, 61):
    N[k] = len(set(l[0] % (1 << k) for l in leaves(k, '3n+1')))
print("(4) max_k N_k / 2^{sk} for k<=60:", max(N[k] / 2**(s * k) for k in N), " recursion N_k=N_{k-3}+N_{k-4} holds for k>=5:",
      all(N[k] == N[k - 3] + N[k - 4] for k in range(5, 61)))
