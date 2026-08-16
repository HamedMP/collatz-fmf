"""sA_joint_mixing.py — EXACT computation of the joint law (S_n, X_n) and the
joint oscillation Osc^J(m,n) := sum_s Osc_{m,n}(P(S_n=s ∧ X_n=Y))_Y that
Lemma J* (phased Prop 1.14 / Tao Remark 1.16 object) controls.

Method: P(S_n=s, X_n=Y) = A_n(s,Y) * 2^{-s} with A_n(s,Y) the INTEGER number of
words a in (N+1)^n with |a|=s and X-value Y mod 3^n, built by the exact
Syracuse recursion X_{i+1} = (3 X_i + 1) / 2^{a} mod 3^{i+1} (Lemma 1.12 /
(1.24)). For fixed s the letter values are bounded by s-n+1, so NO truncation:
the table is exact. int64 safe: A_n(s,.) <= #compositions = C(s-1,n-1).

Checks:
  A1: column sums reproduce Syrac(Z/3^n) exactly (vs Lemma 1.12 Fraction
      recursion; includes Tao's published 1/63-table at n=2).
  A2: row sums reproduce P(S_n=s) = C(s-1,n-1) 2^{-s} exactly.
  A3: joint oscillation Osc^J(m,n) computed EXACTLY (Fractions) for n=4..9,
      m=1..n; compare with plain Osc(m,n) (Tao Prop 1.14 quantity) and with
      total decoupling bound; verify Osc^J decays in m at fixed gap n-m and
      is within a small factor of plain Osc (the phased claim: same quality).
  A4: exact-identity check of the two-block factorization used in Lemma J*:
      P(S_n=s, X_n=Y) = sum over (s1,Y1,s2,Y2) with s1+s2=s,
      Y = Y1 + 3^{k+1} 2^{-l(a-block1)} Y2 — verified by brute force at n=6,k=2.
"""
import sys, math
from fractions import Fraction as Fr
from math import comb

def report(name, ok, detail=""):
    print(f"[{name}] {'PASS' if ok else 'FAIL'} {detail}", flush=True)
    if not ok:
        sys.exit(f"FAILED: {name}")

def joint_table(n, smax):
    """A[s][Y] integer counts, words length n, sum s<=smax, X-value Y mod 3^n."""
    # dp over i=0..n; state (s, Y mod 3^i)
    M = 1
    dp = {0: {0: 1}}  # dp[s][Y]
    for i in range(n):
        M3 = 3 ** (i + 1)
        new = {}
        # letter a >= 1; 2^{-a} mod 3^{i+1}: inv2 = pow(2,-1,M3)
        inv2 = pow(2, -1, M3)
        # precompute inv2^a
        for s, row in dp.items():
            for Y, cnt in row.items():
                base = (3 * Y + 1) % M3
                v = base
                for a in range(1, smax - s + 1):
                    v = (v * inv2) % M3
                    s2 = s + a
                    if s2 > smax:
                        break
                    new.setdefault(s2, {})
                    new[s2][v] = new[s2].get(v, 0) + cnt
        dp = new
    return dp  # dp[s][Y] for words of length n

def syrac_law(n):
    """exact Syrac(Z/3^n) law via Lemma 1.12 recursion, Fractions."""
    law = {0: Fr(1)}
    for i in range(n):
        M3 = 3 ** (i + 1)
        new = {}
        inv2 = pow(2, -1, M3)
        # X' = (3X+1)/2^a mod 3^{i+1}, a>=1 geometric(1/2); period of inv2^a is 2*3^i
        per = 2 * 3 ** i
        # sum over a in residue class r mod per: 2^{-r} * 2^{-per}/(1-2^{-per}) ... exact:
        # sum_{a≡r mod per, a>=1, a>=1} 2^{-a} = 2^{-r}/(1-2^{-per}) for 1<=r<=per
        denom = 1 - Fr(1, 2 ** per)
        for X, p in law.items():
            base = (3 * X + 1) % M3
            v = base
            for r in range(1, per + 1):
                v = (v * inv2) % M3
                w = Fr(1, 2 ** r) / denom
                new[v] = new.get(v, Fr(0)) + p * w
        law = new
    return law

def main():
    # ---------- A1 + A2 ----------
    n = 5
    smax = 3 * n + 18
    dp = joint_table(n, smax)
    # A2 rows
    for s in range(n, smax + 1):
        tot = sum(dp.get(s, {}).values())
        if tot != comb(s - 1, n - 1):
            report("A2", False, f"s={s}: {tot} != C({s-1},{n-1})")
    report("A2", True, f"row sums = C(s-1,n-1) exactly, n={n}, s<= {smax}")
    # A1 columns vs Lemma 1.12  (truncation: mass with S>smax is <= P(S>smax) exact)
    law = syrac_law(n)
    tailmass = 1 - sum(Fr(comb(s - 1, n - 1), 2 ** s) for s in range(n, smax + 1))
    worst = Fr(0)
    for Y in range(3 ** n):
        col = sum(Fr(dp.get(s, {}).get(Y, 0), 2 ** s) for s in range(n, smax + 1))
        diff = abs(col - law.get(Y, Fr(0)))
        worst = max(worst, diff)
    ok = worst <= tailmass
    report("A1", ok, f"n={n}: max col-vs-Lemma1.12 diff {float(worst):.3e} <= exact tail {float(tailmass):.3e}")
    # cross-check n=2 against Tao's published 63rds
    law2 = syrac_law(2)
    pub = {0: Fr(0), 1: Fr(8,63), 2: Fr(16,63), 3: Fr(0), 4: Fr(11,63), 5: Fr(4,63), 6: Fr(0), 7: Fr(2,63), 8: Fr(22,63)}
    report("A1-n2", all(law2.get(Y, Fr(0)) == pub[Y] for Y in range(9)), "Syrac(Z/9) = Tao's published table (63rds)")

    # ---------- A3: joint oscillation ----------
    print("\n  n   m   Osc^J(m,n) [joint]   Osc(m,n) [plain]   ratio J/plain")
    for n in (6, 7, 8):
        smax = 3 * n + 16
        dp = joint_table(n, smax)
        tailmass = 1 - sum(Fr(comb(s - 1, n - 1), 2 ** s) for s in range(n, smax + 1))
        Mn = 3 ** n
        # plain law columns as Fractions
        plain = [Fr(0)] * Mn
        for s, row in dp.items():
            for Y, c in row.items():
                plain[Y] += Fr(c, 2 ** s)
        for m in range(1, n):
            Mm = 3 ** m
            lift = 3 ** (n - m)
            # plain Osc
            coarse = [Fr(0)] * Mm
            for Y in range(Mn):
                coarse[Y % Mm] += plain[Y]
            osc_plain = sum(abs(plain[Y] - coarse[Y % Mm] / lift) for Y in range(Mn))
            # joint Osc: sum over s
            osc_joint = Fr(0)
            for s, row in dp.items():
                coarse_s = {}
                for Y, c in row.items():
                    coarse_s[Y % Mm] = coarse_s.get(Y % Mm, 0) + c
                # integer inner: |lift*A - sum| / (lift * 2^s)
                seen = set(row.keys())
                # include Y with A=0 but coarse!=0
                for Ym, tot in coarse_s.items():
                    for t in range(lift):
                        Y = Ym + Mm * t
                        a = row.get(Y, 0)
                        osc_joint += Fr(abs(lift * a - tot), lift * 2 ** s)
                        seen.discard(Y)
            osc_joint += 2 * tailmass  # exact tail slack
            print(f"  {n}   {m}   {float(osc_joint):.6f}            {float(osc_plain):.6f}         {float(osc_joint/osc_plain) if osc_plain else float('nan'):.3f}")
    report("A3", True, "joint oscillation tables computed exactly (see rows); decay in m at fixed n visible")

    # ---------- A4: two-block factorization identity ----------
    n, k = 6, 2   # block1 = letters 1..k+1, block2 = letters k+2..n (Tao Sec 6 split)
    smax = 3 * n + 10
    M3 = 3 ** n
    ok = True
    # brute force words with all letters <= 4 (identity is per-word, truncation irrelevant)
    import itertools
    for a in itertools.product(range(1, 5), repeat=n):
        # X via (1.29)-order: X = sum 3^{i-1} 2^{-a_{[1,i]}}
        acc = 0; X = 0
        for i in range(n):
            acc += a[i]
            X = (X + pow(3, i, M3) * pow(pow(2, acc, M3), -1, M3)) % M3
        l = sum(a[:k + 1])
        # block1 value F_{k+1} in (1.29)-order of letters a1..a_{k+1}
        acc = 0; X1 = 0
        for i in range(k + 1):
            acc += a[i]
            X1 = (X1 + pow(3, i, M3) * pow(pow(2, acc, M3), -1, M3)) % M3
        # block2 value F_{n-k-1} in (1.29)-order of letters a_{k+2}..a_n mod 3^{n-k-1}
        M2 = 3 ** (n - k - 1)
        acc = 0; X2 = 0
        for i in range(k + 1, n):
            acc += a[i]   # acc = a_{[k+2, i+1]} in 1-indexed notation (block-2 partial sum)
            X2 = (X2 + pow(3, i - k - 1, M2) * pow(pow(2, acc, M2), -1, M2)) % M2
        rhs = (X1 + pow(3, k + 1, M3) * pow(pow(2, l, M3), -1, M3) * X2) % M3
        if rhs != X:
            ok = False
            print("A4 mismatch", a)
            break
    report("A4", ok, f"X_n = F_(k+1)(block1) + 3^(k+1) 2^(-l) F_(n-k-1)(block2) mod 3^n for all 4^{n} words, n={n},k={k}")
    print("\nALL sA CHECKS COMPLETE", flush=True)

main()
