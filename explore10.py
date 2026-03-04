"""
explore10.py - Analyze FMF graph structure (text-based)

Each odd number is a node. An edge from a to b means: starting from a,
one FMF hop (find first multiple of 4, divide by LPT) leads to b.

This explores the structure: convergence funnels, hub nodes, tree depth, etc.
"""
from collections import defaultdict


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def fmf_hop(x):
    """One FMF hop: returns (next_odd, fmf_collatz_steps, fmf_value)."""
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        steps = 1
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            steps = 3
        else:
            t = v2(k + 1)
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            steps = 3 + 2 * t
    else:
        return None, 0, 0

    p = v2(fmf)
    return fmf >> p, steps + p, fmf


def fmf_trajectory(x_start, max_hops=200):
    """Full FMF trajectory to 1."""
    x = x_start
    traj = [x]
    for _ in range(max_hops):
        if x == 1:
            break
        nxt, _, _ = fmf_hop(x)
        if nxt is None:
            break
        traj.append(nxt)
        x = nxt
    return traj


# === Part 1: FMF Graph Structure ===
N = 500
edges = {}  # source -> target
in_degree = defaultdict(int)
out_targets = defaultdict(list)  # target -> list of sources (predecessors)

for x in range(1, N + 1, 2):
    nxt, steps, _ = fmf_hop(x)
    if nxt is not None:
        edges[x] = nxt
        in_degree[nxt] += 1
        out_targets[nxt].append(x)

print("=== FMF Graph Structure (odd numbers 1 to 500) ===\n")

# Hub nodes: highest in-degree (most numbers funnel into them)
hub_list = sorted(in_degree.items(), key=lambda x: -x[1])[:20]
print("Top 20 hub nodes (highest in-degree = most predecessors):")
print(f"  {'node':>6} {'in-deg':>7} {'mod4':>5} {'predecessors (sample)'}")
for node, deg in hub_list:
    preds = sorted(out_targets[node])[:8]
    preds_str = ", ".join(str(p) for p in preds)
    if len(out_targets[node]) > 8:
        preds_str += f", ... (+{len(out_targets[node])-8} more)"
    m4 = f"4k+{node%4}" if node > 1 else "1"
    print(f"  {node:>6} {deg:>7} {m4:>5}  <- [{preds_str}]")

# Leaf nodes: in-degree 0 (no predecessors within range)
leaves = [x for x in range(1, N + 1, 2) if x in edges and in_degree[x] == 0]
print(f"\nLeaf nodes (in-degree 0, no predecessor in [1,{N}]): {len(leaves)}")
print(f"  Examples: {leaves[:20]}")

# Count by class
n_4k1 = sum(1 for x in range(1, N+1, 2) if x % 4 == 1)
n_4k3 = sum(1 for x in range(1, N+1, 2) if x % 4 == 3)
leaves_4k1 = sum(1 for x in leaves if x % 4 == 1)
leaves_4k3 = sum(1 for x in leaves if x % 4 == 3)
print(f"  Leaves by class: {leaves_4k1} are 4k+1, {leaves_4k3} are 4k+3")
print(f"  Total nodes: {n_4k1} are 4k+1, {n_4k3} are 4k+3 (plus node 1)")


# === Part 2: Convergence Funnels ===
# Which numbers converge to the same node after 1 hop? After 2 hops?
print(f"\n\n=== Convergence Funnels ===\n")
print("Numbers that share the same FMF successor (converge after 1 hop):")
convergence_groups = defaultdict(list)
for x in range(3, N + 1, 2):
    nxt, _, _ = fmf_hop(x)
    if nxt is not None:
        convergence_groups[nxt].append(x)

big_groups = sorted(convergence_groups.items(), key=lambda x: -len(x[1]))[:10]
for target, sources in big_groups:
    print(f"  -> {target:>5}: {sources}")


# === Part 3: Trajectories as text ===
print(f"\n\n=== FMF Trajectories (odd milestones) ===\n")
test_nums = [27, 31, 63, 127, 255, 511, 703, 7527, 9663]
for n in test_nums:
    traj = fmf_trajectory(n)
    hops = len(traj) - 1

    # Show trajectory with mod4 classification
    parts = []
    for val in traj:
        m4 = val % 4
        tag = "A" if m4 == 1 else ("B" if m4 == 3 else "*")
        parts.append(f"{val}({tag})")

    traj_str = " -> ".join(parts[:25])
    if len(traj) > 25:
        traj_str += f" -> ... -> {traj[-1]}"

    print(f"x={n}: {hops} hops")
    print(f"  {traj_str}\n")


# === Part 4: Tree depth analysis ===
# For each node, how far is it from 1 in the FMF graph?
print(f"\n=== Distance to 1 (FMF hops) distribution ===\n")
depth_dist = defaultdict(int)
max_depth = 0
max_depth_num = 0
for x in range(3, 10001, 2):
    traj = fmf_trajectory(x)
    d = len(traj) - 1
    depth_dist[d] += 1
    if d > max_depth:
        max_depth = d
        max_depth_num = x

print(f"{'depth':>6} {'count':>7} {'cumul%':>8} {'bar'}")
total = sum(depth_dist.values())
cumul = 0
for d in sorted(depth_dist):
    cumul += depth_dist[d]
    bar = "#" * (depth_dist[d] // 10)
    print(f"  {d:>4} {depth_dist[d]:>7} {cumul/total*100:>7.1f}%  {bar}")

print(f"\nMax depth: {max_depth} hops (x={max_depth_num})")
print(f"Mean depth: {sum(d*c for d,c in depth_dist.items())/total:.2f}")


# === Part 5: "Release valve" pattern ===
# When a 4k+3 number produces a 4k+1 successor, that's a release valve
# (4k+1 always drops: 3(4k+1)+1 = 12k+4 = 4(3k+1), strong shrinkage)
print(f"\n\n=== Release Valve Analysis ===")
print("When FMF hop sends 4k+3 -> 4k+1, the next hop is always a 'release' (immediate /4)\n")

release_count = 0
non_release = 0
for x in range(3, 10001, 2):
    if x % 4 != 3:
        continue
    nxt, _, _ = fmf_hop(x)
    if nxt is not None:
        if nxt % 4 == 1:
            release_count += 1
        else:
            non_release += 1

total_3mod4 = release_count + non_release
print(f"4k+3 numbers in [3,10000]: {total_3mod4}")
print(f"  -> land on 4k+1 (release): {release_count} ({release_count/total_3mod4*100:.1f}%)")
print(f"  -> land on 4k+3 (continue): {non_release} ({non_release/total_3mod4*100:.1f}%)")


# === Part 6: Summary Statistics ===
print(f"\n\n=== Summary of FMF Framework ===")
print(f"{'Odd numbers tested':>25}: 3 to 10,000")

total_hops = 0
total_steps = 0
for x in range(3, 10001, 2):
    traj = fmf_trajectory(x)
    total_hops += len(traj) - 1
    steps = 0
    for j in range(len(traj) - 1):
        _, s, _ = fmf_hop(traj[j])
        steps += s
    total_steps += steps

n_tested = 5000
print(f"{'Average FMF hops to 1':>25}: {total_hops/n_tested:.2f}")
print(f"{'Average Collatz steps':>25}: {total_steps/n_tested:.2f}")
print(f"{'Compression ratio':>25}: {total_steps/total_hops:.2f} steps/hop")
print(f"\n{'Key Formulas':>25}:")
print(f"  FMF step:  3 + 2*v_2(k+1)  for x=4k+3")
print(f"  FMF value: 3^(t+2)*(k+1)/2^(t-1) - 2  where t=v_2(k+1)")
print(f"  v_2(FMF):  1 + v_2(m - (3^(t+2))^{{-1}})  where m=(k+1)/2^t")
print(f"  T_i(x):    3^i*(x+1)/2^i - 1  (chained odd-step operator)")
