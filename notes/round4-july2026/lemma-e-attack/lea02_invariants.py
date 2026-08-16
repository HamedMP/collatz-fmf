"""lea02_invariants.py -- Lemma E attack, part 2: the exact invariant /
denominator structure of the (s,v) block maps (the machinery that produced
Lemma P's 11-adic identity), block-power bounds, and the complete
constant-letter classification.

For a finite hop word u with S = sum s, H = sum h, the composed map is
    x' = (3^S x + B_u)/2^H,   B_u > 0,
and with D_u = 2^H - 3^S, phi_u = B_u/D_u, U(x) = D_u x - B_u:
    U(x') = 3^S U(x) / 2^H          (exact identity, both signs of D).

BLOCK-POWER LEMMA (PROVED):  if the hop word of x contains u^k starting at
position j (k complete blocks; the state after the last block exists because
F is total), then
    v_2( D_u x_j - B_u ) >= k * H_u,     unless x_j = phi_u.
x_j = phi_u forces phi_u to be a positive odd integer and the orbit to be a
Collatz cycle with |u| FMF hops per period.
  - single letters: a 1-hop cycle; excluded for every letter != (1,2)
    (Steiner 1977 1-circuit theorem; also Hercher 2023 m<=91 via the repo's
    Theorem 53 identity FMF hops = Simons-de Weger m).  (1,2) gives x=1.
  - |u| <= 91: excluded by Hercher m <= 91.
CONSEQUENCES (PROVED):
  - EFFECTIVE RUN BOUND: the number of consecutive u-blocks readable from
    state x is <= v_2(D_u x - B_u)/H_u  (x != phi_u); generalizes Lemma P
    (u=(3,2): v_2(11x+19) >= 4k) to every letter and block:
        (2,2): v_2(x+5)      >= 3k
        (4,2): v_2(49x+65)   >= 5k        <- the depth-2 identity asked for
        (5,2): v_2(179x+211) >= 6k
    m-coordinate forms (x = 2^s m - 1): (3,2): 16(11m'+1)=27(11m+1) [Lemma P];
        (2,2): 8(m'+1)=9(m+1);  (4,2): 32(49m'+1)=81(49m+1);
        general (s,2): 2^(s+1)*(d_s m' + 1) = 3^s (d_s m + 1), d_s = 3^s-2^(s+1).
  - no orbit's hop word ends in u^infty for ANY u with |u| <= 91 (else a
    nontrivial cycle with <= 91 hops).  For all-expanding u (e.g. any u over
    {(s,2): s>=2}) the exclusion is unconditional for every |u|:
    cycles need 2^H > 3^S.
This script verifies all identities exactly and prints the tables.
"""
import sys, random
from fractions import Fraction
random.seed(20260721)

def v2(n):
    return (n & -n).bit_length() - 1

def hop(x):
    s = v2(x + 1)
    m = (x + 1) >> s
    core = 3**s * m - 1
    vv = 1 + v2(core)
    return s, vv, core >> (vv - 1)

def word_of(x, N):
    w = []
    for _ in range(N):
        s, vv, x = hop(x)
        w.append((s, vv))
    return tuple(w)

def compose(u):
    """Affine data (S, H, B) of the block map x -> (3^S x + B)/2^H."""
    A, B, H = 1, 0, 0
    S = 0
    for (s, v) in u:
        a, c, h = 3**s, 3**s - 2**s, s + v - 1
        A, B, H = a * A, a * B + c * (1 << H), H + h
        S += s
    assert A == 3**S
    return S, H, B

def letter_class(s, v):
    mu = (pow(3, -s, 1 << v) * (1 + (1 << (v - 1)))) % (1 << v)
    return ((mu << s) - 1) % (1 << (s + v)), s + v

def class_rep(word):
    (s, v) = word[-1]
    r, qe = letter_class(s, v)
    for (s, v) in reversed(word[:-1]):
        h = s + v - 1
        c = 3**s - 2**s
        rho, _ = letter_class(s, v)
        x0p = (3**s * rho + c) >> h
        need = (r - x0p) % (1 << qe)
        t = ((need >> 1) * pow(3**s, -1, 1 << (qe - 1))) % (1 << (qe - 1))
        r = (rho + (t << (h + 1))) % (1 << (h + qe))
        qe = h + qe
    return r, qe

def factorize(n):
    n = abs(n)
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def fstr(n):
    if abs(n) == 1:
        return str(n)
    f = factorize(n)
    s = "*".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
    return ("-" if n < 0 else "") + s

# ---------------- identity check ----------------
def check_identity():
    fails = 0
    for trial in range(3000):
        L = random.randint(1, 4)
        u = tuple((random.randint(1, 5), random.randint(2, 5)) for _ in range(L))
        S, H, B = compose(u)
        D = (1 << H) - 3**S
        x = Fraction(random.getrandbits(30) | 1)
        xp = (3**S * x + B) / (1 << H)
        if D * xp - B != Fraction(3**S, 1 << H) * (D * x - B):
            fails += 1
    print(f"U-identity U(x')=3^S U(x)/2^H on 3000 random blocks: fails={fails}")
    return fails == 0

# ---------------- single-letter table ----------------
def letter_table():
    print("\nSingle-letter invariant table: x' = (3^s x + B)/2^h, D = 2^h - 3^s,")
    print("phi = B/D, identity 2^h*(|D| x' + sgn*B) = 3^s*(|D| x + sgn*B):")
    print(f"{'(s,v)':7s} {'h':>2s} {'D':>10s} {'B':>8s} {'phi':>12s}  "
          f"{'|D| factored':16s} expanding?")
    for s in range(1, 7):
        for v in range(2, 7):
            h = s + v - 1
            D = (1 << h) - 3**s
            B = 3**s - (1 << s)
            phi = Fraction(B, D) if D else None
            exp = 3**s > (1 << h)
            mark = " <== fixed point x=1" if (s, v) == (1, 2) else ""
            print(f"({s},{v})   {h:2d} {D:10d} {B:8d} {str(phi):>12s}  "
                  f"{fstr(D):16s} {'YES' if exp else 'no '}{mark}")
    print("m-coordinate identities (x = 2^s m - 1), v=2 letters:")
    for s in range(2, 7):
        d = 3**s - (1 << (s + 1))
        print(f"  (s={s}): 2^{s+1}*({d} m' + 1) = 3^{s}*({d} m + 1)   "
              f"[d = 3^{s}-2^{s+1} = {fstr(d)}]")

# ---------------- constant-letter classification ----------------
def check_classification(SMAX=300):
    hits = []
    for s in range(1, SMAX + 1):
        p3 = 3**s
        # candidates: 3^s < 2^(s+v-1) <= 2*3^s - 2^s  (D>0 and D <= B)
        v = 2
        while (1 << (s + v - 1)) <= p3:
            v += 1
        while (1 << (s + v - 1)) <= 2 * p3 - (1 << s):
            D = (1 << (s + v - 1)) - p3
            B = p3 - (1 << s)
            if B % D == 0 and (B // D) % 2 == 1 and B // D > 0:
                hits.append((s, v, B // D))
            v += 1
    print(f"\nConstant-letter classification scan s <= {SMAX}: positive odd "
          f"integer fixed points: {hits}")
    print("  => phi in Z_{>0} only for (1,2) (x=1).  For ALL (s,v) this is")
    print("     PROVED unconditionally: any other phi would be a 1-hop cycle,")
    print("     excluded by Steiner 1977 (and by Hercher m<=91 + Theorem 53).")
    return hits == [(1, 2, 1)]

# ---------------- pair table ----------------
def pair_table():
    letters = [(s, v) for s in range(1, 5) for v in range(2, 5)]
    print("\nPair blocks u = (l1,l2): D_u = 2^H - 3^S (the invariant modulus / "
          "denominator structure):")
    bad = []
    shown = 0
    for l1 in letters:
        for l2 in letters:
            u = (l1, l2)
            S, H, B = compose(u)
            D = (1 << H) - 3**S
            if D != 0 and B % D == 0 and B // D > 0 and (B // D) % 2 == 1:
                if not all(l == (1, 2) for l in u):
                    bad.append((u, B // D))
            if l1 <= l2 and l1[1] == 2 and l2[1] == 2:
                print(f"  u={u}: S={S:2d} H={H:2d}  D={D:8d} = {fstr(D):14s} "
                      f"B={B:6d}  phi={Fraction(B, D)}")
                shown += 1
    print(f"  2-hop positive odd integer fixed points besides (1,2)^2: {bad}")
    print("  (none expected: a hit would be a 2-hop cycle, dead by Hercher)")
    return bad == []

# ---------------- block-power lemma verification ----------------
def check_block_power():
    fails = tested = 0
    # (a) constructed: x in the class of u^k must satisfy v_2(D x - B) >= k H
    blocks = [((3, 2),), ((4, 2),), ((2, 2),), ((5, 2),), ((2, 2), (3, 2)),
              ((3, 2), (4, 2)), ((1, 3), (2, 2)), ((4, 2), (2, 3))]
    for u in blocks:
        S, H, B = compose(u)
        D = (1 << H) - 3**S
        for k in range(1, 6):
            w = u * k
            r, qe = class_rep(w)
            for j in range(3):
                x = r + (1 << qe) * j
                if x <= 1:
                    continue
                # confirm the word really starts with u^k
                if word_of(x, len(w)) != w:
                    fails += 1
                    print("power class FAIL", u, k)
                    continue
                tested += 1
                if x * D == B:
                    continue
                if v2(D * x - B) < k * H:
                    fails += 1
                    print("block-power FAIL", u, k, x)
    # (b) sharpness + converse direction on random states: run length observed
    #     vs bound v_2(D x - B)/H for single letters
    for trial in range(20000):
        x = random.getrandbits(40) | 1
        if x <= 1:
            continue
        s, vv, _ = hop(x)
        u = ((s, vv),)
        S, H, B = compose(u)
        D = (1 << H) - 3**S
        if D * x == B:
            continue
        bound = v2(D * x - B) // H
        # actual run of letter (s,vv)
        k, y = 0, x
        while True:
            ss, vv2, y2 = hop(y)
            if (ss, vv2) != (s, vv):
                break
            k += 1
            y = y2
            if k > bound + 2:
                break
        tested += 1
        if k > bound:
            fails += 1
            print("run-bound FAIL", x, (s, vv), k, bound)
    print(f"\nblock-power lemma + run bounds: {tested} checks, fails={fails}")
    # Lemma P cross-check in x-form: v_2(11x+19) >= 4k for (3,2)^k
    r, qe = class_rep(((3, 2),) * 5)
    x = r if r > 1 else r + (1 << qe)
    print(f"  Lemma P x-form: x={x} starts (3,2)^5, v_2(11x+19) = "
          f"{v2(11 * x + 19)} >= 20 ? {v2(11 * x + 19) >= 20}")
    # depth-2 identity: v_2(49x+65) >= 5k for (4,2)^k
    r, qe = class_rep(((4, 2),) * 5)
    x = r if r > 1 else r + (1 << qe)
    print(f"  depth-2 form: x={x} starts (4,2)^5, v_2(49x+65) = "
          f"{v2(49 * x + 65)} >= 25 ? {v2(49 * x + 65) >= 25}")
    return fails == 0

if __name__ == "__main__":
    ok = check_identity()
    letter_table()
    ok &= check_classification()
    ok &= pair_table()
    ok &= check_block_power()
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
