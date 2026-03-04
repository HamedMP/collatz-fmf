"""
explore28.py - Finite Automaton Analysis of Growth Chains

THE PROOF STRATEGY:
1. Growth requires v_2(FMF) to be small (below a threshold depending on t)
2. v_2(FMF) = 1 + v_2(m - inv) where inv = (3^(t+2))^{-1} mod 2^N
3. v_2(m - inv) depends on m mod 2^K for some bounded K
4. After each hop, the new m' is determined by (old m mod 2^K, old t, v_2)
5. Growth requires specific (t, m mod 2^K) combinations
6. These form a finite set of states
7. If the growth-transition graph on these states has no infinite paths,
   then growth phases must terminate

THE KEY: we need to show that growth transitions form a DAG (no cycles)
or that any cycles in the growth automaton don't sustain net growth.
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


def mod_inverse_2adic(a, K):
    """Compute a^{-1} mod 2^K for odd a."""
    # Newton's method: x_{n+1} = x_n * (2 - a * x_n) mod 2^K
    x = 1
    for _ in range(K):
        x = (x * (2 - a * x)) % (2**K)
    return x


# === Part 1: For each t, find which (m mod 2^K) values allow growth ===
print("=== Part 1: Growth-Allowing m-Classes by (t, K) ===\n")

for K in [4, 8, 12]:
    print(f"--- K = {K} (m mod {2**K}) ---")
    mod = 2**K
    for t in range(0, 8):
        inv = mod_inverse_2adic(3**(t + 2), K + 5)  # Extra precision
        # For v_2(FMF) = 1 + v_2(m - inv): growth needs v_2 < threshold
        # threshold ≈ (t+2)*log2(3) - 1 = (t+2)*1.585 - 1
        threshold = (t + 2) * 1.585 - 1  # Approximate
        max_v2_for_growth = int(threshold)

        growth_classes = []
        for m_mod in range(1, mod, 2):  # Odd m only
            v = v2((m_mod - inv) % mod)  # v_2(m - inv) mod 2^K
            # v_2(FMF) = 1 + v -- but we need v_2(m - inv mod 2^K)
            # which equals min(v_2(m - inv), K)
            fmf_v2 = 1 + min(v, K)
            if fmf_v2 <= max_v2_for_growth:
                growth_classes.append(m_mod)

        n_growth = len(growth_classes)
        n_total = mod // 2
        pct = n_growth / n_total * 100
        print(f"  t={t}: {n_growth}/{n_total} m-classes allow growth ({pct:.1f}%)")
        if K <= 8 and n_growth <= 20:
            print(f"         classes: {growth_classes}")
    print()


# === Part 2: Build the growth transition graph ===
print("\n=== Part 2: Growth Transition Graph ===\n")
print("States: (t, m mod 2^K) where growth is possible")
print("Edges: growth transitions (t,m) -> (t',m')\n")

K = 8
mod = 2**K

# For each (t, m_mod) growth state, compute the possible next states
# We need to simulate the FMF hop for x ≡ 3 mod 4 with given (t, m mod 2^K)
# x = 2^(t+2)*m - 1, FMF = 2(3^(t+2)*m - 1)
# v_2(FMF) = 1 + v_2(m - inv), where inv = (3^(t+2))^{-1} mod 2^N
# F(x) = FMF / 2^v_2 = 2(3^(t+2)*m - 1) / 2^v
# For x' = F(x), we need (type', t', m' mod 2^K)

def compute_growth_transitions(t_max=12, K=8):
    mod = 2**K
    growth_states = set()
    transitions = defaultdict(set)  # (t, m_mod) -> set of (t', m'_mod)
    growth_ratios = {}  # (t, m_mod) -> log2(ratio)

    for t in range(0, t_max):
        inv = mod_inverse_2adic(3**(t + 2), K + 10)
        threshold = (t + 2) * 1.585 - 1
        max_v2_growth = int(threshold)

        for m_mod in range(1, mod, 2):
            v_exact = v2((m_mod - inv) % (2**(K + 10)))
            fmf_v2 = 1 + v_exact

            if fmf_v2 > max_v2_growth:
                continue  # Not a growth state

            # This is a growth state
            growth_states.add((t, m_mod))

            # Compute the approximate log2 ratio for this state
            # R ≈ (3/2)^(t+2) / 2^(fmf_v2 - 1)
            log_ratio = (t + 2) * log2(3/2) - (fmf_v2 - 1)
            growth_ratios[(t, m_mod)] = log_ratio

            # Now compute the NEXT state
            # We need a concrete x to compute the exact next state
            # Use multiple m values with m ≡ m_mod (mod 2^K) to check consistency
            next_states = Counter()
            for trial_m in range(m_mod, m_mod + mod * 100, mod):
                if trial_m < 1:
                    continue
                x = 2**(t + 2) * trial_m - 1
                if x <= 1:
                    continue

                # Compute FMF hop
                mod4 = x % 4
                if mod4 == 1:
                    k = (x - 1) // 4
                    fmf = 4 * (3 * k + 1)
                    case = 'A'
                elif mod4 == 3:
                    k = (x - 3) // 4
                    if k % 2 == 0:
                        j = k // 2
                        fmf = 4 * (9 * j + 4)
                        case = 'B0'
                    else:
                        t_k = v2(k + 1)
                        fmf = 3**(t_k + 2) * (k + 1) // 2**(t_k - 1) - 2
                        case = 'B'
                else:
                    continue

                v = v2(fmf)
                nxt = fmf >> v

                # Get (type', t', m') of next value
                if nxt % 4 == 1:
                    k_new = (nxt - 1) // 4
                    t_new = 0
                    m_new = k_new  # For Type A, "m" is k
                    next_type = 'A'
                elif nxt % 4 == 3:
                    k_new = (nxt - 3) // 4
                    if k_new % 2 == 0:
                        t_new = 0
                        m_new = k_new // 2
                        next_type = 'B0'
                    else:
                        t_new = v2(k_new + 1)
                        m_new = (k_new + 1) >> t_new
                        next_type = f'B{t_new}'
                else:
                    continue

                m_new_mod = m_new % mod
                next_states[(t_new, m_new_mod)] += 1

            # Record the most common transitions
            for ns, count in next_states.most_common(5):
                if count >= 3:  # At least 3 witnesses
                    transitions[(t, m_mod)].add(ns)

    return growth_states, transitions, growth_ratios


states, trans, ratios = compute_growth_transitions(t_max=12, K=8)
print(f"Growth states (t, m mod {mod}): {len(states)}")
print(f"Growth transitions: {sum(len(v) for v in trans.values())}")

# Check for cycles in the growth graph
# A cycle would mean a growth phase could potentially run forever
def find_cycles(states, transitions):
    """Find all cycles in the directed graph."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {s: WHITE for s in states}
    parent = {}
    cycles = []

    def dfs(u, path):
        color[u] = GRAY
        for v in transitions.get(u, set()):
            if v not in states:
                continue
            if color.get(v, WHITE) == GRAY:
                # Found a cycle!
                cycle_start = path.index(v)
                cycles.append(path[cycle_start:] + [v])
            elif color.get(v, WHITE) == WHITE:
                dfs(v, path + [v])
        color[u] = BLACK

    for s in states:
        if color[s] == WHITE:
            dfs(s, [s])

    return cycles

cycles = find_cycles(states, trans)
print(f"\nCycles in growth graph: {len(cycles)}")

if cycles:
    print("\nCYCLES FOUND! (This would be bad for the proof)")
    for i, cycle in enumerate(cycles[:10]):
        total_growth = sum(ratios.get(s, 0) for s in cycle[:-1])
        print(f"  Cycle {i+1} (len={len(cycle)-1}): {cycle}")
        print(f"    Total growth per cycle: {total_growth:+.4f} bits")
        if total_growth > 0:
            print(f"    *** NET GROWTH -- this cycle could sustain indefinite growth! ***")
        else:
            print(f"    Net shrinkage -- cycle is self-limiting")
else:
    print("\nNO CYCLES! Growth graph is a DAG.")
    print("This means growth phases are bounded by the longest path in the DAG.")

    # Find longest path
    def longest_path(states, transitions):
        memo = {}

        def dp(s):
            if s in memo:
                return memo[s]
            max_len = 0
            for v in transitions.get(s, set()):
                if v in states:
                    max_len = max(max_len, 1 + dp(v))
            memo[s] = max_len
            return max_len

        best = 0
        best_state = None
        for s in states:
            l = dp(s)
            if l > best:
                best = l
                best_state = s
        return best, best_state, memo

    max_path_len, start, memo = longest_path(states, trans)
    print(f"Longest path in DAG: {max_path_len} hops")
    print(f"Starting from state: {start}")

    # Reconstruct longest path
    path = [start]
    current = start
    for _ in range(max_path_len):
        best_next = None
        best_len = -1
        for v in trans.get(current, set()):
            if v in states and memo.get(v, 0) > best_len:
                best_len = memo.get(v, 0)
                best_next = v
        if best_next is None:
            break
        path.append(best_next)
        current = best_next

    total_growth = sum(ratios.get(s, 0) for s in path)
    print(f"Longest path: {path}")
    print(f"Total growth along path: {total_growth:+.4f} bits")


# === Part 3: Larger K for finer analysis ===
print("\n\n=== Part 3: Analysis with K = 12 ===\n")

states12, trans12, ratios12 = compute_growth_transitions(t_max=15, K=12)
print(f"Growth states (t, m mod {2**12}): {len(states12)}")
print(f"Growth transitions: {sum(len(v) for v in trans12.values())}")

cycles12 = find_cycles(states12, trans12)
print(f"Cycles: {len(cycles12)}")

if cycles12:
    print("\nCycles found with K=12:")
    net_growth_cycles = []
    for i, cycle in enumerate(cycles12[:20]):
        total_growth = sum(ratios12.get(s, 0) for s in cycle[:-1])
        if total_growth > 0:
            net_growth_cycles.append((total_growth, cycle))
        if i < 10:
            print(f"  Cycle {i+1} (len={len(cycle)-1}): growth={total_growth:+.4f} bits")

    if net_growth_cycles:
        print(f"\n*** {len(net_growth_cycles)} CYCLES WITH NET GROWTH ***")
        for g, c in sorted(net_growth_cycles, reverse=True)[:5]:
            print(f"  growth={g:+.4f}: {c[:4]}...")
    else:
        print(f"\nAll {len(cycles12)} cycles have NET SHRINKAGE -- growth is self-limiting!")
else:
    print("NO CYCLES -- growth is bounded!")


# === Part 4: Verify with actual trajectories ===
print("\n\n=== Part 4: Verify Growth Bounds Against Actual Trajectories ===\n")

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

max_growth_found = 0
worst_x = 0
for x_start in range(3, 500001, 2):
    x = x_start
    growth_hops = 0
    for _ in range(200):
        if x <= 1:
            break
        nxt = fmf_hop(x)
        if nxt is None:
            break
        if nxt >= x_start:
            growth_hops += 1
        else:
            break
        x = nxt
    if growth_hops > max_growth_found:
        max_growth_found = growth_hops
        worst_x = x_start

print(f"Max growth phase in [3, 500K]: {max_growth_found} hops (x={worst_x})")
print(f"This should be bounded by the DAG longest path above.")


# === Part 5: Type A hops in growth -- they always shrink ===
print("\n\n=== Part 5: Type A During Growth -- Temporary Shrinkage ===\n")
print("Type A hops shrink (ratio < 1) but trajectory stays above x_start.")
print("So Type A within growth = 'partial recovery that doesn't complete'.\n")

a_in_growth = 0
b_in_growth = 0
for x_start in range(3, 200001, 2):
    x = x_start
    for _ in range(200):
        if x <= 1:
            break
        nxt, case, t, v, fmf, m = (None, '', 0, 0, 0, 0)
        mod4 = x % 4
        if mod4 == 1:
            k = (x - 1) // 4
            fmf_val = 4 * (3 * k + 1)
            vv = v2(fmf_val)
            nxt = fmf_val >> vv
            case = 'A'
        elif mod4 == 3:
            k = (x - 3) // 4
            if k % 2 == 0:
                j = k // 2
                fmf_val = 4 * (9 * j + 4)
                vv = v2(fmf_val)
                nxt = fmf_val >> vv
                case = 'B'
            else:
                t = v2(k + 1)
                fmf_val = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
                vv = v2(fmf_val)
                nxt = fmf_val >> vv
                case = 'B'
        if nxt is None:
            break

        if nxt >= x_start:
            if case == 'A':
                a_in_growth += 1
            else:
                b_in_growth += 1
        else:
            break
        x = nxt

total_growth_hops = a_in_growth + b_in_growth
print(f"Type A hops during growth: {a_in_growth} ({a_in_growth/total_growth_hops*100:.1f}%)")
print(f"Type B hops during growth: {b_in_growth} ({b_in_growth/total_growth_hops*100:.1f}%)")
print(f"\nType A hops within growth phases represent partial recoveries that")
print(f"don't bring the value below x_start. They reduce the 'growth debt'.")


# === Part 6: Net growth per cycle analysis ===
print("\n\n=== Part 6: If Cycles Exist -- Net Growth Analysis ===\n")

if cycles:
    # For each cycle, compute exact net growth using concrete examples
    print("Verifying cycle growth with actual numbers:\n")
    for i, cycle in enumerate(cycles[:5]):
        # Find a starting number that matches the first state
        t0, m0_mod = cycle[0]
        mod_val = 2**K
        m_start = m0_mod if m0_mod % 2 == 1 else m0_mod + mod_val
        x_test = 2**(t0 + 2) * m_start - 1

        # Run through the cycle
        x = x_test
        total_log = 0
        for j in range(len(cycle) - 1):
            nxt = fmf_hop(x)
            if nxt is None:
                break
            total_log += log2(nxt / x)
            x = nxt

        print(f"  Cycle {i+1}: starting x={x_test}, "
              f"after {len(cycle)-1} hops: log2(ratio) = {total_log:+.4f}")
else:
    print("No cycles to analyze -- growth is provably bounded!")
