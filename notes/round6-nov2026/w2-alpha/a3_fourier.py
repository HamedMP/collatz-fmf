"""2-adic Fourier transform of the natural self-similar measure mu_E at LOW (real-small) frequencies h/2^n.
mu_E-hat(h/2^n) = sum over level-n leaves u of x^{Q_u} e(h r_u / 2^n), x^3+x^4=1 (exact identity; floats only in the sum).
Also checks the hull statement: residues 27^{-k} e mod 2^m cover all classes = 5,7 mod 8 (exact)."""
import sys, math, cmath
import numpy as np
from a1_core import leaves
name = sys.argv[1]
x = 0.8191725133961643; s = -math.log2(x)
print("n   |E_n|   sqrt-cancel 2^(-sn/2)   |muhat(h/2^n)| for h=1,3,5,11,2^(n//2)+1")
for n in range(16, 61, 4):
    lv = list(leaves(n, name))
    r = np.array([float(l[0] % (1 << n)) / float(1 << n) for l in lv])   # r/2^n in [0,1): exact to 53 bits (enough for small h)
    wt = np.array([x ** l[1] for l in lv])
    assert abs(wt.sum() - 1) < 1e-9
    out = []
    for h in (1, 3, 5, 11):
        out.append(abs((wt * np.exp(2j * np.pi * h * r)).sum()))
    # generic high frequency, exact reduction of h*r mod 2^n
    h = (1 << (n // 2)) + 1
    ph = np.array([float((h * l[0]) % (1 << n)) / float(1 << n) for l in lv])
    out.append(abs((wt * np.exp(2j * np.pi * ph)).sum()))
    print(f"{n:3d} {len(lv):8d} {2**(-s*n/2):10.5f}   " + "  ".join(f"{v:.5f}" for v in out))
# hull check
for m in (6, 10, 14):
    got = set(); e = 7; inv = pow(27, -1, 1 << m)
    for k in range(1 << m):
        got.add(e % (1 << m)); e = e * inv % (1 << m)
    want = set(v for v in range(1 << m) if v % 8 in (5, 7))
    print(f"hull check m={m}: orbit of 7 under 27^-1 mod 2^m == {{5,7 mod 8}}: {got == want}")
for m in (3, 5, 7):
    got = set(); e = 8; inv = pow(16, -1, 3 ** m)
    for k in range(3 ** m):
        got.add(e); e = e * inv % 3 ** m
    print(f"hull check 3-adic m={m}: orbit of 8 under 16^-1 mod 3^m == {{2 mod 3}}: {got == set(v for v in range(3**m) if v % 3 == 2)}")
