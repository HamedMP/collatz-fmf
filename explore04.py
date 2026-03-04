"""
explore04.py - Deep dive into FMF chains and the multiplicative dynamics

After hitting FMF and dividing by LPT, we get an odd number. This number is either:
  - 4k'+1 form: next step hits multiple of 4 immediately (1 step)
  - 4k'+3 form: we apply the FMF formula again

Key questions:
1. What's the "net multiplier" at each FMF hop? (ratio of odd_after to odd_before)
2. Is the product of multipliers < 1 after enough hops? (this would prove descent)
3. Is there structure in which 4k+1 vs 4k+3 we land on?
"""
from math import log2, log


def tzb(k):
    n = k + 1
    count = 0
    while n & 1 == 0:
        count += 1
        n >>= 1
    return count


def v2(n):
    """2-adic valuation of n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def find_fmf_brute(x):
    n = x
    for step in range(1, 100000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None


def lpt(n):
    power = 0
    while n % 2 == 0:
        n //= 2
        power += 1
    return n, power


def fmf_chain_detail(x_start, max_hops=50):
    """Detailed FMF chain with multiplier analysis."""
    x = x_start
    total_log_multiplier = 0.0
    hops = []

    for hop in range(max_hops):
        # Classify x mod 4
        mod4 = x % 4
        if mod4 == 1:
            k_val = (x - 1) // 4
            case = "4k+1"
            # 3(4k+1)+1 = 4(3k+1), one step
            fmf = 4 * (3 * k_val + 1)
            fmf_step = 1
        elif mod4 == 3:
            k_val = (x - 3) // 4
            if k_val % 2 == 0:
                case = "4k+3,k_even"
                # 3 steps to multiple of 4
                j = k_val // 2
                fmf = 4 * (9 * j + 4)
                fmf_step = 3
            else:
                case = "4k+3,k_odd"
                t = tzb(k_val)
                fmf_step = 3 + 2 * t
                # FMF = 3^(t+2) * (k+1) / 2^(t-1) - 2
                fmf = 3**(t + 2) * (k_val + 1) // 2**(t - 1) - 2
        else:
            break  # shouldn't happen for odd x

        odd_after, lpt_power = lpt(fmf)
        multiplier = odd_after / x
        log_mult = log(odd_after / x) / log(2) if odd_after > 0 else 0
        total_log_multiplier += log_mult

        hops.append({
            'x': x,
            'case': case,
            'fmf_step': fmf_step,
            'fmf': fmf,
            'v2_fmf': lpt_power,
            'odd_after': odd_after,
            'multiplier': multiplier,
            'log2_mult': log_mult,
            'cumulative_log2': total_log_multiplier,
        })

        if odd_after < x_start or odd_after == 1:
            return hops, True
        x = odd_after

    return hops, False


# Detailed trace for some interesting numbers
print("=" * 120)
print("Detailed FMF chains for selected starting values")
print("=" * 120)

for x_start in [7, 27, 31, 63, 127, 255, 511, 703, 871]:
    hops, descended = fmf_chain_detail(x_start)
    print(f"\n--- x = {x_start} ({len(hops)} hops) ---")
    print(f"{'hop':>3} {'x':>8} {'case':>14} {'fmf_step':>8} {'FMF':>10} {'v2(FMF)':>7} {'odd_after':>10} "
          f"{'mult':>8} {'log2(m)':>8} {'cumul':>8}")
    for i, h in enumerate(hops):
        print(f"{i+1:>3} {h['x']:>8} {h['case']:>14} {h['fmf_step']:>8} {h['fmf']:>10} {h['v2_fmf']:>7} "
              f"{h['odd_after']:>10} {h['multiplier']:>8.4f} {h['log2_mult']:>8.3f} {h['cumulative_log2']:>8.3f}")
    if descended:
        print(f"  -> DESCENDED. Net log2 multiplier: {hops[-1]['cumulative_log2']:.3f} "
              f"(net factor: {2**hops[-1]['cumulative_log2']:.4f})")


# Now: the key theoretical question.
# At each hop, the "growth" is from 3^s applications and the "shrinkage" is from 2^v2(FMF).
# Net log2 multiplier at a hop = s*log2(3) - v2(FMF)  (roughly)
# For descent, we need sum of these to be negative.

print("\n\n" + "=" * 120)
print("Growth vs Shrinkage accounting at each hop")
print("=" * 120)
print(f"{'x_start':>8} {'hops':>5} {'total_3x':>8} {'total_div2':>9} {'3x_bits':>8} {'div2_bits':>9} {'net_bits':>9}")

for x_start in range(3, 1000, 4):  # all 4k+3 numbers
    hops, descended = fmf_chain_detail(x_start)
    if not descended:
        continue
    total_3x_steps = 0
    total_div2 = 0
    for h in hops:
        # fmf_step tells us how many Collatz steps, which includes both 3x+1 and /2 steps
        # In cycle (a), each T application = one 3x+1 and one /2. Plus possibly one more 3x+1.
        # Actually, fmf_step is total Collatz steps. Among those, roughly half are 3x+1 and half /2.
        # But after FMF we also divide by v2(FMF).
        # Let's count: the 3x+1 ops contribute log2(3) each, the /2 ops contribute -1 each.
        # fmf_step Collatz steps, then division by 2^v2(FMF)
        # Total multiplier = product of (3n+1 or n/2) / x at each real Collatz step
        total_div2 += h['v2_fmf']
        # Count 3x+1 steps within fmf_step Collatz steps
        # For 4k+1: 1 step which is 3x+1 (result is even, then it's mult of 4 already)
        if h['case'] == '4k+1':
            total_3x_steps += 1
        elif h['case'] == '4k+3,k_even':
            total_3x_steps += 2  # two 3x+1 and one /2 in 3 steps
        else:
            # 4k+3 k odd: fmf_step = 3+2t steps. Pattern is (3x+1, /2) repeated, then 3x+1
            # Number of 3x+1 in fmf_step steps: ceil(fmf_step/2) = (fmf_step+1)/2
            total_3x_steps += (h['fmf_step'] + 1) // 2

    three_bits = total_3x_steps * log2(3)  # growth in bits from 3x+1
    div2_bits = total_div2  # shrinkage from dividing by 2
    # Also need to account for /2 within the fmf_step computation
    total_internal_div2 = sum(h['fmf_step'] for h in hops) - total_3x_steps
    net = three_bits - div2_bits - total_internal_div2

    if x_start < 200 or len(hops) > 10:
        print(f"{x_start:>8} {len(hops):>5} {total_3x_steps:>8} {total_div2:>9} "
              f"{three_bits:>8.2f} {div2_bits + total_internal_div2:>9} {net:>9.2f}")
