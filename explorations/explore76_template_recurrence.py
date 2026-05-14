"""
explore76_template_recurrence.py

Diagnostic for the density-free prefix-recurrence cutoffs on standard
aperiodic binary templates.

The paper now proves that any binary ordinary landing must avoid fast recurring
prefixes: return candidates cannot have infinitely recurring prefix ratios
below about 3.244, and reduced-gap candidates cannot have ratios below about
6.394.  This script checks canonical higher-complexity templates against those
cutoffs.

This is finite evidence only; it is not a proof for any infinite template class.
"""

from __future__ import annotations

import argparse
from math import log2

from explore71_aperiodic_templates import Template
from explore71_aperiodic_templates import fibonacci_word
from explore71_aperiodic_templates import period_doubling_word
from explore71_aperiodic_templates import sqrt2_mechanical_word
from explore71_aperiodic_templates import thue_morse_word


DEFAULT_LENGTH = 1024
DEFAULT_SEARCH_FACTOR = 16
MILESTONES = (16, 32, 64, 128, 256, 512, 1024, 2048)
RETURN_CUTOFF = 3 / log2(243 / 128)
GAP_CUTOFF = 7 / (log2(243 / 128) + log2(9 / 8))


def templates() -> tuple[Template, ...]:
    return (
        Template("fibonacci", fibonacci_word),
        Template("thue-morse", thue_morse_word),
        Template("period-doubling", period_doubling_word),
        Template("mechanical-sqrt2", sqrt2_mechanical_word),
    )


def first_prefix_recurrence(word: tuple[int, ...], prefix_length: int) -> int | None:
    prefix = word[:prefix_length]
    last_start = len(word) - prefix_length
    for start in range(1, last_start + 1):
        if word[start : start + prefix_length] == prefix:
            return start
    return None


def run(max_length: int, search_factor: int) -> None:
    print("template prefix recurrence diagnostic")
    print(
        f"max_length={max_length} search_factor={search_factor} "
        f"return_cutoff={RETURN_CUTOFF:.3f} gap_cutoff={GAP_CUTOFF:.3f}"
    )
    milestones = tuple(mark for mark in MILESTONES if mark <= max_length)
    final_summary = []

    for template in templates():
        search_length = max_length * search_factor + max_length
        word = template.generator(search_length)
        rows = []
        below_return = 0
        below_gap = 0
        print(template.name)

        for prefix_length in milestones:
            recurrence = first_prefix_recurrence(word, prefix_length)
            ratio = None if recurrence is None else recurrence / prefix_length
            rows.append((prefix_length, recurrence))

            if ratio is None:
                print(f"  L={prefix_length:4d} tau=>{prefix_length * search_factor}")
                continue

            below_return += int(ratio < RETURN_CUTOFF)
            below_gap += int(ratio < GAP_CUTOFF)
            print(
                f"  L={prefix_length:4d} tau={recurrence:6d} "
                f"tau/L={ratio:7.3f} "
                f"below_return={ratio < RETURN_CUTOFF} "
                f"below_gap={ratio < GAP_CUTOFF}"
            )

        print(
            f"  below-cutoff milestones: "
            f"return={below_return}/{len(rows)} gap={below_gap}/{len(rows)}"
        )
        final_summary.append((template.name, tuple(rows)))

    if max_length == DEFAULT_LENGTH and search_factor == DEFAULT_SEARCH_FACTOR:
        expected = (
            (
                "fibonacci",
                (
                    (16, 13),
                    (32, 21),
                    (64, 55),
                    (128, 89),
                    (256, 233),
                    (512, 377),
                    (1024, 987),
                ),
            ),
            (
                "thue-morse",
                (
                    (16, 24),
                    (32, 48),
                    (64, 96),
                    (128, 192),
                    (256, 384),
                    (512, 768),
                    (1024, 1536),
                ),
            ),
            (
                "period-doubling",
                (
                    (16, 32),
                    (32, 64),
                    (64, 128),
                    (128, 256),
                    (256, 512),
                    (512, 1024),
                    (1024, 2048),
                ),
            ),
            (
                "mechanical-sqrt2",
                (
                    (16, 29),
                    (32, 29),
                    (64, 29),
                    (128, 169),
                    (256, 169),
                    (512, 985),
                    (1024, 985),
                ),
            ),
        )
        assert tuple(final_summary) == expected, final_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH)
    parser.add_argument("--search-factor", type=int, default=DEFAULT_SEARCH_FACTOR)
    args = parser.parse_args()
    run(args.length, args.search_factor)
