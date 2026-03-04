"""
explore15.py - Supermartingale Construction: f(x) = x^alpha

The key remaining gap: prove E[f(F(x))] < f(x) for some function f.
If f(x) = x^alpha, this requires E[(F(x)/x)^alpha] < 1.

From explore14, the MGF M(theta) = E[exp(theta * log2(F(x)/x))]
equals 1 at theta* = 0.6986.

Now: exp(theta * log2(r)) = r^(theta/ln(2)) = r^(theta * log2(e))
Hmm, actually: E[exp(theta * log2(F/x))] = E[(F/x)^(theta/ln2)]

Wait, let's be more careful.
Let R = F(x)/x. We want E[R^alpha] < 1.
log2(R) has mean -0.83.
E[exp(theta * log2(R))] = E[2^(theta * log2(R))] = E[R^theta] (if we use natural log)

No: E[exp(theta * log2(R))] = E[exp(theta * ln(R)/ln(2))]

Let's just directly compute E[(F(x)/x)^alpha] for various alpha.

If E[(F(x)/x)^alpha] < 1, then f(x) = x^alpha is a supermartingale under F,
which proves:
1. F^n(x) -> 0 a.s. (and since F maps to positive integers, this means F^n(x) = 1 eventually)
2. E[f(F^n(x))] <= f(x), so the trajectory is bounded in f-expectation

This would be a COMPLETE proof of convergence (no need for i.i.d. assumption).
"""
from math import log, log2


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


# === Part 1: Direct computation of E[(F(x)/x)^alpha] ===
print("=== Part 1: E[(F(x)/x)^alpha] for various alpha ===\n")
print("If E[R^alpha] < 1, then f(x) = x^alpha is a supermartingale.\n")

# Compute for range of x values
N = 100000
ratios = []
for x in range(3, 2*N+1, 2):
    nxt = fmf_hop(x)
    if nxt and nxt > 0:
        ratios.append(nxt / x)

print(f"Sample size: {len(ratios)} odd numbers from [3, {2*N}]\n")
print(f"{'alpha':>8} {'E[R^alpha]':>12} {'< 1?':>6} {'ln(E[R^alpha])':>16}")
print("-" * 50)

results = {}
for alpha_10 in range(1, 30):
    alpha = alpha_10 / 10.0
    er = sum(r**alpha for r in ratios) / len(ratios)
    lt1 = "YES" if er < 1 else "no"
    results[alpha] = er
    print(f"{alpha:>8.1f} {er:>12.6f} {lt1:>6} {log(er):>16.6f}")


# === Part 2: Find the critical alpha ===
print("\n\n=== Part 2: Critical alpha where E[R^alpha] = 1 ===\n")
# Binary search
lo, hi = 0.0, 3.0
for _ in range(50):
    mid = (lo + hi) / 2
    er = sum(r**mid for r in ratios) / len(ratios)
    if er < 1:
        lo = mid
    else:
        hi = mid

alpha_star = (lo + hi) / 2
print(f"alpha* = {alpha_star:.10f}")
print(f"E[R^alpha*] = {sum(r**alpha_star for r in ratios) / len(ratios):.10f}")
print(f"\nFor alpha < alpha*, E[R^alpha] < 1 -> f(x) = x^alpha is a supermartingale.")
print(f"For alpha > alpha*, E[R^alpha] > 1 -> not a supermartingale.\n")


# === Part 3: Does the supermartingale property hold CONDITIONALLY? ===
# The real question: is E[F(x)^alpha | x] < x^alpha for ALL x, not just on average?
print("=== Part 3: Conditional supermartingale: E[F(x)^alpha | x] vs x^alpha ===\n")

alpha_test = 0.5  # A safe value below alpha*
print(f"Testing alpha = {alpha_test}. Need E[F(x)^alpha | x] < x^alpha for ALL x.\n")

# But wait: F is deterministic! F(x) is a single value, not a random variable.
# The "expectation" interpretation: over a RANGE of x values with similar magnitude,
# is the average of F(x)^alpha / x^alpha < 1?

# Actually, the correct interpretation for a supermartingale:
# Since F(x) is deterministic, we need F(x)^alpha < x^alpha for all x,
# i.e., F(x) < x for all x. But that's FALSE -- many hops increase x.

# The supermartingale must work differently. Perhaps:
# Define S_n = F^n(x). We need {S_n^alpha} to be a supermartingale w.r.t.
# the "natural filtration" of the FMF chain.
# But since the chain is deterministic, there's no randomness!

# The KEY REALIZATION: The supermartingale argument works when we consider
# x as random (uniformly distributed among odd numbers of a given magnitude).
# Then F(x)^alpha is a random variable, and E[F(x)^alpha] < E[x^alpha]
# means the process CONTRACTS on average.

# But for a PROOF of Collatz, we need it for EACH individual x.
# Since each F(x) is deterministic, we need a different approach.

print("IMPORTANT REALIZATION:")
print("F(x) is deterministic, so F(x)^alpha < x^alpha iff F(x) < x.")
print("But F(x) > x for ~29% of x values (the growing hops).")
print()
print("So f(x) = x^alpha is NOT a pointwise supermartingale!")
print("Instead, the drift argument works STATISTICALLY over the chain.")
print()
print("The correct approach: show that along ANY FMF chain,")
print("the product R_1 * R_2 * ... * R_n -> 0, i.e., sum log(R_i) -> -inf.")
print("This requires showing the ERGODIC AVERAGE of log(R) is negative.")
print()

# === Part 4: The ergodic approach ===
# Along a specific chain x_0 -> x_1 -> ... -> x_n = 1:
# sum log2(R_i) = log2(1/x_0) < 0 (always, since we reach 1)
# But we need to show this TERMINATES, which is circular.

# INSTEAD: Show that for a "typical" odd number of size ~X,
# E[R^alpha] < 1, uniformly in X.
# Combined with the Borel-Cantelli lemma: if P(F(x) > x) has
# exponential tail, then the chain can't grow unboundedly.

print("\n=== Part 4: E[R^alpha] by magnitude class ===\n")
alpha = 0.5
print(f"Alpha = {alpha}. E[R^alpha] should be < 1 uniformly across magnitudes.\n")
print(f"{'bits':>6} {'count':>7} {'E[R^alpha]':>12} {'E[log2(R)]':>12}")

by_bits = {}
for x in range(3, 200001, 2):
    nxt = fmf_hop(x)
    if nxt and nxt > 0:
        bl = x.bit_length()
        if bl not in by_bits:
            by_bits[bl] = []
        by_bits[bl].append(nxt / x)

for bl in sorted(by_bits):
    rs = by_bits[bl]
    if len(rs) >= 50:
        er = sum(r**alpha for r in rs) / len(rs)
        el = sum(log2(r) for r in rs) / len(rs)
        print(f"  {bl:>4} {len(rs):>7} {er:>12.6f} {el:>+12.4f}")


# === Part 5: The REAL path forward: prove mixing ===
print("\n\n=== Part 5: Why Mixing is the Key ===\n")
print("""
The supermartingale approach FAILS because F is deterministic.
The Cramer bound WORKS if the increments log2(R_i) are i.i.d. or "mixing."

The FMF chain is NOT random -- but it BEHAVES like a random walk because:
1. Transition probabilities are state-independent (Theorem 12)
2. Drift is magnitude-independent (Theorem 14)
3. The 2-adic structure makes successive m-values "pseudo-random"

The mathematical formalization:
- The FMF map acts on the 2-adic integers Z_2
- The map is "ergodic" in the sense that orbits equidistribute
- This is similar to how x -> 3x+1 mod 2^k is studied in the 2-adic setting

The precise gap: proving that the 2-adic map is sufficiently ergodic
that the empirical distribution of log2(R) along any orbit converges
to the global distribution.

This is related to the NORMALITY of 3-adic expansions in base 2,
which is itself an open problem in number theory.
""")


# === Part 6: Alternative approach -- weighted average ===
# Instead of x^alpha, try a different Lyapunov function
# that accounts for the mod-4 structure.
print("=== Part 6: Alternative Lyapunov function ===\n")
print("Try L(x) = x^alpha * w(x mod 8) where w is a weight function.\n")

# The idea: Type A and Type B have different expected multipliers.
# If we weight them differently, we might get a uniform contraction.
# E[L(F(x))] / L(x) = E[(F(x)/x)^alpha * w(F(x) mod 8) / w(x mod 8)]

# For this to work for ALL x, we need:
# For each residue class r mod 8:
# E[(F(x)/x)^alpha * w(F(x) mod 8)] / w(r) < 1

# Let's compute the transition weights empirically
from collections import defaultdict

alpha = 0.5
mod8_transitions = defaultdict(lambda: defaultdict(list))

for x in range(3, 200001, 2):
    nxt = fmf_hop(x)
    if nxt and nxt > 0:
        r_from = x % 8
        r_to = nxt % 8
        ratio = nxt / x
        mod8_transitions[r_from][r_to].append(ratio**alpha)

print(f"Transition matrix of E[R^alpha] by mod-8 class:")
print(f"{'from\\to':>8}", end="")
all_mods = sorted(set(r for d in mod8_transitions.values() for r in d))
for m in all_mods:
    print(f" {m:>8}", end="")
print()

for r_from in sorted(mod8_transitions):
    print(f"{r_from:>8}", end="")
    for r_to in all_mods:
        vals = mod8_transitions[r_from].get(r_to, [])
        if vals:
            print(f" {sum(vals)/len(vals):>8.4f}", end="")
        else:
            print(f" {'--':>8}", end="")
    total_from = sum(len(v) for v in mod8_transitions[r_from].values())
    weighted = sum(sum(v) for v in mod8_transitions[r_from].values()) / total_from
    print(f"  | avg: {weighted:.4f}")
