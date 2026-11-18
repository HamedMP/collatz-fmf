# -E litmus: the 3n-1 system a'(w)=(9w-1)/8 on w=1 mod 8, b'(w)=27w/16 on 16|w has E' = -E; fibres identical.
from collections import Counter
E = {0: [0], 1: [0, 1], 2: [0, 1], 3: [0, 1]}
Ep = {0: [0], 1: [0, 1], 2: [0, 3], 3: [0, 7]}
for k in range(4, 31):
    m = 1 << k
    E[k] = [((8 * z + 1) * pow(9, -1, m)) % m for z in E[k - 3]] + [(16 * z * pow(27, -1, m)) % m for z in E[k - 4]]
    Ep[k] = [((8 * z - 1) * pow(9, -1, m)) % m for z in Ep[k - 3]] + [(16 * z * pow(27, -1, m)) % m for z in Ep[k - 4]]
    assert set(E[k]) == {(-c) % m for c in Ep[k]}
N = [len(E[k]) for k in range(31)]
for k in range(31):
    for n in range(k + 1):
        assert max(Counter(c % (1 << n) for c in E[k]).values()) <= 2 * N[k - n]
    assert 0 in E[k] and 1 % (1 << k) in E[k]      # two infinite points: nothing can assert emptiness
print("-E: E'_k = -E_k (k<=30), Lemma 6 holds, 0 and 1 in every E'_k")
