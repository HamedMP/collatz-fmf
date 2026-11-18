# Referee script 1: independent simulator, residue-class claim, Theorem B finite form.
import itertools, sys
from math import gcd

def step(w):
    if w % 8 == 7: return 'a', (9*w+1)//8
    if w % 16 == 0: return 'b', 27*w//16
    return None, None

def itin(w, maxlen):
    s = []
    while len(s) < maxlen:
        l, w2 = step(w)
        if l is None: break
        s.append(l); w = w2
    return ''.join(s)

def Bw(v): return 3*v.count('a') + 4*v.count('b')

def has_prefix(w, u):
    for ch in u:
        l, w = step(w)
        if l != ch: return False
    return True

# ---- 1a. brute force: all w in [0, N) grouped by itinerary prefix
N = 1 << 21
from collections import defaultdict
groups = defaultdict(list)
for w in range(0, N):
    s = itin(w, 8)
    for n in range(1, len(s)+1):
        groups[s[:n]].append(w)
bad = 0; checked = 0; rep = {}
for n in range(1, 9):
    for t in itertools.product('ab', repeat=n):
        u = ''.join(t); B = Bw(u); L = groups.get(u, [])
        if B <= 21:
            # must be exactly one class mod 2^B
            if len(L) != N >> B or len({w % (1 << B) for w in L}) != 1:
                bad += 1; print('BAD class', u, len(L))
            else: rep[u] = L[0] % (1 << B)
            checked += 1
        else:
            if len({w % (1 << B) for w in L}) > 1: bad += 1; print('BAD class(large)', u)
print('1a: words with B<=21 fully brute-forced:', checked, 'bad:', bad)

# ---- 1b. forward lift (own derivation) for every word len<=8, verified by simulation
def classes(maxlen):
    # returns dict u -> (r, B) ; forward extension
    out = {'': (0, 0, 0, 0)}  # r, B, e(pow of 3), W (image of r)
    res = {}
    frontier = {'': (0, 0, 1, 0)}  # r, B, 3^e, W_r  ; w = r + 2^B s -> W_r + 3^e s
    for n in range(maxlen):
        new = {}
        for u, (r, B, p3, W) in frontier.items():
            # a: W + p3*s == 7 mod 8
            s = ((7 - W) * pow(p3, -1, 8)) % 8
            r2 = r + (s << B); W2 = W + p3 * s
            assert W2 % 8 == 7
            new[u+'a'] = (r2, B+3, p3*9, (9*W2+1)//8)
            s = ((0 - W) * pow(p3, -1, 16)) % 16
            r2 = r + (s << B); W2 = W + p3 * s
            assert W2 % 16 == 0
            new[u+'b'] = (r2, B+4, p3*27, 27*W2//16)
        res.update(new); frontier = new
    return res
cl = classes(8)
bad = 0
for u, (r, B, p3, W) in cl.items():
    assert B == Bw(u)
    if u in rep and rep[u] != r: bad += 1; print('rep mismatch', u)
    for k in (0, 1, 2, 3, 12345):
        if not has_prefix(r + (k << B), u): bad += 1; print('lift fails', u)
    # no other class mod 2^B: half-shift must fail
    if has_prefix(r + (1 << (B-1)), u): bad += 1; print('half shift also works', u)
print('1b: all', len(cl), 'words len<=8: lift verified, bad:', bad)

# ---- 1c. Theorem B finite form
def class_of(P):
    r, B, p3, W = 0, 0, 1, 0
    for ch in P:
        if ch == 'a':
            s = ((7 - W) * pow(p3, -1, 8)) % 8
            r += s << B; W += p3*s; B += 3; p3 *= 9; W = (9*W+1)//8
        else:
            s = ((-W) * pow(p3, -1, 16)) % 16
            r += s << B; W += p3*s; B += 4; p3 *= 27; W = 27*W//16
    return r, B

def concl(w0, BX):
    return (w0+1)**4 * 3**(9*BX) > 2**(16*BX)

words = [''.join(t) for n in range(1, 5) for t in itertools.product('ab', repeat=n)]
KM = int(sys.argv[1]) if len(sys.argv) > 1 else 7
from fractions import Fraction
import math
viol = 0; cases = 0; minratio = 1e9; arg = None
viol33 = 0; min33 = 1e9; arg33 = None
simchk = 0
for X in words:
    BX = Bw(X)
    for Y in words:
        shapes = [('cc', X+X)]
        for k in range(1, KM+1):
            for j in range(1, KM+1):
                shapes.append((f'c d^{k} c^{j} d', X + Y*k + X*j + Y))
        for name, P in shapes:
            r, B = class_of(P)
            w0 = r if r > 0 else (1 << B)
            if cases % 97 == 0:
                assert has_prefix(w0, P); simchk += 1
                assert w0 < (1 << B) or r == 0
            cases += 1
            if not concl(w0, BX):
                viol += 1; print('VIOLATION', X, Y, name, w0)
            q = math.log2(w0+1)/BX
            if q < minratio: minratio, arg = q, (X, Y, name, w0)
            # smallest w0 == 32 mod 33 in class
            M = 1 << B
            t = ((32 - r) * pow(M, -1, 33)) % 33
            w33 = r + t*M
            if w33 == 0: w33 = 33*M
            assert w33 % 33 == 32 and w33 % M == r
            if not concl(w33, BX):
                viol33 += 1; print('VIOLATION33', X, Y, name, w33)
            q = math.log2(w33+1)/BX
            if q < min33: min33, arg33 = q, (X, Y, name, w33)
print('1c: cases', cases, 'violations', viol, 'min log2(w0+1)/B(X) =', minratio, arg, 'threshold 0.43383; sim-checked', simchk)
print('1c (w0=32 mod 33): violations', viol33, 'min ratio', min33, arg33)
