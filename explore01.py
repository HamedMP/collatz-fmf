"""
explore01.py - Verify FMF formula for large ranges

FMF Conjecture: For x = 4k+3 (k odd), the first multiple of 4 in the
Collatz sequence appears at step: fmf_step = 3 + 2 * TZB(k)
where TZB(k) = number of trailing zeros in binary of (k+1).

Also verifies:
- Case 4k+1: always reaches multiple of 4 in exactly 1 step (via 3x+1)
- Case 4k+3 (k even): always reaches multiple of 4 in exactly 3 steps
"""


def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def tzb(k):
    """Trailing zero bits of (k+1)."""
    n = k + 1
    count = 0
    while n & 1 == 0:
        count += 1
        n >>= 1
    return count


def find_fmf_step(x):
    """Find the step where Collatz sequence first hits a multiple of 4."""
    n = x
    for step in range(1, 10000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None


def verify_range(max_k):
    """Verify FMF formula for all odd k up to max_k."""
    failures_4k1 = 0
    failures_4k3_even = 0
    failures_4k3_odd = 0
    total_4k1 = 0
    total_4k3_even = 0
    total_4k3_odd = 0

    for k in range(0, max_k):
        # Case 1: 4k+1
        x = 4 * k + 1
        if x > 1:
            total_4k1 += 1
            step, fmf = find_fmf_step(x)
            # 3(4k+1)+1 = 12k+4 = 4(3k+1), so step should be 1
            if step != 1:
                failures_4k1 += 1
                if failures_4k1 <= 5:
                    print(f"FAIL 4k+1: k={k}, x={x}, step={step}")

        # Case 2: 4k+3, k even
        if k % 2 == 0:
            x = 4 * k + 3
            total_4k3_even += 1
            step, fmf = find_fmf_step(x)
            expected_step = 3  # from the derivation
            if step != expected_step:
                failures_4k3_even += 1
                if failures_4k3_even <= 5:
                    print(f"FAIL 4k+3 (k even): k={k}, x={x}, step={step}, expected={expected_step}")

        # Case 3: 4k+3, k odd -- THE KEY CONJECTURE
        if k % 2 == 1:
            x = 4 * k + 3
            total_4k3_odd += 1
            step, fmf = find_fmf_step(x)
            expected_step = 3 + 2 * tzb(k)
            if step != expected_step:
                failures_4k3_odd += 1
                if failures_4k3_odd <= 5:
                    print(f"FAIL 4k+3 (k odd): k={k}, x={x}, TZB={tzb(k)}, step={step}, expected={expected_step}")

    print(f"\n=== Results for k in [0, {max_k}) ===")
    print(f"4k+1:           {total_4k1:>8} tested, {failures_4k1} failures")
    print(f"4k+3 (k even):  {total_4k3_even:>8} tested, {failures_4k3_even} failures")
    print(f"4k+3 (k odd):   {total_4k3_odd:>8} tested, {failures_4k3_odd} failures")

    if failures_4k1 == 0 and failures_4k3_even == 0 and failures_4k3_odd == 0:
        print("\nAll cases PASSED.")
    else:
        print("\nSome cases FAILED!")


if __name__ == "__main__":
    import time
    for max_k in [1000, 100_000, 1_000_000]:
        t0 = time.time()
        verify_range(max_k)
        print(f"Time: {time.time() - t0:.2f}s\n")
