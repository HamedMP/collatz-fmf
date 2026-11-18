#!/usr/bin/env python3
"""w4-E e4: hop letters (s = run of odd steps, v-1 = following run of even steps) on the 5n+1 orbit of 7.
Run: taskset -c 4 python e4_letters.py"""
from collections import Counter
x = 7; K = 20000; par = []
for k in range(K):
    par.append(x & 1); x = (5 * x + 1) // 2 if x & 1 else x // 2
i = 0; letters = []
while i < K and par[i] == 0: i += 1
while i < K:
    s = 0
    while i < K and par[i] == 1: s += 1; i += 1
    z = 0
    while i < K and par[i] == 0: z += 1; i += 1
    if i < K: letters.append((s, z + 1))
c = Counter(letters); n = len(letters)
g01 = c[(2, 2)] + c[(3, 2)]
print("hops: %d ; letters in G01={(2,2),(3,2)}: %d (%.4f) ; random-model value 1/8+1/16 = 0.1875" % (n, g01, g01 / n))
print("last index with a non-G01 letter: %d of %d" % (max(j for j, l in enumerate(letters) if l not in ((2, 2), (3, 2))), n))
print("most common:", c.most_common(8))
