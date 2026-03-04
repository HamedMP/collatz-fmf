#!/usr/bin/env python3
"""
explore42.py -- Is the FMF map mod 2^K ERGODIC?

We build the transition graph of odd residues under the FMF map modulo 2^K
and test for strong connectivity, spectral gap, mixing time, and whether
individual deterministic orbits visit all states.
"""

import math
import time
from collections import defaultdict, deque

# ── utility functions ──────────────────────────────────────────────────

def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def fmf_hop(x):
    """Return the odd part of FMF(x) for odd x."""
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        return fmf >> v2(fmf)
    elif mod4 == 3:
        k = (x - 3) // 4
        t = v2(k + 1)
        m = (k + 1) >> t
        fmf_val = 2 * (3 ** (t + 2) * m - 1)
        return fmf_val >> v2(fmf_val)
    return None


# ── Part 1: Transition graph mod 2^K ──────────────────────────────────

def build_graph(K):
    """
    Build the FMF transition graph on odd residues mod 2^K.
    Returns (adj, nodes) where adj[u] = set of successors.
    """
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    adj = defaultdict(set)
    for r in nodes:
        img = fmf_hop(r) % mod
        adj[r].add(img)
    return adj, nodes


def tarjan_scc(adj, nodes):
    """Tarjan's SCC algorithm. Returns list of SCCs (each a list of nodes)."""
    index_counter = [0]
    stack = []
    on_stack = set()
    index = {}
    lowlink = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])
        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in nodes:
        if v not in index:
            strongconnect(v)
    return sccs


def tarjan_scc_iterative(adj, nodes):
    """Iterative Tarjan's SCC to avoid recursion-depth issues for large K."""
    index_counter = [0]
    stack = []
    on_stack = set()
    idx = {}
    lowlink = {}
    sccs = []

    for start in nodes:
        if start in idx:
            continue
        # DFS stack: (node, iterator_over_neighbours, is_first_visit)
        dfs = [(start, iter(adj.get(start, [])), True)]
        idx[start] = lowlink[start] = index_counter[0]
        index_counter[0] += 1
        stack.append(start)
        on_stack.add(start)

        while dfs:
            v, it, _ = dfs[-1]
            pushed = False
            for w in it:
                if w not in idx:
                    idx[w] = lowlink[w] = index_counter[0]
                    index_counter[0] += 1
                    stack.append(w)
                    on_stack.add(w)
                    dfs.append((w, iter(adj.get(w, [])), True))
                    pushed = True
                    break
                elif w in on_stack:
                    lowlink[v] = min(lowlink[v], idx[w])
            if not pushed:
                # finished v
                if lowlink[v] == idx[v]:
                    scc = []
                    while True:
                        w = stack.pop()
                        on_stack.discard(w)
                        scc.append(w)
                        if w == v:
                            break
                    sccs.append(scc)
                if len(dfs) > 1:
                    parent = dfs[-2][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[v])
                dfs.pop()
    return sccs


print("=" * 72)
print("PART 1: Transition graph of FMF map on odd residues mod 2^K")
print("=" * 72)
print()

part1_results = {}
for K in [4, 6, 8, 10, 12]:
    t0 = time.time()
    adj, nodes = build_graph(K)
    n_nodes = len(nodes)
    n_edges = sum(len(adj[v]) for v in nodes)

    if K <= 10:
        sccs = tarjan_scc_iterative(adj, nodes)
    else:
        sccs = tarjan_scc_iterative(adj, nodes)

    scc_sizes = sorted([len(s) for s in sccs], reverse=True)
    biggest = scc_sizes[0]
    elapsed = time.time() - t0

    part1_results[K] = {
        'nodes': n_nodes,
        'edges': n_edges,
        'n_scc': len(sccs),
        'biggest_scc': biggest,
        'scc_sizes': scc_sizes[:10],
    }
    strongly_connected = (len(sccs) == 1)
    pct = biggest / n_nodes * 100

    print(f"K={K:2d}  |  nodes={n_nodes:6d}  edges={n_edges:6d}  "
          f"SCCs={len(sccs):4d}  biggest={biggest:6d} ({pct:5.1f}%)  "
          f"strongly_connected={strongly_connected}  [{elapsed:.2f}s]")
    if len(scc_sizes) > 1:
        print(f"       SCC sizes (top 10): {scc_sizes[:10]}")

print()

# ── Part 2: Spectral gap of the transition matrix ────────────────────

def build_transition_matrix(K):
    """
    Build stochastic transition matrix as dict-of-dicts.
    M[i][j] = probability of going from state i to state j.
    (For FMF, each state has exactly 1 successor, so it's a permutation-like matrix.)
    """
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    node_idx = {r: i for i, r in enumerate(nodes)}
    n = len(nodes)
    # Build as list of lists for power iteration
    # But since each row has exactly 1 nonzero entry, store as a map
    successor = {}
    for r in nodes:
        img = fmf_hop(r) % mod
        successor[node_idx[r]] = node_idx[img]
    return n, successor, nodes, node_idx


def mat_vec_mult(successor, n, vec):
    """Multiply transition matrix by vector. M^T * vec (right eigenvector)."""
    result = [0.0] * n
    for i in range(n):
        j = successor[i]
        result[j] += vec[i]
    return result


def mat_T_vec_mult(successor, n, vec):
    """Multiply M * vec (each row i gets vec[successor[i]])."""
    result = [0.0] * n
    for i in range(n):
        result[i] = vec[successor[i]]
    return result


def power_iteration_second_eigenvalue(successor, n, max_iter=5000, tol=1e-12):
    """
    Find |lambda_2| via power iteration on M - (1/n)*J where J is all-ones.

    Since the leading eigenvector is uniform (1/n, ..., 1/n) with eigenvalue 1,
    we deflate: project out the uniform component at each step.
    """
    import random
    random.seed(42)
    # Start with a random vector orthogonal to uniform
    vec = [random.gauss(0, 1) for _ in range(n)]
    mean_v = sum(vec) / n
    vec = [v - mean_v for v in vec]
    norm = math.sqrt(sum(v * v for v in vec))
    if norm < 1e-30:
        return 0.0
    vec = [v / norm for v in vec]

    eigenval = 0.0
    for iteration in range(max_iter):
        # Apply M^T (since FMF is deterministic, M is a permutation-like matrix)
        new_vec = mat_T_vec_mult(successor, n, vec)
        # Project out uniform component
        mean_nv = sum(new_vec) / n
        new_vec = [v - mean_nv for v in new_vec]
        norm = math.sqrt(sum(v * v for v in new_vec))
        if norm < 1e-30:
            return 0.0
        new_eigenval = norm
        new_vec = [v / norm for v in new_vec]
        if abs(new_eigenval - eigenval) < tol:
            return new_eigenval
        eigenval = new_eigenval
        vec = new_vec
    return eigenval


print("=" * 72)
print("PART 2: Spectral gap of the FMF transition matrix mod 2^K")
print("=" * 72)
print()
print("Since each odd residue has exactly ONE successor under FMF mod 2^K,")
print("the transition matrix is a PERMUTATION MATRIX (deterministic map).")
print("Eigenvalues of a permutation matrix are roots of unity determined")
print("by the cycle structure. |lambda_2| = 1 unless the map is a single cycle.")
print()

for K in [4, 6, 8, 10]:
    t0 = time.time()
    n, successor, nodes, node_idx = build_transition_matrix(K)

    # Find cycle structure directly (more informative than power iteration)
    visited = [False] * n
    cycles = []
    for start in range(n):
        if visited[start]:
            continue
        path = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            path.append(cur)
            cur = successor[cur]
        # cur is now a node we've seen before; find the cycle
        if cur in path:
            idx = path.index(cur)
            cycle = path[idx:]
            cycles.append(len(cycle))

    cycles.sort(reverse=True)
    total_in_cycles = sum(cycles)

    # For a permutation, |lambda_2| = 1 unless there's a single cycle of length n.
    # The eigenvalues are all L-th roots of unity for each cycle of length L.
    # Spectral gap = 1 - |lambda_2|. For a single cycle of length n, lambda_2 = e^{2pi i/n},
    # so |lambda_2| = 1 and spectral gap = 0. BUT the spectral gap for MIXING is different:
    # it's 1 - Re(lambda_2) = 1 - cos(2pi/n) ~ 2pi^2/n^2.

    # Check if single cycle
    is_single_cycle = (len(cycles) == 1 and cycles[0] == n)

    # For the largest cycle of length L, the "worst" eigenvalue for mixing is
    # cos(2*pi/L) with gap ~ 2*pi^2/L^2
    if cycles:
        L = cycles[0]
        re_lambda2 = math.cos(2 * math.pi / L) if L > 1 else 0
        spectral_gap = 1 - re_lambda2
    else:
        spectral_gap = 0

    elapsed = time.time() - t0
    print(f"K={K:2d}  |  n={n:5d}  cycles={len(cycles):4d}  "
          f"largest_cycle={cycles[0] if cycles else 0}  "
          f"single_cycle={is_single_cycle}")
    print(f"       cycle lengths (top 5): {cycles[:5]}")
    print(f"       nodes in cycles: {total_in_cycles}/{n}  "
          f"spectral_gap(Re)={spectral_gap:.6e}  [{elapsed:.2f}s]")
    # Also compute gcd of cycle lengths
    if cycles:
        g = cycles[0]
        for c in cycles[1:]:
            g = math.gcd(g, c)
        print(f"       gcd of cycle lengths: {g}  "
              f"(aperiodic requires gcd=1)")
    print()

# But wait -- the FMF map mod 2^K might NOT be a permutation!
# Multiple odd residues could map to the same residue. Let's check.
print("--- Checking if FMF mod 2^K is a PERMUTATION (injective) ---")
print()
for K in [4, 6, 8, 10]:
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    images = [fmf_hop(r) % mod for r in nodes]
    unique_images = len(set(images))
    is_perm = (unique_images == len(nodes))
    # Check that all images are odd
    all_odd = all(img % 2 == 1 for img in images)
    print(f"K={K:2d}  |  nodes={len(nodes)}  unique_images={unique_images}  "
          f"injective={is_perm}  all_images_odd={all_odd}")
    if not is_perm:
        # Count in-degrees
        in_deg = defaultdict(int)
        for img in images:
            in_deg[img] += 1
        max_in = max(in_deg.values())
        zero_in = len(nodes) - len(in_deg)
        print(f"       max_in_degree={max_in}  nodes_with_0_in_degree={zero_in}")

print()


# ── Part 2b: Spectral analysis for NON-permutation case ─────────────

print("=" * 72)
print("PART 2b: Spectral gap via power iteration (handles non-permutation)")
print("=" * 72)
print()

for K in [4, 6, 8]:
    t0 = time.time()
    n, successor, nodes, node_idx = build_transition_matrix(K)
    lam2 = power_iteration_second_eigenvalue(successor, n, max_iter=10000)
    spectral_gap = 1.0 - lam2
    elapsed = time.time() - t0
    print(f"K={K:2d}  |  n={n:4d}  |lambda_2|={lam2:.8f}  "
          f"spectral_gap={spectral_gap:.8f}  [{elapsed:.2f}s]")

print()


# ── Part 3: Mixing time ──────────────────────────────────────────────

print("=" * 72)
print("PART 3: Mixing time — total variation distance to uniform")
print("=" * 72)
print()
print("Starting from each odd residue, iterate FMF mod 2^K and track the")
print("empirical distribution. Measure TV distance to uniform after t steps.")
print()

def tv_distance_to_uniform(visit_counts, n, total):
    """Total variation distance between empirical distribution and uniform."""
    uniform = total / n
    return 0.5 * sum(abs(visit_counts.get(i, 0) - uniform) for i in range(n)) / total


for K in [4, 6, 8, 10]:
    t0 = time.time()
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    node_set = set(nodes)
    n = len(nodes)
    node_idx = {r: i for i, r in enumerate(nodes)}

    max_steps = min(50 * n, 100000)
    check_points = [n, 2 * n, 5 * n, 10 * n, 20 * n, 50 * n]
    check_points = [c for c in check_points if c <= max_steps]

    worst_tv = {cp: 0.0 for cp in check_points}
    avg_tv = {cp: 0.0 for cp in check_points}

    for start in nodes:
        visit_counts = defaultdict(int)
        cur = start
        for step in range(1, max_steps + 1):
            cur = fmf_hop(cur) % mod
            visit_counts[node_idx[cur]] += 1
            if step in check_points:
                tv = tv_distance_to_uniform(visit_counts, n, step)
                if tv > worst_tv[step]:
                    worst_tv[step] = tv
                avg_tv[step] += tv

    for cp in check_points:
        avg_tv[cp] /= n

    elapsed = time.time() - t0
    print(f"K={K:2d}  |  n={n:4d}  max_steps={max_steps}  [{elapsed:.2f}s]")
    for cp in check_points:
        print(f"       t={cp:7d} ({cp/n:5.1f}n):  "
              f"worst_TV={worst_tv[cp]:.6f}  avg_TV={avg_tv[cp]:.6f}")
    print()


# ── Part 4: Can ergodicity close the gap? ────────────────────────────

print("=" * 72)
print("PART 4: Does ergodicity close the 'almost all -> all' gap?")
print("=" * 72)
print()

print("""ANALYSIS:

The FMF map mod 2^K is a DETERMINISTIC map on a finite state space.
Key observations:

1. GRAPH STRUCTURE: Each node has out-degree 1 (deterministic), but
   in-degree may vary. The map is NOT necessarily a permutation.

2. EVENTUAL PERIODICITY: Every orbit of a deterministic map on a finite
   set is eventually periodic: x, f(x), f^2(x), ..., enters a cycle.
   The orbit visits AT MOST n states (where n = 2^{K-1} odd residues).

3. ERGODICITY vs DETERMINISM: The ergodic theorem for Markov chains
   requires RANDOMNESS (or at minimum, the ability to transition to
   multiple states). A deterministic map gives a degenerate Markov chain
   where each row has a single 1. This chain is:
   - Irreducible IFF the map is a PERMUTATION and consists of a single cycle
   - Aperiodic IFF the cycle length is 1 (a fixed point)

   So standard Markov ergodic theory does NOT directly apply.

4. WHAT DOES WORK: If the map is a permutation with a single cycle,
   then the orbit of ANY starting point visits ALL states -- this is
   the discrete analogue of ergodicity for deterministic systems.
   This is called a "cyclic permutation" or "single-orbit" property.

5. KEY QUESTION: Is the FMF map mod 2^K a single-cycle permutation?
   If NOT a permutation: the map has attracting cycles, and some states
   are transient. Orbits from transient states converge to cycles but
   don't visit all states.

   If a permutation but MULTIPLE cycles: each orbit stays in its cycle
   and never visits states in other cycles.

   ONLY if it's a single-cycle permutation do all orbits visit all states.

6. FOR THE COLLATZ PROOF: Even if the map mod 2^K is NOT ergodic in the
   strict sense, the density result still has value:
   - The "Quartering Law" says growth-B chains have density (1/4)^k
   - This is a structural property of the residues, not a dynamical one
   - For any specific trajectory, the key question is whether it spends
     enough time in "favorable" residues (Type A or low-growth Type B)
   - If the orbit enters the big SCC, it visits a positive fraction of
     states, and the density result applies to those states
""")


# ── Part 5: Do all orbits visit all states? ──────────────────────────

print("=" * 72)
print("PART 5: Testing if all orbits visit all odd residues mod 2^K")
print("=" * 72)
print()

for K in [4, 6, 8, 10, 12]:
    t0 = time.time()
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    n = len(nodes)
    node_set = set(nodes)

    # For each starting node, find the cycle it enters and the set of states visited
    # (run for at most 2*n steps, which is enough to find the cycle)
    max_orbit_len = 3 * n

    all_visit_all = True
    min_visited = n
    max_visited = 0
    cycle_lengths = set()
    tail_lengths = []

    orbits_visiting_all = 0
    orbit_details = defaultdict(int)  # visited_count -> how many orbits

    for start in nodes:
        visited = set()
        visited_order = []
        cur = start
        for step in range(max_orbit_len):
            visited.add(cur)
            visited_order.append(cur)
            cur = fmf_hop(cur) % mod
            if cur in visited:
                break

        nv = len(visited)
        orbit_details[nv] += 1
        if nv < min_visited:
            min_visited = nv
        if nv > max_visited:
            max_visited = nv
        if nv == n:
            orbits_visiting_all += 1
        else:
            all_visit_all = False

        # Find the cycle: keep going until we return to cur
        cycle_start = cur
        cycle_len = 1
        c = fmf_hop(cur) % mod
        while c != cycle_start:
            c = fmf_hop(c) % mod
            cycle_len += 1
        cycle_lengths.add(cycle_len)

        # Tail length = steps before entering cycle
        tail = 0
        c = start
        in_cycle = set()
        cc = cycle_start
        for _ in range(cycle_len):
            in_cycle.add(cc)
            cc = fmf_hop(cc) % mod
        while c not in in_cycle:
            c = fmf_hop(c) % mod
            tail += 1
        tail_lengths.append(tail)

    elapsed = time.time() - t0
    print(f"K={K:2d}  |  n={n:5d}  all_visit_all={all_visit_all}  "
          f"orbits_visiting_all={orbits_visiting_all}/{n}")
    print(f"       min_visited={min_visited}  max_visited={max_visited}  "
          f"({max_visited/n*100:.1f}%)")
    print(f"       distinct cycle lengths: {sorted(cycle_lengths)}")
    avg_tail = sum(tail_lengths) / len(tail_lengths) if tail_lengths else 0
    max_tail = max(tail_lengths) if tail_lengths else 0
    print(f"       tail: avg={avg_tail:.1f}  max={max_tail}")

    if len(orbit_details) <= 20:
        print(f"       orbit coverage distribution: ", end="")
        for nv in sorted(orbit_details.keys()):
            print(f"  {nv}states:{orbit_details[nv]}orbits", end="")
        print()
    else:
        # Summarize
        print(f"       orbit coverage: {len(orbit_details)} distinct values")
        top5 = sorted(orbit_details.items(), key=lambda x: -x[1])[:5]
        print(f"       most common: {top5}")
    print()


# ── Part 6: Refined analysis — what fraction of states does the ──────
#    attracting set cover?

print("=" * 72)
print("PART 6: Attracting set analysis — the eventual image")
print("=" * 72)
print()
print("The 'eventual image' of a deterministic map f is the set of states")
print("that are visited infinitely often (i.e., the union of all cycles).")
print("If this set covers a large fraction of odd residues, the density")
print("result still applies to long trajectories.")
print()

for K in [4, 6, 8, 10, 12]:
    t0 = time.time()
    mod = 1 << K
    nodes = [r for r in range(1, mod, 2)]
    n = len(nodes)

    # Find the eventual image: iterate f^n for all starting points
    # The eventual image = union of all cycles
    # Efficient: compute f^n(x) for large enough n, then find the cycle
    in_cycles = set()

    for start in nodes:
        # Floyd's cycle detection
        slow = start
        fast = start
        for _ in range(2 * n):
            slow = fmf_hop(slow) % mod
            fast = fmf_hop(fmf_hop(fast) % mod) % mod
            if slow == fast:
                break
        # Now slow is in the cycle; traverse it
        cur = slow
        while True:
            in_cycles.add(cur)
            cur = fmf_hop(cur) % mod
            if cur == slow:
                break

    coverage = len(in_cycles) / n * 100
    elapsed = time.time() - t0
    print(f"K={K:2d}  |  n={n:5d}  states_in_cycles={len(in_cycles):5d}  "
          f"coverage={coverage:.1f}%  [{elapsed:.2f}s]")

    # How many distinct cycles?
    remaining = set(in_cycles)
    num_cycles = 0
    cycle_list = []
    while remaining:
        start = min(remaining)
        cycle = []
        cur = start
        while True:
            cycle.append(cur)
            remaining.discard(cur)
            cur = fmf_hop(cur) % mod
            if cur == start:
                break
        num_cycles += 1
        cycle_list.append(len(cycle))
    cycle_list.sort(reverse=True)
    print(f"       num_cycles={num_cycles}  "
          f"cycle_lengths={cycle_list[:10]}{'...' if len(cycle_list) > 10 else ''}")

print()


# ── Part 7: The real test — does the ACTUAL trajectory of a large ────
#    number show ergodic-like behavior?

print("=" * 72)
print("PART 7: Actual trajectory analysis for large odd numbers")
print("=" * 72)
print()
print("For specific large odd numbers, run the FMF trajectory and check")
print("the distribution of residues mod 2^K along the trajectory.")
print()

test_numbers = [
    2**32 + 1,
    2**48 - 1,
    3**30 + 2,
    7**15,
    2**64 + 27,
    999999999999999989,  # a large prime-ish number
]

# Make them odd
test_numbers = [x | 1 for x in test_numbers]

for K in [4, 6, 8]:
    mod = 1 << K
    n_residues = mod // 2  # number of odd residues
    print(f"--- K={K}, mod=2^{K}={mod}, {n_residues} odd residues ---")

    for x0 in test_numbers:
        cur = x0
        steps = min(200 * n_residues, 50000)
        residue_counts = defaultdict(int)
        for step in range(steps):
            r = cur % mod
            residue_counts[r] += 1
            cur = fmf_hop(cur)
            if cur == 1:
                break

        n_visited = len(residue_counts)
        total = sum(residue_counts.values())
        # TV distance to uniform
        uniform = total / n_residues
        tv = 0.5 * sum(abs(residue_counts.get(r, 0) - uniform)
                       for r in range(1, mod, 2)) / total
        print(f"  x0={x0:>24d}  steps={total:6d}  "
              f"residues_hit={n_visited}/{n_residues}  TV={tv:.4f}")

    print()


# ── SUMMARY ──────────────────────────────────────────────────────────

print("=" * 72)
print("SUMMARY OF FINDINGS")
print("=" * 72)
print()
print("""
KEY FINDINGS:

1. GRAPH STRUCTURE: The FMF map mod 2^K is a deterministic map (out-degree
   1 for every node) that is decisively NOT injective. At K=8, 128 nodes
   map to only 64 distinct images (50% collapse). At K=10, 512 nodes
   map to 250 images (49%). Roughly half the state space has in-degree 0
   (transient) and the other half absorbs multiple predecessors.

2. STRONG CONNECTIVITY: NONE. The graph is almost entirely acyclic.
   Every SCC has size 1 (trivially, a single node) except for rare small
   cycles (a 6-cycle at K=8, a 2-cycle at K=10). The graph is a
   collection of trees feeding into tiny attracting cycles, not a rich
   interconnected structure.

3. ATTRACTING SET IS TINY: The eventual image (union of all cycles)
   covers a vanishing fraction of the state space:
     K=4: 1/8 (12.5%), K=6: 1/32 (3.1%), K=8: 7/128 (5.5%),
     K=10: 3/512 (0.6%), K=12: 1/2048 (~0.05%).
   Typically there is just a single fixed point (residue 1 maps to 1)
   plus occasionally a small cycle. The coverage SHRINKS as K grows.

4. ORBIT COVERAGE IS LOW: No orbit visits all states. The maximum number
   of distinct residues visited by any orbit (tail + cycle) is:
     K=4: 5/8, K=6: 11/32, K=8: 12/128, K=10: 27/512, K=12: 32/2048.
   Coverage fraction DECREASES with K (~O(K/2^K) scaling).

5. MIXING DOES NOT OCCUR mod 2^K: The TV distance from the empirical
   distribution to uniform remains near 1.0 even after 50n steps:
     K=4: worst_TV=0.875, K=6: 0.969, K=8: 0.992, K=10: 0.998.
   This is getting WORSE with K, not better. The orbit concentrates on
   its tiny cycle, not spreading over the state space.

6. ACTUAL TRAJECTORIES BEHAVE DIFFERENTLY: When we run FMF on actual
   large numbers (not residues), the trajectory DOES visit many distinct
   residues mod 2^K (e.g., 8/8 at K=4, 30/32 at K=6). This is because
   the ACTUAL trajectory changes its high bits at every step, so it
   effectively samples different branches of the mod-2^K tree. The
   deterministic orbit mod 2^K is misleading because it discards the
   high-bit information that drives equidistribution.

7. ERGODICITY VERDICT: DEFINITIVELY NO.
   The FMF map mod 2^K is:
   - Not injective (not a permutation)
   - Not strongly connected (almost all SCCs are singletons)
   - Has a vanishing attracting set (coverage -> 0 as K -> infinity)
   - Has no mixing (TV distance -> 1)
   ERGODICITY OF THE MOD-2^K MAP CANNOT CLOSE THE GAP.

8. WHY THE GAP MIGHT STILL CLOSE (alternative approaches):
   (a) MULTI-SCALE / CHANGING-MODULUS ARGUMENT: The actual trajectory
       is not confined to one residue class. As the number changes, its
       residue mod 2^K shifts unpredictably. The equidistribution comes
       from the NUMBER CHANGING, not from the map being ergodic at a
       fixed modulus. Part 7 confirms this: actual trajectories hit
       nearly all residues mod 2^K.
   (b) EFFECTIVE INDEPENDENCE: If consecutive FMF outputs have residues
       that are effectively independent (because the high bits scramble
       the low bits), then the Quartering Law density applies to time
       averages by a law-of-large-numbers argument, without needing
       formal ergodicity of any fixed-modulus map.
   (c) TREE STRUCTURE ARGUMENT: The mod-2^K map is a collection of trees
       flowing into a tiny attractor. But at DIFFERENT scales K, the tree
       structure changes. A number's trajectory passes through all scales,
       so it sees different "trees" at each step.
""")
