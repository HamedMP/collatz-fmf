"""verify_identities.py -- exact checks for sunit/REPORT.md (track sunit, round 6).

Run:  taskset -c 2 /home/matrix/home/projects/collatz/venv/bin/python verify_identities.py
Expected last line:  ALL CHECKS PASSED

Generalised hop map for x -> (a x + d)/2 on odd x (a odd >= 3, d odd):
    y = (a-2) x + d = 2^s m   (m odd, s >= 1, y != 0),
    y' = (a^s m - d)/2^(v-1) + d,   v-1 = v_2(a^s m - d) >= 1,   h = s + v - 1.
(a,d) = (3,1) is the repo's FMF hop: x' = (3^s m - 1)/2^(v-1), letter (s,v).
Negative x with (3,1) is the 3n-1 map.

Checked, all in exact integer arithmetic:
 H1  one-hop:  2^h y' = a^s y + d (2^h - 2^s), and for (3,1) agreement with the literal Collatz
     definition of FMF (first orbit value divisible by 4).
 H2  k-hop identity (STATE.md section A, hop-word version), tuple form sum = 0:
       2^(T-s0) m_k - a^(S_k) m_0 - sum_i d a^(sig_i) 2^(H_(i+1)-s0) + sum_i d a^(sig_i) 2^(H_i+s_i-s0) = 0
     T = H_k + s_k, sig_i = S_k - S_(i+1).
 H3  2-adic valuation pattern of the 2k+2 terms (before dividing by 2^s0):
       s0, s0, H_1, H_1+s_1, ..., H_k, H_k+s_k  -- one tie, then strictly increasing.
 H4  brute force: no vanishing proper non-empty subsum (k <= 5: all 2^(2k+2)-2 subsets).
 H5  gcd of the tuple divides d (so = 1 for d = 1).
 H6  size: |Z_k| <= 2^k a^(S_k) |y_0| with Z_k = 2^(H_k) y_k; hence max|x_i| of the tuple is
     <= 2^(k+1) a^(S_k) |m_0| ; and S-free part product <= |m_0 m_k| d^(2k).
 R1-R4 the same for the binary return map in v = 8(33n+32) coordinates (and a = 5 analogue).
"""
import random
import sys
from math import gcd
from itertools import combinations

random.seed(20261117)
CHK = {}


def bump(k, n=1):
    CHK[k] = CHK.get(k, 0) + n


def v2(x):
    assert x != 0
    x = abs(x)
    return (x & -x).bit_length() - 1


def hop(y, a=3, d=1):
    """one generalised hop in y-coordinates; returns (s, v, y')"""
    assert y != 0 and y % 2 == 0
    s = v2(y)
    m = y >> s            # exact (python >> on negative even multiples is exact here)
    assert m * (1 << s) == y and m % 2 != 0
    p = a ** s * m - d
    assert p != 0 and p % 2 == 0
    v1 = v2(p)
    q = p >> v1
    assert q * (1 << v1) == p
    return s, v1 + 1, q + d


def fmf_literal(x):
    """literal definition: first value in the Collatz orbit of odd x divisible by 4; returns x'."""
    assert x % 2 != 0
    z = x
    while True:
        z = 3 * z + 1 if z % 2 else z // 2
        if z % 4 == 0:
            break
    return z >> v2(z), v2(z)


def no_vanishing_subsum(xs):
    n = len(xs)
    assert sum(xs) == 0
    # enumerate subsets containing index 0 (complement symmetric), sizes 1..n-1
    # Gray-code free simple enumeration
    rest = xs[1:]
    tot = xs[0]
    for mask in range(0, (1 << (n - 1)) - 1):  # exclude the full set
        s = tot
        mm = mask
        i = 0
        while mm:
            if mm & 1:
                s += rest[i]
            mm >>= 1
            i += 1
        if s == 0:
            return False
    return True


def check_orbit(y0, k, a=3, d=1, brute=True, tag=""):
    """returns T_k or None if the orbit hits y = 0 within k hops."""
    ys = [y0]
    ss, hs = [], []
    y = y0
    for _ in range(k):
        s, v, y2 = hop(y, a, d)
        h = s + v - 1
        assert (1 << h) * y2 == a ** s * y + d * ((1 << h) - (1 << s))       # H1
        bump("H1")
        ss.append(s)
        hs.append(h)
        ys.append(y2)
        y = y2
        if y == 0:
            return None
    sk = v2(ys[k])
    S = [0]
    H = [0]
    for i in range(k):
        S.append(S[-1] + ss[i])
        H.append(H[-1] + hs[i])
    s_all = ss + [sk]
    T = H[k] + sk
    m0 = ys[0] >> ss[0]
    mk = ys[k] >> sk
    # raw terms (before dividing by 2^s0)
    terms = [(1 << T) * mk, -(a ** S[k]) * ys[0]]
    vals = [T, ss[0]]
    for i in range(k):
        sig = S[k] - S[i + 1]
        terms.append(-d * a ** sig * (1 << H[i + 1]))
        vals.append(H[i + 1])
        terms.append(d * a ** sig * (1 << (H[i] + s_all[i])))
        vals.append(H[i] + s_all[i])
    assert sum(terms) == 0                                                    # H2
    bump("H2")
    for t, vv in zip(terms, vals):
        assert t != 0 and v2(t) == vv
    sv = sorted(vals)
    expect = []
    for i in range(k + 1):
        expect += [H[i] + s_all[i]] + ([H[i + 1]] if i < k else [])
    expect = sorted([ss[0]] + expect)
    assert sv == expect
    assert sv[0] == sv[1] == ss[0] and all(sv[j] < sv[j + 1] for j in range(1, len(sv) - 1))   # H3
    bump("H3")
    red = [t >> ss[0] for t in terms]
    assert all(r * (1 << ss[0]) == t for r, t in zip(red, terms))
    g = 0
    for r in red:
        g = gcd(g, r)
    assert d % g == 0                                                         # H5
    bump("H5")
    if brute and len(red) <= 12:
        assert no_vanishing_subsum(red), (y0, k, a, d)                        # H4
        bump("H4")
    # H6 size
    Zk = (1 << H[k]) * ys[k]
    cd = 2 if d == 1 else 1 + abs(d) + d * d      # |Z_(j+1)| <= cd * a^(s_j) |Z_j|  (REPORT Lemma 3)
    assert abs(Zk) <= cd ** k * a ** S[k] * abs(ys[0])
    assert max(abs(r) for r in red) <= cd ** k * a ** S[k] * abs(m0)
    bump("H6")
    return T


def seed_for_word(letters, s_last, a=3, d=1):
    """least positive y0 (as residue mod 2^(H_k+s_last+1)) whose first k hop letters are `letters`
    [(s,v),...] and whose k-th iterate has v_2(y_k) = s_last.  Returns y0 or None."""
    S = sum(s for s, v in letters)
    H = 0
    B = 0
    A = 1
    # 2^(H) y_k = a^S y_0 + B, built by the recursion 2^h y' = a^s y + d(2^h - 2^s)
    for s, v in letters:
        h = s + v - 1
        B = a ** s * B + d * ((1 << (H + h)) - (1 << (H + s)))
        A *= a ** s
        H += h
    mod = 1 << (H + s_last + 1)
    yk = 1 << s_last
    y0 = ((yk * (1 << H) - B) * pow(A, -1, mod)) % mod
    return y0, mod


def main():
    # ---- literal FMF agreement for (3,1) ----
    for x in list(range(1, 20001, 2)) + [random.getrandbits(80) | 1 for _ in range(3000)] \
            + [(1 << n) - 1 for n in range(1, 200)]:
        s, v, y2 = hop(x + 1)
        xl, vl = fmf_literal(x)
        assert xl == y2 - 1 and vl == v, x
        bump("FMF-literal")

    # ---- random orbits, (3,1), positive ----
    for _ in range(6000):
        bits = random.choice([8, 16, 40, 100, 300])
        x0 = random.getrandbits(bits) | 1
        k = random.randint(1, 5)
        check_orbit(x0 + 1, k)
    for _ in range(600):
        x0 = random.getrandbits(200) | 1
        check_orbit(x0 + 1, random.randint(6, 40), brute=False)
    # ---- exhaustive small ----
    for x0 in range(1, 6001, 2):
        for k in (1, 2, 3, 4):
            check_orbit(x0 + 1, k)
    # ---- adversarial: 2^n - 1, 2^n m - 1 ----
    for n in range(1, 400):
        for k in (1, 2, 3, 4, 5):
            check_orbit(1 << n, k, brute=(n < 120))
        check_orbit(1 << n, 30, brute=False)
    for _ in range(1500):
        n = random.randint(1, 150)
        m = random.getrandbits(random.choice([3, 10, 60])) | 1
        check_orbit((1 << n) * m, random.randint(1, 5))
    # ---- adversarial: prescribed hop words (growth chains, spikes), least-residue seeds ----
    made = 0
    for _ in range(4000):
        k = random.randint(1, 5)
        mode = random.choice(["g01", "spike", "rand", "deep"])
        if mode == "g01":
            letters = [(random.choice([2, 3]), 2) for _ in range(k)]
        elif mode == "spike":
            r = random.choice([1.2, 1.5, 2.0])
            s = random.randint(2, 9)
            letters = []
            for _ in range(k):
                letters.append((int(s), 2))
                s = s * r + 1
        elif mode == "deep":
            letters = [(random.randint(1, 40), random.randint(2, 30)) for _ in range(k)]
        else:
            letters = [(random.randint(1, 6), random.randint(2, 6)) for _ in range(k)]
        s_last = random.randint(1, 60)
        y0, mod = seed_for_word(letters, s_last)
        if y0 == 0:
            continue
        # verify the seed realises the word
        y = y0
        ok = True
        for (s, v) in letters:
            s2, v_2, y = hop(y)
            if (s2, v_2) != (s, v):
                ok = False
                break
        assert ok and v2(y) == s_last, (letters, s_last)
        made += 1
        bump("word-seed-realised")
        T = check_orbit(y0, k)
        H = sum(s + v - 1 for s, v in letters)
        assert T == H + s_last
        assert y0 < 2 ** (T + 1)          # so T_k > log2(y0) - 1 : ratio >= ~1 family
    # long growth chains (k up to 60, no brute)
    for _ in range(300):
        k = random.randint(10, 60)
        letters = [(random.choice([2, 3]), 2) for _ in range(k)]
        y0, mod = seed_for_word(letters, 1)
        check_orbit(y0, k, brute=False)
        check_orbit(y0 + mod * random.getrandbits(20), k, brute=False)
        bump("growth-chain")

    # ---- litmus maps ----
    # 3n-1 == negative x under (3,1); skip orbits hitting y = 0 (x = -1)
    hit0 = 0
    for x0 in list(range(-1, -8001, -2)) + [-(random.getrandbits(60) | 1) for _ in range(3000)]:
        if x0 == -1:
            continue
        for k in (1, 2, 3, 4):
            if check_orbit(x0 + 1, k) is None:
                hit0 += 1
    CHK["3n-1 orbits reaching x=-1 (degenerate, m_k=0) skipped"] = hit0
    # cycles of 3n-1: -5 and -17 (as negative 3n+1)
    for x0 in (-5, -7, -17, -25, -37, -55, -41, -61, -91):
        for k in (1, 2, 3, 4, 5):
            check_orbit(x0 + 1, k)
    # 5n+1: y = 3x+1
    for x0 in list(range(1, 8001, 2)) + [random.getrandbits(80) | 1 for _ in range(3000)] + [13, 33, 83, 17, 27, 43]:
        for k in (1, 2, 3, 4):
            check_orbit(3 * x0 + 1, k, a=5, d=1)
    # literal check of 5n+1 hop: x' = ((5^s m - 1)/2^(v-1))/3 is the first even value /2^.. of the orbit
    for x0 in range(1, 4001, 2):
        y = 3 * x0 + 1
        s, v, y2 = hop(y, 5, 1)
        z = x0
        for _ in range(s):
            assert z % 2 == 1
            z = (5 * z + 1) // 2
        assert z % 2 == 0 and (y2 - 1) % 3 == 0 and (z >> v2(z)) == (y2 - 1) // 3 and v2(z) == v - 1
        bump("5n+1 literal")
    # F_5(13) = 13 with letter (3,5)
    assert hop(40, 5, 1) == (3, 5, 40)
    # 3n+d and an+d
    for (a, d) in ((3, 5), (3, 7), (3, -5), (3, 11), (3, 13), (5, 3), (7, 1), (5, -1), (9, 1)):
        for x0 in list(range(1, 3001, 2)) + [random.getrandbits(50) | 1 for _ in range(800)]:
            y0 = (a - 2) * x0 + d
            if y0 == 0:
                continue
            for k in (1, 2, 3):
                check_orbit(y0, k, a=a, d=d)

    # ---- trivial-cycle witness for non-uniformity in k: x0 = 1 gives T_k = 2k+1, L_0 = 1 ----
    for k in range(1, 60):
        assert check_orbit(2, k, brute=(k <= 5)) == 2 * k + 1
    # 5n+1 cycle through 13: T_k = 7k + 3 with y_0 = 40
    for k in range(1, 40):
        assert check_orbit(40, k, a=5, brute=(k <= 5)) == 7 * k + 3
    # 3n-1 cycle (x = -5: y = -4): periodic, T_k linear in k
    Ts = [check_orbit(-4, k, brute=(k <= 5)) for k in range(1, 30)]
    assert all(Ts[i + 1] - Ts[i] == Ts[1] - Ts[0] for i in range(len(Ts) - 1)), Ts
    CHK["cycle slopes (T_k - T_(k-1)): 3n+1@1 = 2, 5n+1@13 = 7, 3n-1@-5 ="] = Ts[1] - Ts[0]

    # =================== return-map version ===================
    def T_step(n, a=3):
        if a == 3:
            y = 33 * n + 32
        else:
            y = 109 * n + 102
        if y == 0:
            return None, None
        t = v2(y)
        if t % 4:
            return None, None
        r = t // 4
        w = y >> t
        assert w * (1 << t) == y
        # block in v-coordinates: v = 8 y = 2^(4r+3) w -> v' = a^(3r+2) w + 1 ; need v' = 0 mod 8 and
        # the corresponding n' integral
        vp = a ** (3 * r + 2) * w + 1
        if vp % 8:
            return None, None
        yp = vp // 8
        den, off = (33, 32) if a == 3 else (109, 102)
        if (yp - off) % den:
            return None, None
        return (yp - off) // den, r

    # R0: agreement with the repo's closed form T(n) = (P_r n + D_r)/Q_r, gate w = 7/5 mod 8
    def repo_T(n):
        y = 33 * n + 32
        if y == 0:
            return None, None
        t = v2(y)
        if t % 4:
            return None, None
        r = t // 4
        w = y >> t
        if w % 8 != (7 if r % 2 == 0 else 5):
            return None, None
        P = 9 * 27 ** r
        Q = 1 << (4 * r + 3)
        D = 1 if r == 0 else (96 * 27 ** r - 85 * 16 ** r) // 11
        assert (P * n + D) % Q == 0
        return (P * n + D) // Q, r
    for n in list(range(-60000, 60000)) + [random.getrandbits(70) for _ in range(20000)]:
        assert T_step(n) == repo_T(n), n
        bump("R0 block form == repo closed form")

    def ret_check(n0, smax, a=3):
        den, off = (33, 32) if a == 3 else (109, 102)
        states = [n0]
        word = []
        n = n0
        while len(word) < smax + 1:
            n2, r = T_step(n, a)
            if n2 is None:
                break
            word.append(r)
            states.append(n2)
            n = n2
        L = len(word)
        if L < 2:
            return 0
        vs = [8 * (den * n + off) for n in states]
        al = [4 * r + 3 for r in word]
        bl = [3 * r + 2 for r in word]
        ws = []
        for j in range(L):
            assert v2(vs[j]) == al[j]
            ws.append(vs[j] >> al[j])
            assert vs[j + 1] == a ** bl[j] * ws[j] + 1                         # R1
            bump("R1")
        for s in range(1, L):
            A = sum(al[1:s + 1])
            B = sum(bl[0:s])
            units = [a ** sum(bl[l:s]) * 2 ** sum(al[1:l]) for l in range(1, s + 1)]
            tup = [(1 << A) * ws[s], -(a ** B) * ws[0]] + [-u for u in units]
            assert sum(tup) == 0                                               # R2
            vals = sorted(v2(t) for t in tup)
            assert vals[0] == vals[1] == 0 and all(vals[j] < vals[j + 1] for j in range(1, len(vals) - 1))  # R3
            g = 0
            for t in tup:
                g = gcd(g, t)
            assert g == 1
            if len(tup) <= 12:
                assert no_vanishing_subsum(tup)                                # R4
            assert sum(units) <= a ** B
            bump("R2-R4")
        return L

    longest = 0
    for n0 in range(-300000, 300000):
        longest = max(longest, ret_check(n0, 8))
    for n0 in range(0, 200000):
        ret_check(n0, 8, a=5)
    # least residues of random words (a = 3): build by composing blocks
    for _ in range(3000):
        L = random.randint(2, 9)
        word = [min(6, int(random.expovariate(1.2))) for _ in range(L)]
        P, Q, D = 1, 1, 0
        for r in word:
            p = 9 * 27 ** r
            q = 1 << (4 * r + 3)
            dd = 1 if r == 0 else (96 * 27 ** r - 85 * 16 ** r) // 11
            P, Q, D = p * P, q * Q, p * D + dd * Q
        R = (-D * pow(P, -1, Q)) % Q
        n0 = R + Q * random.randint(0, 5)
        assert ret_check(n0, L - 1) >= L
        bump("return word seeds")
    CHK["longest return word seen in |n| < 3e5"] = longest

    for k in sorted(CHK):
        print(f"  {k}: {CHK[k]}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
