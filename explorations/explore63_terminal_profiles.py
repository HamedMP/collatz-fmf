"""
explore63_terminal_profiles.py

Profiles expansion factors and terminal states for low finite-height prefix
residues.

The terminal-window identities show that low starts correspond to normalized
terminal heights in short intervals.  This script records the actual expansion
and terminal-height ranges on exact low frontiers, making the remaining
stopping-time problem concrete.
"""

from __future__ import annotations

from fractions import Fraction

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state


RETURN_BITS = 32
GAP_BITS = 32

EXPECTED_RETURN_PROFILE = {
    1: (8, Fraction(9, 8), 10_341_485_552),
    4: (134, Fraction(6561, 4096), 154_993_677_308),
    9: (19, Fraction(387_420_489, 134_217_728), 54_288_292_472),
}

EXPECTED_GAP_PROFILE = {
    1: (9, Fraction(243, 128), 10_051_745_656),
    2: (28, Fraction(59_049, 16_384), 28_909_398_100),
    4: (7, Fraction(3_486_784_401, 268_435_456), 26_693_547_682),
}


def return_profile(bits: int = RETURN_BITS):
    bound = (1 << bits) - 1
    states = [RETURN_EMPTY]
    profile = {}
    level = 0

    while True:
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, bound + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return profile
        states = next_states
        level += 1

        expansions = [Fraction(state.coefficient, state.modulus) for state in states]
        terminals = [state.auxiliary for state in states]
        profile[level] = (
            len(states),
            min(expansions),
            max(expansions),
            min(terminals),
            max(terminals),
        )


def gap_profile(bits: int = GAP_BITS):
    bound = (1 << bits) - 1
    states = [GAP_EMPTY]
    profile = {}
    level = 0

    while True:
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, bound + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= bound:
                    next_states.append(candidate)
        if not next_states:
            return profile
        states = next_states
        level += 1

        expansions = [Fraction(state.coefficient, state.modulus) for state in states]
        terminals = [state.auxiliary for state in states]
        profile[level] = (
            len(states),
            min(expansions),
            max(expansions),
            min(terminals),
            max(terminals),
        )


def verify_return_profile() -> None:
    profile = return_profile()
    for level, (count, min_expansion, max_terminal) in EXPECTED_RETURN_PROFILE.items():
        observed = profile[level]
        assert observed[0] == count
        assert observed[1] == min_expansion
        assert observed[4] == max_terminal

    print(f"return terminal profile for B=2^{RETURN_BITS}-1")
    for level in sorted(profile):
        count, min_expansion, max_expansion, min_terminal, max_terminal = profile[level]
        print(
            f"  level={level:2d} count={count:4d} "
            f"E=[{float(min_expansion):.6f}, {float(max_expansion):.6f}] "
            f"U=[{min_terminal}, {max_terminal}]"
        )


def verify_gap_profile() -> None:
    profile = gap_profile()
    for level, (count, min_expansion, max_terminal) in EXPECTED_GAP_PROFILE.items():
        observed = profile[level]
        assert observed[0] == count
        assert observed[1] == min_expansion
        assert observed[4] == max_terminal

    print(f"gap terminal profile for B=2^{GAP_BITS}-1")
    for level in sorted(profile):
        count, min_expansion, max_expansion, min_terminal, max_terminal = profile[level]
        print(
            f"  level={level:2d} count={count:4d} "
            f"E=[{float(min_expansion):.6f}, {float(max_expansion):.6f}] "
            f"u=[{min_terminal}, {max_terminal}]"
        )


if __name__ == "__main__":
    verify_return_profile()
    verify_gap_profile()
