"""
explore81_rank_bound_frontier.py

Profiles the finite frontier for the exact unweighted terminal-window/rank
constants requested by the missing Collatz-proof bridge.

For each bound B=2^bits-1 this computes the largest constant needed in

    W_R(B,L) <= C_R (B+1) (2/15)^L
    W_G(B,L) <= C_G B 112^(-L)

over every reachable finite terminal-window level under that height cutoff.
This is diagnostic evidence for the target theorem, not a proof of the uniform
bound.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction

from explore64_terminal_ranks import worst_gap_terminal_rank
from explore64_terminal_ranks import worst_return_terminal_rank


DEFAULT_BITS = tuple(range(24, 61, 4))
EXTENDED_BITS = (64,)

EXPECTED_RETURN = {
    24: (6, 262_143, 2),
    28: (6, 262_143, 2),
    32: (10, 391_188_479, 1),
    36: (11, 8_589_934_591, 3),
    40: (11, 8_589_934_591, 3),
    44: (15, 4_398_046_511_103, 1),
    48: (16, 67_477_744_910_335, 3),
    52: (16, 67_477_744_910_335, 3),
    56: (16, 67_477_744_910_335, 3),
    60: (16, 67_477_744_910_335, 3),
    64: (16, 67_477_744_910_335, 3),
}

EXPECTED_GAP = {
    24: (3, 1_565_883, 4),
    28: (4, 32_679_099, 2),
    32: (4, 32_679_099, 2),
    36: (4, 32_679_099, 2),
    40: (4, 32_679_099, 2),
    44: (4, 32_679_099, 2),
    48: (4, 32_679_099, 2),
    52: (4, 32_679_099, 2),
    56: (4, 32_679_099, 2),
    60: (4, 32_679_099, 2),
    64: (4, 32_679_099, 2),
}


@dataclass(frozen=True)
class FrontierRow:
    bits: int
    return_level: int
    return_terminal: int
    return_rank: int
    return_constant: Fraction
    gap_level: int
    gap_terminal: int
    gap_rank: int
    gap_constant: Fraction


def parse_bits(values: list[str] | None) -> tuple[int, ...]:
    if not values:
        return DEFAULT_BITS
    bits = tuple(int(value) for value in values)
    if any(bit <= 0 for bit in bits):
        raise SystemExit("bit cutoffs must be positive")
    return bits


def frontier_row(bits: int) -> FrontierRow:
    return_worst = worst_return_terminal_rank(bits)
    gap_worst = worst_gap_terminal_rank(bits)
    return FrontierRow(
        bits=bits,
        return_level=return_worst.level,
        return_terminal=return_worst.terminal_coordinate,
        return_rank=return_worst.rank,
        return_constant=return_worst.ratio,
        gap_level=gap_worst.level,
        gap_terminal=gap_worst.terminal_coordinate,
        gap_rank=gap_worst.rank,
        gap_constant=gap_worst.ratio,
    )


def verify_expected(row: FrontierRow) -> None:
    if row.bits in EXPECTED_RETURN:
        expected = EXPECTED_RETURN[row.bits]
        actual = (row.return_level, row.return_terminal, row.return_rank)
        assert actual == expected, (row.bits, "return", actual, expected)

    if row.bits in EXPECTED_GAP:
        expected = EXPECTED_GAP[row.bits]
        actual = (row.gap_level, row.gap_terminal, row.gap_rank)
        assert actual == expected, (row.bits, "gap", actual, expected)


def print_rows(rows: list[FrontierRow]) -> None:
    print("finite rank-bound frontier")
    print(
        "bits  return_level  return_terminal  return_rank  C_R_needed  "
        "gap_level  gap_terminal  gap_rank  C_G_needed"
    )
    for row in rows:
        print(
            f"{row.bits:4d}  "
            f"{row.return_level:12d}  "
            f"{row.return_terminal:15d}  "
            f"{row.return_rank:11d}  "
            f"{float(row.return_constant):10.6f}  "
            f"{row.gap_level:9d}  "
            f"{row.gap_terminal:12d}  "
            f"{row.gap_rank:8d}  "
            f"{float(row.gap_constant):10.6f}"
        )


def summarize(rows: list[FrontierRow]) -> None:
    return_peak = max(rows, key=lambda row: row.return_constant)
    gap_peak = max(rows, key=lambda row: row.gap_constant)
    print(
        "peak return constant: "
        f"C_R >= {float(return_peak.return_constant):.6f} "
        f"at bits={return_peak.bits}, level={return_peak.return_level}, "
        f"terminal={return_peak.return_terminal}, rank={return_peak.return_rank}"
    )
    print(
        "peak gap constant:    "
        f"C_G >= {float(gap_peak.gap_constant):.6f} "
        f"at bits={gap_peak.bits}, level={gap_peak.gap_level}, "
        f"terminal={gap_peak.gap_terminal}, rank={gap_peak.gap_rank}"
    )
    print(
        "scope: finite cutoffs only; this does not prove the uniform "
        "terminal-window/rank theorem."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bits",
        nargs="*",
        help="bit cutoffs B=2^bits-1 to scan; defaults to 24,28,...,60",
    )
    parser.add_argument(
        "--extended",
        action="store_true",
        help="also scan the slower recorded 64-bit spot check",
    )
    args = parser.parse_args()

    bits = parse_bits(args.bits)
    if args.extended and not args.bits:
        bits = bits + EXTENDED_BITS

    rows = [frontier_row(bit) for bit in bits]
    for row in rows:
        verify_expected(row)
    print_rows(rows)
    summarize(rows)


if __name__ == "__main__":
    main()
