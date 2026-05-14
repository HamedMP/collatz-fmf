"""
explore53_gap_minima.py

Certifies least prefix residues in the reduced binary {0,1} gap system.

The key pruning rule is exact.  If a length-L gap prefix has least residue
S_L < B, then every earlier least residue is also < B by monotonicity.  For a
current prefix composition

    H_i a_i = A_i a_0 - C_i,

any extension with starting value a_0 < B has intermediate state
a_i < A_i B / H_i.  If the next gap is k, then 8^k <= a_i, so necessarily
8^k H_i < A_i B.  A bound B therefore reduces the search for prefixes below
B to a finite tree.

Using the all-zero length-L prefix as B gives a certificate for the global
minimum at that length: either a smaller prefix is found inside the finite
tree, or the all-zero prefix is minimal.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from explore52_binary_partial_map import gap_prefix_code


@dataclass(frozen=True)
class GapState:
    word: tuple[int, ...]
    coefficient: int
    modulus: int
    constant: int
    residue: int
    auxiliary: int


EMPTY = GapState((), 1, 1, 0, 0, 0)


def extend(state: GapState, gap: int) -> GapState:
    step_coefficient = 3 ** (2 * gap + 5)
    step_modulus = 2 ** (3 * gap + 7)
    step_constant = 8**gap

    digit = (
        (step_constant - step_coefficient * state.auxiliary)
        * pow(step_coefficient * state.coefficient, -1, step_modulus)
    ) % step_modulus

    residue = state.residue + digit * state.modulus
    coefficient = step_coefficient * state.coefficient
    modulus = step_modulus * state.modulus
    constant = step_coefficient * state.constant + step_constant * state.modulus

    assert (coefficient * residue - constant) % modulus == 0
    auxiliary = (coefficient * residue - constant) // modulus

    return GapState(
        state.word + (gap,),
        coefficient,
        modulus,
        constant,
        residue,
        auxiliary,
    )


def all_zero_state(length: int) -> GapState:
    state = EMPTY
    for _ in range(length):
        state = extend(state, 0)
    return state


def gap_bound_for_state(state: GapState, bound: int) -> int:
    if bound <= 1:
        return 0

    gap = 0
    while 8 ** (gap + 1) * state.modulus < state.coefficient * bound:
        gap += 1
    return gap


def exact_minimum(length: int) -> tuple[GapState, list[int], int]:
    threshold = all_zero_state(length).residue
    best = all_zero_state(length)
    max_gap_seen = 0

    states = [EMPTY]
    frontier_sizes: list[int] = []

    for depth in range(length):
        next_states: list[GapState] = []
        for state in states:
            max_gap = gap_bound_for_state(state, threshold)
            max_gap_seen = max(max_gap_seen, max_gap)
            for gap in range(max_gap + 1):
                candidate = extend(state, gap)
                if candidate.residue >= threshold:
                    continue
                if depth == length - 1 and candidate.residue < best.residue:
                    best = candidate
                next_states.append(candidate)
        frontier_sizes.append(len(next_states))
        states = next_states

    direct = gap_prefix_code(best.word)
    assert direct.residue == best.residue
    assert direct.modulus == best.modulus
    assert direct.coefficient == best.coefficient
    assert direct.constant == best.constant

    return best, frontier_sizes, max_gap_seen


EXPECTED_MINIMA = {
    1: (59, (0,)),
    2: (9403, (0, 0)),
    3: (800827, (0, 2, 1)),
    4: (29048088, (1, 0, 0, 0)),
    5: (17315652795, (0, 0, 1, 0, 0)),
    6: (1087464711355, (0, 0, 0, 0, 1, 0)),
    7: (425502516796475, (0, 1, 0, 1, 0, 0, 0)),
    8: (21303984324256955, (0, 0, 0, 0, 0, 0, 0, 0)),
    9: (1999277499308784920, (1, 0, 0, 0, 0, 1, 0, 0, 0)),
    10: (574896789218913330363, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    11: (28909095686436784612539, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    12: (
        823772158218558831240379,
        (0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1),
    ),
    13: (
        558250406302741458205189307,
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ),
    14: (
        40172331663434910254977164475,
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    ),
}


def verify_known_minima(max_length: int = 12) -> None:
    if max_length > max(EXPECTED_MINIMA):
        raise ValueError(f"no expected minima recorded beyond {max(EXPECTED_MINIMA)}")

    for length in range(1, max_length + 1):
        best, frontier_sizes, max_gap = exact_minimum(length)
        expected_residue, expected_word = EXPECTED_MINIMA[length]
        assert best.residue == expected_residue, (length, best)
        assert best.word == expected_word, (length, best)
        print(
            f"length={length:2d} min={best.residue} bits={best.residue.bit_length():3d} "
            f"word={best.word} max_gap={max_gap:2d} frontier={frontier_sizes[-3:]}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=12)
    args = parser.parse_args()
    verify_known_minima(args.max_length)
