"""
explore54_return_minima.py

Certifies least prefix residues in the binary return-block system.

For a current return-prefix composition

    Q_i n_i = P_i n_0 + D_i,

any length-L extension with final least residue R_L < B has intermediate state
n_i < (P_i B + D_i) / Q_i.  If the next return length is r, then

    33 n_i + 32 = 16^r w

with w positive odd, so necessarily

    16^r Q_i < 33(P_i B + D_i) + 32 Q_i.

Together with prefix-residue monotonicity, this gives a finite exhaustive
search below any height bound B.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from explore51_binary_return_code import block, prefix_code


@dataclass(frozen=True)
class ReturnState:
    word: tuple[int, ...]
    coefficient: int
    modulus: int
    constant: int
    residue: int
    auxiliary: int


EMPTY = ReturnState((), 1, 1, 0, 0, 0)


def extend(state: ReturnState, ones: int) -> ReturnState:
    step = block(ones)
    digit = (
        -(step.p * state.auxiliary + step.d)
        * pow(step.p * state.coefficient, -1, step.q)
    ) % step.q

    residue = state.residue + digit * state.modulus
    coefficient = step.p * state.coefficient
    modulus = step.q * state.modulus
    constant = step.p * state.constant + step.d * state.modulus

    assert (coefficient * residue + constant) % modulus == 0
    auxiliary = (coefficient * residue + constant) // modulus

    return ReturnState(
        state.word + (ones,),
        coefficient,
        modulus,
        constant,
        residue,
        auxiliary,
    )


def all_zero_state(length: int) -> ReturnState:
    state = EMPTY
    for _ in range(length):
        state = extend(state, 0)
    return state


def return_bound_for_state(state: ReturnState, bound: int) -> int:
    right = 33 * (state.coefficient * bound + state.constant) + 32 * state.modulus
    ones = 0
    while 16 ** (ones + 1) * state.modulus < right:
        ones += 1
    return ones


def exact_minimum(length: int) -> tuple[ReturnState, list[int], int]:
    threshold = all_zero_state(length).residue
    best = all_zero_state(length)
    max_ones_seen = 0

    states = [EMPTY]
    frontier_sizes: list[int] = []

    for depth in range(length):
        next_states: list[ReturnState] = []
        for state in states:
            max_ones = return_bound_for_state(state, threshold)
            max_ones_seen = max(max_ones_seen, max_ones)
            for ones in range(max_ones + 1):
                candidate = extend(state, ones)
                if candidate.residue >= threshold:
                    continue
                if depth == length - 1 and candidate.residue < best.residue:
                    best = candidate
                next_states.append(candidate)
        frontier_sizes.append(len(next_states))
        states = next_states

    direct = prefix_code(best.word)
    assert direct.residue == best.residue
    assert direct.q == best.modulus
    assert direct.p == best.coefficient
    assert direct.d == best.constant

    return best, frontier_sizes, max_ones_seen


EXPECTED_MINIMA = {
    1: (7, (0,)),
    2: (63, (0, 0)),
    3: (511, (0, 0, 0)),
    4: (4095, (0, 0, 0, 0)),
    5: (32767, (0, 0, 0, 0, 0)),
    6: (170047, (0, 0, 1, 0, 0, 0)),
    7: (1657008, (1, 0, 0, 0, 0, 0, 0)),
    8: (16777215, (0, 0, 0, 0, 0, 0, 0, 0)),
    9: (120777543, (0, 1, 0, 0, 0, 0, 0, 0, 0)),
    10: (391188479, (0, 0, 0, 0, 1, 0, 0, 0, 0, 0)),
    11: (5502926847, (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)),
    12: (23370661887, (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)),
    13: (549755813887, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    14: (4398046511103, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    15: (4398046511103, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
    16: (
        32499281723391,
        (0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    17: (
        1375297073223743,
        (0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
    ),
    18: (
        1693247906775039,
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
    ),
    19: (
        50655743145148415,
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    20: (1152921504606846975, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
}


def verify_known_minima(max_length: int = 18) -> None:
    if max_length > max(EXPECTED_MINIMA):
        raise ValueError(f"no expected minima recorded beyond {max(EXPECTED_MINIMA)}")

    for length in range(1, max_length + 1):
        best, frontier_sizes, max_ones = exact_minimum(length)
        expected_residue, expected_word = EXPECTED_MINIMA[length]
        assert best.residue == expected_residue, (length, best)
        assert best.word == expected_word, (length, best)
        print(
            f"length={length:2d} min={best.residue} bits={best.residue.bit_length():3d} "
            f"word={best.word} max_r={max_ones:2d} frontier={frontier_sizes[-3:]}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=18)
    args = parser.parse_args()
    verify_known_minima(args.max_length)
