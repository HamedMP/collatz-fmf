"""
explore52_binary_partial_map.py

Verifies the single partial-map formulation of the binary-depth return dynamics.

For a depth-0 return state n, the next binary return block can be read from
33*n + 32.  If

    33*n + 32 = 16^r * w,

with w odd and w congruent to 7 mod 8 for even r, or 5 mod 8 for odd r, then
the branch returns to depth 0 after r ones and

    n_next = (3 * 27^r * w - 85) / 88.

Otherwise the branch exits the binary-depth domain before another depth-0
return.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from explore51_binary_return_code import block, prefix_code


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def v3(n: int) -> int:
    count = 0
    while n % 3 == 0:
        n //= 3
        count += 1
    return count


@dataclass(frozen=True)
class ReturnStep:
    ones: int
    w: int
    n_next: int


@dataclass(frozen=True)
class GapPrefix:
    word: tuple[int, ...]
    coefficient: int
    modulus: int
    constant: int
    residue: int


def transition_step(t: int, n: int) -> tuple[int, int] | None:
    if t == 0 and n % 8 == 7:
        return 0, (9 * n + 1) // 8
    if t == 0 and n % 16 == 0:
        return 1, 9 * n // 16
    if t == 1 and n % 8 == 3:
        return 0, (27 * n + 7) // 8
    if t == 1 and n % 16 == 14:
        return 1, (27 * n + 6) // 16
    return None


def simulated_return(n: int, max_ones: int = 10_000) -> ReturnStep | None:
    start_n = n
    step = transition_step(0, n)
    if step is None:
        return None

    t, n = step
    if t == 0:
        w = 33 * start_n + 32
        return ReturnStep(0, w, n)

    ones = 1
    while ones <= max_ones:
        step = transition_step(t, n)
        if step is None:
            return None
        t, n = step
        if t == 0:
            w = (33 * start_n + 32) // 16**ones
            return ReturnStep(ones, w, n)
        ones += 1

    raise RuntimeError("return search exceeded max_ones")


def partial_return_map(n: int) -> ReturnStep | None:
    value = 33 * n + 32
    exponent = v2(value)
    if exponent % 4 != 0:
        return None

    ones = exponent // 4
    w = value >> exponent
    epsilon = 7 if ones % 2 == 0 else 5
    if w % 8 != epsilon:
        return None

    numerator = 3 * 27**ones * w - 85
    if numerator % 88 != 0:
        return None

    return ReturnStep(ones, w, numerator // 88)


def partial_gap_map(a: int) -> tuple[int, int] | None:
    exponent = v2(a)
    if exponent % 3 != 0:
        return None

    gap = exponent // 3
    b = a >> exponent
    if (3 * pow(9, gap, 128) * (b % 128) - 49) % 128 != 0:
        return None

    numerator = 3 ** (2 * gap + 5) * b - 1
    if numerator % 128 != 0:
        return None

    return gap, numerator // 128


def gap_prefix_code(word: tuple[int, ...]) -> GapPrefix:
    coefficient = 1
    modulus = 1
    constant = 0

    for gap in word:
        step_coefficient = 3 ** (2 * gap + 5)
        step_modulus = 2 ** (3 * gap + 7)
        step_constant = 8**gap
        constant = step_coefficient * constant + step_constant * modulus
        coefficient *= step_coefficient
        modulus *= step_modulus

    residue = (constant * pow(coefficient, -1, modulus)) % modulus
    return GapPrefix(word, coefficient, modulus, constant, residue)


def verify_partial_map(limit: int = 2_000_000) -> None:
    for n in range(limit + 1):
        direct = partial_return_map(n)
        simulated = simulated_return(n)

        if direct is None:
            assert simulated is None, (n, direct, simulated)
            continue

        assert simulated is not None, (n, direct, simulated)
        assert direct.ones == simulated.ones, (n, direct, simulated)
        assert direct.w == simulated.w, (n, direct, simulated)
        assert direct.n_next == simulated.n_next, (n, direct, simulated)
        assert direct.w == (33 * n + 32) // 16**direct.ones
        assert direct.n_next > n

    print(f"Binary partial return map verified for 0 <= n <= {limit}")


def verify_survival_density(max_returns: int = 8, max_ones: int = 40) -> None:
    one_step = sum(Fraction(1, 2 ** (4 * r + 3)) for r in range(max_ones + 1))
    exact_one_step = Fraction(2, 15)
    tail = exact_one_step - one_step
    assert tail == Fraction(2, 15 * 16 ** (max_ones + 1))

    print(f"One-return density: {exact_one_step}")
    for length in range(1, max_returns + 1):
        density = exact_one_step**length
        print(f"  return length >= {length}: density {density}")


def verify_return_length_law(max_ones: int = 12, max_bound: int = 6) -> None:
    one_step = Fraction(2, 15)
    mean = sum(Fraction(r * 15, 16 ** (r + 1)) for r in range(max_ones + 1))
    tail_mean = Fraction(1, 15) - mean
    assert tail_mean > 0

    print("Conditional return-length law:")
    for r in range(max_ones + 1):
        density = Fraction(1, 2 ** (4 * r + 3))
        conditional = density / one_step
        assert conditional == Fraction(15, 16 ** (r + 1))
        print(f"  r={r:2d}: P={conditional}")

    for bound in range(max_bound + 1):
        bounded = sum(Fraction(1, 2 ** (4 * r + 3)) for r in range(bound + 1))
        assert bounded == Fraction(2, 15) * (1 - Fraction(1, 16 ** (bound + 1)))


def verify_return_odd_modulus_independence(
    max_ones: int = 12,
    max_length: int = 4,
    max_word_ones: int = 4,
    odd_moduli: tuple[int, ...] = (3, 5, 7, 9, 11, 13, 25, 81),
) -> None:
    exact_one_step = Fraction(2, 15)
    for modulus in odd_moduli:
        assert modulus % 2 == 1
        for residue in range(modulus):
            for ones in range(max_ones + 1):
                dyadic_modulus = 2 ** (4 * ones + 3)
                b = block(ones)
                assert gcd(modulus, dyadic_modulus) == 1

                combined = (
                    b.gate_residue
                    + dyadic_modulus
                    * (
                        (residue - b.gate_residue)
                        * pow(dyadic_modulus, -1, modulus)
                    )
                ) % (modulus * dyadic_modulus)
                assert combined % modulus == residue
                assert combined % dyadic_modulus == b.gate_residue

                relative_density = Fraction(1, dyadic_modulus)
                conditional = relative_density / exact_one_step
                assert conditional == Fraction(15, 16 ** (ones + 1))

    checked_words = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_word_ones + 1), repeat=length):
            pfx = prefix_code(word)
            expected_density = Fraction(1, pfx.q)
            for ones in word:
                expected_density *= 2 ** (4 * ones + 3)
            assert expected_density == 1

            for modulus in odd_moduli:
                for residue in range(modulus):
                    assert gcd(modulus, pfx.q) == 1
                    combined = (
                        pfx.residue
                        + pfx.q
                        * ((residue - pfx.residue) * pow(pfx.q, -1, modulus))
                    ) % (modulus * pfx.q)
                    assert combined % modulus == residue
                    assert combined % pfx.q == pfx.residue
            checked_words += 1

    print(
        "Binary return odd-modulus independence verified for "
        f"odd moduli {odd_moduli}, r <= {max_ones}, "
        f"finite words={checked_words}"
    )


def verify_return_reset_neighborhood_transparency(
    max_s: int = 4,
    max_length: int = 4,
    max_word_ones: int = 4,
) -> None:
    checked_words = 0
    for s in range(1, max_s + 1):
        reset_modulus = 3**s
        reset_residue = (-85 * pow(88, -1, reset_modulus)) % reset_modulus
        assert (88 * reset_residue + 85) % reset_modulus == 0

        for length in range(1, max_length + 1):
            for bound in range(max_word_ones + 1):
                total = Fraction(0, 1)
                for word in product(range(bound + 1), repeat=length):
                    pfx = prefix_code(word)
                    assert gcd(reset_modulus, pfx.q) == 1
                    combined = (
                        pfx.residue
                        + pfx.q
                        * (
                            (reset_residue - pfx.residue)
                            * pow(pfx.q, -1, reset_modulus)
                        )
                    ) % (reset_modulus * pfx.q)
                    assert combined % reset_modulus == reset_residue
                    assert combined % pfx.q == pfx.residue

                    density = Fraction(1, pfx.q)
                    expected = Fraction(1, 1)
                    for ones in word:
                        expected *= Fraction(1, 2 ** (4 * ones + 3))
                    assert density == expected
                    total += density
                    checked_words += 1

                restricted = (
                    Fraction(2, 15) * (1 - Fraction(1, 16 ** (bound + 1)))
                ) ** length
                assert total == restricted

    print(
        "Binary return reset-neighborhood transparency verified for "
        f"3^s, s <= {max_s}, length <= {max_length}, r <= {max_word_ones}"
    )


def verify_y_normal_form(limit: int = 1_000_000) -> None:
    checked = 0
    for n in range(limit + 1):
        step = partial_return_map(n)
        if step is None:
            continue

        y = 33 * n + 32
        y_next = 33 * step.n_next + 32
        assert y == 16**step.ones * step.w
        assert 8 * y_next == 9 * 27**step.ones * step.w + 1
        assert 8 * 16**step.ones * y_next == 9 * 27**step.ones * y + 16**step.ones
        assert y_next > y
        checked += 1

    print(f"Binary y-normal form verified on {checked} returns for n <= {limit}")


def verify_all_zero_branch(max_length: int = 20) -> None:
    for length in range(1, max_length + 1):
        n = 8**length - 1
        for index in range(length + 1):
            assert n == 9**index * 8 ** (length - index) - 1
            if index == length:
                break
            step = partial_return_map(n)
            assert step is not None and step.ones == 0, (length, index, n, step)
            n = step.n_next

    print(f"All-zero binary return branch verified for L <= {max_length}")


def verify_periodic_return_obstruction(max_period: int = 5, max_ones: int = 5) -> None:
    checked = 0
    for period in range(1, max_period + 1):
        for word in product(range(max_ones + 1), repeat=period):
            multiplier = Fraction(1, 1)
            offset = Fraction(0, 1)
            for ones in word:
                alpha = Fraction(9 * 27**ones, 8 * 16**ones)
                offset = alpha * offset + Fraction(1, 8)
                multiplier *= alpha

            assert multiplier > 1
            fixed = offset / (1 - multiplier)
            assert fixed < 0, (word, fixed)
            checked += 1

    print(
        f"Periodic binary return obstruction verified: periods <= {max_period}, "
        f"r <= {max_ones}, words={checked}"
    )


def verify_periodic_gap_obstruction(max_period: int = 5, max_gap: int = 5) -> None:
    checked = 0
    for period in range(1, max_period + 1):
        for word in product(range(max_gap + 1), repeat=period):
            multiplier = Fraction(1, 1)
            offset = Fraction(0, 1)
            for gap in word:
                alpha = Fraction(243, 128) * Fraction(9, 8) ** gap
                offset = alpha * offset - Fraction(1, 128)
                multiplier *= alpha

            assert multiplier > 1
            fixed = -offset / (multiplier - 1)
            assert 0 < fixed < 1, (word, fixed)
            checked += 1

    print(
        f"Periodic {{0,1}} gap obstruction verified: periods <= {max_period}, "
        f"gaps <= {max_gap}, words={checked}"
    )


def verify_all_zero_gap_branch(max_length: int = 12) -> None:
    for length in range(1, max_length + 1):
        modulus = 128**length
        a = pow(115, -1, modulus)
        assert (115 * a - 1) % modulus == 0
        for index in range(length):
            assert (115 * a - 1) % 128 ** (length - index) == 0
            numerator = 243 * a - 1
            assert numerator % 128 == 0
            a = numerator // 128

    print(f"All-zero {{0,1}} gap branch verified for L <= {max_length}")


def verify_constant_gap_branch(max_gap: int = 8, max_length: int = 6) -> None:
    for gap in range(max_gap + 1):
        coefficient = 3 ** (2 * gap + 5)
        modulus_step = 2 ** (3 * gap + 7)
        constant = 8**gap
        denominator = coefficient - modulus_step
        assert denominator > constant

        for length in range(1, max_length + 1):
            modulus = modulus_step**length
            a = (constant * pow(denominator, -1, modulus)) % modulus
            assert (denominator * a - constant) % modulus == 0

            current = a
            for _ in range(length):
                numerator = coefficient * current - constant
                assert numerator % modulus_step == 0, (gap, length, current)
                current = numerator // modulus_step

    print(f"Constant {{0,1}} gap branches verified for gaps <= {max_gap}, L <= {max_length}")


def verify_finite_word_realization(max_length: int = 5, max_ones: int = 5) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_ones + 1), repeat=length):
            pfx = prefix_code(word)
            n = pfx.residue
            realized = []
            for _ in word:
                step = partial_return_map(n)
                assert step is not None, (word, pfx, realized)
                realized.append(step.ones)
                n = step.n_next
            assert tuple(realized) == word, (word, tuple(realized), pfx)
            checked += 1

    print(
        f"Finite binary return words verified: length <= {max_length}, "
        f"r <= {max_ones}, words={checked}"
    )


def verify_3_adic_reset(max_ones: int = 12, samples: int = 20) -> None:
    for ones in range(max_ones + 1):
        modulus = 3 ** (3 * ones + 2)
        residue = ((2 * 3 ** (3 * ones + 1) - 85) * pow(88, -1, modulus)) % modulus
        b = block(ones)
        for k in range(samples):
            n = b.gate_residue + k * b.q
            step = partial_return_map(n)
            assert step is not None and step.ones == ones, (ones, n, step)
            assert step.n_next % modulus == residue, (ones, n, step, residue)

    print(f"Binary 3-adic reset verified for r <= {max_ones}")


def verify_binary_gap_clock(max_gap: int = 12, samples: int = 5) -> None:
    for gap in range(max_gap + 1):
        word = (1,) + (0,) * gap + (1,)
        pfx = prefix_code(word)
        modulus = pfx.q
        for sample in range(samples):
            n = pfx.residue + sample * modulus
            first = partial_return_map(n)
            assert first is not None and first.ones == 1, (gap, sample, first)
            n = first.n_next
            assert v3(n + 1) == 1, (gap, sample, n)
            for index in range(gap):
                step = partial_return_map(n)
                assert step is not None and step.ones == 0, (gap, sample, index, step)
                n = step.n_next
                assert v3(n + 1) == 2 * (index + 1) + 1, (gap, sample, index, n)
            final = partial_return_map(n)
            assert final is not None and final.ones == 1, (gap, sample, final)

    print(f"Binary {{0,1}} gap 3-adic clock verified for gaps <= {max_gap}")


def verify_binary_gap_map(max_gap: int = 12, samples: int = 5) -> None:
    for gap in range(max_gap + 1):
        word = (1,) + (0,) * gap + (1,)
        pfx = prefix_code(word)
        modulus = pfx.q
        for sample in range(samples):
            n = pfx.residue + sample * modulus
            first = partial_return_map(n)
            assert first is not None and first.ones == 1, (gap, sample, first)
            n = first.n_next
            assert (n + 1) % 3 == 0, (gap, sample, n)
            a = (n + 1) // 3

            for _ in range(gap):
                step = partial_return_map(n)
                assert step is not None and step.ones == 0, (gap, sample, step)
                n = step.n_next

            final = partial_return_map(n)
            assert final is not None and final.ones == 1, (gap, sample, final)
            n_next = final.n_next
            assert (n_next + 1) % 3 == 0, (gap, sample, n_next)
            a_next = (n_next + 1) // 3

            numerator = 3 ** (2 * gap + 5) * a - 8**gap
            denominator = 2 ** (3 * gap + 7)
            assert numerator % denominator == 0, (gap, sample, numerator)
            assert a_next == numerator // denominator, (gap, sample, a, a_next)
            assert a_next == Fraction(243, 128) * Fraction(9, 8) ** gap * a - Fraction(1, 128)
            assert a_next > a, (gap, sample, a, a_next)

    print(f"Binary {{0,1}} gap map verified for gaps <= {max_gap}")


def verify_binary_gap_critical_series(max_length: int = 5, max_gap: int = 4) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_gap + 1), repeat=length):
            pfx = gap_prefix_code(gaps)
            alpha_product = Fraction(1, 1)
            critical = Fraction(0, 1)
            for gap in gaps:
                alpha_product *= Fraction(243, 128) * Fraction(9, 8) ** gap
                critical += Fraction(1, 128) / alpha_product

            assert critical == Fraction(pfx.constant, pfx.coefficient), gaps
            assert 0 < critical < Fraction(1, 115), gaps
            assert (
                pfx.residue
                == (pfx.constant * pow(pfx.coefficient, -1, pfx.modulus))
                % pfx.modulus
            )
            assert (pfx.coefficient * pfx.residue - pfx.constant) % pfx.modulus == 0
            checked += 1

    print(
        f"Binary {{0,1}} gap critical series verified: length <= {max_length}, "
        f"gaps <= {max_gap}, words={checked}"
    )


def verify_binary_gap_ordinary_landing_divisibility(
    max_length: int = 5,
    max_gap: int = 4,
) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_gap + 1), repeat=length):
            start = gap_prefix_code(gaps).residue
            for prefix_length in range(1, length + 1):
                prefix = gap_prefix_code(gaps[:prefix_length])
                exponent = sum(3 * gap + 7 for gap in gaps[:prefix_length])
                value = prefix.coefficient * start - prefix.constant
                assert v2(value) >= exponent, (gaps, prefix_length, value)
                assert value % prefix.modulus == 0
            checked += 1

    print(
        f"Binary {{0,1}} gap ordinary-landing divisibility verified: "
        f"length <= {max_length}, gaps <= {max_gap}, words={checked}"
    )


def verify_binary_gap_landing_growth_envelope(max_length: int = 5, max_gap: int = 4) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_gap + 1), repeat=length):
            start = gap_prefix_code(gaps).residue
            prefix = gap_prefix_code(gaps[:-1])
            a = start
            for gap in gaps[:-1]:
                numerator = 3 ** (2 * gap + 5) * a - 8**gap
                denominator = 2 ** (3 * gap + 7)
                assert numerator % denominator == 0, (gaps, gap, a)
                a = numerator // denominator

            assert a == (prefix.coefficient * start - prefix.constant) // prefix.modulus
            assert a * prefix.modulus <= start * prefix.coefficient

            next_gap = gaps[-1]
            assert 8**next_gap <= a
            assert 8**next_gap * prefix.modulus <= start * prefix.coefficient
            checked += 1

    print(
        f"Binary {{0,1}} gap landing growth envelope verified: "
        f"length <= {max_length}, gaps <= {max_gap}, words={checked}"
    )


def verify_binary_gap_partial_map(max_gap: int = 12, samples: int = 5) -> None:
    for gap in range(max_gap + 1):
        word = (1,) + (0,) * gap + (1,)
        pfx = prefix_code(word)
        modulus = pfx.q
        for sample in range(samples):
            n = pfx.residue + sample * modulus
            first = partial_return_map(n)
            assert first is not None and first.ones == 1, (gap, sample, first)
            n = first.n_next
            a = (n + 1) // 3

            gap_step = partial_gap_map(a)
            assert gap_step is not None and gap_step[0] == gap, (gap, sample, a, gap_step)
            assert a % 8**gap == 0, (gap, sample, a)
            b = a // 8**gap
            assert b % 2 == 1, (gap, sample, b)
            assert (3 * 9**gap * b - 49) % 128 == 0, (gap, sample, b)

            for _ in range(gap):
                step = partial_return_map(n)
                assert step is not None and step.ones == 0, (gap, sample, step)
                n = step.n_next
            final = partial_return_map(n)
            assert final is not None and final.ones == 1, (gap, sample, final)
            a_next = (final.n_next + 1) // 3
            assert a_next == (3 ** (2 * gap + 5) * b - 1) // 128
            assert gap_step[1] == a_next

    print(f"Binary {{0,1}} gap partial map verified for gaps <= {max_gap}")


def verify_finite_gap_word_realization(max_length: int = 4, max_gap: int = 5) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_gap + 1), repeat=length):
            return_word = [1]
            for gap in gaps:
                return_word.extend([0] * gap)
                return_word.append(1)

            pfx = prefix_code(tuple(return_word))
            n = pfx.residue
            first = partial_return_map(n)
            assert first is not None and first.ones == 1, (gaps, first)
            n = first.n_next
            a = (n + 1) // 3

            realized = []
            for gap in gaps:
                actual_gap = 0
                while True:
                    step = partial_return_map(n)
                    assert step is not None, (gaps, realized, actual_gap)
                    if step.ones == 1:
                        n = step.n_next
                        break
                    assert step.ones == 0, (gaps, realized, step)
                    actual_gap += 1
                    n = step.n_next
                realized.append(actual_gap)

            assert tuple(realized) == gaps, (gaps, tuple(realized), a)
            checked += 1

    print(
        f"Finite {{0,1}} gap words verified: length <= {max_length}, "
        f"gaps <= {max_gap}, words={checked}"
    )


def verify_gap_prefix_code(max_length: int = 4, max_gap: int = 5) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_gap + 1), repeat=length):
            pfx = gap_prefix_code(gaps)
            a = pfx.residue
            for gap in gaps:
                numerator = 3 ** (2 * gap + 5) * a - 8**gap
                denominator = 2 ** (3 * gap + 7)
                assert numerator % denominator == 0, (gaps, a, gap)
                a = numerator // denominator
            checked += 1

    print(
        f"Gap-prefix codes verified: length <= {max_length}, "
        f"gaps <= {max_gap}, words={checked}"
    )


def verify_gap_prefix_monotonicity() -> None:
    word = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
    previous = -1
    plateau = False
    for length in range(1, len(word) + 1):
        residue = gap_prefix_code(word[:length]).residue
        assert residue >= previous
        if residue == previous:
            assert length == 16
            plateau = True
        previous = residue

    assert plateau
    print("Gap-prefix monotonicity and finite plateau example verified")


def verify_gap_prefix_digit_recurrence(max_length: int = 5, max_gap: int = 4) -> None:
    checked = 0
    zero_digits = 0
    for length in range(0, max_length):
        for prefix in product(range(max_gap + 1), repeat=length):
            pfx = gap_prefix_code(prefix)
            u = (pfx.coefficient * pfx.residue - pfx.constant) // pfx.modulus
            assert pfx.coefficient * pfx.residue - pfx.constant == pfx.modulus * u
            for gap in range(max_gap + 1):
                extended = gap_prefix_code(prefix + (gap,))
                digit = (extended.residue - pfx.residue) // pfx.modulus
                assert extended.residue == pfx.residue + digit * pfx.modulus

                p = 3 ** (2 * gap + 5)
                q = 2 ** (3 * gap + 7)
                c = 8**gap
                expected = ((c - p * u) * pow(p * pfx.coefficient, -1, q)) % q
                assert digit == expected, (prefix, gap, digit, expected)
                if digit == 0:
                    assert (p * u - c) % q == 0
                    zero_digits += 1
                checked += 1

    print(
        f"Gap-prefix digit recurrence verified on {checked} extensions "
        f"({zero_digits} zero digits)"
    )


def verify_binary_gap_survival_density(max_gap: int = 12, max_length: int = 6) -> None:
    one_step = sum(Fraction(1, 2 ** (3 * gap + 7)) for gap in range(max_gap + 1))
    exact_one_step = Fraction(1, 112)
    tail = exact_one_step - one_step
    assert tail == Fraction(1, 112 * 8 ** (max_gap + 1))

    print(f"Binary {{0,1}} gap one-step density: {exact_one_step}")
    for length in range(1, max_length + 1):
        print(f"  gap transitions >= {length}: density {exact_one_step**length}")

    for gap in range(max_gap + 1):
        density = Fraction(1, 2 ** (3 * gap + 7))
        conditional = density / exact_one_step
        assert conditional == Fraction(7, 8 ** (gap + 1))

    mean = sum(Fraction(gap * 7, 8 ** (gap + 1)) for gap in range(max_gap + 1))
    assert Fraction(1, 7) - mean > 0
    print(f"Binary {{0,1}} conditional gap law verified for gaps <= {max_gap}")


def verify_binary_gap_odd_modulus_independence(
    max_gap: int = 12,
    max_length: int = 4,
    max_word_gap: int = 4,
    odd_moduli: tuple[int, ...] = (3, 5, 7, 9, 11, 13, 25, 81),
) -> None:
    exact_one_step = Fraction(1, 112)
    for modulus in odd_moduli:
        assert modulus % 2 == 1
        for residue in range(modulus):
            for gap in range(max_gap + 1):
                dyadic_modulus = 2 ** (3 * gap + 7)
                dyadic_residue = (
                    8**gap * 49 * pow(3 * 9**gap, -1, 128)
                ) % dyadic_modulus
                assert gcd(modulus, dyadic_modulus) == 1

                combined = (
                    dyadic_residue
                    + dyadic_modulus
                    * (
                        (residue - dyadic_residue)
                        * pow(dyadic_modulus, -1, modulus)
                    )
                ) % (modulus * dyadic_modulus)
                assert combined % modulus == residue
                assert combined % dyadic_modulus == dyadic_residue

                relative_density = Fraction(1, dyadic_modulus)
                conditional = relative_density / exact_one_step
                assert conditional == Fraction(7, 8 ** (gap + 1))

    checked_words = 0
    for length in range(1, max_length + 1):
        for gaps in product(range(max_word_gap + 1), repeat=length):
            pfx = gap_prefix_code(gaps)
            expected_density = Fraction(1, pfx.modulus)
            for gap in gaps:
                expected_density *= 2 ** (3 * gap + 7)
            assert expected_density == 1

            for modulus in odd_moduli:
                for residue in range(modulus):
                    assert gcd(modulus, pfx.modulus) == 1
                    combined = (
                        pfx.residue
                        + pfx.modulus
                        * (
                            (residue - pfx.residue)
                            * pow(pfx.modulus, -1, modulus)
                        )
                    ) % (modulus * pfx.modulus)
                    assert combined % modulus == residue
                    assert combined % pfx.modulus == pfx.residue
            checked_words += 1

    print(
        "Binary {0,1} odd-modulus independence verified for "
        f"odd moduli {odd_moduli}, gaps <= {max_gap}, "
        f"finite words={checked_words}"
    )


def verify_binary_gap_reset_neighborhood_transparency(
    max_s: int = 4,
    max_length: int = 4,
    max_word_gap: int = 4,
) -> None:
    checked_words = 0
    for s in range(1, max_s + 1):
        reset_modulus = 3**s
        reset_residue = (-pow(128, -1, reset_modulus)) % reset_modulus
        assert (128 * reset_residue + 1) % reset_modulus == 0

        for length in range(1, max_length + 1):
            for bound in range(max_word_gap + 1):
                total = Fraction(0, 1)
                for gaps in product(range(bound + 1), repeat=length):
                    pfx = gap_prefix_code(gaps)
                    assert gcd(reset_modulus, pfx.modulus) == 1
                    combined = (
                        pfx.residue
                        + pfx.modulus
                        * (
                            (reset_residue - pfx.residue)
                            * pow(pfx.modulus, -1, reset_modulus)
                        )
                    ) % (reset_modulus * pfx.modulus)
                    assert combined % reset_modulus == reset_residue
                    assert combined % pfx.modulus == pfx.residue

                    density = Fraction(1, pfx.modulus)
                    expected = Fraction(1, 1)
                    for gap in gaps:
                        expected *= Fraction(1, 2 ** (3 * gap + 7))
                    assert density == expected
                    total += density
                    checked_words += 1

                restricted = (
                    Fraction(1, 112) * (1 - Fraction(1, 8 ** (bound + 1)))
                ) ** length
                assert total == restricted

    print(
        "Binary {0,1} gap reset-neighborhood transparency verified for "
        f"3^s, s <= {max_s}, length <= {max_length}, gaps <= {max_word_gap}"
    )


def verify_binary_gap_core_recurrence(max_gap: int = 8, samples: int = 3) -> None:
    for gap in range(max_gap + 1):
        for next_gap in range(max_gap + 1):
            word = (1,) + (0,) * gap + (1,) + (0,) * next_gap + (1,)
            pfx = prefix_code(word)
            modulus = pfx.q
            for sample in range(samples):
                n = pfx.residue + sample * modulus
                first = partial_return_map(n)
                assert first is not None and first.ones == 1, (gap, next_gap, sample, first)
                n = first.n_next
                a = (n + 1) // 3
                assert a % 8**gap == 0, (gap, next_gap, sample, a)
                b = a // 8**gap
                assert b % 2 == 1
                assert (3 * 9**gap * b - 49) % 128 == 0

                for _ in range(gap):
                    step = partial_return_map(n)
                    assert step is not None and step.ones == 0, (gap, next_gap, sample, step)
                    n = step.n_next
                final = partial_return_map(n)
                assert final is not None and final.ones == 1, (gap, next_gap, sample, final)
                n = final.n_next
                a_next = (n + 1) // 3
                assert a_next % 8**next_gap == 0
                b_next = a_next // 8**next_gap
                assert b_next % 2 == 1
                assert 2 ** (3 * next_gap + 7) * b_next == 3 ** (2 * gap + 5) * b - 1
                assert b_next % 3 == ((-1) ** next_gap) % 3

    print(f"Binary {{0,1}} gap-core recurrence verified for gaps <= {max_gap}")


def verify_binary_post_one_3_adic_reset(max_gap: int = 12, samples: int = 5) -> None:
    fixed_mod_81 = (-pow(128, -1, 81)) % 81
    assert fixed_mod_81 == 31

    for gap in range(max_gap + 1):
        word = (1,) + (0,) * gap + (1,)
        pfx = prefix_code(word)
        modulus = pfx.q
        reset_modulus = 3 ** (2 * gap + 5)
        reset_residue = (-pow(128, -1, reset_modulus)) % reset_modulus
        for sample in range(samples):
            n = pfx.residue + sample * modulus
            first = partial_return_map(n)
            assert first is not None and first.ones == 1, (gap, sample, first)
            n = first.n_next
            for _ in range(gap):
                step = partial_return_map(n)
                assert step is not None and step.ones == 0, (gap, sample, step)
                n = step.n_next
            final = partial_return_map(n)
            assert final is not None and final.ones == 1, (gap, sample, final)
            a_next = (final.n_next + 1) // 3
            assert a_next % reset_modulus == reset_residue, (gap, sample, a_next)
            assert a_next % 81 == 31, (gap, sample, a_next)

    print(f"Binary {{0,1}} post-one 3-adic reset verified for gaps <= {max_gap}")


def scan_long_orbits(limit: int = 20_000_000, max_returns: int = 20) -> None:
    best_length = 0
    best = None

    for n0 in range(limit + 1):
        n = n0
        word: list[int] = []
        for _ in range(max_returns):
            step = partial_return_map(n)
            if step is None:
                break
            word.append(step.ones)
            n = step.n_next

        if len(word) > best_length:
            best_length = len(word)
            best = (n0, tuple(word), n)

    print(f"Longest binary return orbit for n <= {limit}: {best}")


def scan_gap_orbits(limit: int = 5_000_000, max_transitions: int = 20) -> None:
    best_length = 0
    best = None

    for a0 in range(1, limit + 1):
        a = a0
        word: list[int] = []
        for _ in range(max_transitions):
            step = partial_gap_map(a)
            if step is None:
                break
            gap, a = step
            word.append(gap)

        if len(word) > best_length:
            best_length = len(word)
            best = (a0, tuple(word), a)

    print(f"Longest binary {{0,1}} gap orbit for a <= {limit}: {best}")


if __name__ == "__main__":
    verify_partial_map()
    verify_survival_density()
    verify_return_length_law()
    verify_return_odd_modulus_independence()
    verify_return_reset_neighborhood_transparency()
    verify_y_normal_form()
    verify_all_zero_branch()
    verify_periodic_return_obstruction()
    verify_periodic_gap_obstruction()
    verify_all_zero_gap_branch()
    verify_constant_gap_branch()
    verify_finite_word_realization()
    verify_3_adic_reset()
    verify_binary_gap_clock()
    verify_binary_gap_map()
    verify_binary_gap_critical_series()
    verify_binary_gap_ordinary_landing_divisibility()
    verify_binary_gap_landing_growth_envelope()
    verify_binary_gap_partial_map()
    verify_finite_gap_word_realization()
    verify_gap_prefix_code()
    verify_gap_prefix_monotonicity()
    verify_gap_prefix_digit_recurrence()
    verify_binary_gap_survival_density()
    verify_binary_gap_odd_modulus_independence()
    verify_binary_gap_reset_neighborhood_transparency()
    verify_binary_gap_core_recurrence()
    verify_binary_post_one_3_adic_reset()
    scan_long_orbits()
    scan_gap_orbits()
