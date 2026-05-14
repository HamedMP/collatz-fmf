"""
explore74_mechanical_landing.py

Diagnostic verifier for the mechanical landing normal form.

The paper reduces the balanced/Sturmian frontier to lower or upper mechanical
binary words with irrational slope.  This script checks the exact floor/ceiling
prefix-sum formula and the return/gap coefficient recurrences against the
existing prefix engines on representative quadratic-irrational slopes.

This is evidence and regression coverage for the algebraic normal form; it is
not a proof that all irrational mechanical landings diverge.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return


DEFAULT_LENGTH = 128
MILESTONES = (16, 32, 64, 128, 256, 512)


@dataclass(frozen=True)
class MechanicalSample:
    name: str
    radicand: int
    subtract: int
    intercept: Fraction
    convention: str


@dataclass(frozen=True)
class NormalReturn:
    coefficient: int
    modulus: int
    constant: int


@dataclass(frozen=True)
class NormalGap:
    coefficient: int
    modulus: int
    constant: int


SAMPLES = (
    MechanicalSample("sqrt2-minus-1-lower-rho0", 2, 1, Fraction(0), "lower"),
    MechanicalSample("sqrt2-minus-1-upper-rho1_3", 2, 1, Fraction(1, 3), "upper"),
    MechanicalSample("sqrt3-minus-1-lower-rho1_2", 3, 1, Fraction(1, 2), "lower"),
    MechanicalSample("sqrt3-minus-1-upper-rho2_3", 3, 1, Fraction(2, 3), "upper"),
    MechanicalSample("sqrt5-minus-2-lower-rho1_5", 5, 2, Fraction(1, 5), "lower"),
    MechanicalSample("sqrt5-minus-2-upper-rho3_5", 5, 2, Fraction(3, 5), "upper"),
)


def floor_surd_fraction(multiple: int, radicand: int, offset: int, denom: int) -> int:
    """Return floor((multiple * sqrt(radicand) + offset) / denom) exactly."""
    if multiple == 0:
        return offset // denom

    square = radicand * multiple * multiple
    estimate = (isqrt(square) + offset) // denom

    def leq(candidate: int) -> bool:
        threshold = denom * candidate - offset
        if threshold <= 0:
            return True
        return threshold * threshold <= square


    while leq(estimate + 1):
        estimate += 1
    while not leq(estimate):
        estimate -= 1
    return estimate


def floor_n_slope_plus_intercept(index: int, sample: MechanicalSample) -> int:
    # slope = sqrt(radicand) - subtract, with 0 < slope < 1.
    intercept = sample.intercept
    denom = intercept.denominator
    multiple = denom * index
    offset = intercept.numerator - denom * sample.subtract * index
    return floor_surd_fraction(multiple, sample.radicand, offset, denom)


def ceil_n_slope_plus_intercept(index: int, sample: MechanicalSample) -> int:
    intercept = sample.intercept
    denom = intercept.denominator
    multiple = denom * index
    offset = intercept.numerator - denom * sample.subtract * index
    floor_value = floor_surd_fraction(multiple, sample.radicand, offset, denom)
    if multiple == 0 and offset % denom == 0:
        return floor_value
    return floor_value + 1


def prefix_sum(index: int, sample: MechanicalSample) -> int:
    if sample.convention == "lower":
        return floor_n_slope_plus_intercept(index, sample)
    if sample.convention == "upper":
        return ceil_n_slope_plus_intercept(index, sample)
    raise ValueError(sample.convention)


def mechanical_word(length: int, sample: MechanicalSample) -> tuple[int, ...]:
    values = [prefix_sum(index, sample) for index in range(length + 1)]
    return tuple(values[index + 1] - values[index] for index in range(length))


def extend_normal_return(state: NormalReturn, digit: int) -> NormalReturn:
    step_coefficient = 9 * 27**digit
    step_modulus = 2 ** (4 * digit + 3)
    step_constant = 1 if digit == 0 else 112
    return NormalReturn(
        coefficient=step_coefficient * state.coefficient,
        modulus=step_modulus * state.modulus,
        constant=step_coefficient * state.constant + step_constant * state.modulus,
    )


def extend_normal_gap(state: NormalGap, digit: int) -> NormalGap:
    step_coefficient = 3 ** (5 + 2 * digit)
    step_modulus = 2 ** (7 + 3 * digit)
    step_constant = 8**digit
    return NormalGap(
        coefficient=step_coefficient * state.coefficient,
        modulus=step_modulus * state.modulus,
        constant=step_coefficient * state.constant + step_constant * state.modulus,
    )


def verify_sample(sample: MechanicalSample, length: int) -> list[tuple[int, int, int, int]]:
    word = mechanical_word(length, sample)
    return_state = RETURN_EMPTY
    gap_state = GAP_EMPTY
    normal_return = NormalReturn(1, 1, 0)
    normal_gap = NormalGap(1, 1, 0)
    rows: list[tuple[int, int, int, int]] = []
    milestones = {mark for mark in MILESTONES if mark <= length}
    milestones.add(length)

    for level, digit in enumerate(word, start=1):
        assert digit in (0, 1), (sample, level, digit)

        return_state = extend_return(return_state, digit)
        gap_state = extend_gap(gap_state, digit)
        normal_return = extend_normal_return(normal_return, digit)
        normal_gap = extend_normal_gap(normal_gap, digit)

        ones = sum(word[:level])
        exact_ones = prefix_sum(level, sample) - prefix_sum(0, sample)
        assert ones == exact_ones, (sample, level, ones, exact_ones)

        assert normal_return.coefficient == 9**level * 27**ones
        assert normal_return.modulus == 2 ** (3 * level + 4 * ones)
        assert normal_return.coefficient == return_state.coefficient
        assert normal_return.modulus == return_state.modulus
        assert normal_return.constant == return_state.constant

        assert normal_gap.coefficient == 3 ** (5 * level + 2 * ones)
        assert normal_gap.modulus == 2 ** (7 * level + 3 * ones)
        assert normal_gap.coefficient == gap_state.coefficient
        assert normal_gap.modulus == gap_state.modulus
        assert normal_gap.constant == gap_state.constant

        if level in milestones:
            rows.append(
                (
                    level,
                    ones,
                    return_state.residue.bit_length(),
                    gap_state.residue.bit_length(),
                )
            )

    return rows


def run(length: int) -> None:
    print("mechanical landing normal-form verifier")
    final_summary = []
    for sample in SAMPLES:
        rows = verify_sample(sample, length)
        print(sample.name)
        for level, ones, return_bits, gap_bits in rows:
            print(
                f"  L={level:3d} ones={ones:3d} "
                f"return_bits={return_bits:5d} gap_bits={gap_bits:5d}"
            )
        final_summary.append((sample.name, *rows[-1]))

    if length == DEFAULT_LENGTH:
        expected = (
            ("sqrt2-minus-1-lower-rho0", 128, 53, 595, 1050),
            ("sqrt2-minus-1-upper-rho1_3", 128, 53, 596, 1055),
            ("sqrt3-minus-1-lower-rho1_2", 128, 94, 759, 1178),
            ("sqrt3-minus-1-upper-rho2_3", 128, 94, 759, 1178),
            ("sqrt5-minus-2-lower-rho1_5", 128, 30, 497, 986),
            ("sqrt5-minus-2-upper-rho3_5", 128, 30, 504, 985),
        )
        assert tuple(final_summary) == expected, final_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH)
    args = parser.parse_args()
    run(args.length)
