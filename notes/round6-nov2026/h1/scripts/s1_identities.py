"""s1_identities.py -- exact machine check of the identities used in REPORT.md.

Run:  python s1_identities.py           (expected last line: ALL IDENTITY CHECKS PASSED)

 I1. v-coordinate block form.  v = 8(33n+32) = 2^(4r+3) w  (w odd)  ==>  v' = 8(33T(n)+32) = 3^(3r+2) w + 1.
 I2. Collatz-type sum identity for a word (r_0..r_s) from any admissible start:
        2^(A_s) w_s = 3^(B_s) w_0 + sum_{l=1}^{s} 3^(b_l+...+b_{s-1}) 2^(a_1+...+a_{l-1}),
     a_l = 4 r_l + 3, b_l = 3 r_l + 2, A_s = a_1+..+a_s, B_s = b_0+..+b_{s-1};
     all s unit terms are positive {2,3}-units, the l=1 term is a pure power of 3 and the l=s term
     a pure power of 2 (so gcd of the unit terms is 1), and their sum is <= 3^(B_s).
 I3. m-coordinate form: m = n+1, m' = (3^(3r+2) m - kappa_r)/2^(4r+3), kappa_r = 3(27^r-16^r)/11 >= 0.
 I4. Mahler form: for a start M with word of length >= N, n_N = E_N*(M - M_N), with
     M_N = -D_N/P_N in [-1,0) strictly decreasing; and for every finite prefix
     n_N/E_N <= n_{N+1}/E_{N+1} and (n_{N+1}+1)/E_{N+1} <= (n_N+1)/E_N  (nested intervals).
 I5. Negative world: T(-1) = -1 with letter 0; for n <= -2, |T(n)+1| > (9/8)|n+1|; the only integer
     preimage of -1 is -1.
 I6. Same checks I1, I2 for negative starts (signs: w_0 < 0), exhibiting the vanishing subsum at n = -1.
 I7. a = 5 analogue of I1/I2 (5n+1 litmus): v = 2^(4r+3) w -> 5^(3r+2) w + c5  (derived numerically
     from the repo's P_r = 25*125^r, D_r = (160*125^r - 51*16^r)/109).
"""
import random
import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ret import block, T_step, orbit_word, compose, least_residue, v2  # noqa: E402

random.seed(20261117)
checks = 0


def rand_word(L, pmax=6):
    w = []
    for _ in range(L):
        r = 0
        while random.random() < 0.45 and r < pmax:
            r += 1
        w.append(r)
    return w


# ---------- I1, I2 on least residues of random words and on random lifts ----------
for trial in range(4000):
    L = random.randint(1, 9)
    word = rand_word(L)
    R, Q, U = least_residue(word)
    n0 = R + Q * random.randint(0, 50)
    got, states = orbit_word(n0, maxlen=L)
    assert got == word, (word, got)
    vs = [8 * (33 * n + 32) for n in states]
    a = [4 * r + 3 for r in word]
    b = [3 * r + 2 for r in word]
    ws = []
    for j in range(L):
        assert v2(vs[j]) == a[j]
        ws.append(vs[j] >> a[j])
        assert vs[j + 1] == 3 ** b[j] * ws[j] + 1          # I1
        checks += 1
    # I2 with s = L-1 (needs the valuation of the last state; use word[0..s])
    s = L - 1
    if s >= 1:
        A = sum(a[1:s + 1])
        B = sum(b[0:s])
        units = [3 ** sum(b[l:s]) * 2 ** sum(a[1:l]) for l in range(1, s + 1)]
        assert (1 << A) * ws[s] == 3 ** B * ws[0] + sum(units)
        assert units[0] == 3 ** sum(b[1:s]) and units[-1] == 2 ** sum(a[1:s])
        assert sum(units) <= 3 ** B
        assert all(u > 0 for u in units)
        checks += 1

# ---------- I3 ----------
for r in range(0, 40):
    P, Q, D = block(r)
    kappa = P - Q - D
    assert kappa * 11 == 3 * (27 ** r - 16 ** r) and kappa >= 0
    for n in (-7, -1, 0, 5, 10 ** 9 + 7):
        m = n + 1
        assert Fraction(P * n + D, Q) + 1 == Fraction(3 ** (3 * r + 2) * m - kappa, Q)
    checks += 1

# ---------- I4 ----------
for trial in range(1500):
    L = random.randint(1, 10)
    word = rand_word(L)
    R, Q, U = least_residue(word)
    M = R + Q * random.randint(0, 3)
    _, states = orbit_word(M, maxlen=L)
    prevM = Fraction(0)
    P, Qc, D = 1, 1, 0
    for N in range(1, L + 1):
        p, q, d = block(word[N - 1])
        P, Qc, D = p * P, q * Qc, p * D + d * Qc
        MN = Fraction(-D, P)
        assert -1 <= MN < prevM <= 0
        E = Fraction(P, Qc)
        assert states[N] == E * (M - MN)
        if N < L:
            p2, q2, d2 = block(word[N])
            E2 = E * Fraction(p2, q2)
            assert Fraction(states[N]) / E <= Fraction(states[N + 1]) / E2
            assert Fraction(states[N + 1] + 1) / E2 <= Fraction(states[N] + 1) / E
        prevM = MN
        checks += 1

# ---------- I5 ----------
assert T_step(-1) == (-1, 0)
for n in range(-200000, -1):
    m, r = T_step(n)
    if m is not None:
        assert abs(m + 1) * 8 > 9 * abs(n + 1)
        assert m != -1
        checks += 1
for r in range(0, 60):
    P, Q, D = block(r)
    num = Q * (-1) - D
    assert (num % P == 0) == (r == 0)
checks += 1

# ---------- I6: negative starts, same identities, vanishing subsum at -1 ----------
neg_found = 0
for n0 in range(-400000, 0):
    word, states = orbit_word(n0, maxlen=6)
    L = len(word)
    if L < 2:
        continue
    neg_found += 1
    vs = [8 * (33 * n + 32) for n in states]
    a = [4 * r + 3 for r in word]
    b = [3 * r + 2 for r in word]
    ws = [vs[j] >> a[j] if j < L else None for j in range(L + 1)]
    for j in range(L):
        assert vs[j + 1] == 3 ** b[j] * ws[j] + 1
    s = L - 1
    A = sum(a[1:s + 1]); B = sum(b[0:s])
    units = [3 ** sum(b[l:s]) * 2 ** sum(a[1:l]) for l in range(1, s + 1)]
    assert (1 << A) * ws[s] == 3 ** B * ws[0] + sum(units)
    checks += 1
    # no vanishing non-empty subsum of the Theorem-2 vector x = (3^B w_0, units), also for w_0 < 0
    x = [3 ** B * ws[0]] + units
    for mask in range(1, 1 << len(x)):
        assert sum(x[i] for i in range(len(x)) if mask >> i & 1) != 0
    checks += 1
# The seed -1 (w_0 = -1, word 0^infinity): x = (-9^s, 9^(s-1), 9^(s-2)*8, ..., 8^(s-1)), sum = -8^s.
# Evertse's Theorem 2 applies (no vanishing subsum) and reads 1 * 8^(-s) >= C(eps,s) * 9^(-s*eps):
# TRUE for each fixed s, but it forces C(eps, s) <= (9^eps/8)^s -> 0.  Recorded for the litmus section.
for s in range(1, 14):
    units = [9 ** (s - l) * 8 ** (l - 1) for l in range(1, s + 1)]
    x = [-(9 ** s)] + units
    assert sum(x) == -(8 ** s)
    for mask in range(1, 1 << len(x)):
        assert sum(x[i] for i in range(len(x)) if mask >> i & 1) != 0
    checks += 1
print("neg starts with >=2 blocks checked:", neg_found)

# ---------- I7: a = 5 ----------
def block5(r):
    P = 25 * 125 ** r
    Q = 1 << (4 * r + 3)
    num = 160 * 125 ** r - 51 * 16 ** r
    assert num % 109 == 0
    return P, Q, num // 109

# find the affine coordinate v = alpha*n + beta in which every block reads v -> (P_r/Q_r) v + c
# with the same c: need (P_r - Q_r) * beta/alpha... solve: v' = alpha*(P n + D)/Q + beta
#  = (P/Q) (alpha n + beta) + [alpha D/Q + beta - P beta/Q]; constant c = (alpha D_r + beta (Q_r - P_r))/Q_r
# independent of r.  For a = 3: alpha = 264, beta = 256, c = 1.
for (blk, alpha, beta, c) in ((block, 264, 256, 1), (block5, 872, 816, 1)):
    for r in range(0, 30):
        P, Q, D = blk(r)
        assert Fraction(alpha * D + beta * (Q - P), Q) == c, (r, Fraction(alpha * D + beta * (Q - P), Q))
        checks += 1

print("checks:", checks)
print("ALL IDENTITY CHECKS PASSED")
