"""
explore68_periodic_branches.py

Verifies the exact periodic-shadow formulas.

For a return period word w with one-period data

    Q_w n' = P_w n + D_w,

the repeated word w^L has residue

    n == -D_w / (P_w - Q_w)  (mod Q_w^L).

For a reduced-gap period word w with one-period data

    H_w a' = A_w a - C_w,

the repeated word w^L has residue

    a == C_w / (A_w - H_w)  (mod H_w^L).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from explore51_binary_return_code import prefix_code
from explore52_binary_partial_map import gap_prefix_code, partial_gap_map, partial_return_map


def verify_periodic_return(
    max_period: int = 4,
    max_ones: int = 4,
    max_repeats: int = 4,
    samples: int = 2,
) -> None:
    checked = 0
    for period in range(1, max_period + 1):
        for word in product(range(max_ones + 1), repeat=period):
            one = prefix_code(word)
            denominator = one.p - one.q
            fixed = Fraction(-one.d, denominator)
            assert Fraction(-1, 1) <= fixed < 0, (word, fixed)
            assert denominator % 2 == 1

            for repeats in range(1, max_repeats + 1):
                repeated = word * repeats
                pfx = prefix_code(repeated)
                modulus = one.q**repeats
                expected = (-one.d * pow(denominator, -1, modulus)) % modulus
                assert pfx.q == modulus
                assert pfx.residue == expected, (word, repeats, pfx.residue, expected)

                for offset in range(samples):
                    n = expected + offset * modulus
                    for _ in range(repeats):
                        for ones in word:
                            step = partial_return_map(n)
                            assert step is not None
                            assert step.ones == ones
                            n = step.n_next
                    checked += 1

    print(
        "Periodic return branches verified: "
        f"period <= {max_period}, r <= {max_ones}, repeats <= {max_repeats}, "
        f"samples={samples}, checks={checked}"
    )


def verify_periodic_gap(
    max_period: int = 4,
    max_gap: int = 4,
    max_repeats: int = 4,
    samples: int = 2,
) -> None:
    checked = 0
    for period in range(1, max_period + 1):
        for word in product(range(max_gap + 1), repeat=period):
            one = gap_prefix_code(word)
            denominator = one.coefficient - one.modulus
            fixed = Fraction(one.constant, denominator)
            assert 0 < fixed < 1, (word, fixed)
            assert denominator % 2 == 1

            for repeats in range(1, max_repeats + 1):
                repeated = word * repeats
                pfx = gap_prefix_code(repeated)
                modulus = one.modulus**repeats
                expected = (one.constant * pow(denominator, -1, modulus)) % modulus
                assert pfx.modulus == modulus
                assert pfx.residue == expected, (word, repeats, pfx.residue, expected)

                for offset in range(samples):
                    a = expected + offset * modulus
                    for _ in range(repeats):
                        for gap in word:
                            step = partial_gap_map(a)
                            assert step is not None
                            assert step[0] == gap
                            a = step[1]
                    checked += 1

    print(
        "Periodic gap branches verified: "
        f"period <= {max_period}, k <= {max_gap}, repeats <= {max_repeats}, "
        f"samples={samples}, checks={checked}"
    )


if __name__ == "__main__":
    verify_periodic_return()
    verify_periodic_gap()
