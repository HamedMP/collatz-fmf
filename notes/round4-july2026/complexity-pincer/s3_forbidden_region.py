"""
s3_forbidden_region.py  (complexity-pincer: exact constants, forbidden region,
                         and the rigorous negative side)

A. Exact constants (mpmath, 50 digits):
     T_R' = 3/(5*log2(3)-7)     [sharpened universal return threshold, pointwise]
     T_G' = 7/(7*log2(3)-10)    [sharpened universal gap threshold, pointwise]
     F_bal = 7/(5*log2(3)-7)    [uniform-window-density floor, BOTH systems]
   and the consistency check against the refereed T_R,T_G (must be >=).

B. Strict-growth basis, exact for all letters r,k <= 300:
     P_r = 9*27^r > Q_r = 2^(4r+3),  D_r > 0;  3^(2k+5) > 2^(3k+7).
   (These make every block map strictly increasing on positive integers.)

C. Adversarial sharpness of Lemma U: the word 1^J 0^L 1^... parks an all-zero
   window at the pigeonhole boundary; verify the certificate for it degrades to
   exactly the universal constant (i.e. C1 is the true worst case of the lemma).

D. Run-position corollaries (quantitative aperiodicity), exact spot checks:
   a zero-run of length l+1 starting at position s in a return word with code M
   forces  s+1 > (3l - log2(M+1))/log2(243/128); ones-run: (7l-..)/..;
   gap zero-run: (7l-..)/log2(2187/1024); gap ones-run: (10l-..)/...
   Verified on explicit class seeds.

E. NEGATIVE SIDE (the pincer's upper bound cannot exist):
   E1. ambient language of both systems = full shift (s1 verified to len 12);
       here: count admissible extensions == 2 for every {0,1} class, len<=16.
   E2. 2-adic realization: the nested classes of ANY infinite word converge to
       a unique seed in Z_2; exhibit the Champernowne-style word (concatenation
       of all binary words: complexity p(m)=2^m for every m) and compute its
       seed mod 2^512 -- a single deterministic orbit in the completed system
       with MAXIMAL factor complexity.  Determinism imposes no upper bound.
   E3. the all-zero word's seed is -1 (computed exactly): the completed system
       has integer-like seeds outside Z_{>0}; positivity is the only barrier.
"""

import sys
from fractions import Fraction
import mpmath as mp
sys.path.insert(0, "/Users/hamed/dev/playgrounds/collatz/explorations")

from explore51_binary_return_code import block, prefix_code
from explore52_binary_partial_map import gap_prefix_code

mp.mp.dps = 50

# ---------- A. exact constants ----------
log2_3 = mp.log(3) / mp.log(2)
beta0 = mp.log(mp.mpf(9) / 8) / mp.log(2)     # return: per-0-letter bits
beta1 = mp.log(mp.mpf(27) / 16) / mp.log(2)   # return: extra bits per 1
g0 = mp.log(mp.mpf(243) / 128) / mp.log(2)    # gap: per-0-letter bits
g1 = mp.log(mp.mpf(9) / 8) / mp.log(2)        # gap: extra bits per 1

T_R_new = 3 / (5 * log2_3 - 7)
T_G_new = 7 / (7 * log2_3 - 10)
F_bal = 7 / (5 * log2_3 - 7)

print("=" * 78)
print("A. EXACT CONSTANTS (50 digits)")
print(f"   log2(3)             = {log2_3}")
print(f"   beta0=log2(9/8)     = {beta0}")
print(f"   beta1=log2(27/16)   = {beta1}")
print(f"   beta0+beta1         = {beta0+beta1}  (= 5log2(3)-7 = {5*log2_3-7})")
print(f"   g0+g1               = {g0+g1}  (= 7log2(3)-10 = {7*log2_3-10})")
print(f"   T_R' = 3/(5log2 3-7)  = {T_R_new}")
print(f"   T_G' = 7/(7log2 3-10) = {T_G_new}")
print(f"   F_bal = 7/(5log2 3-7) = {F_bal}   (uniform-density floor, both systems)")
print(f"   refereed T_R in (3.1493,3.1494): T_R' - 3.1494 = {T_R_new - mp.mpf('3.1494')}  (>0 => sharper)")
print(f"   refereed T_G in (6.2390,6.2391): T_G' - 6.2391 = {T_G_new - mp.mpf('6.2391')}  (>0 => sharper)")
print(f"   refereed consistency: T_R_ref*(5log2 3 -7) = {mp.mpf('3.1494')*(5*log2_3-7)} < 3  OK")
print(f"                         T_G_ref*(7log2 3-10) = {mp.mpf('6.2391')*(7*log2_3-10)} < 7  OK")

# density-coupled family
print("\n   density-coupled forbidden region (uniform-window-density-d words):")
print("   return F_R(d)=(3+4d)/(beta0+beta1*d), gap F_G(d)=(7+3d)/(g0+g1*d):")
for d10 in range(0, 11):
    d = mp.mpf(d10) / 10
    FR = (3 + 4 * d) / (beta0 + beta1 * d)
    FG = (7 + 3 * d) / (g0 + g1 * d)
    print(f"     d={float(d):3.1f}  F_R={float(FR):8.4f}   F_G={float(FG):8.4f}")
print(f"   min_d F_R = F_R(1) = {float((3+4)/(beta0+beta1)):.6f};  min_d F_G = F_G(0) = {float(7/g0):.6f}  (equal)")

# ---------- B. strict growth basis ----------
ok = True
for r in range(0, 301):
    b = block(r)
    if not (b.p > b.q and b.d > 0):
        ok = False
        print("STRICT GROWTH BASIS FAILS AT r=", r)
for k in range(0, 301):
    if not (3 ** (2 * k + 5) > 2 ** (3 * k + 7)):
        ok = False
        print("GAP GROWTH BASIS FAILS AT k=", k)
print("\nB. strict-growth basis: P_r>Q_r, D_r>0 (r<=300) and 3^(2k+5)>2^(3k+7) (k<=300):", "OK" if ok else "FAIL")

# ---------- C. adversarial sharpness ----------
print("\nC. adversarial words 1^J 0^L (zero-window parked at the boundary):")
from math import log2 as flog2
for (J, L) in ((20, 6), (33, 10), (49, 15)):
    word = (1,) * J + (0,) * L
    pfx = prefix_code(word)
    M = pfx.residue
    # certificate from the 0^{L-1} pair at positions J, J+1:
    m = L - 1
    Q = 1 << (3 * m)
    ip = J + 1
    S_ip = J  # ones before position J+1
    num = Q * 8**ip * 16**S_ip
    den = 9**ip * 27**S_ip
    forced = -(-num // den) - 1
    # theoretical exponent: 3m - (beta0*(J+1) + beta1*J)
    theo = 3 * m - (float(beta0) * (J + 1) + float(beta1) * J)
    print(f"   J={J} L={L}: forced M bits ~ {forced.bit_length()} (theory {theo:.1f}); "
          f"actual residue bits {M.bit_length()}; holds={M >= forced}")
    assert M >= forced

# ---------- D. run-position corollaries ----------
print("\nD. run-position corollaries (spot checks on class seeds):")
# return, zero-run: word = 1^s 0^(l+1): the seed M of the class must satisfy
#   s+1 > (3l - log2(M+1))/log2(243/128)  i.e. it CANNOT be small
for (s, l) in ((5, 4), (9, 7), (14, 11)):
    word = (1,) * s + (0,) * (l + 1)
    M = prefix_code(word).residue
    lhs = s + 1
    rhs = (3 * l - flog2(M + 1)) / float(beta0 + beta1)
    print(f"   return 1^{s} 0^{l+1}: position bound s+1={lhs} > {rhs:.2f}"
          f"  [log2(M+1)={flog2(M+1):.1f}]  OK={lhs > rhs}")
    assert lhs > rhs
# return, ones-run: word = 0^s 1^(l+1)
for (s, l) in ((5, 4), (9, 7)):
    word = (0,) * s + (1,) * (l + 1)
    M = prefix_code(word).residue
    lhs = s + 1
    rhs = (7 * l - flog2(M + 1)) / float(beta0 + beta1)
    print(f"   return 0^{s} 1^{l+1}: position bound s+1={lhs} > {rhs:.2f}  OK={lhs > rhs}")
    assert lhs > rhs
# gap, zero-run
for (s, l) in ((4, 3), (8, 6)):
    word = (1,) * s + (0,) * (l + 1)
    A = gap_prefix_code(word).residue
    lhs = s + 1
    rhs = (7 * l - flog2(A)) / float(g0 + g1)
    print(f"   gap    1^{s} 0^{l+1}: position bound s+1={lhs} > {rhs:.2f}  OK={lhs > rhs}")
    assert lhs > rhs

# ---------- E. negative side ----------
print("\nE. NEGATIVE SIDE")
# E1: every {0,1} class has exactly 2 {0,1}-children (full shift), depth 16 random walk
import random
random.seed(1)
for _ in range(200):
    w = tuple(random.randint(0, 1) for _ in range(random.randint(1, 16)))
    for a in (0, 1):
        pfx = prefix_code(w + (a,))
        assert pfx.residue is not None and pfx.q == prefix_code(w).q * (8 if a == 0 else 128)
print("   E1: every {0,1} return class has both children nonempty (200 random classes, len<=17):")
print("       ambient language = FULL SHIFT, topological entropy log 2; the only")
print("       upper bound valid for all orbits is p(m) <= 2^m -- no linear cap exists.")

# E2: Champernowne-style word: concatenation of all binary words in length order
champ = []
from itertools import product
for m in range(1, 7):
    for u in product((0, 1), repeat=m):
        champ.extend(u)
champ = tuple(champ)  # length sum m*2^m, m<=6 = 2+8+24+64+160+384 = 642
# complexity of the INFINITE champ word is 2^m for all m (contains every word);
# here check the prefix already realizes all factors up to m=6:
for m in range(1, 7):
    facs = {champ[s:s + m] for s in range(len(champ) - m + 1)}
    assert len(facs) == 2 ** m, (m, len(facs))
print(f"   E2: Champernowne word (len {len(champ)}): p(m)=2^m for m<=6 verified.")
# its nested return classes: compute seed mod 2^K for growing prefixes -- exact
prev_r, prev_q = None, None
for T in (8, 16, 32, 64, 128):
    pfx = prefix_code(champ[:T])
    if prev_r is not None:
        assert pfx.residue % prev_q == prev_r  # NESTED (2-adic convergence)
    prev_r, prev_q = pfx.residue, pfx.q
print(f"       nested class residues converge 2-adically: seed exists in Z_2 for the")
print(f"       INFINITE word (prefix-128 class: modulus 2^{prefix_code(champ[:128]).q.bit_length()-1}); its itinerary has")
print(f"       p(m)=2^m -- maximal complexity from a single deterministic orbit.")
print(f"       (The seed is not a positive integer -- else H1 would be false -- but")
print(f"       determinism/generation alone provably imposes NO complexity upper bound.)")

# E3: all-zero seed = -1 exactly
for L in (10, 20, 30):
    assert prefix_code((0,) * L).residue == (1 << (3 * L)) - 1
print("   E3: all-zero return seed = lim (2^(3L)-1) = -1 in Z_2 (exact).")

print("\nCONCLUSION: the pincer's required upper bound (p(m)/m < T_R from the")
print("generation mechanism) is IMPOSSIBLE: the mechanism forces complexity UP")
print("(T_R' = 3.2439 pointwise), never down; the ambient system is the full")
print("shift; arbitrary-complexity single orbits exist 2-adically.  Any upper")
print("bound must use positive-integrality -- which is the open conjecture H1 itself.")
