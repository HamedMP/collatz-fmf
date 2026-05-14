"""
explore79_q9_boundary.py

Targeted recurrence search for the first q=9 symbolic-prefix boundary case.

The reduced-gap symbolic-prefix diagnostic in explore78 leaves one q=9 case:

    0 -> 011111111
    1 -> 100000000

For this morphism, the best witness up to symbolic prefix length 18 is c=2,
tau=17, with gap margin slightly negative.  This script uses a Z-array to scan
first recurrences for all prefix lengths up to a larger bound in one pass.
"""

from __future__ import annotations

import argparse
from math import log2


IMAGE_ZERO = tuple(map(int, "011111111"))
IMAGE_ONE = tuple(map(int, "100000000"))
Q = 9

RETURN_ZERO_HEIGHT = log2(9 / 8)
RETURN_ONE_HEIGHT = log2(27 / 16)
GAP_ZERO_HEIGHT = log2(243 / 128)
GAP_ONE_HEIGHT = log2(9 / 8)
RETURN_CUTOFF = 3 / log2(243 / 128)
GAP_CUTOFF = 7 / (log2(243 / 128) + log2(9 / 8))


def fixed_prefix(length: int) -> list[int]:
    word = [0]
    while len(word) < length:
        expanded: list[int] = []
        for digit in word:
            expanded.extend(IMAGE_ZERO if digit == 0 else IMAGE_ONE)
        word = expanded
    return word[:length]


def z_array(word: list[int]) -> list[int]:
    z = [0] * len(word)
    left = 0
    right = 0
    for i in range(1, len(word)):
        if i <= right:
            z[i] = min(right - i + 1, z[i - left])
        while i + z[i] < len(word) and word[z[i]] == word[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1
    return z


def first_recurrences(word: list[int], max_prefix: int) -> list[int | None]:
    z = z_array(word)
    first: list[int | None] = [None] * (max_prefix + 1)
    parent = list(range(max_prefix + 2))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for shift, match_length in enumerate(z[1:], start=1):
        upto = min(match_length, max_prefix)
        prefix_length = find(1)
        while prefix_length <= upto:
            first[prefix_length] = shift
            parent[prefix_length] = find(prefix_length + 1)
            prefix_length = find(prefix_length)
    return first


def limiting_density() -> float:
    ones_zero = sum(IMAGE_ZERO)
    ones_one = sum(IMAGE_ONE)
    return ones_zero / (Q - ones_one + ones_zero)


def margins(prefix_length: int, recurrence: int, density: float) -> tuple[float, float]:
    ratio = recurrence / prefix_length
    return_margin = (
        3
        + 4 * density
        - ratio * (RETURN_ZERO_HEIGHT + density * RETURN_ONE_HEIGHT)
    )
    gap_margin = (
        7
        + 3 * density
        - ratio * (GAP_ZERO_HEIGHT + density * GAP_ONE_HEIGHT)
    )
    return return_margin, gap_margin


def run(max_prefix: int, search_factor: int) -> None:
    search_length = max_prefix * search_factor + max_prefix
    density = limiting_density()
    word = fixed_prefix(search_length)
    first = first_recurrences(word, max_prefix)

    best_return: tuple[float, int, int, float, float] | None = None
    best_gap: tuple[float, int, int, float, float] | None = None
    first_gap_success: tuple[int, int, float, float] | None = None
    missing = 0

    for prefix_length in range(1, max_prefix + 1):
        recurrence = first[prefix_length]
        if recurrence is None:
            missing += 1
            continue
        ratio = recurrence / prefix_length
        return_margin, gap_margin = margins(prefix_length, recurrence, density)
        if best_return is None or return_margin > best_return[0]:
            best_return = (return_margin, prefix_length, recurrence, ratio, gap_margin)
        if best_gap is None or gap_margin > best_gap[0]:
            best_gap = (gap_margin, prefix_length, recurrence, ratio, return_margin)
        if first_gap_success is None and (
            ratio < GAP_CUTOFF or gap_margin > 0
        ):
            first_gap_success = (prefix_length, recurrence, ratio, gap_margin)

    print("q=9 boundary recurrence scan")
    print(
        f"max_prefix={max_prefix} search_factor={search_factor} "
        f"search_length={search_length} density={density:.6f}"
    )
    print(f"missing_recurrences={missing}")
    if best_return is not None:
        margin, prefix_length, recurrence, ratio, gap_margin = best_return
        print(
            "best_return="
            f"margin={margin:.6f} c={prefix_length} tau={recurrence} "
            f"T={ratio:.6f} gap_margin={gap_margin:.6f}"
        )
    if best_gap is not None:
        margin, prefix_length, recurrence, ratio, return_margin = best_gap
        print(
            "best_gap="
            f"margin={margin:.6f} c={prefix_length} tau={recurrence} "
            f"T={ratio:.6f} return_margin={return_margin:.6f}"
        )
    if first_gap_success is None:
        print("gap_success=none")
    else:
        prefix_length, recurrence, ratio, gap_margin = first_gap_success
        print(
            "gap_success="
            f"c={prefix_length} tau={recurrence} T={ratio:.6f} "
            f"margin={gap_margin:.6f}"
        )

    if max_prefix == 50000 and search_factor == 32:
        assert best_gap is not None
        assert best_gap[:4] == (
            -0.08308753677896519,
            2,
            17,
            8.5,
        ), best_gap
        assert first_gap_success is None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-prefix", type=int, default=50000)
    parser.add_argument("--search-factor", type=int, default=32)
    args = parser.parse_args()
    run(args.max_prefix, args.search_factor)
