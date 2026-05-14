"""
explore69_window_shells.py

Profiles low normalized terminal-window frontiers by dyadic expansion shell.

The current proof gap is not terminal escape itself: even the smallest
expansion grows exponentially with prefix length.  What is missing is an
arithmetic separation theorem for normalized terminal heights.  This diagnostic
shows how the exact low frontiers are distributed across expansion scales.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from explore64_terminal_ranks import gap_levels, return_levels


BIT_CASES = (32, 36, 40)

EXPECTED_RETURN_PROFILES = {
    32: (
        (1, 8, 0, 5, 2, 1),
        (2, 29, 0, 5, 13, 1),
        (3, 72, 0, 5, 21, 16),
        (4, 134, 0, 5, 56, 8),
        (5, 142, 0, 5, 105, 1),
        (6, 121, 1, 4, 56, 37),
        (7, 80, 1, 4, 40, 4),
        (8, 50, 1, 3, 44, 5),
        (9, 19, 1, 3, 9, 9),
        (10, 3, 1, 3, 1, 1),
    ),
    36: (
        (1, 9, 0, 6, 2, 1),
        (2, 39, 0, 7, 13, 1),
        (3, 105, 0, 7, 47, 1),
        (4, 219, 0, 6, 91, 2),
        (5, 279, 0, 6, 126, 1),
        (6, 272, 1, 5, 180, 8),
        (7, 246, 1, 5, 123, 3),
        (8, 190, 1, 5, 120, 2),
        (9, 82, 1, 5, 66, 1),
        (10, 26, 1, 4, 14, 1),
        (11, 9, 1, 2, 8, 8),
        (12, 3, 2, 2, 3, 3),
    ),
    40: (
        (1, 10, 0, 6, 2, 2),
        (2, 47, 0, 7, 13, 2),
        (3, 151, 0, 7, 64, 5),
        (4, 352, 0, 7, 204, 4),
        (5, 521, 0, 7, 210, 1),
        (6, 613, 1, 7, 378, 1),
        (7, 584, 1, 6, 437, 7),
        (8, 537, 1, 6, 330, 1),
        (9, 291, 1, 5, 210, 11),
        (10, 139, 1, 5, 110, 2),
        (11, 57, 1, 4, 30, 15),
        (12, 18, 2, 3, 13, 5),
        (13, 2, 2, 2, 2, 2),
    ),
}

EXPECTED_GAP_PROFILES = {
    32: (
        (1, 9, 0, 2, 6, 2),
        (2, 28, 1, 2, 27, 27),
        (3, 26, 2, 3, 22, 22),
        (4, 7, 3, 4, 5, 2),
    ),
    36: (
        (1, 11, 0, 2, 6, 4),
        (2, 39, 1, 3, 27, 11),
        (3, 62, 2, 3, 58, 58),
        (4, 26, 3, 4, 21, 21),
        (5, 4, 4, 4, 4, 4),
    ),
    40: (
        (1, 12, 0, 2, 6, 5),
        (2, 49, 1, 3, 27, 21),
        (3, 97, 2, 4, 91, 2),
        (4, 76, 3, 4, 71, 71),
        (5, 20, 4, 5, 16, 4),
        (6, 1, 5, 5, 1, 1),
    ),
}


def expansion_shell(expansion: Fraction) -> int:
    """Return the unique s with 2**s <= expansion < 2**(s+1)."""
    shell = expansion.numerator.bit_length() - expansion.denominator.bit_length()
    while expansion < Fraction(2**shell, 1):
        shell -= 1
    while expansion >= Fraction(2 ** (shell + 1), 1):
        shell += 1
    return shell


def summarize_shells(states) -> tuple[int, int, int, int, int]:
    shells = Counter(
        expansion_shell(Fraction(state.coefficient, state.modulus)) for state in states
    )
    low_shell = min(shells)
    high_shell = max(shells)
    max_shell_count = max(shells.values())
    high_shell_count = shells[high_shell]
    return len(states), low_shell, high_shell, max_shell_count, high_shell_count


def return_shell_profile(bits: int):
    bound = (1 << bits) - 1
    return [
        (level, *summarize_shells(states))
        for level, states in enumerate(return_levels(bound), start=1)
    ]


def gap_shell_profile(bits: int):
    bound = (1 << bits) - 1
    return [
        (level, *summarize_shells(states))
        for level, states in enumerate(gap_levels(bound), start=1)
    ]


def verify_profiles() -> None:
    for bits in BIT_CASES:
        return_profile = return_shell_profile(bits)
        gap_profile = gap_shell_profile(bits)
        assert tuple(return_profile) == EXPECTED_RETURN_PROFILES[bits]
        assert tuple(gap_profile) == EXPECTED_GAP_PROFILES[bits]

        print(f"return expansion shells for B=2^{bits}-1")
        for level, count, low_shell, high_shell, max_shell_count, high_shell_count in return_profile:
            print(
                f"  level={level:2d} count={count:4d} "
                f"shells=[{low_shell:2d},{high_shell:2d}] "
                f"max_shell_count={max_shell_count:3d} high_shell_count={high_shell_count:3d}"
            )

        print(f"gap expansion shells for B=2^{bits}-1")
        for level, count, low_shell, high_shell, max_shell_count, high_shell_count in gap_profile:
            print(
                f"  level={level:2d} count={count:4d} "
                f"shells=[{low_shell:2d},{high_shell:2d}] "
                f"max_shell_count={max_shell_count:3d} high_shell_count={high_shell_count:3d}"
            )


if __name__ == "__main__":
    verify_profiles()
