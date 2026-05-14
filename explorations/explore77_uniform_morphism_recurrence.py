"""
explore77_uniform_morphism_recurrence.py

Finite diagnostic for binary q-uniform morphism fixed points.

The paper excludes all binary 2-, 3-, 4-, 5-, and 6-uniform fixed-point
templates by classification plus recurrence criteria.
This script enumerates binary q-uniform morphisms prolongable on 0 and checks
whether their pure power-length fixed-point prefixes recur below the
density-free return and gap cutoffs.  It also evaluates the sharper
density-recurrence margin from the paper at the sampled prefix lengths.
The companion script explore78 checks symbolic prefix witnesses c q^h; this is
needed for the 6-uniform theorem because pure q^h prefixes are not always the
right recurrence scale.

This is finite diagnostic evidence only.  It is not a proof for all q-uniform
or automatic sequences.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from math import log2


RETURN_CUTOFF = 3 / log2(243 / 128)
GAP_CUTOFF = 7 / (log2(243 / 128) + log2(9 / 8))
RETURN_ZERO_HEIGHT = log2(9 / 8)
RETURN_ONE_HEIGHT = log2(27 / 16)
GAP_ZERO_HEIGHT = log2(243 / 128)
GAP_ONE_HEIGHT = log2(9 / 8)


@dataclass(frozen=True)
class RecurrenceMetric:
    prefix_length: int
    recurrence: int
    ratio: float
    prefix_one_density: float
    recurrence_one_density: float
    return_margin: float
    gap_margin: float


def all_binary_words(length: int):
    return tuple(product((0, 1), repeat=length))


def morphism_fixed_prefix(
    image_zero: tuple[int, ...],
    image_one: tuple[int, ...],
    length: int,
) -> tuple[int, ...]:
    word = (0,)
    while len(word) < length:
        expanded: list[int] = []
        for digit in word:
            expanded.extend(image_zero if digit == 0 else image_one)
        word = tuple(expanded)
    return word[:length]


def first_prefix_recurrence(word: tuple[int, ...], prefix_length: int) -> int | None:
    prefix = word[:prefix_length]
    last_start = len(word) - prefix_length
    for start in range(1, last_start + 1):
        if word[start : start + prefix_length] == prefix:
            return start
    return None


def recurrence_metric(
    word: tuple[int, ...], prefix_length: int, recurrence: int
) -> RecurrenceMetric:
    ratio = recurrence / prefix_length
    prefix_one_density = sum(word[:prefix_length]) / prefix_length
    recurrence_one_density = sum(word[:recurrence]) / recurrence
    return_margin = (
        3
        + 4 * prefix_one_density
        - ratio * (RETURN_ZERO_HEIGHT + recurrence_one_density * RETURN_ONE_HEIGHT)
    )
    gap_margin = (
        7
        + 3 * prefix_one_density
        - ratio * (GAP_ZERO_HEIGHT + recurrence_one_density * GAP_ONE_HEIGHT)
    )
    return RecurrenceMetric(
        prefix_length=prefix_length,
        recurrence=recurrence,
        ratio=ratio,
        prefix_one_density=prefix_one_density,
        recurrence_one_density=recurrence_one_density,
        return_margin=return_margin,
        gap_margin=gap_margin,
    )


def rendered_morphism(image_zero: tuple[int, ...], image_one: tuple[int, ...]) -> str:
    return f"0->{''.join(map(str, image_zero))} 1->{''.join(map(str, image_one))}"


def obvious_eventually_periodic_kind(
    image_zero: tuple[int, ...], image_one: tuple[int, ...]
) -> str | None:
    """Detect the exact eventual-periodic cases that matter in the q=3 scan."""
    if all(digit == 0 for digit in image_zero):
        return "0^infinity"
    if all(digit == 1 for digit in image_zero[1:]) and all(
        digit == 1 for digit in image_one
    ):
        return "0 1^infinity"
    return None


def run(
    q: int, max_power: int, search_factor: int, verbose: bool, exceptions: bool
) -> None:
    milestones = tuple(q**power for power in range(1, max_power + 1))
    max_length = milestones[-1]
    search_length = max_length * search_factor + max_length
    image_zeros = tuple(word for word in all_binary_words(q) if word[0] == 0)
    image_ones = all_binary_words(q)

    total = 0
    below_return_all = 0
    below_gap_all = 0
    sampled_return_density_positive = 0
    sampled_gap_density_positive = 0
    sampled_return_fast_or_density = 0
    sampled_gap_fast_or_density = 0
    obvious_eventually_periodic = 0
    return_covered_by_sample_or_periodic = 0
    gap_covered_by_sample_or_periodic = 0
    missing = 0
    worst_ratio = 0.0
    worst_case = None
    weakest_return_margin = None
    weakest_return_case = None
    weakest_gap_margin = None
    weakest_gap_case = None

    print("uniform morphism prefix recurrence diagnostic")
    print(
        f"q={q} max_power={max_power} search_factor={search_factor} "
        f"return_cutoff={RETURN_CUTOFF:.3f} gap_cutoff={GAP_CUTOFF:.3f}"
    )

    for image_zero in image_zeros:
        for image_one in image_ones:
            total += 1
            periodic_kind = obvious_eventually_periodic_kind(image_zero, image_one)
            obvious_eventually_periodic += int(periodic_kind is not None)
            word = morphism_fixed_prefix(image_zero, image_one, search_length)
            metrics: list[RecurrenceMetric] = []
            ratios: list[float | None] = []
            has_missing = False

            for prefix_length in milestones:
                recurrence = first_prefix_recurrence(word, prefix_length)
                if recurrence is None:
                    has_missing = True
                    ratios.append(None)
                    continue
                metric = recurrence_metric(word, prefix_length, recurrence)
                metrics.append(metric)
                ratios.append(metric.ratio)
                if metric.ratio > worst_ratio:
                    worst_ratio = metric.ratio
                    worst_case = (
                        image_zero,
                        image_one,
                        prefix_length,
                        recurrence,
                        metric.ratio,
                    )
                if (
                    weakest_return_margin is None
                    or metric.return_margin < weakest_return_margin
                ):
                    weakest_return_margin = metric.return_margin
                    weakest_return_case = (image_zero, image_one, metric)
                if weakest_gap_margin is None or metric.gap_margin < weakest_gap_margin:
                    weakest_gap_margin = metric.gap_margin
                    weakest_gap_case = (image_zero, image_one, metric)

            if has_missing:
                missing += 1

            concrete_ratios = [ratio for ratio in ratios if ratio is not None]
            below_return = bool(concrete_ratios) and all(
                ratio < RETURN_CUTOFF for ratio in concrete_ratios
            )
            below_gap = bool(concrete_ratios) and all(
                ratio < GAP_CUTOFF for ratio in concrete_ratios
            )
            return_density_positive = bool(metrics) and all(
                metric.return_margin > 0 for metric in metrics
            )
            gap_density_positive = bool(metrics) and all(
                metric.gap_margin > 0 for metric in metrics
            )
            below_return_all += int(below_return and not has_missing)
            below_gap_all += int(below_gap and not has_missing)
            sampled_return_density_positive += int(
                return_density_positive and not has_missing
            )
            sampled_gap_density_positive += int(gap_density_positive and not has_missing)
            sampled_return_fast_or_density += int(
                (below_return or return_density_positive) and not has_missing
            )
            sampled_gap_fast_or_density += int(
                (below_gap or gap_density_positive) and not has_missing
            )
            return_covered_by_sample_or_periodic += int(
                ((below_return or return_density_positive) and not has_missing)
                or periodic_kind is not None
            )
            gap_covered_by_sample_or_periodic += int(
                ((below_gap or gap_density_positive) and not has_missing)
                or periodic_kind is not None
            )

            if exceptions:
                should_report = (
                    has_missing
                    or not below_return
                    or not below_gap
                    or not return_density_positive
                    or not gap_density_positive
                )
                if should_report:
                    rendered = ", ".join(
                        "missing" if ratio is None else f"{ratio:.3f}"
                        for ratio in ratios
                    )
                    if metrics:
                        min_return = min(metric.return_margin for metric in metrics)
                        min_gap = min(metric.gap_margin for metric in metrics)
                        margin_summary = (
                            f" R_margin>={min_return:.3f} G_margin>={min_gap:.3f}"
                        )
                    else:
                        margin_summary = ""
                    periodic_summary = (
                        "" if periodic_kind is None else f" periodic={periodic_kind}"
                    )
                    print(
                        f"  exception {rendered_morphism(image_zero, image_one)}: "
                        f"{rendered}{margin_summary}{periodic_summary}"
                    )

            if verbose:
                rendered = ", ".join(
                    "missing" if ratio is None else f"{ratio:.3f}" for ratio in ratios
                )
                margin_summary = ""
                if metrics:
                    min_return = min(metric.return_margin for metric in metrics)
                    min_gap = min(metric.gap_margin for metric in metrics)
                    margin_summary = f" R_margin>={min_return:.3f} G_margin>={min_gap:.3f}"
                periodic_summary = (
                    "" if periodic_kind is None else f" periodic={periodic_kind}"
                )
                print(
                    f"  {rendered_morphism(image_zero, image_one)}: "
                    f"{rendered}{margin_summary}{periodic_summary}"
                )

    print(f"total={total}")
    print(f"all_below_return_cutoff={below_return_all}")
    print(f"all_below_gap_cutoff={below_gap_all}")
    print(f"all_sampled_return_density_positive={sampled_return_density_positive}")
    print(f"all_sampled_gap_density_positive={sampled_gap_density_positive}")
    print(f"all_sampled_return_fast_or_density={sampled_return_fast_or_density}")
    print(f"all_sampled_gap_fast_or_density={sampled_gap_fast_or_density}")
    print(f"obvious_eventually_periodic={obvious_eventually_periodic}")
    print(
        "return_covered_by_sample_or_obvious_periodic="
        f"{return_covered_by_sample_or_periodic}"
    )
    print(
        "gap_covered_by_sample_or_obvious_periodic="
        f"{gap_covered_by_sample_or_periodic}"
    )
    print(f"with_missing_recurrence={missing}")
    if worst_case is not None:
        image_zero, image_one, prefix_length, recurrence, ratio = worst_case
        print(
            "worst_ratio="
            f"{ratio:.3f} at {rendered_morphism(image_zero, image_one)} "
            f"L={prefix_length} tau={recurrence}"
        )
    if weakest_return_case is not None:
        image_zero, image_one, metric = weakest_return_case
        print(
            "weakest_return_density_margin="
            f"{metric.return_margin:.3f} at {rendered_morphism(image_zero, image_one)} "
            f"L={metric.prefix_length} tau={metric.recurrence} "
            f"a={metric.prefix_one_density:.3f} b={metric.recurrence_one_density:.3f}"
        )
    if weakest_gap_case is not None:
        image_zero, image_one, metric = weakest_gap_case
        print(
            "weakest_gap_density_margin="
            f"{metric.gap_margin:.3f} at {rendered_morphism(image_zero, image_one)} "
            f"L={metric.prefix_length} tau={metric.recurrence} "
            f"a={metric.prefix_one_density:.3f} b={metric.recurrence_one_density:.3f}"
        )

    if q == 3 and max_power == 5 and search_factor == 16:
        expected = (
            32,
            30,
            31,
            31,
            31,
            31,
            31,
            9,
            32,
            32,
            1,
            4.0,
            ("011", "100", 3, 12),
        )
        observed = (
            total,
            below_return_all,
            below_gap_all,
            sampled_return_density_positive,
            sampled_gap_density_positive,
            sampled_return_fast_or_density,
            sampled_gap_fast_or_density,
            obvious_eventually_periodic,
            return_covered_by_sample_or_periodic,
            gap_covered_by_sample_or_periodic,
            missing,
            worst_ratio,
            None
            if worst_case is None
            else (
                "".join(map(str, worst_case[0])),
                "".join(map(str, worst_case[1])),
                worst_case[2],
                worst_case[3],
            ),
        )
        assert observed == expected, observed
    elif q == 4 and max_power == 4 and search_factor == 16:
        expected = (
            128,
            116,
            127,
            127,
            127,
            127,
            127,
            17,
            128,
            128,
            1,
            6.0,
            ("0111", "1100", 4, 24),
        )
        observed = (
            total,
            below_return_all,
            below_gap_all,
            sampled_return_density_positive,
            sampled_gap_density_positive,
            sampled_return_fast_or_density,
            sampled_gap_fast_or_density,
            obvious_eventually_periodic,
            return_covered_by_sample_or_periodic,
            gap_covered_by_sample_or_periodic,
            missing,
            worst_ratio,
            None
            if worst_case is None
            else (
                "".join(map(str, worst_case[0])),
                "".join(map(str, worst_case[1])),
                worst_case[2],
                worst_case[3],
            ),
        )
        assert observed == expected, observed
    elif q == 5 and max_power == 4 and search_factor == 16:
        expected = (
            512,
            460,
            507,
            511,
            511,
            511,
            511,
            33,
            512,
            512,
            1,
            8.0,
            ("01111", "11100", 5, 40),
        )
        observed = (
            total,
            below_return_all,
            below_gap_all,
            sampled_return_density_positive,
            sampled_gap_density_positive,
            sampled_return_fast_or_density,
            sampled_gap_fast_or_density,
            obvious_eventually_periodic,
            return_covered_by_sample_or_periodic,
            gap_covered_by_sample_or_periodic,
            missing,
            worst_ratio,
            None
            if worst_case is None
            else (
                "".join(map(str, worst_case[0])),
                "".join(map(str, worst_case[1])),
                worst_case[2],
                worst_case[3],
            ),
        )
        assert observed == expected, observed
    elif q == 6 and max_power == 3 and search_factor == 16:
        expected = (
            2048,
            1822,
            2021,
            2037,
            2042,
            2037,
            2042,
            65,
            2038,
            2043,
            1,
            10.0,
            ("011111", "111100", 6, 60),
        )
        observed = (
            total,
            below_return_all,
            below_gap_all,
            sampled_return_density_positive,
            sampled_gap_density_positive,
            sampled_return_fast_or_density,
            sampled_gap_fast_or_density,
            obvious_eventually_periodic,
            return_covered_by_sample_or_periodic,
            gap_covered_by_sample_or_periodic,
            missing,
            worst_ratio,
            None
            if worst_case is None
            else (
                "".join(map(str, worst_case[0])),
                "".join(map(str, worst_case[1])),
                worst_case[2],
                worst_case[3],
            ),
        )
        assert observed == expected, observed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--max-power", type=int, default=5)
    parser.add_argument("--search-factor", type=int, default=16)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--exceptions", action="store_true")
    args = parser.parse_args()
    run(args.q, args.max_power, args.search_factor, args.verbose, args.exceptions)
