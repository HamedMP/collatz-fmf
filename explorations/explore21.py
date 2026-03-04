"""
explore21.py - Pointwise Lyapunov Bound: Bounding Growth Per Residue Class

The question: for each residue class r mod M, what is the WORST-CASE
single-hop ratio L(F(x))/L(x)?

If we can show:
  max_{r mod M} max_{x ≡ r mod M} L(F(x))/L(x) = C < infinity

then after at most ceil(log(C) / log(1/rho)) hops of "average" contraction,
any growth is recovered. This gives a deterministic bound on how many
hops before L decreases.

Even better: if we can compute, for each r mod M, the probability that
L(F(x))/L(x) > 1, and show that after k hops the PRODUCT of worst-case
and average contraction is < 1, we have a pointwise multi-step bound.
"""
from collections import defaultdict
from math import log2, log


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


weights_8 = {1: 0.669, 3: 0.633, 5: 0.366, 7: 1.000}
ALPHA = 0.53


def L(x):
    return x**ALPHA * weights_8[x % 8]


# === Part 1: Single-hop ratio distribution by residue class ===
print("=== Part 1: Single-Hop L-Ratio by Residue Class (mod 8) ===\n")

N = 500000
ratio_by_class = defaultdict(list)

for x in range(3, N + 1, 2):
    nxt = fmf_hop(x)
    if nxt is None or nxt <= 0:
        continue
    r = x % 8
    ratio = L(nxt) / L(x)
    ratio_by_class[r].append(ratio)

print(f"{'r mod 8':>8} {'count':>8} {'mean ratio':>11} {'max ratio':>11} "
      f"{'P(>1)':>7} {'P(>1.5)':>8} {'P(>2)':>7}")
for r in sorted(ratio_by_class):
    vals = ratio_by_class[r]
    mean = sum(vals) / len(vals)
    mx = max(vals)
    p1 = sum(1 for v in vals if v > 1) / len(vals)
    p15 = sum(1 for v in vals if v > 1.5) / len(vals)
    p2 = sum(1 for v in vals if v > 2) / len(vals)
    print(f"{r:>8} {len(vals):>8} {mean:>11.6f} {mx:>11.6f} "
          f"{p1:>7.4f} {p15:>8.4f} {p2:>7.4f}")


# === Part 2: What's the theoretical max ratio? ===
print("\n\n=== Part 2: Theoretical Maximum Single-Hop Ratio ===\n")

# For Type A (x = 4k+1):
#   F(x) = (3k+1) / 2^v where v = v_2(3k+1)
#   Worst case: v_2(3k+1) = 0, so F(x) = 3k+1 ≈ 3x/4
#   Ratio = (3/4)^alpha * w(F(x) mod 8) / w(x mod 8)
#   Max over weights: w(7)/w(5) = 1.0/0.366 = 2.732
#   So worst A ratio ≈ (3/4)^0.53 * 2.732 = 0.863 * 2.732 = 2.36
# But this doesn't account for LPT division... let's check empirically.

print("Type A worst cases (x ≡ 1 mod 4):")
worst_a = []
for x in range(5, N + 1, 4):
    nxt = fmf_hop(x)
    if nxt and nxt > 0:
        ratio = L(nxt) / L(x)
        if ratio > 1.5:
            worst_a.append((ratio, x, nxt))
worst_a.sort(reverse=True)
for ratio, x, nxt in worst_a[:10]:
    print(f"  x={x:>8} (mod8={x%8}), F(x)={nxt:>8} (mod8={nxt%8}), "
          f"L-ratio={ratio:.6f}, raw ratio={nxt/x:.4f}")

print("\nType B worst cases (x ≡ 3 mod 4):")
worst_b = []
for x in range(3, N + 1, 4):
    nxt = fmf_hop(x)
    if nxt and nxt > 0:
        ratio = L(nxt) / L(x)
        if ratio > 2.0:
            worst_b.append((ratio, x, nxt))
worst_b.sort(reverse=True)
for ratio, x, nxt in worst_b[:10]:
    _, case, t, fmf = fmf_hop_detailed(x)
    v = v2(fmf)
    print(f"  x={x:>8} (mod8={x%8}), F(x)={nxt:>8} (mod8={nxt%8}), "
          f"L-ratio={ratio:.6f}, t={t}, v2={v}, raw={nxt/x:.4f}")


# === Part 3: Does the max ratio converge? ===
print("\n\n=== Part 3: Max Ratio vs Number Magnitude ===\n")
print("Does the worst-case ratio stabilize or grow with x?\n")

for bits in range(4, 22):
    lo = 2**(bits-1)
    hi = 2**bits
    worst = 0
    worst_x = 0
    count = 0
    for x in range(lo | 1, hi + 1, 2):
        nxt = fmf_hop(x)
        if nxt and nxt > 0:
            r = L(nxt) / L(x)
            count += 1
            if r > worst:
                worst = r
                worst_x = x
    print(f"  {bits:>2}-bit: max L-ratio = {worst:.6f} at x={worst_x}")


# === Part 4: What TYPE of numbers produce the worst ratios? ===
print("\n\n=== Part 4: Anatomy of Worst-Case Single Hops ===\n")

# The worst case is when:
# 1. x has a high-t value (lots of 3x+1 iterations before hitting /4)
# 2. v_2(FMF) is small (so the LPT division is minimal)
# 3. The weight ratio w(F(x) mod 8) / w(x mod 8) is large

# For Type B with high t and small v_2:
#   F(x)/x ≈ (3/2)^(t+2) / 2^v
#   Worst: v=1 (minimum), so F(x)/x ≈ (3/2)^(t+2) / 2
#   For t=10: (3/2)^12 / 2 ≈ 129.7 / 2 ≈ 64.9

# But how often does v=1 occur? P(v=1) = 1/2 (geometric distribution)
# So half of all Type B hops with t=10 would grow by ~65x!

# The KEY: these happen with probability 1/2^(t+2) = 1/4096 for t=10.
# And when they DO happen, the self-correction (Theorem 18) kicks in:
# the next hop is Type A with high probability (91% for t=11).

print("Single-hop growth by (t, v_2) combination:")
tv_stats = defaultdict(list)
for x in range(3, N + 1, 2):
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None or nxt <= 0:
        continue
    v = v2(fmf)
    if case == 'B' and t >= 1:
        ratio = nxt / x
        tv_stats[(t, v)].append(ratio)

print(f"{'(t, v2)':>10} {'count':>7} {'mean ratio':>12} {'max ratio':>12} {'growth?':>8}")
for key in sorted(tv_stats):
    t, v = key
    vals = tv_stats[key]
    if len(vals) < 5:
        continue
    mean = sum(vals) / len(vals)
    mx = max(vals)
    grows = "YES" if mean > 1 else "no"
    if t <= 6:
        print(f"  ({t:>1}, {v:>2}) {len(vals):>7} {mean:>12.4f} {mx:>12.4f} {grows:>8}")


# === Part 5: Two-hop guarantee ===
print("\n\n=== Part 5: Two-Hop Guarantee Analysis ===\n")
print("After a growth hop (F(x) > x), does the NEXT hop always compensate?\n")

growth_then_total = []
for x in range(3, N + 1, 2):
    nxt = fmf_hop(x)
    if nxt is None or nxt <= 1:
        continue
    if nxt <= x:
        continue
    # This was a growth hop. Check the next hop.
    nxt2 = fmf_hop(nxt)
    if nxt2 is None or nxt2 <= 0:
        continue

    two_hop_ratio = L(nxt2) / L(x)
    growth_then_total.append((two_hop_ratio, x, nxt, nxt2))

growth_then_total.sort(reverse=True)
above_one = sum(1 for r, _, _, _ in growth_then_total if r > 1)
print(f"Growth hops: {len(growth_then_total)}")
print(f"Two-hop ratio > 1 after growth: {above_one} ({above_one/len(growth_then_total)*100:.2f}%)")
print(f"Max two-hop ratio: {growth_then_total[0][0]:.6f}")
print(f"\nWorst two-hop-after-growth cases:")
for ratio, x, n1, n2 in growth_then_total[:15]:
    _, c1, t1, _ = fmf_hop_detailed(x)
    _, c2, t2, _ = fmf_hop_detailed(n1)
    print(f"  x={x:>8} -> {n1:>8} -> {n2:>8}  "
          f"L-ratio={ratio:.6f}  types: {c1}(t={t1})->{c2}(t={t2})")


# === Part 6: Bounded growth streaks ===
print("\n\n=== Part 6: Maximum Growth in L Before Guaranteed Decrease ===\n")

# For each x, compute the maximum L(F^j(x)) / L(x) before L drops below L(x)
max_peak_L = []
for x in range(3, min(N + 1, 200001), 2):
    y = x
    peak = 1.0
    steps_to_below = None
    for j in range(1, 100):
        if y <= 1:
            break
        y = fmf_hop(y)
        if y is None:
            break
        r = L(y) / L(x)
        peak = max(peak, r)
        if r < 1.0 and steps_to_below is None:
            steps_to_below = j
            break

    if steps_to_below is not None:
        max_peak_L.append((peak, steps_to_below, x))

if max_peak_L:
    max_peak_L.sort(reverse=True)
    print(f"Among {len(max_peak_L)} numbers that eventually L-descend:")
    print(f"  Max peak L-ratio before descent: {max_peak_L[0][0]:.6f} (x={max_peak_L[0][2]})")
    print(f"  Max hops to L-descent: {max(s for _, s, _ in max_peak_L)}")
    print(f"\nTop 15 hardest L-descent cases:")
    for peak, steps, x in max_peak_L[:15]:
        print(f"  x={x:>8}: peak L-ratio = {peak:.4f}, descends at hop {steps}")

    # Distribution of steps-to-L-descent
    print(f"\nSteps to L-descent distribution:")
    step_counts = defaultdict(int)
    for _, s, _ in max_peak_L:
        step_counts[s] += 1
    for s in sorted(step_counts):
        cnt = step_counts[s]
        pct = cnt / len(max_peak_L) * 100
        if s <= 20 or cnt > 10:
            print(f"  {s:>3} hops: {cnt:>6} ({pct:.1f}%)")
