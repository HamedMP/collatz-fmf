"""
explore75_mechanical_recurrence.py

Diagnostic for the prefix-recurrence obstruction in the balanced mechanical
frontier.

The paper now shows that a lower mechanical ordinary landing would force the
first recurrence time of every sufficiently long prefix to exceed a large
slope-dependent multiple of the prefix length.  This script checks exact
quadratic-irrational lower mechanical samples and reports how their observed
prefix recurrence ratios compare with those thresholds.

This is finite evidence only.  It does not prove that every irrational
mechanical word has fast prefix recurrences infinitely often.
"""

from __future__ import annotations

import argparse
from math import log2, sqrt

from explore74_mechanical_landing import MechanicalSample
from explore74_mechanical_landing import SAMPLES
from explore74_mechanical_landing import mechanical_word


DEFAULT_LENGTH = 128
DEFAULT_SEARCH_FACTOR = 64
MILESTONES = (8, 16, 32, 64, 128, 256, 512)


def slope_float(sample: MechanicalSample) -> float:
    return sqrt(sample.radicand) - sample.subtract


def return_threshold(alpha: float) -> float:
    return (3 + 4 * alpha) / (log2(9 / 8) + alpha * log2(27 / 16))


def gap_threshold(alpha: float) -> float:
    return (7 + 3 * alpha) / (log2(243 / 128) + alpha * log2(9 / 8))


def first_prefix_recurrence(word: tuple[int, ...], prefix_length: int) -> int | None:
    prefix = word[:prefix_length]
    last_start = len(word) - prefix_length
    for start in range(1, last_start + 1):
        if word[start : start + prefix_length] == prefix:
            return start
    return None


def lower_samples() -> tuple[MechanicalSample, ...]:
    return tuple(sample for sample in SAMPLES if sample.convention == "lower")


def verify_sample(
    sample: MechanicalSample,
    max_length: int,
    search_factor: int,
) -> list[tuple[int, int | None, float | None]]:
    search_limit = max_length * search_factor
    word = mechanical_word(search_limit + max_length, sample)
    rows: list[tuple[int, int | None, float | None]] = []

    for prefix_length in MILESTONES:
        if prefix_length > max_length:
            continue
        recurrence = first_prefix_recurrence(word, prefix_length)
        ratio = None if recurrence is None else recurrence / prefix_length
        rows.append((prefix_length, recurrence, ratio))

    return rows


def run(max_length: int, search_factor: int) -> None:
    print("mechanical prefix recurrence diagnostic")
    print(f"max_length={max_length} search_factor={search_factor}")
    final_summary = []

    for sample in lower_samples():
        alpha = slope_float(sample)
        threshold_r = return_threshold(alpha)
        threshold_g = gap_threshold(alpha)
        rows = verify_sample(sample, max_length, search_factor)
        final_summary.append((sample.name, tuple(row[:2] for row in rows)))
        below_return = 0
        below_gap = 0

        print(sample.name)
        print(
            f"  alpha~{alpha:.12f} "
            f"return_threshold~{threshold_r:.3f} "
            f"gap_threshold~{threshold_g:.3f}"
        )

        for prefix_length, recurrence, ratio in rows:
            if recurrence is None or ratio is None:
                print(f"  L={prefix_length:3d} tau=>{prefix_length * search_factor}")
                continue
            below_return += int(ratio < threshold_r)
            below_gap += int(ratio < threshold_g)
            print(
                f"  L={prefix_length:3d} tau={recurrence:5d} "
                f"tau/L={ratio:7.3f} "
                f"below_return={ratio < threshold_r} "
                f"below_gap={ratio < threshold_g}"
            )

        print(
            f"  below-threshold milestones: "
            f"return={below_return}/{len(rows)} gap={below_gap}/{len(rows)}"
        )

    if max_length == DEFAULT_LENGTH and search_factor == DEFAULT_SEARCH_FACTOR:
        expected = (
            (
                "sqrt2-minus-1-lower-rho0",
                ((8, 5), (16, 29), (32, 29), (64, 29), (128, 169)),
            ),
            (
                "sqrt3-minus-1-lower-rho1_2",
                ((8, 4), (16, 26), (32, 56), (64, 56), (128, 56)),
            ),
            (
                "sqrt5-minus-2-lower-rho1_5",
                ((8, 4), (16, 17), (32, 17), (64, 72), (128, 161)),
            ),
        )
        assert tuple(final_summary) == expected, final_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH)
    parser.add_argument("--search-factor", type=int, default=DEFAULT_SEARCH_FACTOR)
    args = parser.parse_args()
    run(args.length, args.search_factor)
