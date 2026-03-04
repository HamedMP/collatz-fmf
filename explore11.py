"""
explore11.py - Markov Chain Model of FMF Dynamics

The FMF hop maps odd numbers to odd numbers. We model this as a Markov chain
where the state captures the key parameters that determine the next hop's behavior.

Key parameters at each hop:
- type: A (4k+1) or B (4k+3)
- For type B: t = v_2(k+1), which determines the growth factor 3^(t+2)

Questions:
1. What are the transition probabilities between states?
2. What is the expected log-multiplier per hop?
3. Does the stationary distribution give negative drift? (needed for descent)

If E[log(F(x)/x)] < 0 under the empirical distribution, this is strong
evidence that the FMF chain contracts on average.
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


def fmf_hop(x):
    """One FMF hop: returns (next_odd, collatz_steps, fmf_value, case_info)."""
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        steps = 1
        case = ('A', 0)
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            steps = 3
            case = ('B', 0)  # t=0 for k-even case
        else:
            t = v2(k + 1)
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            steps = 3 + 2 * t
            case = ('B', t)
    else:
        return None, 0, 0, None

    p = v2(fmf)
    return fmf >> p, steps + p, fmf, case


# === Part 1: Transition Matrix ===
# State = (type, t_value) where type is 'A' or 'B', t_value is the TZB parameter
# For type A, t=0 always. For type B, t >= 0.

print("=== Part 1: Empirical Transition Probabilities ===\n")

transitions = defaultdict(Counter)  # (from_state) -> Counter of (to_state)
hop_log_multiplier = defaultdict(list)  # state -> list of log2(F(x)/x)
state_counts = Counter()

for x in range(3, 100001, 2):
    mod4 = x % 4
    if mod4 == 1:
        from_state = ('A', 0)
    else:
        k = (x - 3) // 4
        if k % 2 == 0:
            from_state = ('B', 0)
        else:
            from_state = ('B', v2(k + 1))

    nxt, steps, fmf, case = fmf_hop(x)
    if nxt is None or nxt == 0:
        continue

    state_counts[from_state] += 1

    # Classify the result
    if nxt == 1:
        to_state = ('A', 0)  # 1 is 4*0+1
    elif nxt % 4 == 1:
        to_state = ('A', 0)
    else:
        k2 = (nxt - 3) // 4
        if k2 % 2 == 0:
            to_state = ('B', 0)
        else:
            to_state = ('B', v2(k2 + 1))

    transitions[from_state][to_state] += 1

    # Log multiplier
    if nxt > 0 and x > 0:
        lm = log2(nxt / x)
        hop_log_multiplier[from_state].append(lm)

# Print transition matrix (aggregate t values for readability)
print("From → To transition counts (states with t > 5 grouped as t=5+):")
print()

# Simplify: group by (type, min(t, 5))
def simplify_state(s):
    typ, t = s
    return (typ, min(t, 5))

simple_transitions = defaultdict(Counter)
simple_counts = Counter()
simple_log_mult = defaultdict(list)

for from_s, to_counts in transitions.items():
    sf = simplify_state(from_s)
    simple_counts[sf] += state_counts[from_s]
    for to_s, count in to_counts.items():
        st = simplify_state(to_s)
        simple_transitions[sf][st] += count

for from_s, mults in hop_log_multiplier.items():
    sf = simplify_state(from_s)
    simple_log_mult[sf].extend(mults)

# All states
all_states = sorted(set(list(simple_counts.keys()) + [s for t in simple_transitions.values() for s in t.keys()]))

# Print header
header = f"{'From':>8} {'count':>7} |"
for s in all_states:
    label = f"{s[0]}{s[1]}{'+'if s[1]==5 else ''}"
    header += f" {label:>7}"
header += " | E[log2(m)]"
print(header)
print("-" * len(header))

for from_s in all_states:
    if simple_counts[from_s] == 0:
        continue
    total = sum(simple_transitions[from_s].values())
    label = f"{from_s[0]}{from_s[1]}{'+'if from_s[1]==5 else ''}"
    row = f"{label:>8} {simple_counts[from_s]:>7} |"
    for to_s in all_states:
        count = simple_transitions[from_s].get(to_s, 0)
        if total > 0:
            row += f" {count/total*100:>6.1f}%"
        else:
            row += f" {'0':>6}%"

    # Expected log multiplier
    mults = simple_log_mult.get(from_s, [])
    if mults:
        row += f"  {sum(mults)/len(mults):>+.4f}"
    print(row)


# === Part 2: Expected Log Multiplier by State ===
print("\n\n=== Part 2: Expected Log2 Multiplier by Detailed State ===\n")
print(f"{'State':>10} {'count':>7} {'E[log2]':>10} {'median':>10} {'P(shrink)':>10} {'P(grow)':>10}")

for state in sorted(hop_log_multiplier.keys()):
    mults = hop_log_multiplier[state]
    if len(mults) < 10:
        continue
    mults_sorted = sorted(mults)
    n = len(mults)
    e = sum(mults) / n
    med = mults_sorted[n // 2]
    p_shrink = sum(1 for m in mults if m < 0) / n
    p_grow = sum(1 for m in mults if m > 0) / n
    label = f"{state[0]}(t={state[1]})"
    print(f"{label:>10} {n:>7} {e:>+10.4f} {med:>+10.4f} {p_shrink:>10.4f} {p_grow:>10.4f}")


# === Part 3: Overall Expected Drift ===
print("\n\n=== Part 3: Overall Expected Drift ===\n")

# Compute weighted average of log multipliers
all_mults = []
for mults in hop_log_multiplier.values():
    all_mults.extend(mults)

print(f"Total FMF hops analyzed: {len(all_mults)}")
print(f"Overall E[log2(F(x)/x)]: {sum(all_mults)/len(all_mults):+.6f}")
print(f"Median log2(F(x)/x): {sorted(all_mults)[len(all_mults)//2]:+.6f}")
print(f"P(shrink per hop): {sum(1 for m in all_mults if m < 0)/len(all_mults):.4f}")
print(f"P(grow per hop): {sum(1 for m in all_mults if m > 0)/len(all_mults):.4f}")


# === Part 4: Multi-hop drift ===
# Track cumulative log multiplier over chains
print("\n\n=== Part 4: Cumulative Drift Along FMF Chains ===\n")
print("For selected starting values, track cumulative log2(multiplier):\n")

def fmf_chain_with_drift(x_start, max_hops=200):
    """Returns list of (hop_num, x, state, cumul_log2)."""
    x = x_start
    cumul = 0.0
    chain = [(0, x, None, 0.0)]
    for hop in range(max_hops):
        if x == 1:
            break
        nxt, steps, fmf, case = fmf_hop(x)
        if nxt is None:
            break
        lm = log2(nxt / x) if nxt > 0 else 0
        cumul += lm
        chain.append((hop + 1, nxt, case, cumul))
        x = nxt
    return chain

for x_start in [27, 703, 6171, 7527, 9663]:
    chain = fmf_chain_with_drift(x_start)
    print(f"x={x_start} ({len(chain)-1} hops):")
    print(f"  {'hop':>4} {'x':>10} {'state':>10} {'cum_log2':>10} {'cum_mult':>12}")
    for i, (hop, x, state, cl) in enumerate(chain):
        if i == 0 or i == len(chain) - 1 or i % max(1, (len(chain)//10)) == 0:
            s_str = f"{state[0]}(t={state[1]})" if state else "start"
            print(f"  {hop:>4} {x:>10} {s_str:>10} {cl:>+10.3f} {2**cl:>12.6f}")
    max_cl = max(cl for _, _, _, cl in chain)
    min_cl = min(cl for _, _, _, cl in chain)
    print(f"  Peak growth: 2^{max_cl:.2f} = {2**max_cl:.2f}x. Final: 2^{chain[-1][3]:.2f}")
    print()


# === Part 5: The t-value distribution along chains ===
print("\n=== Part 5: Distribution of t-values Encountered in FMF Chains ===\n")
t_values_seen = Counter()
type_seen = Counter()
total_hops_counted = 0

for x_start in range(3, 50001, 2):
    x = x_start
    for hop in range(500):
        if x == 1:
            break
        nxt, steps, fmf, case = fmf_hop(x)
        if nxt is None:
            break
        if case:
            t_values_seen[case[1]] += 1
            type_seen[case[0]] += 1
            total_hops_counted += 1
        x = nxt

print(f"Total hops across all chains: {total_hops_counted}")
print(f"\nType distribution:")
for typ in sorted(type_seen):
    print(f"  Type {typ}: {type_seen[typ]} ({type_seen[typ]/total_hops_counted*100:.1f}%)")

print(f"\nt-value distribution (for Type B hops):")
total_b = sum(c for (t, c) in t_values_seen.items())
for t in sorted(t_values_seen):
    print(f"  t={t}: {t_values_seen[t]:>7} ({t_values_seen[t]/total_b*100:.1f}%)")


# === Part 6: The key theoretical computation ===
# For the Markov chain to prove drift, we need:
# E[log2(multiplier)] < 0 at stationarity
#
# From Type A: multiplier = 3(4k+1)+1 / (4k+1) / 2^v2 = (12k+4)/((4k+1)*2^v2)
#   = 4(3k+1)/((4k+1)*2^v2)
#   For random k, E[log2] = log2(3/4) + adjustment ≈ -0.415 + ...
#
# From Type B(t): multiplier = 3^(t+2)*m / (2^(t+2)*m) / 2^{v2-1} ≈ (3/2)^(t+2) / 2^{v2-1}
#   E[log2] = (t+2)*log2(3/2) - (v2-1) = 0.585(t+2) - E[v2] + 1
#
# With E[v2(FMF)] = 1 + E[v2(m - inv)] = 1 + 2 = 3 (geometric distribution)
# E[log2] for B(t) ≈ 0.585(t+2) - 3 + 1 = 0.585t + 1.17 - 2 = 0.585t - 0.83
#
# So for t=1: E ≈ -0.245 (shrinking)
#    for t=2: E ≈ +0.34 (growing!)
#    for t≥2: growing on average
#
# But most hops have t=0 or t=1, so the weighted average might still be negative.

print("\n\n=== Part 6: Theoretical E[log2(multiplier)] by state ===\n")
print("Using the formula: E[log2] ≈ 0.585(t+2) - E[v2(FMF)] + 1")
print("With E[v2(FMF)] ≈ 3 (geometric distribution):\n")
for t in range(0, 8):
    theoretical = 0.585 * (t + 2) - 3 + 1
    empirical_mults = hop_log_multiplier.get(('B', t), [])
    emp = sum(empirical_mults) / len(empirical_mults) if empirical_mults else None
    a_mults = hop_log_multiplier.get(('A', 0), [])
    print(f"  B(t={t}): theoretical ≈ {theoretical:+.3f}, "
          f"empirical = {emp:+.4f}" if emp else f"  B(t={t}): theoretical ≈ {theoretical:+.3f}, empirical = N/A")

a_mults = hop_log_multiplier.get(('A', 0), [])
if a_mults:
    print(f"  A(t=0): empirical = {sum(a_mults)/len(a_mults):+.4f}")

print(f"\n  Weighted overall: theoretical ≈ {sum(all_mults)/len(all_mults):+.6f}")
print(f"  (This uses the EMPIRICAL state distribution, not stationary.)")
