"""
explore71_aperiodic_templates.py

Diagnostic checks for low-complexity aperiodic {0,1} templates.

The compactness lemmas now rule out bounded-defect perturbations of eventually
periodic templates.  The next natural bounded-alphabet frontier is genuinely
aperiodic words, especially low-complexity examples such as Fibonacci/Sturmian
and Thue-Morse prefixes.

This script computes prefix-residue growth along a few canonical templates in
both the binary return and reduced {0,1} gap systems.  It is evidence only, not
a proof of divergence for the full aperiodic class.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import isqrt
from typing import Callable, Iterable

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return


DEFAULT_LENGTH = 256
MILESTONES = (16, 32, 64, 128, 256, 512, 1024)


@dataclass(frozen=True)
class Template:
    name: str
    generator: Callable[[int], tuple[int, ...]]


def fibonacci_word(length: int) -> tuple[int, ...]:
    word = "0"
    while len(word) < length:
        word = "".join("01" if char == "0" else "0" for char in word)
    return tuple(int(char) for char in word[:length])


def thue_morse_word(length: int) -> tuple[int, ...]:
    return tuple(index.bit_count() & 1 for index in range(length))


def period_doubling_word(length: int) -> tuple[int, ...]:
    # Fixed point of 0 -> 01, 1 -> 00.
    word = "0"
    while len(word) < length:
        word = "".join("01" if char == "0" else "00" for char in word)
    return tuple(int(char) for char in word[:length])


def sqrt2_mechanical_word(length: int) -> tuple[int, ...]:
    # Lower mechanical word with irrational slope sqrt(2)-1.
    # Since floor(n * (sqrt(2)-1)) = floor(n * sqrt(2)) - n, integer
    # square roots give exact finite prefixes without floating-point decisions.
    def floor_n_alpha(index: int) -> int:
        return isqrt(2 * index * index) - index

    return tuple(
        floor_n_alpha(index + 1) - floor_n_alpha(index)
        for index in range(length)
    )


def prefix_profiles(word: Iterable[int], milestones: tuple[int, ...]):
    return_state = RETURN_EMPTY
    gap_state = GAP_EMPTY
    word_tuple = tuple(word)
    rows = []
    milestone_set = set(milestones)
    for index, digit in enumerate(word_tuple, start=1):
        return_state = extend_return(return_state, digit)
        gap_state = extend_gap(gap_state, digit)
        if index in milestone_set:
            prefix = word_tuple[:index]
            rows.append(
                (
                    index,
                    sum(prefix),
                    return_state.residue.bit_length(),
                    gap_state.residue.bit_length(),
                    return_state.residue,
                    gap_state.residue,
                )
            )
    return rows


def run(length: int, show_residues: bool = False) -> None:
    milestones = tuple(m for m in MILESTONES if m <= length)
    if length not in milestones:
        milestones = milestones + (length,)

    templates = (
        Template("fibonacci", fibonacci_word),
        Template("thue-morse", thue_morse_word),
        Template("period-doubling", period_doubling_word),
        Template("mechanical-sqrt2", sqrt2_mechanical_word),
    )

    for template in templates:
        print(template.name)
        rows = prefix_profiles(template.generator(length), milestones)
        for level, ones, return_bits, gap_bits, return_residue, gap_residue in rows:
            line = (
                f"  L={level:3d} ones={ones:3d} "
                f"return_bits={return_bits:5d} gap_bits={gap_bits:5d}"
            )
            if show_residues:
                line += f" return_residue={return_residue} gap_residue={gap_residue}"
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH)
    parser.add_argument("--show-residues", action="store_true")
    args = parser.parse_args()
    run(args.length, args.show_residues)
