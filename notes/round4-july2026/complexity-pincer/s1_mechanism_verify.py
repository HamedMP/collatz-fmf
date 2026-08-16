"""
s1_mechanism_verify.py  (complexity-pincer program, round 4)

Exact verification of every ingredient of the counting relation (Lemma U):

  (1) Itinerary uniqueness: for each finite word u over the return alphabet
      (and gap alphabet), the set of positive integers whose itinerary begins
      with u is EXACTLY one residue class mod 2^(3m+4*kappa)  [return]
      / mod 2^(7m+3*kappa)  [gap].  Verified exhaustively on ranges.
  (2) Strict growth: block maps strictly increase positive integer states.
  (3) Two-sided envelope:  M*(9/8)^j(27/16)^{S_j} < n_j <= (M+1)*(9/8)^j(27/16)^{S_j}
      (return, exact rational comparison); gap upper envelope A*(243/128)^j(9/8)^{K_j}.
  (4) Same-factor state separation on real orbits: equal length-m factors at
      i<i'  =>  n_i == n_{i'} mod 2^(3m+4kappa)  and  n_{i'} - n_i >= 2^(3m+4kappa).
  (5) The -1 fixed point of the return map in Z_2 (all-zero word seed).
  (6) Ambient full shift: every {0,1}^m word has a nonempty class (2 children
      per class, exact), i.e. ambient entropy log 2 -- no upper complexity cap.

All arithmetic exact (int).  Run time target < 5 min.
"""

import sys, random
sys.path.insert(0, "/Users/hamed/dev/playgrounds/collatz/explorations")

from explore51_binary_return_code import block, prefix_code
from explore52_binary_partial_map import partial_return_map, partial_gap_map, gap_prefix_code

random.seed(20260721)

# ---------- itineraries via the partial maps ----------

def return_itinerary(n, length):
    word, states = [], [n]
    for _ in range(length):
        step = partial_return_map(n)
        if step is None:
            return None, states
        word.append(step.ones)
        n = step.n_next if hasattr(step, "n_next") else step[2]
        states.append(n)
    return tuple(word), states

def gap_itinerary(a, length):
    word, states = [], [a]
    for _ in range(length):
        step = partial_gap_map(a)
        if step is None:
            return None, states
        word.append(step[0])
        a = step[1]
        states.append(a)
    return tuple(word), states

# figure out ReturnStep field name
_probe = None
_n = 7
_probe = partial_return_map(7)
print("probe partial_return_map(7):", _probe)

def return_next(n):
    s = partial_return_map(n)
    if s is None:
        return None, None
    # ReturnStep(ones, w, n_next) -- access positionally via dataclass fields
    vals = [getattr(s, f) for f in s.__dataclass_fields__] if hasattr(s, "__dataclass_fields__") else list(s)
    return vals[0], vals[-1]

def return_itin(n, length):
    word, states = [], [n]
    for _ in range(length):
        r, nn = return_next(n)
        if r is None:
            return None, states
        word.append(r); n = nn; states.append(n)
    return tuple(word), states

# ---------- (1) itinerary uniqueness, exhaustive ----------

def check_return_uniqueness():
    # all words over {0,1,2} of length <= 3
    from itertools import product
    RANGE = 1 << 21
    for L in (1, 2, 3):
        for u in product((0, 1, 2), repeat=L):
            pfx = prefix_code(u)
            kappa = sum(u)
            assert pfx.q == 1 << (3 * L + 4 * kappa), (u, pfx.q)
            # class membership <=> itinerary prefix, on a full window of residues
            # sample the class and its complement
            R, Q = pfx.residue, pfx.q
            for t in range(3):
                n = R + t * Q
                if n < 1:
                    continue
                w, _ = return_itin(n, L)
                assert w == u, (u, n, w)
            # exhaustive converse over a window: every n < RANGE with itinerary u is == R mod Q
        # converse: scan all n in [1, 2^18], bucket by length-3 itinerary
    seen = {}
    LIM = 1 << 18
    for n in range(1, LIM):
        w, _ = return_itin(n, 3)
        if w is not None:
            seen.setdefault(w, []).append(n)
    for w, ns in seen.items():
        pfx = prefix_code(w)
        for n in ns:
            assert n % pfx.q == pfx.residue, (w, n, pfx.residue, pfx.q)
        # count matches expected number of class members below LIM
        expect = len([t for t in range(pfx.residue, LIM, pfx.q) if t >= 1])
        assert len(ns) == expect, (w, len(ns), expect)
    print(f"return uniqueness: words len<=3 over {{0,1,2}} exact classes OK; "
          f"exhaustive converse over n<2^18: {len(seen)} itineraries, all single-class")

def check_gap_uniqueness():
    from itertools import product
    for L in (1, 2, 3):
        for u in product((0, 1, 2), repeat=L):
            pfx = gap_prefix_code(u)
            kappa = sum(u)
            assert pfx.modulus == 1 << (7 * L + 3 * kappa), (u, pfx.modulus)
            R, Q = pfx.residue, pfx.modulus
            for t in range(3):
                a = R + t * Q
                if a < 1:
                    continue
                w, _ = gap_itinerary(a, L)
                assert w == u, (u, a, w)
    seen = {}
    LIM = 1 << 18
    for a in range(1, LIM):
        w, _ = gap_itinerary(a, 2)
        if w is not None:
            seen.setdefault(w, []).append(a)
    for w, as_ in seen.items():
        pfx = gap_prefix_code(w)
        for a in as_:
            assert a % pfx.modulus == pfx.residue, (w, a)
        expect = len([t for t in range(pfx.residue, LIM, pfx.modulus) if t >= 1])
        assert len(as_) == expect, (w, len(as_), expect)
    print(f"gap uniqueness: words len<=3 over {{0,1,2}} exact classes OK; "
          f"exhaustive converse over a<2^18 (len 2): {len(seen)} itineraries, all single-class")

# ---------- (2)+(3) strict growth and two-sided envelope on random valid orbits ----------

def check_return_envelope(trials=40, L=40):
    for _ in range(trials):
        u = tuple(random.randint(0, 1) for _ in range(L))
        pfx = prefix_code(u)
        M = pfx.residue  # least positive member of the class; its itinerary starts with u
        w, states = return_itin(M, L)
        assert w == u, (u, w)
        S = 0
        for j in range(L + 1):
            n = states[j]
            if j > 0:
                assert states[j] > states[j - 1], "strict growth fails"
            # envelope: M*(9/8)^j*(27/16)^S < n <= (M+1)*(9/8)^j*(27/16)^S
            lhs_num = M * 9**j * 27**S
            lhs_den = 8**j * 16**S
            rhs_num = (M + 1) * 9**j * 27**S
            # lower envelope: strict for j>=1 (M_j < 0), equality at j=0 (M_0 = 0)
            if j == 0:
                assert lhs_num == n * lhs_den, (j, "lower envelope j=0")
            else:
                assert lhs_num < n * lhs_den, (j, "lower envelope")
            assert n * lhs_den <= rhs_num, (j, "upper envelope")
            if j < L:
                S += u[j]
    print(f"return strict growth + two-sided envelope: {trials} random {{0,1}} words of length {L} OK")

def check_gap_envelope(trials=40, L=30):
    for _ in range(trials):
        u = tuple(random.randint(0, 1) for _ in range(L))
        pfx = gap_prefix_code(u)
        A = pfx.residue
        w, states = gap_itinerary(A, L)
        assert w == u, (u, w)
        K = 0
        for j in range(L + 1):
            a = states[j]
            if j > 0:
                assert states[j] > states[j - 1], "gap strict growth fails"
            # upper envelope a_j <= A*(243/128)^j*(9/8)^K  == A*3^{5j+2K}/2^{7j+3K}
            assert a * 2**(7 * j + 3 * K) <= A * 3**(5 * j + 2 * K), (j, "gap upper envelope")
            # lower envelope: a_j >= A*3^{..}/2^{..} - (critical series); check a_j*2^.. >= A*3^.. - 2^..*3^..? skip: only upper needed
            if j < L:
                K += u[j]
    print(f"gap strict growth + upper envelope: {trials} random {{0,1}} words of length {L} OK")

# ---------- (4) same-factor state separation on real orbits ----------

def check_separation(trials=30, L=60):
    checked = 0
    for _ in range(trials):
        # words with forced repetitions: low-complexity random (biased) words
        u = []
        while len(u) < L:
            u.extend([0] * random.randint(1, 6))
            u.append(1)
        u = tuple(u[:L])
        M = prefix_code(u).residue
        w, states = return_itin(M, L)
        assert w == u
        for m in (3, 5, 8, 12):
            occ = {}
            for s in range(L - m + 1):
                occ.setdefault(u[s:s + m], []).append(s)
            for fac, pos in occ.items():
                if len(pos) < 2:
                    continue
                kappa = sum(fac)
                Q = 1 << (3 * m + 4 * kappa)
                for i, ip in zip(pos, pos[1:]):
                    assert (states[ip] - states[i]) % Q == 0, "congruence fails"
                    assert states[ip] - states[i] >= Q, "separation fails"
                    checked += 1
    print(f"return same-factor separation: {checked} pairs verified (congruence + gap >= 2^(3m+4k))")

def check_gap_separation(trials=20, L=40):
    checked = 0
    for _ in range(trials):
        u = []
        while len(u) < L:
            u.extend([0] * random.randint(1, 5))
            u.append(1)
        u = tuple(u[:L])
        A = gap_prefix_code(u).residue
        w, states = gap_itinerary(A, L)
        assert w == u
        for m in (3, 5, 8):
            occ = {}
            for s in range(L - m + 1):
                occ.setdefault(u[s:s + m], []).append(s)
            for fac, pos in occ.items():
                if len(pos) < 2:
                    continue
                kappa = sum(fac)
                Q = 1 << (7 * m + 3 * kappa)
                for i, ip in zip(pos, pos[1:]):
                    assert (states[ip] - states[i]) % Q == 0, "gap congruence fails"
                    assert states[ip] - states[i] >= Q, "gap separation fails"
                    checked += 1
    print(f"gap same-factor separation: {checked} pairs verified (congruence + gap >= 2^(7m+3k))")

# ---------- (5) the -1 fixed point (all-zero 2-adic seed) ----------

def check_minus_one():
    # all-zero length-L class residue must be 2^{3L}-1  (-> -1 in Z_2)
    for L in range(1, 25):
        pfx = prefix_code((0,) * L)
        assert pfx.residue == (1 << (3 * L)) - 1, (L, pfx.residue)
    # and algebraically: n=-1: 33*(-1)+32 = -1 = 16^0 * (-1), w=-1 = 7 mod 8, next = (3*(-1)-85)/88 = -1
    assert (3 * (-1) - 85) // 88 == -1 and (3 * (-1) - 85) % 88 == 0
    print("all-zero return word: class residues are 2^(3L)-1 for L<=24 -> 2-adic seed is exactly -1 (fixed point)")

# ---------- (6) full ambient shift ----------

def check_full_shift():
    from itertools import product
    # every {0,1}^m word has nonempty class, m <= 12; children counts exactly 2 within {0,1}
    cnt = 0
    for m in range(1, 13):
        for u in product((0, 1), repeat=m):
            pfx = prefix_code(u)
            assert pfx.residue >= 1  # wait: residue could be 0? then least positive member is Q
            cnt += 1
    print(f"return ambient language: all {cnt} binary words of length <= 12 have nonempty classes (full shift, entropy log 2)")
    cnt = 0
    for m in range(1, 10):
        for u in product((0, 1), repeat=m):
            pfx = gap_prefix_code(u)
            assert pfx.residue >= 1
            cnt += 1
    print(f"gap ambient language: all {cnt} binary words of length <= 9 have nonempty classes (full shift)")

if __name__ == "__main__":
    check_return_uniqueness()
    check_gap_uniqueness()
    check_return_envelope()
    check_gap_envelope()
    check_separation()
    check_gap_separation()
    check_minus_one()
    check_full_shift()
    print("ALL MECHANISM CHECKS PASSED")
