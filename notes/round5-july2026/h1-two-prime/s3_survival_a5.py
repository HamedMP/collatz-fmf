"""s3_survival_a5.py — the a=5 (5n+1) litmus for the two-prime pincer.

Derived structure for a=5 (verified here from scratch):
  gate variable: 545 n + 32 = 16^r * w   (545 = 5*109, 109 = 5^3 - 16)
  block: n' = (P_r n + D_r)/Q_r, P_r = 25*125^r = 5^(3r+2), Q_r = 2^(4r+3),
         D_r = (160*125^r - 51*16^r)/109  (D_0 = 1)
  return map: T5(n) = (5*125^r w - 51)/872,  872 = 8*109, 51 = 32*5 - 109
  transfer identity: 872*T5(n) + 51 = 5^(3r+1) * w, w == 2 mod 5  (5-adic mirror of 88T+85=3^(3r+1)w)
  gate mod 8 on w: w == 7 (r even) / 3 (r odd);  mod-109 part automatic since 125 == 16 mod 109.

Checks: all identities; mirror U_N = V_N (5-adic); survival census M <= 10^6 with kill mechanisms;
special seeds: the genuine 5n+1 cycle member 13 (F_5(13)=13) and the (believed divergent) orbit of 7.
"""
import itertools, random
from collections import Counter

def v2(x):
    return (x & -x).bit_length() - 1

def v5(x):
    v = 0
    while x % 5 == 0:
        x //= 5
        v += 1
    return v

def block_data5(r):
    P = 25 * 125**r
    Q = 2**(4*r+3)
    if r == 0:
        D = 1
    else:
        assert (160 * 125**r - 51 * 16**r) % 109 == 0
        D = (160 * 125**r - 51 * 16**r) // 109
    return P, Q, D

def T5_step(n):
    x = 545 * n + 32
    t = v2(x)
    if t % 4 != 0:
        return None, 'K1'
    r = t // 4
    w = x >> t
    if w % 8 != (7 if r % 2 == 0 else 3):
        return None, 'K2'
    num = 5 * 125**r * w - 51
    assert num % 872 == 0, (n, r, w)
    return num // 872, r

def compose5(word):
    P, Q, D = 1, 1, 0
    for r in word:
        p, q, d = block_data5(r)
        D = p * D + d * Q
        P *= p
        Q *= q
    return P, Q, D

print("== structural identities, a=5 ==")
assert 125 % 109 == 16 % 109
assert 109 == 5**3 - 16 and 51 == 32*5 - 109 and 872 == 8*109 and 545 == 5*109
# also re-express a=3 constants in the same dictionary
assert 11 == 3**3 - 16 and 85 == 32*3 - 11 and 88 == 8*11 and 33 == 3*11
print("  dictionary: modulus a^3-16 (11 <-> 109), gate var a(a^3-16)n+32, const 32a-(a^3-16) (85 <-> 51): OK")
rng = random.Random(5)
for r in range(0, 5):
    P, Q, D = block_data5(r)
    assert P == 5**(3*r+2) and Q == 2**(4*r+3)
    assert D % 5 != 0            # v5(D_r) = 0
    Pinv = pow(P, -1, Q)
    n0 = (-D * Pinv) % Q
    for tcase in range(3):
        n = n0 + tcase * Q
        x = 545*n + 32
        assert v2(x) == 4*r
        w = x >> (4*r)
        assert w % 8 == (7 if r % 2 == 0 else 3)
        n2, rr = T5_step(n)
        assert rr == r and n2 == (P*n + D)//Q
        lhs = 872*n2 + 51
        assert lhs == 5**(3*r+1) * w and w % 5 == 2
        assert v5(lhs) == 3*r+1
print("  gate class mod 2^(4r+3); w == 7/3 mod 8 by parity of r; 872T5+51 = 5^(3r+1)w, w==2 mod 5: OK")

# mirror U = V, a=5
words = [w for L in range(1, 5) for w in itertools.product(range(0, 3), repeat=L)]
for _ in range(300):
    L = rng.randrange(5, 11)
    words.append(tuple(rng.choice([0,0,0,1,1,2,3]) for _ in range(L)))
for w in words:
    N, S = len(w), sum(w)
    P, Q, D = compose5(w)
    assert P == 5**(2*N+3*S) and Q == 2**(3*N+4*S)
    assert D % 5 != 0 and 0 < D < P
    R = (-D * pow(P, -1, Q)) % Q
    U = (P*R + D)
    assert U % Q == 0
    U //= Q
    V = (D * pow(Q, -1, P)) % P
    assert U == V, w
print(f"  mirror U_N = V_N verified on {len(words)} words (5-adic side): OK")

print("== survival census, a=5, seeds 1..10^6 ==")
LIMIT = 10**6
hist = Counter(); kills = Counter(); step_events = Counter()
firsts = {}
maxL, argmax = -1, None
for M in range(1, LIMIT+1):
    n = M
    L = 0
    while True:
        x = 545*n + 32
        t = v2(x)
        if t % 4 != 0:
            kills['K1'] += 1; step_events['K1'] += 1
            break
        r = t//4
        w = x >> t
        if w % 8 != (7 if r % 2 == 0 else 3):
            kills['K2'] += 1; step_events['K2'] += 1
            break
        step_events['OK'] += 1
        n = (5 * 125**r * w - 51) // 872
        assert n > 0
        L += 1
        if L not in firsts:
            firsts[L] = M
    hist[L] += 1
    if L > maxL:
        maxL, argmax = L, M
tot = sum(hist.values())
cum = tot
print("  L : count : P(>=L) vs (2/15)^L")
for L in sorted(hist):
    print(f"    L={L:2d}  {hist[L]:8d}   P(>= {L}) = {cum/tot:.6g}   (2/15)^{L} = {(2/15)**L:.6g}")
    cum -= hist[L]
k1, k2 = kills['K1'], kills['K2']
print(f"  kill split K1:K2 = {k1/(k1+k2):.5f}:{k2/(k1+k2):.5f}  (heuristic {7/13:.5f}:{6/13:.5f})")
se = step_events; tots = sum(se.values())
print(f"  per-step: OK {se['OK']/tots:.5f} (2/15) K1 {se['K1']/tots:.5f} (7/15) K2 {se['K2']/tots:.5f} (6/15)")
print("  mu_L:", ", ".join(f"mu_{L}={firsts[L]}" for L in sorted(firsts)))
print(f"  max depth {maxL} at M={argmax}")

print("== special 5n+1 seeds ==")
for M in [13, 33, 83, 7, 9, 11]:
    n = M; wd = []
    while True:
        out = T5_step(n)
        if out[0] is None:
            print(f"  seed {M}: word {wd}, dies by {out[1]} after {len(wd)} blocks")
            break
        n = out[0]; wd.append(out[1])
        if len(wd) > 60:
            print(f"  seed {M}: SURVIVES > 60 blocks (!)", wd)
            break
