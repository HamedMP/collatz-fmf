"""lea03_lp_nogo.py -- Lemma E attack, part 3: exact LP / extreme-ray analysis
of the non-descent ballot constraint on (s,v) letter statistics.

The ONLY proved linear constraint on the letters of a non-descending prefix is
the exact ballot ledger (repo Theorem 55, bridge01 F4): if x_j >= x_0 for all
j <= N then  2^(H_N) x_0^(S_N) <= (3 x_0 + 1)^(S_N).  Per letter this charges
    w(s,v) = (s+v-1) - s*log2(3+1/x_0)
and requires all prefix sums of w to stay <= 0.

RESULT 1 (exact letter dichotomy; PROVED):  sum-zero feasibility of the
single-letter word l^infty is equivalent to w(l) <= 0, and
    w(s,v) < 0 for x_0 large  <=>  2^(s+v-1) < 3^s  <=>  l is EXPANDING.
So the letters that can appear with limiting density 1 in a ballot-feasible
word are EXACTLY the expanding letters -- which include (4,2), (5,2), (4,3),
(6,4), ... : all deep letters with v=2, and v>=3 letters of large depth.

RESULT 2 (LP no-go for a statistical Lemma E; PROVED by witnesses):
  (a) the word (4,2)^infty is prefix-ballot-feasible (non-G01 density 1);
  (b) for every s0 the word [(s0,2) (1,2)^K]^infty with the exact maximal K
      is prefix-ballot-feasible, and K(s0) -> infinity, so Type-A density can
      be pushed ABOVE ANY delta < 1;
  (c) (4,3)^infty is prefix-ballot-feasible (v>=3 density 1).
  Hence NO bound of the form "non-G01 letters have density <= delta_0 < 1"
  or "v>=3 letters have density -> 0" or "s>=4 letters have density -> 0"
  follows from the ballot inequality + letter statistics alone.  Any proof of
  (any quantitative form of) Lemma E must use the 2-adic/positional structure
  (as LE-B / LE1 in lea01 do), not just frequencies.  This sharpens WHY the
  problem is hard: the ballot polytope's recession cone contains all deep
  letters.

RESULT 3 (what the ballot DOES force; PROVED, quantitative):
  For any non-descending orbit with all letters of depth <= D (s <= D+2,
  any v), the Type-A letter density obeys (Banach limit along any subsequence)
      f_A <= (Wmax + d0*(D+2)) / (Wmax + (2 - log2(3))),
  Wmax = (D+2)log2(3) - (D+3), d0 = log2(1+1/(3 x_0)) -- e.g. for D=1
  (G01 + Type A) and x_0 -> infinity:  f_A <= 0.645195...; D=2: 0.763447...
  Similarly X_N <= (log2(3)-1+d0) T'_N - (2-log2(3)-d0) N exactly (repo).

log2(3) is certified by integer power comparisons (convergent sandwich).
"""
import sys
from fractions import Fraction

def certified_log2_3():
    """Rational sandwich for log2 3 via continued-fraction convergents,
    certified by exact big-integer comparisons."""
    lo, hi = None, None
    # convergents p/q of log2 3: 3^q vs 2^p decides side
    for (p, q) in [(1054, 665), (24727, 15601)]:
        if 3**q > 2**p:
            lo = Fraction(p, q)
        else:
            hi = Fraction(p, q)
    assert lo is not None and hi is not None and lo < hi
    assert 3**lo.denominator > 2**lo.numerator          # certifies log2 3 > lo
    assert 3**hi.denominator < 2**hi.numerator          # certifies log2 3 < hi
    return lo, hi

def check_prefix_ballot(word_period, x0, periods=3, verbose=""):
    """EXACT check that the periodic word (word_period)^infty satisfies the
    non-descent ballot ledger 2^H x0^S <= (3x0+1)^S at every prefix.
    Rigorous for the infinite word: verifies (i) every prefix inside the
    first `periods` periods, (ii) the per-period drift is <= 1 (so prefix
    values decrease period-on-period and (i) propagates to all N)."""
    S = H = 0
    ok = True
    for rep in range(periods):
        for (s, v) in word_period:
            S += s
            H += s + v - 1
            if (1 << H) * x0**S > (3 * x0 + 1)**S:
                ok = False
    Sp = sum(s for s, v in word_period)
    Hp = sum(s + v - 1 for s, v in word_period)
    drift_le_1 = (1 << Hp) * x0**Sp <= (3 * x0 + 1)**Sp
    if verbose:
        print(f"  {verbose}: prefixes over {periods} periods OK={ok}, "
              f"per-period drift<=1: {drift_le_1}"
              f"  => feasible for ALL N: {ok and drift_le_1}")
    return ok and drift_le_1

def result1():
    lo, hi = certified_log2_3()
    print(f"certified: log2(3) in ({lo} , {hi})  "
          f"= ({float(lo):.12f}, {float(hi):.12f})")
    print("\nRESULT 1: ballot-self-sustaining letters = expanding letters "
          "(2^(s+v-1) < 3^s), exact integer test:")
    rows = []
    for s in range(1, 8):
        exp_vs = [v for v in range(2, 9) if (1 << (s + v - 1)) < 3**s]
        rows.append((s, exp_vs))
    for s, vs in rows:
        print(f"  s={s}: expanding for v in {vs if vs else 'NONE'}")
    print("  (4,2),(5,2),(6,2),(4,3),(5,3),(6,3),(6,4)... are all "
          "self-sustaining; non-G01 and unconstrained by frequencies.")
    return True

def result2():
    print("\nRESULT 2: explicit prefix-ballot-feasible witness words "
          "(exact integer verification, x0 = 2^20+3... arbitrary):")
    x0 = (1 << 20) + 3
    ok = True
    ok &= check_prefix_ballot([(4, 2)], x0, 5, "(4,2)^infty  [non-G01 density 1]")
    ok &= check_prefix_ballot([(4, 3)], x0, 5, "(4,3)^infty  [v>=3 density 1]")
    ok &= check_prefix_ballot([(10, 2)], x0, 5, "(10,2)^infty [depth 8, density 1]")
    print("  Type-A density -> 1 family  [(s0,2) then K Type-A letters]:")
    for s0 in (8, 16, 32, 64, 128):
        # find max K with feasibility (deep letter FIRST, then A-run)
        K = 0
        while True:
            per = [(s0, 2)] + [(1, 2)] * (K + 1)
            if not check_prefix_ballot(per, x0, 2):
                break
            K += 1
        per = [(s0, 2)] + [(1, 2)] * K
        assert check_prefix_ballot(per, x0, 3)
        dens = Fraction(K, K + 1)
        print(f"    s0={s0:4d}: max K={K:4d}, Type-A density = {K}/{K+1} "
              f"= {float(dens):.4f}")
    print("  => sup of achievable Type-A density = 1;  no delta_0 < 1 exists.")
    return ok

def result3():
    lo, hi = certified_log2_3()
    print("\nRESULT 3: what the ballot DOES force (bounded-depth alphabets, "
          "x0 -> infinity limits, certified interval arithmetic):")
    for D in (1, 2, 3, 4):
        # f_A <= Wmax/(Wmax + (2-lam)); Wmax = (D+2)lam-(D+3): use interval
        WmaxL = (D + 2) * lo - (D + 3)
        WmaxH = (D + 2) * hi - (D + 3)
        bL = WmaxL / (WmaxL + (2 - lo))
        bH = WmaxH / (WmaxH + (2 - hi))
        b = max(bL, bH)
        print(f"  depth <= {D} (s <= {D+2}, any v) + Type A: "
              f"f_A <= {float(b):.9f}")
    print("  (proof: sum w(l_j) <= S_N d0 with w >= 2-log2(3) on Type A and "
          "w >= -Wmax on the rest)")
    print("  X_N ledger (repo, restated): X_N <= (log2(3)-1+d0)T'_N - "
          "(2-log2(3)-d0)N  -- caps mean v-excess only via mean depth.")
    return True

if __name__ == "__main__":
    ok = result1()
    ok &= result2()
    ok &= result3()
    print("\nCONCLUSION (PROVED): the ballot inequality constrains letter "
          "FREQUENCIES not at all beyond\nthe expanding/contracting dichotomy: "
          "every expanding letter spans a feasible ray, and mixed\nrays reach "
          "Type-A density -> 1.  A statistical quantitative Lemma E is FALSE "
          "at the level of\nthe ballot LP; Lemma E must be attacked with "
          "2-adic/positional tools (lea01, lea02, lea04).")
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
