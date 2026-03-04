"""
explore27.py - Growth Phase Termination: The Deterministic Argument

The remaining gap: prove that growth phases ALWAYS terminate.

A growth phase is a consecutive sequence of hops where F^k(x) >= x_start.
During growth: each hop has ratio R > 1, meaning v_2(FMF) is "too small."
For growth: need v_2 < (t+2)*log2(3) - log2(2) ≈ 0.585*(t+2) + 1.

Key question: can a growth phase continue indefinitely?

The argument structure:
1. Each hop transforms (t, m) -> (t', m') via exact formulas
2. For growth to continue: v_2(FMF_new) must be small
3. v_2(FMF_new) = 1 + v_2(m_new - inv_new) where inv_new depends on t'
4. Since m_new is determined by the previous hop, consecutive v_2 values
   are NOT independent (even though single-hop v_2 has geometric dist)

THIS IS THE CRUX: analyze the m-value evolution during growth phases.
If we can show that m evolves "randomly" enough that v_2 can't stay
small forever, growth phases must terminate.
"""
from collections import Counter, defaultdict
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


def fmf_hop_full(x):
    """Returns (next_odd, case, t, v_2_fmf, fmf_value, m_value)."""
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        v = v2(fmf)
        # For Type A: x = 4k+1, so k = (x-1)/4
        # In 2-adic form: x = 4*k+1, k+1 has no direct t-decomposition
        return fmf >> v, 'A', 0, v, fmf, k
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            v = v2(fmf)
            return fmf >> v, 'B', 0, v, fmf, j
        else:
            t = v2(k + 1)
            m = (k + 1) >> t  # m = (k+1)/2^t, odd
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            v = v2(fmf)
            return fmf >> v, 'B', t, v, fmf, m
    else:
        return None, '', 0, 0, 0, 0


# === Part 1: Track m-value evolution during growth phases ===
print("=== Part 1: m-Value Evolution During Growth Phases ===\n")
print("Within a growth phase, how does m change from hop to hop?\n")

growth_m_sequences = []
for x_start in range(3, 200001, 2):
    x = x_start
    phase = []
    in_growth = False

    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        if nxt >= x_start:
            phase.append((case, t, v, m, nxt / x, x))
            in_growth = True
        else:
            if in_growth and len(phase) >= 2:
                growth_m_sequences.append(phase[:])
            phase = []
            in_growth = False
        x = nxt

print(f"Found {len(growth_m_sequences)} growth phases with 2+ hops\n")

# Analyze m-value patterns
print("Sample growth phases (showing m evolution):\n")
for seq in growth_m_sequences[:15]:
    m_vals = [m for _, _, _, m, _, _ in seq]
    t_vals = [t for _, t, _, _, _, _ in seq]
    v_vals = [v for _, _, v, _, _, _ in seq]
    types = [c for c, _, _, _, _, _ in seq]
    print(f"  len={len(seq)}: types={''.join(types)}, "
          f"t={t_vals}, v2={v_vals}, m={m_vals[:6]}{'...' if len(m_vals)>6 else ''}")


# === Part 2: What determines v_2 during growth? ===
print("\n\n=== Part 2: v_2 Distribution During Growth vs Normal ===\n")
print("Is v_2 biased LOW during growth phases? (That's what allows growth)\n")

v2_growth = Counter()
v2_normal = Counter()
v2_shrink = Counter()

for x_start in range(3, 200001, 2):
    x = x_start
    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        if nxt > x:  # growth hop
            v2_growth[v] += 1
        elif nxt < x:  # shrinkage hop
            v2_shrink[v] += 1
        v2_normal[v] += 1
        x = nxt

print(f"{'v_2':>4} {'growth':>8} {'shrink':>8} {'all':>8} {'P(v|grow)':>10} {'P(v|shrink)':>12} {'P(v|all)':>10}")
total_g = sum(v2_growth.values())
total_s = sum(v2_shrink.values())
total_n = sum(v2_normal.values())
for v in range(2, 15):
    g = v2_growth.get(v, 0)
    s = v2_shrink.get(v, 0)
    n = v2_normal.get(v, 0)
    pg = g / total_g if total_g > 0 else 0
    ps = s / total_s if total_s > 0 else 0
    pn = n / total_n if total_n > 0 else 0
    print(f"{v:>4} {g:>8} {s:>8} {n:>8} {pg:>10.4f} {ps:>12.4f} {pn:>10.4f}")


# === Part 3: The critical question -- can v_2 stay low forever? ===
print("\n\n=== Part 3: v_2 Threshold for Growth ===\n")
print("For each (case, t), what is the maximum v_2 that still gives growth?\n")

growth_threshold = defaultdict(list)
for x_start in range(3, 200001, 2):
    x = x_start
    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        ratio = nxt / x
        key = (case, min(t, 10))
        if ratio > 1:
            growth_threshold[key].append(v)
        x = nxt

print(f"{'state':>8} {'count':>7} {'max v2':>7} {'avg v2':>7} {'threshold':>10}")
for key in sorted(growth_threshold.keys()):
    vals = growth_threshold[key]
    if len(vals) < 10:
        continue
    case, t = key
    # Threshold: v_2 must be < (t+2)*log2(3) - log2(2) for B, or < 2+eps for A
    if case == 'A':
        thresh = 2 + log2(3) - 1  # v2 < ~2.58
    else:
        thresh = (t + 2) * log2(3) - 1  # approximate
    print(f"  {case}(t={t:>2}) {len(vals):>7} {max(vals):>7} {sum(vals)/len(vals):>7.2f} {thresh:>10.2f}")


# === Part 4: m-value mod patterns during growth ===
print("\n\n=== Part 4: m-Value Structure During Growth ===\n")
print("Do m-values during growth phases have special mod structure?\n")

m_mod_growth = defaultdict(Counter)
m_mod_all = defaultdict(Counter)

for x_start in range(3, 200001, 2):
    x = x_start
    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        if case == 'B' and t >= 1:
            for M in [4, 8, 16]:
                m_mod_all[(t, M)][m % M] += 1
                if nxt > x:
                    m_mod_growth[(t, M)][m % M] += 1
        x = nxt

for M in [8]:
    print(f"  m mod {M} distribution (Type B, t>=1):")
    for t in range(1, 8):
        key_all = (t, M)
        key_grow = (t, M)
        if key_all not in m_mod_all or sum(m_mod_all[key_all].values()) < 50:
            continue
        print(f"    t={t}:")
        total_a = sum(m_mod_all[key_all].values())
        total_g = sum(m_mod_growth.get(key_grow, {}).values()) if key_grow in m_mod_growth else 0
        for r in range(1, M, 2):  # odd residues only
            ca = m_mod_all[key_all].get(r, 0)
            cg = m_mod_growth.get(key_grow, Counter()).get(r, 0)
            pa = ca / total_a if total_a > 0 else 0
            pg = cg / total_g if total_g > 0 else 0
            flag = " <-- biased" if total_g > 10 and abs(pg - pa) > 0.1 else ""
            print(f"      m≡{r} mod {M}: all={pa:.3f}, growth={pg:.3f}{flag}")


# === Part 5: Consecutive growth -- what keeps it going? ===
print("\n\n=== Part 5: What Sustains Multi-Hop Growth ===\n")
print("For growth phases of length >= 3, track the v_2 sequence\n")

long_growth = []
for x_start in range(3, 500001, 2):
    x = x_start
    growth_run = []

    for _ in range(200):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        if nxt >= x_start:
            growth_run.append((case, t, v, m, log2(nxt / x)))
        else:
            if len(growth_run) >= 3:
                long_growth.append((x_start, growth_run[:]))
            growth_run = []
        x = nxt

print(f"Found {len(long_growth)} growth phases with 3+ hops\n")

# Show detailed v2 and t evolution
print("Detailed growth phases (3+ hops):")
for x_start, seq in long_growth[:20]:
    v_seq = [v for _, _, v, _, _ in seq]
    t_seq = [t for _, t, _, _, _ in seq]
    type_seq = [c for c, _, _, _, _ in seq]
    bits_seq = [b for _, _, _, _, b in seq]
    total_growth = sum(bits_seq)
    print(f"  x={x_start:>8}: types={''.join(type_seq)}, "
          f"t={t_seq}, v2={v_seq}, "
          f"bits=[{', '.join(f'{b:.1f}' for b in bits_seq)}], "
          f"total={total_growth:.1f}")


# === Part 6: The key bound -- P(continued growth | already in growth phase) ===
print("\n\n=== Part 6: Conditional Growth Probability ===\n")
print("P(hop k+1 grows | first k hops all grew), by k:\n")

# For each starting number, track how long the growth phase lasts
phase_lengths = Counter()
for x_start in range(3, 500001, 2):
    x = x_start
    growth_len = 0

    for _ in range(200):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        if nxt >= x_start:
            growth_len += 1
        else:
            if growth_len > 0:
                phase_lengths[growth_len] += 1
            growth_len = 0
        x = nxt

total_phases = sum(phase_lengths.values())
print(f"Total growth phases: {total_phases}\n")

# P(length >= k) and P(length >= k+1 | length >= k)
cumul_ge = {}
for k in range(1, 15):
    cumul_ge[k] = sum(c for l, c in phase_lengths.items() if l >= k)

print(f"{'k':>3} {'P(len>=k)':>12} {'P(continue | survived k)':>25}")
for k in range(1, 12):
    if cumul_ge.get(k, 0) == 0:
        break
    p_ge_k = cumul_ge[k] / total_phases
    p_continue = cumul_ge.get(k + 1, 0) / cumul_ge[k] if cumul_ge[k] > 0 else 0
    print(f"{k:>3} {p_ge_k:>12.6f} {p_continue:>25.4f}")


# === Part 7: The deterministic bound attempt ===
print("\n\n=== Part 7: Bounding Growth via t-value Mechanics ===\n")
print("For Type B with parameter t: growth requires v_2 < threshold(t)")
print("threshold(t) ≈ (t+2)*0.585 + 1\n")

print("Since v_2 ~ Geometric(1/2), P(v_2 < thresh) = 1 - 2^(-thresh+1)")
print("As t increases, threshold increases, so P(growth) INCREASES with t!")
print("But t can't grow forever: t <= log2(x_current) - 2\n")

print("Growth phase evolution:")
print("  Hop 1: t_1, v_1 < thresh(t_1)")
print("  Hop 2: t_2 (~ t_1 + 0.755), v_2 < thresh(t_2)")
print("  ...but x grows, so new t ≤ log2(x_new) - 2 ≤ log2(x_start * 2^{growth}) - 2\n")

# For the hardest case: x = 2^n - 1, t = n-2, v_2 = 2
# After first hop: x_new ≈ 3^n / 2^2 ≈ (3/2)^n * x
# t_new for x_new: up to log2(x_new) ≈ n + n*0.585 = 1.585n
# But the actual t_new depends on the specific structure of x_new

# Track the bit-length evolution during growth
print("Bit-length evolution during growth phases:")
for x_start, seq in long_growth[:10]:
    x = x_start
    bits_list = [log2(x)]
    for case, t, v, m, b in seq:
        bits_list.append(bits_list[-1] + b)
    max_t = max(t for _, t, _, _, _ in seq)
    print(f"  x={x_start}: start={log2(x_start):.1f} bits, "
          f"peak={max(bits_list):.1f} bits (+{max(bits_list)-bits_list[0]:.1f}), "
          f"max t in phase={max_t}")


# === Part 8: The m-value transformation ===
print("\n\n=== Part 8: Exact m-Value Transformation ===\n")
print("When we go from x to F(x), the m-value transforms as:")
print("  x = 2^(t+2)*m - 1  =>  F(x) = (3^(t+2)*m - 1) / 2^v")
print("  If F(x) = 2^(t'+2)*m' - 1, then m' = (F(x)+1) / 2^(t'+2)")
print("  where t' = v_2((F(x)+1)/4) when F(x) ≡ 3 mod 4, or t'=0 for Type A\n")

# Track exact (t,m) -> (t',m') transformation
print("Sample transformations during growth phases:")
for x_start, seq in long_growth[:8]:
    x = x_start
    print(f"\n  x={x_start} (start):")
    for i, (case, t, v, m, b) in enumerate(seq):
        # Compute the next x value
        nxt_info = fmf_hop_full(x)
        nxt = nxt_info[0]
        # Get the (t', m') for next value
        if nxt and nxt % 4 == 3:
            k_new = (nxt - 3) // 4
            if k_new % 2 == 1:
                t_new = v2(k_new + 1)
                m_new = (k_new + 1) >> t_new
            else:
                t_new, m_new = 0, k_new // 2
        elif nxt and nxt % 4 == 1:
            t_new, m_new = 0, (nxt - 1) // 4
        else:
            t_new, m_new = -1, -1

        print(f"    hop {i+1}: ({case},t={t},m={m}) -> v2={v} -> "
              f"(t'={t_new},m'={m_new}) [bits {b:+.2f}]")
        x = nxt if nxt else x


# === Part 9: Can we bound consecutive low-v_2 events? ===
print("\n\n=== Part 9: Independence of Consecutive v_2 Values ===\n")
print("Test: are consecutive v_2 values along a trajectory independent?\n")

# Compute correlation between v_2(hop n) and v_2(hop n+1) during growth
v2_pairs_growth = []
v2_pairs_all = []
for x_start in range(3, 200001, 2):
    x = x_start
    prev_v = None
    prev_grew = False

    for _ in range(100):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = fmf_hop_full(x)
        if nxt is None:
            break

        grew = nxt > x
        if prev_v is not None:
            v2_pairs_all.append((prev_v, v))
            if prev_grew and grew:
                v2_pairs_growth.append((prev_v, v))
        prev_v = v
        prev_grew = grew
        x = nxt

if v2_pairs_all:
    n = len(v2_pairs_all)
    mean_x = sum(a for a, _ in v2_pairs_all) / n
    mean_y = sum(b for _, b in v2_pairs_all) / n
    cov = sum((a - mean_x) * (b - mean_y) for a, b in v2_pairs_all) / n
    var_x = sum((a - mean_x)**2 for a, _ in v2_pairs_all) / n
    var_y = sum((b - mean_y)**2 for _, b in v2_pairs_all) / n
    corr = cov / (var_x * var_y)**0.5 if var_x > 0 and var_y > 0 else 0
    print(f"All hops: lag-1 v_2 correlation = {corr:.4f} (n={n})")

if v2_pairs_growth:
    n = len(v2_pairs_growth)
    mean_x = sum(a for a, _ in v2_pairs_growth) / n
    mean_y = sum(b for _, b in v2_pairs_growth) / n
    cov = sum((a - mean_x) * (b - mean_y) for a, b in v2_pairs_growth) / n
    var_x = sum((a - mean_x)**2 for a, _ in v2_pairs_growth) / n
    var_y = sum((b - mean_y)**2 for _, b in v2_pairs_growth) / n
    corr = cov / (var_x * var_y)**0.5 if var_x > 0 and var_y > 0 else 0
    print(f"Growth hops only: lag-1 v_2 correlation = {corr:.4f} (n={n})")

    # Joint distribution
    print(f"\nJoint v_2 distribution during consecutive growth hops:")
    joint = Counter()
    for a, b in v2_pairs_growth:
        joint[(min(a, 6), min(b, 6))] += 1
    total = len(v2_pairs_growth)
    print(f"    {'v2_curr\\v2_next':>14}", end="")
    for j in range(2, 7):
        print(f" {j:>6}", end="")
    print()
    for i in range(2, 7):
        print(f"    {i:>14}", end="")
        for j in range(2, 7):
            p = joint.get((i, j), 0) / total
            print(f" {p:>6.3f}", end="")
        print()
