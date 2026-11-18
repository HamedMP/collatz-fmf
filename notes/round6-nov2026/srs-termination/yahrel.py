"""Numerical companion to REPORT.md Prop. C3 (relation of the growth-B system G
to the Yolcu-Aaronson-Heule systems).  Checks for all odd 3 <= x <= N:
 (1) every G-step is a composition of steps of YAH's S_2 = S minus {tfO -> O}:
       x = 7 mod 8  : (3x+1)/2                    [S rule  tO -> 2O]
       x = 11 mod 16: (3x+1)/2 then (3y+1)/4, y = 1 mod 8   [tO -> 2O, ffO -> 0O]
 (2) along a real growth-B hop no Collatz iterate (odd or even) from x up to
     but excluding F(x) is = 5 (mod 8); F(x) itself is not 5 (mod 8) whenever it
     is Type B (= 3 mod 4), which is the case at every hop of an infinite chain.
usage: yahrel.py [N]
"""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
hops = 0
for x in range(3, N + 1, 2):
    if x % 8 == 7:
        assert x % 4 == 3
    if x % 16 == 11:
        y = (3 * x + 1) // 2
        assert y % 8 == 1 and (3 * y + 1) // 4 == (9 * x + 5) // 8
    if x % 4 != 3:
        continue
    # real hop
    seq = [x]
    y = 3 * x + 1
    seq.append(y)
    while y % 4:
        y = y // 2 if y % 2 == 0 else 3 * y + 1
        seq.append(y)
    v = (y & -y).bit_length() - 1
    if v != 2:
        continue
    seq.append(y // 2)
    assert all(s % 8 != 5 for s in seq), (x, seq)
    if (y // 4) % 4 == 3:
        assert (y // 4) % 8 != 5
    hops += 1
print('yahrel: OK for all odd x <= %d (%d growth-B hops; none passes through 5 mod 8)' % (N, hops))
