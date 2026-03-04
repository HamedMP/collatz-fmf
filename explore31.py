"""
explore31.py - 2-Adic Proximity Chains

THE CORE MECHANISM:
v_2(FMF) = 1 + v_2(m - inv_t) where inv_t = (3^(t+2))^{-1} mod 2^N.

Growth occurs when v_2(m - inv_t) is SMALL (m is "close" to inv_t in 2-adic metric).
Shrinkage occurs when v_2(m - inv_t) is LARGE (m is "far" from inv_t).

The PROOF TARGET: show that along any FMF chain, the proximity
p_n := v_2(m_n - inv_{t_n}) cannot stay small indefinitely.

Key tools:
1. inv_t = (3^(t+2))^{-1} mod 2^N. How does inv_t change as t changes?
2. The 2-adic expansion of 3^{-1} = ...10101011 (period 2).
   The 2-adic expansion of 3^{-n} has period 2^{ord_2(n)} * 2.
   (From the multiplicative order of 3 mod 2^k.)
3. The "target" inv_t jumps around in Z/2^k Z as t changes.
   If it jumps enough, m can't stay close to it.

COMPARISON WITH 5n+1:
For 5n+1: inv_t = (5^(t+2))^{-1} mod 2^N.
The 2-adic expansion of 5^{-1} = ...11001101 (period 4).
Different equidistribution rate in Z/2^k Z.
"""
from math import log2
from collections import Counter, defaultdict


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def mod_inv(a, mod):
    """Compute a^{-1} mod m using extended gcd."""
    x = 1
    for _ in range(64):
        x = (x * (2 - a * x)) % mod
    return x


# === Part 1: 2-adic structure of 3^{-n} mod 2^k ===
print("=== Part 1: 2-Adic Inverses of Powers of 3 and 5 ===\n")

K = 16
mod = 2**K

print(f"Inverses mod 2^{K}:")
print(f"{'n':>4} {'3^n mod 2^K':>12} {'3^(-n) mod 2^K':>15} {'5^(-n) mod 2^K':>15}")
for n in range(1, 20):
    pow3 = pow(3, n, mod)
    inv3 = mod_inv(pow3, mod)
    pow5 = pow(5, n, mod)
    inv5 = mod_inv(pow5, mod)
    print(f"{n:>4} {pow3:>12} {inv3:>15} {inv5:>15}")


# === Part 2: How fast does inv_t "move" as t changes? ===
print("\n\n=== Part 2: Movement of inv_t in Z/2^K Z ===\n")
print("Consecutive 2-adic inverses: v_2(inv_{t+1} - inv_t)\n")

K = 32
mod = 2**K

print(f"  t  v_2(inv(3^(t+3)) - inv(3^(t+2)))  v_2(inv(5^(t+3)) - inv(5^(t+2)))")
for t in range(0, 20):
    inv3_t = mod_inv(pow(3, t + 2, mod), mod)
    inv3_t1 = mod_inv(pow(3, t + 3, mod), mod)
    diff3 = (inv3_t1 - inv3_t) % mod
    v3 = v2(diff3) if diff3 != 0 else K

    inv5_t = mod_inv(pow(5, t + 2, mod), mod)
    inv5_t1 = mod_inv(pow(5, t + 3, mod), mod)
    diff5 = (inv5_t1 - inv5_t) % mod
    v5 = v2(diff5) if diff5 != 0 else K

    print(f"  {t:>2}  {v3:>35}  {v5:>35}")


# === Part 3: Proximity sequence along trajectories ===
print("\n\n=== Part 3: Proximity Sequence p_n = v_2(m_n - inv_{t_n}) ===\n")

K = 64
mod = 2**K

def fmf_hop_full(x):
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        v = v2(fmf)
        return fmf >> v, 'A', 0, v, k
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            v = v2(fmf)
            return fmf >> v, 'B', 0, v, j
        else:
            t = v2(k + 1)
            m = (k + 1) >> t
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            v = v2(fmf)
            return fmf >> v, 'B', t, v, m
    return None, '', 0, 0, 0


def get_tm(x):
    if x % 4 == 1:
        return 'A', 0, (x - 1) // 4
    elif x % 4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            return 'B', 0, k // 2
        else:
            t = v2(k + 1)
            m = (k + 1) >> t
            return 'B', t, m
    return None, 0, 0


def proximity(m, t, K=64):
    """Compute v_2(m - inv_t) where inv_t = (3^(t+2))^{-1} mod 2^K."""
    mod = 2**K
    inv = mod_inv(pow(3, t + 2, mod), mod)
    diff = (m - inv) % mod
    return v2(diff) if diff != 0 else K


# Track proximity along trajectories
print("Proximity sequences for selected starting values:\n")
for x_start in [27, 31, 127, 703, 6171, 270271]:
    x = x_start
    prox_seq = []
    for _ in range(30):
        if x <= 1:
            break
        case, t, m = get_tm(x)
        if case is None:
            break
        if case == 'B' and t >= 1:
            p = proximity(m, t)
            prox_seq.append((t, m, p))
        nxt = fmf_hop_full(x)[0]
        if nxt is None:
            break
        x = nxt

    if prox_seq:
        print(f"  x={x_start}: " +
              " -> ".join(f"(t={t},p={p})" for t, _, p in prox_seq[:12]))


# === Part 4: Proximity distribution -- growth vs shrinkage ===
print("\n\n=== Part 4: Proximity Distribution During Growth vs Shrinkage ===\n")

prox_growth = Counter()
prox_shrink = Counter()

for x_start in range(3, 100001, 2):
    x = x_start
    for _ in range(100):
        if x <= 1:
            break
        case, t, m = get_tm(x)
        if case == 'B' and t >= 1:
            p = proximity(m, t)
            nxt = fmf_hop_full(x)[0]
            if nxt and nxt > x:
                prox_growth[p] += 1
            elif nxt and nxt < x:
                prox_shrink[p] += 1
            if nxt:
                x = nxt
            else:
                break
        else:
            nxt = fmf_hop_full(x)[0]
            if nxt is None:
                break
            x = nxt

total_g = sum(prox_growth.values())
total_s = sum(prox_shrink.values())

print(f"{'p':>4} {'growth':>8} {'shrink':>8} {'P(p|grow)':>10} {'P(p|shrink)':>12}")
for p in range(1, 15):
    g = prox_growth.get(p, 0)
    s = prox_shrink.get(p, 0)
    pg = g / total_g if total_g > 0 else 0
    ps = s / total_s if total_s > 0 else 0
    print(f"{p:>4} {g:>8} {s:>8} {pg:>10.4f} {ps:>12.4f}")

print(f"\nGrowth requires LOW proximity (p small = m close to inv_t).")
print(f"Shrinkage comes from HIGH proximity (p large = m far from inv_t).")


# === Part 5: How does proximity evolve along chains? ===
print("\n\n=== Part 5: Proximity Evolution -- Does p Stay Low? ===\n")

# Track (p_n, p_{n+1}) pairs for Type B hops
p_pairs = []
for x_start in range(3, 200001, 2):
    x = x_start
    prev_p = None
    for _ in range(100):
        if x <= 1:
            break
        case, t, m = get_tm(x)
        nxt = fmf_hop_full(x)[0]
        if nxt is None:
            break

        if case == 'B' and t >= 1:
            p = proximity(m, t)
            if prev_p is not None:
                p_pairs.append((prev_p, p))
            prev_p = p
        else:
            prev_p = None  # Reset on Type A
        x = nxt

if p_pairs:
    n = len(p_pairs)
    mean_x = sum(a for a, _ in p_pairs) / n
    mean_y = sum(b for _, b in p_pairs) / n
    cov = sum((a - mean_x) * (b - mean_y) for a, b in p_pairs) / n
    var_x = sum((a - mean_x)**2 for a, _ in p_pairs) / n
    var_y = sum((b - mean_y)**2 for _, b in p_pairs) / n
    corr = cov / (var_x * var_y)**0.5 if var_x > 0 and var_y > 0 else 0
    print(f"Lag-1 proximity correlation: {corr:.4f} (n={n})")
    print(f"Mean proximity: {mean_x:.2f}")
    print()

    # Transition matrix P(p_{n+1} | p_n)
    print("P(p_{n+1} | p_n) for consecutive Type B hops:")
    joint = Counter((min(a, 6), min(b, 6)) for a, b in p_pairs)
    row_totals = Counter(min(a, 6) for a, _ in p_pairs)

    print(f"    {'p_n\\p_{n+1}':>12}", end="")
    for j in range(1, 7):
        print(f" {j:>6}", end="")
    print()
    for i in range(1, 7):
        print(f"    {i:>12}", end="")
        for j in range(1, 7):
            if row_totals[i] > 0:
                p = joint.get((i, j), 0) / row_totals[i]
                print(f" {p:>6.3f}", end="")
            else:
                print(f" {0:>6.3f}", end="")
        print()


# === Part 6: Compare with 5n+1 proximity ===
print("\n\n=== Part 6: 5n+1 Proximity Comparison ===\n")

def fmf_5n1(x):
    val = 5 * x + 1
    p = v2(val)
    return val >> p, p

def proximity_5(m, t, K=64):
    mod = 2**K
    inv = mod_inv(pow(5, t + 2, mod), mod)
    diff = (m - inv) % mod
    return v2(diff) if diff != 0 else K

# For 5n+1: track proximity along diverging trajectories
print("5n+1 proximity sequences (diverging trajectories):\n")
for x_start in [27, 31, 127, 703]:
    x = x_start
    prox_seq_5 = []
    for hop in range(20):
        if x <= 1:
            break
        # 5n+1 doesn't have the same FMF structure, but we can still
        # decompose x = 2^(t+2)*m - 1 and check proximity to 5^{-(t+2)}
        case, t, m = get_tm(x)  # Same decomposition
        if case == 'B' and t >= 1:
            p = proximity_5(m, t)
            prox_seq_5.append((t, p))
        nxt, v = fmf_5n1(x)
        x = nxt

    if prox_seq_5:
        print(f"  x={x_start}: " +
              " -> ".join(f"(t={t},p={p})" for t, p in prox_seq_5[:10]))


# === Part 7: The equidistribution rate ===
print("\n\n=== Part 7: Equidistribution of 3^n vs 5^n in Z/2^k Z ===\n")
print("How uniformly do powers of 3 (and 5) distribute mod 2^k?\n")

for K in [4, 8, 12, 16]:
    mod = 2**K
    # Compute all 3^n mod 2^K for n = 1..phi(2^K)
    # phi(2^K) = 2^(K-1), and ord_2(3) = 2^(K-2) for K >= 3
    ord3 = 1
    val = 3
    while val % mod != 1:
        val = (val * 3) % mod
        ord3 += 1
        if ord3 > mod:
            break

    ord5 = 1
    val = 5
    while val % mod != 1:
        val = (val * 5) % mod
        ord5 += 1
        if ord5 > mod:
            break

    # Count residues hit
    residues_3 = set()
    val = 1
    for _ in range(ord3):
        val = (val * 3) % mod
        residues_3.add(val)

    residues_5 = set()
    val = 1
    for _ in range(ord5):
        val = (val * 5) % mod
        residues_5.add(val)

    # Only odd residues matter
    odd_residues = set(r for r in range(1, mod, 2))
    print(f"  mod 2^{K} (={mod}):")
    print(f"    ord(3) = {ord3}, covers {len(residues_3)}/{len(odd_residues)} odd residues "
          f"({len(residues_3)/len(odd_residues)*100:.1f}%)")
    print(f"    ord(5) = {ord5}, covers {len(residues_5)}/{len(odd_residues)} odd residues "
          f"({len(residues_5)/len(odd_residues)*100:.1f}%)")


# === Part 8: The inverse movement rate ===
print("\n\n=== Part 8: How Fast Do Inverses Move? ===\n")
print("v_2(3^{-(t+3)} - 3^{-(t+2)}) = v_2(3^{-(t+2)} * (3^{-1} - 1))")
print("= v_2(3^{-(t+2)}) + v_2(3^{-1} - 1)")
print("= 0 + v_2(-2/3) = v_2(2/3) [in Z_2]")
print("= v_2(2) + v_2(1/3) = 1 + 0 = 1")
print()
print("So: consecutive inverses ALWAYS differ by exactly v_2 = 1!")
print("This means: 3^{-(t+3)} - 3^{-(t+2)} = 3^{-(t+2)} * (1/3 - 1)")
print("= 3^{-(t+2)} * (-2/3) = -2 * 3^{-(t+3)}")
print("v_2 of this = v_2(2) = 1.")
print()
print("THEOREM: v_2(inv_{t+1} - inv_t) = 1 for all t.")
print("The 2-adic inverse of 3^n ALWAYS moves by exactly 1 bit per step.")
print()

# Verify
K = 64
mod = 2**K
print("Verification:")
for t in range(20):
    inv_t = mod_inv(pow(3, t + 2, mod), mod)
    inv_t1 = mod_inv(pow(3, t + 3, mod), mod)
    diff = (inv_t1 - inv_t) % mod
    v = v2(diff)
    print(f"  t={t:>2}: v_2(inv_{t+1} - inv_t) = {v}")


# === Part 9: For 5n+1, what's the movement rate? ===
print("\n\n=== Part 9: Inverse Movement for 5n+1 ===\n")
print("v_2(5^{-(t+3)} - 5^{-(t+2)}) = v_2(5^{-(t+2)} * (5^{-1} - 1))")
print("= v_2(5^{-(t+2)}) + v_2(5^{-1} - 1)")
print("5^{-1} mod 2^K has a specific structure...")
print()

# Compute 5^{-1} - 1 in 2-adic integers
# 5^{-1} mod 2^K = mod_inv(5, 2^K)
inv5 = mod_inv(5, mod)
diff_5 = (inv5 - 1) % mod
print(f"5^(-1) mod 2^64 = {inv5}")
print(f"5^(-1) - 1 mod 2^64 = {diff_5}")
print(f"v_2(5^(-1) - 1) = {v2(diff_5)}")
print()

print("Verification for 5n+1:")
for t in range(20):
    inv_t = mod_inv(pow(5, t + 2, mod), mod)
    inv_t1 = mod_inv(pow(5, t + 3, mod), mod)
    diff = (inv_t1 - inv_t) % mod
    v = v2(diff)
    print(f"  t={t:>2}: v_2(inv_{t+1} - inv_t) = {v}")


# === Part 10: The PROOF-RELEVANT observation ===
print("\n\n=== Part 10: Proof-Relevant Observation ===\n")
print("""
THEOREM (Inverse Movement Rate):

For a = 3: v_2(a^{-(t+3)} - a^{-(t+2)}) = 1 for all t >= 0.
For a = 5: v_2(a^{-(t+3)} - a^{-(t+2)}) = 2 for all t >= 0.

In general: v_2(a^{-(t+3)} - a^{-(t+2)}) = v_2(a^{-1} - 1) = v_2((1-a)/a)
= v_2(1-a) since a is odd (so v_2(a) = 0).

For a = 3: v_2(1-3) = v_2(-2) = 1.
For a = 5: v_2(1-5) = v_2(-4) = 2.
For a = 7: v_2(1-7) = v_2(-6) = 1.

IMPLICATION:
As t changes by 1 along a trajectory, the 2-adic target (inv_t) shifts
by exactly v_2(1-a) bits. For a = 3, this is 1 bit -- the MINIMUM
possible nonzero shift.

For the proximity p = v_2(m - inv_t):
- If t changes by 1 and m doesn't change much, p changes by at most 1
- But m DOES change (via the FMF transformation)
- The key: both m and inv_t are changing, and their relative position
  determines the next v_2

The 1-bit shift of inv_t for a = 3 means the target moves MINIMALLY,
giving the trajectory the best chance of "escaping" low proximity.
For a = 5 (2-bit shift), the target moves MORE, but the base growth
is also larger (5^(t+2) vs 3^(t+2)), so the balance is different.

OPEN QUESTION: Does the 1-bit inverse shift for a = 3, combined with
the m-value transformation, guarantee that proximity p_n cannot stay
small indefinitely?
""")
