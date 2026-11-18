#!/usr/bin/env python3
"""w2-delta s8: exact check of the identity behind the 'second generation' lead (Lemma G2).
For a parity vector v of length L with a ones, r_v = sum_i 3^(a-1-i) 2^(d_i), let y_v be the unique integer in
[2^L, 2^(L+1)) with that vector.  Then  T^L(y_v) = 3^a + tau_v,  tau_v = T^L(y_v - 2^L),
tau_v == r_v * 2^(-L) (mod 3^a) and 0 <= tau_v < 3^a + (3/2)^a, i.e. tau_v is the least residue of the Syracuse-type
value r_v/2^L mod 3^a (or that residue + 3^a when it is < (3/2)^a).
Run: taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python s8_syracuse_identity.py
"""
def T(x): return x // 2 if x % 2 == 0 else (3 * x + 1) // 2
cnt = 0; plus = 0
for L in range(1, 17):
    for y in range(2**L, 2**(L + 1)):
        x = y; a = 0; r = 0
        for j in range(L):
            if x & 1: r = 3 * r + 2**j; a += 1
            x = T(x)
        z = x
        rho = y - 2**L; t = rho
        for j in range(L): t = T(t)
        assert z * 2**L == 3**a * y + r
        assert z == 3**a + t
        res = (r * pow(2, -L, 3**a)) % 3**a if a > 0 else 0
        assert t in (res, res + 3**a) and t * 2**a < (3**a * 2**a + 3**a)
        plus += (t != res); cnt += 1
print("identity T^L(y_v) = 3^a + (r_v 2^-L mod 3^a) [+3^a in %d cases]: %d exact instances OK" % (plus, cnt))
