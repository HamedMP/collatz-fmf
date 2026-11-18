"""F_2[x] Collatz (S_3 form) helpers.  Polynomials are Python ints (bit i = coeff of x^i)."""
def s3(F):
    G = F ^ (F << 1)
    return G ^ (1 << (G.bit_length() - 1))
def t(F):
    k = 0
    while F != 1:
        F = s3(F); k += 1
    return k
def trace(F):
    """list of (level m, gap r) macro-steps; sum of gaps = t(F)."""
    out = []
    while F != 1:
        m = F.bit_length() - 1
        g = F ^ (1 << m)
        r = m - (g.bit_length() - 1)
        out.append((m, r))
        for _ in range(r): F = s3(F)
    return out
def T_collatz(f):
    """original Hicks et al. map"""
    return f >> 1 if f & 1 == 0 else (f ^ (f << 1) ^ 1)
def tmin(f):
    k = 0
    while f != 1:
        f = T_collatz(f); k += 1
    return k
def rev(f):
    n = f.bit_length()
    return int(bin(f)[2:][::-1], 2)
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
def ppow1(k):
    """(x+1)^k"""
    r = 1
    for _ in range(k): r ^= r << 1
    return r
