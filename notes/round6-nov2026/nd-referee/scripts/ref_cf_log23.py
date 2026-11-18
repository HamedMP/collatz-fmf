"""Continued fraction of log2(3): min over q <= Q of ||q b||*q, and of ||q b||*q^7.616, q^13.3 (referee check).
||q b|| is minimised at convergent denominators, so only convergents (and q=1) need testing."""
from mpmath import mp, mpf, log, floor, nint
mp.dps = 400
b = log(3) / log(2)
x = b; h0, h1, k0, k1 = 0, 1, 1, 0
amax = 0; worst1 = mpf(10); rows = []
for i in range(300):
    a = int(floor(x)); x = 1 / (x - a) if x != a else None
    h0, h1 = h1, a * h1 + h0; k0, k1 = k1, a * k1 + k0
    q = k1
    if q > mpf(10) ** 150: break
    d = abs(q * b - nint(q * b))
    if i > 0: amax = max(amax, a)
    worst1 = min(worst1, d * q)
    rows.append((i, a, q, d))
print("partial quotients (first 30):", [r[1] for r in rows[:30]])
print("convergent denominators (first 14):", [r[2] for r in rows[:14]])
print(f"number of convergents with q <= 1e150: {len(rows)};  max partial quotient: {amax}")
print(f"min over these q of ||q b|| * q        = {float(worst1):.6f}")
print(f"min over these q of ||q b|| * q^7.616  = {float(min(r[3]*mpf(r[2])**mpf('7.616') for r in rows)):.6f}  (attained at q=1: ||b||={float(abs(b-nint(b))):.6f})")
print(f"explicit Rhin-(7) consequence 2^-13.3/ln2 = {float(mpf(2)**mpf('-13.3')/log(2)):.3e} <= ||q b|| q^13.3 : holds trivially on this range")
