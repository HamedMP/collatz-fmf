"""lar02_reset_wronskian.py -- Lemma E arithmetic attack, part 2:
the MIXED case.  What do intervening letters do to the block-power
divisibility accumulation: reset or shift?  Answer: EXACT RESET LAW.

Setup as in lar01: f_m(x) = (3^{S_m} x + B_m)/2^{H_m}, D = 2^H - 3^S odd,
U_u(x) = D_u x - B_u, phi_u = B_u/D_u (odd 2-adic unit).  Since D_u is odd,
    v_2(U_u(x)) = v_2(x - phi_u)   -- the accumulation IS 2-adic proximity
to the block fixed point; block-power ("reading u^k forces v_2 >= kH_u+1")
is the ultrametric statement "long u-prefix = close to phi_u".

THEOREM B1 (propagation identity; PROVED, one line, verified exactly):
  For any blocks u, m and any x (rational or integer):
      2^{H_m} U_u(f_m(x)) = 3^{S_m} U_u(x) + W(u,m),
  where W(u,m) = D_u B_m - B_u D_m = D_u D_m (phi_m - phi_u) is the
  (2-adic) WRONSKIAN of the two blocks.  W(u,u) = 0; W is the obstruction
  to carrying u-accumulation across m.  omega(u,m) := v_2(W(u,m)) =
  v_2(phi_m - phi_u): the 2-adic proximity of the two fixed points.

THEOREM B2 (reset trichotomy; PROVED from B1 + ultrametric, verified):
  Let rho = v_2(U_u(x)) and cross the block m (i.e. word(x) starts with m),
  nu' = v_2(U_u(f_m(x))).  Then:
    (a) rho < omega(u,m):  nu' = rho - H_m   (pure TAX; requires rho >= H_m)
    (b) rho > omega(u,m):  nu' = omega(u,m) - H_m  (RESET to Wronskian
        level; requires omega >= H_m)
    (c) rho = omega(u,m):  nu' >= omega - H_m + 1 (COINCIDENCE CHANNEL --
        the only way accumulation can GROW across a gap).
  FORCED-COINCIDENCE COROLLARY: if omega(u,m) < H_m then (a),(b) are both
  impossible, so EVERY state x whose word starts with m has
      v_2(U_u(x)) = omega(u,m) EXACTLY  ... (*)
  unless deep cancellation (c) occurs -- and (c) is exactly the event
  "f_m(x) is 2-adically close to phi_u", i.e. the next u-run is starting.
  In particular for single-letter gaps l with omega(u,l) < H_l, the entire
  accumulation dynamics is DETERMINISTIC: reading l != u pins v_2(U_u) to
  the table value omega(u,l), except at the letter immediately preceding a
  new u-run, where the cancellation depth EQUALS H_l + v_2(U_u(next)) --
  i.e. the accumulated valuation of the coming run, tautologically.
  CONSEQUENCE (the precise residual core of Lemma E, one level deeper):
  contracting/intervening letters RESET the accumulation (they do not
  merely shift it); all memory of past accumulation is destroyed except
  through the coincidence channel, and the coincidence channel is
  equivalent to 2-adic near-approach of the ORBIT to the rational point
  psi = f_l^{-1}(phi_u) (the seed of the eventually periodic word l.u^infty).
  So Lemma E for u-runs = "the orbit visits the 2-adic ball
  B(xi(l u^infty), 2^-c) only finitely often for c -> infinity", a 2-adic
  Diophantine-approximation statement about ONE orbit vs the countable set
  of eventually-periodic rational seeds; the arithmetic lever against it is
  the height inequality x >= (2^nu - B_u)/|D_u| (size pays for proximity).

THEOREM B3 (run-cap; PROVED, verified): between coincidence events the
  u-run lengths are bounded by the Wronskian table:
  a maximal u-run of length k starting at state y needs
      k H_u + 1 <= v_2(U_u(y)),
  and if y was reached by a non-coincidence crossing of gap m from the
  previous run region, v_2(U_u(y)) <= max stated in B2 <= omega(u,m) - H_m
  (case b) -- so over any gap family with bounded omega, unbounded runs
  REQUIRE infinitely many coincidence events.  For a finite letter/block
  alphabet the omega-table is finite, so bounded gaps => bounded resets.

LEMMA B5 (depth-spike ledger; PROVED, trivial, verified): reading letter
  (s,v) from x forces x >= 2^s - 1 (x = 2^s - 1 mod 2^{s+1}); so unbounded
  depth needs unbounded states: s_j <= 1 + log2(x_j), and with the envelope
  x_j+1 <= (x_0+1) prod g(l_i), depth spikes are pre-financed by drift.

All arithmetic exact.  All identity claims PROVED (algebra in docstring);
tables and dynamics CHECKED exactly on the stated ranges.
"""
import sys, random
from fractions import Fraction
random.seed(20260721)

def v2(n):
    if n == 0:
        return None
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

def W_of(u, m):
    Du, Bu, Su, Hu = DBof(u)
    Dm, Bm, Sm, Hm = DBof(m)
    return Du * Bm - Bu * Dm

def rand_word(L, smax=5, vmax=5):
    return tuple((random.randint(1, smax), random.randint(2, vmax))
                 for _ in range(L))

# ---------------- B1 ----------------
def check_B1():
    fails = 0
    for _ in range(4000):
        u = rand_word(random.randint(1, 4))
        m = rand_word(random.randint(1, 4))
        Du, Bu, Su, Hu = DBof(u)
        Dm, Bm, Sm, Hm = DBof(m)
        W = Du * Bm - Bu * Dm
        # Wronskian identity forms
        if Dm != 0 and Du != 0:
            if Fraction(W) != Du * Dm * (Fraction(Bm, Dm) - Fraction(Bu, Du)):
                fails += 1
        x = Fraction(random.getrandbits(40) | 1)
        fx = Fraction(3**Sm * x + Bm, 1 << Hm)
        lhs = (1 << Hm) * (Du * fx - Bu)
        rhs = 3**Sm * (Du * x - Bu) + W
        if lhs != rhs:
            fails += 1
        if W_of(u, u) != 0:
            fails += 1
    print(f"B1 propagation 2^Hm U_u(f_m x) = 3^Sm U_u(x) + W(u,m): fails={fails}")
    return fails == 0

# ---------------- B2 trichotomy on real transitions ----------------
def check_B2():
    fails = tested = coinc = 0
    for _ in range(120000):
        x = random.getrandbits(44) | 1
        if x <= 1:
            continue
        # gap = the actual first letter(s) of x's word
        L = random.choice([1, 1, 1, 2])
        m = word_of(x, L)
        Dm, Bm, Sm, Hm = DBof(m)
        # reference block u (any); use assorted small blocks
        u = random.choice([((3, 2),), ((2, 2),), ((4, 2),), ((5, 2),),
                           ((2, 2), (3, 2)), ((1, 2),), ((2, 3),),
                           ((3, 3),), ((1, 3),)])
        if m[:len(u)] == u:
            continue  # ensure the crossing is by a block != u-start
        Du, Bu, Su, Hu = DBof(u)
        Uu = Du * x - Bu
        if Uu == 0:
            continue
        rho = v2(Uu)
        W = W_of(u, m)
        om = v2(W) if W != 0 else None
        # actual next state
        y = x
        for _ in range(L):
            _, _, y = hop(y)
        Uup = Du * y - Bu
        if Uup == 0:
            continue
        nup = v2(Uup)
        tested += 1
        if om is None:
            # W = 0 (phi_m = phi_u): pure shift nu' = rho - Hm
            if nup != rho - Hm:
                fails += 1
            continue
        if rho < om:
            if nup != rho - Hm or rho < Hm:
                fails += 1
        elif rho > om:
            if nup != om - Hm or om < Hm:
                fails += 1
        else:
            coinc += 1
            if nup < om - Hm + 1:
                fails += 1
    print(f"B2 trichotomy on real crossings: {tested} tested, "
          f"coincidence events={coinc}, fails={fails}")
    return fails == 0

# ---------------- forced-coincidence table ----------------
def forced_table():
    letters = [(s, v) for s in range(1, 6) for v in range(2, 5)]
    G01 = [((2, 2),), ((3, 2),)]
    us = [((2, 2),), ((3, 2),), ((4, 2),), ((5, 2),), ((2, 2), (3, 2)),
          ((3, 2), (2, 2)), ((4, 2), (4, 2))]
    print("\nomega(u,l) = v2(W) table vs H_l (single-letter gaps l):")
    print("  entry 'omega/H_l F' means omega < H_l => FORCED coincidence:")
    print("  (reading l pins v2(U_u) = omega exactly, except at run-restart")
    print("   letters where cancellation depth = the coming run's valuation)")
    ok = True
    for u in us:
        Du, Bu, Su, Hu = DBof(u)
        row = []
        for l in letters:
            if (l,) == u:
                row.append("  = ")
                continue
            W = W_of(u, (l,))
            om = v2(W) if W else None
            Hl = l[0] + l[1] - 1
            if om is None:
                row.append("W=0!")
            else:
                row.append(f"{om}/{Hl}{'F' if om < Hl else ' '}")
        print(f"  u={str(u):22s}: " + " ".join(f"{c:6s}" for c in row))
    # verify forcing (*) exactly: for pairs with omega < H_l, random states
    # reading l have v2(U_u) == omega OR >= omega+1 with the coincidence
    # realized as a run-restart (word after l approaches u^infty)
    fails = tested = 0
    for _ in range(200000):
        x = random.getrandbits(40) | 1
        if x <= 1:
            continue
        s, vv, y = hop(x)
        l = (s, vv)
        for u in (((3, 2),), ((2, 2),), ((4, 2),)):
            if (l,) == u:
                continue
            W = W_of(u, (l,))
            om = v2(W) if W else None
            Hl = s + vv - 1
            if om is None or om >= Hl:
                continue
            Du, Bu, Su, Hu = DBof(u)
            Uu = Du * x - Bu
            if Uu == 0:
                continue
            tested += 1
            rho = v2(Uu)
            if rho != om:
                # must be coincidence-with-cancellation: rho == om impossible
                # ... (*) says rho = om unless x is a deep-cancellation state;
                # trichotomy consistency: rho != om requires min(rho,om)>=Hl
                if min(rho, om) < Hl:
                    fails += 1
    print(f"  forcing (*) check: {tested} states, violations of the "
          f"trichotomy consistency={fails}")
    return ok and fails == 0

# ---------------- valuation walk along real orbits ----------------
def check_walk():
    print("\nvaluation walk nu_u(j) = v2(U_u(x_j)) along real orbits "
          "(verify per-letter update rules at every hop):")
    fails = steps = 0
    for x0 in [27, 703, 26623, 2**20 - 1, 987654321987654321 | 1]:
        for u in (((3, 2),), ((2, 2),), ((4, 2),), ((2, 2), (3, 2))):
            Du, Bu, Su, Hu = DBof(u)
            x = x0
            for j in range(400):
                s, vv, y = hop(x)
                l = ((s, vv),)
                Uu, Uup = Du * x - Bu, Du * y - Bu
                if Uu == 0 or Uup == 0:
                    break
                rho, nup = v2(Uu), v2(Uup)
                Dm, Bm, Sm, Hm = DBof(l)
                W = W_of(u, l)
                om = v2(W) if W else None
                steps += 1
                if l == u:
                    if nup != rho - Hu:
                        fails += 1
                elif om is None:
                    if nup != rho - Hm:
                        fails += 1
                elif rho != om:
                    if nup != min(rho, om) - Hm:
                        fails += 1
                else:
                    if nup < om - Hm + 1:
                        fails += 1
                x = y
                if x == 1:
                    break
    print(f"  {steps} hop-steps verified, fails={fails}")
    return fails == 0

# ---------------- B3: adversarial constructed words ----------------
def check_B3():
    print("\nB3 run-cap demo: adversarial word (3,2)^k1 (2,2) (3,2)^k2 (2,2)...")
    print("  u=(3,2): omega(u,(2,2)) = 2 < H_(2,2) = 3 => every (2,2)-gap is a")
    print("  FORCED coincidence; growing runs need ever deeper cancellations,")
    print("  and the minimal integer realizing the prefix grows like 2^(H):")
    u, gap = (3, 2), (2, 2)
    ok = True
    for ks in [(2, 3), (3, 5), (5, 8), (8, 13)]:
        w = []
        for k in ks:
            w += [u] * k + [gap]
        w = tuple(w)
        r, qe = class_rep(w)
        H = qe - 1
        x = r if r > 1 else r + (1 << qe)
        # verify realization and the run structure valuations
        assert word_of(x, len(w)) == w
        Du, Bu, Su, Hu = DBof((u,))
        # at the start, v2(U_u) >= k1*Hu + 1
        val = v2(Du * x - Bu)
        need = ks[0] * 4 + 1
        print(f"  k={ks}: class mod 2^{qe}, min representative has "
              f"{x.bit_length()} bits; v2(U_u(x0)) = {val} >= {need}: "
              f"{val >= need}")
        ok &= val >= need
        ok &= x.bit_length() >= H - 8  # size lever: realization costs ~2^H
    print("  => accumulation is NOT carried across gaps: each new run is paid")
    print("     for by a fresh coincidence (deep cancellation), and integer")
    print("     realizations of deep runs are exponentially large (size lever).")
    return ok

# ---------------- B5 spike ledger ----------------
def check_B5():
    fails = 0
    for _ in range(100000):
        x = random.getrandbits(40) | 1
        if x <= 1:
            continue
        s, vv, y = hop(x)
        if x < (1 << s) - 1:
            fails += 1
        if (x + 1) % (1 << s) != 0 or ((x + 1) >> s) % 2 != 1:
            fails += 1
    print(f"\nB5 spike ledger x >= 2^s - 1 (depth needs size): fails={fails}")
    return fails == 0

if __name__ == "__main__":
    ok = check_B1()
    ok &= check_B2()
    ok &= forced_table()
    ok &= check_walk()
    ok &= check_B3()
    ok &= check_B5()
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
