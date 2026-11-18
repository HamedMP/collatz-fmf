# Exact checks (rational arithmetic) of:
#  (1) E_k recursion vs words, (2) mirror identity  c/2^K == x - {x}_3 (mod 1), x = f_v(z)/2^K,
#  (3) ab/ba pairing formula, (4) generic-zeta family: |T^zeta| for zeta=1 vs random zeta.
import sys, cmath, math, random
from fractions import Fraction as Fr
K = int(sys.argv[1]) if len(sys.argv) > 1 else 22
def Ek(k):
    if k == 0: return [0]
    if k <= 3: return [0, 2**k - 1]
    M = 1 << k
    i9 = pow(9, -1, M); i27 = pow(27, -1, M)
    return [((8*z-1)*i9) % M for z in Ek(k-3)] + [(16*z*i27) % M for z in Ek(k-4)]
# words: (P,Q,D) with f_v(z) = (2^Q z - D)/3^P ; D_{va}=9D+2^Q, D_{vb}=27D
def words(K):
    out = []
    st = [(0, 0, 0, '')]
    while st:
        P, Q, D, w = st.pop()
        if K - Q <= 3:
            out.append((P, Q, D, w)); continue
        st.append((P+2, Q+3, 9*D + (1 << Q), w+'a'))
        st.append((P+3, Q+4, 27*D, w+'b'))
    return out
E = sorted(Ek(K)); M = 1 << K
W = words(K)
pts = []   # (c, rational r=f_v(z)) pairs
for P, Q, D, w in W:
    kap = K - Q
    for z in ([0] if kap == 0 else [0, -1]):
        r = Fr((z << Q) - D if z == 0 else -(1 << Q) - D, 3**P)
        c = (r.numerator * pow(r.denominator, -1, M)) % M
        pts.append((c, r, P))
assert sorted(c for c, _, _ in pts) == E, "word parametrisation != E_K"
print("K=%d N_K=%d words ok; all f_v(z) in (-2,0]: %s" % (K, len(E), all(-2 < r <= 0 for _, r, _ in pts)))
def frac3(x):  # 3-adic fractional part of x in Z[1/6]: x = n/(2^a 3^b)
    n, d = x.numerator, x.denominator
    b = 0
    while d % 3 == 0: d //= 3; b += 1
    return Fr((n * pow(d, -1, 3**b)) % 3**b, 3**b)
bad = 0
for h in [1, 2, 3, 5, 11, 1001, 3**7, -7, 2**K//3 + 1]:
    for c, r, P in pts:
        x = Fr(h) * r / M
        lhs = Fr(h * c, M)
        if (lhs - (x - frac3(x))).denominator != 1: bad += 1
print("mirror identity h*c/2^K == x - {x}_3 (mod 1): failures =", bad)
# ab/ba pairing: coefficient of T_{k-7}(xi/243) has modulus 2|cos(pi*11*xi*243^{-1}/2^k)|
random.seed(1); badp = 0
for _ in range(200):
    k = random.randint(8, 60); xi = random.randrange(1, 1 << k); Mk = 1 << k
    z1 = cmath.exp(2j*math.pi*((-xi*pow(9, -1, Mk)) % Mk)/Mk)
    z2 = cmath.exp(2j*math.pi*((-16*xi*pow(243, -1, Mk)) % Mk)/Mk)
    if abs(abs(z1+z2) - 2*abs(math.cos(math.pi*((11*xi*pow(243, -1, Mk)) % Mk)/Mk))) > 1e-9: badp += 1
print("ab/ba modulus formula failures:", badp)
# two-step recursion check against direct sums
def T(k, xi):
    Mk = 1 << k
    return sum(cmath.exp(2j*math.pi*((xi*c) % Mk)/Mk) for c in Ek(k))
badr = 0
for _ in range(20):
    k = random.randint(8, 20); xi = random.randrange(1, 1 << k); Mk = 1 << k
    e = lambda n: cmath.exp(2j*math.pi*(n % Mk)/Mk)
    i3 = lambda p: pow(3, -p, Mk)
    rhs = e(-xi*i3(2) - 8*xi*i3(4))*T(k-6, (xi*i3(4)) % (1 << (k-6))) \
        + (e(-xi*i3(2)) + e(-16*xi*i3(5)))*T(k-7, (xi*i3(5)) % (1 << (k-7))) \
        + T(k-8, (xi*i3(6)) % (1 << (k-8)))
    if abs(T(k, xi) - rhs) > 1e-6: badr += 1
print("2-block recursion failures:", badr)
# zeta-family: T^zeta = sum_v e(-{zeta f_v(z)}_3)  (zeta in Z_3); Collatz: zeta = -h 2^{-K}, plus tiny real phase
Pm = max(P for _, _, P in pts); M3 = 3**Pm
def Tz(zeta):
    s = 0
    for c, r, P in pts:
        n = int(r * M3) % M3                       # r = n/3^Pm
        s += cmath.exp(-2j*math.pi*((zeta*n) % M3)/M3)
    return abs(s)
N = len(pts)
print("zeta=1: |T|/N = %.4f ; zeta=2: %.4f ; zeta=1/5: %.4f ; zeta=1/11: %.4f" % (Tz(1)/N, Tz(2)/N, Tz(pow(5, -1, M3))/N, Tz(pow(11, -1, M3))/N))
rs = [Tz(random.randrange(M3))/math.sqrt(N) for _ in range(20)]
print("random zeta: |T|/sqrt(N) mean %.3f max %.3f" % (sum(rs)/len(rs), max(rs)))
z = (-pow(2, -K, M3)) % M3
print("Collatz zeta=-2^-K: |T^zeta|/sqrt(N) = %.3f ; true |T_K(1)|/sqrt(N) = %.3f" % (Tz(z)/math.sqrt(N), abs(T(K, 1))/math.sqrt(N)))
