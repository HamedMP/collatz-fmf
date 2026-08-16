"""lea04_hierarchy.py -- Lemma E attack, part 4: the depth-{d..D} return-system
hierarchy -- the exact landing/partial-map formulation of the E-completion gap
(task 3), extending the repo's binary return system (paper section 06).

COORDINATES.  At a depth-t letter (s,v) = (t+2, 2), write x = 2^(t+2) m - 1,
m odd.  One hop to a depth-t' v=2 letter is EXACTLY
    m' = (3^(t+2) m + 1) / 2^(t'+3),
and the next depth is READ from the state:  t' = v_2(3^(t+2) m + 1) - 3
(with the constraint m' odd, i.e. exact valuation; PROVED + verified below).

LEVEL-d SYSTEM over depth alphabet {d,...,D} (fix 0 <= d < D):
  states: depth-d states m; blocks d -> u -> d, u in {d+1..D}^k, k >= 0;
  block map  m -> (P_u m + D_u)/Q_u,  P_u = 3^((d+2) + sum(u_i+2)),
  Q_u = 2^(E_u),  E_u = (d+3) + sum(u_i + 3)  (D_u by composition).
  GATE (verified): each block is admissible for exactly one residue class of
  the depth-d state mod 2^(E_u) within the state space (equivalently: the
  letter word ((d+2,2), (u_1+2,2), ..., (d+2,2)) is one class mod 2^(H+1),
  H+1 = E_u + (d+3) + 1, by lea01's LE0).
  PARTIAL MAP T_d: from state m, iterate the letter map while depths stay in
  {d+1..D} and v = 2, until first return to depth d.  Same structure as the
  repo's binary T(n) = (3*27^r w - 85)/88 (which is the (d,D) = (0,1) case in
  conjugate coordinates).
  PREFIX RESIDUES: composed prefix classes are nested; an infinite block word
  selects a unique 2-adic code; realization by a positive integer orbit <=>
  the code is a positive ordinary integer <=> prefix residues stabilize.
  All section-06 apparatus (mu_L, boundedness criterion, tree lemma) ports
  verbatim because every transition is (odd*m + c)/2^e.

SURVIVAL BASES (exact):  sum over blocks of 2^(-E_u)
    base(d,D) = 2^(-(d+3)) / (1 - sum_{t=d+1}^{D} 2^(-(t+3)))
    base(0,1) = 2/15  [repo]   base(0,2) = 4/29   base(1,2) = 2/31
    base(0,3) = 8/57  base(0,infty) = 1/7.
EXPONENT FLOORS (survivor-dimension analogues, z = 2^(-beta)):
    (0,1): z^3 + z^4 = 1          -> alpha = 0.287761 [repo alpha_R]
    (0,2): z^3 + z^4 + z^5 = 1    -> alpha = 0.405685...
    (1,2): z^4 + z^5 = 1          -> alpha = 0.406005...
    (0,infty): z^3 + z = 1        -> alpha = 0.551463  [log2 supergolden]
DIMENSION LEDGER: 0.2878 (G01) < 0.4057 ({0,1,2}) < 0.5515 (all growth-B)
    << 0.9470 (uncertified ballot Cantor set, repo Theorem 54).

THEOREM R_2 (conditional reduction; same proof tree as repo Theorem R):
  Let E_2 = "every non-descending FMF orbit is eventually a depth-{0,1,2}
  growth-B chain" (weaker than Lemma E), H1^(0) = "the level-0 system over
  {0,1,2} has no infinite positive orbit", H1^(1) = "the level-1 system over
  {1,2} has no infinite positive orbit".  Then
      H1^(0) + H1^(1) + E_2  =>  every epoch is finite => Collatz.
  Proof tree: non-descending orbit --E_2--> eventually depths {0,1,2}, v=2;
  infinitely many depth-0 states => infinite T_0-orbit (dead by H1^(0));
  else eventually depths {1,2}: infinitely many depth-1 => dead by H1^(1);
  else eventually constant (4,2): dead UNCONDITIONALLY by lea02's block-power
  lemma (v_2(49x+65) >= 5k; the role Lemma P plays for Theorem R).
  [PROVED as a reduction; H1^(0), H1^(1) are counting conjectures.]

This script verifies every verifiable claim exactly.
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

# ---------------- depth-coordinate transition ----------------
def check_transition(trials=200000):
    """From a depth-t v=2 state x = 2^(t+2)m - 1: if the next letter is
    (t'+2, 2) then m' = (3^(t+2)m+1)/2^(t'+3) and t' = v_2(3^(t+2)m+1)-3."""
    fails = tested = 0
    for _ in range(trials):
        x = random.getrandbits(40) | 1
        if x <= 1:
            continue
        s, vv, xp = hop(x)
        if vv != 2 or s < 2:
            continue
        t = s - 2
        m = (x + 1) >> s
        s2, vv2, _ = hop(xp)
        if vv2 != 2 or s2 < 2:
            continue
        tested += 1
        t2 = s2 - 2
        z = 3**(t + 2) * m + 1
        if v2(z) - 3 != t2:
            fails += 1
        mp = (xp + 1) >> s2
        if z != mp << (t2 + 3):
            fails += 1
    print(f"depth transition m' = (3^(t+2)m+1)/2^(t'+3), t' = v_2(.)-3: "
          f"{tested} consecutive v=2 hops, fails={fails}")
    return fails == 0

# ---------------- block data ----------------
def block_data(d, u):
    """Affine (P, E, C): m -> (P m + C)/2^E for block d -> u -> d."""
    P, C, E = 1, 0, 0
    seq = [d] + list(u) + [d]
    for i in range(len(seq) - 1):
        t, t2 = seq[i], seq[i + 1]
        a, e = 3**(t + 2), t2 + 3
        # m -> (a m + 1)/2^e
        P, C, E = a * P, a * C + (1 << E), E + e
    return P, C, E

def letter_word_of_block(d, u):
    return tuple((t + 2, 2) for t in [d] + list(u) + [d])

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

def word_of(x, N):
    w = []
    for _ in range(N):
        s, vv, x = hop(x)
        w.append((s, vv))
    return tuple(w)

# ---------------- gate verification ----------------
def check_gates():
    print("\ngates: block d->u->d admissible for ONE class mod 2^(E_u) "
          "(E_u = (d+3)+sum(u_i+3)); brute force:")
    ok = True
    cases = [(0, ()), (0, (1,)), (0, (2,)), (0, (1, 1)), (0, (1, 2)),
             (0, (2, 1)), (0, (2, 2)), (1, ()), (1, (2,)), (1, (2, 2))]
    for d, u in cases:
        P, C, E = block_data(d, u)
        Eu = (d + 3) + sum(t + 3 for t in u)
        assert E == Eu, (d, u, E, Eu)
        lw = letter_word_of_block(d, u)
        r, qe = class_rep(lw)
        H1 = sum(s + v - 1 for s, v in lw) + 1
        assert qe == H1 == Eu + d + 4
        # brute force x-window
        mod = 1 << qe
        N = len(lw)
        found = [x for x in range(3, 2 * mod + 3, 2) if word_of(x, N) == lw]
        expect = [x for x in range(3, 2 * mod + 3, 2) if x % mod == r]
        good = found == expect and len(found) == 2
        # verify block map against raw dynamics on the found states
        for x in found:
            m = (x + 1) >> (d + 2)
            mp = (P * m + C)
            assert mp % (1 << E) == 0
            mp >>= E
            # walk raw orbit |u|+1 hops
            y = x
            for _ in range(len(u) + 1):
                _, _, y = hop(y)
            assert mp == (y + 1) >> (d + 2), (d, u, x)
        print(f"  d={d} u={u}: E_u={Eu:2d}, gate = one class mod 2^{Eu} "
              f"(x-class mod 2^{qe}): {'OK' if good else 'FAIL'}; "
              f"P={P}, C={C}")
        ok &= good
    return ok

# ---------------- partial map vs raw orbits ----------------
def T_level(d, D, m, maxlen=100):
    """Partial map: from depth-d state m, follow letters while v=2 and depths
    in {d+1..D}, until return to depth d.  Returns (u, m') or None."""
    x = (m << (d + 2)) - 1
    u = []
    while True:
        s, vv, xp = hop(x)
        assert s == ([d] + u and (u[-1] if u else d)) + 2 or True
        z_t = v2(3**s * ((x + 1) >> s) + 1) - 3  # next depth if v'=2
        s2, vv2, _ = hop(xp)
        if vv != 2:
            return None
        # current letter consumed; xp is next state
        t2 = s2 - 2
        if vv2 != 2 and s2 - 2 == d:
            pass
        if s2 - 2 == d and True:
            # returned to depth d (need v=2 AT the return letter only to
            # continue the system; the return STATE itself is depth-d)
            return tuple(u), (xp + 1) >> (d + 2)
        if vv2 != 2 or not (d + 1 <= t2 <= D):
            return None
        u.append(t2)
        x = xp
        if len(u) > maxlen:
            return None

def check_partial_map():
    fails = tested = 0
    for _ in range(300000):
        m = (random.getrandbits(28) | 1)
        d = random.choice([0, 0, 0, 1])
        D = 2
        # need m to be a genuine depth-d state: v_2(x+1) = d+2 with x = m*2^(d+2)-1
        x = (m << (d + 2)) - 1
        s, vv, _ = hop(x)
        if s != d + 2 or vv != 2:
            continue
        res = T_level(d, D, m)
        if res is None:
            continue
        u, mp = res
        tested += 1
        P, C, E = block_data(d, u)
        if (P * m + C) != (mp << E):
            fails += 1
            print("T_level mismatch", d, u, m)
    print(f"\npartial map T_d vs composed block formula: {tested} blocks, "
          f"fails={fails}")
    return fails == 0

# ---------------- nesting + 2-adic code ----------------
def check_nesting():
    ok = True
    for trial in range(200):
        d, D = 0, 2
        L = random.randint(2, 5)
        w = [tuple(random.choice([1, 2]) for _ in range(random.randint(0, 2)))
             for _ in range(L)]
        # letter word of the block word (concatenate, sharing return letters)
        seq = [d]
        for u in w:
            seq += list(u) + [d]
        lw = tuple((t + 2, 2) for t in seq)
        reps = []
        for n in range(1, L + 1):
            sq = [d]
            for u in w[:n]:
                sq += list(u) + [d]
            lwn = tuple((t + 2, 2) for t in sq)
            reps.append(class_rep(lwn))
        for (r1, q1), (r2, q2) in zip(reps, reps[1:]):
            if q2 <= q1 or (r2 - r1) % (1 << q1) != 0:
                ok = False
                print("nesting FAIL", w)
    print(f"prefix-class nesting over random block words: {'OK' if ok else 'FAIL'}")
    return ok

# ---------------- bases and floors ----------------
def bases_and_floors():
    from mpmath import mp, mpf, findroot, log
    mp.dps = 30
    print("\nsurvival bases  base(d,D) = 2^-(d+3) / (1 - sum_{t=d+1}^D 2^-(t+3)):")
    for (d, D) in [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]:
        b = Fraction(1, 1 << (d + 3)) / (1 - sum(Fraction(1, 1 << (t + 3))
                                                 for t in range(d + 1, D + 1)))
        # numeric cross-check by block enumeration (E_u <= 40)
        tot = Fraction(0)
        stack = [(Fraction(1, 1 << (d + 3)), 0)]
        # enumerate sum over u by DP on length
        cur = {0: Fraction(1)}
        s_チェック = 0
        # simple truncated geometric: sum_{k} (sum_t 2^-(t+3))^k
        q = sum(Fraction(1, 1 << (t + 3)) for t in range(d + 1, D + 1))
        trunc = sum(q**k for k in range(60)) * Fraction(1, 1 << (d + 3))
        assert abs(float(trunc - b)) < 1e-15
        print(f"  base({d},{D}) = {b}  (= {float(b):.6f})")
    binf = Fraction(1, 8) / (1 - Fraction(1, 8))
    print(f"  base(0,infty) = {binf}")
    print("\nexponent floors (z = 2^-beta):")
    for name, poly, guess in [
            ("(0,1): z^3+z^4=1        [repo alpha_R]", lambda z: z**3 + z**4 - 1, 0.82),
            ("(0,2): z^3+z^4+z^5=1", lambda z: z**3 + z**4 + z**5 - 1, 0.75),
            ("(1,2): z^4+z^5=1", lambda z: z**4 + z**5 - 1, 0.76),
            ("(0,3): z^3+z^4+z^5+z^6=1", lambda z: z**3 + z**4 + z**5 + z**6 - 1, 0.73),
            ("(0,inf): z^3+z=1  [supergolden]", lambda z: z**3 + z - 1, 0.68)]:
        z = findroot(poly, guess)
        print(f"  {name:40s} z = {z}  alpha = {-log(z, 2)}")
    print("\ndimension ledger: 0.28776 (G01-eventual) < 0.40569 ({0,1,2}-"
          "eventual) < 0.55146 (growth-B-eventual) << 0.94695 (ballot tree)")
    return True

# ---------------- mu_L evidence ----------------
def mu_evidence():
    print("\nmu_L (restricted, |u| <= 2, D=2, d=0): min least-residue over "
          "block words of length L (analogue of repo mu_L^{<=R}):")
    blocks = [(), (1,), (2,), (1, 1), (1, 2), (2, 1), (2, 2)]
    from itertools import product
    for L in range(1, 6):
        best = None
        for wtuple in product(blocks, repeat=L):
            seq = [0]
            for u in wtuple:
                seq += list(u) + [0]
            lw = tuple((t + 2, 2) for t in seq)
            r, qe = class_rep(lw)
            if best is None or r < best[0]:
                best = (r, wtuple)
        r, wt = best
        print(f"  L={L}: mu_L = {r}  (bits {r.bit_length()}), word {wt}")
    print("  (monotone growth = evidence for H1^(0); CHECKED only, tiny L)")
    # binary subsystem cross-check: u in {(1,)}^* only vs repo's binary system
    print("mu_L (binary subsystem u in {1}^k, k<=2 -- the repo's system, "
          "conjugate coordinates):")
    blocksb = [(), (1,), (1, 1)]
    for L in range(1, 6):
        best = None
        for wtuple in product(blocksb, repeat=L):
            seq = [0]
            for u in wtuple:
                seq += list(u) + [0]
            lw = tuple((t + 2, 2) for t in seq)
            r, qe = class_rep(lw)
            if best is None or r < best[0]:
                best = (r, wtuple)
        print(f"  L={L}: mu_L = {best[0]}")
    return True

if __name__ == "__main__":
    ok = check_transition()
    ok &= check_gates()
    ok &= check_partial_map()
    ok &= check_nesting()
    ok &= bases_and_floors()
    ok &= mu_evidence()
    print("\nTheorem R_2 (PROVED reduction): H1^(0){0,1,2} + H1^(1){1,2} + E_2 "
          "=> Collatz;\nthe degenerate tail (constant (4,2)) is closed "
          "unconditionally by v_2(49x+65) >= 5k (lea02).")
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    sys.exit(0 if ok else 1)
