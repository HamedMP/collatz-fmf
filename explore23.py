"""
explore23.py - 2^n - 1 Trajectory Analysis: The Hardest Cases

Numbers of the form 2^n - 1 produce the worst single-hop growth ratios
because they have t = n-2 and v_2(FMF) = 2 (the minimum for B-type).

Questions:
1. After the big first hop, how quickly does the trajectory "normalize"?
2. Is there a pattern in the trajectory of 2^n - 1?
3. Does the trajectory of 2^(n+1) - 1 pass through 2^n - 1?
4. Can we bound the maximum value reached in the trajectory?

If 2^n - 1 trajectories are the hardest and they ALL converge,
that would be strong evidence. But we need a STRUCTURAL argument.
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


# === Part 1: Trajectories of 2^n - 1 ===
print("=== Part 1: FMF Trajectories of 2^n - 1 ===\n")

for n in range(3, 25):
    x_start = 2**n - 1
    x = x_start
    hops = 0
    peak = x
    peak_ratio = 1.0
    hops_to_descend = None

    for hop in range(500):
        if x <= 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        hops += 1
        if nxt > peak:
            peak = nxt
        if nxt / x_start > peak_ratio:
            peak_ratio = nxt / x_start
        if nxt < x_start and hops_to_descend is None:
            hops_to_descend = hops
        x = nxt

    if hops_to_descend is None:
        hops_to_descend = hops  # reached 1
    hops_to_1 = hops
    print(f"  2^{n:>2}-1 = {x_start:>12}: "
          f"hops_to_1={hops_to_1:>3}, "
          f"hops_to_descend={hops_to_descend:>3}, "
          f"peak/x={peak_ratio:>10.2f}, "
          f"peak_bits={log2(peak):.1f}")


# === Part 2: First hop analysis for 2^n - 1 ===
print("\n\n=== Part 2: First Hop of 2^n - 1 ===\n")
print("For x = 2^n - 1 = 2^(t+2)*m - 1 with m=1, t=n-2:")
print("  FMF = 2(3^(t+2) - 1)")
print("  v_2(FMF) = v_2(3^n - 1) = 1 (n odd) or v_2(n)+2 (n even)")
print("  F(x) = (3^n - 1) / 2^{v_2(3^n-1)-1}\n")

for n in range(3, 25):
    x = 2**n - 1
    nxt, case, t, fmf = fmf_hop_detailed(x)
    v = v2(fmf)
    ratio = nxt / x if nxt else 0
    print(f"  n={n:>2}: x={x:>12}, t={t:>2}, v2(FMF)={v:>2}, "
          f"F(x)={nxt:>12}, ratio={ratio:>10.4f}")


# === Part 3: Does 2^(n+1)-1 pass through 2^n-1? ===
print("\n\n=== Part 3: Do Larger Mersenne Numbers Pass Through Smaller Ones? ===\n")

mersenne_set = {2**n - 1 for n in range(3, 30)}
for n in range(3, 22):
    x_start = 2**n - 1
    x = x_start
    visited_mersenne = []
    for hop in range(500):
        if x <= 1:
            break
        if x in mersenne_set and x != x_start:
            visited_mersenne.append(x)
        nxt, _, _, _ = fmf_hop_detailed(x)
        if nxt is None:
            break
        x = nxt
    if visited_mersenne:
        print(f"  2^{n:>2}-1 = {x_start:>8} passes through: "
              f"{', '.join(str(m) for m in visited_mersenne[:5])}")


# === Part 4: The trajectory AFTER the big first hop ===
print("\n\n=== Part 4: Post-First-Hop Behavior ===\n")
print("After the big growth hop, how quickly does the trajectory normalize?\n")

for n in [7, 10, 13, 17, 20]:
    x_start = 2**n - 1
    x = x_start
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None:
        continue

    print(f"\n2^{n}-1 = {x_start}: first hop to {nxt} (ratio {nxt/x_start:.2f})")

    # Track the next 20 hops from F(2^n-1)
    x = nxt
    cumul = log2(nxt / x_start)
    for hop in range(20):
        if x <= 1:
            break
        nxt2, c2, t2, fmf2 = fmf_hop_detailed(x)
        if nxt2 is None:
            break
        log_r = log2(nxt2 / x)
        cumul += log_r
        marker = ""
        if cumul < 0:
            marker = " << NET DESCENT"
        print(f"  hop {hop+2:>2}: {c2}(t={t2:>2}), v2={v2(fmf2):>2}, "
              f"log2(R)={log_r:>+7.3f}, cumul from start={cumul:>+8.3f}{marker}")
        if cumul < 0:
            break
        x = nxt2


# === Part 5: The output of 2^n-1 modular analysis ===
print("\n\n=== Part 5: Output F(2^n-1) Modular Structure ===\n")
print("F(2^n-1) = (3^n - 1) / 2^{v_2(3^n-1)-1}")
print("What's the structure of this number?\n")

for n in range(3, 25):
    x = 2**n - 1
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None:
        continue
    mod4 = nxt % 4
    mod8 = nxt % 8
    if mod4 == 1:
        k_out = (nxt - 1) // 4
        t_out = 0
        type_out = "A"
    else:
        k_out = (nxt - 3) // 4
        if k_out % 2 == 0:
            t_out = 0
            type_out = "B0"
        else:
            t_out = v2(k_out + 1)
            type_out = f"B{t_out}"

    print(f"  n={n:>2}: F(x)={nxt:>12}, mod4={mod4}, mod8={mod8}, "
          f"type={type_out:>4}, "
          f"k_out={k_out}")


# === Part 6: The maximum value in any trajectory ===
print("\n\n=== Part 6: Peak Value / Starting Value for All Numbers ===\n")

# For each x, compute peak/x ratio
peak_data = []
for x_start in range(3, 200001, 2):
    x = x_start
    peak = x
    for hop in range(500):
        if x <= 1:
            break
        nxt, _, _, _ = fmf_hop_detailed(x)
        if nxt is None:
            break
        if nxt > peak:
            peak = nxt
        x = nxt
    peak_ratio = peak / x_start
    peak_data.append((peak_ratio, x_start))

peak_data.sort(reverse=True)
print("Top 20 highest peak/start ratios:")
for ratio, x in peak_data[:20]:
    bits = int(log2(x)) + 1
    print(f"  x={x:>8} ({bits:>2}-bit): peak/start = {ratio:>12.2f}, "
          f"peak bits = {log2(ratio*x):>.1f}")

# Is peak/start bounded?
print(f"\nPeak/start ratio vs bit-length:")
for bits in range(3, 19):
    lo = 2**(bits-1)
    hi = 2**bits
    vals = [(r, x) for r, x in peak_data if lo <= x < hi]
    if not vals:
        continue
    max_r, max_x = max(vals)
    avg_r = sum(r for r, _ in vals) / len(vals)
    print(f"  {bits:>2}-bit: max peak/start = {max_r:>12.2f} (x={max_x}), "
          f"avg = {avg_r:>.2f}")
