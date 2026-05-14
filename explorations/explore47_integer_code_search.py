"""
explore47_integer_code_search.py

Searches directly for positive integer 2-adic codes for infinite growth-B
continuation chains.

By the coding lemmas, a positive integer code is exactly a positive odd m0 and
starting depth t0 whose deterministic growth-B recurrence never exits:

    q_i = (3^(t_i+2) * m_i + 1) / 8
    t_{i+1} = v2(q_i)
    m_{i+1} = odd_part(q_i)

The recurrence can continue inside the growth-B continuation domain only when
3^(t_i+2) * m_i == 7 (mod 8). This is stronger than asking for one growth-B
hop: it requires the hop to be growth-B and the output to be Type B, so that
there is a next continuation state.

The returned length is the number of successful continuation steps before
exiting this domain. A finite scan cannot prove nonexistence, but it tests the
exact positive-integer obstruction isolated by the 2-adic coding lemmas.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import log2


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


@dataclass(frozen=True)
class Survivor:
    m0: int
    t0: int
    length: int
    final_m: int
    final_t: int
    peak_m: int


def growth_b_tail_length(m0: int, t0: int, max_steps: int = 10_000) -> Survivor:
    m = m0
    t = t0
    peak = m

    for step in range(max_steps):
        a = 3 ** (t + 2)
        if (a * m) % 8 != 7:
            return Survivor(m0, t0, step, m, t, peak)
        q = (a * m + 1) // 8
        t = v2(q)
        m = q >> t
        assert m % 3 == (1 if t % 2 == 1 else 2)
        if (3 ** (t + 2) * m) % 8 == 7:
            assert m % 24 == (13 if t % 2 == 1 else 23)
        peak = max(peak, m)

    raise RuntimeError(f"tail survived {max_steps} steps for m0={m0}, t0={t0}")


def scan_integer_codes(max_m0: int = 200_000, max_t0: int = 20) -> None:
    best = Survivor(1, 0, 0, 1, 0, 1)
    by_length: dict[int, int] = {}

    for m0 in range(1, max_m0 + 1, 2):
        for t0 in range(max_t0 + 1):
            result = growth_b_tail_length(m0, t0)
            by_length[result.length] = by_length.get(result.length, 0) + 1
            if result.length > best.length:
                best = result

    print(f"Scanned odd m0 <= {max_m0}, t0 <= {max_t0}")
    print(f"Best continuation survivor: {best}")
    print(f"Best length / log2(m0): {best.length / max(log2(best.m0), 1):.3f}")
    print("Length distribution tail:")
    for length in sorted(by_length)[-12:]:
        print(f"  length={length:3d} count={by_length[length]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search bounded positive integer growth-B continuation codes."
    )
    parser.add_argument("--max-m0", type=int, default=200_000)
    parser.add_argument("--max-t0", type=int, default=20)
    args = parser.parse_args()
    scan_integer_codes(args.max_m0, args.max_t0)
