"""
explore70_bounded_alphabet_minima.py

Exact finite checks for the first nonconstant bounded alphabets.

The proof obligations now isolate the first bounded-alphabet targets:

    mu_L^(<=1) -> infinity       for binary return lengths {0, 1}
    nu_L^(<=1) -> infinity       for reduced gap lengths {0, 1}

This script exhaustively enumerates those two-symbol alphabets at finite depth
and records the least prefix residues.  It is diagnostic evidence only; finite
enumeration does not prove divergence.

Use --profile-ones L to group length-L words by the number of 1 labels and
print the least residue in each stratum.
"""

from __future__ import annotations

import argparse

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return


MAX_LENGTH = 20

EXPECTED_RETURN_MINIMA = (
    (1, 7, (0,)),
    (2, 63, (0, 0)),
    (3, 511, (0, 0, 0)),
    (4, 4095, (0, 0, 0, 0)),
    (5, 32767, (0, 0, 0, 0, 0)),
    (6, 170047, (0, 0, 1, 0, 0, 0)),
    (7, 1657008, (1, 0, 0, 0, 0, 0, 0)),
    (8, 16777215, (0, 0, 0, 0, 0, 0, 0, 0)),
    (9, 120777543, (0, 1, 0, 0, 0, 0, 0, 0, 0)),
    (10, 391188479, (0, 0, 0, 0, 1, 0, 0, 0, 0, 0)),
    (11, 5502926847, (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)),
    (12, 23370661887, (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)),
    (13, 549755813887, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (14, 4398046511103, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (15, 4398046511103, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
    (16, 32499281723391, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (17, 1375297073223743, (0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)),
    (18, 1693247906775039, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)),
    (19, 50655743145148415, (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (20, 1152921504606846975, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
)

EXPECTED_GAP_MINIMA = (
    (1, 59, (0,)),
    (2, 9403, (0, 0)),
    (3, 1221819, (0, 0, 0)),
    (4, 29048088, (1, 0, 0, 0)),
    (5, 17315652795, (0, 0, 1, 0, 0)),
    (6, 1087464711355, (0, 0, 0, 0, 1, 0)),
    (7, 425502516796475, (0, 1, 0, 1, 0, 0, 0)),
    (8, 21303984324256955, (0, 0, 0, 0, 0, 0, 0, 0)),
    (9, 1999277499308784920, (1, 0, 0, 0, 0, 1, 0, 0, 0)),
    (10, 574896789218913330363, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (11, 28909095686436784612539, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (12, 823772158218558831240379, (0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1)),
    (13, 558250406302741458205189307, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
    (14, 40172331663434910254977164475, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)),
    (15, 1008339061639395756883060106427, (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0)),
    (16, 284918499996251793677073916837144, (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)),
    (17, 15680483929519685525412524107932859, (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (18, 37726958071669264427461097780478649531, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (19, 936987362784094399040437222242446910651, (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0)),
    (20, 5327483134500439866600283610852124435643, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)),
)


def bounded_return_minima(max_length: int = MAX_LENGTH):
    states = [RETURN_EMPTY]
    minima = []
    for level in range(1, max_length + 1):
        states = [extend_return(state, digit) for state in states for digit in (0, 1)]
        best = min(states, key=lambda state: state.residue)
        minima.append((level, best.residue, best.word))
    return minima


def bounded_gap_minima(max_length: int = MAX_LENGTH):
    states = [GAP_EMPTY]
    minima = []
    for level in range(1, max_length + 1):
        states = [extend_gap(state, digit) for state in states for digit in (0, 1)]
        best = min(states, key=lambda state: state.residue)
        minima.append((level, best.residue, best.word))
    return minima


def states_at_length(empty_state, extend, length: int):
    states = [empty_state]
    for _ in range(length):
        states = [extend(state, digit) for state in states for digit in (0, 1)]
    return states


def ones_profile(states):
    best_by_ones = {}
    for state in states:
        ones = sum(state.word)
        if ones not in best_by_ones or state.residue < best_by_ones[ones].residue:
            best_by_ones[ones] = state
    return sorted(best_by_ones.items())


def print_ones_profile(length: int) -> None:
    print(f"return {{0,1}} minima by ones at L={length}")
    for ones, state in ones_profile(states_at_length(RETURN_EMPTY, extend_return, length)):
        print(
            f"  ones={ones:2d} min={state.residue:24d} "
            f"bits={state.residue.bit_length():3d} word={state.word}"
        )

    print(f"gap {{0,1}} minima by ones at L={length}")
    for ones, state in ones_profile(states_at_length(GAP_EMPTY, extend_gap, length)):
        print(
            f"  ones={ones:2d} min={state.residue:24d} "
            f"bits={state.residue.bit_length():3d} word={state.word}"
        )


def verify_bounded_minima(max_length: int = MAX_LENGTH) -> None:
    return_minima = bounded_return_minima(max_length)
    gap_minima = bounded_gap_minima(max_length)
    if max_length == MAX_LENGTH:
        assert tuple(return_minima) == EXPECTED_RETURN_MINIMA
        assert tuple(gap_minima) == EXPECTED_GAP_MINIMA

    print("return {0,1} bounded-alphabet minima")
    for level, residue, word in return_minima:
        print(
            f"  L={level:2d} min={residue:24d} bits={residue.bit_length():3d} "
            f"ones={sum(word):2d} word={word}"
        )

    print("gap {0,1} bounded-alphabet minima")
    for level, residue, word in gap_minima:
        print(
            f"  L={level:2d} min={residue:24d} bits={residue.bit_length():3d} "
            f"ones={sum(word):2d} word={word}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=MAX_LENGTH)
    parser.add_argument("--profile-ones", type=int)
    args = parser.parse_args()
    if args.profile_ones is not None:
        print_ones_profile(args.profile_ones)
    else:
        verify_bounded_minima(args.max_length)
