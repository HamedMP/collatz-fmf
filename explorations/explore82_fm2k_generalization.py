"""
explore82_fm2k_generalization.py

Tests the "First Multiple of 2^k" (FM2^k) generalization of the FMF hop.

For odd x, FM2^k(x) is the first orbit value divisible by 2^k, and the FM2^k
hop map is F_k(x) = FM2^k(x) / 2^{v_2(FM2^k(x))}. FMF is k = 2.

Questions:
  1. Is the FM2^k hop exactly a geometric(2^{-(k-2)}) number of FMF hops?
     (Exact residue counting mod 2^K.)
  2. Is the mean log2-drift per underlying Collatz step k-independent?
  3. Does the pointwise worst-case growth ratio still grow with bit-length
     for k = 3, 4, 5?  (If yes, the pointwise gap is chunking-invariant.)
  4. Is there any k for which max_x |F_k(x)| / x < 1 pointwise on a range?
"""

from __future__ import annotations

import argparse
import math
import random


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def fm2k_hop(x: int, k: int) -> tuple[int, int, int]:
    """Return (F_k(x), collatz_steps, number_of_fmf_hops) for odd x > 1.

    Returns (1, steps, hops) if the orbit reaches 1 before any multiple of
    2^k: for k >= 3 the trivial cycle 1->4->2->1 contains no multiple of 2^k,
    so FM2^k is undefined there. FMF (k=2) is the largest k with a total map.
    """
    mod = 1 << k
    steps = 0
    fmf_hops = 0
    y = x
    while True:
        if y == 1:
            return 1, steps, fmf_hops
        # one Collatz step from odd y
        y = 3 * y + 1
        steps += 1
        while y % 4 != 0:
            if y % 2 == 0:
                y //= 2
                steps += 1
            else:
                y = 3 * y + 1
                steps += 1
        # y is now a multiple of 4: an FMF landing
        fmf_hops += 1
        v = v2(y)
        steps += v
        y >>= v
        if (1 << v) % mod == 0:
            return y, steps, fmf_hops


def exact_geometric_check(k: int, K: int) -> list[float]:
    """Fraction of odd residues mod 2^K needing exactly j FMF hops, j=1..4."""
    counts = [0] * 6
    total = 0
    for r in range(1, 1 << K, 2):
        # add a large multiple to stay clear of the trivial cycle
        x = r + (1 << (K + 24)) * 3
        _, _, hops = fm2k_hop(x, k)
        if hops < 6:
            counts[hops] += 1
        total += 1
    return [c / total for c in counts[1:5]]


def drift_per_step(k: int, samples: int, bits: int, rng: random.Random):
    tot_log = 0.0
    tot_steps = 0
    for _ in range(samples):
        x = rng.getrandbits(bits) | 1
        if x < 5:
            continue
        y, steps, _ = fm2k_hop(x, k)
        tot_log += math.log2(y / x)
        tot_steps += steps
    return tot_log / tot_steps, tot_steps / samples


def long_orbit_drift(bits: int, hops: int, rng: random.Random):
    """Per-Collatz-step drift along one long orbit (chunking-invariant), plus
    the mean FMF-hop log-ratio conditioned on the previous landing's v_2."""
    x = rng.getrandbits(bits) | 1
    tot_log = 0.0
    tot_steps = 0
    by_prev_v: dict[str, list[float]] = {"v=2": [], "v=3": [], "v>=4": []}
    prev_v = None
    for _ in range(hops):
        y, steps, _ = fm2k_hop(x, 2)
        lr = math.log2(y / x)
        tot_log += lr
        tot_steps += steps
        if prev_v is not None:
            key = "v=2" if prev_v == 2 else ("v=3" if prev_v == 3 else "v>=4")
            by_prev_v[key].append(lr)
        prev_v = _landing_v2(x)
        x = y
    return tot_log / tot_steps, {k: (sum(v) / len(v), len(v))
                                 for k, v in by_prev_v.items() if v}


def _landing_v2(x: int) -> int:
    y = 3 * x + 1
    while y % 4 != 0:
        y = y // 2 if y % 2 == 0 else 3 * y + 1
    return v2(y)


def worst_ratio(k: int, bits: int, samples: int, rng: random.Random):
    worst = 0.0
    worst_x = 0
    for _ in range(samples):
        x = rng.getrandbits(bits) | 1
        if x < 5:
            continue
        y, _, _ = fm2k_hop(x, k)
        r = y / x
        if r > worst:
            worst, worst_x = r, x
    # 2^bits - 1 is the canonical adversary for FMF; test it too
    x = (1 << bits) - 1
    y, _, _ = fm2k_hop(x, k)
    if y / x > worst:
        worst, worst_x = y / x, x
    return worst, worst_x


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=16)
    ap.add_argument("--samples", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=82)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    print("== 1. FM2^k hop as a count of FMF hops (exact residues mod 2^K) ==")
    for k in (2, 3, 4, 5):
        fr = exact_geometric_check(k, args.K)
        p = 2.0 ** -(k - 2)
        pred = [p * (1 - p) ** (j - 1) for j in range(1, 5)]
        print(f"k={k}: observed {['%.4f' % f for f in fr]}  "
              f"geometric(p={p}) {['%.4f' % f for f in pred]}")

    print("\n== 2a. Single FM2^k hop from uniform x: log-drift per Collatz step ==")
    for k in (2, 3, 4, 5, 6):
        d, s = drift_per_step(k, args.samples, 40, rng)
        print(f"k={k}: drift/step = {d:+.4f} bits   steps/hop = {s:.2f}")
    print("   (theory: (log2(3)-2)/3 = "
          f"{(math.log2(3) - 2) / 3:+.4f} per Collatz step, k-independent by "
          "Wald's identity since N = number of FMF sub-hops is a stopping time)")

    print("\n== 2b. Long orbit: chunking-invariant drift; next-hop ratio by prev v_2 ==")
    d, cond = long_orbit_drift(4000, 3000, rng)
    print(f"long-orbit drift/step = {d:+.4f} bits")
    for key, (mean_lr, n) in cond.items():
        print(f"  E[log2 hop ratio | previous landing {key}] = {mean_lr:+.3f} "
              f"(n={n})")

    print("\n== 3. Worst-case single-hop ratio |F_k(x)|/x vs bit-length ==")
    for k in (2, 3, 4, 5):
        row = []
        for bits in (8, 12, 16, 20, 24, 28):
            w, wx = worst_ratio(k, bits, args.samples, rng)
            row.append(f"{bits}b:{w:7.1f}")
        print(f"k={k}: " + "  ".join(row))

    print("\n== 4. Fraction of x with F_k(x) > x (growth) ==")
    for k in (2, 3, 4, 5, 6, 8):
        g = 0
        n = 0
        for _ in range(args.samples):
            x = rng.getrandbits(32) | 1
            if x < 5:
                continue
            y, _, _ = fm2k_hop(x, k)
            n += 1
            g += y > x
        print(f"k={k}: P(growth) = {g / n:.4f}")


if __name__ == "__main__":
    main()
