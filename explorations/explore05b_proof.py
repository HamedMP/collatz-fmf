"""
explore05b_proof.py - Complete algebraic proof of FMF step formula

THEOREM: For x = 4k+3 with k odd, the first multiple of 4 in the Collatz
sequence of x appears at step fmf_step = 3 + 2*v_2(k+1), where v_2 is
the 2-adic valuation (number of trailing zeros in binary).

PROOF:

Let t = v_2(k+1) >= 1 (since k is odd, k+1 is even, so t >= 1).
Write k+1 = 2^t * m where m is odd.
Then x = 4k+3 = 4(2^t*m - 1) + 3 = 2^(t+2)*m - 1.

We track the sequence as (a*m + b) where a is the coefficient of m and b is constant.
Initial state: (a_0, b_0) = (2^(t+2), -1). Value is odd since 2^(t+2)*m is even.

CLAIM: The sequence strictly alternates 3x+1 and /2 for 2t+3 steps:
  - After odd  step 2j+1: (a, b) = (3^(j+1) * 2^(t+2-j), -2)
  - After even step 2j:   (a, b) = (3^j * 2^(t+2-j), -1)

Proof of claim by induction on step:

Base: step 1 (3x+1): a = 3*2^(t+2), b = 3*(-1)+1 = -2.
  Formula gives j=0: a = 3^1 * 2^(t+2), b = -2. MATCH.

Inductive step (even): Given step 2j+1 has (3^(j+1)*2^(t+2-j), -2).
  Since t+2-j >= 2 (for j <= t), value = 3^(j+1)*2^(t+2-j)*m - 2.
  First term divisible by 4, so value ≡ -2 ≡ 2 (mod 4). EVEN but NOT mult of 4.
  Apply /2: a = 3^(j+1)*2^(t+1-j), b = -1.
  This is step 2j+2 = 2(j+1). Formula gives: a = 3^(j+1)*2^(t+2-(j+1)) = 3^(j+1)*2^(t+1-j). MATCH.

  Value = 3^(j+1)*2^(t+1-j)*m - 1.
  Since t+1-j >= 1 (for j <= t), first term is even, so value is ODD. ✓

Inductive step (odd): Given step 2j has (3^j*2^(t+2-j), -1), value is odd.
  Apply 3x+1: a = 3^(j+1)*2^(t+2-j), b = -2.
  This is step 2j+1. Formula gives j: a = 3^(j+1)*2^(t+2-j). MATCH. ✓

MULTIPLE OF 4 CHECK:

After odd step 2j+1: value = 3^(j+1)*2^(t+2-j)*m - 2.
  - For j < t+1: power of 2 in first term is t+2-j >= 2, so first term ≡ 0 (mod 4),
    hence value ≡ -2 (mod 4). Divisible by 2 but NOT by 4.
  - For j = t+1 (step 2t+3): power of 2 is t+2-(t+1) = 1.
    Value = 2*3^(t+2)*m - 2 = 2(3^(t+2)*m - 1).
    Since 3^(t+2) is odd and m is odd, their product is odd, so 3^(t+2)*m - 1 is EVEN.
    Hence value = 2 * (even) = divisible by 4. ✓

After even step 2j: value = 3^j*2^(t+2-j)*m - 1.
  This is always ODD (shown above), hence never divisible by 4.

THEREFORE: The first multiple of 4 appears at step 2(t+1)+1 = 2t+3 = 3+2t = 3+2*v_2(k+1). QED.

FMF VALUE: At step 2t+3, value = 2(3^(t+2)*m - 1) where m = (k+1)/2^t.
  Hence FMF = 3^(t+2)*(k+1)/2^(t-1) - 2. ✓
"""

# Verification that the proof is correct by checking all claims
from fractions import Fraction


def verify_proof_claims(max_t=15):
    """Verify every algebraic claim in the proof."""
    print("Verifying proof claims for t = 1 to", max_t)
    all_ok = True

    for t in range(1, max_t + 1):
        # Initial state
        a = Fraction(2**(t + 2))
        b = Fraction(-1)

        for step in range(1, 2*t + 4):  # go up to step 2t+3
            j_float = (step - 1) / 2  # for tracking

            if step % 2 == 1:  # odd step: should be 3x+1
                # Verify value is odd: a*m+b for odd m
                # a is even (power of 2 >= 1), b = -1, so a*m+b is odd ✓
                assert b == -1, f"t={t}, step={step}: b should be -1 before 3x+1"
                a_int = int(a)
                assert a_int % 2 == 0, f"t={t}, step={step}: a should be even"

                # Apply 3x+1
                a, b = 3*a, 3*b + 1

                # Verify formula
                j = (step - 1) // 2
                expected_a = Fraction(3**(j+1) * 2**(t+2-j))
                assert a == expected_a, f"t={t}, step={step}: a={a} != expected {expected_a}"
                assert b == -2, f"t={t}, step={step}: b={b} != -2"

                # Check if mult of 4
                # value = a*m - 2 for any odd m
                # a = 3^(j+1) * 2^(t+2-j)
                power_of_2 = t + 2 - j
                if j < t + 1:
                    # power_of_2 >= 2, so a*m ≡ 0 mod 4, value ≡ -2 mod 4
                    assert power_of_2 >= 2, f"t={t}, j={j}: expected power >= 2"
                    # NOT a mult of 4
                elif j == t + 1:
                    # power_of_2 = 1, value = 2*(3^(t+2)*m - 1), which IS mult of 4
                    assert power_of_2 == 1, f"t={t}: expected power = 1 at FMF"
                    assert step == 2*t + 3, f"t={t}: FMF at step {step} != expected {2*t+3}"

            else:  # even step: should be /2
                # Verify value is even but not mult of 4
                assert b == -2, f"t={t}, step={step}: b should be -2 before /2"

                # Apply /2
                a, b = a/2, b/2

                # Verify formula
                j = step // 2
                expected_a = Fraction(3**j * 2**(t+2-j))
                assert a == expected_a, f"t={t}, step={step}: a={a} != expected {expected_a}"
                assert b == -1, f"t={t}, step={step}: b={b} != -1"

        print(f"  t={t:>2}: All claims verified. FMF at step {2*t+3}.")

    print(f"\nAll proof claims verified for t = 1..{max_t}. QED.")


verify_proof_claims(15)


# Also verify with actual Collatz sequences for many m values
print("\n\nCross-checking with brute-force Collatz for various (t, m) pairs...")

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def find_fmf(x):
    n = x
    for step in range(1, 10000):
        n = collatz_step(n)
        if n % 4 == 0:
            return step, n
    return None, None

errors = 0
total = 0
for t in range(1, 13):
    for m in range(1, 200, 2):  # odd m values
        x = 2**(t+2) * m - 1
        step, fmf = find_fmf(x)
        expected_step = 3 + 2*t
        expected_fmf = 2 * (3**(t+2) * m - 1)
        total += 1
        if step != expected_step or fmf != expected_fmf:
            errors += 1
            if errors <= 5:
                print(f"  MISMATCH: t={t}, m={m}, x={x}: step={step}/{expected_step}, fmf={fmf}/{expected_fmf}")

print(f"Cross-check: {total} cases, {errors} errors.")
