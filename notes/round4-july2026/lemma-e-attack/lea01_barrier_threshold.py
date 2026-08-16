"""lea01_barrier_threshold.py -- Lemma E attack, part 1: the hop-word
factor-recurrence barrier and the bounded-alphabet complexity threshold.

Hop coordinates (repo Theorem 55 / bridge01): for odd x>1, s = v_2(x+1),
m = (x+1)/2^s odd, FMF(x) = 2(3^s m - 1), v = 1 + v_2(3^s m - 1) >= 2,
next odd state x' = F(x) = (3^s x + 3^s - 2^s)/2^h, h = s+v-1.
Letter l = (s,v).  For a word w: S = sum s, H = sum h, y := x+1.

THEOREM LE0 (word-class congruence; constructive re-proof of the repo's
mixed-pattern shadow theorem):
  the set of odd x whose first N hop letters equal a given word w is exactly
  one residue class mod 2^(H+1).  Constructive induction: letter class is one
  class mod 2^(s+v) (= 2^(h+1)); pulling a class mod 2^qe of x' back through
  x' = (3^s x + c)/2^h restricted to the letter class gives one class mod
  2^(h+qe).  [PROVED below by exact lifting + verified by brute force.]

LEMMA LE-B (hop-word factor-recurrence barrier; exact):
  Let x_0 > 1 be odd with hop word w.  If w has equal length-m factors at
  positions i < i' and x_i != x_{i'}, then
      2^(H_f + 1) <= |x_{i'} - x_i| < max(x_i, x_{i'}) + 1,
  where H_f = sum of h over the factor.  Combined with the exact envelope
      y_{j+1} <= y_j * (3^s + 2^(v-1) - 1)/2^h        (uses y_j >= 2^s),
  any upper bound on letter growth converts factor repetition into a size
  certificate.  [PROVED: LE0 + strict separation + envelope; all verified.]

THEOREM LE1 (bounded-alphabet complexity threshold for Lemma E; effective):
  Let x_0 > 1 be odd whose hop word w lies in A^infty, A a finite alphabet.
  Put h_min = min_A (s+v-1), g(l) = (3^s + 2^(v-1) - 1)/2^(s+v-1),
  Gamma = log2 max_A g.
  (a) If Gamma <= 0 then the orbit is bounded, hence eventually periodic,
      hence enters a Collatz cycle.
  (b) If Gamma > 0 and w is NOT eventually periodic, then for EVERY m >= 1
        p_w(m) > (h_min*m + 1 - log2(x_0+1)) / Gamma,
      where p_w = factor complexity.  Hence liminf p_w(m)/m >= h_min/Gamma.
  (c) If w IS eventually periodic, the orbit enters a Collatz cycle (repo E1);
      by the FMF-hop = Simons-de Weger identity (repo Theorem 53) + Hercher
      m<=91, its period is >= 92 hops.  If every letter of A is expanding
      (3^s > 2^h), a cycle is impossible outright: a cycle satisfies
      (2^H - 3^S) x = B > 0, but all-expanding forces 3^S > 2^H.
  Proof of (b): for each m the p(m)+1 windows at positions 0..p(m) contain two
  equal factors at i < i' <= p(m); not-eventually-periodic => x_i != x_{i'};
  LE-B gives 2^(h_min*m + 1) < max(x_i,x_{i'}) + ... < y_0 2^(Gamma i').

COROLLARY C1 (depth-{0,1,2}; unconditional):
  A = {(2,2),(3,2),(4,2)} (depths 0,1,2, growth-B).  All letters expanding =>
  no eventually-periodic realization at all, and every odd x_0>1 whose hop
  word is eventually over A satisfies, for the tail word,
      liminf p(m)/m >= 3/log2(41/16) = 2.2098...
  In particular NO orbit realizes a depth-{0,1,2} word with infinitely many
  (4,2) letters of sub-threshold complexity (Sturmian, substitutive of low
  complexity, linearly recurrent with small constant, ...).  This is the first
  proved piece of Lemma E strictly beyond depth {0,1} + eventual periodicity.

This script verifies every ingredient exactly and prints the threshold table.
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

def letter_class(s, v):
    """Letter (s,v) <=> one residue class mod 2^(s+v). Returns (rep, exp)."""
    mu = (pow(3, -s, 1 << v) * (1 + (1 << (v - 1)))) % (1 << v)
    return ((mu << s) - 1) % (1 << (s + v)), s + v

def class_rep(word):
    """LE0 constructive: class (rep, exponent) of odd x performing word.
    Backward lifting; exponent = H+1 exactly."""
    (s, v) = word[-1]
    h = s + v - 1
    r, qe = letter_class(s, v)          # exponent h+1
    for (s, v) in reversed(word[:-1]):
        h = s + v - 1
        c = 3**s - 2**s
        rho, _ = letter_class(s, v)
        x0p = (3**s * rho + c)
        assert x0p % (1 << h) == 0
        x0p >>= h                        # image of the class rep, odd
        assert x0p & 1
        # x = rho + 2^(h+1) t ; x' = x0p + 2*3^s t == r (mod 2^qe)
        need = (r - x0p) % (1 << qe)
        assert need % 2 == 0
        t = ((need >> 1) * pow(3**s, -1, 1 << (qe - 1))) % (1 << (qe - 1))
        r = (rho + (t << (h + 1))) % (1 << (h + qe))
        qe = h + qe
    return r, qe

# ---------------- LE0 verification ----------------
def check_LE0():
    fails = 0
    # (a) brute force: random words, exact set = one class mod 2^(H+1)
    for trial in range(60):
        N = random.randint(1, 4)
        w = tuple((random.randint(1, 4), random.randint(2, 4)) for _ in range(N))
        H = sum(s + v - 1 for s, v in w)
        r, qe = class_rep(w)
        assert qe == H + 1
        mod = 1 << qe
        found = [x for x in range(3, 2 * mod + 3, 2) if word_of(x, N) == w]
        expect = [x for x in range(3, 2 * mod + 3, 2) if x % mod == r]
        if found != expect:
            fails += 1
            print("LE0 brute FAIL", w, found[:3], expect[:3])
    # (b) ground truth: class contains the x it was read from
    for trial in range(4000):
        x = random.getrandbits(40) | 1
        if x <= 1:
            continue
        N = random.randint(1, 12)
        w = word_of(x, N)
        r, qe = class_rep(w)
        if x % (1 << qe) != r:
            fails += 1
            print("LE0 ground-truth FAIL", x, w)
    # (c) pairwise congruence: same first-N letters => v_2(x - x'') >= H+1
    for trial in range(2000):
        x = random.getrandbits(36) | 1
        if x <= 1:
            continue
        N = random.randint(1, 8)
        w = word_of(x, N)
        H = sum(s + v - 1 for s, v in w)
        r, qe = class_rep(w)
        xx = x + (1 << qe) * random.randint(1, 50)
        if word_of(xx, N) != w:
            fails += 1
            print("LE0 class-forward FAIL", x, xx)
        if v2(x - xx) < H + 1:
            fails += 1
            print("LE0 congruence FAIL")
    print(f"LE0 word-class congruence (mod 2^(H+1)): brute + ground truth + "
          f"pairwise, fails={fails}")
    return fails == 0

# ---------------- envelope + expansion ----------------
def check_envelope():
    fails = 0
    for trial in range(200000):
        x = random.getrandbits(44) | 1
        if x <= 1:
            continue
        s, vv, xp = hop(x)
        h = s + vv - 1
        y, yp = x + 1, xp + 1
        # exact identity y' = (3^s y + 2^h - 2^s)/2^h
        if yp * (1 << h) != 3**s * y + (1 << h) - (1 << s):
            fails += 1
        # envelope y' <= y (3^s + 2^(v-1) - 1)/2^h   (exact rational)
        if yp * (1 << h) > y * (3**s + (1 << (vv - 1)) - 1):
            fails += 1
        # strict growth for expanding letters
        if 3**s > (1 << h) and not xp > x:
            fails += 1
    print(f"envelope identity + bound + strict growth on 2e5 random x: fails={fails}")
    return fails == 0

# ---------------- threshold table ----------------
def g_of(s, v):
    return Fraction(3**s + (1 << (v - 1)) - 1, 1 << (s + v - 1))

def threshold_table():
    from math import log2
    rows = [
        ("G01 = {(2,2),(3,2)}            ", [(2, 2), (3, 2)]),
        ("depth-{0,1,2} {(2,2),(3,2),(4,2)}", [(2, 2), (3, 2), (4, 2)]),
        ("{(2,2),(4,2)}                  ", [(2, 2), (4, 2)]),
        ("{(3,2),(4,2)}  (no depth-0)    ", [(3, 2), (4, 2)]),
        ("depth-{0..3}  (s<=5)           ", [(s, 2) for s in range(2, 6)]),
        ("depth-{0..4}  (s<=6)           ", [(s, 2) for s in range(2, 7)]),
        ("depth-{0..5}  (s<=7)  VACUOUS  ", [(s, 2) for s in range(2, 8)]),
        ("G01 + TypeA (1,2)              ", [(1, 2), (2, 2), (3, 2)]),
        ("{(1,2),(2,2)}                  ", [(1, 2), (2, 2)]),
        ("{(1,2),(4,2)}                  ", [(1, 2), (4, 2)]),
        ("G01+{(4,2)}+{(1,2)}            ", [(1, 2), (2, 2), (3, 2), (4, 2)]),
    ]
    print("\nLE1 threshold table: realized non-eventually-periodic words over A "
          "need liminf p(m)/m >= h_min/Gamma")
    print(f"{'alphabet':38s} h_min  Gamma=log2(max g)   threshold h_min/Gamma")
    for name, A in rows:
        hmin = min(s + v - 1 for s, v in A)
        gmax = max(g_of(s, v) for s, v in A)
        Gamma = log2(gmax)
        thr = hmin / Gamma if Gamma > 0 else float('inf')
        note = " (>1: bites aperiodic words)" if thr > 1 else " (<=1: silent)"
        print(f"{name:38s}  {hmin}    {Gamma:.6f} (max g={gmax})   "
              f"{thr:.6f}{note}")
    print("Sharp values: 3/log2(7/4) = %.6f (G01), 3/log2(41/16) = %.6f "
          "(depth-{0,1,2})" % (3/log2(Fraction(7, 4)), 3/log2(Fraction(41, 16))))

# ---------------- C1 demo: Sturmian over {(2,2),(4,2)} ----------------
def sturmian_word(N, alpha_num=None):
    """Sturmian coding of golden rotation: letter (4,2) iff floor((j+1)a)-floor(ja)=1
    with a = 1/phi, done exactly with integer sqrt."""
    # a = (sqrt(5)-1)/2; floor(j*a) = floor((isqrt(5 j^2) - j)/2)
    from math import isqrt
    def fl(j):
        return (isqrt(5 * j * j) - j) // 2
    w = []
    for j in range(N):
        b = fl(j + 1) - fl(j)
        w.append((4, 2) if b == 1 else (2, 2))
    return w

def fib_word(N):
    """Fibonacci substitution a->ab, b->a over a=(2,2), b=(4,2)."""
    s = "a"
    while len(s) < N:
        s = "".join("ab" if ch == "a" else "a" for ch in s)
    return [(2, 2) if ch == "a" else (4, 2) for ch in s[:N]]

def tm_word(N, la=(2, 2), lb=(3, 2)):
    return [lb if bin(j).count("1") % 2 else la for j in range(N)]

def complexity(w, mmax):
    p = {}
    for m in range(1, mmax + 1):
        p[m] = len({tuple(w[i:i + m]) for i in range(len(w) - m)})
    return p

def check_C1_demo():
    from math import log2
    ok = True
    N = 20000
    st = sturmian_word(N)
    p = complexity(st, 16)
    print("\nC1 demo: Sturmian word over {(2,2),(4,2)} (infinitely many (4,2), "
          "density 1/phi^2 of (2,2)...)")
    print("  p(m) for m=1..16:", [p[m] for m in range(1, 17)],
          " (Sturmian: p(m)=m+1)")
    ok &= all(p[m] == m + 1 for m in range(1, 17))
    # exact certificate: no realization with y_0 <= 2^64, at m=40:
    # need NOT( 3m+1 < 64 + log2(41/16) * p(m) ), i.e. show
    # 2^(3m+1) * 16^(p(m)) > 2^64 * 41^(p(m))   with p(40)=41
    m = 40
    pm = m + 1
    lhs = (1 << (3 * m + 1)) * (1 << (4 * pm))
    rhs = (1 << 64) * 41**pm
    print(f"  exact certificate at m={m}: 2^(3m+1)*16^p > 2^64*41^p ? {lhs > rhs}"
          f"  (so no realizing x_0 < 2^64 - 1)")
    ok &= lhs > rhs
    # for every size bound B0 the certificate m ~ (B0+1.36)/1.642 exists:
    for B0 in (128, 512, 4096):
        m = 1
        while not (1 << (3 * m + 1)) * (1 << (4 * (m + 1))) > (1 << B0) * 41**(m + 1):
            m += 1
        print(f"    y_0 <= 2^{B0}: certificate at m = {m}")
    # direct evidence: nested prefix residues R_N must stabilize for a realized
    # word; here they grow like 2^(H_N):
    print("  nested prefix residues R_N (bit lengths) vs H_N+1:")
    for Nw in (25, 50, 100, 150):
        w = st[:Nw]
        r, qe = class_rep(w)
        print(f"    N={Nw:4d}: bits(R_N)={r.bit_length():4d}   H_N+1={qe:4d}")
    # same for Fibonacci-substitution word
    fw = fib_word(4000)
    pf = complexity(fw, 12)
    ok &= all(pf[m] == m + 1 for m in range(1, 13))
    r, qe = class_rep(fw[:120])
    print(f"  Fibonacci-substitution word: p(m)=m+1 verified (m<=12); "
          f"R_120 bits = {r.bit_length()} of {qe} (grows: unrealizable)")
    # Thue-Morse over G01: threshold 3.7158 vs p_TM(m) <= 10m/3
    tw = tm_word(N)
    pt = complexity(tw, 16)
    mx = max(pt[m] / m for m in range(3, 17))
    print(f"  Thue-Morse over G01: max p(m)/m for m in [3,16] = {mx:.4f} "
          f"< 3.7158 threshold => EXCLUDED (no orbit has eventual TM depth word)")
    ok &= mx < 3 / log2(Fraction(7, 4))
    # honesty: a random word over {(2,2),(4,2)} has p(m) ~ 2^m: theorem silent
    rw = [random.choice([(2, 2), (4, 2)]) for _ in range(N)]
    pr = complexity(rw, 14)
    print(f"  honesty check: random word p(14) = {pr[14]} (~2^14): "
          f"threshold silent for positive-entropy words (open regime)")
    return ok

# ---------------- LE-B numeric sanity on a real orbit ----------------
def check_barrier_on_true_orbits():
    """The barrier inequality direction on real (descending) orbits:
    whenever equal factors occur at i<i' with x_i != x_{i'}, verify
    2^(H_f+1) <= |x_{i'} - x_i| exactly."""
    fails = tested = 0
    for x0 in [27, 703, 26623, 2**20 - 1, 123456789]:
        xs, ws = [x0], []
        x = x0
        for _ in range(300):
            s, vv, x = hop(x)
            ws.append((s, vv))
            xs.append(x)
            if x == 1:
                break
        L = len(ws)
        for m in (1, 2, 3):
            seen = {}
            for i in range(L - m):
                f = tuple(ws[i:i + m])
                if f in seen:
                    i0 = seen[f]
                    if xs[i0] != xs[i]:
                        tested += 1
                        Hf = sum(s + v - 1 for s, v in f)
                        if abs(xs[i] - xs[i0]) < (1 << (Hf + 1)):
                            fails += 1
                            print("barrier FAIL", x0, i0, i, f)
                else:
                    seen[f] = i
    print(f"\nLE-B on true orbits: {tested} equal-factor pairs, fails={fails}")
    return fails == 0

if __name__ == "__main__":
    ok = check_LE0()
    ok &= check_envelope()
    threshold_table()
    ok &= check_C1_demo()
    ok &= check_barrier_on_true_orbits()
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
