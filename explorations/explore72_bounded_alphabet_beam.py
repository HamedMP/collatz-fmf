"""
explore72_bounded_alphabet_beam.py

Beam search for long low-residue words in the first nonconstant alphabets.

Exhaustive enumeration for return/gap labels {0,1} is now locked through
length 20 in explore70.  This script pushes further with a beam heuristic,
keeping states with the smallest least-prefix residues.  It is diagnostic only:
beam survival or beam failure is not a proof.
"""

from __future__ import annotations

import argparse

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import GapState
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import ReturnState
from explore54_return_minima import extend as extend_return


def state_key(state: ReturnState | GapState) -> tuple[int, int, int]:
    # Prefer genuinely small ordinary residues; use fewer 1 labels as a stable
    # tie-breaker to make sparse candidates visible.
    return (state.residue.bit_length(), state.residue, sum(state.word))


def prune(states, beam_width: int):
    states.sort(key=state_key)
    return states[:beam_width]


def describe(label: str, level: int, states) -> None:
    best = min(states, key=state_key)
    ones = sum(best.word)
    print(
        f"{label:6s} L={level:4d} residue_bits={best.residue.bit_length():6d} "
        f"modulus_bits={best.modulus.bit_length() - 1:6d} ones={ones:4d} "
        f"tail={best.word[-32:]}"
    )


def beam_search(max_length: int, beam_width: int, report_every: int) -> None:
    return_states = [RETURN_EMPTY]
    gap_states = [GAP_EMPTY]

    print(
        f"bounded {{0,1}} beam search: max_length={max_length}, "
        f"beam_width={beam_width}, report_every={report_every}"
    )

    for level in range(1, max_length + 1):
        return_states = prune(
            [extend_return(state, digit) for state in return_states for digit in (0, 1)],
            beam_width,
        )
        gap_states = prune(
            [extend_gap(state, digit) for state in gap_states for digit in (0, 1)],
            beam_width,
        )

        if level <= 20 or level % report_every == 0 or level == max_length:
            describe("return", level, return_states)
            describe("gap", level, gap_states)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=200)
    parser.add_argument("--beam-width", type=int, default=5000)
    parser.add_argument("--report-every", type=int, default=20)
    args = parser.parse_args()
    beam_search(args.max_length, args.beam_width, args.report_every)
