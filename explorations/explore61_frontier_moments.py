"""
explore61_frontier_moments.py

Diagnostic for the backward moment-contraction approach.

The immediate backward maps contract sufficiently high moments, but this does
not by itself give the finite-height rank bound.  This script measures the
cubic mass of low least-prefix residues:

    sum_{R_w <= B} R_w^3 / B^3
    sum_{S_w <= B} S_w^3 / B^3

over exact finite-height frontiers.  The normalized frontier cubic mass grows
in the displayed samples, so a successful proof needs an additional terminal
height/escape estimate, not just immediate moment contraction.
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


RETURN_CASES = (24, 32, 40, 48)
GAP_CASES = (24, 32, 40, 48, 56)

EXPECTED_RETURN_WORST = {
    24: (4, 37),
    32: (4, 134),
    40: (8, 537),
    48: (8, 3212),
}

EXPECTED_GAP_WORST = {
    24: (2, 12),
    32: (2, 28),
    40: (4, 76),
    48: (4, 296),
    56: (5, 865),
}


@dataclass(frozen=True)
class WorstMoment:
    level: int
    count: int
    ratio: Fraction


def worst_return_frontier_moment(bits: int) -> WorstMoment:
    bound = (1 << bits) - 1
    states = [RETURN_EMPTY]
    best = WorstMoment(0, 0, Fraction(0, 1))
    level = 0

    while True:
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return best
        states = next_states
        level += 1
        ratio = Fraction(sum(state.residue**3 for state in states), bound**3)
        if ratio > best.ratio:
            best = WorstMoment(level, len(states), ratio)


def worst_gap_frontier_moment(bits: int) -> WorstMoment:
    bound = (1 << bits) - 1
    states = [GAP_EMPTY]
    best = WorstMoment(0, 0, Fraction(0, 1))
    level = 0

    while True:
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return best
        states = next_states
        level += 1
        ratio = Fraction(sum(state.residue**3 for state in states), bound**3)
        if ratio > best.ratio:
            best = WorstMoment(level, len(states), ratio)


def verify_return_frontier_moments() -> None:
    for bits in RETURN_CASES:
        worst = worst_return_frontier_moment(bits)
        assert (worst.level, worst.count) == EXPECTED_RETURN_WORST[bits]
        print(
            f"return bits={bits:3d} level={worst.level:3d} "
            f"count={worst.count:5d} cubic={float(worst.ratio):.6f}"
        )


def verify_gap_frontier_moments() -> None:
    for bits in GAP_CASES:
        worst = worst_gap_frontier_moment(bits)
        assert (worst.level, worst.count) == EXPECTED_GAP_WORST[bits]
        print(
            f"gap    bits={bits:3d} level={worst.level:3d} "
            f"count={worst.count:5d} cubic={float(worst.ratio):.6f}"
        )


if __name__ == "__main__":
    verify_return_frontier_moments()
    verify_gap_frontier_moments()
