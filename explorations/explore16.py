"""
explore16.py - Autocorrelation of FMF Increments

The key remaining gap: are successive log2-multipliers independent enough?

If we define X_i = log2(F^i(x) / F^{i-1}(x)), the Cramer bound requires
X_i to be i.i.d. or at least have fast-decaying autocorrelations.

We measure:
1. Autocorrelation: corr(X_i, X_{i+k}) for various lags k
2. Conditional expectations: E[X_{i+1} | X_i = large positive]
3. Whether "bad" hops (large X_i) tend to cluster

If autocorrelation decays exponentially, the random walk tools
apply rigorously via standard mixing-time arguments.
"""
from math import log2
from collections import defaultdict


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


def fmf_chain(x_start, max_hops=500):
    """Returns list of log2-multipliers along the FMF chain."""
    x = x_start
    mults = []
    for _ in range(max_hops):
        if x == 1:
            break
        nxt = fmf_hop(x)
        if nxt is None or nxt == 0:
            break
        mults.append(log2(nxt / x))
        x = nxt
    return mults


# === Part 1: Autocorrelation along individual chains ===
print("=== Part 1: Autocorrelation Along FMF Chains ===\n")

# Collect all consecutive increments from long chains
all_pairs = {k: [] for k in range(1, 11)}  # lag k -> list of (X_i, X_{i+k}) pairs

for x_start in range(3, 50001, 2):
    mults = fmf_chain(x_start)
    if len(mults) < 3:
        continue
    for lag in range(1, min(11, len(mults))):
        for i in range(len(mults) - lag):
            all_pairs[lag].append((mults[i], mults[i + lag]))

print(f"{'lag':>4} {'n_pairs':>10} {'corr':>10} {'interpretation'}")
print("-" * 60)

for lag in range(1, 11):
    pairs = all_pairs[lag]
    if not pairs:
        continue
    n = len(pairs)
    mean_x = sum(p[0] for p in pairs) / n
    mean_y = sum(p[1] for p in pairs) / n
    var_x = sum((p[0] - mean_x)**2 for p in pairs) / n
    var_y = sum((p[1] - mean_y)**2 for p in pairs) / n
    cov = sum((p[0] - mean_x) * (p[1] - mean_y) for p in pairs) / n
    corr = cov / (var_x * var_y)**0.5 if var_x > 0 and var_y > 0 else 0

    if abs(corr) < 0.01:
        interp = "~independent"
    elif abs(corr) < 0.05:
        interp = "very weak"
    elif abs(corr) < 0.1:
        interp = "weak"
    else:
        interp = f"notable ({'+' if corr > 0 else '-'})"

    print(f"{lag:>4} {n:>10} {corr:>+10.6f}  {interp}")


# === Part 2: Conditional distribution ===
# After a "bad" hop (X_i > 2), what happens next?
print("\n\n=== Part 2: E[X_{i+1} | X_i in bucket] ===\n")
print("Does a growing hop predict the next hop's behavior?\n")

buckets = {
    "X<-3": lambda x: x < -3,
    "-3<X<-1": lambda x: -3 <= x < -1,
    "-1<X<0": lambda x: -1 <= x < 0,
    "0<X<1": lambda x: 0 <= x < 1,
    "1<X<3": lambda x: 1 <= x < 3,
    "X>3": lambda x: x >= 3,
}

conditional = {name: [] for name in buckets}

for x_start in range(3, 50001, 2):
    mults = fmf_chain(x_start)
    for i in range(len(mults) - 1):
        for name, pred in buckets.items():
            if pred(mults[i]):
                conditional[name].append(mults[i + 1])
                break

print(f"{'X_i bucket':>12} {'count':>8} {'E[X_{i+1}]':>12} {'P(shrink)':>10}")
for name in buckets:
    vals = conditional[name]
    if vals:
        e = sum(vals) / len(vals)
        p_shrink = sum(1 for v in vals if v < 0) / len(vals)
        print(f"{name:>12} {len(vals):>8} {e:>+12.4f} {p_shrink:>10.4f}")


# === Part 3: Do "bad" hops cluster? ===
print("\n\n=== Part 3: Do Growing Hops Cluster? ===\n")
print("P(X_{i+1} > 0 | X_i > 0) vs P(X_{i+1} > 0) overall\n")

# Overall P(grow)
total_hops = 0
total_grow = 0
consecutive_grow_pairs = 0
grow_then_anything = 0

for x_start in range(3, 50001, 2):
    mults = fmf_chain(x_start)
    for i in range(len(mults)):
        total_hops += 1
        if mults[i] > 0:
            total_grow += 1
            if i < len(mults) - 1:
                grow_then_anything += 1
                if mults[i + 1] > 0:
                    consecutive_grow_pairs += 1

p_grow = total_grow / total_hops
p_grow_given_grow = consecutive_grow_pairs / grow_then_anything if grow_then_anything > 0 else 0

print(f"P(X > 0) overall:           {p_grow:.6f}")
print(f"P(X_{'{i+1}'} > 0 | X_i > 0):    {p_grow_given_grow:.6f}")
print(f"Ratio (should be ~1 if independent): {p_grow_given_grow / p_grow:.6f}")
print()

# Streak analysis
print("Longest growing streaks in chains:")
max_streaks = []
for x_start in range(3, 50001, 2):
    mults = fmf_chain(x_start)
    streak = 0
    max_streak = 0
    for m in mults:
        if m > 0:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    if max_streak >= 5:
        max_streaks.append((max_streak, x_start))

max_streaks.sort(reverse=True)
print(f"{'streak':>7} {'x_start':>10}")
for streak, x in max_streaks[:15]:
    print(f"{streak:>7} {x:>10}")


# === Part 4: Type sequence analysis ===
print("\n\n=== Part 4: Type Sequence Autocorrelation ===\n")
print("Encode each hop as: 0 = Type A, 1 = Type B(t=0), 2 = Type B(t=1), ...\n")

type_pairs = defaultdict(list)

for x_start in range(3, 50001, 2):
    x = x_start
    types = []
    for _ in range(500):
        if x == 1:
            break
        mod4 = x % 4
        if mod4 == 1:
            t_val = -1  # Type A
        else:
            k = (x - 3) // 4
            if k % 2 == 0:
                t_val = 0
            else:
                t_val = v2(k + 1)
        types.append(t_val)
        nxt = fmf_hop(x)
        if nxt is None:
            break
        x = nxt

    for i in range(len(types) - 1):
        type_pairs[types[i]].append(types[i + 1])

print(f"{'type_i':>8} {'count':>7} {'P(A next)':>10} {'P(B0)':>8} {'P(B1)':>8} {'P(B2+)':>8}")
for t_from in sorted(type_pairs):
    nexts = type_pairs[t_from]
    n = len(nexts)
    if n < 100:
        continue
    p_a = sum(1 for t in nexts if t == -1) / n
    p_b0 = sum(1 for t in nexts if t == 0) / n
    p_b1 = sum(1 for t in nexts if t == 1) / n
    p_b2p = sum(1 for t in nexts if t >= 2) / n
    label = "A" if t_from == -1 else f"B(t={t_from})"
    print(f"{label:>8} {n:>7} {p_a:>10.4f} {p_b0:>8.4f} {p_b1:>8.4f} {p_b2p:>8.4f}")


# === Part 5: Effective independence conclusion ===
print("\n\n=== Part 5: Conclusion on Independence ===\n")
print(f"""
SUMMARY OF CORRELATION ANALYSIS:

Lag-1 autocorrelation of log2-multipliers: [to be filled from Part 1]
Conditional E[X_{{i+1}} | X_i]: [to be filled from Part 2]
P(grow|grow) vs P(grow): ratio = [to be filled from Part 3]
Type transitions: [to be filled from Part 4]

If lag-1 correlation is < 0.05 and decays with lag, the chain
is effectively a random walk with weakly dependent increments.

For such walks, the Central Limit Theorem and Large Deviation
Principle still hold (with adjusted constants), and the Cramer
bound P(max >= H) <= exp(-c*H) remains valid.

MATHEMATICAL IMPLICATION:
If the autocorrelation at lag k is |rho_k| < C * r^k for some r < 1,
then the chain satisfies alpha-mixing with exponential rate, and
the drift argument goes through rigorously.
""")
