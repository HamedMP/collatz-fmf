"""
explore05.py - Algebraic proof of the FMF formula

Conjecture: For x = 4k+3 with k odd, the first multiple of 4 in the Collatz
sequence appears at step fmf_step = 3 + 2*TZB(k), where TZB(k) = v_2(k+1).

Strategy: Prove by induction on t = TZB(k) = v_2(k+1).

Key idea: write k+1 = 2^t * m where m is odd. Then k = 2^t * m - 1.
x = 4k + 3 = 4(2^t * m - 1) + 3 = 2^(t+2) * m - 1.

So x = 2^(t+2)*m - 1 where m is odd and t >= 1.

Let's trace the Collatz sequence step by step for general t.

Step pattern for x = 4k+3 with k odd:
The sequence alternates: 3x+1 (odd->even), /2 (even->odd or even), ...
With the modified view, each "U cycle" is one 3x+1 followed by one /2.

Let's trace using the T_i formula and see WHY fmf_step = 3 + 2t.
"""

from fractions import Fraction


def trace_symbolic(t, m_val=1):
    """Trace Collatz steps for x = 2^(t+2)*m - 1 symbolically.

    We'll use exact fractions to track coefficients of m.
    x = 2^(t+2) * m - 1
    """
    # Express current value as a*m + b (exact rational)
    a = Fraction(2**(t + 2))
    b = Fraction(-1)

    steps = []
    for step in range(1, 30):
        current_form = f"{a}*m + {b}"

        # Determine if a*m + b is odd or even
        # a*m is even iff a is even (since m is odd)
        # a*m + b: parity depends on a (mod 2) and b (mod 2)
        a_even = (a.numerator % 2 == 0) and (a.denominator == 1)
        b_int = b.numerator // b.denominator if b.denominator == 1 else None

        if a.denominator != 1 or b.denominator != 1:
            # Non-integer coefficients - need to be careful
            # Evaluate numerically to check
            val = a * m_val + b
            is_even = val % 2 == 0
            is_mult4 = val % 4 == 0
        else:
            a_int = int(a)
            b_int = int(b)
            # a*m + b: since m is odd, a*m has same parity as a
            # so a*m+b has parity (a+b) mod 2
            is_odd_for_odd_m = (a_int + b_int) % 2 == 1
            is_even = not is_odd_for_odd_m
            # Check mult of 4: a*m + b ≡ 0 mod 4
            # For ALL odd m, need a ≡ 0 mod 4 and b ≡ 0 mod 4
            # Or more precisely: a*m + b mod 4 depends on m mod 4
            # Since m is odd: m ≡ 1 or 3 mod 4
            val1 = a_int * 1 + b_int
            val3 = a_int * 3 + b_int
            is_mult4_all = (val1 % 4 == 0) and (val3 % 4 == 0)
            is_mult4_some = (val1 % 4 == 0) or (val3 % 4 == 0)
            is_mult4 = is_mult4_all

        op = ""
        if is_even:
            # Divide by 2
            a = a / 2
            b = b / 2
            op = "/2"
        else:
            # 3x + 1
            a = 3 * a
            b = 3 * b + 1
            op = "3x+1"

        result_form = f"{a}*m + {b}"

        # Check if result is always multiple of 4
        if a.denominator == 1 and b.denominator == 1:
            a_int = int(a)
            b_int = int(b)
            val1 = a_int * 1 + b_int
            val3 = a_int * 3 + b_int
            mult4 = (val1 % 4 == 0) and (val3 % 4 == 0)
        else:
            mult4 = False

        steps.append((step, op, current_form, result_form, mult4))

        if mult4:
            break

    return steps


print("=" * 100)
print("Symbolic Collatz trace for x = 2^(t+2)*m - 1")
print("=" * 100)

for t in range(1, 8):
    expected_steps = 3 + 2 * t
    print(f"\n--- t = {t}, expected fmf_step = {expected_steps} ---")
    print(f"x = 2^{t+2} * m - 1 = {2**(t+2)}m - 1")

    steps = trace_symbolic(t)
    for step, op, before, after, mult4 in steps:
        marker = " <-- MULT OF 4" if mult4 else ""
        print(f"  Step {step:>2}: {op:>5}  {before:>30} -> {after:>30}{marker}")

    actual_steps = len(steps)
    print(f"  FMF at step {actual_steps}, expected {expected_steps}: {'MATCH' if actual_steps == expected_steps else 'MISMATCH'}")


# Now let's see the general pattern more clearly
print("\n\n" + "=" * 100)
print("Simplified view: tracking coefficients (a, b) where value = a*m + b")
print("=" * 100)

for t in range(1, 10):
    a = Fraction(2**(t + 2))
    b = Fraction(-1)
    print(f"\nt={t}: x = {a}m + {b}")

    for step in range(1, 30):
        # Check parity for odd m
        if a.denominator == 1 and b.denominator == 1:
            parity_test = (int(a) + int(b)) % 2
        else:
            # fractional - evaluate
            parity_test = int(a + b) % 2  # m=1 case

        if parity_test == 1:  # odd
            a, b = 3*a, 3*b + 1
            op = "3x+1"
        else:
            a, b = a/2, b/2
            op = "/2  "

        # Check mult of 4
        if a.denominator == 1 and b.denominator == 1:
            v1 = int(a) * 1 + int(b)
            v3 = int(a) * 3 + int(b)
            m4 = v1 % 4 == 0 and v3 % 4 == 0
        else:
            m4 = False

        marker = " *** FMF ***" if m4 else ""
        print(f"  step {step:>2} {op}: ({a}, {b}){marker}")
        if m4:
            break

# The key insight: let's see what the coefficient of m is at each step
print("\n\n" + "=" * 100)
print("Coefficient of m at FMF step (should relate to 3^(t+2)/2^(t-1))")
print("=" * 100)

for t in range(1, 12):
    a = Fraction(2**(t + 2))
    b = Fraction(-1)

    for step in range(1, 50):
        if a.denominator == 1 and b.denominator == 1:
            parity_test = (int(a) + int(b)) % 2
        else:
            parity_test = int(a + b) % 2

        if parity_test == 1:
            a, b = 3*a, 3*b + 1
        else:
            a, b = a/2, b/2

        if a.denominator == 1 and b.denominator == 1:
            v1 = int(a) * 1 + int(b)
            v3 = int(a) * 3 + int(b)
            m4 = v1 % 4 == 0 and v3 % 4 == 0
        else:
            m4 = False

        if m4:
            expected_a = Fraction(3**(t+2), 2**(t-1))
            print(f"t={t:>2}: FMF at step {step:>2} (expected {3+2*t:>2}), "
                  f"value = {a}*m + {b}, "
                  f"expected coeff = {expected_a}, "
                  f"match_a={a == expected_a}, match_b={b == Fraction(-2)}")
            break
