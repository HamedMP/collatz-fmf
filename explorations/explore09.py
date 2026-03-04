"""
explore09.py - Accelerated Collatz via FMF: skip entire blocks of iterations

We now have everything needed to "fast-forward" through Collatz sequences:

Given odd x:
1. Classify: x ≡ 1 mod 4 or x ≡ 3 mod 4
2. If x ≡ 1 mod 4: FMF = 4*(3k+1) where k=(x-1)/4. Steps = 1.
3. If x ≡ 3 mod 4, k even: FMF = 4*(9j+4) where j=k/2. Steps = 3.
4. If x ≡ 3 mod 4, k odd: FMF = 3^(t+2)*(k+1)/2^(t-1) - 2. Steps = 3+2t.
5. Divide FMF by LPT to get next odd number. Total steps += v_2(FMF).

This gives O(log(x)) FMF hops instead of O(x^?) Collatz steps.
Let's verify this produces the correct trajectory.
"""


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def collatz_to_one(n):
    """Standard Collatz, returns total steps to reach 1."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def fmf_accelerated(x_start):
    """Compute Collatz trajectory using FMF acceleration.
    Returns (total_collatz_steps, fmf_hops, trajectory_of_odd_numbers)."""
    x = x_start
    total_steps = 0
    hops = 0
    trajectory = [x]

    while x != 1:
        if x % 2 == 0:
            # x is even: just divide by LPT to get odd
            p = v2(x)
            x = x >> p
            total_steps += p
            trajectory.append(x)
            continue

        mod4 = x % 4
        if mod4 == 1:
            k = (x - 1) // 4
            fmf = 4 * (3 * k + 1)
            fmf_collatz_steps = 1  # one 3x+1 step
        elif mod4 == 3:
            k = (x - 3) // 4
            if k % 2 == 0:
                j = k // 2
                fmf = 4 * (9 * j + 4)
                fmf_collatz_steps = 3
            else:
                t = v2(k + 1)
                fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
                fmf_collatz_steps = 3 + 2 * t
        else:
            break  # shouldn't reach here

        # Now divide FMF by its LPT
        p = v2(fmf)
        odd_after = fmf >> p
        total_steps += fmf_collatz_steps + p  # FMF steps + division steps
        hops += 1
        x = odd_after
        trajectory.append(x)

    return total_steps, hops, trajectory


# Verify against standard Collatz
print("=== Verifying FMF-accelerated Collatz ===\n")
errors = 0
for n in range(3, 10001, 2):
    standard_steps = collatz_to_one(n)
    accel_steps, hops, traj = fmf_accelerated(n)
    if standard_steps != accel_steps:
        errors += 1
        if errors <= 5:
            print(f"MISMATCH: n={n}, standard={standard_steps}, accel={accel_steps}")

print(f"Verified {5000} odd numbers [3, 10001]: {errors} errors\n")


# Show some trajectories
print("=== FMF-accelerated trajectories (odd milestones only) ===\n")
for n in [7, 27, 31, 127, 255, 703, 9663, 27]:
    steps, hops, traj = fmf_accelerated(n)
    traj_str = " -> ".join(str(x) for x in traj[:20])
    if len(traj) > 20:
        traj_str += f" -> ... -> {traj[-1]}"
    print(f"x={n:>5}: {steps:>4} Collatz steps, {hops:>3} FMF hops, "
          f"{len(traj):>3} odd milestones")
    print(f"         {traj_str}\n")


# Performance comparison
import time

print("=== Performance: FMF acceleration vs brute force ===\n")
test_numbers = [2**n - 1 for n in range(10, 31)]
for n in test_numbers:
    t0 = time.time()
    s1 = collatz_to_one(n)
    t1 = time.time()
    s2, hops, traj = fmf_accelerated(n)
    t2 = time.time()

    brute_time = t1 - t0
    accel_time = t2 - t1
    speedup = brute_time / accel_time if accel_time > 0 else float('inf')
    print(f"x=2^{n.bit_length()-1}-1 ({n:>12}): steps={s1:>6}, "
          f"hops={hops:>4}, milestones={len(traj):>5}, "
          f"brute={brute_time*1000:>8.3f}ms, accel={accel_time*1000:>8.3f}ms, "
          f"speedup={speedup:>6.1f}x")


# The "compression ratio": how many Collatz steps per FMF hop
print(f"\n\n=== Compression ratio: Collatz steps per FMF hop ===")
ratios = []
for n in range(3, 100001, 2):
    steps, hops, _ = fmf_accelerated(n)
    if hops > 0:
        ratios.append(steps / hops)

import statistics
print(f"Mean steps/hop:   {statistics.mean(ratios):.2f}")
print(f"Median steps/hop: {statistics.median(ratios):.2f}")
print(f"Min steps/hop:    {min(ratios):.2f}")
print(f"Max steps/hop:    {max(ratios):.2f}")
