"""
explore02b.py - Verify the closed-form FMF VALUE formula

Derived formula: For x = 4k+3 with k odd, t = TZB(k):
    FMF = 3^(t+2) * (k+1) / 2^(t-1) - 2

Derivation:
    fmf_step = 3 + 2t (always odd since k is odd => t >= 1)
    u_steps = (fmf_step - 1) / 2 = t + 1
    T_{t+1}(x) = 3^(t+1) * (x+1) / 2^(t+1) - 1
    FMF = 3 * T_{t+1}(x) + 1   (the extra 3x+1 since fmf_step is odd)
        = 3^(t+2) * (x+1) / 2^(t+1) - 2
        = 3^(t+2) * 4(k+1) / 2^(t+1) - 2
        = 3^(t+2) * (k+1) / 2^(t-1) - 2
"""


def tzb(k):
    n = k + 1
    count = 0
    while n & 1 == 0:
        count += 1
        n >>= 1
    return count


def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def find_fmf_brute(x):
    n = x
    for step in range(1, 10000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None


def fmf_formula(k):
    """Closed-form FMF value for x = 4k+3 (k odd)."""
    t = tzb(k)
    return 3**(t + 2) * (k + 1) // 2**(t - 1) - 2


def verify(max_k):
    failures = 0
    total = 0
    for k in range(1, max_k, 2):
        x = 4 * k + 3
        total += 1
        _, fmf_actual = find_fmf_brute(x)
        fmf_pred = fmf_formula(k)
        if fmf_actual != fmf_pred:
            failures += 1
            if failures <= 5:
                print(f"FAIL: k={k}, x={x}, actual={fmf_actual}, predicted={fmf_pred}")
    print(f"Verified {total} values (k odd, 1 to {max_k}): {failures} failures")
    return failures == 0


# Also verify for k even (case 2: 4k+3 with k even -> always 3 steps)
def fmf_formula_k_even(k):
    """For x=4k+3, k even: 3 steps, FMF = 4(9j+4) where k=2j"""
    j = k // 2
    # From derivation: 3(4k+3)+1 = 12k+10, /2 = 6k+5, 3(6k+5)+1 = 18k+16 = 2(9k+8)
    # Wait let me trace: x=4k+3, k even=2j -> x=8j+3
    # Step 1: 3(8j+3)+1 = 24j+10
    # Step 2: (24j+10)/2 = 12j+5
    # Step 3: 3(12j+5)+1 = 36j+16 = 4(9j+4) ✓
    return 4 * (9 * (k // 2) + 4)


def verify_k_even(max_k):
    failures = 0
    total = 0
    for k in range(0, max_k, 2):
        x = 4 * k + 3
        total += 1
        _, fmf_actual = find_fmf_brute(x)
        fmf_pred = fmf_formula_k_even(k)
        if fmf_actual != fmf_pred:
            failures += 1
            if failures <= 5:
                print(f"FAIL (k even): k={k}, x={x}, actual={fmf_actual}, predicted={fmf_pred}")
    print(f"Verified {total} values (k even, 0 to {max_k}): {failures} failures")
    return failures == 0


if __name__ == "__main__":
    import time

    print("=== Verifying FMF VALUE formula (k odd) ===")
    t0 = time.time()
    verify(100_000)
    print(f"Time: {time.time() - t0:.2f}s\n")

    print("=== Verifying FMF VALUE formula (k even) ===")
    t0 = time.time()
    verify_k_even(100_000)
    print(f"Time: {time.time() - t0:.2f}s\n")

    print("=== Large-scale verification (k odd) ===")
    t0 = time.time()
    verify(1_000_000)
    print(f"Time: {time.time() - t0:.2f}s\n")

    # Show the growth ratio FMF/x for different TZB values
    print("=== FMF/x ratio by TZB ===")
    print(f"{'TZB':>4} {'asymptotic FMF/x':>18} {'= 3^(t+2)/2^(t+1)':>20}")
    for t in range(1, 12):
        ratio = 3**(t + 2) / 2**(t + 1)
        print(f"{t:>4} {ratio:>18.4f} {'':>20}")
