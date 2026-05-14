"""
explore46_infinite_code.py

Computes finite-prefix approximations to the exact 2-adic code for an
infinite growth-B depth sequence.

For a depth prefix t_0, ..., t_{n-1}, any infinite growth-B chain with that
prefix must have starting parameter m_0 satisfying

    m_0 == -C_n * A_n^{-1} (mod B_n),

where B_n is a power of 2. The inverse limit of these residues is the unique
2-adic code for the infinite depth word.

This script is exploratory. It does not prove the code is never a positive
integer, but it makes the remaining obstruction directly computable.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class PrefixCode:
    modulus: int
    residue: int
    bits: int


def inv_mod_power_of_two(odd: int, modulus: int) -> int:
    return pow(odd % modulus, -1, modulus)


def prefix_code(depths: list[int]) -> PrefixCode:
    if len(depths) < 2:
        raise ValueError("Need at least two depths to encode one continuation step")

    a_total = 1
    b_total = 1
    c_total = 0

    for i in range(len(depths) - 1):
        a = 3 ** (depths[i] + 2)
        b = 2 ** (depths[i + 1] + 3)
        c_total = a * c_total + b_total
        a_total *= a
        b_total *= b

    residue = (-c_total * inv_mod_power_of_two(a_total, b_total)) % b_total
    return PrefixCode(modulus=b_total, residue=residue, bits=b_total.bit_length() - 1)


def prefix_code_state(depths: list[int]) -> tuple[int, int, int, int]:
    """Return (A_n, B_n, C_n, r_n) for a finite depth prefix."""
    if len(depths) < 2:
        raise ValueError("Need at least two depths")

    a_total = 1
    b_total = 1
    c_total = 0

    for i in range(len(depths) - 1):
        a = 3 ** (depths[i] + 2)
        b = 2 ** (depths[i + 1] + 3)
        c_total = a * c_total + b_total
        a_total *= a
        b_total *= b

    residue = (-c_total * inv_mod_power_of_two(a_total, b_total)) % b_total
    return a_total, b_total, c_total, residue


def extension_digit(depths: list[int], next_t: int) -> int:
    """Return the base-B digit added when extending a prefix by next_t."""
    a_total, b_total, c_total, residue = prefix_code_state(depths)
    s = (a_total * residue + c_total) // b_total
    a = 3 ** (depths[-1] + 2)
    b = 2 ** (next_t + 3)
    a_next = a * a_total
    return (-(a * s + 1) * inv_mod_power_of_two(a_next, b)) % b


def show_codes(name: str, depths: list[int], checkpoints: list[int]) -> None:
    print(f"\n{name}")
    for n in checkpoints:
        if n > len(depths):
            continue
        code = prefix_code(depths[:n])
        print(
            f"prefix={n:3d} bits={code.bits:5d} "
            f"residue_bits={code.residue.bit_length():5d} "
            f"residue={code.residue} "
            f"low_hex={code.residue & ((1 << min(code.bits, 64)) - 1):016x}"
        )


def scan_small_residue_prefixes(max_length: int = 8, max_t: int = 3) -> None:
    print(f"\nSmallest prefix residues for words over t <= {max_t}")
    for length in range(2, max_length + 1):
        best_word = None
        best_code = None
        for word in product(range(max_t + 1), repeat=length):
            code = prefix_code(list(word))
            key = (code.residue.bit_length(), code.residue)
            best_key = (
                (best_code.residue.bit_length(), best_code.residue)
                if best_code is not None
                else None
            )
            if best_key is None or key < best_key:
                best_word = word
                best_code = code
        assert best_code is not None
        print(
            f"length={length:2d} min_residue_bits={best_code.residue.bit_length():4d} "
            f"mod_bits={best_code.bits:4d} residue={best_code.residue} word={best_word}"
        )


def scan_zero_extension_runs(max_length: int = 9, max_t: int = 3) -> None:
    max_run = 0
    best = None

    for word in product(range(max_t + 1), repeat=max_length):
        residues = [prefix_code(list(word[:n])).residue for n in range(2, max_length + 1)]
        run = 0
        for index in range(1, len(residues)):
            if residues[index] == residues[index - 1]:
                run += 1
                if run > max_run:
                    max_run = run
                    best = (word, index + 2, run, residues[index])
            else:
                run = 0

    print(f"\nZero extension-digit scan: length={max_length}, t <= {max_t}")
    print(f"Longest observed run of unchanged residues: {max_run}")
    print(f"Best example: {best}")


def thue_morse_depths(length: int) -> list[int]:
    return [bin(i).count("1") % 2 for i in range(length)]


def paperfolding_like_depths(length: int) -> list[int]:
    # A simple nonperiodic low-depth word: v2(i+1) mod 4.
    depths = []
    for i in range(length):
        n = i + 1
        t = 0
        while n % 2 == 0:
            n //= 2
            t += 1
        depths.append(t % 4)
    return depths


if __name__ == "__main__":
    checkpoints = [2, 3, 4, 5, 8, 12, 16, 24, 32, 48, 64]

    show_codes("constant zero depths", [0] * 80, checkpoints)
    show_codes("alternating 0/1 depths", [i % 2 for i in range(80)], checkpoints)
    show_codes("thue-morse depths", thue_morse_depths(80), checkpoints)
    show_codes("v2(i+1) mod 4 depths", paperfolding_like_depths(80), checkpoints)
    scan_small_residue_prefixes()
    scan_zero_extension_runs()
