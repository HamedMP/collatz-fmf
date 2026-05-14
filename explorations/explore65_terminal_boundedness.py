"""
explore65_terminal_boundedness.py

Finite verification of the terminal boundedness criteria.

For an ordinary start following a forced finite return or gap itinerary, the
rounded normalized terminal coordinate is the least prefix residue.  Once the
prefix modulus exceeds the start, that least residue must equal the start
itself.  This is the finite shadow of the paper's terminal boundedness
criterion for infinite words.
"""

from __future__ import annotations

from explore52_binary_partial_map import partial_gap_map, partial_return_map
from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return


RETURN_LIMIT = 50_000
RETURN_DEPTH = 7
GAP_LIMIT = 500_000
GAP_DEPTH = 4

EXPECTED_RETURN = (7_687, 20, 0, 6_667)
EXPECTED_GAP = (4_503, 8, 0, 4_465)


def return_terminal_coordinate(state) -> int:
    normalized_num = state.auxiliary * state.modulus
    coordinate = normalized_num // state.coefficient
    assert coordinate == state.residue
    return coordinate


def gap_terminal_coordinate(state) -> int:
    normalized_num = state.auxiliary * state.modulus
    coordinate = (normalized_num + state.coefficient - 1) // state.coefficient
    assert coordinate == state.residue
    return coordinate


def verify_return_terminal_boundedness(
    limit: int = RETURN_LIMIT,
    depth: int = RETURN_DEPTH,
) -> None:
    checked_prefixes = 0
    stabilized_prefixes = 0
    zero_increments = 0
    surviving_starts = 0

    for start in range(limit + 1):
        n = start
        state = RETURN_EMPTY
        survived = False
        previous_coordinate = None
        previous_modulus = None

        for _ in range(depth):
            step = partial_return_map(n)
            if step is None:
                break
            state = extend_return(state, step.ones)
            n = step.n_next
            survived = True
            checked_prefixes += 1

            coordinate = return_terminal_coordinate(state)
            assert start % state.modulus == coordinate
            if previous_coordinate is not None:
                assert coordinate >= previous_coordinate
                assert (coordinate - previous_coordinate) % previous_modulus == 0
                if coordinate == previous_coordinate:
                    zero_increments += 1
            if state.modulus > start:
                assert coordinate == start
                stabilized_prefixes += 1
            previous_coordinate = coordinate
            previous_modulus = state.modulus

        if survived:
            surviving_starts += 1

    if limit == RETURN_LIMIT and depth == RETURN_DEPTH:
        assert (
            checked_prefixes,
            stabilized_prefixes,
            zero_increments,
            surviving_starts,
        ) == EXPECTED_RETURN

    print(
        f"return boundedness checked: starts <= {limit}, depth <= {depth}, "
        f"prefixes={checked_prefixes}, stabilized={stabilized_prefixes}, "
        f"zero_increments={zero_increments}, survivors={surviving_starts}"
    )


def verify_gap_terminal_boundedness(
    limit: int = GAP_LIMIT,
    depth: int = GAP_DEPTH,
) -> None:
    checked_prefixes = 0
    stabilized_prefixes = 0
    zero_increments = 0
    surviving_starts = 0

    for start in range(1, limit + 1):
        a = start
        state = GAP_EMPTY
        survived = False
        previous_coordinate = None
        previous_modulus = None

        for _ in range(depth):
            step = partial_gap_map(a)
            if step is None:
                break
            gap, a = step
            state = extend_gap(state, gap)
            survived = True
            checked_prefixes += 1

            coordinate = gap_terminal_coordinate(state)
            assert start % state.modulus == coordinate
            if previous_coordinate is not None:
                assert coordinate >= previous_coordinate
                assert (coordinate - previous_coordinate) % previous_modulus == 0
                if coordinate == previous_coordinate:
                    zero_increments += 1
            if state.modulus > start:
                assert coordinate == start
                stabilized_prefixes += 1
            previous_coordinate = coordinate
            previous_modulus = state.modulus

        if survived:
            surviving_starts += 1

    if limit == GAP_LIMIT and depth == GAP_DEPTH:
        assert (
            checked_prefixes,
            stabilized_prefixes,
            zero_increments,
            surviving_starts,
        ) == EXPECTED_GAP

    print(
        f"gap    boundedness checked: starts <= {limit}, depth <= {depth}, "
        f"prefixes={checked_prefixes}, stabilized={stabilized_prefixes}, "
        f"zero_increments={zero_increments}, survivors={surviving_starts}"
    )


if __name__ == "__main__":
    verify_return_terminal_boundedness()
    verify_gap_terminal_boundedness()
