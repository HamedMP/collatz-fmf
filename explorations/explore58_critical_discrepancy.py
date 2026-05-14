"""
explore58_critical_discrepancy.py

Scans the finite-height counting discrepancy over all critical heights up to a
chosen bound.

For fixed L, the prefix count N(B,L) is a nondecreasing step function of B.
Therefore the normalized ratios

    N_R(B,L) / ((B+1) (2/15)^L)
    N_G(B,L) / (B (1/112)^L)

can only attain a maximum at a height B equal to a realized least prefix
residue.  This script enumerates the exact prefix frontiers up to a height
bound and checks those critical heights directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_CASES = (24, 32, 40, 48, 52, 56)
GAP_CASES = (24, 32, 40, 48, 56, 64, 72)

EXPECTED_RETURN_WORST = {
    24: (6, 262143, 2),
    32: (10, 391188479, 1),
    40: (11, 8589934591, 3),
    48: (16, 67477744910335, 3),
    52: (16, 67477744910335, 3),
    56: (16, 67477744910335, 3),
}

EXPECTED_GAP_WORST = {
    24: (3, 1565883, 4),
    32: (4, 32679099, 2),
    40: (4, 32679099, 2),
    48: (4, 32679099, 2),
    56: (4, 32679099, 2),
    64: (4, 32679099, 2),
    72: (4, 32679099, 2),
}


@dataclass(frozen=True)
class Worst:
    level: int
    height: int
    count: int
    ratio: Fraction


def return_frontiers(bound: int, max_depth: int = 200) -> list[list[int]]:
    states = [RETURN_EMPTY]
    frontiers: list[list[int]] = []

    for _ in range(max_depth):
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return frontiers
        frontiers.append(sorted(state.residue for state in next_states))
        states = next_states

    raise RuntimeError(f"return search reached max_depth={max_depth}")


def gap_frontiers(bound: int, max_depth: int = 200) -> list[list[int]]:
    states = [GAP_EMPTY]
    frontiers: list[list[int]] = []

    for _ in range(max_depth):
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return frontiers
        frontiers.append(sorted(state.residue for state in next_states))
        states = next_states

    raise RuntimeError(f"gap search reached max_depth={max_depth}")


def worst_return_critical(bits: int) -> Worst:
    bound = (1 << bits) - 1
    rho = Fraction(2, 15)
    best = Worst(0, 0, 0, Fraction(0, 1))

    for level, residues in enumerate(return_frontiers(bound), start=1):
        for index, residue in enumerate(residues, start=1):
            ratio = Fraction(index, 1) / ((residue + 1) * rho**level)
            if ratio > best.ratio:
                best = Worst(level, residue, index, ratio)

    return best


def worst_gap_critical(bits: int) -> Worst:
    bound = (1 << bits) - 1
    rho = Fraction(1, 112)
    best = Worst(0, 0, 0, Fraction(0, 1))

    for level, residues in enumerate(gap_frontiers(bound), start=1):
        for index, residue in enumerate(residues, start=1):
            ratio = Fraction(index, 1) / (residue * rho**level)
            if ratio > best.ratio:
                best = Worst(level, residue, index, ratio)

    return best


def verify_return_critical_discrepancy() -> None:
    for bits in RETURN_CASES:
        worst = worst_return_critical(bits)
        expected = EXPECTED_RETURN_WORST[bits]
        assert (worst.level, worst.height, worst.count) == expected, worst
        print(
            f"return bits={bits:3d} level={worst.level:3d} "
            f"height={worst.height:17d} count={worst.count:5d} "
            f"critical={float(worst.ratio):.6f}"
        )


def verify_gap_critical_discrepancy() -> None:
    for bits in GAP_CASES:
        worst = worst_gap_critical(bits)
        expected = EXPECTED_GAP_WORST[bits]
        assert (worst.level, worst.height, worst.count) == expected, worst
        print(
            f"gap    bits={bits:3d} level={worst.level:3d} "
            f"height={worst.height:17d} count={worst.count:5d} "
            f"critical={float(worst.ratio):.6f}"
        )


if __name__ == "__main__":
    verify_return_critical_discrepancy()
    verify_gap_critical_discrepancy()
