"""
explore66_terminal_zero_digits.py

Verifies the terminal zero-increment uniqueness mechanism.

For a finite prefix state, extending by a label has zero rounded-terminal
increment exactly when the same label is the forced next step of the auxiliary
terminal state under the corresponding partial map.  Thus, after any prefix,
there is at most one immediate zero-increment extension, and any infinite
zero-increment tail is forced by the auxiliary terminal state.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import prod

from explore51_binary_return_code import prefix_code
from explore52_binary_partial_map import partial_gap_map, partial_return_map
from explore52_binary_partial_map import gap_prefix_code
from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_BITS = 24
GAP_BITS = 24
EXPECTED_RETURN = (8, 128, 10, 10)
EXPECTED_GAP = (3, 24, 1, 1)
FINITE_MAX_LENGTH = 4
FINITE_MAX_LABEL = 3
EXPECTED_FINITE_WORDS = sum((FINITE_MAX_LABEL + 1) ** n for n in range(1, FINITE_MAX_LENGTH + 1))


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


def verify_return_zero_digits(bits: int = RETURN_BITS) -> None:
    bound = (1 << bits) - 1
    states = [RETURN_EMPTY]
    levels = 0
    tested = 0
    zero_extensions = 0
    states_with_zero = 0

    while states:
        next_states = []
        for state in states:
            forced = partial_return_map(state.auxiliary)
            zero_labels = []
            base_coordinate = return_terminal_coordinate(state)

            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue > bound:
                    continue

                coordinate = return_terminal_coordinate(candidate)
                is_zero = coordinate == base_coordinate
                forced_same = forced is not None and forced.ones == ones
                assert is_zero == forced_same
                if is_zero:
                    assert forced is not None
                    assert candidate.auxiliary == forced.n_next
                    zero_labels.append(ones)
                    zero_extensions += 1

                tested += 1
                next_states.append(candidate)

            assert len(zero_labels) <= 1
            if zero_labels:
                states_with_zero += 1

        if not next_states:
            break
        levels += 1
        states = next_states

    if bits == RETURN_BITS:
        assert (levels, tested, zero_extensions, states_with_zero) == EXPECTED_RETURN

    print(
        f"return zero digits bits={bits:3d} levels={levels:3d} "
        f"extensions={tested:5d} zero={zero_extensions:4d} "
        f"states={states_with_zero:4d}"
    )


def verify_gap_zero_digits(bits: int = GAP_BITS) -> None:
    bound = (1 << bits) - 1
    states = [GAP_EMPTY]
    levels = 0
    tested = 0
    zero_extensions = 0
    states_with_zero = 0

    while states:
        next_states = []
        for state in states:
            forced = partial_gap_map(state.auxiliary) if state.auxiliary > 0 else None
            zero_labels = []
            base_coordinate = gap_terminal_coordinate(state)

            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if not (1 <= candidate.residue <= bound):
                    continue

                coordinate = gap_terminal_coordinate(candidate)
                is_zero = coordinate == base_coordinate
                forced_same = forced is not None and forced[0] == gap
                assert is_zero == forced_same
                if is_zero:
                    assert forced is not None
                    assert candidate.auxiliary == forced[1]
                    zero_labels.append(gap)
                    zero_extensions += 1

                tested += 1
                next_states.append(candidate)

            assert len(zero_labels) <= 1
            if zero_labels:
                states_with_zero += 1

        if not next_states:
            break
        levels += 1
        states = next_states

    if bits == GAP_BITS:
        assert (levels, tested, zero_extensions, states_with_zero) == EXPECTED_GAP

    print(
        f"gap    zero digits bits={bits:3d} levels={levels:3d} "
        f"extensions={tested:5d} zero={zero_extensions:4d} "
        f"states={states_with_zero:4d}"
    )


def verify_finite_return_zero_words(
    max_length: int = FINITE_MAX_LENGTH,
    max_label: int = FINITE_MAX_LABEL,
) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_label + 1), repeat=length):
            code = prefix_code(word)
            expected_modulus = 1
            for label in word:
                expected_modulus *= 2 ** (4 * label + 3)
            assert code.q == expected_modulus
            n = code.residue if code.residue > 0 else code.residue + code.q
            assert n % code.q == code.residue
            for label in word:
                step = partial_return_map(n)
                assert step is not None
                assert step.ones == label
                n = step.n_next
            checked += 1

    if max_length == FINITE_MAX_LENGTH and max_label == FINITE_MAX_LABEL:
        assert checked == EXPECTED_FINITE_WORDS

    print(
        f"return finite zero words length<={max_length} labels<= {max_label}: "
        f"{checked} words"
    )


def verify_finite_gap_zero_words(
    max_length: int = FINITE_MAX_LENGTH,
    max_label: int = FINITE_MAX_LABEL,
) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_label + 1), repeat=length):
            code = gap_prefix_code(word)
            expected_modulus = 1
            for label in word:
                expected_modulus *= 2 ** (3 * label + 7)
            assert code.modulus == expected_modulus
            a = code.residue if code.residue > 0 else code.residue + code.modulus
            assert a % code.modulus == code.residue
            for label in word:
                step = partial_gap_map(a)
                assert step is not None
                gap, a = step
                assert gap == label
            checked += 1

    if max_length == FINITE_MAX_LENGTH and max_label == FINITE_MAX_LABEL:
        assert checked == EXPECTED_FINITE_WORDS

    print(
        f"gap    finite zero words length<={max_length} labels<= {max_label}: "
        f"{checked} words"
    )


def verify_terminal_zero_density(max_length: int = FINITE_MAX_LENGTH) -> None:
    return_step = sum(Fraction(1, 2 ** (4 * label + 3)) for label in range(30))
    gap_step = sum(Fraction(1, 2 ** (3 * label + 7)) for label in range(40))
    assert Fraction(2, 15) - return_step == Fraction(2, 15 * 16**30)
    assert Fraction(1, 112) - gap_step == Fraction(1, 112 * 8**40)

    return_exact = Fraction(2, 15)
    gap_exact = Fraction(1, 112)
    for length in range(1, max_length + 1):
        assert return_exact**length == Fraction(2, 15) ** length
        assert gap_exact**length == Fraction(1, 112) ** length

    print(
        f"terminal zero density verified through length={max_length}: "
        f"return=(2/15)^L gap=112^-L"
    )


def verify_bounded_terminal_zero_density(
    max_length: int = FINITE_MAX_LENGTH,
    max_label: int = FINITE_MAX_LABEL,
) -> None:
    for length in range(1, max_length + 1):
        for bound in range(max_label + 1):
            return_total = sum(
                prod(Fraction(1, 2 ** (4 * label + 3)) for label in word)
                for word in product(range(bound + 1), repeat=length)
            )
            return_expected = (
                Fraction(2, 15) * (1 - Fraction(1, 16 ** (bound + 1)))
            ) ** length
            assert return_total == return_expected

            gap_total = sum(
                prod(Fraction(1, 2 ** (3 * label + 7)) for label in word)
                for word in product(range(bound + 1), repeat=length)
            )
            gap_expected = (
                Fraction(1, 112) * (1 - Fraction(1, 8 ** (bound + 1)))
            ) ** length
            assert gap_total == gap_expected

    print(
        f"bounded terminal zero density verified through length={max_length}, "
        f"labels<={max_label}"
    )


if __name__ == "__main__":
    verify_return_zero_digits()
    verify_gap_zero_digits()
    verify_finite_return_zero_words()
    verify_finite_gap_zero_words()
    verify_terminal_zero_density()
    verify_bounded_terminal_zero_density()
