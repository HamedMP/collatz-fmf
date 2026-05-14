"""
explore78_uniform_morphism_symbolic_witness.py

Finite symbolic-prefix witness scan for binary q-uniform morphic fixed points.

The power-length scan in explore77 checks prefixes of length q^h.  This script
checks symbolic prefixes of length c first, then lifts the recurrence by applying
phi^h.  If the length-c prefix recurs at symbolic shift tau, then the length
c q^h prefix recurs at shift tau q^h for every h.

For a non-eventually-periodic binary q-uniform morphism, the one-densities of
phi^h(0) and phi^h(1) converge to the same limit p.  Thus a symbolic witness
(c, tau) gives the asymptotic density-recurrence margins with T=tau/c and
a=b=p.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from explore77_uniform_morphism_recurrence import GAP_CUTOFF
from explore77_uniform_morphism_recurrence import GAP_ONE_HEIGHT
from explore77_uniform_morphism_recurrence import GAP_ZERO_HEIGHT
from explore77_uniform_morphism_recurrence import RETURN_CUTOFF
from explore77_uniform_morphism_recurrence import RETURN_ONE_HEIGHT
from explore77_uniform_morphism_recurrence import RETURN_ZERO_HEIGHT
from explore77_uniform_morphism_recurrence import all_binary_words
from explore77_uniform_morphism_recurrence import first_prefix_recurrence
from explore77_uniform_morphism_recurrence import morphism_fixed_prefix
from explore77_uniform_morphism_recurrence import obvious_eventually_periodic_kind
from explore77_uniform_morphism_recurrence import rendered_morphism


@dataclass(frozen=True)
class SymbolicWitness:
    prefix_symbols: int
    recurrence_symbols: int
    ratio: float
    density_limit: float
    return_margin: float
    gap_margin: float
    return_kind: str
    gap_kind: str


def limiting_one_density(
    q: int, image_zero: tuple[int, ...], image_one: tuple[int, ...]
) -> float:
    ones_zero = sum(image_zero)
    ones_one = sum(image_one)
    return ones_zero / (q - ones_one + ones_zero)


def witness_for(
    q: int,
    image_zero: tuple[int, ...],
    image_one: tuple[int, ...],
    max_prefix_symbols: int,
    search_length: int,
) -> SymbolicWitness | None:
    word = morphism_fixed_prefix(image_zero, image_one, search_length)
    density = limiting_one_density(q, image_zero, image_one)

    best: SymbolicWitness | None = None
    for prefix_symbols in range(1, max_prefix_symbols + 1):
        recurrence_symbols = first_prefix_recurrence(word, prefix_symbols)
        if recurrence_symbols is None:
            continue
        ratio = recurrence_symbols / prefix_symbols
        return_margin = (
            3
            + 4 * density
            - ratio * (RETURN_ZERO_HEIGHT + density * RETURN_ONE_HEIGHT)
        )
        gap_margin = (
            7
            + 3 * density
            - ratio * (GAP_ZERO_HEIGHT + density * GAP_ONE_HEIGHT)
        )
        return_kind = (
            "fast"
            if ratio < RETURN_CUTOFF
            else "density"
            if return_margin > 0
            else "none"
        )
        gap_kind = (
            "fast"
            if ratio < GAP_CUTOFF
            else "density"
            if gap_margin > 0
            else "none"
        )
        candidate = SymbolicWitness(
            prefix_symbols=prefix_symbols,
            recurrence_symbols=recurrence_symbols,
            ratio=ratio,
            density_limit=density,
            return_margin=return_margin,
            gap_margin=gap_margin,
            return_kind=return_kind,
            gap_kind=gap_kind,
        )
        if return_kind != "none" and gap_kind != "none":
            return candidate
        if best is None or min(return_margin, gap_margin) > min(
            best.return_margin, best.gap_margin
        ):
            best = candidate

    return best


def run(q: int, max_prefix_symbols: int, search_length: int, verbose: bool) -> None:
    image_zeros = tuple(word for word in all_binary_words(q) if word[0] == 0)
    image_ones = all_binary_words(q)

    total = 0
    periodic = 0
    return_covered = 0
    gap_covered = 0
    both_covered = 0
    missing_return: list[tuple[tuple[int, ...], tuple[int, ...], SymbolicWitness]] = []
    missing_gap: list[tuple[tuple[int, ...], tuple[int, ...], SymbolicWitness]] = []

    return_kind_counts = {"fast": 0, "density": 0, "periodic": 0}
    gap_kind_counts = {"fast": 0, "density": 0, "periodic": 0}
    weakest_return: tuple[float, tuple[int, ...], tuple[int, ...], SymbolicWitness] | None = None
    weakest_gap: tuple[float, tuple[int, ...], tuple[int, ...], SymbolicWitness] | None = None

    print("uniform morphism symbolic-prefix witness diagnostic")
    print(
        f"q={q} max_prefix_symbols={max_prefix_symbols} "
        f"search_length={search_length}"
    )

    for image_zero in image_zeros:
        for image_one in image_ones:
            total += 1
            periodic_kind = obvious_eventually_periodic_kind(image_zero, image_one)
            if periodic_kind is not None:
                periodic += 1
                return_covered += 1
                gap_covered += 1
                both_covered += 1
                return_kind_counts["periodic"] += 1
                gap_kind_counts["periodic"] += 1
                continue

            witness = witness_for(
                q, image_zero, image_one, max_prefix_symbols, search_length
            )
            if witness is None:
                raise RuntimeError(
                    f"no symbolic recurrence found for "
                    f"{rendered_morphism(image_zero, image_one)}"
                )

            has_return = witness.return_kind != "none"
            has_gap = witness.gap_kind != "none"
            return_covered += int(has_return)
            gap_covered += int(has_gap)
            both_covered += int(has_return and has_gap)
            if has_return:
                return_kind_counts[witness.return_kind] += 1
            else:
                missing_return.append((image_zero, image_one, witness))
            if has_gap:
                gap_kind_counts[witness.gap_kind] += 1
            else:
                missing_gap.append((image_zero, image_one, witness))

            if weakest_return is None or witness.return_margin < weakest_return[0]:
                weakest_return = (
                    witness.return_margin,
                    image_zero,
                    image_one,
                    witness,
                )
            if weakest_gap is None or witness.gap_margin < weakest_gap[0]:
                weakest_gap = (witness.gap_margin, image_zero, image_one, witness)

            if verbose:
                print(
                    f"  {rendered_morphism(image_zero, image_one)}: "
                    f"c={witness.prefix_symbols} tau={witness.recurrence_symbols} "
                    f"T={witness.ratio:.3f} p={witness.density_limit:.3f} "
                    f"R={witness.return_margin:.3f}/{witness.return_kind} "
                    f"G={witness.gap_margin:.3f}/{witness.gap_kind}"
                )

    print(f"total={total}")
    print(f"obvious_eventually_periodic={periodic}")
    print(f"return_covered={return_covered}")
    print(f"gap_covered={gap_covered}")
    print(f"both_covered={both_covered}")
    print(f"return_kind_counts={return_kind_counts}")
    print(f"gap_kind_counts={gap_kind_counts}")
    if weakest_return is not None:
        margin, image_zero, image_one, witness = weakest_return
        print(
            "weakest_return_margin="
            f"{margin:.3f} at {rendered_morphism(image_zero, image_one)} "
            f"c={witness.prefix_symbols} tau={witness.recurrence_symbols} "
            f"T={witness.ratio:.3f} p={witness.density_limit:.3f}"
        )
    if weakest_gap is not None:
        margin, image_zero, image_one, witness = weakest_gap
        print(
            "weakest_gap_margin="
            f"{margin:.3f} at {rendered_morphism(image_zero, image_one)} "
            f"c={witness.prefix_symbols} tau={witness.recurrence_symbols} "
            f"T={witness.ratio:.3f} p={witness.density_limit:.3f}"
        )
    if missing_return:
        print("missing_return_cases=")
        for image_zero, image_one, witness in missing_return[:20]:
            print(
                f"  {rendered_morphism(image_zero, image_one)} "
                f"best c={witness.prefix_symbols} tau={witness.recurrence_symbols} "
                f"T={witness.ratio:.3f} R={witness.return_margin:.3f}"
            )
    if missing_gap:
        print("missing_gap_cases=")
        for image_zero, image_one, witness in missing_gap[:20]:
            print(
                f"  {rendered_morphism(image_zero, image_one)} "
                f"best c={witness.prefix_symbols} tau={witness.recurrence_symbols} "
                f"T={witness.ratio:.3f} G={witness.gap_margin:.3f}"
            )

    if q == 6 and max_prefix_symbols == 6:
        expected = (2048, 65, 2048, 2048, 2048)
        observed = (total, periodic, return_covered, gap_covered, both_covered)
        assert observed == expected, observed
    elif q == 7 and max_prefix_symbols == 7:
        expected = (8192, 129, 8192, 8192, 8192)
        observed = (total, periodic, return_covered, gap_covered, both_covered)
        assert observed == expected, observed
    elif q == 8 and max_prefix_symbols == 8:
        expected = (32768, 257, 32768, 32768, 32768)
        observed = (total, periodic, return_covered, gap_covered, both_covered)
        assert observed == expected, observed
    elif q == 9 and max_prefix_symbols == 18:
        expected = (131072, 513, 131072, 131071, 131071)
        observed = (total, periodic, return_covered, gap_covered, both_covered)
        assert observed == expected, observed
        rendered_missing_gap = tuple(
            rendered_morphism(image_zero, image_one)
            for image_zero, image_one, _witness in missing_gap
        )
        assert rendered_missing_gap == ("0->011111111 1->100000000",)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=6)
    parser.add_argument("--max-prefix-symbols", type=int)
    parser.add_argument("--search-length", type=int, default=4096)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    run(
        q=args.q,
        max_prefix_symbols=args.max_prefix_symbols or args.q,
        search_length=args.search_length,
        verbose=args.verbose,
    )
