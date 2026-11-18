"""Search for long orbits of the single-coordinate W-map on ALL positive z:
     z -> 27z/16 (z = 0 mod 16),   z -> (9z+1)/8 (z = 7 mod 8).
Both branches are strictly increasing on z >= 1, so there are no cycles; the
question is only whether an infinite orbit exists.  Prints the record orbit
lengths over 1 <= z <= B, overall and inside the H1 class z = 10 (mod 11),
and the number of z with orbit length >= L (to compare with (3/16)^L * B).

usage: wsearch.py [B]      (default 10^9; exact: python ints re-check the records)
"""
import sys
import numpy as np
from numba import njit

B = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9


@njit(cache=True)
def scan(B, hist, rec, rec11):
    best = 0
    best11 = 0
    LIM = 1 << 57
    for z0 in range(1, B + 1):
        r = z0 & 15
        if r != 0 and (r & 7) != 7:
            continue
        z = z0
        n = 0
        while True:
            if z >= LIM:
                n = -1
                break
            if (z & 15) == 0:
                z = 27 * (z >> 4)
            elif (z & 7) == 7:
                z = (9 * z + 1) >> 3
            else:
                break
            n += 1
        if n < 0:
            return z0          # overflow guard hit: report
        hist[n] += 1
        if n > best:
            best = n
            rec[n] = z0
        if z0 % 11 == 10 and n > best11:
            best11 = n
            rec11[n] = z0
    return 0


def exact_len(z):
    n = 0
    while True:
        if z % 16 == 0:
            z = 27 * z // 16
        elif z % 8 == 7:
            z = (9 * z + 1) // 8
        else:
            return n
        n += 1


hist = np.zeros(200, dtype=np.int64)
rec = np.zeros(200, dtype=np.int64)
rec11 = np.zeros(200, dtype=np.int64)
ov = scan(B, hist, rec, rec11)
print('B =', B, ' overflow-guard start (0 = none):', ov)
print('records, all z      :', [(L, int(z)) for L, z in enumerate(rec) if z])
print('records, z=10 mod 11:', [(L, int(z)) for L, z in enumerate(rec11) if z])
for L, z in list(enumerate(rec)) + list(enumerate(rec11)):
    if z:
        assert exact_len(int(z)) == L
tot = 0
print('L : #z<=B with orbit length >= L : (3/16)^L * B')
for L in range(199, 0, -1):
    tot += int(hist[L])
    if tot:
        print('%2d : %12d : %14.1f' % (L, tot, (3 / 16) ** L * B))
