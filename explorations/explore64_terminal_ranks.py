"""
explore64_terminal_ranks.py

Verifies the terminal-rank formulation of the finite-height discrepancy
problem.

The paper proves that return least residues are recovered by

    R = floor(U / E),

and gap least residues are recovered by

    S = ceil(u / E).

Therefore the critical-rank scans can be performed by sorting finite words by
these rounded normalized terminal coordinates, without separately referring to
prefix residues.  This script checks that formulation against the known small
critical-discrepancy witnesses.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_CASES = (24, 32, 36, 40)
GAP_CASES = (24, 32, 36, 40)

EXPECTED_RETURN_WORST = {
    24: (6, 262_143, 2),
    32: (10, 391_188_479, 1),
    36: (11, 8_589_934_591, 3),
    40: (11, 8_589_934_591, 3),
}

EXPECTED_GAP_WORST = {
    24: (3, 1_565_883, 4),
    32: (4, 32_679_099, 2),
    36: (4, 32_679_099, 2),
    40: (4, 32_679_099, 2),
}

EXPECTED_GAP_MULTIPLICITY = {
    24: (3, 12_053_155, 2),
    32: (3, 12_053_155, 2),
    36: (1, 72_813_864_874, 2),
    40: (1, 72_813_864_874, 2),
}


@dataclass(frozen=True)
class Worst:
    level: int
    terminal_coordinate: int
    rank: int
    ratio: Fraction


def return_levels(bound: int, max_depth: int = 200):
    states = [RETURN_EMPTY]
    for _ in range(max_depth):
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return
        yield next_states
        states = next_states
    raise RuntimeError(f"return search reached max_depth={max_depth}")


def gap_levels(bound: int, max_depth: int = 200):
    states = [GAP_EMPTY]
    for _ in range(max_depth):
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return
        yield next_states
        states = next_states
    raise RuntimeError(f"gap search reached max_depth={max_depth}")


def return_terminal_coordinate(state) -> int:
    normalized_num = state.auxiliary * state.modulus
    coordinate = normalized_num // state.coefficient
    assert coordinate == state.residue
    return coordinate


def gap_terminal_coordinate(state) -> int:
    normalized_num = state.auxiliary * state.modulus
    coordinate = (normalized_num + state.coefficient - 1) // state.coefficient
    assert coordinate == state.residue
    return coordinate


def verify_terminal_depth_bounds() -> None:
    return_checked = 0
    gap_checked = 0

    for bits in RETURN_CASES:
        bound = (1 << bits) - 1
        for level, states in enumerate(return_levels(bound), start=1):
            for state in states:
                assert state.auxiliary * state.modulus >= state.coefficient
                assert state.coefficient * 8**level >= state.modulus * 9**level
                return_checked += 1

    for bits in GAP_CASES:
        bound = (1 << bits) - 1
        for level, states in enumerate(gap_levels(bound), start=1):
            for state in states:
                assert state.auxiliary * 115 * state.modulus > 114 * state.coefficient
                assert state.coefficient * 128**level >= state.modulus * 243**level
                gap_checked += 1

    print(
        f"terminal depth bounds verified: "
        f"return states={return_checked:5d}, gap states={gap_checked:5d}"
    )


def worst_return_terminal_rank(bits: int) -> Worst:
    bound = (1 << bits) - 1
    rho = Fraction(2, 15)
    best = Worst(0, 0, 0, Fraction(0, 1))

    for level, states in enumerate(return_levels(bound), start=1):
        ordered = sorted(states, key=return_terminal_coordinate)
        for rank, state in enumerate(ordered, start=1):
            coordinate = return_terminal_coordinate(state)
            ratio = Fraction(rank, 1) / ((coordinate + 1) * rho**level)
            if ratio > best.ratio:
                best = Worst(level, coordinate, rank, ratio)

    return best


def worst_gap_terminal_rank(bits: int) -> Worst:
    bound = (1 << bits) - 1
    rho = Fraction(1, 112)
    best = Worst(0, 0, 0, Fraction(0, 1))

    for level, states in enumerate(gap_levels(bound), start=1):
        ordered = sorted(states, key=gap_terminal_coordinate)
        for rank, state in enumerate(ordered, start=1):
            coordinate = gap_terminal_coordinate(state)
            ratio = Fraction(rank, 1) / (coordinate * rho**level)
            if ratio > best.ratio:
                best = Worst(level, coordinate, rank, ratio)

    return best


def verify_return_terminal_ranks() -> None:
    for bits in RETURN_CASES:
        worst = worst_return_terminal_rank(bits)
        expected = EXPECTED_RETURN_WORST[bits]
        assert (worst.level, worst.terminal_coordinate, worst.rank) == expected, worst
        print(
            f"return bits={bits:3d} level={worst.level:3d} "
            f"terminal={worst.terminal_coordinate:12d} rank={worst.rank:4d} "
            f"critical={float(worst.ratio):.6f}"
        )


def verify_return_weighted_window(theta: int = 3) -> None:
    for bits in RETURN_CASES:
        bound = (1 << bits) - 1
        worst_ratio = Fraction(0, 1)
        cutoff_checks = 0
        linear_cutoff_checks = 0
        checked = 0
        for states in return_levels(bound):
            seen_terminal_states: set[int] = set()
            weighted = Fraction(0, 1)
            terminal_zeta_sum = Fraction(0, 1)
            inverse_expansions: list[Fraction] = []
            for state in states:
                assert state.auxiliary not in seen_terminal_states
                seen_terminal_states.add(state.auxiliary)

                inverse_expansion = Fraction(state.modulus, state.coefficient)
                assert inverse_expansion <= Fraction(bound + 1, state.auxiliary)
                weighted += inverse_expansion**theta
                terminal_zeta_sum += Fraction(1, state.auxiliary**theta)
                inverse_expansions.append(inverse_expansion)
                checked += 1

            denominator = (bound + 1) ** theta * terminal_zeta_sum
            assert weighted <= denominator
            if denominator:
                worst_ratio = max(worst_ratio, weighted / denominator)

            for cutoff in (1, 2, 4, 8, 16):
                count = sum(
                    1
                    for inverse_expansion in inverse_expansions
                    if inverse_expansion >= Fraction(1, cutoff)
                )
                assert count <= cutoff**theta * denominator
                assert count <= cutoff * (bound + 1) - 1
                cutoff_checks += 1
                linear_cutoff_checks += 1

        print(
            f"return weighted window bits={bits:3d} theta={theta} "
            f"states={checked:5d} cutoffs={cutoff_checks:3d} "
            f"linear={linear_cutoff_checks:3d} "
            f"ratio={float(worst_ratio):.6f}"
        )


def verify_gap_terminal_ranks() -> None:
    for bits in GAP_CASES:
        worst = worst_gap_terminal_rank(bits)
        expected = EXPECTED_GAP_WORST[bits]
        assert (worst.level, worst.terminal_coordinate, worst.rank) == expected, worst
        print(
            f"gap    bits={bits:3d} level={worst.level:3d} "
            f"terminal={worst.terminal_coordinate:12d} rank={worst.rank:4d} "
            f"critical={float(worst.ratio):.6f}"
        )


def zeta_integer_upper_bound(exponent: int) -> Fraction:
    assert exponent > 1
    return Fraction(1, 1) + Fraction(1, exponent - 1)


def verify_gap_weighted_window(theta: int = 3) -> None:
    for bits in GAP_CASES:
        bound = (1 << bits) - 1
        zeta_bound = zeta_integer_upper_bound(theta - 1)
        worst_ratio = Fraction(0, 1)
        checked = 0
        for level, states in enumerate(gap_levels(bound), start=1):
            weighted = sum(
                Fraction(state.modulus, state.coefficient) ** theta for state in states
            )
            denominator = bound**theta * Fraction(43, 81) ** level * zeta_bound
            assert weighted <= denominator
            if denominator:
                worst_ratio = max(worst_ratio, weighted / denominator)
            checked += len(states)

        print(
            f"gap    weighted window bits={bits:3d} theta={theta} "
            f"states={checked:5d} ratio={float(worst_ratio):.6f}"
        )


def verify_gap_distinct_terminal_cutoffs() -> None:
    for bits in GAP_CASES:
        bound = (1 << bits) - 1
        cutoff_checks = 0
        word_count_checks = 0
        for level, states in enumerate(gap_levels(bound), start=1):
            for cutoff in (1, 2, 4, 8, 16):
                low_expansion_states = [
                    state
                    for state in states
                    if Fraction(state.modulus, state.coefficient) >= Fraction(1, cutoff)
                ]
                terminals = {state.auxiliary for state in low_expansion_states}
                assert len(terminals) <= cutoff * bound
                cutoff_checks += 1

                contraction = Fraction(43, 81) ** level
                terminal_counts = Counter(state.auxiliary for state in low_expansion_states)
                local_bound = 0
                for terminal, multiplicity in terminal_counts.items():
                    allowed = contraction * terminal
                    allowed_floor = allowed.numerator // allowed.denominator
                    assert multiplicity <= allowed_floor
                    local_bound += allowed_floor

                max_terminal = cutoff * bound - 1
                global_bound = contraction * max_terminal * (max_terminal + 1) / 2
                assert len(low_expansion_states) <= local_bound
                assert len(low_expansion_states) <= global_bound
                word_count_checks += 1

        print(
            f"gap    distinct terminal cutoffs bits={bits:3d} "
            f"checks={cutoff_checks:3d} word_bounds={word_count_checks:3d}"
        )


def verify_gap_terminal_multiplicity() -> None:
    for bits in GAP_CASES:
        bound = (1 << bits) - 1
        best = (0, 0, 0)
        for level, states in enumerate(gap_levels(bound), start=1):
            counts = Counter(state.auxiliary for state in states)
            terminal, multiplicity = max(counts.items(), key=lambda item: item[1])
            if multiplicity > best[2]:
                best = (level, terminal, multiplicity)

        assert best == EXPECTED_GAP_MULTIPLICITY[bits], best
        print(
            f"gap    terminal multiplicity bits={bits:3d} "
            f"level={best[0]:3d} terminal={best[1]:12d} multiplicity={best[2]:3d}"
        )


if __name__ == "__main__":
    verify_terminal_depth_bounds()
    verify_return_terminal_ranks()
    verify_return_weighted_window()
    verify_gap_terminal_ranks()
    verify_gap_weighted_window()
    verify_gap_distinct_terminal_cutoffs()
    verify_gap_terminal_multiplicity()
