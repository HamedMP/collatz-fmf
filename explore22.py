"""
explore22.py - Growth Phase Structure: Duration, Magnitude, and t-Value Decay

The key remaining gap: growth phases (consecutive hops where F(x) > x or
L(F(x)) > L(x)) ALWAYS terminate empirically, but we need to prove this.

Hypothesis: during a growth phase, the t-value of the current number
DECREASES on average. Since growth requires high t AND low v_2, and
Theorem 18 shows high-t outputs bias toward Type A (which always shrinks),
growth phases are self-terminating.

If we can show:
  (1) Growth phases have bounded duration (proportional to initial t)
  (2) Total growth during a phase is bounded by some function of initial t
  (3) The average contraction between phases compensates for growth

Then Collatz follows from:
  - Growth phases are rare (probability ~ 1/2^t for a t-growth phase)
  - Growth phases are short (duration ~ t)
  - Average contraction (rho = 0.8638) overwhelms the rare growth
"""
from collections import defaultdict, Counter
from math import log2


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


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


# === Part 1: Growth phase identification and analysis ===
print("=== Part 1: Growth Phase Statistics ===\n")

N = 300000
phase_stats = []  # (start_x, duration, total_growth_log2, initial_t, t_sequence)

for x_start in range(3, N + 1, 2):
    x = x_start
    in_growth = False
    phase_start = None
    growth_log = 0
    duration = 0
    t_seq = []
    initial_t = 0

    for hop in range(200):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break

        log_r = log2(nxt / x)

        if log_r > 0:  # Growth hop
            if not in_growth:
                in_growth = True
                phase_start = x
                growth_log = 0
                duration = 0
                t_seq = []
                initial_t = t
            growth_log += log_r
            duration += 1
            t_seq.append(t)
        else:
            if in_growth:
                phase_stats.append((phase_start, duration, growth_log, initial_t, t_seq[:]))
                in_growth = False

        x = nxt

    if in_growth:
        phase_stats.append((phase_start, duration, growth_log, initial_t, t_seq[:]))

print(f"Total growth phases found: {len(phase_stats)}")
print(f"Max duration: {max(d for _, d, _, _, _ in phase_stats)}")
print(f"Max total growth: {max(g for _, _, g, _, _ in phase_stats):.2f} bits")

# Duration distribution
dur_counts = Counter(d for _, d, _, _, _ in phase_stats)
print(f"\nDuration distribution:")
for d in sorted(dur_counts):
    cnt = dur_counts[d]
    pct = cnt / len(phase_stats) * 100
    avg_growth = sum(g for _, dd, g, _, _ in phase_stats if dd == d) / cnt
    print(f"  {d:>2} hops: {cnt:>7} ({pct:>6.2f}%)  avg growth = {avg_growth:>+.3f} bits")


# === Part 2: t-value decay during growth phases ===
print("\n\n=== Part 2: t-Value Behavior During Growth Phases ===\n")
print("Does the t-value decrease during growth phases?\n")

# For growth phases of length >= 2, check if t decreases
t_changes = []
for _, d, _, init_t, t_seq in phase_stats:
    if d >= 2:
        for i in range(1, len(t_seq)):
            t_changes.append(t_seq[i] - t_seq[i-1])

if t_changes:
    avg_change = sum(t_changes) / len(t_changes)
    p_decrease = sum(1 for c in t_changes if c < 0) / len(t_changes)
    p_increase = sum(1 for c in t_changes if c > 0) / len(t_changes)
    p_same = sum(1 for c in t_changes if c == 0) / len(t_changes)
    print(f"Consecutive t-value changes within growth phases:")
    print(f"  Mean change: {avg_change:+.3f}")
    print(f"  P(decrease): {p_decrease:.4f}")
    print(f"  P(same): {p_same:.4f}")
    print(f"  P(increase): {p_increase:.4f}")

# t-value at END vs START of growth phase
print(f"\nInitial vs final t-value of growth phases:")
t_start_end = defaultdict(list)
for _, d, _, init_t, t_seq in phase_stats:
    if d >= 1 and t_seq:
        t_start_end[init_t].append(t_seq[-1])

print(f"{'initial t':>10} {'count':>7} {'avg final t':>12} {'P(final < initial)':>19}")
for it in sorted(t_start_end):
    if it > 10 or len(t_start_end[it]) < 5:
        continue
    finals = t_start_end[it]
    avg_f = sum(finals) / len(finals)
    p_dec = sum(1 for f in finals if f < it) / len(finals)
    print(f"{it:>10} {len(finals):>7} {avg_f:>12.3f} {p_dec:>19.4f}")


# === Part 3: Growth bounded by initial t? ===
print("\n\n=== Part 3: Is Total Growth Bounded by Initial t? ===\n")

# Theory: if x has t-value t0, the first hop grows by log2((3/2)^(t0+2)/2^v)
# Max growth (v=1): log2((3/2)^(t0+2)/2) = (t0+2)*0.585 - 1
# If subsequent hops have SMALLER t, total growth is bounded by
# sum_{j=0}^{t0} ((t0-j+2)*0.585 - 1) * P(growth at step j)

growth_by_initial_t = defaultdict(list)
for _, d, g, init_t, _ in phase_stats:
    growth_by_initial_t[init_t].append(g)

print(f"{'initial t':>10} {'count':>7} {'avg growth':>11} {'max growth':>11} "
      f"{'theory max':>11} {'bounded?':>9}")
for it in sorted(growth_by_initial_t):
    if it > 12 or len(growth_by_initial_t[it]) < 3:
        continue
    vals = growth_by_initial_t[it]
    avg = sum(vals) / len(vals)
    mx = max(vals)
    # Theoretical max: (t+2)*0.585 - 1 for v=1 first hop
    theory = (it + 2) * 0.585 - 1
    bounded = "YES" if mx <= theory * 3 else "close" if mx <= theory * 5 else "NO"
    print(f"{it:>10} {len(vals):>7} {avg:>+11.3f} {mx:>+11.3f} "
          f"{theory:>+11.3f} {bounded:>9}")


# === Part 4: What happens AFTER a growth phase? ===
print("\n\n=== Part 4: Contraction After Growth Phases ===\n")
print("How much shrinkage follows a growth phase?\n")

post_growth = []
for x_start in range(3, min(N + 1, 200001), 2):
    x = x_start
    in_growth = False
    growth_log = 0
    pre_growth_x = 0

    for hop in range(200):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break

        log_r = log2(nxt / x)

        if log_r > 0:
            if not in_growth:
                in_growth = True
                pre_growth_x = x
                growth_log = 0
            growth_log += log_r
        else:
            if in_growth:
                # Growth phase just ended. Track the shrinkage.
                shrink_log = log_r
                post_growth.append((growth_log, shrink_log, pre_growth_x))
                in_growth = False

        x = nxt

# Bucket by growth magnitude
growth_buckets = defaultdict(list)
for g, s, _ in post_growth:
    bucket = min(int(g), 10)
    growth_buckets[bucket].append(s)

print(f"{'growth (bits)':>14} {'count':>7} {'avg shrinkage':>14} {'P(compensates)':>15}")
for b in sorted(growth_buckets):
    vals = growth_buckets[b]
    if len(vals) < 10:
        continue
    avg_s = sum(vals) / len(vals)
    p_comp = sum(1 for s in vals if abs(s) >= b for s in vals) / len(vals)
    print(f"  [{b:>+3}, {b+1:>+3}) {len(vals):>7} {avg_s:>+14.3f} {p_comp:>15.4f}")


# === Part 5: The key bound attempt ===
print("\n\n=== Part 5: Growth Phase Total vs Subsequent Shrinkage ===\n")
print("After a growth phase of G bits, how many hops until net L-change < 0?\n")

# For each growth phase, trace until net contraction compensates the growth
for x_start in [131071, 524287, 2097151, 8388607]:  # 2^n - 1 cases
    if x_start > 10000000:
        continue
    x = x_start
    cumulative = 0
    print(f"\nx = {x_start} = 2^{int(log2(x_start+1))}-1:")
    for hop in range(50):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        log_r = log2(nxt / x)
        cumulative += log_r
        marker = " ***" if cumulative < 0 and hop > 0 else ""
        print(f"  hop {hop+1:>2}: {case}(t={t:>2}), v2={v2(fmf):>2}, "
              f"log2(R)={log_r:>+7.3f}, cumulative={cumulative:>+8.3f}{marker}")
        if cumulative < 0 and hop > 0:
            print(f"  -> Net descent at hop {hop+1} (started above at hop 1)")
            break
        x = nxt
