"""
explore17.py - Weighted Lyapunov Function L(x) = x^alpha * w(x mod M)

The key insight from explore15: f(x) = x^alpha alone can't be a pointwise
supermartingale because some residue classes (x ≡ 7 mod 8) have average
ratio > 1, while others (x ≡ 5 mod 8) have average ratio < 1.

Idea: define L(x) = x^alpha * w(x mod M) where w is a weight function
chosen so that L(F(x)) < L(x) for ALL odd x > 1.

For this to work:
  L(F(x)) / L(x) = (F(x)/x)^alpha * w(F(x) mod M) / w(x mod M) < 1

This is a FINITE system of inequalities (one per residue class of x mod M
and per possible output class of F(x) mod M).

If we can find alpha and w such that this holds for all classes,
we've proven Collatz!

Let's try M = 4, 8, 16, 32, ...
"""
from collections import defaultdict
from math import log, log2
import sys


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


# === Part 1: Transition structure by mod M ===
# For each x mod M, compute the distribution of (F(x) mod M, F(x)/x)

def analyze_mod(M, N=200000, alpha=0.5):
    """For each residue r mod M (odd r only), compute:
    - Distribution of F(x) mod M
    - Average (F(x)/x)^alpha * (1 for each output class)
    """
    # trans[r_from][r_to] = list of (F(x)/x)^alpha values
    trans = defaultdict(lambda: defaultdict(list))
    counts = defaultdict(int)

    for x in range(3, N + 1, 2):
        r = x % M
        nxt = fmf_hop(x)
        if nxt and nxt > 0:
            r_out = nxt % M
            ratio = (nxt / x) ** alpha
            trans[r][r_out].append(ratio)
            counts[r] += 1

    return trans, counts


# === Part 2: Can we find weights that make ALL transitions contract? ===
# We need: for each r_from, sum over r_to of:
#   P(F(x) mod M = r_to | x mod M = r_from) * E[(F(x)/x)^alpha | both] * w(r_to) / w(r_from)
# to be < 1.
#
# In matrix form: let T be the matrix where
#   T[r_from, r_to] = P * E[R^alpha | from->to]
# We need: (T * diag(w)) * (1/w) < 1 componentwise
# i.e., sum_j T[i,j] * w[j] / w[i] < 1 for all i
# i.e., sum_j T[i,j] * w[j] < w[i]
# i.e., T * w < w (componentwise)
#
# This is equivalent to: the spectral radius rho(T) < 1.
# If rho(T) < 1, then we can find w > 0 with T*w < w (the Perron eigenvector).

def compute_transition_matrix(M, N=200000, alpha=0.5):
    trans, counts = analyze_mod(M, N, alpha)
    odd_residues = sorted(r for r in range(1, M, 2))

    # Build matrix T[i][j] = sum of R^alpha values from i to j / count(i)
    T = {}
    for r_from in odd_residues:
        T[r_from] = {}
        total = counts[r_from]
        if total == 0:
            continue
        for r_to in odd_residues:
            vals = trans[r_from].get(r_to, [])
            T[r_from][r_to] = sum(vals) / total if total > 0 else 0

    return T, odd_residues


def power_iteration(T, residues, num_iter=100):
    """Compute spectral radius and dominant eigenvector via power iteration."""
    n = len(residues)
    # Start with uniform vector
    v = {r: 1.0 for r in residues}

    for _ in range(num_iter):
        # Multiply: v_new = T * v
        v_new = {}
        for r in residues:
            v_new[r] = sum(T.get(r, {}).get(s, 0) * v[s] for s in residues)

        # Normalize
        norm = max(abs(v_new[r]) for r in residues)
        if norm > 0:
            for r in residues:
                v_new[r] /= norm

        eigenvalue = norm
        v = v_new

    return eigenvalue, v


print("=== Weighted Lyapunov Function Analysis ===\n")
print("For L(x) = x^alpha * w(x mod M), need spectral radius rho(T) < 1.")
print("T[i,j] = P(F(x)≡j | x≡i) * E[(F(x)/x)^alpha | x≡i, F(x)≡j]\n")

for M in [4, 8, 16, 32]:
    print(f"\n{'='*60}")
    print(f"M = {M}")
    print(f"{'='*60}")

    for alpha_10 in [3, 5, 7, 9, 10, 11, 12]:
        alpha = alpha_10 / 10.0
        T, residues = compute_transition_matrix(M, N=200000, alpha=alpha)

        # Compute spectral radius
        rho, eigvec = power_iteration(T, residues)

        marker = " *** CONTRACTION ***" if rho < 1 else ""
        print(f"  alpha={alpha:.1f}: rho(T) = {rho:.6f}{marker}")

        if alpha == 0.5 and M <= 16:
            print(f"    Eigenvector (optimal weights):")
            for r in residues:
                print(f"      w({r} mod {M}) = {eigvec[r]:.6f}")


# === Part 3: Search for the optimal alpha for each M ===
print("\n\n=== Part 3: Optimal Alpha Search ===\n")

for M in [4, 8, 16, 32, 64]:
    print(f"\nM = {M}:")
    # Binary search for best alpha
    best_rho = float('inf')
    best_alpha = 0

    for alpha_100 in range(10, 120, 2):
        alpha = alpha_100 / 100.0
        T, residues = compute_transition_matrix(M, N=100000, alpha=alpha)
        rho, _ = power_iteration(T, residues)
        if rho < best_rho:
            best_rho = rho
            best_alpha = alpha

    # Refine around best
    for alpha_100 in range(int(best_alpha*100) - 10, int(best_alpha*100) + 10):
        alpha = alpha_100 / 100.0
        if alpha <= 0:
            continue
        T, residues = compute_transition_matrix(M, N=100000, alpha=alpha)
        rho, eigvec = power_iteration(T, residues)
        if rho < best_rho:
            best_rho = rho
            best_alpha = alpha

    print(f"  Best alpha = {best_alpha:.2f}, rho = {best_rho:.6f}", end="")
    if best_rho < 1:
        print(" *** THIS PROVES COLLATZ (for numbers up to N) ***")
    else:
        print(f"  (gap from 1: {best_rho - 1:+.6f})")


# === Part 4: The fundamental limitation ===
print("\n\n=== Part 4: Why This Approach Has Limits ===\n")
print("""
The spectral radius rho(T) is computed from a FINITE sample of numbers.
Even if rho < 1 for x in [3, N], this doesn't prove it for ALL x.

However, by Theorem 12, the transition probabilities are determined by
the 2-adic structure, which is independent of magnitude. So if the
transition matrix converges as N -> infinity, the spectral radius
also converges, and rho < 1 would hold universally.

The question: does the transition matrix T(M, alpha) converge as N -> inf?
""")

# Check convergence by computing T for different N values
print("Convergence check: rho vs N for M=8, alpha=0.5:")
for N in [10000, 50000, 100000, 200000, 500000]:
    T, residues = compute_transition_matrix(8, N=N, alpha=0.5)
    rho, _ = power_iteration(T, residues)
    print(f"  N={N:>7}: rho = {rho:.8f}")
