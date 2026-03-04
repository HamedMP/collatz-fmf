"""
explore18.py - Self-Correction Proof: Why Large-t Hops are Followed by Type A

From explore16, we observed that after B(t>=2) hops, the NEXT hop is
disproportionately likely to be Type A (shrinking). This is a compensatory
mechanism that prevents sustained growth.

Question: Can we prove this algebraically?

After a B(t) hop, the output is:
  F(x) = (3^(t+2)*m - 1) / 2^v  where v = v_2(3^(t+2)*m - 1)

For F(x) to be Type A (≡ 1 mod 4), we need F(x) ≡ 1 mod 4.
For F(x) to be Type B (≡ 3 mod 4), we need F(x) ≡ 3 mod 4.

From Theorem 12, P(Type A) = 50% when m ranges uniformly over odds.
But the KEY QUESTION is: does the m of the OUTPUT x' have the same
distribution as a "random" odd number?

If F(x) is large (high-t hop = growth), does that bias the OUTPUT's
residue class in a way that favors shrinkage?
"""
from collections import Counter, defaultdict
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
    """Returns (next_odd, case, t_value, fmf_value)."""
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


# === Part 1: Type of F(x) given t-value of x ===
print("=== Part 1: P(next type | current t-value) ===\n")
print("Does a high-t hop bias the next hop toward Type A?\n")

# Along chains (not just single hops)
chain_transitions = defaultdict(Counter)  # (case, t) -> Counter of next (case, t)

for x_start in range(3, 100001, 2):
    x = x_start
    prev_info = None
    for _ in range(500):
        if x == 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        current_info = (case, t)
        if prev_info is not None:
            chain_transitions[prev_info][current_info] += 1
        prev_info = current_info
        x = nxt

print(f"{'from':>10} {'count':>7} {'P(A)':>7} {'P(B,t=0)':>9} {'P(B,t=1)':>9} {'P(B,t>=2)':>10}")
for from_state in sorted(chain_transitions, key=lambda s: (s[0], s[1])):
    nexts = chain_transitions[from_state]
    total = sum(nexts.values())
    if total < 50:
        continue
    p_a = sum(v for (c, t), v in nexts.items() if c == 'A') / total
    p_b0 = nexts.get(('B', 0), 0) / total
    p_b1 = nexts.get(('B', 1), 0) / total
    p_b2p = sum(v for (c, t), v in nexts.items() if c == 'B' and t >= 2) / total
    label = f"{from_state[0]}(t={from_state[1]})"
    print(f"{label:>10} {total:>7} {p_a:>7.4f} {p_b0:>9.4f} {p_b1:>9.4f} {p_b2p:>10.4f}")


# === Part 2: Algebraic analysis ===
# After a B(t) hop with output F(x) = (3^(t+2)*m - 1) / 2^v:
# F(x) mod 4 is determined by the low bits.
# The KEY: v = v_2(m - inv) where inv = (3^(t+2))^{-1} mod 2^large.
# After removing 2^v, we get F(x) = 3^(t+2) * (m - inv) / 2^v + correction.
# The low bits of F(x) come from 3^(t+2) * u where u = (m-inv)/2^v is the odd part.

# For the SECOND hop: F(x) is the new starting point.
# F(x) mod 4 determines if it's Type A or B.
# If Type B, the new k = (F(x)-3)/4, and the new t' = v_2(k+1).

# The question: is there a structural reason why large v_2(m-inv) (which
# correlates with large t in the CURRENT hop) affects the NEXT hop's type?

print("\n\n=== Part 2: v_2(FMF) vs Next Hop Type ===\n")
print("Does larger v_2 (= more division = more shrinkage) predict next type?\n")

v2_vs_next = defaultdict(Counter)

for x in range(3, 200001, 2):
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None or nxt <= 1:
        continue

    v = v2(fmf)
    nxt2, case2, t2, _ = fmf_hop_detailed(nxt)
    if nxt2 is None:
        continue

    v2_vs_next[v][case2] += 1

print(f"{'v2(FMF)':>8} {'count':>7} {'P(A next)':>10} {'P(B next)':>10}")
for v_val in sorted(v2_vs_next):
    if v_val > 12:
        continue
    counts = v2_vs_next[v_val]
    total = sum(counts.values())
    if total < 20:
        continue
    p_a = counts.get('A', 0) / total
    p_b = counts.get('B', 0) / total
    print(f"{v_val:>8} {total:>7} {p_a:>10.4f} {p_b:>10.4f}")


# === Part 3: The shrinkage-after-growth mechanism ===
print("\n\n=== Part 3: Growth Magnitude vs Next Hop Shrinkage ===\n")

growth_vs_next = defaultdict(list)

for x in range(3, 100001, 2):
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None or nxt <= 1:
        continue

    log_r = log2(nxt / x)
    nxt2, case2, t2, _ = fmf_hop_detailed(nxt)
    if nxt2 is None:
        continue

    log_r2 = log2(nxt2 / nxt)

    # Bucket by growth magnitude
    bucket = int(log_r)
    growth_vs_next[bucket].append(log_r2)

print(f"{'growth bucket':>14} {'count':>7} {'E[next log2(R)]':>16} {'P(shrink next)':>15}")
for bucket in sorted(growth_vs_next):
    vals = growth_vs_next[bucket]
    if len(vals) < 20:
        continue
    e = sum(vals) / len(vals)
    p_shrink = sum(1 for v in vals if v < 0) / len(vals)
    lo = bucket
    hi = bucket + 1
    print(f"  [{lo:>+3}, {hi:>+3}) {len(vals):>7} {e:>+16.4f} {p_shrink:>15.4f}")


# === Part 4: Algebraic explanation attempt ===
print("\n\n=== Part 4: Why Self-Correction Happens ===\n")

# The mechanism: when F(x) is large (growth), it tends to have a large
# value relative to the range [1, N]. Large values are more likely to be
# Type A (4k+1) because... actually they're 50/50 by Theorem 12.

# BUT: the self-correction comes from v_2 structure.
# After a large growth (small v_2 in the FMF), the output F(x) is large.
# The NEXT hop's v_2 depends on the output's k-value.
# If the output is Type A: always 1 hop with strong shrinkage.
# If the output is Type B: the t-value of the output matters.

# Key insight: the t-value distribution IS uniform (Theorem 12),
# BUT the correlation comes from: when the current hop has small v_2,
# the output is large -> the output's binary representation has specific
# properties -> the output's k-value has specific v_2 properties.

# Let's check: is the correlation coming from the TYPE or from the v_2?
print("Decomposing the self-correction:")
print()

# After growth by > 2 bits, what's the type and t-value distribution?
after_growth = Counter()
after_shrink = Counter()

for x in range(3, 100001, 2):
    nxt, case, t, fmf = fmf_hop_detailed(x)
    if nxt is None or nxt <= 1:
        continue

    log_r = log2(nxt / x)
    nxt2, case2, t2, _ = fmf_hop_detailed(nxt)
    if nxt2 is None:
        continue

    state = f"{case2}(t={t2})"
    if log_r > 1:
        after_growth[state] += 1
    elif log_r < -1:
        after_shrink[state] += 1

total_g = sum(after_growth.values())
total_s = sum(after_shrink.values())
all_states = sorted(set(list(after_growth.keys()) + list(after_shrink.keys())))

print(f"{'state':>10} {'after growth>1':>15} {'after shrink<-1':>16}")
for state in all_states[:10]:
    pg = after_growth.get(state, 0) / total_g * 100 if total_g > 0 else 0
    ps = after_shrink.get(state, 0) / total_s * 100 if total_s > 0 else 0
    print(f"{state:>10} {pg:>14.1f}% {ps:>15.1f}%")


# === Part 5: The v_2 chain ===
print("\n\n=== Part 5: Consecutive v_2(FMF) Values ===\n")
print("Is there a pattern in consecutive v_2 values along chains?\n")

v2_consecutive = defaultdict(list)
for x_start in range(3, 50001, 2):
    x = x_start
    prev_v = None
    for _ in range(200):
        if x == 1:
            break
        nxt, case, t, fmf = fmf_hop_detailed(x)
        if nxt is None:
            break
        curr_v = v2(fmf)
        if prev_v is not None:
            v2_consecutive[prev_v].append(curr_v)
        prev_v = curr_v
        x = nxt

print(f"{'prev v2':>8} {'count':>7} {'E[next v2]':>11} {'P(v2>=3)':>9} {'P(v2>=5)':>9}")
for pv in sorted(v2_consecutive):
    if pv > 10:
        continue
    vals = v2_consecutive[pv]
    if len(vals) < 50:
        continue
    e = sum(vals) / len(vals)
    p3 = sum(1 for v in vals if v >= 3) / len(vals)
    p5 = sum(1 for v in vals if v >= 5) / len(vals)
    print(f"{pv:>8} {len(vals):>7} {e:>11.4f} {p3:>9.4f} {p5:>9.4f}")

print("\nIf E[next v2 | prev v2 = small] > E[next v2 overall],")
print("that would explain self-correction: small v2 (growth) leads to")
print("larger next v2 (more division = more shrinkage).")
