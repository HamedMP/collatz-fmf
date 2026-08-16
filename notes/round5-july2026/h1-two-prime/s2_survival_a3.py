"""s2_survival_a3.py — survival census of the binary return map T (a=3).

For every seed M in [1, LIMIT]: iterate T until it dies; record
  L(M)   = number of completed return blocks (survival depth),
  kill   = K1 (v_2(33n+32) not == 0 mod 4)  or  K2 (odd part w in wrong class mod 8),
  POS    = positivity violation count (proved impossible; assert),
  P3     = 3-adic mirror violation count (v_3(88 n_{j+1}+85) != 3 r_j + 1; proved impossible; assert).
Also: mu_L = min seed with L(M) >= L; per-step kill split vs heuristic K1:K2 = 7:6 of kills
(P(K1)=7/15, P(K2)=6/15, survive 2/15 per step); histogram of L vs geometric(2/15).
"""
import sys
from collections import Counter

def v2(x):
    return (x & -x).bit_length() - 1

def v3(x):
    v = 0
    while x % 3 == 0:
        x //= 3
        v += 1
    return v

LIMIT = 10**6

hist = Counter()
kills = Counter()
mu = {}
maxL, argmax = -1, None
step_events = Counter()   # per-step outcome census over all visited states
pos_viol = 0
p3_viol = 0

for M in range(1, LIMIT + 1):
    n = M
    L = 0
    while True:
        x = 33 * n + 32
        t = v2(x)
        if t % 4 != 0:
            kills['K1'] += 1
            step_events['K1'] += 1
            break
        r = t // 4
        w = x >> t
        if w % 8 != (7 if r % 2 == 0 else 5):
            kills['K2'] += 1
            step_events['K2'] += 1
            break
        step_events['OK'] += 1
        n2 = (3 * 27**r * w - 85) // 88
        if n2 <= 0:
            pos_viol += 1
            break
        if v3(88 * n2 + 85) != 3 * r + 1:
            p3_viol += 1
            break
        n = n2
        L += 1
    hist[L] += 1
    if L not in mu:
        mu[L] = M
    if L > maxL:
        maxL, argmax = L, M

assert pos_viol == 0, "positivity kill observed (should be impossible)"
assert p3_viol == 0, "3-adic mirror violation observed (should be impossible)"

print(f"a=3 census, seeds 1..{LIMIT}")
print(f"  positivity violations: {pos_viol}   3-adic mirror violations: {p3_viol}")
tot = sum(hist.values())
print("  survival-depth histogram L : count : empirical P(L>=.) vs (2/15)^L")
cum = tot
for L in sorted(hist):
    print(f"    L={L:2d}  {hist[L]:8d}   P(>= {L}) = {cum/tot:.6g}   (2/15)^{L} = {(2/15)**L:.6g}")
    cum -= hist[L]
print("  kill mechanisms (first kill per orbit):", dict(kills))
k1, k2 = kills['K1'], kills['K2']
print(f"    K1:K2 = {k1/(k1+k2):.5f} : {k2/(k1+k2):.5f}   heuristic 7/13:6/13 = {7/13:.5f} : {6/13:.5f}")
se = step_events
tots = sum(se.values())
print(f"  per-step events over {tots} steps: OK {se['OK']/tots:.5f} (2/15={2/15:.5f}), "
      f"K1 {se['K1']/tots:.5f} (7/15={7/15:.5f}), K2 {se['K2']/tots:.5f} (6/15={6/15:.5f})")
print("  mu_L (min seed surviving >= L blocks):")
best = None
for L in sorted(mu):
    # mu_L = min seed with depth >= L = min over depths >= L
    pass
# recompute properly: mu_L = min{M : L(M) >= L}
depth_min = {}
for L in sorted(hist):
    pass
# second pass for exact mu_L
mu_ge = {}
for M in range(1, LIMIT + 1):
    pass
# cheaper: from mu dict (first M achieving exactly L) we can't get >= directly; redo scan storing firsts
firsts = {}
for M in range(1, LIMIT + 1):
    n = M
    L = 0
    alive = True
    while alive:
        x = 33 * n + 32
        t = v2(x)
        if t % 4 != 0:
            break
        r = t // 4
        w = x >> t
        if w % 8 != (7 if r % 2 == 0 else 5):
            break
        n = (3 * 27**r * w - 85) // 88
        L += 1
        if L not in firsts:
            firsts[L] = M
print("    " + ", ".join(f"mu_{L}={firsts[L]}" for L in sorted(firsts)))
print(f"  max depth: L={maxL} at M={argmax}")

# trace the champion orbit with its word and the mirror data
n = argmax
word = []
states = [n]
while True:
    x = 33*n + 32
    t = v2(x)
    if t % 4 != 0:
        break
    r = t // 4
    w = x >> t
    if w % 8 != (7 if r % 2 == 0 else 5):
        break
    n = (3 * 27**r * w - 85) // 88
    word.append(r)
    states.append(n)
print(f"  champion orbit M={argmax}: word={word}")
print(f"    states={states}")
