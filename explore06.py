"""
explore06.py - v_2(FMF) analysis and the descent condition

FMF = 2(3^(t+2)*m - 1) where x = 2^(t+2)*m - 1, t = v_2(k+1), m = (k+1)/2^t.

The 2-adic valuation of FMF determines LPT:
  v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)

After dividing by LPT, odd_after = FMF / 2^v_2(FMF) = (3^(t+2)*m - 1) / 2^(v_2(FMF)-1)

For descent (odd_after < x = 2^(t+2)*m - 1), we need:
  (3^(t+2)*m - 1) / 2^(v_2(FMF)-1) < 2^(t+2)*m - 1

This simplifies (ignoring the -1 terms for large m) to:
  3^(t+2) / 2^(v_2(FMF)-1) < 2^(t+2)
  3^(t+2) < 2^(t+2) * 2^(v_2(FMF)-1)
  (3/2)^(t+2) < 2^(v_2(FMF)-1)
  v_2(FMF) > (t+2)*log2(3/2) + 1 ≈ 0.585*(t+2) + 1

So we need v_2(FMF) > ~0.585*t + 2.17 for 1-hop descent.

Key question: what is v_2(3^(t+2)*m - 1)?

By the Lifting the Exponent Lemma (LTE) for p=2:
  v_2(3^n - 1) = v_2(3-1) + v_2(3+1) + v_2(n) - 1 = 1 + 2 + v_2(n) - 1 = v_2(n) + 2
  Wait, that's only for v_2(x^n - y^n). Let me be more careful.

Actually for v_2(3^n - 1):
  - If n is odd: 3^n ≡ 3 mod 4, so 3^n - 1 ≡ 2 mod 4, so v_2 = 1
  - If n is even: 3^n = (3^2)^(n/2) = 9^(n/2).
    v_2(3^n - 1) = v_2(9^(n/2) - 1) = v_2(9-1) + v_2(n/2) = 3 + v_2(n/2) = 3 + v_2(n) - 1 = v_2(n) + 2
    (using the LTE for v_2(x^n - 1) with x odd: v_2(x^n - 1) = v_2(x-1) + v_2(x+1) + v_2(n) - 1)

So v_2(3^n - 1) = { 1 if n odd, v_2(n) + 2 if n even }

Now for v_2(3^(t+2)*m - 1): since m is odd, 3^(t+2)*m ≡ 3^(t+2) mod 2.
Actually we need v_2(3^(t+2)*m - 1) more carefully.

3^(t+2)*m - 1: since 3^(t+2) is odd and m is odd, 3^(t+2)*m is odd, so 3^(t+2)*m - 1 is even.
v_2(3^(t+2)*m - 1) depends on m mod powers of 2.

Let's explore this numerically.
"""
from math import log2


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


# Part 1: v_2(3^n - 1) for various n
print("=== v_2(3^n - 1) pattern ===")
print(f"{'n':>4} {'3^n-1':>15} {'v_2':>5} {'v_2(n)+2 if even':>18}")
for n in range(1, 25):
    val = 3**n - 1
    v = v2(val)
    expected = v2(n) + 2 if n % 2 == 0 else 1
    print(f"{n:>4} {val:>15} {v:>5} {expected:>18} {'✓' if v == expected else 'X'}")


# Part 2: v_2(3^(t+2)*m - 1) for various t and m
print(f"\n\n=== v_2(3^(t+2)*m - 1) for odd m ===")
print(f"{'t':>3} {'m':>5} {'n=t+2':>5} {'3^n*m':>12} {'3^n*m-1':>12} {'v2':>4} {'m mod 2^(v2-1)':>15}")

for t in range(1, 7):
    n = t + 2
    print(f"\n--- t={t}, n={n}, 3^n = {3**n} ---")
    for m in range(1, 32, 2):
        val = 3**n * m - 1
        v = v2(val)
        # What determines v2? It's v_2(3^n * m - 1).
        # 3^n * m ≡ 1 (mod 2^v) and 3^n * m ≢ 1 (mod 2^(v+1))
        # i.e., m ≡ (3^n)^{-1} (mod 2^v) (since 3^n is odd, it has an inverse mod any power of 2)
        print(f"{t:>3} {m:>5} {n:>5} {3**n * m:>12} {val:>12} {v:>4}")


# Part 3: The descent condition
# For 1-hop descent: v_2(FMF) > (t+2)*log2(3/2) + 1
# v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)
# So need: v_2(3^(t+2)*m - 1) > (t+2)*log2(3/2) ≈ 0.585*(t+2)
print(f"\n\n=== Descent condition analysis ===")
print(f"{'t':>3} {'threshold':>10} {'v2 needed':>10}")
for t in range(1, 15):
    threshold = (t + 2) * log2(3/2)
    print(f"{t:>3} {threshold:>10.3f} {int(threshold) + 1:>10}")


# Part 4: For what fraction of odd m does 1-hop descent work, by t?
print(f"\n\n=== Fraction of odd m giving 1-hop descent, by t ===")
print(f"{'t':>3} {'v2_needed':>10} {'frac (of 1000 odd m)':>22} {'density':>8}")
for t in range(1, 12):
    threshold = (t + 2) * log2(3/2)
    v2_needed = int(threshold) + 1  # ceiling
    count = 0
    total = 500
    for m in range(1, 2 * total, 2):
        x = 2**(t+2) * m - 1
        fmf = 2 * (3**(t+2) * m - 1)
        v = v2(fmf)
        odd_after = fmf >> v
        if odd_after < x:
            count += 1
    print(f"{t:>3} {v2_needed:>10} {count:>10}/{total} = {count/total:>8.4f}")


# Part 5: Key question - for m where 1-hop fails, what happens in the chain?
# The odd_after lands in some residue class. What's its mod-4 classification?
print(f"\n\n=== After FMF: odd_after mod 4 classification ===")
for t in range(1, 6):
    counts = {1: 0, 3: 0}
    no_descent_count = 0
    for m in range(1, 200, 2):
        x = 2**(t+2) * m - 1
        fmf = 2 * (3**(t+2) * m - 1)
        v = v2(fmf)
        odd_after = fmf >> v
        if odd_after >= x:
            no_descent_count += 1
            counts[odd_after % 4] += 1
    total = counts[1] + counts[3]
    if total > 0:
        print(f"t={t}: no-descent cases: {no_descent_count}. "
              f"odd_after mod 4: 1 -> {counts[1]} ({counts[1]/total*100:.1f}%), "
              f"3 -> {counts[3]} ({counts[3]/total*100:.1f}%)")
