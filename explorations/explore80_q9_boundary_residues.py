"""
explore80_q9_boundary_residues.py

Prefix-residue diagnostic for the q=9 reduced-gap boundary morphism.

The symbolic recurrence scan leaves one q=9 reduced-gap template:

    0 -> 011111111
    1 -> 100000000

This fixed point is the parity of the number of nonzero base-9 digits of the
index.  This script follows that one infinite word and records the least
gap-prefix residue along its prefixes.  Unbounded residues would exclude a
positive ordinary landing for this template; finite residue growth is diagnostic
evidence only.
"""

from __future__ import annotations

import argparse

from explore53_gap_minima import EMPTY
from explore53_gap_minima import GapState
from explore53_gap_minima import extend


DEFAULT_MAX_LENGTH = 1000
DEFAULT_MILESTONES = (1, 2, 9, 10, 81, 100, 729, 1000)


def q9_boundary_digit(index: int) -> int:
    """Return the fixed-point digit at zero-based position index."""
    parity = 0
    while index:
        index, digit = divmod(index, 9)
        parity ^= int(digit != 0)
    return parity


def q9_boundary_prefix(max_length: int):
    for index in range(max_length):
        yield q9_boundary_digit(index)


def run(max_length: int, milestones: tuple[int, ...]) -> list[tuple[int, int, int, int]]:
    state: GapState = EMPTY
    reports: list[tuple[int, int, int, int]] = []
    milestone_set = set(milestones)
    previous_residue = 0
    ones = 0

    for length, digit in enumerate(q9_boundary_prefix(max_length), start=1):
        ones += digit
        state = extend(state, digit)
        assert state.residue >= previous_residue
        previous_residue = state.residue
        if length in milestone_set:
            reports.append((length, state.residue.bit_length(), ones, digit))

    return reports


def parse_milestones(raw: str | None, max_length: int) -> tuple[int, ...]:
    if raw is None:
        return tuple(m for m in DEFAULT_MILESTONES if m <= max_length)
    milestones = tuple(sorted({int(part) for part in raw.split(",") if part}))
    if any(m <= 0 or m > max_length for m in milestones):
        raise ValueError("milestones must be positive and at most max-length")
    return milestones


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=DEFAULT_MAX_LENGTH)
    parser.add_argument("--milestones")
    args = parser.parse_args()

    milestones = parse_milestones(args.milestones, args.max_length)
    reports = run(args.max_length, milestones)

    print("q=9 boundary gap-prefix residue diagnostic")
    print(f"max_length={args.max_length}")
    for length, bits, ones, last_digit in reports:
        print(
            f"  L={length:5d} residue_bits={bits:6d} "
            f"ones={ones:5d} last_digit={last_digit}"
        )

    if args.max_length == DEFAULT_MAX_LENGTH and milestones == DEFAULT_MILESTONES:
        expected = (
            (1, 6, 0, 0),
            (2, 17, 1, 1),
            (9, 86, 8, 1),
            (10, 97, 9, 1),
            (81, 614, 16, 0),
            (100, 773, 25, 0),
            (729, 6707, 536, 1),
            (1000, 8931, 644, 1),
        )
        assert tuple(reports) == expected, reports


if __name__ == "__main__":
    main()
