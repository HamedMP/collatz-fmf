"""
explore48_bounded_depth_beam.py

Searches for bounded-depth prefixes whose exact 2-adic growth-B code has
unusually small least nonnegative residue.

For a fixed depth alphabet {0, ..., T}, a proof that the minimum prefix residue
tends to infinity with prefix length would rule out positive-integer infinite
growth-B codes with depths bounded by T. Exhaustive search grows as
(T+1)^n, so this script uses a beam search to look for dangerous prefixes:
small residues and long zero-extension runs.

This is exploratory only. A beam miss is not a proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


def inv_mod_power_of_two(odd: int, modulus: int) -> int:
    return pow(odd % modulus, -1, modulus)


@dataclass(frozen=True)
class State:
    word: tuple[int, ...]
    a_total: int
    b_total: int
    c_total: int
    residue: int
    zero_run: int
    max_zero_run: int

    @property
    def bits(self) -> int:
        return self.b_total.bit_length() - 1


def initial_state(t0: int, t1: int) -> State:
    a_total = 3 ** (t0 + 2)
    b_total = 2 ** (t1 + 3)
    c_total = 1
    residue = (-c_total * inv_mod_power_of_two(a_total, b_total)) % b_total
    return State((t0, t1), a_total, b_total, c_total, residue, 0, 0)


def extend(state: State, next_t: int) -> State:
    last_t = state.word[-1]
    a = 3 ** (last_t + 2)
    b = 2 ** (next_t + 3)
    a_total = a * state.a_total
    b_total = b * state.b_total
    c_total = a * state.c_total + state.b_total
    residue = (-c_total * inv_mod_power_of_two(a_total, b_total)) % b_total
    zero_run = state.zero_run + 1 if residue == state.residue else 0
    return State(
        state.word + (next_t,),
        a_total,
        b_total,
        c_total,
        residue,
        zero_run,
        max(state.max_zero_run, zero_run),
    )


def state_key(state: State) -> tuple[int, int, int]:
    # Prefer genuinely small ordinary residues, then long unchanged-residue runs.
    return (state.residue.bit_length(), state.residue, -state.max_zero_run)


def beam_search(max_t: int, max_length: int, beam_width: int) -> None:
    states = [
        initial_state(t0, t1)
        for t0 in range(max_t + 1)
        for t1 in range(max_t + 1)
    ]
    states.sort(key=state_key)
    states = states[:beam_width]

    print(
        f"Bounded-depth beam search: t <= {max_t}, "
        f"max_length={max_length}, beam_width={beam_width}"
    )

    for length in range(2, max_length + 1):
        best = min(states, key=state_key)
        best_zero = max(states, key=lambda state: (state.max_zero_run, -state.residue.bit_length()))
        print(
            f"length={length:3d} "
            f"best_residue_bits={best.residue.bit_length():5d} "
            f"mod_bits={best.bits:5d} "
            f"best_state_zero_run={best.max_zero_run:3d} "
            f"beam_max_zero_run={best_zero.max_zero_run:3d} "
            f"residue={best.residue} "
            f"word_tail={best.word[-12:]} "
            f"zero_tail={best_zero.word[-12:]}"
        )

        if length == max_length:
            break

        next_states = []
        for state in states:
            for next_t in range(max_t + 1):
                next_states.append(extend(state, next_t))
        next_states.sort(key=state_key)
        states = next_states[:beam_width]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Beam search for bounded-depth small 2-adic prefix residues."
    )
    parser.add_argument("--max-t", type=int, default=3)
    parser.add_argument("--max-length", type=int, default=40)
    parser.add_argument("--beam-width", type=int, default=5000)
    args = parser.parse_args()
    beam_search(args.max_t, args.max_length, args.beam_width)
