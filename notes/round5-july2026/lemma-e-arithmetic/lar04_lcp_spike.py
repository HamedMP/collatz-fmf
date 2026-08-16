"""lar04_lcp_spike.py -- Lemma E arithmetic attack, part 4:
(A) the word-combinatorial content of the Wronskian (omega = lcp formula),
(B) a NEW unconditional exclusion in the open unbounded-alphabet branch:
    the SPIKE-LEDGER THEOREM.

(A) THEOREM B4 (Wronskian = periodization overlap; EXACT FORMULA, PROVED):
    For blocks u, m (D_u, D_m odd; phi_u, phi_m odd 2-adic integers whose
    hop words are u^infty, m^infty), let q = lcp(u^infty, m^infty) and let
    (s,v) != (s',v') be the first disagreeing letters.  Then
        omega(u,m) = v_2(W(u,m)) = v_2(phi_m - phi_u)
                   = H_q + min(s, s')            if s != s',
                   = H_q + min(h, h')            if s = s', v != v'
    (h = s+v-1).  PROOF: f_q is affine with odd unit slope 3^{S_q}/2^{H_q},
    so v_2(phi_u - phi_m) = H_q + v_2(y - y') with y, y' the post-q states
    reading the disagreeing letters; s != s' gives v_2(y-y') =
    v_2((y+1)-(y'+1)) = min(s,s'); s = s', v != v' gives y+1 = 2^s m,
    y'+1 = 2^s m' and v_2(m - m') = v_2(3^s m - 1 - (3^s m' - 1)) =
    min(v-1, v'-1) since the two cores have distinct valuations v-1, v'-1.
    In particular omega >= H_q + 1 always, and omega is a PURE WORD
    FUNCTIONAL: the reset level of every crossing is word-combinatorial.
    DEGENERACY: W(u,m) = 0 iff phi_u = phi_m iff u^infty = m^infty iff
    u and m are powers of a common primitive block (Fine-Wilf direction
    verified).
    COROLLARY (PROVED, from the exact formula): if u starts with a letter
    of depth s_u >= 4 (any deep non-G01 run block) and m is ANY G01 gap
    block (first letter (2,2) or (3,2)), then q is empty and
        omega(u,m) = s_{m_1} in {2,3} < s_{m_1} + 1 <= H_m:
    EVERY crossing of a G01 gap by a deep-run reference block is a FORCED
    coincidence -- no divisibility accumulation is EVER carried across G01
    gaps into deep runs; each deep run is enabled by a fresh coincidence
    whose cancellation depth equals the full cost of the coming run.  (The
    reset law's bookkeeping consequence; size remains the only
    non-circular lever, cf. Theorem 60.)

(B) SPIKE-LEDGER THEOREM (PROVED; exact):  reading letter (s,v) from x
    forces x >= 2^s - 1 (B5), and every hop obeys the exact envelope
        x' + 1 <= (x + 1) g(l),  g(s,v) = (3^s + 2^{v-1} - 1)/2^{s+v-1}
    (lea01, re-verified in composed product form here).  Hence for ANY
    infinite hop word w = l_1 l_2 ... realized by ANY odd integer x_0 > 1:
        2^{s_j} <= (x_0 + 1) * prod_{i<j} g(l_i)   for every j.        (#)
    COROLLARY (new exclusion; first unconditional slice of the unbounded-
    alphabet branch): if
        sup_j [ s_j - sum_{i<j} log2 g(l_i) ] = infinity
    then w is realized by NO positive integer -- no complexity, recurrence,
    periodicity or descent hypothesis.  Sharp exact family: pure spike
    words ((s_1,2),(s_2,2),...) with s_{j+1}/s_j -> r:
      - r > 24727/15601 (= log2 3 + 2e-9): EXCLUDED (proved via the
        certified power inequality 3^q < 2^p => 3^s < 2^{ps/q} for all s);
      - r < log2 3: the ledger (#) is satisfiable (self-financing spikes)
        -- the criterion is sharp at r = log2 3 (honest boundary).
    In particular doubling spikes s_j = 2^j (and any super-geometric
    spikes) are excluded outright.  5n+1 LITMUS: for ax+1 the envelope
    constant is log2 a, and the same theorem holds with boundary r = log2 a
    -- the spike ledger is NOT 3-specific (expected: it excludes seeds for
    every multiplier; it is a size argument, not a descent argument).

All arithmetic exact; certified sandwich 1054/665 < log2 3 < 24727/15601.
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

def W_of(u, m):
    Du, Bu, Su, Hu = DBof(u)
    Dm, Bm, Sm, Hm = DBof(m)
    return Du * Bm - Bu * Dm

def hmass(w):
    return sum(s + v - 1 for s, v in w)

def lcp_mass(u, m, reps=40):
    uu, mm = list(u) * (reps * len(m)), list(m) * (reps * len(u))
    L = min(len(uu), len(mm))
    j = 0
    while j < L and uu[j] == mm[j]:
        j += 1
    assert j < L, "periodizations agree suspiciously long"
    return hmass(uu[:j]), (uu[j], mm[j])

def certified_log23():
    lo, hi = Fraction(1054, 665), Fraction(24727, 15601)
    assert 3**lo.denominator > 2**lo.numerator
    assert 3**hi.denominator < 2**hi.numerator
    return lo, hi

LO, HI = certified_log23()

# ---------------- (A) omega vs lcp ----------------
def check_lcp_formula():
    fails = tested = 0
    for _ in range(4000):
        u = tuple((random.randint(1, 4), random.randint(2, 4))
                  for _ in range(random.randint(1, 3)))
        m = tuple((random.randint(1, 4), random.randint(2, 4))
                  for _ in range(random.randint(1, 3)))
        W = W_of(u, m)
        if W == 0:
            continue
        om = v2(W)
        Hl, ((s, v), (s2, v2_)) = lcp_mass(u, m)
        tested += 1
        # EXACT formula
        if s != s2:
            pred = Hl + min(s, s2)
        else:
            pred = Hl + min(s + v - 1, s2 + v2_ - 1)
        if om != pred:
            fails += 1
            print("    exact-formula FAIL", u, m, om, pred)
    print(f"(A) EXACT formula omega = H_q + min(s,s') / H_q + min(h,h') "
          f"on {tested} block pairs: fails={fails}")
    # phi identity omega = v2(phi_m - phi_u)
    f2 = 0
    for _ in range(2000):
        u = tuple((random.randint(1, 4), random.randint(2, 4))
                  for _ in range(random.randint(1, 2)))
        m = tuple((random.randint(1, 4), random.randint(2, 4))
                  for _ in range(random.randint(1, 2)))
        Du, Bu, _, _ = DBof(u)
        Dm, Bm, _, _ = DBof(m)
        W = Du * Bm - Bu * Dm
        ph = Fraction(Bm, Dm) - Fraction(Bu, Du)
        if (W == 0) != (ph == 0):
            f2 += 1
        elif W != 0 and v2(W) != v2frac(ph):
            f2 += 1
    print(f"    omega = v2(phi_m - phi_u) identity: fails={f2}")
    # degeneracy: powers of a common root
    f3 = 0
    for _ in range(500):
        root = tuple((random.randint(1, 4), random.randint(2, 4))
                     for _ in range(random.randint(1, 2)))
        a, b = random.randint(1, 3), random.randint(1, 3)
        if W_of(root * a, root * b) != 0:
            f3 += 1
    print(f"    W(root^a, root^b) = 0 (common primitive root): fails={f3}")
    return fails == f2 == f3 == 0

def e_relevant_tables():
    """omega(u, m) for u = non-G01 run blocks, m = G01 gap blocks."""
    G01 = [(2, 2), (3, 2)]
    from itertools import product
    print("\n(A) E-relevant Wronskian levels: u = non-G01 block, m = G01 gap")
    print("    (H_m = h-mass of gap; omega < H_m => forced coincidence)")
    deep_forced = True   # PROVED corollary: s_{u_1} >= 4 => always forced
    for u in [((4, 2),), ((5, 2),), ((6, 2),), ((4, 3),), ((2, 3),),
              ((4, 2), (4, 2)), ((5, 2), (4, 2))]:
        rows = []
        mx = -1
        for L in (1, 2, 3):
            for mm in product(G01, repeat=L):
                W = W_of(u, mm)
                if W == 0:
                    rows.append((mm, None, hmass(mm)))
                    continue
                om = v2(W)
                Hm = hmass(mm)
                rows.append((mm, om, Hm))
                mx = max(mx, om)
                if u[0][0] >= 4:
                    if om != mm[0][0] or om >= Hm:   # exact corollary
                        deep_forced = False
        n_forced = sum(1 for (_, om, Hm) in rows if om is not None and om < Hm)
        print(f"  u={str(u):22s}: max omega over G01 gaps len<=3 = {mx}; "
              f"forced {n_forced}/{len(rows)}"
              + ("  (s_u=2: same-depth case, corollary N/A)" if u[0][0] < 4
                 else ""))
    print(f"  PROVED corollary verified (s_u >= 4: omega = s_gap-first in "
          f"{{2,3}}, always forced): {deep_forced}")
    return deep_forced

# ---------------- (B) spike ledger ----------------
def g_of(s, v):
    return Fraction(3**s + (1 << (v - 1)) - 1, 1 << (s + v - 1))

def check_product_envelope():
    fails = tested = 0
    for _ in range(4000):
        x0 = random.getrandbits(44) | 1
        if x0 <= 1:
            continue
        N = random.randint(1, 16)
        x = x0
        P = Fraction(1)
        for _ in range(N):
            s, vv, x = hop(x)
            P *= g_of(s, vv)
            tested += 1
            if x + 1 > (x0 + 1) * P:
                fails += 1
    print(f"\n(B) composed product envelope x_j+1 <= (x_0+1) prod g: "
          f"{tested} checks, fails={fails}")
    return fails == 0

def check_spike_exclusion():
    ok = True
    # exact requirement (#): (x_0+1) >= R_j := 2^{s_j} / prod_{i<j} g(l_i)
    # doubling spikes s_j = 2^j, v = 2:
    print("(B) doubling-spike word ((2,2),(4,2),(8,2),(16,2),...): exact "
          "lower bounds R_j on x_0+1:")
    P = Fraction(1)
    R_prev = None
    for j in range(1, 15):
        s = 1 << j
        R = Fraction(1 << s, 1) / P          # need x_0+1 >= R
        bits = (R.numerator.bit_length() - R.denominator.bit_length())
        if j <= 6 or j in (10, 14):
            print(f"  j={j:2d} (s_j={s:5d}): R_j ~ 2^{bits}")
        if R_prev is not None and not R > 2 * R_prev:
            ok = False   # proved ratio >= 2 via 3^s+1 <= 4^s
        R_prev = R
        P *= g_of(s, 2)
    print(f"  R_j strictly doubles (proved via 3^s+1 <= 4^s): {ok}")
    print("  => NO positive integer realizes the word (R_j -> infinity).")
    # sharp version via certified sandwich: geometric spikes ratio r
    # excluded iff r > log2 3; verify the two sides with exact ledgers.
    def ledger_bits(seq):
        """exact bits of R_j = 2^{s_j}/prod g for the pure spike word."""
        P = Fraction(1)
        out = []
        for j, s in enumerate(seq):
            R = Fraction(1 << s) / P
            out.append(R.numerator.bit_length() - R.denominator.bit_length())
            P *= g_of(s, 2)
        return out
    import math
    # r = 1.7 > log2 3: excluded (R grows); r = 1.45 < log2 3: self-financed
    for r, lab in [(Fraction(17, 10), "r=1.7 > log2 3"),
                   (Fraction(8, 5), "r=1.6 > log2 3"),
                   (Fraction(29, 20), "r=1.45 < log2 3"),
                   (Fraction(3, 2), "r=1.5 < log2 3")]:
        seq = [max(2, int(4 * r**j)) for j in range(16)]
        lb = ledger_bits(seq)
        growing = lb[-1] > lb[4] + 10
        verdict = ("EXCLUDED (R->inf)" if growing
                   else "self-financing (ledger satisfiable; not excluded)")
        print(f"  {lab}: R_j bits {lb[2]}, {lb[6]}, {lb[10]}, {lb[-1]} -> "
              f"{verdict}")
        if (r > HI) != growing:
            ok = False
    # certified power inequality used in the proof: 3^s < 2^{s*HI} for all s
    # via 3^15601 < 2^24727 raised to any power; spot exact checks:
    for s in (7, 100, 1024):
        if not 3**(s * 15601) < 2**(s * 24727):
            ok = False
    print(f"  certified 3^s < 2^(s*24727/15601) for all s (power argument): "
          f"{ok}")
    # 5n+1 litmus: envelope constant becomes log2 5; the theorem transfers
    # (statement-level check: g_a(s,2) = (a^s+1)/2^{s+1}, boundary log2 a)
    ga = lambda a, s: Fraction(a**s + 1, 1 << (s + 1))
    P5 = Fraction(1)
    R0 = None
    grew = True
    for j in range(1, 12):
        s = 1 << j
        R = Fraction(1 << s) / P5
        if R0 is not None and not R > R0:
            grew = False
        R0 = R
        P5 *= ga(5, s)
    # for a=5, log2 5 = 2.32 > 2 = doubling ratio: doubling spikes NOT
    # excluded for 5n+1 (ledger self-financing) -- the boundary moves to
    # log2 a, so the spike theorem is multiplier-covariant, not 3-specific
    print(f"  5n+1: doubling spikes self-financing (log2 5 > 2): "
          f"{'yes (R_j eventually shrinks)' if not grew else 'NO -- check'}")
    ok &= not grew
    return ok

if __name__ == "__main__":
    ok = check_lcp_formula()
    ok &= e_relevant_tables()
    ok &= check_product_envelope()
    ok &= check_spike_exclusion()
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
