"""
explore62_terminal_windows.py

Verifies the terminal-window identities for low finite-height prefix
residues.

For a return prefix with least residue R and terminal state U:

    U / E = R - M,      R <= U/E < R + 1.
    R = floor(U/E).

For a gap prefix with least residue S and terminal state u:

    u / E = S - L,      S - 1/115 < u/E < S.
    S = ceil(u/E).

These windows are the exact stopping-time interface left after the backward
contraction lemmas: low initial residues force high terminal escape, but the
normalized terminal coordinate stays in a fixed-width interval near the least
prefix residue.
"""

from __future__ import annotations

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_CASES = (24, 32)
GAP_CASES = (24, 32)

EXPECTED_RETURN_TOTAL = {
    24: (8, 128),
    32: (10, 658),
}

EXPECTED_GAP_TOTAL = {
    24: (3, 24),
    32: (4, 70),
}


def verify_return_windows() -> None:
    for bits in RETURN_CASES:
        bound = (1 << bits) - 1
        candidate_bound = 2 * bound + 1
        states = [RETURN_EMPTY]
        total = 0
        levels = 0

        while True:
            next_states = []
            for state in states:
                for ones in range(return_bound_for_state(state, candidate_bound + 1) + 1):
                    candidate = extend_return(state, ones)
                    if candidate.residue <= candidate_bound:
                        next_states.append(candidate)
            if not next_states:
                break

            low_states = []
            for state in next_states:
                # U/E = UQ/P = R + D/P, with 0 <= D/P < 1.
                assert state.constant >= 0
                assert state.constant < state.coefficient
                normalized_num = state.auxiliary * state.modulus
                assert state.coefficient * state.residue <= normalized_num
                assert normalized_num < state.coefficient * (state.residue + 1)
                assert normalized_num // state.coefficient == state.residue
                by_residue = state.residue <= bound
                by_window = normalized_num < state.coefficient * (bound + 1)
                assert by_residue == by_window
                if by_residue:
                    low_states.append(state)

            if not low_states:
                break
            total += len(low_states)
            levels += 1
            states = next_states

        assert (levels, total) == EXPECTED_RETURN_TOTAL[bits]
        print(f"return bits={bits:3d} levels={levels:3d} windows={total:5d}")


def verify_gap_windows() -> None:
    for bits in GAP_CASES:
        bound = (1 << bits) - 1
        candidate_bound = 2 * bound + 1
        states = [GAP_EMPTY]
        total = 0
        levels = 0

        while True:
            next_states = []
            for state in states:
                for gap in range(gap_bound_for_state(state, candidate_bound + 1) + 1):
                    candidate = extend_gap(state, gap)
                    if 1 <= candidate.residue <= candidate_bound:
                        next_states.append(candidate)
            if not next_states:
                break

            low_states = []
            for state in next_states:
                # u/E = uH/A = S - C/A, with 0 < C/A < 1/115.
                assert state.constant > 0
                assert 115 * state.constant < state.coefficient
                normalized_num = state.auxiliary * state.modulus
                assert 115 * normalized_num > 115 * state.coefficient * state.residue - state.coefficient
                assert normalized_num < state.coefficient * state.residue
                assert (normalized_num + state.coefficient - 1) // state.coefficient == state.residue
                by_residue = state.residue <= bound
                by_window = normalized_num < state.coefficient * bound
                assert by_residue == by_window
                if by_residue:
                    low_states.append(state)

            if not low_states:
                break
            total += len(low_states)
            levels += 1
            states = next_states

        assert (levels, total) == EXPECTED_GAP_TOTAL[bits]
        print(f"gap    bits={bits:3d} levels={levels:3d} windows={total:5d}")


if __name__ == "__main__":
    verify_return_windows()
    verify_gap_windows()
