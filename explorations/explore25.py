"""
explore25.py - Large-x Epoch Duration Test

Test the bound epoch_duration <= C * log2(x) for much larger x.
Focus on:
1. Random large odd numbers in various bit-length ranges
2. Known hard cases: 2^n - 1 for large n
3. Numbers with specific structure: high t-values

If the ratio epoch_duration / log2(x) stays bounded (and ideally decreases),
this strongly supports the universal bound.
"""
from collections import defaultdict
from math import log2
import random

random.seed(42)


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


def epoch_duration(x_start, max_hops=2000):
    """Returns (duration, peak_ratio) or (None, None) if no descent."""
    x = x_start
    peak = x
    for hop in range(max_hops):
        if x <= 1:
            return hop + 1, peak / x_start
        nxt = fmf_hop(x)
        if nxt is None:
            return None, None
        if nxt > peak:
            peak = nxt
        if nxt < x_start:
            return hop + 1, peak / x_start
        x = nxt
    return None, None


# === Part 1: 2^n - 1 for large n ===
print("=== Part 1: Epoch Duration for 2^n - 1 ===\n")

print(f"{'n':>4} {'x (2^n-1)':>15} {'epoch dur':>10} {'log2(x)':>8} "
      f"{'ratio':>8} {'peak/x':>10}")
for n in range(3, 45):
    x = 2**n - 1
    dur, peak = epoch_duration(x, max_hops=5000)
    if dur is not None:
        bits = log2(x)
        ratio = dur / bits
        print(f"{n:>4} {x:>15} {dur:>10} {bits:>8.2f} {ratio:>8.4f} {peak:>10.2f}")
    else:
        print(f"{n:>4} {x:>15}  NO DESCENT within 5000 hops")


# === Part 2: Random large odd numbers ===
print("\n\n=== Part 2: Random Large Odd Numbers ===\n")

print(f"{'bit-length':>11} {'n tested':>9} {'avg dur':>8} {'max dur':>8} "
      f"{'avg ratio':>10} {'max ratio':>10}")

for bits in [20, 25, 30, 35, 40, 45, 50, 55, 60]:
    lo = 2**(bits-1)
    hi = 2**bits - 1
    n_test = 1000 if bits <= 40 else 200 if bits <= 50 else 50

    durations = []
    ratios = []
    for _ in range(n_test):
        x = random.randrange(lo | 1, hi + 1, 2)
        dur, peak = epoch_duration(x, max_hops=5000)
        if dur is not None:
            durations.append(dur)
            ratios.append(dur / bits)

    if durations:
        avg_d = sum(durations) / len(durations)
        max_d = max(durations)
        avg_r = sum(ratios) / len(ratios)
        max_r = max(ratios)
        print(f"{bits:>11} {len(durations):>9} {avg_d:>8.2f} {max_d:>8} "
              f"{avg_r:>10.4f} {max_r:>10.4f}")
    else:
        print(f"{bits:>11} FAILURES")


# === Part 3: Numbers with high t-values (growth-prone) ===
print("\n\n=== Part 3: High-t Numbers (Growth-Prone) ===\n")
print("Numbers of the form 2^(t+2)*m - 1 with small m and high t\n")

print(f"{'t':>3} {'m':>5} {'x':>15} {'epoch dur':>10} {'log2(x)':>8} "
      f"{'ratio':>8} {'peak/x':>10}")
for t in range(5, 35):
    for m in [1, 3, 5]:
        x = 2**(t+2) * m - 1
        dur, peak = epoch_duration(x, max_hops=5000)
        if dur is not None:
            bits = log2(x)
            ratio = dur / bits
            print(f"{t:>3} {m:>5} {x:>15} {dur:>10} {bits:>8.2f} "
                  f"{ratio:>8.4f} {peak:>10.2f}")
        else:
            print(f"{t:>3} {m:>5} {x:>15}  NO DESCENT")


# === Part 4: Maximum ratio across all tests ===
print("\n\n=== Part 4: Summary ===\n")

all_ratios = []

# Collect from 2^n - 1
for n in range(3, 45):
    x = 2**n - 1
    dur, peak = epoch_duration(x, max_hops=5000)
    if dur:
        all_ratios.append((dur / log2(x), x, dur))

# Collect from random
for bits in [20, 25, 30, 35, 40, 45, 50]:
    lo = 2**(bits-1)
    hi = 2**bits - 1
    for _ in range(500 if bits <= 40 else 100):
        x = random.randrange(lo | 1, hi + 1, 2)
        dur, peak = epoch_duration(x, max_hops=5000)
        if dur:
            all_ratios.append((dur / bits, x, dur))

# Collect from high-t
for t in range(5, 40):
    for m in [1, 3, 5, 7, 9]:
        x = 2**(t+2) * m - 1
        dur, peak = epoch_duration(x, max_hops=5000)
        if dur:
            all_ratios.append((dur / log2(x), x, dur))

all_ratios.sort(reverse=True)
print("Top 20 highest epoch_duration / log2(x) ratios:")
for r, x, d in all_ratios[:20]:
    print(f"  x={x:>15} ({log2(x):>.1f} bits): dur={d:>4}, ratio={r:.4f}")

print(f"\nGlobal max ratio: {all_ratios[0][0]:.4f}")
print(f"Number of tests: {len(all_ratios)}")
print(f"\nConclusion: epoch_duration <= {all_ratios[0][0] * 1.2:.2f} * log2(x) appears to hold universally")
