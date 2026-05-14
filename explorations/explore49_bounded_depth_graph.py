"""
explore49_bounded_depth_graph.py

Builds a finite-state over-approximation for growth-B continuation paths whose
depths are bounded by T.

State: (t, m mod 2^K), with t <= T and m odd. An edge exists if some lift of
the residue class gives one exact growth-B continuation with next depth t' <= T
and next odd parameter m' in the target residue class.

If this over-approximation is acyclic for some K, then no positive integer
growth-B continuation path with all depths <= T can exist. If cycles remain,
they may be real or spurious; increasing K refines the approximation.
"""

from __future__ import annotations

import argparse
from collections import defaultdict


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


State = tuple[int, int]


def build_graph(max_t: int, bits: int) -> dict[State, set[State]]:
    modulus = 1 << bits
    lift_modulus = 1 << (bits + max_t + 3)
    graph: dict[State, set[State]] = defaultdict(set)

    for t in range(max_t + 1):
        a = 3 ** (t + 2)
        for residue in range(1, modulus, 2):
            source = (t, residue)
            for lift in range(residue, lift_modulus, modulus):
                if (a * lift) % 8 != 7:
                    continue
                q = (a * lift + 1) // 8
                next_t = v2(q)
                if next_t > max_t:
                    continue
                next_m = q >> next_t
                graph[source].add((next_t, next_m % modulus))

    return graph


def cycle_nodes(graph: dict[State, set[State]]) -> set[State]:
    nodes = set(graph)
    for targets in graph.values():
        nodes.update(targets)

    index = 0
    stack: list[State] = []
    on_stack: set[State] = set()
    indices: dict[State, int] = {}
    lowlinks: dict[State, int] = {}
    cyclic: set[State] = set()

    def strongconnect(node: State) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for target in graph.get(node, ()):
            if target not in indices:
                strongconnect(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[target])

        if lowlinks[node] == indices[node]:
            component = []
            while True:
                item = stack.pop()
                on_stack.remove(item)
                component.append(item)
                if item == node:
                    break
            if len(component) > 1:
                cyclic.update(component)
            elif component[0] in graph.get(component[0], ()):
                cyclic.add(component[0])

    for node in sorted(nodes):
        if node not in indices:
            strongconnect(node)

    return cyclic


def summarize(max_t: int, max_bits: int) -> None:
    print(f"Bounded-depth graph over-approximation: T={max_t}")
    for bits in range(3, max_bits + 1):
        graph = build_graph(max_t, bits)
        nodes = {(t, r) for t in range(max_t + 1) for r in range(1, 1 << bits, 2)}
        edge_count = sum(len(targets) for targets in graph.values())
        cyclic = cycle_nodes(graph)
        print(
            f"K={bits:2d} nodes={len(nodes):6d} "
            f"edge_sources={len(graph):6d} edges={edge_count:7d} "
            f"cyclic_nodes={len(cyclic):6d}"
        )
        if not cyclic:
            print(f"  acyclic certificate found for T={max_t} at K={bits}")
            break
        sample = sorted(cyclic)[:8]
        print(f"  sample cyclic nodes: {sample}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Finite-state over-approximation for bounded-depth growth-B paths."
    )
    parser.add_argument("--max-t", type=int, default=1)
    parser.add_argument("--max-bits", type=int, default=12)
    args = parser.parse_args()
    summarize(args.max_t, args.max_bits)
