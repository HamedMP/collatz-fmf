"""
explore59_critical_clusters.py

Displays and verifies the finite-word clusters responsible for the largest
critical discrepancy ratios found by explore58.

The point is diagnostic: the worst tested ratios are caused by small clusters
of low least-prefix residues, not by a single global-minimum word.
"""

from __future__ import annotations

from explore53_gap_minima import EMPTY as GAP_EMPTY
from explore53_gap_minima import extend as extend_gap
from explore53_gap_minima import gap_bound_for_state
from explore54_return_minima import EMPTY as RETURN_EMPTY
from explore54_return_minima import extend as extend_return
from explore54_return_minima import return_bound_for_state
from explore52_binary_partial_map import partial_gap_map


RETURN_LEVEL = 16
RETURN_HEIGHT = 67_477_744_910_335
EXPECTED_RETURN_CLUSTER = (
    (32_499_281_723_391, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    (48_178_543_984_639, (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0)),
    (67_477_744_910_335, (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
)

GAP_LEVEL = 4
GAP_HEIGHT = 32_679_099
EXPECTED_GAP_CLUSTER = (
    (29_048_088, (1, 0, 0, 0), 424_478_101),
    (32_679_099, (0, 0, 0, 0), 424_478_101),
)

EXPECTED_GAP_MERGE_TRACE = (
    (29_048_088, 1, 62_039_227),
    (32_679_099, 0, 62_039_227),
    (62_039_227, 0, 117_777_595),
    (117_777_595, 0, 223_593_403),
    (223_593_403, 0, 424_478_101),
)


def return_cluster():
    states = [RETURN_EMPTY]
    for _ in range(RETURN_LEVEL):
        next_states = []
        for state in states:
            for ones in range(return_bound_for_state(state, RETURN_HEIGHT + 1) + 1):
                candidate = extend_return(state, ones)
                if candidate.residue <= RETURN_HEIGHT:
                    next_states.append(candidate)
        states = next_states
    return sorted(states, key=lambda state: state.residue)


def gap_cluster():
    states = [GAP_EMPTY]
    for _ in range(GAP_LEVEL):
        next_states = []
        for state in states:
            for gap in range(gap_bound_for_state(state, GAP_HEIGHT + 1) + 1):
                candidate = extend_gap(state, gap)
                if 1 <= candidate.residue <= GAP_HEIGHT:
                    next_states.append(candidate)
        states = next_states
    return sorted(states, key=lambda state: state.residue)


def verify_return_cluster() -> None:
    cluster = return_cluster()
    observed = tuple((state.residue, state.word) for state in cluster)
    assert observed == EXPECTED_RETURN_CLUSTER
    assert len({state.auxiliary for state in cluster}) == len(cluster)
    print(f"return level={RETURN_LEVEL} height={RETURN_HEIGHT} cluster={len(cluster)}")
    for state in cluster:
        print(f"  residue={state.residue} word={state.word} landed={state.auxiliary}")


def verify_gap_cluster() -> None:
    cluster = gap_cluster()
    observed = tuple((state.residue, state.word, state.auxiliary) for state in cluster)
    assert observed == EXPECTED_GAP_CLUSTER
    assert len({state.auxiliary for state in cluster}) == 1

    first = partial_gap_map(cluster[0].residue)
    second = partial_gap_map(cluster[1].residue)
    assert first == (1, 62_039_227)
    assert second == (0, 62_039_227)

    trace = [
        (cluster[0].residue, first[0], first[1]),
        (cluster[1].residue, second[0], second[1]),
    ]
    a = first[1]
    while a != cluster[0].auxiliary:
        step = partial_gap_map(a)
        assert step is not None
        trace.append((a, step[0], step[1]))
        a = step[1]
    assert tuple(trace) == EXPECTED_GAP_MERGE_TRACE

    print(f"gap    level={GAP_LEVEL} height={GAP_HEIGHT} cluster={len(cluster)}")
    for state in cluster:
        print(f"  residue={state.residue} word={state.word} landed={state.auxiliary}")
    print("  merge trace:")
    for start, gap, stop in trace:
        print(f"    {start} --{gap}--> {stop}")


if __name__ == "__main__":
    verify_return_cluster()
    verify_gap_cluster()
