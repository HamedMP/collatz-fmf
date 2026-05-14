"""
explore50_binary_depth_affine.py

Derives and checks the affine normal form for growth-B continuation paths with
depths restricted to {0, 1}.

After one continuation step, the modulo-24 normal form gives:

    t = 0: m = 24n + 23
    t = 1: m = 24n + 13

In these coordinates the four possible binary-depth transitions are:

    0 -> 0: n' = (9n + 1) / 8
    0 -> 1: n' = 9n / 16
    1 -> 0: n' = (27n + 7) / 8
    1 -> 1: n' = (27n + 6) / 16

with the displayed divisibility conditions required for integrality.
"""

from __future__ import annotations

from itertools import product


CLASS = {0: 23, 1: 13}


def step_n(t: int, next_t: int, n: int) -> int | None:
    if t == 0 and next_t == 0:
        num, den = 9 * n + 1, 8
    elif t == 0 and next_t == 1:
        num, den = 9 * n, 16
    elif t == 1 and next_t == 0:
        num, den = 27 * n + 7, 8
    elif t == 1 and next_t == 1:
        num, den = 27 * n + 6, 16
    else:
        raise ValueError((t, next_t))
    if num % den:
        return None
    return num // den


def transition_coefficients(t: int, next_t: int) -> tuple[int, int, int]:
    """Return (a, c, e) for n_next = (a*n + c) / 2^e."""
    if t == 0 and next_t == 0:
        return 9, 1, 3
    if t == 0 and next_t == 1:
        return 9, 0, 4
    if t == 1 and next_t == 0:
        return 27, 7, 3
    if t == 1 and next_t == 1:
        return 27, 6, 4
    raise ValueError((t, next_t))


def prepend_congruence(a: int, c: int, e: int, residue: int, bits: int) -> tuple[int, int]:
    """Pull back n_next == residue mod 2^bits through (a*n+c)/2^e."""
    modulus = 1 << (bits + e)
    next_scaled = (1 << e) * residue
    pulled = pow(a, -1, modulus) * ((next_scaled - c) % modulus)
    return pulled % modulus, bits + e


def return_block_residue(ones: int) -> tuple[int, int]:
    """Return n == residue mod 2^bits for a block 0 -> 1^ones -> 0."""
    if ones == 0:
        transitions = [(0, 0)]
    else:
        transitions = [(0, 1)] + [(1, 1)] * (ones - 1) + [(1, 0)]

    residue = 0
    bits = 0
    for t, next_t in reversed(transitions):
        a, c, e = transition_coefficients(t, next_t)
        residue, bits = prepend_congruence(a, c, e, residue, bits)
    return residue, bits


def step_m(t: int, next_t: int, m: int) -> int | None:
    a = 3 ** (t + 2)
    q_num = a * m + 1
    den = 2 ** (next_t + 3)
    if q_num % den:
        return None
    m_next = q_num // den
    if m_next % 2 == 0:
        return None
    return m_next


def verify_affine_maps(limit_n: int = 100_000) -> None:
    for t, next_t in product((0, 1), repeat=2):
        for n in range(limit_n + 1):
            m = 24 * n + CLASS[t]
            m_next = step_m(t, next_t, m)
            n_next = step_n(t, next_t, n)
            if m_next is None or m_next % 24 != CLASS[next_t]:
                assert n_next is None
                continue
            assert n_next is not None
            assert m_next == 24 * n_next + CLASS[next_t]

    print(f"Binary-depth affine maps verified for n <= {limit_n}")


def transition_residue_classes() -> None:
    print("Binary-depth transition congruence conditions:")
    for t, next_t in product((0, 1), repeat=2):
        modulus = 16 if next_t == 1 else 8
        hits = [n for n in range(modulus) if step_n(t, next_t, n) is not None]
        print(f"  {t}->{next_t}: n mod {modulus} in {hits}")


def show_return_block_residues(max_ones: int = 12) -> None:
    print("Binary zero-return block gates:")
    for ones in range(max_ones + 1):
        residue, bits = return_block_residue(ones)
        print(
            f"  0->1^{ones}->0: n mod 2^{bits} == {residue} "
            f"(residue_bits={residue.bit_length()})"
        )


def longest_tail(limit_n: int = 500_000, max_steps: int = 100) -> None:
    best = (0, None)
    for t0 in (0, 1):
        for n0 in range(limit_n + 1):
            stack = [(t0, n0, 0)]
            local_best = 0
            while stack:
                t, n, depth = stack.pop()
                local_best = max(local_best, depth)
                if depth >= max_steps:
                    print("survived max_steps", t0, n0)
                    return
                for next_t in (0, 1):
                    n_next = step_n(t, next_t, n)
                    if n_next is not None:
                        stack.append((next_t, n_next, depth + 1))
            if local_best > best[0]:
                best = (local_best, (t0, n0))

    print(f"Longest binary-depth tail for n <= {limit_n}: {best}")


def verify_zero_return_expansion(limit_n: int = 500_000, max_steps: int = 40) -> None:
    """Every admissible return from t=0 to t=0 strictly increases n."""
    checked = 0
    for n0 in range(limit_n + 1):
        stack = [(0, n0, 0)]
        while stack:
            t, n, depth = stack.pop()
            if depth >= max_steps:
                continue
            for next_t in (0, 1):
                n_next = step_n(t, next_t, n)
                if n_next is None:
                    continue
                if next_t == 0:
                    assert n_next > n0, (n0, n_next, depth + 1)
                    checked += 1
                else:
                    stack.append((next_t, n_next, depth + 1))
    print(f"Binary zero-return expansion verified on {checked} returns")


if __name__ == "__main__":
    verify_affine_maps()
    transition_residue_classes()
    show_return_block_residues()
    longest_tail()
    verify_zero_return_expansion()
