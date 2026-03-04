"""
explore02.py - Analyze FMF values (not just steps)

For x = 4k+3, we know WHEN we hit the first multiple of 4 (fmf_step = 3 + 2*TZB(k)).
But WHAT is that multiple of 4? Is there a closed-form for the FMF value itself?

We already have T_i(x) = 3^i*(x+1)/2^i - 1 and find_fmf from the notebook.
Let's see if the FMF value follows a pattern related to k and TZB(k).
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


def find_fmf(x):
    n = x
    for step in range(1, 10000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None


def T(x, i):
    """T_i(x) = 3^i * (x+1) / 2^i - 1"""
    return 3**i * (x + 1) // 2**i - 1


def compute_fmf_value(k):
    """Compute FMF value using the formula path."""
    x = 4 * k + 3
    fmf_steps = 3 + 2 * tzb(k)

    if fmf_steps % 2 == 0:
        u_steps = fmf_steps // 2
        return T(x, u_steps)
    else:
        u_steps = (fmf_steps - 1) // 2
        odd_result = T(x, u_steps)
        return 3 * odd_result + 1


print("=" * 90)
print("Exploring FMF VALUES for x = 4k+3 (k odd)")
print("=" * 90)

print(f"\n{'k':>5} {'x=4k+3':>7} {'TZB':>4} {'step':>5} {'FMF':>8} {'FMF/x':>8} {'FMF/4':>8} {'FMF/(4x)':>9}")
print("-" * 90)

for k in range(1, 64, 2):
    x = 4 * k + 3
    step, fmf = find_fmf(x)
    ratio = fmf / x
    fmf_div4 = fmf // 4
    print(f"{k:>5} {x:>7} {tzb(k):>4} {step:>5} {fmf:>8} {ratio:>8.3f} {fmf_div4:>8} {fmf/(4*x):>9.4f}")

# Look for formula: for k odd with TZB(k)=t, what's FMF in terms of k?
print("\n\n" + "=" * 90)
print("Grouping by TZB value to find FMF formula")
print("=" * 90)

for t in range(1, 8):
    print(f"\n--- TZB = {t}, fmf_step = {3 + 2*t} ---")
    print(f"{'k':>6} {'x=4k+3':>8} {'FMF':>10} {'FMF/x':>10} {'FMF formula check':>20}")
    items = []
    for k in range(1, 2000, 2):
        if tzb(k) == t:
            x = 4 * k + 3
            step, fmf = find_fmf(x)
            fmf_formula = compute_fmf_value(k)
            items.append((k, x, fmf, fmf / x))
            if len(items) <= 12:
                # Try to find linear relationship: FMF = a*k + b
                print(f"{k:>6} {x:>8} {fmf:>10} {fmf/x:>10.4f} {'OK' if fmf == fmf_formula else 'MISMATCH':>20}")

    if len(items) >= 3:
        # Check if FMF is linear in k: FMF = a*k + b
        k1, _, fmf1, _ = items[0]
        k2, _, fmf2, _ = items[1]
        a = (fmf2 - fmf1) / (k2 - k1)
        b = fmf1 - a * k1
        # Verify on third
        k3, _, fmf3, _ = items[2]
        predicted = a * k3 + b
        print(f"  Linear fit: FMF = {a:.1f}*k + {b:.1f}")
        print(f"  Verification on k={k3}: predicted={predicted:.1f}, actual={fmf3}, match={abs(predicted - fmf3) < 0.5}")

        # Express a as ratio of powers of 3 and 2
        # fmf_step = 3 + 2t, so we apply ceil((3+2t)/2) = t+2 applications of T
        # T_i(4k+3) = 3^i * (4k+4) / 2^i - 1 = 3^i * 4(k+1) / 2^i - 1
        i = t + 1  # number of T applications (roughly)
        print(f"  Note: 3^(t+1)/2^(t-1) = {3**(t+1) / 2**(t-1):.1f}, 3^(t+2)/2^t = {3**(t+2)/2**t:.1f}, a={a:.1f}")
        print(f"  a * 4 / 3^(t+2) = {a * 4 / 3**(t+2):.6f}")
        print(f"  a / (3^(t+1)) = {a / 3**(t+1):.6f}")
