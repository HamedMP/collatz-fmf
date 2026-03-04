"""
explore20.py - Multi-Step Contraction: Does L(F^k(x)) < L(x) Always Hold?

The remaining gap: rho(T) < 1 proves AVERAGE contraction, but we need
POINTWISE: L(F(x)) < L(x) for all x > 1 (or at least L(F^k(x)) < L(x)
for some fixed k).

Since ~29% of single hops grow, L(F(x)) < L(x) fails for many x.
But the self-correction mechanism (Theorem 18) suggests that after
k=2 or k=3 hops, the product of ratios might always be < 1.

Question: For what k does max_x [L(F^k(x)) / L(x)] < 1?

If such k exists, Collatz is proved: every trajectory strictly decreases
in L after at most k hops, guaranteeing convergence.
"""
from collections import defaultdict
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


# === Part 1: k-hop worst-case ratio ===
print("=== Part 1: Worst-Case k-Hop Ratio ===\n")
print("For each k, compute max over all odd x in [3,N] of L(F^k(x))/L(x)")
print("where L(x) = x^alpha. If this max < 1 for some k, Collatz is proved.\n")

alpha = 0.53
N = 200000

for k in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]:
    worst_ratio = 0
    worst_x = 0
    total = 0
    above_one = 0

    for x in range(3, N + 1, 2):
        y = x
        valid = True
        for _ in range(k):
            if y <= 1:
                valid = False
                break
            y = fmf_hop(y)
            if y is None:
                valid = False
                break
        if not valid:
            continue

        total += 1
        ratio = (y / x) ** alpha
        if ratio > 1:
            above_one += 1
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_x = x

    pct_above = above_one / total * 100 if total > 0 else 0
    print(f"  k={k:>2}: worst ratio^alpha = {worst_ratio:.6f}, "
          f"at x={worst_x}, above 1: {pct_above:.2f}% of {total}")


# === Part 2: With weights w(x mod M) ===
print("\n\n=== Part 2: Weighted k-Hop Ratio L(F^k(x))/L(x) ===\n")
print("Using L(x) = x^alpha * w(x mod 8) with optimal weights from explore17.\n")

# Optimal weights from explore17 (M=8, alpha=0.5)
weights_8 = {1: 0.669, 3: 0.633, 5: 0.366, 7: 1.000}


def L(x, alpha=0.53):
    return x**alpha * weights_8[x % 8]


for k in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]:
    worst_ratio = 0
    worst_x = 0
    total = 0
    above_one = 0

    for x in range(3, N + 1, 2):
        y = x
        valid = True
        for _ in range(k):
            if y <= 1:
                valid = False
                break
            y = fmf_hop(y)
            if y is None:
                valid = False
                break
        if not valid:
            continue

        total += 1
        ratio = L(y) / L(x)
        if ratio > 1:
            above_one += 1
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_x = x

    pct_above = above_one / total * 100 if total > 0 else 0
    print(f"  k={k:>2}: worst L-ratio = {worst_ratio:.6f}, "
          f"at x={worst_x}, above 1: {pct_above:.2f}% of {total}")


# === Part 3: Analyze the worst cases ===
print("\n\n=== Part 3: Analyzing Worst-Case Trajectories ===\n")
print("What makes certain starting points resist contraction?\n")

# Find the 20 worst starting points for k=5
worst_cases = []
for x in range(3, N + 1, 2):
    y = x
    valid = True
    for _ in range(5):
        if y <= 1:
            valid = False
            break
        y = fmf_hop(y)
        if y is None:
            valid = False
            break
    if not valid:
        continue
    ratio = L(y) / L(x)
    worst_cases.append((ratio, x))

worst_cases.sort(reverse=True)
print(f"{'rank':>5} {'x':>8} {'L-ratio(5 hops)':>16} {'trajectory (mod 4 types)':>30}")
for i, (ratio, x) in enumerate(worst_cases[:20]):
    # Trace the trajectory
    y = x
    types = []
    for _ in range(5):
        if y <= 1:
            break
        mod4 = y % 4
        if mod4 == 1:
            types.append('A')
        else:
            k = (y - 3) // 4
            if k % 2 == 0:
                types.append('B0')
            else:
                t = v2(k + 1)
                types.append(f'B{t}')
        y = fmf_hop(y)
    traj_str = '->'.join(types)
    print(f"{i+1:>5} {x:>8} {ratio:>16.6f} {traj_str:>30}")


# === Part 4: Maximum consecutive growth hops ===
print("\n\n=== Part 4: Max Consecutive Growth Hops ===\n")

max_consec_growth = defaultdict(int)  # max consec growth -> count of starting x
total_chains = 0

for x in range(3, 500001, 2):
    y = x
    consec = 0
    max_c = 0
    for _ in range(200):
        if y <= 1:
            break
        y2 = fmf_hop(y)
        if y2 is None:
            break
        if y2 > y:
            consec += 1
            max_c = max(max_c, consec)
        else:
            consec = 0
        y = y2
    max_consec_growth[max_c] += 1
    total_chains += 1

print(f"{'max consecutive growth':>22} {'count':>8} {'fraction':>9}")
for mc in sorted(max_consec_growth):
    cnt = max_consec_growth[mc]
    frac = cnt / total_chains
    print(f"{mc:>22} {cnt:>8} {frac:>9.4f}")


# === Part 5: The k that guarantees contraction ===
print("\n\n=== Part 5: For Large x, Does k-Hop Contraction Hold? ===\n")
print("Testing in different magnitude ranges:\n")

for mag in [100, 1000, 10000, 100000, 1000000]:
    lo = mag
    hi = min(mag * 10, 10000000)
    for k in [3, 5, 10, 20]:
        worst = 0
        worst_x = 0
        count = 0
        for x in range(lo | 1, hi + 1, 2):
            if count >= 50000:
                break
            y = x
            valid = True
            for _ in range(k):
                if y <= 1:
                    valid = False
                    break
                y = fmf_hop(y)
                if y is None:
                    valid = False
                    break
            if not valid:
                continue
            count += 1
            r = L(y) / L(x)
            if r > worst:
                worst = r
                worst_x = x

        status = "< 1 YES" if worst < 1 else "> 1 NO"
        print(f"  [{lo:>8}, {hi:>8}] k={k:>2}: worst L-ratio = {worst:.6f} ({status}) at x={worst_x}")
    print()
