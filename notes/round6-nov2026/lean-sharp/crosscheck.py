"""Exact (Fraction) cross-checks of the Lean statements in lean-sharp."""
from fractions import Fraction as F
import math, random

def T(x): return x // 2 if x % 2 == 0 else (3 * x + 1) // 2
def traj(n, k):
    xs = [n]
    for _ in range(k): xs.append(T(xs[-1]))
    return xs
def odd_count(k, n): return sum(v % 2 for v in traj(n, k)[:k])

# 1. product identity (exact), incl. the Lean guards n = 27, 7 at k = 5
for n in list(range(0, 300)) + [random.getrandbits(80) for _ in range(200)]:
    xs = traj(n, 60)
    for k in range(0, 61):
        prod = F(1)
        for v in xs[:k]:
            if v % 2 == 1: prod *= 1 + F(1, 3 * v)
        assert xs[k] * 2**k == n * 3**odd_count(k, n) * prod, (n, k)
print("product identity OK;",
      "n=27:", traj(27, 5), odd_count(5, 27), "n=7:", traj(7, 5), odd_count(5, 7))

# 2. cycle 1 -> 2 -> 1 and clog
assert T(T(1)) == 1 and odd_count(2, 1) == 1 and (4 - 1).bit_length() == 2
assert math.exp(2 / 3) < 2

# 3. landing bound T^j(x) < 3^(a+1) for x < 2^(j+1)
for j in range(0, 13):
    for x in range(0, 2**(j + 1)):
        assert traj(x, j)[j] < 3**(odd_count(j, x) + 1)
print("landing OK")

# 4. parameter conditions of sojourn_abstract
def G(P, Q, d, k): return k**(P + Q - 1) * k**P / ((k**P - 1) * k**(d + 1))
for (P, Q, d, nu, ka, A, q) in [(8, 5, 24, F(16, 15), F(8, 7), 9, F(39, 20)),
                                (65, 41, 211, F(126, 125), F(251, 247), 10, F(9661, 5000))]:
    assert 3**Q <= 2**P and P <= d + 1 and nu >= 1 and ka > 1
    assert 1 + nu**P <= ka**Q * nu**Q
    assert 1 + nu**d + A * G(P, Q, d, ka) <= A * (ka**Q - 1)
    assert ka**Q <= q
    Amin = (1 + nu**d) / (ka**Q - 1 - G(P, Q, d, ka))
    print("params", P, Q, d, nu, ka, "q=", float(ka**Q), "A_min=", float(Amin), "A=", A)

# 5. sojourn bound on real stretches; guard value for 27
xs = traj(27, 75)
assert xs.index(1) == 70 and len(set(xs[:71])) == 71
print("27: count below 32 among first 71 =", sum(1 for v in xs[:71] if v < 32))
worst = 0
for n in range(1, 20001):
    xs = [n]
    while xs[-1] != 1: xs.append(T(xs[-1]))
    for L in range(0, 20):
        c = sum(1 for v in xs if v < 2**L)
        assert c <= 10 * F(9661, 5000)**L and c <= 9 * F(39, 20)**L
        worst = max(worst, c / float(F(9661, 5000)**L))
print("sojourn OK n<=20000; max count/1.9322^L =", worst)
q = F(9661, 5000)
print("beats trivial 2^L-1 from L =", min(L for L in range(1, 200) if 10 * q**L < 2**L - 1))

# 6. HarmonicSharp constants
assert F(26, 15)**2 >= 3 and F(41, 29)**2 <= 2 and (1 + F(26, 15)) / (2 * F(41, 29)) == F(29, 30)
print("H constant:", float((30 * 4 + 1) / (1 - F(2, 8))), "exp(54) =", math.exp(54))
