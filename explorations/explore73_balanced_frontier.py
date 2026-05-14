"""
explore73_balanced_frontier.py

Diagnostic checks for the balanced/Sturmian-like binary frontier.

The paper now reduces the balanced-prefix minima to the exact question of
whether a non-eventually-periodic balanced binary word can land on a positive
ordinary code.  Balanced finite words are sparse enough to enumerate directly,
which gives a sharper finite check than all {0,1} words.

This is evidence only; finite enumeration does not prove balanced-prefix
divergence.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return


DEFAULT_MAX_LENGTH = 64
EXPECTED_DEFAULT_FINAL = (64, 27834, 186, 2, 444, 2)


@dataclass(frozen=True)
class BalancedState:
    word: tuple[int, ...]
    return_state: object
    gap_state: object


def is_balanced(word: tuple[int, ...]) -> bool:
    """Return True iff every equal-length factor pair differs by at most one 1."""
    length = len(word)
    for width in range(1, length + 1):
        count = sum(word[:width])
        low = high = count
        for end in range(width, length):
            count += word[end] - word[end - width]
            if count < low:
                low = count
            elif count > high:
                high = count
            if high - low > 1:
                return False
    return True


def next_balanced_states(states: list[BalancedState]) -> list[BalancedState]:
    next_states: list[BalancedState] = []
    for state in states:
        for digit in (0, 1):
            word = state.word + (digit,)
            if not is_balanced(word):
                continue
            next_states.append(
                BalancedState(
                    word,
                    extend_return(state.return_state, digit),
                    extend_gap(state.gap_state, digit),
                )
            )
    return next_states


def run(max_length: int) -> None:
    states = [BalancedState((), RETURN_EMPTY, GAP_EMPTY)]
    final_summary: tuple[int, int, int, int, int, int] | None = None
    print("balanced binary frontier minima")
    for level in range(1, max_length + 1):
        states = next_balanced_states(states)
        best_return = min(states, key=lambda state: state.return_state.residue)
        best_gap = min(states, key=lambda state: state.gap_state.residue)
        final_summary = (
            level,
            len(states),
            best_return.return_state.residue.bit_length(),
            sum(best_return.word),
            best_gap.gap_state.residue.bit_length(),
            sum(best_gap.word),
        )
        print(
            f"  L={level:3d} count={len(states):7d} "
            f"return_bits={best_return.return_state.residue.bit_length():5d} "
            f"return_ones={sum(best_return.word):3d} "
            f"return_word={best_return.word} "
            f"gap_bits={best_gap.gap_state.residue.bit_length():5d} "
            f"gap_ones={sum(best_gap.word):3d} "
            f"gap_word={best_gap.word}"
        )
    if max_length == DEFAULT_MAX_LENGTH:
        assert final_summary == EXPECTED_DEFAULT_FINAL, final_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=DEFAULT_MAX_LENGTH)
    args = parser.parse_args()
    run(args.max_length)
