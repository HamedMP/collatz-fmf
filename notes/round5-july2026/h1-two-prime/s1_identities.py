"""s1_identities.py — exact verification of the two-prime (2-adic x 3-adic) structure
of the binary return map T(n) = (3*27^r*w - 85)/88, 33n+32 = 16^r*w.

All arithmetic exact (Python ints). Checks:
 A. Block map <-> T formula; gate = one class mod 2^(4r+3); eps_r = 7 (r even) / 5 (r odd) mod 8 on w;
    mod-11 part of the 88-divisibility automatic (27 == 16 mod 11).
 B. One-step transfer identity: 88*T(n) + 85 = 3^(3r+1) * w, w == 2 mod 3, w odd.
    (v_3 exactly 3r+1, leading unit 2 — the word letter is 3-adically readable from the NEXT state.)
 C. v_3(D_r) = 0, D_r == 1 mod 3; D_r mod 3^k cycles with period 3^(k-1) in r (ord_{3^k}(16) = 3^(k-1)).
 D. Composed prefix data: P_N = 3^(2N+3S), Q_N = 2^(3N+4S), v_3(D_N) = 0, 0 < D_N < P_N.
 E. MIRROR IDENTITY (new): U_N = V_N, where U_N = (P_N R_N + D_N)/Q_N (auxiliary 2-adic state of the
    least prefix residue) and V_N = least nonneg residue of D_N * Q_N^{-1} mod 3^(2N+3S_N).
 F. Suffix filtration (new): D_N/Q_N == D_suf/Q_suf mod 3^(v3(P_suf)) for every suffix split,
    and the congruence FAILS one level higher generically (spike sharpness).
 G. State determinism: for any word w alive at depth N and seed M == R_N (mod Q_N), the T-orbit of M
    follows w exactly for N steps, and n_N = (P_N M + D_N)/Q_N; if M = R_N < Q_N then n_N = V_N.
 H. Seed 3-adic freeness (CRT): for an alive word and every class c mod 3^k, there is a seed
    following the word with seed == c mod 3^k.
"""
import itertools, random, sys
from math import gcd

def v2(x):
    return (x & -x).bit_length() - 1

def v3(x):
    v = 0
    while x % 3 == 0:
        x //= 3
        v += 1
    return v

def T_step(n):
    """Return (n', r) if the return block applies at n, else (None, kill_type)."""
    x = 33 * n + 32
    t = v2(x)
    if t % 4 != 0:
        return None, 'K1'
    r = t // 4
    w = x >> t
    need = 7 if r % 2 == 0 else 5
    if w % 8 != need:
        return None, 'K2'
    num = 3 * 27**r * w - 85
    assert num % 88 == 0, (n, r, w)   # mod-8 fixed => mod-11 must be automatic
    n2 = num // 88
    return n2, r

def block_data(r):
    P = 9 * 27**r
    Q = 2**(4*r+3)
    D = 1 if r == 0 else (96 * 27**r - 85 * 16**r) // 11
    if r >= 1:
        assert (96 * 27**r - 85 * 16**r) % 11 == 0
    return P, Q, D

def compose(word):
    P, Q, D = 1, 1, 0
    for r in word:
        p, q, d = block_data(r)
        D = p * D + d * Q
        P *= p
        Q *= q
    return P, Q, D

# ---------- A: block map vs T; gate class uniqueness ----------
print("== A: block/gate structure ==")
for r in range(0, 6):
    P, Q, D = block_data(r)
    assert P == 3**(3*r+2)
    assert Q == 2**(4*r+3)
    # the gate class: solve P n + D == 0 mod Q -> one class mod 2^(4r+3)
    Pinv = pow(P, -1, Q)
    n0 = (-D * Pinv) % Q
    # every n in that class: v2(33n+32) == 4r and w in the right class mod 8
    for tcase in range(3):
        n = n0 + tcase * Q
        x = 33*n + 32
        assert v2(x) == 4*r, (r, n)
        w = x >> (4*r)
        assert w % 8 == (7 if r % 2 == 0 else 5)
        n2, rr = T_step(n)
        assert rr == r
        assert n2 == (P*n + D)//Q and (P*n + D) % Q == 0
print("  block map == T on gate classes, r=0..5: OK")
print("  gate residues: one class mod 2^(4r+3) per r; w == 7 (r even) / 5 (r odd) mod 8: OK")
assert 27 % 11 == 16 % 11   # reason the mod-11 part is automatic
print("  27 == 16 mod 11 (odd-modulus automaticity): OK")

# ---------- B: one-step transfer identity ----------
print("== B: transfer identity 88*T(n)+85 = 3^(3r+1) w ==")
rng = random.Random(20260721)
cnt = 0
for _ in range(20000):
    r = rng.choice([0,0,0,1,1,2,3])
    P, Q, D = block_data(r)
    Pinv = pow(P, -1, Q)
    n = ((-D * Pinv) % Q) + rng.randrange(0, 1 << 40) * Q
    x = 33*n + 32
    w = x >> (4*r)
    n2, rr = T_step(n)
    assert rr == r
    lhs = 88*n2 + 85
    assert lhs == 3**(3*r+1) * w
    assert w % 3 == 2 and w % 2 == 1
    assert v3(lhs) == 3*r + 1        # exact valuation
    cnt += 1
print(f"  {cnt} random gated states: 88T+85 = 3^(3r+1)w, w==2 mod 3, v3 exact: OK")

# ---------- C: v3(D_r), cycling ----------
print("== C: D_r 3-adic structure ==")
for r in range(0, 40):
    P, Q, D = block_data(r)
    assert v3(D) == 0
    assert D % 3 == 1
print("  v3(D_r)=0 and D_r == 1 mod 3 for r=0..39: OK")
for k in range(1, 8):
    m = 3**k
    o = 1
    acc = 16 % m
    while acc != 1:
        acc = (acc * 16) % m
        o += 1
    assert o == 3**(k-1), (k, o)
print("  ord_{3^k}(16) = 3^(k-1) for k=1..7: OK  (=> D_r mod 3^k cycles with period 3^(k-1) once 3r+1 >= k)")
# check the cycling claim itself: for k with 3r+1 >= k, D_r == -85*16^r/11 mod 3^k
for k in range(1, 7):
    m = 3**k
    inv11 = pow(11, -1, m)
    for r in range(max(1, (k+2)//3), 12):
        P, Q, D = block_data(r)
        if 3*r+1 >= k:
            assert D % m == (-85 * pow(16, r, m) * inv11) % m
print("  D_r == -85*16^r/11 mod 3^k whenever 3r+1 >= k: OK")

# ---------- D,E: composed data and the mirror identity ----------
print("== D,E: composed prefix data + MIRROR U_N = V_N ==")
words = []
for L in range(1, 6):
    for w in itertools.product(range(0, 4), repeat=L):
        words.append(w)
rng2 = random.Random(7)
for _ in range(400):
    L = rng2.randrange(6, 14)
    words.append(tuple(rng2.choice([0,0,0,1,1,2,3,4,5]) for _ in range(L)))
checked = 0
for w in words:
    N = len(w)
    S = sum(w)
    P, Q, D = compose(w)
    assert P == 3**(2*N+3*S)
    assert Q == 2**(3*N+4*S)
    assert v3(D) == 0 and 0 < D < P
    R = (-D * pow(P, -1, Q)) % Q          # least prefix residue (2-adic data)
    U = (P * R + D) // Q                  # auxiliary state
    assert (P * R + D) % Q == 0
    V = (D * pow(Q, -1, P)) % P           # least residue of the composed 3-adic class
    assert U == V, (w, U, V)              # THE MIRROR IDENTITY
    assert 0 <= U < P
    checked += 1
print(f"  {checked} words (exhaustive r<=3,L<=5 + 400 random up to L=13,r<=5): U_N = V_N always: OK")

# ---------- F: suffix filtration ----------
print("== F: suffix filtration of the composed 3-adic class ==")
viol_sharp = 0
tested = 0
for w in words[:2000]:
    N = len(w)
    P, Q, D = compose(w)
    for J in range(1, N):
        suf = w[J:]
        Ps, Qs, Ds = compose(suf)
        c = v3(Ps)                        # = 2(N-J) + 3*sum(suf)
        m = 3**c
        lhs = (D * pow(Q, -1, m)) % m
        rhs = (Ds * pow(Qs, -1, m)) % m
        assert lhs == rhs, (w, J)
        # sharpness: one level higher the letter r_{J-1}'s unit enters; generically differs
        m2 = 3**(c+1)
        if (D * pow(Q, -1, m2)) % m2 != (Ds * pow(Qs, -1, m2)) % m2:
            viol_sharp += 1
        tested += 1
print(f"  D_N/Q_N == D_suf/Q_suf mod 3^(v3(P_suf)) for all {tested} splits: OK")
print(f"  congruence breaks at one level higher in {viol_sharp}/{tested} splits (spike enters; sharp)")

# ---------- G: formal word = deterministic orbit; n_N = V_N when M = R_N < Q_N ----------
print("== G: determinism + state formula ==")
det_checked = 0
for w in words:
    N = len(w)
    P, Q, D = compose(w)
    R = (-D * pow(P, -1, Q)) % Q
    for lift in (0, 1, 5):
        M = R + lift * Q
        n = M
        ok = True
        for j, r in enumerate(w):
            out = T_step(n)
            if out[0] is None or out[1] != r:
                ok = False
                break
            n = out[0]
        assert ok, (w, M)
        assert n == (P * M + D) // Q
        if lift == 0:
            V = (D * pow(Q, -1, P)) % P
            assert n == V                # states of the minimal representative = 3-adic least residues
        det_checked += 1
print(f"  {det_checked} (word, seed) pairs: T-orbit follows the word; n_N=(P M+D)/Q; n_N=V_N at M=R_N: OK")

# ---------- H: seed 3-adic freeness ----------
print("== H: seed mod 3^k freeness (CRT) ==")
free_checked = 0
for w in words[:200]:
    N = len(w)
    P, Q, D = compose(w)
    R = (-D * pow(P, -1, Q)) % Q
    for k in (1, 2, 3):
        mk = 3**k
        for c in range(mk):
            # CRT: M == R mod Q, M == c mod 3^k
            M = (R * mk * pow(mk, -1, Q) + c * Q * pow(Q, -1, mk)) % (Q * mk)
            assert M % Q == R and M % mk == c
            n = M
            for j, r in enumerate(w):
                out = T_step(n)
                assert out[0] is not None and out[1] == r
                n = out[0]
            free_checked += 1
print(f"  {free_checked} (word, class-mod-3^k) pairs all realizable: seed 3-adic data forces NOTHING: OK")

print("\nALL s1 CHECKS PASSED")
