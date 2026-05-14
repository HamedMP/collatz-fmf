"""
explore51_binary_return_code.py

Compresses binary-depth growth-B continuation paths into return blocks

    0 -> 1^r -> 0.

Each block gives an affine map on the normalized depth-0 parameter n:

    n_next = (P_r * n + D_r) / Q_r,

where Q_r = 2^(4r+3), P_r = 9*27^r, and D_r is an integer. A finite sequence
of return blocks therefore imposes one residue class for the initial n modulo
the product of the Q_r. This script computes those prefix codes.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


@dataclass(frozen=True)
class Block:
    ones: int
    p: int
    q: int
    d: int
    gate_residue: int


@dataclass(frozen=True)
class Prefix:
    word: tuple[int, ...]
    p: int
    q: int
    d: int
    residue: int


def transition_coefficients(t: int, next_t: int) -> tuple[int, int, int]:
    if t == 0 and next_t == 0:
        return 9, 1, 3
    if t == 0 and next_t == 1:
        return 9, 0, 4
    if t == 1 and next_t == 0:
        return 27, 7, 3
    if t == 1 and next_t == 1:
        return 27, 6, 4
    raise ValueError((t, next_t))


def block_transitions(ones: int) -> list[tuple[int, int]]:
    if ones == 0:
        return [(0, 0)]
    return [(0, 1)] + [(1, 1)] * (ones - 1) + [(1, 0)]


def block(ones: int) -> Block:
    p = 1
    q = 1
    d = 0
    for t, next_t in block_transitions(ones):
        a, c, e = transition_coefficients(t, next_t)
        p = a * p
        d = a * d + c * q
        q <<= e

    gate_residue = (-d * pow(p, -1, q)) % q
    return Block(ones, p, q, d, gate_residue)


def prefix_code(word: tuple[int, ...]) -> Prefix:
    p = 1
    q = 1
    d = 0
    for ones in word:
        b = block(ones)
        d = b.p * d + b.d * q
        p *= b.p
        q *= b.q
    residue = (-d * pow(p, -1, q)) % q
    return Prefix(word, p, q, d, residue)


def verify_blocks(max_ones: int = 20) -> None:
    for ones in range(max_ones + 1):
        b = block(ones)
        assert b.p == 9 * 27**ones
        assert b.q == 1 << (4 * ones + 3)
        epsilon = 7 if ones % 2 == 0 else 5
        assert (33 * b.gate_residue + 32 - epsilon * 16**ones) % b.q == 0
        if ones == 0:
            assert b.d == 1
        else:
            numerator = 2592 * 27 ** (ones - 1) - 85 * 16**ones
            assert numerator % 11 == 0
            assert b.d == numerator // 11
        assert b.d % 3 == 1
        for k in range(10):
            n = b.gate_residue + k * b.q
            w_num = 33 * n + 32
            assert w_num % 16**ones == 0
            w = w_num // 16**ones
            assert w > 0 and w % 2 == 1
            assert w % 8 == epsilon
            assert (16**ones * w - 32) % 33 == 0
            out_num = b.p * n + b.d
            assert out_num % b.q == 0
            n_next = out_num // b.q
            assert 3 * 27**ones * w - 85 == 88 * n_next
            assert n_next > n
            assert n_next % 3 == 2
    print(
        "Binary return blocks, closed gate, reparameterization, "
        f"and mod-3 trap verified for r <= {max_ones}"
    )


def show_blocks(max_ones: int = 12) -> None:
    print("Binary return block coefficients:")
    for ones in range(max_ones + 1):
        b = block(ones)
        print(
            f"r={ones:2d} q_bits={b.q.bit_length()-1:3d} "
            f"gate={b.gate_residue} d={b.d}"
        )


def scan_prefixes(max_length: int = 8, max_ones: int = 4) -> None:
    print(f"\nSmallest binary return-code prefixes: r <= {max_ones}")
    for length in range(1, max_length + 1):
        best: Prefix | None = None
        for word in product(range(max_ones + 1), repeat=length):
            pfx = prefix_code(word)
            if best is None or (pfx.residue.bit_length(), pfx.residue) < (
                best.residue.bit_length(),
                best.residue,
            ):
                best = pfx
        assert best is not None
        print(
            f"length={length:2d} residue_bits={best.residue.bit_length():4d} "
            f"mod_bits={best.q.bit_length()-1:4d} residue={best.residue} "
            f"word={best.word}"
        )


def verify_return_critical_series(max_length: int = 5, max_ones: int = 5) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_ones + 1), repeat=length):
            pfx = prefix_code(word)
            alpha_product = Fraction(1, 1)
            critical = Fraction(0, 1)
            for ones in word:
                b = block(ones)
                alpha_product *= Fraction(b.p, b.q)
                critical -= Fraction(b.d, b.q) / alpha_product

            assert critical == Fraction(-pfx.d, pfx.p), word
            assert Fraction(-1, 1) <= critical < 0, word
            assert pfx.residue == (-pfx.d * pow(pfx.p, -1, pfx.q)) % pfx.q
            checked += 1

    print(
        f"Binary return critical series verified: length <= {max_length}, "
        f"r <= {max_ones}, words={checked}"
    )


def verify_return_ordinary_landing_divisibility(max_length: int = 5, max_ones: int = 4) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_ones + 1), repeat=length):
            start = prefix_code(word).residue
            for prefix_length in range(1, length + 1):
                prefix = prefix_code(word[:prefix_length])
                exponent = sum(4 * ones + 3 for ones in word[:prefix_length])
                value = prefix.p * start + prefix.d
                assert v2(value) >= exponent, (word, prefix_length, value)
                assert value % prefix.q == 0
            checked += 1

    print(
        f"Binary return ordinary-landing divisibility verified: "
        f"length <= {max_length}, r <= {max_ones}, words={checked}"
    )


def verify_return_prefix_digit_recurrence(max_length: int = 5, max_ones: int = 4) -> None:
    checked = 0
    zero_digits = 0
    for length in range(0, max_length):
        for prefix in product(range(max_ones + 1), repeat=length):
            pfx = prefix_code(prefix)
            u = (pfx.p * pfx.residue + pfx.d) // pfx.q
            assert pfx.p * pfx.residue + pfx.d == pfx.q * u
            for ones in range(max_ones + 1):
                b = block(ones)
                extended = prefix_code(prefix + (ones,))
                digit = (extended.residue - pfx.residue) // pfx.q
                assert extended.residue == pfx.residue + digit * pfx.q

                expected = (
                    -(b.p * u + b.d) * pow(b.p * pfx.p, -1, b.q)
                ) % b.q
                assert digit == expected, (prefix, ones, digit, expected)
                if digit == 0:
                    assert (b.p * u + b.d) % b.q == 0
                    zero_digits += 1
                checked += 1

    print(
        f"Binary return-prefix digit recurrence verified on {checked} extensions "
        f"({zero_digits} zero digits)"
    )


def verify_return_landing_growth_envelope(max_length: int = 5, max_ones: int = 4) -> None:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(max_ones + 1), repeat=length):
            start = prefix_code(word).residue
            prefix = prefix_code(word[:-1])
            n = start
            for ones in word[:-1]:
                b = block(ones)
                numerator = b.p * n + b.d
                assert numerator % b.q == 0, (word, ones, n)
                n = numerator // b.q

            assert n == (prefix.p * start + prefix.d) // prefix.q
            assert n * prefix.q <= (start + 1) * prefix.p

            next_ones = word[-1]
            assert 5 * 16**next_ones <= 33 * n + 32
            assert (
                5 * 16**next_ones * prefix.q
                <= 33 * (start + 1) * prefix.p + 32 * prefix.q
            )
            checked += 1

    print(
        f"Binary return landing growth envelope verified: length <= {max_length}, "
        f"r <= {max_ones}, words={checked}"
    )


if __name__ == "__main__":
    verify_blocks()
    verify_return_critical_series()
    verify_return_ordinary_landing_divisibility()
    verify_return_prefix_digit_recurrence()
    verify_return_landing_growth_envelope()
    show_blocks()
    scan_prefixes()
