"""
explore45_bridge_lemmas.py

Tests pointwise bridge lemmas needed to turn the FMF density framework into
a Collatz proof.

This script deliberately checks candidate pointwise statements, not average
or density statements:

1. Growth-B chain length <= 0.55 * log2(m0) + 3
2. Epoch duration <= 3.2 * log2(x)
3. Every tested odd x descends below itself under FMF iteration

These are empirical tests only. Passing them does not prove Collatz.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log2
from itertools import product


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


@dataclass(frozen=True)
class Hop:
    start: int
    end: int
    kind: str
    t: int
    m: int
    fmf_v2: int


def fmf_hop(x: int) -> Hop:
    if x % 4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        p = v2(fmf)
        return Hop(x, fmf >> p, "A", 0, k, p)

    k = (x - 3) // 4
    t = v2(k + 1)
    m = (k + 1) >> t
    fmf = 2 * (3 ** (t + 2) * m - 1)
    p = v2(fmf)
    return Hop(x, fmf >> p, "B", t, m, p)


def growth_b_chain_length(x: int, max_hops: int = 10_000) -> tuple[int, int]:
    first = fmf_hop(x)
    m0 = first.m if first.kind == "B" else 0
    length = 0

    for _ in range(max_hops):
        hop = fmf_hop(x)
        if hop.kind == "B" and hop.fmf_v2 == 2:
            length += 1
            x = hop.end
            continue
        return length, m0

    raise RuntimeError(f"growth-B chain did not terminate within {max_hops} hops")


def epoch_duration(x: int, max_hops: int = 10_000) -> tuple[int, int]:
    start = x
    peak = x
    for step in range(1, max_hops + 1):
        hop = fmf_hop(x)
        x = hop.end
        peak = max(peak, x)
        if x < start:
            return step, peak
        if x == 1:
            return step, peak
    raise RuntimeError(f"epoch did not descend within {max_hops} hops for x={start}")


def scan_range(limit: int) -> None:
    worst_growth_ratio = 0.0
    worst_growth = None
    worst_epoch_ratio = 0.0
    worst_epoch = None
    non_descenders = 0

    for x in range(3, limit + 1, 2):
        glen, m0 = growth_b_chain_length(x)
        if glen > 0 and m0 > 1:
            bound = 0.55 * log2(m0) + 3
            ratio = glen / bound
            if ratio > worst_growth_ratio:
                worst_growth_ratio = ratio
                worst_growth = (x, glen, m0, bound, ratio)
            if glen > bound:
                print("GROWTH BOUND VIOLATION", x, glen, m0, bound)
                return

        duration, peak = epoch_duration(x)
        eratio = duration / log2(x)
        if eratio > worst_epoch_ratio:
            worst_epoch_ratio = eratio
            worst_epoch = (x, duration, peak, eratio)
        if duration > 3.2 * log2(x):
            non_descenders += 1
            print("EPOCH BOUND VIOLATION", x, duration, 3.2 * log2(x), peak)
            return

    print(f"Scanned odd x in [3, {limit}]")
    print(f"Growth-B bound violations: 0")
    print(f"Worst growth-B ratio: {worst_growth}")
    print(f"Epoch bound violations: {non_descenders}")
    print(f"Worst epoch ratio: {worst_epoch}")


def scan_mersennes(max_n: int) -> None:
    print(f"\nMersenne scan: x = 2^n - 1 for n <= {max_n}")
    worst_epoch_ratio = 0.0
    worst = None
    for n in range(3, max_n + 1):
        x = (1 << n) - 1
        glen, m0 = growth_b_chain_length(x)
        duration, peak = epoch_duration(x, max_hops=100_000)
        eratio = duration / log2(x)
        if eratio > worst_epoch_ratio:
            worst_epoch_ratio = eratio
            worst = (n, x, glen, m0, duration, peak, eratio)
        print(
            f"n={n:2d} growth_len={glen:2d} "
            f"epoch={duration:3d} peak_bits={log2(peak / x):7.3f}"
        )
    print(f"Worst Mersenne epoch ratio: {worst}")


def period_fixed_point(t_pattern: tuple[int, ...]) -> Fraction:
    """Return the 2-adic fixed point forced by an infinite periodic t-pattern."""
    a_total = 1
    b_total = 1
    c_total = 0

    for index, t in enumerate(t_pattern):
        next_t = t_pattern[(index + 1) % len(t_pattern)]
        a = 3 ** (t + 2)
        b = 2 ** (next_t + 3)
        c_total = a * c_total + b_total
        a_total *= a
        b_total *= b

    # b_total * m_next = a_total * m + c_total; periodicity forces m_next = m.
    return Fraction(c_total, b_total - a_total)


def scan_periodic_t_patterns(max_period: int = 5, max_t: int = 7) -> None:
    positive_integer_hits = []
    checked = 0

    for period in range(1, max_period + 1):
        for pattern in product(range(max_t + 1), repeat=period):
            checked += 1
            fixed = period_fixed_point(pattern)
            if fixed.denominator == 1 and fixed.numerator > 0 and fixed.numerator % 2 == 1:
                positive_integer_hits.append((pattern, fixed.numerator))

    print(f"\nPeriodic t-pattern scan: periods <= {max_period}, t <= {max_t}")
    print(f"Patterns checked: {checked}")
    print(f"Positive odd integer fixed points: {len(positive_integer_hits)}")
    if positive_integer_hits:
        print(positive_integer_hits[:10])


def growth_word_from_params(t: int, m: int, length: int) -> tuple[int, ...]:
    word = []
    for _ in range(length):
        if (3 ** (t + 2) * m - 1) % 4 != 2:
            break
        word.append(t)
        q = (3 ** (t + 2) * m + 1) // 8
        t = v2(q)
        m = q >> t
    return tuple(word)


def find_realization(word: tuple[int, ...], max_m: int = 2_000_000) -> int | None:
    for m in range(1, max_m, 2):
        if growth_word_from_params(word[0], m, len(word)) == word:
            return m
    return None


def scan_finite_word_realization(max_length: int = 4, max_t: int = 3) -> None:
    missing = []
    max_found = 0
    checked = 0

    for length in range(1, max_length + 1):
        for word in product(range(max_t + 1), repeat=length):
            checked += 1
            m = find_realization(word)
            if m is None:
                missing.append(word)
            else:
                max_found = max(max_found, m)

    print(f"\nFinite depth-word realization scan: length <= {max_length}, t <= {max_t}")
    print(f"Words checked: {checked}")
    print(f"Missing words under search limit: {len(missing)}")
    print(f"Maximum found m: {max_found}")
    if missing:
        print(f"First missing words: {missing[:10]}")


def verify_explicit_zero_depth_family(max_l: int = 20) -> None:
    """Check the closed-form family m_i = 9^i 8^(L-i) - 1."""
    for length in range(1, max_l + 1):
        m = 8**length - 1
        t = 0
        x = 4 * m - 1
        glen, m0 = growth_b_chain_length(x)
        assert m0 == m
        assert glen >= length

        for index in range(length):
            expected = 9**index * 8 ** (length - index) - 1
            assert t == 0
            assert m == expected
            q = (9 * m + 1) // 8
            t = v2(q)
            m = q >> t

    print(f"\nExplicit zero-depth family verified for L <= {max_l}")


def verify_zero_depth_classification(max_l: int = 8, search_limit: int = 200_000) -> None:
    """Check that L zero-depth hops are exactly m == -1 mod 8^L."""
    for length in range(1, max_l + 1):
        modulus = 8**length
        for m0 in range(1, search_limit + 1, 2):
            m = m0
            t = 0
            ok = True
            for _ in range(length):
                if t != 0 or m % 8 != 7:
                    ok = False
                    break
                q = (9 * m + 1) // 8
                t = v2(q)
                m = q >> t
            assert ok == (m0 % modulus == modulus - 1), (length, m0, modulus, ok)

    print(
        f"Zero-depth classification verified for L <= {max_l}, "
        f"m0 <= {search_limit}"
    )


if __name__ == "__main__":
    scan_range(200_000)
    scan_mersennes(50)
    scan_periodic_t_patterns()
    scan_finite_word_realization()
    verify_explicit_zero_depth_family()
    verify_zero_depth_classification()
