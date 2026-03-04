"""
explore24.py - Epoch Analysis: Growth + Recovery Cycles

An "epoch" starting from x is defined as the sequence of FMF hops until
the trajectory first drops below x. Each epoch consists of:
  - A growth phase (where the trajectory may climb above x)
  - A recovery phase (where the trajectory returns below x)

If we can show:
  1. Every epoch terminates (trajectory always returns below x)
  2. Epoch duration is bounded by C * log(x) or similar

Then Collatz follows immediately: each epoch brings the trajectory to
a SMALLER value, and the process can't continue forever.

From explore22-23:
  - Growth phases max 7 hops (for x up to 500K)
  - Recovery takes ~ growth_bits / 0.83 hops
  - 2^n-1 cases: recovery in O(n) hops

The KEY question: is there a DETERMINISTIC bound on epoch duration?
"""
from collections import defaultdict, Counter
from math import log2, log


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


# === Part 1: Epoch statistics ===
print("=== Part 1: Epoch Statistics ===\n")
print("For each odd x, compute the epoch: hops until F^k(x) < x\n")

N = 200000
epoch_data = []  # (x, epoch_duration, peak_ratio, growth_bits)

no_descent = 0
for x_start in range(3, N + 1, 2):
    x = x_start
    peak = x
    for hop in range(500):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        if nxt > peak:
            peak = nxt
        if nxt < x_start:
            epoch_data.append((x_start, hop + 1, peak / x_start, log2(peak / x_start)))
            break
        x = nxt
    else:
        no_descent += 1

print(f"Numbers tested: {N // 2}")
print(f"Numbers with epoch data: {len(epoch_data)}")
print(f"No descent within 500 hops: {no_descent}")

if epoch_data:
    durations = [d for _, d, _, _ in epoch_data]
    peaks = [p for _, _, p, _ in epoch_data]
    print(f"\nEpoch duration: mean={sum(durations)/len(durations):.2f}, "
          f"max={max(durations)}, median={sorted(durations)[len(durations)//2]}")
    print(f"Peak ratio: mean={sum(peaks)/len(peaks):.2f}, max={max(peaks):.2f}")


# === Part 2: Epoch duration vs bit-length ===
print("\n\n=== Part 2: Epoch Duration vs Bit-Length ===\n")
print("Does epoch duration grow with bit-length of x?\n")

bits_data = defaultdict(list)
for x_start, dur, peak, _ in epoch_data:
    bits = int(log2(x_start)) + 1
    bits_data[bits].append((dur, peak))

print(f"{'bits':>5} {'count':>7} {'avg dur':>8} {'max dur':>8} {'avg peak':>9} {'max peak':>10}")
for bits in sorted(bits_data):
    vals = bits_data[bits]
    avg_d = sum(d for d, _ in vals) / len(vals)
    max_d = max(d for d, _ in vals)
    avg_p = sum(p for _, p in vals) / len(vals)
    max_p = max(p for _, p in vals)
    print(f"{bits:>5} {len(vals):>7} {avg_d:>8.2f} {max_d:>8} {avg_p:>9.2f} {max_p:>10.2f}")


# === Part 3: Epoch duration distribution ===
print("\n\n=== Part 3: Epoch Duration Distribution ===\n")

dur_counts = Counter(d for _, d, _, _ in epoch_data)
total = len(epoch_data)
cumul = 0
for d in sorted(dur_counts):
    cnt = dur_counts[d]
    cumul += cnt
    pct = cnt / total * 100
    cpct = cumul / total * 100
    if d <= 30 or cnt > 5:
        print(f"  {d:>3} hops: {cnt:>7} ({pct:>6.2f}%)  cumul: {cpct:>6.1f}%")


# === Part 4: Hardest epochs - what makes them long? ===
print("\n\n=== Part 4: Anatomy of Hardest Epochs ===\n")

epoch_data.sort(key=lambda x: -x[1])  # Sort by duration
print("Top 20 longest epochs:")
print(f"{'x':>10} {'duration':>9} {'peak ratio':>11} {'peak bits':>10}")
for x_start, dur, peak, pbits in epoch_data[:20]:
    print(f"{x_start:>10} {dur:>9} {peak:>11.2f} {pbits:>10.2f}")


# === Part 5: Is epoch duration bounded by C * log(x)? ===
print("\n\n=== Part 5: Epoch Duration / log2(x) Ratio ===\n")

ratios = []
for x_start, dur, _, _ in epoch_data:
    if x_start >= 10:
        r = dur / log2(x_start)
        ratios.append((r, x_start, dur))

ratios.sort(reverse=True)
print(f"Max(duration / log2(x)):")
for r, x, d in ratios[:20]:
    print(f"  x={x:>10}: dur={d:>3}, log2(x)={log2(x):.2f}, ratio={r:.4f}")

max_ratio = ratios[0][0]
print(f"\nMax ratio overall: {max_ratio:.4f}")
print(f"Suggested C bound: {max_ratio * 1.5:.2f}")


# === Part 6: The "Argument B" check ===
print("\n\n=== Part 6: Epoch Decomposition into Growth + Recovery ===\n")

growth_recovery = []
for x_start in range(3, min(N + 1, 100001), 2):
    x = x_start
    growth_hops = 0
    recovery_hops = 0
    peak = x
    in_growth = True  # Start in growth until first descent below peak

    for hop in range(500):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break

        if nxt >= peak and in_growth:
            growth_hops += 1
            peak = max(peak, nxt)
        else:
            in_growth = False
            recovery_hops += 1

        if nxt < x_start:
            growth_recovery.append((x_start, growth_hops, recovery_hops,
                                    growth_hops + recovery_hops, peak / x_start))
            break
        x = nxt

if growth_recovery:
    print(f"{'metric':>20} {'mean':>8} {'max':>8}")
    g_hops = [g for _, g, _, _, _ in growth_recovery]
    r_hops = [r for _, _, r, _, _ in growth_recovery]
    t_hops = [t for _, _, _, t, _ in growth_recovery]
    peaks = [p for _, _, _, _, p in growth_recovery]
    print(f"{'growth hops':>20} {sum(g_hops)/len(g_hops):>8.2f} {max(g_hops):>8}")
    print(f"{'recovery hops':>20} {sum(r_hops)/len(r_hops):>8.2f} {max(r_hops):>8}")
    print(f"{'total epoch':>20} {sum(t_hops)/len(t_hops):>8.2f} {max(t_hops):>8}")
    print(f"{'peak ratio':>20} {sum(peaks)/len(peaks):>8.2f} {max(peaks):>8.2f}")

    # Recovery hops vs peak ratio
    print(f"\nRecovery hops vs peak growth:")
    peak_buckets = defaultdict(list)
    for _, _, r, _, p in growth_recovery:
        bucket = min(int(log2(p)) if p > 1 else 0, 15)
        peak_buckets[bucket].append(r)

    print(f"{'peak (bits)':>12} {'count':>7} {'avg recovery':>13} {'theory':>8}")
    for b in sorted(peak_buckets):
        vals = peak_buckets[b]
        if len(vals) < 5:
            continue
        avg = sum(vals) / len(vals)
        theory = (b + 1) / 0.83  # Expected: peak_bits / drift_rate
        print(f"  [{b:>+3}, {b+1:>+3}) {len(vals):>7} {avg:>13.2f} {theory:>8.1f}")
