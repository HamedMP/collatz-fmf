"""
explore03.py - The descent question: after FMF, does dividing by LPT bring us below x?

FMF is always LARGER than x (ratio ~ (3/2)^(t+1) * 3/2).
But FMF is a multiple of 4, so we divide by LPT (largest power of 2).
The key question: is FMF / LPT(FMF) < x?

If not immediately, how many "FMF hops" until we get below x?
An FMF hop = reach FMF -> divide by LPT -> classify mod 4 -> find next FMF -> ...
"""


def tzb(k):
    n = k + 1
    count = 0
    while n & 1 == 0:
        count += 1
        n >>= 1
    return count


def lpt(n):
    """Largest power of 2 dividing n. Returns (odd_part, power)."""
    power = 0
    while n % 2 == 0:
        n //= 2
        power += 1
    return n, power


def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def find_fmf_brute(x):
    """Returns (step, fmf_value) for first multiple of 4 in Collatz seq of x."""
    n = x
    for step in range(1, 100000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None


def trace_fmf_chain(x_start, max_hops=100):
    """
    Starting from x (odd), repeatedly:
    1. Find FMF (first multiple of 4 in Collatz sequence)
    2. Divide by LPT to get odd part
    3. If odd part < x_start, we have descent. Done.
    4. Otherwise, the odd part is a new odd number -- continue.
    """
    x = x_start
    chain = []
    for hop in range(max_hops):
        step, fmf = find_fmf_brute(x)
        if fmf is None:
            break
        odd_part, power = lpt(fmf)
        chain.append({
            'x': x,
            'fmf': fmf,
            'fmf_step': step,
            'lpt_power': power,
            'odd_after': odd_part,
            'ratio': odd_part / x_start,
        })
        if odd_part < x_start:
            return chain, True  # descent achieved
        if odd_part == 1:
            return chain, True  # reached 1
        x = odd_part
    return chain, False


print("=" * 100)
print("FMF Chain Analysis: how many hops to descend below starting value?")
print("=" * 100)

# Test on first several 4k+3 numbers
descent_hops = []
for k in range(0, 200):
    x = 4 * k + 3
    chain, descended = trace_fmf_chain(x)
    hops = len(chain)
    descent_hops.append(hops)
    if k < 30 or hops > 5:
        final_ratio = chain[-1]['ratio'] if chain else 0
        lpt_powers = [c['lpt_power'] for c in chain]
        print(f"x={x:>5} (k={k:>3}): {hops} hops to descend, "
              f"LPT powers={lpt_powers}, "
              f"final_odd={chain[-1]['odd_after'] if chain else '?':>6}, "
              f"ratio={final_ratio:.4f}, "
              f"{'DESCENDED' if descended else 'NO DESCENT'}")

print(f"\n=== Distribution of hops to descend (k=0..199, x=3..799) ===")
from collections import Counter
counts = Counter(descent_hops)
for hops in sorted(counts):
    print(f"  {hops} hops: {counts[hops]} numbers ({counts[hops]/len(descent_hops)*100:.1f}%)")


# Now let's look deeper: what determines whether 1 hop suffices?
print("\n\n" + "=" * 100)
print("When does 1 FMF hop suffice? (FMF/LPT < x)")
print("=" * 100)
print(f"{'k':>5} {'x':>7} {'TZB':>4} {'FMF':>10} {'LPT_pow':>8} {'odd_after':>10} {'odd/x':>8} {'1-hop?':>7}")

one_hop_count = 0
total = 0
for k in range(1, 500, 2):  # k odd only
    x = 4 * k + 3
    total += 1
    t = tzb(k)
    _, fmf = find_fmf_brute(x)
    odd_part, power = lpt(fmf)
    one_hop = odd_part < x
    if one_hop:
        one_hop_count += 1
    if k < 60 or (not one_hop and k < 200):
        print(f"{k:>5} {x:>7} {t:>4} {fmf:>10} {power:>8} {odd_part:>10} {odd_part/x:>8.4f} {'YES' if one_hop else 'no':>7}")

print(f"\n1-hop descent rate (k odd, 1-499): {one_hop_count}/{total} = {one_hop_count/total*100:.1f}%")


# Key question: what's the LPT of the FMF?
# FMF = 3^(t+2) * (k+1) / 2^(t-1) - 2
# Since k+1 = 2^t * m (m odd), FMF = 3^(t+2) * 2^t * m / 2^(t-1) - 2 = 3^(t+2) * 2m - 2 = 2(3^(t+2)*m - 1)
# v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)
# Since 3^(t+2)*m is odd, 3^(t+2)*m - 1 is even.
# v_2(FMF) = 1 + v_2(3^(t+2)*m - 1) >= 2 (good, it's a multiple of 4)
# The actual LPT depends on v_2(3^(t+2)*m - 1), which relates to the "lifting the exponent" lemma
print("\n\n" + "=" * 100)
print("v_2(FMF) analysis: what determines the LPT of FMF?")
print("FMF = 2 * (3^(t+2)*m - 1) where k+1 = 2^t * m")
print("=" * 100)
print(f"{'k':>5} {'t':>3} {'m':>6} {'3^(t+2)*m':>12} {'v2(FMF)':>8} {'FMF':>10}")

for k in range(1, 128, 2):
    t = tzb(k)
    m = (k + 1) >> t
    val = 3**(t + 2) * m
    fmf = 2 * (val - 1)
    _, v2 = lpt(fmf)
    if k < 40 or v2 >= 5:
        print(f"{k:>5} {t:>3} {m:>6} {val:>12} {v2:>8} {fmf:>10}")
