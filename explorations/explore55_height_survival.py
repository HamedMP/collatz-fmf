"""
explore55_height_survival.py

Computes exact fixed-height survival depths for the binary return system and
the reduced binary {0,1} gap system.

For a bound B, the reported depth is the largest L for which some length-L
prefix has least residue <= B.  Finite-height pruning from explore53 and
explore54 makes this exact for the displayed bounds.
"""

from __future__ import annotations

import argparse

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


def return_survival_depth(bound: int, max_depth: int = 200) -> tuple[int, list[int]]:
    states = [RETURN_EMPTY]
    frontier_sizes: list[int] = []

    for depth in range(max_depth):
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return depth, frontier_sizes
        frontier_sizes.append(len(next_states))
        states = next_states

    raise RuntimeError(f"return search reached max_depth={max_depth}")


def gap_survival_depth(bound: int, max_depth: int = 200) -> tuple[int, list[int]]:
    states = [GAP_EMPTY]
    frontier_sizes: list[int] = []

    for depth in range(max_depth):
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return depth, frontier_sizes
        frontier_sizes.append(len(next_states))
        states = next_states

    raise RuntimeError(f"gap search reached max_depth={max_depth}")


def verify_return_depths(max_bits: int = 52, step: int = 4) -> None:
    expected = {
        4: 1,
        8: 2,
        12: 4,
        16: 5,
        20: 6,
        24: 8,
        28: 9,
        32: 10,
        36: 12,
        40: 13,
        44: 15,
        48: 16,
        52: 18,
    }
    for bits in range(step, max_bits + 1, step):
        bound = (1 << bits) - 1
        depth, frontier = return_survival_depth(bound)
        if bits in expected:
            assert depth == expected[bits], (bits, depth)
        print(
            f"return bits={bits:3d} max_depth={depth:3d} "
            f"frontier_tail={frontier[-3:]}"
        )


def verify_gap_depths(max_bits: int = 64, step: int = 8) -> None:
    expected = {
        8: 1,
        16: 2,
        24: 3,
        32: 4,
        40: 6,
        48: 6,
        56: 8,
        64: 9,
    }
    for bits in range(step, max_bits + 1, step):
        bound = (1 << bits) - 1
        depth, frontier = gap_survival_depth(bound)
        if bits in expected:
            assert depth == expected[bits], (bits, depth)
        print(
            f"gap    bits={bits:3d} max_depth={depth:3d} "
            f"frontier_tail={frontier[-3:]}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--return-max-bits", type=int, default=52)
    parser.add_argument("--gap-max-bits", type=int, default=64)
    args = parser.parse_args()

    verify_return_depths(args.return_max_bits)
    verify_gap_depths(args.gap_max_bits)
