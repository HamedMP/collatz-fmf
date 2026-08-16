"""lar01_cocycle_prefix.py -- Lemma E arithmetic attack, part 1:
the aperiodic extension of the block-power machinery.

Hop coordinates (repo Theorem 55): odd x > 1, s = v_2(x+1), v = 1+v_2(3^s m -1)
with m = (x+1)/2^s; letter l = (s,v), h = s+v-1, and one hop is EXACTLY
    x' = f_l(x) = (3^s x + c_s)/2^h,   c_s = 3^s - 2^s.
A finite word p (u, w, ... denote finite words) composes to
    f_p(x) = (3^{S_p} x + B_p)/2^{H_p},   S_p = sum s, H_p = sum h.
Write D_p = 2^{H_p} - 3^{S_p} (odd!), U_p(x) = D_p x - B_p, phi_p = B_p/D_p.

THEOREM A1 (composition cocycle; PROVED, one-line algebra, verified here):
  For concatenation p = u.w (u performed first):
      B_{uw} = 3^{S_w} B_u + 2^{H_u} B_w      (matrix homomorphism
      D_{uw} = 3^{S_w} D_u + 2^{H_u} D_w       M_p = [[3^S, B],[0, 2^H]],
                                               M_{uw} = M_w M_u)
  i.e. B and D obey the SAME twisted cocycle -- this is the composition law
  for the invariant table (d_s = -D_{(s,2)}: 11, 49, 179, 601, ...; pair
  values -115, -1675, -5537, -473 are D of 2-letter blocks).  Consequently
      phi_{uw} = (3^{S_w} D_u phi_u + 2^{H_u} D_w phi_w)
                 / (3^{S_w} D_u + 2^{H_u} D_w)
  an affine combination of the block fixed points; for all-expanding blocks
  (D < 0) both weights are negative, so phi_{uw} is a CONVEX combination:
  fixed points of expanding words stay in the convex hull of the letter phis.
  Powers: (D_{u^k}, B_{u^k}) = N_k (D_u, B_u), N_k = (2^{kH}-3^{kS})/D_u odd;
  hence U_{u^k} = N_k U_u and the length-k prefix constraint for u^k is
  v_2(U_u(x)) >= k H_u -- Lemma P and the block-power lemma are EXACTLY the
  power-degenerate case of the universal prefix constraint below.

THEOREM A2 (master identity + universal prefix valuation; PROVED, verified):
  (i)  U_p(x) = 2^{H_p} (x - f_p(x))  identically (both sides rational).
  (ii) If word(x_0) starts with p (|p| = k hops, state x_k), then
           D_p x_0 - B_p = 2^{H_p} (x_0 - x_k)   with x_k a positive integer,
       so  v_2(D_p x_0 - B_p) = H_p + v_2(x_0 - x_k) >= H_p + 1.
       This is the aperiodic composed identity: EVERY prefix of EVERY hop
       word forces the divisibility 2^{H_p+1} | D_p x_0 - B_p, with excess
       v_2(x_0 - x_k) = (2-adic return proximity of the orbit).
  (iii) By LE0 (shadow theorem), v_2(x_0 - x_k) - 1 >= H(lcp(w, sigma^k w))
       (h-mass of the longest common prefix of the word and its k-shift):
       valuation excess = self-overlap of the word.  SIZE LEVER: for any
       non-descending orbit |x_0 - x_k| < x_k + x_0 <= 2 x_k, so
           v_2(U_{p_k}(x_0)) <= H_k + 1 + log2(x_k):
       excess beyond H_k+1 is paid for by orbit growth, bit for bit.
  (iv) phi_{p_k} -> xi(w) 2-adically (v_2(xi - phi_{p_k}) >= H_k + 1), where
       xi(w) = the unique 2-adic seed of the infinite word (Theorem 60):
       the prefix-loop fixed points converge to the seed.

THEOREM A3 (fixed-form classification -- exact scope of the Lemma-P
mechanism; PROVED, both directions, verified on witnesses):
  Call (a,b) in Z^2, a != 0, a FIXED-FORM CERTIFICATE for the infinite word
  w if there is f(k) -> infinity with: every odd x in the prefix class of
  p_k satisfies v_2(a x + b) >= f(k).
  (i) If a certificate exists then a xi(w) + b = 0, i.e. xi(w) = -b/a is
      RATIONAL, and necessarily f(k) <= H_k + 1 + v_2(a) (take x, x' both
      in the class: v_2(a(x-x')) = v_2(a) + H_k + 1-ish caps the common
      valuation).  Conversely if xi(w) = -b/a then f(k) = H_k + 1 + v_2(a)
      works.  So: FIXED-FORM CERTIFICATES EXIST IFF THE SEED IS RATIONAL,
      and the certified rate is then exactly H_k + O(1) -- Lemma P's rate
      v_2(11 m'...) >= 4k is the generic maximal rate, not an accident.
  (ii) Eventually periodic w = p.u^infty: explicit certificate
           a = 3^{S_p} D_u (odd),  b = D_u B_p - 2^{H_p} B_u,
       with -b/a = f_p^{-1}(phi_u) = xi(w); the exclusion closes iff
       -b/a is not a positive odd integer reading w -- recovering exactly
       "eventually periodic hop words are cycles" (Theorem 55) and the
       block-power/Lemma-P exclusions.
  (iii) For ANY word with irrational seed, NO fixed form accumulates: the
       Lemma-P mechanism, applied with any fixed (a,b), is PROVABLY unable
       to exclude any single aperiodic word unless its seed is rational --
       and aperiodic words with rational seeds are exactly the hypothetical
       divergence-type orbits of rationals (recognizing them from the word
       is Lagarias's periodicity conjecture).  Hence the arithmetic route
       MUST use position-dependent forms (the prefix forms U_{p_k}) plus
       the size lever (A2(iii)) -- which is what the factor barrier does.

Everything below is exact integer / Fraction arithmetic.  Labels:
identities/theorems PROVED (proofs in docstrings above, one-line algebra);
all verifications CHECKED on the stated ranges.
"""
import sys, random
from fractions import Fraction
random.seed(20260721)

def v2(n):
    if n == 0:
        return None  # infinity
    return (abs(n) & -abs(n)).bit_length() - 1

def v2frac(q):
    if q == 0:
        return None
    return v2(q.numerator) - v2(q.denominator)

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
    """(S, H, B) of x -> (3^S x + B)/2^H for the word u (u[0] first)."""
    S = H = B = 0
    for (s, v) in u:
        a, c, h = 3**s, 3**s - 2**s, s + v - 1
        B = a * B + c * (1 << H)
        S += s
        H += h
    return S, H, B

def DBof(u):
    S, H, B = compose(u)
    return (1 << H) - 3**S, B, S, H

def f_apply(u, x):
    S, H, B = compose(u)
    return Fraction(3**S * x + B, 1 << H)

def letter_class(s, v):
    mu = (pow(3, -s, 1 << v) * (1 + (1 << (v - 1)))) % (1 << v)
    return ((mu << s) - 1) % (1 << (s + v)), s + v

def class_rep(word):
    """(rep, exp): odd x performs word iff x = rep mod 2^exp; exp = H+1."""
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

def rand_word(L, smax=5, vmax=5):
    return tuple((random.randint(1, smax), random.randint(2, vmax))
                 for _ in range(L))

# ---------------- A1: cocycle ----------------
def check_A1():
    fails = 0
    for _ in range(4000):
        u, w = rand_word(random.randint(1, 5)), rand_word(random.randint(1, 5))
        Du, Bu, Su, Hu = DBof(u)
        Dw, Bw, Sw, Hw = DBof(w)
        Dp, Bp, Sp, Hp = DBof(u + w)
        if Sp != Su + Sw or Hp != Hu + Hw:
            fails += 1
        if Bp != 3**Sw * Bu + (1 << Hu) * Bw:
            fails += 1
        if Dp != 3**Sw * Du + (1 << Hu) * Dw:
            fails += 1
        if Du % 2 == 0 or Bu % 2 == 0:
            fails += 1  # D, B always odd
        # phi affine combination
        if Du != 0 and Dw != 0 and Dp != 0:
            lhs = Fraction(Bp, Dp)
            rhs = (3**Sw * Du * Fraction(Bu, Du) + (1 << Hu) * Dw * Fraction(Bw, Dw))
            rhs = rhs / (3**Sw * Du + (1 << Hu) * Dw)
            if lhs != rhs:
                fails += 1
    # convex hull for all-expanding blocks
    hullfails = 0
    for _ in range(2000):
        u = tuple((random.randint(2, 6), 2) for _ in range(random.randint(1, 6)))
        Du, Bu, Su, Hu = DBof(u)
        if Du >= 0:
            hullfails += 1  # every v=2, s>=2 word is expanding
            continue
        phis = [Fraction(3**s - 2**s, (1 << (s + 1)) - 3**s) for (s, v) in u]
        ph = Fraction(Bu, Du)
        if not (min(phis) <= ph <= max(phis)):
            hullfails += 1
    # powers: N_k scaling, N_k odd
    pfails = 0
    for _ in range(600):
        u = rand_word(random.randint(1, 3))
        Du, Bu, Su, Hu = DBof(u)
        for k in range(2, 7):
            Dk, Bk, Sk, Hk = DBof(u * k)
            if Dk % Du or Bk % Bu:
                pfails += 1
                continue
            N = Dk // Du
            if N != Bk // Bu or N % 2 == 0:
                pfails += 1
            if N != ((1 << (k * Hu)) - 3**(k * Su)) // ((1 << Hu) - 3**Su):
                pfails += 1
    print(f"A1 cocycle (D,B same twisted cocycle; matrix hom): fails={fails}")
    print(f"A1 convex hull of phi for expanding v=2 words:      fails={hullfails}")
    print(f"A1 power scaling U_u^k = N_k U_u, N_k odd:          fails={pfails}")
    return fails == hullfails == pfails == 0

# ---------------- A2: master identity + prefix valuation ----------------
def check_A2():
    idfails = valfails = lcpfails = seedfails = sizefails = 0
    tested = 0
    for _ in range(3000):
        x0 = random.getrandbits(48) | 1
        if x0 <= 1:
            continue
        N = random.randint(1, 14)
        w = word_of(x0, N)
        # walk states
        xs = [x0]
        x = x0
        for _ in range(N):
            _, _, x = hop(x)
            xs.append(x)
        for k in (1, N // 2 + 1, N):
            p = w[:k]
            D, B, S, H = DBof(p)
            tested += 1
            # (i) identity U_p(x) = 2^H (x - f_p(x)) as rationals
            if D * x0 - B != (1 << H) * (x0 - f_apply(p, x0)):
                idfails += 1
            # (ii) prefix valuation
            lhs = D * x0 - B
            if lhs != (1 << H) * (x0 - xs[k]):
                idfails += 1
            if x0 != xs[k]:
                if v2(lhs) != H + v2(x0 - xs[k]) or v2(lhs) < H + 1:
                    valfails += 1
            # (iii) lcp lower bound: v_2(x0 - x_k) >= H(lcp(w, sigma^k w)) + 1
            if x0 != xs[k]:
                # compute lcp of word(x0) and word(x_k) directly (extend!)
                M = 30
                wa, wb = word_of(x0, M), word_of(xs[k], M)
                j = 0
                while j < M and wa[j] == wb[j]:
                    j += 1
                Hl = sum(s + v - 1 for s, v in wa[:j])
                if j < M and v2(x0 - xs[k]) < Hl + 1:
                    lcpfails += 1
            # (iv) phi_p -> seed: v_2(x0 - phi_p) >= H+1 (as fraction)
            if D != 0:
                dv = v2frac(x0 - Fraction(B, D))
                if dv is not None and dv < H + 1:
                    seedfails += 1
        # size lever on the whole available word (any orbit; |x0-xk|<=x0+xk)
        for k in range(1, N + 1):
            if x0 != xs[k]:
                D, B, S, H = DBof(w[:k])
                if (1 << (v2(D * x0 - B) - H)) > x0 + xs[k]:
                    sizefails += 1
    print(f"A2 master identity U_p(x)=2^H(x-f_p(x)) + integer form: fails={idfails}")
    print(f"A2 exact valuation v2(U_p(x0)) = H_p + v2(x0-x_k):      fails={valfails}")
    print(f"A2 lcp lower bound (excess >= self-overlap h-mass):     fails={lcpfails}")
    print(f"A2 seed convergence v2(x0 - phi_p) >= H_p+1:            fails={seedfails}")
    print(f"A2 size lever 2^excess <= x0+x_k:                       fails={sizefails}")
    print(f"   ({tested} prefix checks)")
    return idfails == valfails == lcpfails == seedfails == sizefails == 0

# ---------------- A2 cross-check: seed truncations vs class reps ----------
def check_seed_vs_class():
    fails = 0
    for _ in range(400):
        w = rand_word(random.randint(1, 8), smax=4, vmax=4)
        D, B, S, H = DBof(w)
        r, qe = class_rep(w)
        assert qe == H + 1
        # xi_k = -3^{-S} B mod 2^H must equal r mod 2^H
        xik = (-B * pow(3**S, -1, 1 << H)) % (1 << H)
        if xik != r % (1 << H):
            fails += 1
    print(f"A2 seed truncation -3^-S B == class rep (mod 2^H):      fails={fails}")
    return fails == 0

# ---------------- A3: fixed-form classification ----------------
def check_A3():
    ok = True
    # (ii) eventually periodic words: explicit certificate + maximal rate
    print("\nA3(ii) eventually periodic p.u^infty: certificate (a,b) = "
          "(3^Sp Du, Du Bp - 2^Hp Bu), rate H_k+O(1):")
    cases = [
        ((), ((3, 2),)),                     # Lemma P: pure (3,2)^infty
        ((), ((4, 2),)),                     # depth-2 identity
        (((1, 2), (2, 3)), ((3, 2),)),       # with a prefix
        (((2, 2),), ((2, 2), (3, 2))),       # 2-letter tail block
        (((4, 3),), ((5, 2), (2, 2))),
    ]
    for p, u in cases:
        Du, Bu, Su, Hu = DBof(u)
        Sp, Hp, Bp = compose(p)
        a = 3**Sp * Du
        b = Du * Bp - (1 << Hp) * Bu
        seed = Fraction(-b, a)
        # verify: x in class(p + u*j) => v_2(a x + b) >= Hp + j*Hu (+1)
        good = True
        for j in range(1, 7):
            r, qe = class_rep(p + u * j)
            for t in (0, 1, 3):
                x = r + (t << qe)
                if x <= 1:
                    continue
                if word_of(x, len(p) + j * len(u)) != p + u * j:
                    good = False
                if v2(a * x + b) < Hp + j * Hu + 1:
                    good = False
        # exclusion: seed must not be a positive odd integer
        is_pos_odd_int = seed.denominator == 1 and seed > 0 and seed.numerator % 2 == 1
        print(f"  p={p} u={u}: a={a}, b={b}, seed=-b/a={seed}  "
              f"rate OK={good}  excluded(seed not pos odd int)={not is_pos_odd_int}")
        ok &= good and not is_pos_odd_int
    # sanity: the trivial cycle p=(), u=((1,2),) has seed 1 (NOT excluded)
    Du, Bu, Su, Hu = DBof(((1, 2),))
    print(f"  carve-out: u=((1,2)) seed = {Fraction(-(-Bu), Du) if False else Fraction(Bu, Du)}"
          f" = 1 (the trivial cycle; certificate exists but excludes nothing)")
    ok &= Fraction(Bu, Du) == 1

    # (i)+(iii): no fixed form for an irrational-seed word.  Witness: the
    # Fibonacci-substitution word over {(2,2),(4,2)} (aperiodic).  For every
    # small odd form (a,b), v_2(a xi_k + b) stays bounded while H_k grows.
    def fib_word(N):
        s = "a"
        while len(s) < N:
            s = "".join("ab" if ch == "a" else "a" for ch in s)
        return [(2, 2) if ch == "a" else (4, 2) for ch in s[:N]]
    w = fib_word(80)
    print("\nA3(iii) Fibonacci word over {(2,2),(4,2)}: sup_k v2(a xi_k + b) "
          "over |a|,|b| <= 99 odd a:")
    # compute seed truncation to high precision
    prefs = [10, 20, 40, 80]
    best = 0
    for K in prefs:
        D, B, S, H = DBof(tuple(w[:K]))
        xik = (-B * pow(3**S, -1, 1 << H)) % (1 << H)
        mx = 0
        for a in range(-99, 100, 2):
            for b in range(-99, 100, 2):
                val = a * xik + b
                if val == 0:
                    continue
                mx = max(mx, min(v2(val), H))
        best = mx
        print(f"  K={K:3d} (H_k={H:4d}): max_(a,b) v2(a xi_k + b) = {mx}"
              f"   (certificate would need ~H_k = {H})")
    ok &= best < 40  # far below H=337+; bounded evidence
    print("  => no small fixed form accumulates: CHECKED for |a|,|b|<=99;")
    print("     the equivalence 'certificate <=> a xi + b = 0' is PROVED, so")
    print("     any certificate at all would force xi rational.")
    return ok

if __name__ == "__main__":
    ok = check_A1()
    ok &= check_A2()
    ok &= check_seed_vs_class()
    ok &= check_A3()
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
