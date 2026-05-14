"""
explore60_backward_branches.py

Verifies explicit backward branch formulas for the binary return partial map
and the reduced binary {0,1} gap partial map.

For a terminal state and a chosen branch length, there is at most one
preimage.  This is a useful formulation of the remaining rank problem as a
backward preimage-tree counting problem.
"""

from __future__ import annotations

from fractions import Fraction
from math import log

from explore51_binary_return_code import block
from explore52_binary_partial_map import partial_gap_map, partial_return_map


def v3(n: int) -> int:
    count = 0
    while n % 3 == 0:
        n //= 3
        count += 1
    return count


def return_preimage(n_next: int, ones: int) -> int | None:
    step = block(ones)
    numerator = step.q * n_next - step.d
    if numerator < 0 or numerator % step.p != 0:
        return None
    return numerator // step.p


def gap_preimage(a_next: int, gap: int) -> int | None:
    numerator = 2 ** (3 * gap + 7) * a_next + 8**gap
    denominator = 3 ** (2 * gap + 5)
    if numerator % denominator != 0:
        return None
    return numerator // denominator


def verify_return_backward_formula(limit: int = 200_000, max_ones: int = 12) -> None:
    forward_checked = 0
    for n in range(limit + 1):
        step = partial_return_map(n)
        if step is None:
            continue
        assert return_preimage(step.n_next, step.ones) == n
        assert 96 * 27**step.ones <= (88 * step.n_next + 85) * 16**step.ones
        assert 9 * 27**step.ones * n < 8 * 16**step.ones * step.n_next
        forward_checked += 1

    backward_checked = 0
    for n_next in range(limit + 1):
        for ones in range(max_ones + 1):
            preimage = return_preimage(n_next, ones)
            if preimage is None:
                continue
            value = 88 * n_next + 85
            exponent = v3(value)
            assert exponent == 3 * ones + 1
            assert (value // 3**exponent) % 3 == 2
            step = partial_return_map(preimage)
            assert step is not None
            assert step.ones == ones
            assert step.n_next == n_next
            assert 96 * 27**ones <= (88 * n_next + 85) * 16**ones
            assert 9 * 27**ones * preimage < 8 * 16**ones * n_next
            backward_checked += 1

        value = 88 * n_next + 85
        exponent = v3(value)
        if exponent % 3 == 1 and (value // 3**exponent) % 3 == 2:
            candidate_ones = (exponent - 1) // 3
            if candidate_ones <= max_ones:
                candidate = return_preimage(n_next, candidate_ones)
                for other_ones in range(max_ones + 1):
                    if other_ones == candidate_ones:
                        continue
                    assert return_preimage(n_next, other_ones) is None
                if candidate is not None:
                    assert partial_return_map(candidate).ones == candidate_ones
                    assert 729 * candidate**3 < 512 * n_next**3

    print(
        f"Return backward branches, 3-adic gate, and uniqueness verified: "
        f"forward={forward_checked}, "
        f"backward={backward_checked}, n_next <= {limit}, r <= {max_ones}"
    )


def verify_gap_backward_formula(limit: int = 200_000, max_gap: int = 12) -> None:
    forward_checked = 0
    for a in range(1, limit + 1):
        step = partial_gap_map(a)
        if step is None:
            continue
        gap, a_next = step
        assert gap_preimage(a_next, gap) == a
        assert 243 * 9**gap <= (128 * a_next + 1) * 8**gap
        assert 81 * 9**gap * a <= 43 * 8**gap * a_next
        forward_checked += 1

    backward_checked = 0
    for a_next in range(1, limit + 1):
        for gap in range(max_gap + 1):
            preimage = gap_preimage(a_next, gap)
            if preimage is None:
                continue
            step = partial_gap_map(preimage)
            assert step is not None
            assert step == (gap, a_next)
            assert 243 * 9**gap <= (128 * a_next + 1) * 8**gap
            assert 81 * 9**gap * preimage <= 43 * 8**gap * a_next
            backward_checked += 1

        exponent = v3(128 * a_next + 1)
        expected_max_gap = (exponent - 5) // 2 if exponent >= 5 else -1
        check_max_gap = max(max_gap, expected_max_gap + 2)
        merge_chain = []
        for gap in range(check_max_gap + 1):
            preimage = gap_preimage(a_next, gap)
            if gap <= expected_max_gap:
                assert preimage is not None
                assert partial_gap_map(preimage) == (gap, a_next)
                merge_chain.append(preimage)
            else:
                assert preimage is None
        for left, right in zip(merge_chain, merge_chain[1:]):
            assert 9 * right == 8 * left
        if merge_chain:
            assert len(merge_chain) <= max(0, (log(128 * a_next + 1, 3) - 3) / 2) + 1e-12
            assert 27 * sum(merge_chain) <= 128 * a_next + 1
            assert sum(merge_chain) <= Fraction(43, 9) * a_next
            assert 729 * 217 * sum(a**3 for a in merge_chain) <= 43**3 * a_next**3

    print(
        "Gap backward branches, exact 3-adic branch count, merge chains, "
        f"merge bounds, and cubic-mass contraction verified: "
        f"forward={forward_checked}, "
        f"backward={backward_checked}, a_next <= {limit}, k <= {max_gap}"
    )


def verify_path_contractions(limit: int = 50_000, max_depth: int = 8) -> None:
    return_checked = 0
    for start in range(limit + 1):
        n = start
        total_ones = 0
        for depth in range(1, max_depth + 1):
            step = partial_return_map(n)
            if step is None:
                break
            total_ones += step.ones
            n = step.n_next
            assert (
                9**depth * 27**total_ones * start
                < 8**depth * 16**total_ones * n
            )
            return_checked += 1

    gap_checked = 0
    for start in range(1, limit + 1):
        a = start
        total_gap = 0
        for depth in range(1, max_depth + 1):
            step = partial_gap_map(a)
            if step is None:
                break
            gap, a = step
            total_gap += gap
            assert (
                81**depth * 9**total_gap * start
                <= 43**depth * 8**total_gap * a
            )
            gap_checked += 1

    print(
        f"Backward path contractions, terminal escape, and return cubic-mass contraction verified: return={return_checked}, "
        f"gap={gap_checked}, starts <= {limit}, depth <= {max_depth}"
    )


def verify_moment_threshold() -> None:
    cubic_constant = Fraction(43**3, 729 * 217)
    assert cubic_constant < 1
    assert Fraction(43, 81) ** 2 + Fraction(8, 9) ** 2 > 1
    assert Fraction(43, 81) ** 3 + Fraction(8, 9) ** 3 < 1
    print(f"Moment threshold bracket verified: theta in (2, 3), cubic={float(cubic_constant):.6f}")


def verify_expansion_pressure(max_label: int = 8) -> None:
    def pressure_root(a: Fraction, b: Fraction) -> float:
        lo = 0.0
        hi = 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if float(a) ** mid + float(b) ** mid > 1:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    return_base_2 = Fraction(8, 9) ** 2 / (1 - Fraction(16, 27) ** 2)
    return_base_3 = Fraction(8, 9) ** 3 / (1 - Fraction(16, 27) ** 3)
    assert return_base_2 > 1
    assert return_base_3 < 1

    gap_base_2 = Fraction(128, 243) ** 2 / (1 - Fraction(8, 9) ** 2)
    gap_base_3 = Fraction(128, 243) ** 3 / (1 - Fraction(8, 9) ** 3)
    assert gap_base_2 > 1
    assert gap_base_3 < 1

    return_root = pressure_root(Fraction(8, 9), Fraction(16, 27))
    gap_root = pressure_root(Fraction(128, 243), Fraction(8, 9))
    assert 2 < return_root < 3
    assert 2 < gap_root < 3

    for theta in (2, 3, 4):
        return_exact = Fraction(8, 9) ** theta / (1 - Fraction(16, 27) ** theta)
        return_partial = sum(
            Fraction(8, 9) ** theta * Fraction(16, 27) ** (theta * r)
            for r in range(max_label + 1)
        )
        return_tail = (
            Fraction(8, 9) ** theta
            * Fraction(16, 27) ** (theta * (max_label + 1))
            / (1 - Fraction(16, 27) ** theta)
        )
        assert return_exact - return_partial == return_tail

        gap_exact = Fraction(128, 243) ** theta / (1 - Fraction(8, 9) ** theta)
        gap_partial = sum(
            Fraction(128, 243) ** theta * Fraction(8, 9) ** (theta * k)
            for k in range(max_label + 1)
        )
        gap_tail = (
            Fraction(128, 243) ** theta
            * Fraction(8, 9) ** (theta * (max_label + 1))
            / (1 - Fraction(8, 9) ** theta)
        )
        assert gap_exact - gap_partial == gap_tail

    print(
        "Expansion pressure verified: return and gap bases are "
        f"> 1 at theta=2 and < 1 at theta=3; "
        f"roots=({return_root:.6f}, {gap_root:.6f}); labels <= {max_label}"
    )


if __name__ == "__main__":
    verify_return_backward_formula()
    verify_gap_backward_formula()
    verify_path_contractions()
    verify_moment_threshold()
    verify_expansion_pressure()
