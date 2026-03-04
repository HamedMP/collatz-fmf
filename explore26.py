"""
explore26.py - Deterministic Proof Attempt: The 2-adic Cesaro Argument

We have: rho = E[R^alpha] < 1 for alpha = 0.53 (Theorem 19, from exact formulas).
We need: every trajectory x_0, x_1 = F(x_0), x_2 = F^2(x_0), ... reaches 1.

Key idea: If the TIME AVERAGE of log(R_i) equals the SPACE AVERAGE (-0.83),
then log(x_n/x_0) = sum log(R_i) ~ -0.83n -> -inf, so x_n -> 0 -> 1.

The time average equals the space average IF the sequence x_i mod M
is equidistributed (Weyl's equidistribution theorem analogue).

QUESTION: Is x_n mod M equidistributed along every FMF trajectory?

This is what we test here. If x_n mod M visits each residue class with
the correct frequency (as predicted by the state-independent transitions),
then the deterministic proof is complete.

The state-independence (Theorem 12) says: regardless of x_n mod M,
the NEXT value x_{n+1} mod M has a fixed distribution. This is like
a "one-step mixing" property. The question is whether this single-step
mixing guarantees equidistribution of the entire orbit.

For a Markov chain with a unique stationary distribution and mixing,
this follows from the convergence theorem. The state-independence
actually makes our chain STRONGLY mixing: every transition matrix row
is the same, so the chain "forgets" its initial state after ONE step.

THIS IS THE KEY INSIGHT FOR THE DETERMINISTIC PROOF:
If the transition matrix is row-constant (all rows identical), then
for ANY initial distribution, the distribution after 1 step is the
stationary distribution. The orbit is not just asymptotically
equidistributed -- it IS equidistributed from step 1 onward!
"""
from collections import Counter, defaultdict
from math import log2


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def fmf_hop(x):
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
        else:
            t = v2(k + 1)
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
    else:
        return None
    p = v2(fmf)
    return fmf >> p


def fmf_hop_detailed(x):
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        case, t = 'A', 0
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            case, t = 'B', 0
        else:
            t = v2(k + 1)
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            case = 'B'
    else:
        return None, '', 0, 0
    p = v2(fmf)
    return fmf >> p, case, t, fmf


# === Part 1: Test equidistribution mod M along trajectories ===
print("=== Part 1: Equidistribution of F^n(x) mod M Along Trajectories ===\n")
print("If the transition matrix is row-constant, F^n(x) mod M should have")
print("the SAME distribution regardless of starting x, after step 1.\n")

M = 4
stat_dist = {1: 0.5, 3: 0.5}  # Stationary distribution mod 4

for x_start in [27, 31, 127, 703, 6171, 131071, 524287, 999999]:
    counts = Counter()
    x = x_start
    n_hops = 0
    for _ in range(500):
        if x <= 1:
            break
        x = fmf_hop(x)
        if x is None:
            break
        counts[x % M] += 1
        n_hops += 1

    if n_hops < 5:
        continue
    total = sum(counts.values())
    p1 = counts.get(1, 0) / total
    p3 = counts.get(3, 0) / total
    print(f"  x={x_start:>8}: {n_hops:>3} hops, "
          f"P(mod4=1)={p1:.4f} (expect 0.50), "
          f"P(mod4=3)={p3:.4f} (expect 0.50)")


# === Part 2: But wait -- the issue isn't mod M distribution ===
print("\n\n=== Part 2: The Real Issue -- Correlation of Ratios ===\n")
print("The transition matrix being row-constant means P(x_{n+1} mod M | x_n mod M)")
print("is independent of x_n. But E[R^alpha | x_n mod M] IS class-dependent.\n")
print("So we need: the TIME AVERAGE of R_i^alpha equals the SPACE AVERAGE.\n")

# For this, what matters is the JOINT distribution of (residue class, ratio)
# along the trajectory. Even if the marginal mod-M distribution is correct,
# the ratio distribution conditional on the class might not be.

# But here's the key: E[R^alpha | x ≡ r mod M, x in trajectory] should
# equal E[R^alpha | x ≡ r mod M, x arbitrary].
# This follows if: for a given residue class r, the SPECIFIC x values
# visited by the trajectory are "representative" of all x ≡ r mod M.

# The state-independence theorem says the OUTPUT distribution is the same.
# But the RATIO depends on the specific x, not just x mod M.

# HOWEVER: for large x, R ≈ 3^s / 2^d, where s and d are determined by
# the TYPE (A or B) and v_2(FMF). The type is determined by x mod 4.
# And v_2(FMF) has EXACT geometric distribution (Theorem 3+7).

# So for large x: R^alpha is essentially determined by (type, v_2), and
# v_2 has the exact same distribution regardless of the specific x.

# The "large x" approximation: R = (3^s * m_out) / (2^d * m_in)
# For large m_in and m_out: m_out/m_in ≈ 3^s/2^d, so R ≈ 3^s/2^d exactly.

# Let's verify: does the error term (R - 3^s/2^d) shrink with x?

print("Ratio vs asymptotic formula, for large x:\n")
for x_start in [1000001, 10000001, 100000001]:
    x = x_start | 1  # Make sure it's odd
    errors = []
    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        v = v2(fmf)
        actual_R = nxt / x
        if case == 'A':
            asymptotic_R = 3 / (4 * 2**max(0, v - 2))
        else:
            asymptotic_R = (3/2)**(t+2) / 2**v
        rel_error = abs(actual_R - asymptotic_R) / actual_R
        errors.append(rel_error)
        x = nxt

    if errors:
        avg_err = sum(errors) / len(errors)
        max_err = max(errors)
        print(f"  x_start ~ 10^{len(str(x_start))-1}: "
              f"avg relative error = {avg_err:.8f}, max = {max_err:.8f}")


# === Part 3: The Deterministic Proof Structure ===
print("\n\n=== Part 3: Deterministic Proof Structure ===\n")
print("""
THE PROOF (modulo one lemma):

Lemma (2-adic equidistribution along orbits):
  For any odd x_0 > 1, the sequence x_0, F(x_0), F^2(x_0), ... satisfies:
  For any M and any odd residue r (1 ≤ r < M, r odd):
    lim_{N->inf} (1/N) * #{0 ≤ n < N : x_n ≡ r mod M} = 1/(M/2)

In other words, the orbit is equidistributed mod M among odd residues.

IF this lemma holds, then by the strong law for dependent sequences:

  (1/N) * sum_{n=0}^{N-1} log(R_n^alpha) -> E[log(R^alpha)] = log(rho) < 0

where rho = 0.8638 < 1. This means:

  sum_{n=0}^{N-1} log(R_n^alpha) -> -infinity

  => log(x_N / x_0)^alpha -> -infinity  (since log(R_n^alpha) = alpha*log(x_{n+1}/x_n))

  => x_N -> 0

  => x_N = 1 for sufficiently large N.  QED.

WHY THE LEMMA SHOULD HOLD:

The FMF map on the 2-adic integers Z_2 is:
  F(x) = (3^(t+2) * m - 1) / 2^v  where x = 2^(t+2)*m - 1

This map preserves the Haar measure on Z_2 (up to a constant).
By Theorem 12, the output x_{n+1} mod M has a FIXED distribution
regardless of x_n. This means the chain on Z/MZ has spectral gap 1
(maximum possible mixing rate). The orbit equidistributes mod M
after a single step.

The subtlety: equidistribution mod M is about the RESIDUE of x_n,
but the ratio R_n depends on more than just x_n mod M. It depends
on the full value of x_n (through the higher-order bits).

Resolution: for large x_n, the ratio R_n ≈ 3^s / 2^d, where s and d
are determined by (type, v_2), which in turn depends only on
x_n mod 2^(t+3) or so. As x_n is large, the error is O(1/x_n).
Since sum O(1/x_n) converges (because x_n grows like the trajectory,
which has bounded peaks), the error in the average is negligible.
""")


# === Part 4: Verify the error bound ===
print("\n=== Part 4: Sum of Error Terms Along Trajectories ===\n")

for x_start in [27, 127, 703, 6171, 131071, 999999]:
    x = x_start
    alpha = 0.53
    sum_log_R_alpha = 0
    sum_log_asymp = 0
    error_sum = 0
    n_hops = 0

    for _ in range(500):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        v = v2(fmf)

        actual_R = nxt / x
        if case == 'A':
            asymptotic_R = 3 / (4 * 2**max(0, v - 2))
        else:
            asymptotic_R = (3/2)**(t+2) / 2**v

        sum_log_R_alpha += alpha * log2(actual_R)
        sum_log_asymp += alpha * log2(asymptotic_R)
        error_sum += abs(alpha * log2(actual_R) - alpha * log2(asymptotic_R))
        n_hops += 1
        x = nxt

    if n_hops > 0:
        avg_log = sum_log_R_alpha / n_hops
        print(f"  x={x_start:>8}: {n_hops:>3} hops, "
              f"avg log(R^alpha)={avg_log:>+.6f} (expect -0.44), "
              f"total error={error_sum:.6f}, error/hop={error_sum/n_hops:.6f}")


# === Part 5: The final piece -- does the orbit cover all residues? ===
print("\n\n=== Part 5: Orbit Residue Coverage ===\n")
print("For each trajectory, check if ALL odd residues mod M are visited.\n")

for M in [4, 8, 16, 32]:
    odd_residues = set(r for r in range(1, M, 2))
    n_expected = len(odd_residues)
    all_covered = 0
    total = 0

    for x_start in range(3, 100001, 2):
        x = x_start
        visited = set()
        for _ in range(200):
            if x <= 1:
                break
            visited.add(x % M)
            x = fmf_hop(x)
            if x is None:
                break

        visited_odd = visited & odd_residues
        if len(visited_odd) == n_expected:
            all_covered += 1
        total += 1

    pct = all_covered / total * 100
    print(f"  mod {M:>2}: {all_covered}/{total} trajectories cover all "
          f"{n_expected} odd residues ({pct:.1f}%)")


# === Part 6: The product of ratios ===
print("\n\n=== Part 6: Product of Ratios Along Trajectories ===\n")
print("x_n / x_0 = product of (x_{i+1}/x_i) for i=0..n-1")
print("If this product -> 0, then x_n -> 0, so x_n = 1.\n")

for x_start in [27, 127, 703, 6171, 131071, 999999, 2097151]:
    x = x_start
    product_log = 0
    max_product_log = 0

    for hop in range(500):
        if x <= 1:
            break
        nxt = fmf_hop(x)
        if nxt is None:
            break
        product_log += log2(nxt / x)
        max_product_log = max(max_product_log, product_log)
        x = nxt

    print(f"  x={x_start:>8}: final product log2 = {product_log:>+10.4f} "
          f"(= ratio {2**product_log:.6e}), "
          f"peak log2 = {max_product_log:>+8.4f}, "
          f"avg per hop = {product_log/hop:>+.4f}")
