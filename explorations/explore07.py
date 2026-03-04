"""
explore07.py - The hard cases: numbers requiring many FMF hops

Which numbers require the most FMF hops to descend?
What structural property makes them hard?
Are 2^n - 1 numbers always the hardest?
"""
from collections import defaultdict


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def tzb(k):
    return v2(k + 1)


def fmf_chain_hops(x_start, max_hops=200):
    """Count FMF hops to descend below x_start."""
    x = x_start
    for hop in range(max_hops):
        mod4 = x % 4
        if mod4 == 1:
            k_val = (x - 1) // 4
            fmf = 4 * (3 * k_val + 1)
        elif mod4 == 3:
            k_val = (x - 3) // 4
            if k_val % 2 == 0:
                j = k_val // 2
                fmf = 4 * (9 * j + 4)
            else:
                t = tzb(k_val)
                fmf = 3**(t + 2) * (k_val + 1) // 2**(t - 1) - 2
        else:
            return hop, True

        v = v2(fmf)
        odd_after = fmf >> v

        if odd_after < x_start or odd_after == 1:
            return hop + 1, True
        x = odd_after

    return max_hops, False


# Find the hardest numbers in a range
print("=== Hardest numbers (most FMF hops to descend) in [3, 10000] ===\n")
results = []
for x in range(3, 10001, 2):  # odd numbers only
    hops, ok = fmf_chain_hops(x)
    results.append((hops, x))

results.sort(reverse=True)
print(f"{'rank':>4} {'x':>8} {'binary':>25} {'hops':>6} {'form':>15}")
for rank, (hops, x) in enumerate(results[:40], 1):
    binary = bin(x)[2:]
    # Check if x = 2^n - 1
    is_mersenne = all(b == '1' for b in binary)
    form = f"2^{len(binary)}-1" if is_mersenne else ""
    if not form:
        # Check other forms
        if (x + 1) & x == 0:
            form = f"2^{len(binary)}-1"
        elif x % 4 == 3:
            k = (x - 3) // 4
            form = f"4*{k}+3, k={k}"
    print(f"{rank:>4} {x:>8} {binary:>25} {hops:>6} {form:>15}")


# Focus on 2^n - 1 numbers
print(f"\n\n=== 2^n - 1 numbers (Mersenne-like) ===")
print(f"{'n':>4} {'x=2^n-1':>12} {'hops':>6} {'hops/n':>8}")
for n in range(2, 22):
    x = 2**n - 1
    hops, ok = fmf_chain_hops(x)
    print(f"{n:>4} {x:>12} {hops:>6} {hops/n:>8.2f}")


# Explore what makes numbers hard: the "consecutive 1s in binary" hypothesis
print(f"\n\n=== Consecutive 1-bits and hop count ===")
print(f"{'x':>8} {'binary':>20} {'max_consec_1s':>14} {'total_1s':>9} {'hops':>6}")

for hops, x in results[:30]:
    binary = bin(x)[2:]
    # Count max consecutive 1s
    max_ones = max(len(s) for s in binary.split('0'))
    total_ones = binary.count('1')
    print(f"{x:>8} {binary:>20} {max_ones:>14} {total_ones:>9} {hops:>6}")


# Explore: is there a pattern in the k values that appear in FMF chains of hard numbers?
print(f"\n\n=== FMF chain detail for x=27 (a famously hard small number) ===")
x = 27
chain = []
for hop in range(50):
    mod4 = x % 4
    if mod4 == 1:
        k_val = (x - 1) // 4
        case = "4k+1"
        t = 0
    elif mod4 == 3:
        k_val = (x - 3) // 4
        if k_val % 2 == 0:
            case = "4k+3,k_even"
            t = 0
        else:
            case = "4k+3,k_odd"
            t = tzb(k_val)
    else:
        break

    if case == "4k+1":
        fmf = 4 * (3 * k_val + 1)
    elif case == "4k+3,k_even":
        j = k_val // 2
        fmf = 4 * (9 * j + 4)
    else:
        fmf = 3**(t + 2) * (k_val + 1) // 2**(t - 1) - 2

    v = v2(fmf)
    odd_after = fmf >> v
    print(f"  hop {hop+1:>2}: x={x:>6} ({case:>14}, k={k_val:>4}, t={t}) -> FMF={fmf:>8}, v2={v:>2}, odd={odd_after:>6}")
    if odd_after < 27 or odd_after == 1:
        break
    x = odd_after


# Now explore the average hops as a function of number size (bit length)
print(f"\n\n=== Average FMF hops by bit length ===")
by_bits = defaultdict(list)
for x in range(3, 50001, 2):
    hops, _ = fmf_chain_hops(x)
    bits = x.bit_length()
    by_bits[bits].append(hops)

print(f"{'bits':>5} {'count':>7} {'avg_hops':>10} {'max_hops':>10} {'median':>8}")
for bits in sorted(by_bits):
    vals = by_bits[bits]
    vals_sorted = sorted(vals)
    median = vals_sorted[len(vals_sorted)//2]
    print(f"{bits:>5} {len(vals):>7} {sum(vals)/len(vals):>10.2f} {max(vals):>10} {median:>8}")
