"""
explore57_start_counts.py

Verifies the start-count formulas for the binary return system and the
reduced binary {0,1} gap system.

For each displayed bound B and level L, the script compares:

    A_R(B,L) = sum_{|w|=L, R_w <= B} (floor((B - R_w) / Q_w) + 1)

and the equivalent terminal-coordinate formula using R_w = floor(U_w/E_w)
against a direct count of ordinary starts 0 <= n <= B that survive L binary
return blocks.  It also checks the sharp bridge

    N_R(B,L) <= A_R(B,L) <= N_R(B,L) + (B+1)(2/15)^L.

The gap side is identical, with starts 1 <= a <= B and density rate 1/112.
"""

from __future__ import annotations

from fractions import Fraction

from explore52_binary_partial_map import partial_gap_map, partial_return_map
from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_CASES = (
    (12, 1),
    (12, 2),
    (16, 3),
    (20, 4),
    (20, 5),
)

GAP_CASES = (
    (12, 1),
    (16, 2),
    (20, 3),
    (24, 3),
)

EXPECTED_RETURN_COUNTS = {
    (12, 1): (4095, 3, 546),
    (12, 2): (4095, 3, 72),
    (16, 3): (65535, 5, 153),
    (20, 4): (1048575, 15, 330),
    (20, 5): (1048575, 7, 43),
}

EXPECTED_GAP_COUNTS = {
    (12, 1): (4095, 2, 36),
    (16, 2): (65535, 1, 4),
    (20, 3): (1048575, 1, 1),
    (24, 3): (16777215, 6, 13),
}


def return_prefix_states(bound: int, level: int):
    states = [RETURN_EMPTY]
    for _ in range(level):
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        states = next_states
    return states


def gap_prefix_states(bound: int, level: int):
    states = [GAP_EMPTY]
    for _ in range(level):
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= bound:
                    next_states.append(candidate)
        states = next_states
    return states


def return_formula_count(bound: int, level: int) -> tuple[int, int]:
    states = return_prefix_states(bound, level)
    prefix_count = len(states)
    start_count = sum((bound - state.residue) // state.modulus + 1 for state in states)
    terminal_start_count = 0
    for state in states:
        terminal_coordinate = (state.auxiliary * state.modulus) // state.coefficient
        assert terminal_coordinate == state.residue
        terminal_start_count += (bound - terminal_coordinate) // state.modulus + 1
    assert terminal_start_count == start_count
    return prefix_count, start_count


def gap_formula_count(bound: int, level: int) -> tuple[int, int]:
    states = gap_prefix_states(bound, level)
    prefix_count = len(states)
    start_count = sum((bound - state.residue) // state.modulus + 1 for state in states)
    terminal_start_count = 0
    for state in states:
        normalized_num = state.auxiliary * state.modulus
        terminal_coordinate = (normalized_num + state.coefficient - 1) // state.coefficient
        assert terminal_coordinate == state.residue
        terminal_start_count += (bound - terminal_coordinate) // state.modulus + 1
    assert terminal_start_count == start_count
    return prefix_count, start_count


def direct_return_count(bound: int, level: int) -> int:
    total = 0
    for start in range(bound + 1):
        n = start
        survives = True
        for _ in range(level):
            step = partial_return_map(n)
            if step is None:
                survives = False
                break
            n = step.n_next
        if survives:
            total += 1
    return total


def direct_gap_count(bound: int, level: int) -> int:
    total = 0
    for start in range(1, bound + 1):
        a = start
        survives = True
        for _ in range(level):
            step = partial_gap_map(a)
            if step is None:
                survives = False
                break
            _, a = step
        if survives:
            total += 1
    return total


def verify_return_start_counts() -> None:
    rho = Fraction(2, 15)
    for bits, level in RETURN_CASES:
        bound = (1 << bits) - 1
        prefix_count, formula_count = return_formula_count(bound, level)
        direct_count = direct_return_count(bound, level)

        expected_bound, expected_prefixes, expected_starts = EXPECTED_RETURN_COUNTS[(bits, level)]
        assert bound == expected_bound
        assert prefix_count == expected_prefixes
        assert formula_count == expected_starts
        assert direct_count == formula_count
        assert prefix_count <= formula_count
        assert Fraction(formula_count - prefix_count, 1) <= (bound + 1) * rho**level

        print(
            f"return bits={bits:2d} level={level:2d} "
            f"prefixes={prefix_count:4d} starts={formula_count:6d}"
        )


def verify_gap_start_counts() -> None:
    rho = Fraction(1, 112)
    for bits, level in GAP_CASES:
        bound = (1 << bits) - 1
        prefix_count, formula_count = gap_formula_count(bound, level)
        direct_count = direct_gap_count(bound, level)

        expected_bound, expected_prefixes, expected_starts = EXPECTED_GAP_COUNTS[(bits, level)]
        assert bound == expected_bound
        assert prefix_count == expected_prefixes
        assert formula_count == expected_starts
        assert direct_count == formula_count
        assert prefix_count <= formula_count
        assert Fraction(formula_count - prefix_count, 1) <= bound * rho**level

        print(
            f"gap    bits={bits:2d} level={level:2d} "
            f"prefixes={prefix_count:4d} starts={formula_count:6d}"
        )


if __name__ == "__main__":
    verify_return_start_counts()
    verify_gap_start_counts()
