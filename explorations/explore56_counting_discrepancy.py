"""
explore56_counting_discrepancy.py

Measures finite-height prefix counts against the natural density rates.

For each height B=2^bits-1, the script enumerates exact survivor frontiers
using explore55 and reports the largest normalized discrepancy for least
prefix residues:

    N_R(B,L) / ((B+1) (2/15)^L)
    N_G(B,L) / (B (1/112)^L)

over all surviving levels L in the displayed range.
"""

from __future__ import annotations

from fractions import Fraction

from explore55_height_survival import gap_survival_depth, return_survival_depth


RETURN_CASES = (24, 32, 40, 48, 52)
GAP_CASES = (24, 32, 40, 48, 56, 64)

EXPECTED_RETURN_WORST = {
    24: (8, 1),
    32: (10, 3),
    40: (12, 18),
    48: (16, 6),
    52: (18, 1),
}

EXPECTED_GAP_WORST = {
    24: (3, 6),
    32: (4, 7),
    40: (6, 1),
    48: (6, 35),
    56: (8, 1),
    64: (9, 7),
}


def worst_return_discrepancy(bits: int) -> tuple[int, int, Fraction]:
    bound = (1 << bits) - 1
    _, frontier = return_survival_depth(bound)
    rho = Fraction(2, 15)
    worst_level = 0
    worst_count = 0
    worst_ratio = Fraction(0, 1)

    for level, count in enumerate(frontier, start=1):
        ratio = Fraction(count, 1) / ((bound + 1) * rho**level)
        if ratio > worst_ratio:
            worst_level = level
            worst_count = count
            worst_ratio = ratio

    return worst_level, worst_count, worst_ratio


def worst_gap_discrepancy(bits: int) -> tuple[int, int, Fraction]:
    bound = (1 << bits) - 1
    _, frontier = gap_survival_depth(bound)
    rho = Fraction(1, 112)
    worst_level = 0
    worst_count = 0
    worst_ratio = Fraction(0, 1)

    for level, count in enumerate(frontier, start=1):
        ratio = Fraction(count, 1) / (bound * rho**level)
        if ratio > worst_ratio:
            worst_level = level
            worst_count = count
            worst_ratio = ratio

    return worst_level, worst_count, worst_ratio


def verify_return_discrepancies() -> None:
    for bits in RETURN_CASES:
        level, count, ratio = worst_return_discrepancy(bits)
        assert (level, count) == EXPECTED_RETURN_WORST[bits]
        print(
            f"return bits={bits:3d} worst_level={level:3d} "
            f"count={count:5d} normalized={float(ratio):.6f}"
        )


def verify_gap_discrepancies() -> None:
    for bits in GAP_CASES:
        level, count, ratio = worst_gap_discrepancy(bits)
        assert (level, count) == EXPECTED_GAP_WORST[bits]
        print(
            f"gap    bits={bits:3d} worst_level={level:3d} "
            f"count={count:5d} normalized={float(ratio):.6f}"
        )


if __name__ == "__main__":
    verify_return_discrepancies()
    verify_gap_discrepancies()
