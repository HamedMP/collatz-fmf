"""ret.py -- exact-arithmetic core for the binary return partial map (track h1).

Multiplier a (a=3 is Collatz; a=5 is the 5n+1 litmus).  For a=3:
    P_r = 9*27^r, Q_r = 2^(4r+3), D_0 = 1, D_r = (96*27^r - 85*16^r)/11,
    gate 33n+32 = 16^r w, w = 7 (r even) / 5 (r odd) mod 8,
    T(n) = (P_r n + D_r)/Q_r = (3*27^r*w - 85)/88.
All functions use Python ints only.
"""
from math import gcd


def v2(x):
    assert x != 0
    return (x & -x).bit_length() - 1


def vp(x, p):
    assert x != 0
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def block(r):
    """(P_r, Q_r, D_r) for a = 3."""
    P = 9 * 27**r
    Q = 1 << (4 * r + 3)
    if r == 0:
        D = 1
    else:
        num = 96 * 27**r - 85 * 16**r
        assert num % 11 == 0
        D = num // 11
    return P, Q, D


def T_step(n):
    """One step of the return partial map on any integer n (positive or negative).
    Returns (n', r) or (None, None) if undefined."""
    y = 33 * n + 32
    if y == 0:
        return None, None
    t = v2(y)
    if t % 4:
        return None, None
    r = t // 4
    w = y >> t
    if w % 8 != (7 if r % 2 == 0 else 5):
        return None, None
    num = 3 * 27**r * w - 85
    assert num % 88 == 0
    return num // 88, r


def orbit_word(n, maxlen=10**9):
    """Forced return word of n (list of letters) and the list of states."""
    word, states = [], [n]
    while len(word) < maxlen:
        m, r = T_step(n)
        if m is None:
            break
        word.append(r)
        states.append(m)
        n = m
    return word, states


def compose(word):
    """(P_W, Q_W, D_W) with Q_W n_N = P_W n_0 + D_W."""
    P, Q, D = 1, 1, 0
    for r in word:
        p, q, d = block(r)
        P, Q, D = p * P, q * Q, p * D + d * Q
    return P, Q, D


def least_residue(word):
    """R_W = least non-negative n with the return word W, and Q_W, U_W."""
    P, Q, D = compose(word)
    R = (-D * pow(P, -1, Q)) % Q
    U = (P * R + D) // Q
    return R, Q, U


def sfree(x, primes=(2, 3)):
    """S-free part of |x| (remove all factors from `primes`)."""
    x = abs(x)
    for p in primes:
        while x % p == 0:
            x //= p
    return x
