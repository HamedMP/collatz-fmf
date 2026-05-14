"""
explore67_constant_branches.py

Verifies the constant-branch formulas for one-letter return and reduced-gap
alphabets.

Return:

    n_* = -D_r / (P_r - Q_r),       n_0 == n_* (mod Q_r^L).

Gap:

    a_* = 8^k / (3^(2k+5) - 2^(3k+7)),
    a_0 == a_* (mod Q_k^L).

These are the explicit base cases for bounded alphabets: every one-letter
alphabet has arbitrarily long finite shadows, but its infinite 2-adic code is
not a positive ordinary integer.
"""

from __future__ import annotations

from fractions import Fraction

from explore51_binary_return_code import block, prefix_code
from explore52_binary_partial_map import gap_prefix_code, partial_gap_map, partial_return_map


def verify_constant_return(max_ones: int = 8, max_length: int = 6, samples: int = 3) -> None:
    checked = 0
    for ones in range(max_ones + 1):
        step = block(ones)
        fixed = Fraction(-step.d, step.p - step.q)
        assert Fraction(-1, 1) <= fixed < 0
        assert (step.p - step.q) % 2 == 1

        for length in range(1, max_length + 1):
            modulus = step.q**length
            expected = (-step.d * pow(step.p - step.q, -1, modulus)) % modulus
            assert prefix_code((ones,) * length).residue == expected

            for offset in range(samples):
                n = expected + offset * modulus
                for _ in range(length):
                    actual = partial_return_map(n)
                    assert actual is not None
                    assert actual.ones == ones
                    n = actual.n_next
                checked += 1

    print(
        "Constant return branches verified: "
        f"r <= {max_ones}, length <= {max_length}, samples={samples}, checks={checked}"
    )


def verify_constant_gap(max_gap: int = 8, max_length: int = 6, samples: int = 3) -> None:
    checked = 0
    for gap in range(max_gap + 1):
        coefficient = 3 ** (2 * gap + 5)
        modulus_one = 2 ** (3 * gap + 7)
        constant = 8**gap
        denominator = coefficient - modulus_one
        fixed = Fraction(constant, denominator)
        assert 0 < fixed < 1
        assert denominator % 2 == 1

        for length in range(1, max_length + 1):
            modulus = modulus_one**length
            expected = (constant * pow(denominator, -1, modulus)) % modulus
            assert gap_prefix_code((gap,) * length).residue == expected

            for offset in range(samples):
                a = expected + offset * modulus
                for _ in range(length):
                    actual = partial_gap_map(a)
                    assert actual is not None
                    assert actual[0] == gap
                    a = actual[1]
                checked += 1

    print(
        "Constant gap branches verified: "
        f"k <= {max_gap}, length <= {max_length}, samples={samples}, checks={checked}"
    )


if __name__ == "__main__":
    verify_constant_return()
    verify_constant_gap()
