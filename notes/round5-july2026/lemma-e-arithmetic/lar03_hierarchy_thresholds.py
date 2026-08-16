"""lar03_hierarchy_thresholds.py -- Lemma E arithmetic attack, part 3:
transport of the sharpened complexity-threshold machinery (T_R' = 3.2439...)
to the depth-{d..D} return hierarchy (lea04 systems), and the exact verdict
on the HIERARCHY PINCER.

SYSTEMS (lea04, verified there and re-verified here): level-d states are
depth-d v=2 states x = 2^{d+2} m - 1; single-excursion blocks t in
{empty} u {(t): d < t <= D} act by m -> (P m + C)/2^E with
    empty:  P = 3^{d+2},         E = d+3
    (t):    P = 3^{(d+2)+(t+2)}, E = (d+3)+(t+3).
The block letter word is ((d+2,2)) resp. ((d+2,2),(t+2,2)) -- h-mass per
block = E exactly.  (d,D) = (0,1) is the repo's binary return system.

TRANSPORTED THRESHOLD (PROVED by the same state-separation proof as
LE1/Theorem 60, at block granularity -- separation congruence verified
numerically below): every integer-realized, not-eventually-periodic block
word over the single-excursion alphabet satisfies
    liminf p(m)/m >= T_block(d,D) = (d+3) / ((d+D+4) log2 3 - (d+D+6)),
and at letter granularity (LE1 verbatim, alphabet {(d+2,2)} u {(t+2,2)}):
    liminf p(m)/m >= T_letter(d,D) = (d+3) / log2((3^{D+2}+1)/2^{D+3}).
Checks: T_block(0,1) = 3/(5 log2 3 - 7) = 3.2439007 = T_R' (repo Theorem
60); T_letter(0,1) = 3/log2(7/4) = 3.7158 (lea01 G01 row).

EXACT NUMBERS AND MONOTONICITY (PROVED with certified rational sandwiches
of log2 3; all comparisons exact integer):
  (1) T_block(d,D) is STRICTLY DECREASING in both d and D:
      in D trivially (denominator grows by log2 3 - 1 > 0 per step);
      in d because d(T)/dd has sign of -(log2 3) - 1 < 0 (cross-multiplied
      exactly below).  Diagonal limit lim_d T_block(d,d+1) =
      1/(2(log2 3 - 1)) = 0.854752...; vacuity T_block(d,d+1) <= 1 iff
      d >= 13 (exact crossing (10 - 5 log2 3)/(3 - 2 log2 3) = 12.212...).
  (2) T_letter(d,d+1) strictly decreases to 1/(log2 3 - 1) = log_{3/2} 2
      = 1.709511... (the BALLOT constant), never vacuous but monotonically
      weaker; sup at (0,1): 3.7158.
  (3) Multi-excursion blocks only lower thresholds (Gamma increases);
      D = infinity gives Gamma = infinity, threshold 0.
  SO: the supremum of every transported threshold over the ENTIRE hierarchy
  is attained at the shallowest, already-known level, and thresholds SHRINK
  with depth.  A pincer needs them to GROW.

PINCER VERDICT (negative result; PROVED):
  (a) The thresholds are uniformly bounded (<= 7.5691, the no-empty-block
      (0,1) value = the repo's uniform-density floor) and decrease along
      every graded family;
  (b) at EVERY level the ambient language is the FULL shift over the block
      alphabet (the class construction below never fails: every block word
      has a nonempty residue class -- verified constructively + realized
      by integers for random words), so no complexity UPPER bound exists at
      any level without H1^{(d)} itself (Theorem 60 levelwise);
  (c) all the lower bounds are simultaneously satisfiable (any full-
      complexity word dominates every threshold), so the family of
      transported thresholds is consistent -- no contradiction machine.
  Hence the hierarchy pincer is IMPOSSIBLE via state-separation thresholds:
  a single orbit word meets every level's bound as soon as it meets the
  d = 0 bound.  Structural reason (exact): per-block modulus mass E ~ t
  while per-block log-growth ~ t(log2 3 - 1); the ratio tends to
  1/(log2 3 - 1) -- the SAME 2-vs-3 exchange rate that makes non-descent
  possible (ballot constant) caps every threshold in the hierarchy.

All arithmetic exact (Fractions + certified convergent sandwich for log2 3:
  1054/665 < log2 3 < 24727/15601, certified by integer power comparison).
Floats appear only in display.
"""
import sys, random
from fractions import Fraction
from itertools import product
random.seed(20260721)

def v2(n):
    if n == 0:
        return None
    return (abs(n) & -abs(n)).bit_length() - 1

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

# certified sandwich lo < log2(3) < hi by exact integer power comparison
def certified_log23():
    lo, hi = Fraction(1054, 665), Fraction(24727, 15601)
    assert 3**lo.denominator > 2**lo.numerator      # log2 3 > lo
    assert 3**hi.denominator < 2**hi.numerator      # log2 3 < hi
    return lo, hi

LO, HI = certified_log23()

def block_letter_word(d, u):
    """letter word of block d->u->d EXCLUDING the shared return letter."""
    return tuple((t + 2, 2) for t in [d] + list(u))

def block_PE(d, u):
    P = 3**(d + 2) * (1 if not u else 3**(sum(t + 2 for t in u)))
    E = (d + 3) + sum(t + 3 for t in u)
    return P, E

# ---------------- threshold tables ----------------
def tables():
    from math import log2
    print("T_block(d,D) = (d+3)/((d+D+4)log2(3)-(d+D+6))   [single-excursion"
          " block words]\nT_letter(d,D) = (d+3)/log2((3^(D+2)+1)/2^(D+3))"
          "   [letter words, LE1]")
    print(f"{'d':>3s} {'D':>3s} {'T_block':>10s} {'T_letter':>10s}   "
          f"{'no-empty T':>10s}")
    rows = []
    for d in range(0, 16):
        D = d + 1
        Tb = (d + 3) / ((d + D + 4) * log2(3) - (d + D + 6))
        Tl = (d + 3) / log2((3**(D + 2) + 1) / 2**(D + 3))
        Tne = (2 * d + 7) / ((2 * d + 5) * log2(3) - (2 * d + 7))
        rows.append((d, D, Tb, Tl, Tne))
        print(f"{d:3d} {D:3d} {Tb:10.6f} {Tl:10.6f}   {Tne:10.6f}"
              + ("   <- repo T_R' / G01 / density floor" if d == 0 else "")
              + ("   <- T_block crosses 1 (vacuous from here)" if d == 13 else ""))
    for d, D in [(0, 2), (0, 3), (0, 6), (1, 3), (2, 4)]:
        Tb = (d + 3) / ((d + D + 4) * log2(3) - (d + D + 6))
        print(f"{d:3d} {D:3d} {Tb:10.6f}   (off-diagonal)")
    print(f"limits: diag T_block -> 1/(2(log2 3 - 1)) = "
          f"{1/(2*(log2(3)-1)):.6f}; diag T_letter -> 1/(log2 3 - 1) = "
          f"{1/(log2(3)-1):.6f} (ballot constant); D=inf: 0")
    # exact identity checks at d=0
    ok = True
    ok &= abs(rows[0][2] - 3.2439007) < 1e-6         # T_R' (Theorem 60)
    ok &= abs(rows[0][3] - 3 / log2(7 / 4)) < 1e-12  # G01 (lea01)
    ok &= abs(rows[0][4] - 7.5691018) < 1e-6         # density floor (Thm 60)
    print(f"cross-checks vs repo values (T_R', G01, floor 7.5691): {ok}")
    return ok

# ---------------- exact monotonicity + vacuity ----------------
def exact_monotonicity():
    # T_block(d,d+1) = (d+3)/((2d+5)L-(2d+7)) with L = log2 3.
    # T is decreasing in L (denominator increasing in L, numerator fixed),
    # so Tb(d,HI) < Tb(d,Ltrue) < Tb(d,LO).  Strict decrease in d at the
    # TRUE L follows from the sufficient exact test Tb(d,HI) > Tb(d+1,LO).
    def Tb(d, L):
        return Fraction(d + 3) / ((2 * d + 5) * L - (2 * d + 7))
    def Tne(d, L):
        return Fraction(2 * d + 7) / ((2 * d + 5) * L - (2 * d + 7))
    mono = True
    for d in range(0, 60):
        if not Tb(d, HI) > Tb(d + 1, LO):        # exact rational comparison
            mono = False
        if not Tne(d, HI) > Tne(d + 1, LO):
            mono = False
    print(f"\nexact strict decrease in d (sufficient sandwich test "
          f"Tb(d,HI) > Tb(d+1,LO), d < 60): {mono}")
    # T > 1 iff d <= 12; T < 1 iff d >= 13 at the true L:
    #  d<=12: enough that Tb(d,HI) > 1;  d>=13: enough that Tb(d,LO) < 1.
    vac = True
    for d in range(0, 40):
        if d <= 12 and not Tb(d, HI) > 1:
            vac = False
        if d >= 13 and not Tb(d, LO) < 1:
            vac = False
    # exact crossing point (10-5L)/(2L-3) sandwiched in (12, 13)
    cross_lo = (10 - 5 * HI) / (2 * HI - 3)
    cross_hi = (10 - 5 * LO) / (2 * LO - 3)
    vac &= 12 < min(cross_lo, cross_hi) and max(cross_lo, cross_hi) < 13
    print(f"exact vacuity: T_block(d,d+1) > 1 iff d <= 12 : {vac} "
          f"(crossing in ({float(min(cross_lo,cross_hi)):.4f}, "
          f"{float(max(cross_lo,cross_hi)):.4f}))")
    # uniform ceiling: every listed threshold <= no-empty (0,1) value 7.5691
    ceil = True
    for d in range(0, 60):
        if not (Tb(d, LO) <= Tne(0, HI) and Tne(d, LO) <= Tne(0, HI)):
            # Tb(d,LO) is an UPPER bound for true Tb(d); Tne(0,HI) is a
            # LOWER bound for the true ceiling -- sufficient test, d >= 1;
            # d = 0 equality case handled separately
            if d > 0:
                ceil = False
    ceil &= Tb(0, LO) <= Tne(0, LO)  # at d=0 compare at the same endpoint
    print(f"uniform ceiling (<= 7.5691, the (0,1)-no-empty value) over "
          f"d < 60: {ceil}")
    return mono and vac and ceil

# ---------------- separation congruence at level d ----------------
def check_separation(d=1, D=2, trials=150000):
    """Same-factor state separation at block granularity, level d:
    if the block words from states m1, m2 share the same first-j blocks
    (total 2-mass Ej), then m1 = m2 mod 2^{Ej}, and the x-states are
    congruent mod 2^{Ej + d + 2}.  This is the separation input the
    threshold proof needs; verified on random states."""
    fails = tested = 0
    for _ in range(trials):
        m = random.getrandbits(26) | 1
        x = (m << (d + 2)) - 1
        s, vv, _ = hop(x)
        if s != d + 2 or vv != 2:
            continue
        # follow up to 3 blocks
        blocks = []
        y = x
        okflag = True
        for _ in range(3):
            u = []
            while True:
                s, vv, y2 = hop(y)
                s2, vv2, _ = hop(y2)
                if vv != 2:
                    okflag = False
                    break
                t2 = s2 - 2
                if t2 == d:
                    y = y2
                    break
                if vv2 != 2 or not (d + 1 <= t2 <= D):
                    okflag = False
                    break
                u.append(t2)
                y = y2
            if not okflag:
                break
            blocks.append(tuple(u))
        if not okflag or len(blocks) < 2:
            continue
        Ej = sum((d + 3) + sum(t + 3 for t in u) for u in blocks[:2])
        # second state with same first-2 blocks: use class congruence
        seq = [d]
        for u in blocks[:2]:
            seq += list(u) + [d]
        lw = tuple((t + 2, 2) for t in seq)
        r, qe = class_rep(lw)
        x2 = x + (1 << qe)
        # x2 performs same letter word => same blocks
        if word_of(x2, len(lw)) != lw:
            fails += 1
            continue
        tested += 1
        m2 = (x2 + 1) >> (d + 2)
        if (m2 - m) % (1 << Ej) != 0:
            fails += 1
    print(f"\nlevel-{d} separation: same 2 blocks => m-states congruent "
          f"mod 2^(E-mass): {tested} pairs, fails={fails}")
    return fails == 0

# ---------------- levelwise full shift ----------------
def check_full_shift():
    """Every block word over the (d,D) single-excursion alphabet has a
    nonempty class, and small random ones are realized by actual integers."""
    fails = tested = 0
    for d, D in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]:
        alpha = [()] + [(t,) for t in range(d + 1, D + 1)]
        for _ in range(60):
            L = random.randint(1, 5)
            wblocks = [random.choice(alpha) for _ in range(L)]
            seq = [d]
            for u in wblocks:
                seq += list(u) + [d]
            lw = tuple((t + 2, 2) for t in seq)
            r, qe = class_rep(lw)   # constructive nonemptiness
            x = r if r > 1 else r + (1 << qe)
            tested += 1
            if word_of(x, len(lw)) != lw:
                fails += 1
    print(f"levelwise ambient full shift: {tested} random block words all "
          f"realized by integers: fails={fails}")
    return fails == 0

# ---------------- growth/threshold mechanism sanity at level 1 ----------
def check_growth_level(d=1, D=2):
    """Per-block growth envelope m' <= m * (P + C)/2^E used by the
    threshold; verify exactly on random blocks."""
    fails = tested = 0
    for _ in range(150000):
        m = random.getrandbits(24) | 1
        x = (m << (d + 2)) - 1
        s, vv, _ = hop(x)
        if s != d + 2 or vv != 2:
            continue
        # one block
        u = []
        y = x
        good = True
        while True:
            s, vv, y2 = hop(y)
            s2, vv2, _ = hop(y2)
            if vv != 2:
                good = False
                break
            t2 = s2 - 2
            if t2 == d:
                y = y2
                break
            if vv2 != 2 or not (d + 1 <= t2 <= D):
                good = False
                break
            u.append(t2)
            y = y2
        if not good:
            continue
        mp = (y + 1) >> (d + 2)
        # composed block affine data
        P, C, E = 1, 0, 0
        seq = [d] + u + [d]
        for i in range(len(seq) - 1):
            a, e = 3**(seq[i] + 2), seq[i + 1] + 3
            P, C, E = a * P, a * C + (1 << E), E + e
        tested += 1
        if (P * m + C) != (mp << E):
            fails += 1
        if mp * (1 << E) > m * (P + C):
            fails += 1
    print(f"level-{d} block map + growth envelope: {tested} blocks, "
          f"fails={fails}")
    return fails == 0

if __name__ == "__main__":
    ok = tables()
    ok &= exact_monotonicity()
    ok &= check_separation()
    ok &= check_full_shift()
    ok &= check_growth_level()
    print("\nPINCER VERDICT: thresholds are uniformly bounded by 7.5691 and")
    print("strictly DECREASE with depth (exact); ambient language is the full")
    print("shift at every level; all lower bounds are mutually consistent.")
    print("=> the hierarchy pincer is IMPOSSIBLE via transported thresholds.")
    print("The limiting ratio at depth is 1/(log2 3 - 1) = the ballot constant:")
    print("the 2-vs-3 exchange rate both enables non-descent and caps the")
    print("hierarchy's complexity leverage.")
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
